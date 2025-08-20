import os
import uuid
import qrcode
from PIL import Image
from typing import Dict, Optional
import json
from datetime import datetime
from sqlalchemy.orm import Session
from models import PaymentQRCode, Order, PaymentProof, User
import logging

class PaymentService:
    def __init__(self):
        self.upload_folder = "uploads"
        self.qrcode_folder = os.path.join(self.upload_folder, "qrcodes")
        self.proof_folder = os.path.join(self.upload_folder, "proofs")
        
        # 创建上传目录
        os.makedirs(self.qrcode_folder, exist_ok=True)
        os.makedirs(self.proof_folder, exist_ok=True)
    
    def upload_qrcode(self, file_data: bytes, payment_type: str, qrcode_name: str, db: Session) -> Dict:
        """上传收款码"""
        try:
            # 生成唯一文件名
            file_ext = "png"
            filename = f"{uuid.uuid4().hex}.{file_ext}"
            filepath = os.path.join(self.qrcode_folder, filename)
            
            # 保存文件
            with open(filepath, "wb") as f:
                f.write(file_data)
            
            # 压缩图片
            self.compress_image(filepath)
            
            # 保存到数据库
            qrcode = PaymentQRCode(
                payment_type=payment_type,
                qrcode_url=f"/uploads/qrcodes/{filename}",
                qrcode_name=qrcode_name,
                status="active"
            )
            
            db.add(qrcode)
            db.commit()
            db.refresh(qrcode)
            
            return {
                'success': True,
                'qrcode_id': qrcode.id,
                'url': qrcode.qrcode_url,
                'message': '收款码上传成功'
            }
            
        except Exception as e:
            logging.error(f"Upload QR code error: {e}")
            return {'success': False, 'message': f'上传失败: {str(e)}'}
    
    def compress_image(self, filepath: str, max_size: tuple = (800, 800), quality: int = 85):
        """压缩图片"""
        try:
            with Image.open(filepath) as image:
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                
                # 限制图片大小
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                image.save(filepath, optimize=True, quality=quality)
                
        except Exception as e:
            logging.error(f"Compress image error: {e}")
    
    def get_active_qrcodes(self, payment_type: Optional[str] = None, db: Session = None) -> list:
        """获取活跃的收款码"""
        query = db.query(PaymentQRCode).filter(PaymentQRCode.status == "active")
        if payment_type:
            query = query.filter(PaymentQRCode.payment_type == payment_type)
        
        return query.order_by(PaymentQRCode.sort_order).all()
    
    def create_order(self, user_id: int, plan_type: str, amount: float, payment_method: str, db: Session) -> Dict:
        """创建订单"""
        try:
            order_no = self.generate_order_no()
            
            order = Order(
                user_id=user_id,
                order_no=order_no,
                plan_type=plan_type,
                amount=amount,
                payment_method=payment_method,
                status="pending"
            )
            
            db.add(order)
            db.commit()
            db.refresh(order)
            
            return {
                'success': True,
                'order_id': order.id,
                'order_no': order_no,
                'amount': amount,
                'message': '订单创建成功'
            }
            
        except Exception as e:
            logging.error(f"Create order error: {e}")
            return {'success': False, 'message': f'订单创建失败: {str(e)}'}
    
    def generate_order_no(self) -> str:
        """生成订单号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = str(uuid.uuid4().hex)[:8].upper()
        return f"ORD{timestamp}{random_str}"
    
    def upload_payment_proof(self, order_id: int, file_data: bytes, payment_amount: float, remark: str, db: Session) -> Dict:
        """上传支付凭证"""
        try:
            # 检查订单是否存在
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return {'success': False, 'message': '订单不存在'}
            
            # 生成文件名
            filename = f"proof_{order_id}_{uuid.uuid4().hex[:8]}.jpg"
            filepath = os.path.join(self.proof_folder, filename)
            
            # 保存文件
            with open(filepath, "wb") as f:
                f.write(file_data)
            
            # 压缩图片
            self.compress_image(filepath)
            
            # 保存到数据库
            proof = PaymentProof(
                order_id=order_id,
                proof_image_url=f"/uploads/proofs/{filename}",
                payment_amount=payment_amount,
                payment_time=datetime.now(),
                remark=remark,
                status="pending"
            )
            
            db.add(proof)
            db.commit()
            db.refresh(proof)
            
            # 更新订单
            order.proof_id = proof.id
            db.commit()
            
            return {
                'success': True,
                'proof_id': proof.id,
                'url': proof.proof_image_url,
                'message': '支付凭证上传成功'
            }
            
        except Exception as e:
            logging.error(f"Upload payment proof error: {e}")
            return {'success': False, 'message': f'上传失败: {str(e)}'}
    
    def review_order(self, order_id: int, action: str, reviewer_id: int, reason: str = "", db: Session = None) -> Dict:
        """审核订单"""
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return {'success': False, 'message': '订单不存在'}
            
            proof = db.query(PaymentProof).filter(PaymentProof.order_id == order_id).first()
            if not proof:
                return {'success': False, 'message': '支付凭证不存在'}
            
            if action == "approved":
                # 通过审核
                order.status = "paid"
                order.paid_at = datetime.now()
                proof.status = "approved"
                proof.reviewed_by = reviewer_id
                proof.reviewed_at = datetime.now()
                
                # 激活用户会员
                self.activate_membership(order.user_id, order.plan_type, db)
                
                message = "订单审核通过，会员已激活"
                
            elif action == "rejected":
                # 拒绝审核
                order.status = "failed"
                proof.status = "rejected"
                proof.reviewed_by = reviewer_id
                proof.reviewed_at = datetime.now()
                proof.remark = reason
                
                message = "订单审核被拒绝"
            
            else:
                return {'success': False, 'message': '无效的审核操作'}
            
            db.commit()
            
            return {'success': True, 'message': message}
            
        except Exception as e:
            logging.error(f"Review order error: {e}")
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def activate_membership(self, user_id: int, plan_type: str, db: Session):
        """激活用户会员"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.membership_level = plan_type
                db.commit()
                logging.info(f"User {user_id} membership activated: {plan_type}")
                
        except Exception as e:
            logging.error(f"Activate membership error: {e}")
    
    def get_orders_for_review(self, status: str = "pending", db: Session = None) -> list:
        """获取待审核订单"""
        query = db.query(Order).join(PaymentProof)
        
        if status:
            query = query.filter(PaymentProof.status == status)
        
        return query.order_by(Order.created_at.desc()).all()
    
    def get_user_orders(self, user_id: int, db: Session) -> list:
        """获取用户订单"""
        return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
    
    def get_order_status(self, order_id: int, db: Session) -> Dict:
        """获取订单状态"""
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {'success': False, 'message': '订单不存在'}
        
        return {
            'success': True,
            'data': {
                'order_id': order.id,
                'order_no': order.order_no,
                'status': order.status,
                'amount': order.amount,
                'plan_type': order.plan_type,
                'created_at': order.created_at.isoformat(),
                'paid_at': order.paid_at.isoformat() if order.paid_at else None
            }
        }
