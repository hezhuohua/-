# 测试改进指南

本文档提供了完善测试覆盖率和测试质量的具体方案。

## 🧪 测试框架配置

### 1. 安装测试依赖

```bash
pip install pytest pytest-asyncio pytest-cov httpx pytest-mock
```

### 2. 配置pytest

#### 创建 `pytest.ini`

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --strict-config
    --cov=backend
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
asyncio_mode = auto
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
    security: Security tests
```

## 🔧 单元测试

### 1. 认证模块测试

#### 创建 `tests/test_auth.py`

```python
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from jose import jwt

from backend.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    verify_token,
    get_current_user
)
from backend.models import User

class TestPasswordHandling:
    def test_password_hashing(self):
        """测试密码哈希"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)
    
    def test_password_hash_uniqueness(self):
        """测试密码哈希唯一性"""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2  # 每次哈希应该不同（因为salt）

class TestJWTTokens:
    def test_create_access_token(self):
        """测试JWT令牌创建"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_token_with_expiration(self):
        """测试带过期时间的令牌"""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)
        
        # 解码验证过期时间
        from backend.auth import SECRET_KEY, ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert "exp" in payload
        assert payload["sub"] == "test@example.com"
    
    def test_verify_valid_token(self):
        """测试验证有效令牌"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        
        email = verify_token(token)
        assert email == "test@example.com"
    
    def test_verify_invalid_token(self):
        """测试验证无效令牌"""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid_token")
        
        assert exc_info.value.status_code == 401

@pytest.mark.asyncio
class TestUserAuthentication:
    async def test_get_current_user_valid(self):
        """测试获取当前用户 - 有效令牌"""
        # Mock数据库会话
        mock_db = MagicMock()
        mock_user = User(id=1, email="test@example.com", username="testuser")
        mock_db.query().filter().first.return_value = mock_user
        
        # Mock认证凭据
        from fastapi.security import HTTPAuthorizationCredentials
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=create_access_token({"sub": "test@example.com"})
        )
        
        user = get_current_user(mock_credentials, mock_db)
        assert user.email == "test@example.com"
    
    async def test_get_current_user_invalid_token(self):
        """测试获取当前用户 - 无效令牌"""
        from fastapi import HTTPException
        from fastapi.security import HTTPAuthorizationCredentials
        
        mock_db = MagicMock()
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid_token"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials, mock_db)
        
        assert exc_info.value.status_code == 401
```

### 2. 预测服务测试

#### 创建 `tests/test_prediction_service.py`

```python
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio

from backend.prediction_service import PredictionService

class TestPredictionService:
    def setup_method(self):
        """每个测试方法前的设置"""
        self.service = PredictionService()
    
    @pytest.mark.asyncio
    async def test_predict_basic(self):
        """测试基本预测功能"""
        symbol = "BTCUSDT"
        timeframes = ["1m", "5m"]
        market_data = {
            "binance": {
                "price": 43250.0,
                "change_percent_24h": 2.5,
                "volume_24h": 50000
            }
        }
        
        result = await self.service.predict(symbol, timeframes, market_data)
        
        assert isinstance(result, dict)
        assert "1m" in result
        assert "5m" in result
        
        for timeframe, prediction in result.items():
            assert "direction" in prediction
            assert "probability" in prediction
            assert "confidence" in prediction
            assert prediction["direction"] in ["up", "down", "neutral"]
            assert 0 <= prediction["probability"] <= 100
            assert 0 <= prediction["confidence"] <= 1
    
    @pytest.mark.asyncio
    async def test_predict_empty_market_data(self):
        """测试空市场数据的预测"""
        symbol = "BTCUSDT"
        timeframes = ["1m"]
        market_data = {}
        
        result = await self.service.predict(symbol, timeframes, market_data)
        
        assert isinstance(result, dict)
        assert "1m" in result
        assert result["1m"]["direction"] == "neutral"
    
    @pytest.mark.asyncio
    @patch('backend.prediction_service.PredictionService.call_deepseek_api')
    async def test_deepseek_api_call(self, mock_api_call):
        """测试DEEPSEEK API调用"""
        mock_api_call.return_value = "基于技术分析，预计价格将上涨，置信度75%"
        
        symbol = "BTCUSDT"
        timeframe = "1h"
        market_data = {"binance": {"price": 43250.0, "change_percent_24h": 2.5}}
        
        result = await self.service.deepseek_analysis(symbol, timeframe, market_data)
        
        assert result["direction"] in ["up", "down", "neutral"]
        assert "reasoning" in result
        mock_api_call.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_prediction_caching(self):
        """测试预测结果缓存"""
        # 这个测试需要实际的缓存实现
        pass
```

### 3. 交易所管理器测试

#### 创建 `tests/test_exchange_manager.py`

```python
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio

from backend.exchange_manager import ExchangeDataManager, MarketData

class TestMarketData:
    def test_market_data_creation(self):
        """测试市场数据对象创建"""
        data = MarketData()
        data.symbol = "BTCUSDT"
        data.exchange = "binance"
        data.price = 43250.0
        
        result = data.to_dict()
        
        assert result["symbol"] == "BTCUSDT"
        assert result["exchange"] == "binance"
        assert result["price"] == 43250.0

class TestExchangeDataManager:
    def setup_method(self):
        """每个测试方法前的设置"""
        self.manager = ExchangeDataManager()
    
    def test_initialization(self):
        """测试初始化"""
        assert isinstance(self.manager.market_data, dict)
        assert "BTCUSDT" in self.manager.market_data
        assert "ETHUSDT" in self.manager.market_data
    
    def test_get_latest_market_data(self):
        """测试获取最新市场数据"""
        # 添加一些测试数据
        test_data = MarketData()
        test_data.symbol = "BTCUSDT"
        test_data.exchange = "binance"
        test_data.price = 43250.0
        
        self.manager.market_data["BTCUSDT"]["binance"] = test_data
        
        result = self.manager.get_latest_market_data()
        
        assert "BTCUSDT" in result
        assert "binance" in result["BTCUSDT"]
        assert result["BTCUSDT"]["binance"]["price"] == 43250.0
    
    def test_get_symbol_data(self):
        """测试获取指定交易对数据"""
        # 添加测试数据
        test_data = MarketData()
        test_data.symbol = "BTCUSDT"
        test_data.exchange = "binance"
        test_data.price = 43250.0
        
        self.manager.market_data["BTCUSDT"]["binance"] = test_data
        
        result = self.manager.get_symbol_data("BTCUSDT")
        
        assert "binance" in result
        assert result["binance"]["price"] == 43250.0
    
    def test_get_aggregated_data(self):
        """测试获取聚合数据"""
        # 添加多个交易所数据
        exchanges = ["binance", "okx", "bybit"]
        prices = [43250.0, 43260.0, 43240.0]
        
        for exchange, price in zip(exchanges, prices):
            data = MarketData()
            data.symbol = "BTCUSDT"
            data.exchange = exchange
            data.price = price
            data.volume_24h = 10000
            
            self.manager.market_data["BTCUSDT"][exchange] = data
        
        result = self.manager.get_aggregated_data("BTCUSDT")
        
        assert "avg_price" in result
        assert "max_price" in result
        assert "min_price" in result
        assert result["avg_price"] == sum(prices) / len(prices)
        assert result["max_price"] == max(prices)
        assert result["min_price"] == min(prices)
```

## 🔗 集成测试

### 1. API端点测试

#### 创建 `tests/test_api.py`

```python
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app
from backend.database import get_db
from backend.models import User

# 测试数据库依赖覆盖
def override_get_db():
    # 使用内存SQLite数据库进行测试
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 创建表
    from backend.models import Base
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestAuthAPI:
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
    
    def test_register_user(self):
        """测试用户注册"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = self.client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"
    
    def test_register_duplicate_email(self):
        """测试重复邮箱注册"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        # 第一次注册
        self.client.post("/api/auth/register", json=user_data)
        
        # 第二次注册相同邮箱
        response = self.client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "邮箱已被注册" in response.json()["detail"]
    
    def test_login_valid_user(self):
        """测试有效用户登录"""
        # 先注册用户
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        self.client.post("/api/auth/register", json=user_data)
        
        # 登录
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = self.client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
    
    def test_login_invalid_credentials(self):
        """测试无效凭据登录"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = self.client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401

class TestMarketAPI:
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
    
    @patch('backend.main.exchange_manager')
    def test_get_market_data(self, mock_manager):
        """测试获取市场数据"""
        mock_manager.get_symbol_data.return_value = {
            "binance": {
                "price": 43250.0,
                "change_percent_24h": 2.5
            }
        }
        
        response = self.client.get("/api/market/data/BTCUSDT")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

class TestPredictionAPI:
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
    
    def test_prediction_without_auth(self):
        """测试未认证的预测请求"""
        prediction_data = {
            "symbol": "BTCUSDT",
            "timeframes": ["1m", "5m"]
        }
        
        response = self.client.post("/api/prediction/predict", json=prediction_data)
        
        assert response.status_code == 401
    
    def test_prediction_with_auth(self):
        """测试已认证的预测请求"""
        # 先注册并登录获取token
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        register_response = self.client.post("/api/auth/register", json=user_data)
        token = register_response.json()["access_token"]
        
        # 发送预测请求
        prediction_data = {
            "symbol": "BTCUSDT",
            "timeframes": ["1m", "5m"]
        }
        headers = {"Authorization": f"Bearer {token}"}
        
        response = self.client.post(
            "/api/prediction/predict", 
            json=prediction_data, 
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "predictions" in data
```

## 🔒 安全测试

### 1. 安全漏洞测试

#### 创建 `tests/test_security.py`

```python
import pytest
from fastapi.testclient import TestClient
from backend.main import app

class TestSecurityVulnerabilities:
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
    
    def test_sql_injection_protection(self):
        """测试SQL注入防护"""
        malicious_input = "'; DROP TABLE users; --"
        
        response = self.client.post("/api/auth/login", json={
            "email": malicious_input,
            "password": "test"
        })
        
        # 应该返回验证错误，而不是服务器错误
        assert response.status_code in [400, 422, 401]
    
    def test_xss_protection(self):
        """测试XSS防护"""
        xss_payload = "<script>alert('xss')</script>"
        
        response = self.client.post("/api/auth/register", json={
            "username": xss_payload,
            "email": "test@example.com",
            "password": "testpassword123"
        })
        
        # 应该被输入验证拦截
        assert response.status_code in [400, 422]
    
    def test_rate_limiting(self):
        """测试速率限制"""
        # 快速发送多个请求
        for _ in range(10):
            response = self.client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "wrongpassword"
            })
        
        # 最后几个请求应该被限制
        assert response.status_code in [429, 401]
    
    def test_jwt_token_validation(self):
        """测试JWT令牌验证"""
        # 使用无效token
        headers = {"Authorization": "Bearer invalid_token"}
        
        response = self.client.post(
            "/api/prediction/predict",
            json={"symbol": "BTCUSDT", "timeframes": ["1m"]},
            headers=headers
        )
        
        assert response.status_code == 401
```

## 📊 测试覆盖率配置

### 1. 覆盖率配置文件

#### 创建 `.coveragerc`

```ini
[run]
source = backend
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    class .*\(Protocol\):
    @(abc\.)?abstractmethod

[html]
directory = htmlcov
```

## 🚀 运行测试

### 1. 测试命令

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_auth.py

# 运行特定测试类
pytest tests/test_auth.py::TestPasswordHandling

# 运行特定测试方法
pytest tests/test_auth.py::TestPasswordHandling::test_password_hashing

# 运行带覆盖率的测试
pytest --cov=backend --cov-report=html

# 运行并生成详细报告
pytest -v --cov=backend --cov-report=term-missing

# 只运行单元测试
pytest -m unit

# 只运行集成测试
pytest -m integration

# 运行安全测试
pytest -m security
```

### 2. 持续集成配置

#### 创建 `.github/workflows/test.yml`

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio
    
    - name: Run tests
      run: |
        pytest --cov=backend --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

完成这些测试后，您的代码质量和可靠性将大大提升！
