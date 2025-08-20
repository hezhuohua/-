from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class MembershipLevel(enum.Enum):
    trial = "trial"
    basic = "basic"
    pro = "pro"
    premium = "premium"

class OrderStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class PaymentType(enum.Enum):
    alipay = "alipay"
    wechat = "wechat"

class QRCodeStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    membership_level = Column(Enum(MembershipLevel), default=MembershipLevel.trial)
    trial_start_time = Column(DateTime)
    trial_used_predictions = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    orders = relationship("Order", back_populates="user")
    usage_records = relationship("UsageRecord", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_type = Column(Enum(MembershipLevel), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="active")
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="subscriptions")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_no = Column(String(50), unique=True, nullable=False)
    plan_type = Column(String(20))
    amount = Column(Float, nullable=False)
    payment_method = Column(String(20))
    payment_type = Column(String(10), default="api")  # api 或 qrcode
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    qrcode_id = Column(Integer, ForeignKey("payment_qrcodes.id"))
    proof_id = Column(Integer, ForeignKey("payment_proofs.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)
    
    # 关系
    user = relationship("User", back_populates="orders")
    qrcode = relationship("PaymentQRCode")
    proof = relationship("PaymentProof")

class PaymentQRCode(Base):
    __tablename__ = "payment_qrcodes"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_type = Column(Enum(PaymentType), nullable=False)
    qrcode_url = Column(String(255), nullable=False)
    qrcode_name = Column(String(100))
    status = Column(Enum(QRCodeStatus), default=QRCodeStatus.active)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PaymentProof(Base):
    __tablename__ = "payment_proofs"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    proof_image_url = Column(String(255), nullable=False)
    payment_amount = Column(Float)
    payment_time = Column(DateTime)
    remark = Column(Text)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    reviewed_by = Column(Integer, ForeignKey("admin_users.id"))
    reviewed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    order = relationship("Order")
    reviewer = relationship("AdminUser")

class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prediction_type = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    cost = Column(Float, default=0)
    remaining_quota = Column(Integer)
    
    # 关系
    user = relationship("User", back_populates="usage_records")

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="operator")  # admin, operator
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class AdminLog(Base):
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admin_users.id"))
    action = Column(String(100), nullable=False)
    target_type = Column(String(50))
    target_id = Column(Integer)
    details = Column(Text)  # JSON格式
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    admin = relationship("AdminUser")

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    exchange = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    volume_24h = Column(Float)
    change_24h = Column(Float)
    change_percent_24h = Column(Float)
    high_24h = Column(Float)
    low_24h = Column(Float)
    funding_rate = Column(Float)
    open_interest = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class PredictionResult(Base):
    __tablename__ = "prediction_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String(20), nullable=False)
    timeframe = Column(String(10), nullable=False)
    prediction_time = Column(DateTime, default=datetime.utcnow)
    predicted_direction = Column(String(10))  # up, down
    predicted_price = Column(Float)
    confidence = Column(Float)
    actual_price = Column(Float)
    actual_direction = Column(String(10))
    is_correct = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
