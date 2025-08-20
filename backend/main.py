from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import json
import logging
from typing import List, Dict, Optional
import redis
from datetime import datetime, timedelta
import os

from database import engine, SessionLocal, Base
from models import User, Order, PaymentQRCode, UsageRecord
from auth import get_current_user, create_access_token, verify_password, get_password_hash
from exchange_manager import ExchangeDataManager
from prediction_service import PredictionService
from payment_service import PaymentService
from rate_limiter import RateLimitMiddleware, check_rate_limit
from schemas import (
    UserRegister, UserLogin, PredictionRequest, OrderCreate,
    TokenResponse, PredictionResponse, APIResponse, UserResponse
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="永续合约预测系统",
    version="1.0.0",
    description="基于AI的加密货币永续合约价格预测系统",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加速率限制中间件
app.add_middleware(RateLimitMiddleware)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Redis连接
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 全局服务实例
exchange_manager = ExchangeDataManager()
prediction_service = PredictionService()
payment_service = PaymentService()

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        # 检查数据库连接
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        logging.error(f"Database health check failed: {e}")
        db_status = "unhealthy"

    # 检查Redis连接
    try:
        redis_client.ping()
        redis_status = "healthy"
    except Exception as e:
        logging.error(f"Redis health check failed: {e}")
        redis_status = "unhealthy"

    # 检查服务状态
    services_status = {
        "exchange_manager": "healthy" if exchange_manager else "unhealthy",
        "prediction_service": "healthy" if prediction_service else "unhealthy",
        "payment_service": "healthy" if payment_service else "unhealthy"
    }

    overall_status = "healthy" if all([
        db_status == "healthy",
        redis_status == "healthy",
        all(status == "healthy" for status in services_status.values())
    ]) else "unhealthy"

    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": db_status,
            "redis": redis_status,
            **services_status
        },
        "version": "1.0.0"
    }

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info(f"Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logging.info(f"Client disconnected. Total: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except:
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    logging.basicConfig(level=logging.INFO)

    # 启动交易所数据管理器
    asyncio.create_task(exchange_manager.start_all_connections())

    # 启动数据广播任务
    asyncio.create_task(broadcast_market_data())

async def broadcast_market_data():
    """广播市场数据给所有WebSocket客户端"""
    while True:
        try:
            # 获取最新市场数据
            market_data = exchange_manager.get_latest_market_data()
            if market_data and manager.active_connections:
                message = {
                    "type": "market_update",
                    "data": market_data,
                    "timestamp": datetime.now().isoformat()
                }
                await manager.broadcast(json.dumps(message))

            await asyncio.sleep(1)  # 每秒广播一次
        except Exception as e:
            logging.error(f"Broadcast error: {e}")
            await asyncio.sleep(5)

# 依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# WebSocket端点
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # 发送初始数据
        initial_data = {
            "type": "initial_data",
            "data": exchange_manager.get_latest_market_data(),
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(initial_data))

        # 保持连接
        while True:
            data = await websocket.receive_text()
            # 处理客户端消息
            try:
                message = json.loads(data)
                if message.get("type") == "subscribe":
                    # 处理订阅请求
                    pass
            except:
                pass

    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 用户认证相关API
@app.post("/api/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegister, request: Request, db = Depends(get_db)):
    """用户注册"""
    # 速率限制检查
    check_rate_limit(request, "auth/register")

    try:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="邮箱已被注册")

        # 检查用户名是否已存在
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="用户名已被使用")

        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hashed_password,
            membership_level="trial",
            trial_start_time=datetime.now()
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # 生成访问令牌
        access_token = create_access_token(data={"sub": user.email})

        # 创建用户响应对象
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            membership_level=user.membership_level,
            created_at=user.created_at
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"用户注册失败: {e}")
        raise HTTPException(status_code=500, detail="注册失败，请稍后重试")

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(login_data: UserLogin, request: Request, db = Depends(get_db)):
    """用户登录"""
    # 速率限制检查
    check_rate_limit(request, "auth/login")

    try:
        user = db.query(User).filter(User.email == login_data.email).first()

        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="邮箱或密码错误")

        access_token = create_access_token(data={"sub": user.email})

        # 创建用户响应对象
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            membership_level=user.membership_level,
            created_at=user.created_at
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"用户登录失败: {e}")
        raise HTTPException(status_code=500, detail="登录失败，请稍后重试")

# 市场数据API
@app.get("/api/market/data/{symbol}")
async def get_market_data(symbol: str):
    """获取指定交易对的市场数据"""
    data = exchange_manager.get_symbol_data(symbol)
    return {"success": True, "data": data}

@app.get("/api/market/aggregated/{symbol}")
async def get_aggregated_data(symbol: str):
    """获取聚合市场数据"""
    key = f"aggregated:{symbol}"
    data = redis_client.get(key)
    if data:
        return {"success": True, "data": json.loads(data)}
    return {"success": False, "message": "数据不可用"}

# 预测相关API
@app.post("/api/prediction/predict", response_model=PredictionResponse)
async def make_prediction(
    prediction_data: PredictionRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """进行价格预测"""
    # 速率限制检查
    check_rate_limit(request, "prediction/predict")

    try:
        # 检查用户配额
        quota_check = check_user_quota(current_user, db)
        if not quota_check["allowed"]:
            return PredictionResponse(
                success=False,
                predictions={},
                message=quota_check["message"],
                quota_remaining=quota_check["remaining"]
            )

        # 获取市场数据
        market_data = exchange_manager.get_symbol_data(prediction_data.symbol)
        if not market_data:
            return PredictionResponse(
                success=False,
                predictions={},
                message="市场数据暂时不可用，请稍后重试"
            )

        # 进行预测
        predictions = await prediction_service.predict(
            prediction_data.symbol,
            prediction_data.timeframes,
            market_data
        )

        # 记录使用
        record_usage(current_user.id, "prediction", db)

        # 获取剩余配额
        remaining_quota = get_remaining_quota(current_user, db)

        return PredictionResponse(
            success=True,
            predictions=predictions,
            message="预测完成",
            quota_remaining=remaining_quota
        )

    except Exception as e:
        logging.error(f"预测失败: {e}")
        return PredictionResponse(
            success=False,
            predictions={},
            message="预测服务暂时不可用，请稍后重试"
        )

def check_user_quota(user: User, db) -> Dict:
    """检查用户配额"""
    quota_limits = {
        "trial": 50,
        "basic": 200,
        "pro": 500,
        "premium": float('inf')
    }

    limit = quota_limits.get(user.membership_level, 0)

    if user.membership_level == "premium":
        return {
            "allowed": True,
            "remaining": float('inf'),
            "message": "无限制"
        }

    # 检查今日使用次数
    today = datetime.now().date()
    daily_usage = db.query(UsageRecord).filter(
        UsageRecord.user_id == user.id,
        UsageRecord.timestamp >= today
    ).count()

    remaining = max(0, limit - daily_usage)
    allowed = daily_usage < limit

    return {
        "allowed": allowed,
        "remaining": remaining,
        "message": f"今日剩余 {remaining} 次预测" if allowed else "今日预测次数已用完"
    }

def get_remaining_quota(user: User, db) -> int:
    """获取剩余配额"""
    quota_check = check_user_quota(user, db)
    return quota_check["remaining"] if isinstance(quota_check["remaining"], int) else 999999

def record_usage(user_id: int, usage_type: str, db):
    """记录使用情况"""
    usage = UsageRecord(
        user_id=user_id,
        prediction_type=usage_type,
        timestamp=datetime.now()
    )
    db.add(usage)
    db.commit()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
