"""
速率限制中间件 - 防止API滥用
"""

import time
from collections import defaultdict
from typing import Dict, Tuple, Optional
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

class RateLimiter:
    """速率限制器"""
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.limits = {
            "auth/login": (5, 300),        # 5次/5分钟
            "auth/register": (3, 3600),    # 3次/小时
            "prediction/predict": (100, 3600),  # 100次/小时
            "market/data": (1000, 3600),   # 1000次/小时
            "orders/create": (10, 3600),   # 10次/小时
            "default": (1000, 3600)        # 默认1000次/小时
        }
    
    def get_client_key(self, request: Request) -> str:
        """获取客户端标识"""
        # 优先使用用户ID（如果已认证）
        if hasattr(request.state, 'user_id'):
            return f"user_{request.state.user_id}"
        
        # 使用IP地址
        client_ip = request.client.host
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        return f"ip_{client_ip}"
    
    def get_endpoint_key(self, path: str) -> str:
        """获取端点标识"""
        # 移除/api/前缀
        if path.startswith("/api/"):
            path = path[5:]
        
        # 匹配已定义的端点
        for endpoint in self.limits.keys():
            if endpoint != "default" and endpoint in path:
                return endpoint
        
        return "default"
    
    def is_allowed(self, client_key: str, endpoint_key: str) -> Tuple[bool, Optional[int]]:
        """检查是否允许请求"""
        now = time.time()
        limit, window = self.limits.get(endpoint_key, self.limits["default"])
        
        # 清理过期请求
        self.requests[client_key] = [
            req_time for req_time in self.requests[client_key] 
            if now - req_time < window
        ]
        
        # 检查是否超过限制
        current_requests = len(self.requests[client_key])
        if current_requests >= limit:
            # 计算重置时间
            oldest_request = min(self.requests[client_key]) if self.requests[client_key] else now
            reset_time = int(oldest_request + window - now)
            return False, reset_time
        
        # 记录当前请求
        self.requests[client_key].append(now)
        return True, None
    
    def get_remaining_requests(self, client_key: str, endpoint_key: str) -> int:
        """获取剩余请求次数"""
        limit, _ = self.limits.get(endpoint_key, self.limits["default"])
        current_requests = len(self.requests[client_key])
        return max(0, limit - current_requests)

# 全局速率限制器实例
rate_limiter = RateLimiter()

class RateLimitMiddleware(BaseHTTPMiddleware):
    """速率限制中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 跳过静态文件和健康检查
        if (request.url.path.startswith("/static/") or 
            request.url.path.startswith("/uploads/") or
            request.url.path in ["/health", "/", "/docs", "/openapi.json"]):
            return await call_next(request)
        
        client_key = rate_limiter.get_client_key(request)
        endpoint_key = rate_limiter.get_endpoint_key(request.url.path)
        
        allowed, reset_time = rate_limiter.is_allowed(client_key, endpoint_key)
        
        if not allowed:
            logging.warning(
                f"Rate limit exceeded for {client_key} on {endpoint_key}. "
                f"Reset in {reset_time} seconds."
            )
            
            response = Response(
                content='{"detail": "请求过于频繁，请稍后再试", "error_code": "RATE_LIMIT_EXCEEDED"}',
                status_code=429,
                media_type="application/json"
            )
            response.headers["Retry-After"] = str(reset_time)
            response.headers["X-RateLimit-Limit"] = str(rate_limiter.limits[endpoint_key][0])
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + reset_time)
            return response
        
        # 处理请求
        response = await call_next(request)
        
        # 添加速率限制头部信息
        remaining = rate_limiter.get_remaining_requests(client_key, endpoint_key)
        limit, window = rate_limiter.limits.get(endpoint_key, rate_limiter.limits["default"])
        
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"] = str(window)
        
        return response

def check_rate_limit(request: Request, endpoint: str = "default"):
    """手动检查速率限制的装饰器函数"""
    client_key = rate_limiter.get_client_key(request)
    allowed, reset_time = rate_limiter.is_allowed(client_key, endpoint)
    
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="请求过于频繁，请稍后再试",
            headers={
                "Retry-After": str(reset_time),
                "X-RateLimit-Reset": str(int(time.time()) + reset_time)
            }
        )

# 装饰器版本的速率限制
def rate_limit(endpoint: str = "default"):
    """速率限制装饰器"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 从参数中找到request对象
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                check_rate_limit(request, endpoint)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
