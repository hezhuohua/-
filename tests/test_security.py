"""
安全功能测试
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.main import app
from backend.schemas import UserRegister, UserLogin
from backend.rate_limiter import RateLimiter

class TestInputValidation:
    """测试输入验证"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
    
    def test_user_register_validation(self):
        """测试用户注册输入验证"""
        # 测试无效邮箱
        invalid_email_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "testpassword123"
        }
        response = self.client.post("/api/auth/register", json=invalid_email_data)
        assert response.status_code == 422
        
        # 测试弱密码
        weak_password_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"
        }
        response = self.client.post("/api/auth/register", json=weak_password_data)
        assert response.status_code == 422
        
        # 测试无效用户名
        invalid_username_data = {
            "username": "a",  # 太短
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = self.client.post("/api/auth/register", json=invalid_username_data)
        assert response.status_code == 422
    
    def test_prediction_request_validation(self):
        """测试预测请求验证"""
        # 首先注册并登录获取token
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        register_response = self.client.post("/api/auth/register", json=user_data)
        
        if register_response.status_code == 200:
            token = register_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # 测试无效交易对
            invalid_symbol_data = {
                "symbol": "INVALID",
                "timeframes": ["1m"]
            }
            response = self.client.post(
                "/api/prediction/predict", 
                json=invalid_symbol_data, 
                headers=headers
            )
            assert response.status_code == 422
            
            # 测试无效时间框架
            invalid_timeframe_data = {
                "symbol": "BTCUSDT",
                "timeframes": ["invalid_timeframe"]
            }
            response = self.client.post(
                "/api/prediction/predict", 
                json=invalid_timeframe_data, 
                headers=headers
            )
            assert response.status_code == 422

class TestRateLimiting:
    """测试速率限制"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
        # 重置速率限制器
        from backend.rate_limiter import rate_limiter
        rate_limiter.requests.clear()
    
    def test_login_rate_limiting(self):
        """测试登录速率限制"""
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        # 快速发送多个请求
        responses = []
        for i in range(7):  # 超过5次限制
            response = self.client.post("/api/auth/login", json=login_data)
            responses.append(response.status_code)
        
        # 最后的请求应该被限制
        assert 429 in responses, "速率限制未生效"
    
    def test_rate_limit_headers(self):
        """测试速率限制响应头"""
        response = self.client.get("/api/market/data/BTCUSDT")
        
        # 检查速率限制头部
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Window" in response.headers

class TestAuthenticationSecurity:
    """测试认证安全"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
    
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
    
    def test_missing_authorization_header(self):
        """测试缺少认证头"""
        response = self.client.post(
            "/api/prediction/predict",
            json={"symbol": "BTCUSDT", "timeframes": ["1m"]}
        )
        
        assert response.status_code == 401
    
    def test_malformed_authorization_header(self):
        """测试格式错误的认证头"""
        headers = {"Authorization": "InvalidFormat token"}
        
        response = self.client.post(
            "/api/prediction/predict",
            json={"symbol": "BTCUSDT", "timeframes": ["1m"]},
            headers=headers
        )
        
        assert response.status_code == 401

class TestSQLInjectionProtection:
    """测试SQL注入防护"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
    
    def test_sql_injection_in_login(self):
        """测试登录中的SQL注入防护"""
        malicious_input = "'; DROP TABLE users; --"
        
        response = self.client.post("/api/auth/login", json={
            "email": malicious_input,
            "password": "test"
        })
        
        # 应该返回验证错误，而不是服务器错误
        assert response.status_code in [400, 422, 401]
        assert response.status_code != 500
    
    def test_xss_protection_in_registration(self):
        """测试注册中的XSS防护"""
        xss_payload = "<script>alert('xss')</script>"
        
        response = self.client.post("/api/auth/register", json={
            "username": xss_payload,
            "email": "test@example.com",
            "password": "testpassword123"
        })
        
        # 应该被输入验证拦截
        assert response.status_code in [400, 422]

class TestEnvironmentVariables:
    """测试环境变量安全"""
    
    def test_secret_key_from_environment(self):
        """测试SECRET_KEY从环境变量读取"""
        # 这个测试需要在没有SECRET_KEY环境变量的情况下运行
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="SECRET_KEY environment variable is required"):
                from backend.auth import SECRET_KEY
    
    def test_api_key_from_environment(self):
        """测试API密钥从环境变量读取"""
        from backend.prediction_service import PredictionService
        
        # 测试没有API密钥时的处理
        with patch.dict(os.environ, {}, clear=True):
            service = PredictionService()
            assert service.deepseek_api_key is None

class TestHealthCheck:
    """测试健康检查"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.client = TestClient(app)
    
    def test_health_endpoint(self):
        """测试健康检查端点"""
        response = self.client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "services" in data
        assert "version" in data
    
    def test_health_endpoint_no_rate_limit(self):
        """测试健康检查不受速率限制"""
        # 多次调用健康检查
        for _ in range(10):
            response = self.client.get("/health")
            assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
