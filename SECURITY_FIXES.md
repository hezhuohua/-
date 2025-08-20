# 安全问题修复指南

本文档提供了针对代码安全问题的具体修复方案和代码示例。

## 🔴 严重安全问题修复

### 1. 修复硬编码敏感信息

#### 问题文件: `backend/auth.py`

**当前代码 (有问题)**:
```python
# JWT配置
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30天
```

**修复后代码**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# JWT配置 - 从环境变量读取
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43200"))  # 默认30天
```

#### 问题文件: `backend/prediction_service.py`

**当前代码 (有问题)**:
```python
def __init__(self):
    self.deepseek_api_key = "your-deepseek-api-key"  # 需要配置实际的API密钥
    self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
```

**修复后代码**:
```python
import os
from dotenv import load_dotenv

def __init__(self):
    load_dotenv()
    self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not self.deepseek_api_key:
        raise ValueError("DEEPSEEK_API_KEY environment variable is required")
    self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
```

### 2. 添加输入验证

#### 创建新文件: `backend/schemas.py`

```python
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @validator('username')
    def username_must_be_valid(cls, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError('用户名长度必须在3-50字符之间')
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v
    
    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少8位')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PredictionRequest(BaseModel):
    symbol: str
    timeframes: List[str]
    exchange: Optional[str] = "binance"
    
    @validator('symbol')
    def symbol_must_be_valid(cls, v):
        valid_symbols = ['BTCUSDT', 'ETHUSDT']
        if v not in valid_symbols:
            raise ValueError(f'交易对必须是: {", ".join(valid_symbols)}')
        return v
    
    @validator('timeframes')
    def timeframes_must_be_valid(cls, v):
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
        for tf in v:
            if tf not in valid_timeframes:
                raise ValueError(f'时间框架必须是: {", ".join(valid_timeframes)}')
        return v

class OrderCreate(BaseModel):
    plan_type: str
    amount: float
    payment_method: str
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('金额必须大于0')
        return v
```

#### 修改 `backend/main.py` 使用验证模式

**当前代码 (有问题)**:
```python
@app.post("/api/auth/register")
async def register(user_data: dict, db = Depends(get_db)):
    # 检查用户是否已存在
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
```

**修复后代码**:
```python
from schemas import UserRegister, UserLogin, PredictionRequest, OrderCreate

@app.post("/api/auth/register")
async def register(user_data: UserRegister, db = Depends(get_db)):
    # 检查用户是否已存在
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        membership_level="trial",
        trial_start_time=datetime.now()
    )
```

### 3. 添加速率限制

#### 创建新文件: `backend/rate_limiter.py`

```python
import time
from collections import defaultdict
from fastapi import HTTPException, Request
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.limits = {
            "login": (5, 300),      # 5次/5分钟
            "register": (3, 3600),   # 3次/小时
            "prediction": (100, 3600), # 100次/小时
            "default": (1000, 3600)  # 1000次/小时
        }
    
    def is_allowed(self, key: str, endpoint: str = "default") -> bool:
        now = time.time()
        limit, window = self.limits.get(endpoint, self.limits["default"])
        
        # 清理过期请求
        self.requests[key] = [req_time for req_time in self.requests[key] 
                             if now - req_time < window]
        
        # 检查是否超过限制
        if len(self.requests[key]) >= limit:
            return False
        
        # 记录当前请求
        self.requests[key].append(now)
        return True

rate_limiter = RateLimiter()

def check_rate_limit(request: Request, endpoint: str = "default"):
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip, endpoint):
        raise HTTPException(
            status_code=429, 
            detail="请求过于频繁，请稍后再试"
        )
```

#### 在 `backend/main.py` 中使用速率限制

```python
from rate_limiter import check_rate_limit

@app.post("/api/auth/login")
async def login(
    login_data: UserLogin, 
    request: Request,
    db = Depends(get_db)
):
    check_rate_limit(request, "login")
    # ... 登录逻辑
```

### 4. 添加CSRF保护

#### 修改 `backend/main.py` 添加CSRF中间件

```python
from fastapi.middleware.csrf import CSRFMiddleware

app.add_middleware(
    CSRFMiddleware,
    secret_key=os.getenv("CSRF_SECRET_KEY", "your-csrf-secret-key")
)
```

### 5. 添加请求超时处理

#### 修改 `backend/prediction_service.py`

**当前代码 (有问题)**:
```python
async def call_deepseek_api(self, prompt: str) -> str:
    # 这里使用模拟响应，实际应该调用真实的DEEPSEEK API
    await asyncio.sleep(0.5)  # 模拟API调用时间
```

**修复后代码**:
```python
import httpx
import asyncio

async def call_deepseek_api(self, prompt: str) -> str:
    """调用DEEPSEEK API"""
    headers = {
        "Authorization": f"Bearer {self.deepseek_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    
    timeout = httpx.Timeout(30.0)  # 30秒超时
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                self.deepseek_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="API请求超时")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="API请求失败")
    except Exception as e:
        logging.error(f"DEEPSEEK API error: {e}")
        raise HTTPException(status_code=500, detail="预测服务暂时不可用")
```

### 6. 数据库安全改进

#### 修改 `backend/database.py` 添加连接池

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# 创建引擎with连接池
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## 🔧 环境变量配置

### 更新 `.env` 文件

```env
# 安全配置
SECRET_KEY=your-very-secure-secret-key-here-at-least-32-characters
CSRF_SECRET_KEY=your-csrf-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# 数据库配置
DATABASE_URL=sqlite:///./crypto_prediction.db

# API配置
DEEPSEEK_API_KEY=your-deepseek-api-key-here

# Redis配置
REDIS_URL=redis://localhost:6379

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=False

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 📋 修复检查清单

完成以下修复后，请检查：

- [ ] 所有敏感信息已移至环境变量
- [ ] 添加了输入验证模式
- [ ] 实现了速率限制
- [ ] 添加了CSRF保护
- [ ] 设置了请求超时
- [ ] 配置了数据库连接池
- [ ] 更新了环境变量配置
- [ ] 测试所有修复是否正常工作

## 🧪 测试修复

运行以下命令测试修复：

```bash
# 运行安全测试
python -m pytest tests/test_security.py -v

# 检查环境变量
python -c "import os; print('SECRET_KEY:', bool(os.getenv('SECRET_KEY')))"

# 测试速率限制
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}' \
  --repeat 10
```

完成这些修复后，您的应用将具备基本的安全防护能力。
