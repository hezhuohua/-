# 性能优化修复指南

本文档提供了针对性能问题的具体修复方案和优化建议。

## 🚀 数据库性能优化

### 1. 异步数据库操作

#### 安装异步数据库驱动

```bash
pip install asyncpg databases[postgresql]
# 或者对于SQLite
pip install aiosqlite databases[sqlite]
```

#### 创建异步数据库配置: `backend/async_database.py`

```python
import databases
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./crypto_prediction.db")

# 异步数据库连接
database = databases.Database(DATABASE_URL)

# 异步引擎
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)

# 异步会话
AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

#### 修改 `backend/main.py` 使用异步数据库

**当前代码 (有问题)**:
```python
@app.post("/api/auth/register")
async def register(user_data: UserRegister, db = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
```

**修复后代码**:
```python
from async_database import get_async_db
from sqlalchemy import select

@app.post("/api/auth/register")
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_async_db)):
    # 异步查询
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 创建新用户
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        membership_level="trial",
        trial_start_time=datetime.now()
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
```

### 2. 数据库索引优化

#### 修改 `backend/models.py` 添加索引

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    membership_level = Column(Enum(MembershipLevel), default=MembershipLevel.trial, index=True)
    trial_start_time = Column(DateTime, index=True)
    trial_used_predictions = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 复合索引
    __table_args__ = (
        Index('idx_user_email_membership', 'email', 'membership_level'),
        Index('idx_user_created_membership', 'created_at', 'membership_level'),
    )

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    order_no = Column(String(50), unique=True, nullable=False, index=True)
    plan_type = Column(String(20), index=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(20))
    payment_type = Column(String(10), default="api")
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, index=True)
    qrcode_id = Column(Integer, ForeignKey("payment_qrcodes.id"))
    proof_id = Column(Integer, ForeignKey("payment_proofs.id"))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    paid_at = Column(DateTime, index=True)
    
    # 复合索引
    __table_args__ = (
        Index('idx_order_user_status', 'user_id', 'status'),
        Index('idx_order_created_status', 'created_at', 'status'),
    )
```

## 🔄 缓存优化

### 1. Redis缓存实现

#### 创建缓存服务: `backend/cache_service.py`

```python
import redis
import json
import pickle
from typing import Any, Optional
from datetime import timedelta
import os

class CacheService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = redis.from_url(redis_url, decode_responses=False)
        self.default_ttl = 3600  # 1小时
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            value = self.redis_client.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        try:
            ttl = ttl or self.default_ttl
            serialized_value = pickle.dumps(value)
            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            return bool(self.redis_client.delete(key))
        except Exception:
            return False
    
    async def get_market_data(self, symbol: str, exchange: str) -> Optional[dict]:
        """获取市场数据缓存"""
        key = f"market:{symbol}:{exchange}"
        return await self.get(key)
    
    async def set_market_data(self, symbol: str, exchange: str, data: dict, ttl: int = 60):
        """设置市场数据缓存"""
        key = f"market:{symbol}:{exchange}"
        return await self.set(key, data, ttl)
    
    async def get_prediction(self, symbol: str, exchange: str, timeframes: str) -> Optional[dict]:
        """获取预测结果缓存"""
        key = f"prediction:{symbol}:{exchange}:{timeframes}"
        return await self.get(key)
    
    async def set_prediction(self, symbol: str, exchange: str, timeframes: str, data: dict, ttl: int = 300):
        """设置预测结果缓存"""
        key = f"prediction:{symbol}:{exchange}:{timeframes}"
        return await self.set(key, data, ttl)

cache_service = CacheService()
```

#### 在预测服务中使用缓存

```python
# 修改 backend/prediction_service.py
from cache_service import cache_service

class PredictionService:
    async def predict(self, symbol: str, timeframes: List[str], market_data: Dict, exchange: str = "binance") -> Dict:
        """进行价格预测"""
        # 检查缓存
        timeframes_key = "_".join(sorted(timeframes))
        cached_result = await cache_service.get_prediction(symbol, exchange, timeframes_key)
        if cached_result:
            return cached_result
        
        predictions = {}
        
        for timeframe in timeframes:
            try:
                # ... 预测逻辑
                predictions[timeframe] = final_prediction
                
            except Exception as e:
                logging.error(f"Prediction error for {symbol} {timeframe}: {e}")
                predictions[timeframe] = {
                    "direction": "neutral",
                    "probability": 50.0,
                    "confidence": 0.3,
                    "target_price": 0.0,
                    "reasoning": "预测服务暂时不可用"
                }
        
        # 缓存结果（5分钟）
        await cache_service.set_prediction(symbol, exchange, timeframes_key, predictions, 300)
        
        return predictions
```

## 🌐 WebSocket性能优化

### 1. 连接管理优化

#### 修改 `backend/main.py` 的连接管理器

```python
import asyncio
import weakref
from typing import Dict, Set
import time

class OptimizedConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[int, Set[str]] = {}
        self.connection_timestamps: Dict[str, float] = {}
        self.max_connections_per_user = 3
        self.connection_timeout = 3600  # 1小时
    
    async def connect(self, websocket: WebSocket, user_id: Optional[int] = None):
        await websocket.accept()
        
        connection_id = f"{id(websocket)}_{time.time()}"
        
        # 检查用户连接数限制
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            
            if len(self.user_connections[user_id]) >= self.max_connections_per_user:
                # 关闭最旧的连接
                oldest_connection = min(
                    self.user_connections[user_id],
                    key=lambda x: self.connection_timestamps.get(x, 0)
                )
                await self.disconnect_by_id(oldest_connection)
            
            self.user_connections[user_id].add(connection_id)
        
        self.active_connections[connection_id] = websocket
        self.connection_timestamps[connection_id] = time.time()
        
        # 启动心跳检测
        asyncio.create_task(self.heartbeat_check(connection_id))
        
        logging.info(f"Client connected: {connection_id}. Total: {len(self.active_connections)}")
    
    async def disconnect_by_id(self, connection_id: str):
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].close()
            except:
                pass
            
            del self.active_connections[connection_id]
            del self.connection_timestamps[connection_id]
            
            # 从用户连接中移除
            for user_connections in self.user_connections.values():
                user_connections.discard(connection_id)
    
    async def heartbeat_check(self, connection_id: str):
        """心跳检测"""
        while connection_id in self.active_connections:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.send_text(json.dumps({"type": "ping"}))
                await asyncio.sleep(30)  # 30秒心跳
            except:
                await self.disconnect_by_id(connection_id)
                break
    
    async def cleanup_expired_connections(self):
        """清理过期连接"""
        current_time = time.time()
        expired_connections = [
            conn_id for conn_id, timestamp in self.connection_timestamps.items()
            if current_time - timestamp > self.connection_timeout
        ]
        
        for conn_id in expired_connections:
            await self.disconnect_by_id(conn_id)
    
    async def broadcast_to_user(self, user_id: int, message: str):
        """向特定用户的所有连接广播"""
        if user_id in self.user_connections:
            disconnected = []
            for connection_id in self.user_connections[user_id]:
                if connection_id in self.active_connections:
                    try:
                        await self.active_connections[connection_id].send_text(message)
                    except:
                        disconnected.append(connection_id)
            
            for conn_id in disconnected:
                await self.disconnect_by_id(conn_id)
```

## 📊 前端性能优化

### 1. 资源加载优化

#### 修改 `index.html` 添加资源优化

```html
<!-- 在head部分添加 -->
<head>
    <!-- 预加载关键资源 -->
    <link rel="preload" href="https://unpkg.com/vue@3/dist/vue.global.js" as="script">
    <link rel="preload" href="https://unpkg.com/axios/dist/axios.min.js" as="script">
    
    <!-- DNS预解析 -->
    <link rel="dns-prefetch" href="//unpkg.com">
    <link rel="dns-prefetch" href="//cdnjs.cloudflare.com">
    
    <!-- 关键CSS内联 -->
    <style>
        /* 关键样式内联以避免FOUC */
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        .loading { display: flex; justify-content: center; align-items: center; height: 100vh; }
    </style>
</head>
```

### 2. Vue.js性能优化

```javascript
// 在Vue应用中添加性能优化
const { createApp } = Vue;

createApp({
    // ... 现有配置
    
    // 添加性能优化
    computed: {
        // 缓存计算属性
        filteredMarketData() {
            return Object.entries(this.marketData[this.selectedSymbol] || {})
                .filter(([exchange, data]) => data.price > 0);
        }
    },
    
    watch: {
        // 防抖处理
        selectedSymbol: {
            handler: 'debouncedSymbolChange',
            immediate: false
        }
    },
    
    methods: {
        // 防抖函数
        debouncedSymbolChange: debounce(function() {
            this.changeSymbol();
        }, 300),
        
        // 虚拟滚动（如果列表很长）
        updateVisibleItems() {
            // 只渲染可见的项目
        }
    }
});

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
```

## 📋 性能监控

### 1. 添加性能监控中间件

```python
# backend/performance_middleware.py
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # 记录慢请求
        if process_time > 1.0:  # 超过1秒的请求
            logging.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"took {process_time:.2f}s"
            )
        
        return response

# 在main.py中添加
app.add_middleware(PerformanceMiddleware)
```

## 🧪 性能测试

### 1. 负载测试脚本

```python
# tests/load_test.py
import asyncio
import aiohttp
import time

async def test_endpoint(session, url):
    start = time.time()
    async with session.get(url) as response:
        await response.text()
        return time.time() - start

async def load_test():
    url = "http://localhost:8000/api/market/data/BTCUSDT"
    concurrent_requests = 100
    
    async with aiohttp.ClientSession() as session:
        tasks = [test_endpoint(session, url) for _ in range(concurrent_requests)]
        times = await asyncio.gather(*tasks)
    
    print(f"Average response time: {sum(times)/len(times):.2f}s")
    print(f"Max response time: {max(times):.2f}s")
    print(f"Min response time: {min(times):.2f}s")

if __name__ == "__main__":
    asyncio.run(load_test())
```

完成这些优化后，您的应用性能将显著提升！
