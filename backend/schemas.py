"""
数据验证模式 - 使用Pydantic进行输入验证
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime
import re

class UserRegister(BaseModel):
    """用户注册验证模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=8, max_length=128, description="密码")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    
    @validator('username')
    def username_must_be_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', v):
            raise ValueError('用户名只能包含字母、数字、下划线和中文字符')
        return v
    
    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少8位')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('密码必须包含字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含数字')
        return v
    
    @validator('phone')
    def phone_must_be_valid(cls, v):
        if v and not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('请输入有效的手机号码')
        return v

class UserLogin(BaseModel):
    """用户登录验证模式"""
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=1, max_length=128, description="密码")

class PredictionRequest(BaseModel):
    """预测请求验证模式"""
    symbol: str = Field(..., description="交易对")
    timeframes: List[str] = Field(..., min_items=1, max_items=10, description="时间框架列表")
    exchange: Optional[str] = Field("binance", description="参照交易所")
    
    @validator('symbol')
    def symbol_must_be_valid(cls, v):
        valid_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'DOTUSDT']
        if v.upper() not in valid_symbols:
            raise ValueError(f'交易对必须是: {", ".join(valid_symbols)}')
        return v.upper()
    
    @validator('timeframes')
    def timeframes_must_be_valid(cls, v):
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']
        for tf in v:
            if tf not in valid_timeframes:
                raise ValueError(f'时间框架必须是: {", ".join(valid_timeframes)}')
        return v
    
    @validator('exchange')
    def exchange_must_be_valid(cls, v):
        if v is None:
            return "binance"
        valid_exchanges = ['binance', 'okx', 'bybit', 'coinbase', 'kraken']
        if v.lower() not in valid_exchanges:
            raise ValueError(f'交易所必须是: {", ".join(valid_exchanges)}')
        return v.lower()

class OrderCreate(BaseModel):
    """订单创建验证模式"""
    plan_type: str = Field(..., description="套餐类型")
    amount: float = Field(..., gt=0, description="金额")
    payment_method: str = Field(..., description="支付方式")
    
    @validator('plan_type')
    def plan_type_must_be_valid(cls, v):
        valid_plans = ['basic', 'pro', 'premium']
        if v not in valid_plans:
            raise ValueError(f'套餐类型必须是: {", ".join(valid_plans)}')
        return v
    
    @validator('payment_method')
    def payment_method_must_be_valid(cls, v):
        valid_methods = ['alipay', 'wechat']
        if v not in valid_methods:
            raise ValueError(f'支付方式必须是: {", ".join(valid_methods)}')
        return v
    
    @validator('amount')
    def amount_must_be_reasonable(cls, v):
        if v < 1 or v > 10000:
            raise ValueError('金额必须在1-10000之间')
        return round(v, 2)

class PaymentProofUpload(BaseModel):
    """支付凭证上传验证模式"""
    order_id: int = Field(..., gt=0, description="订单ID")
    proof_type: str = Field(..., description="凭证类型")
    
    @validator('proof_type')
    def proof_type_must_be_valid(cls, v):
        valid_types = ['screenshot', 'receipt']
        if v not in valid_types:
            raise ValueError(f'凭证类型必须是: {", ".join(valid_types)}')
        return v

class UserUpdate(BaseModel):
    """用户信息更新验证模式"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    
    @validator('username')
    def username_must_be_valid(cls, v):
        if v and not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', v):
            raise ValueError('用户名只能包含字母、数字、下划线和中文字符')
        return v
    
    @validator('phone')
    def phone_must_be_valid(cls, v):
        if v and not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('请输入有效的手机号码')
        return v

class PasswordChange(BaseModel):
    """密码修改验证模式"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=8, max_length=128, description="新密码")
    
    @validator('new_password')
    def new_password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度至少8位')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('密码必须包含字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含数字')
        return v

class MarketDataQuery(BaseModel):
    """市场数据查询验证模式"""
    symbol: str = Field(..., description="交易对")
    exchange: Optional[str] = Field(None, description="交易所")
    
    @validator('symbol')
    def symbol_must_be_valid(cls, v):
        valid_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'DOTUSDT']
        if v.upper() not in valid_symbols:
            raise ValueError(f'交易对必须是: {", ".join(valid_symbols)}')
        return v.upper()
    
    @validator('exchange')
    def exchange_must_be_valid(cls, v):
        if v is None:
            return v
        valid_exchanges = ['binance', 'okx', 'bybit', 'coinbase', 'kraken']
        if v.lower() not in valid_exchanges:
            raise ValueError(f'交易所必须是: {", ".join(valid_exchanges)}')
        return v.lower()

# 响应模式
class UserResponse(BaseModel):
    """用户信息响应模式"""
    id: int
    username: str
    email: str
    phone: Optional[str]
    membership_level: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """令牌响应模式"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class PredictionResponse(BaseModel):
    """预测响应模式"""
    success: bool
    predictions: dict
    message: Optional[str] = None
    quota_remaining: Optional[int] = None

class OrderResponse(BaseModel):
    """订单响应模式"""
    id: int
    order_no: str
    plan_type: str
    amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    """通用API响应模式"""
    success: bool
    message: str
    data: Optional[dict] = None
    error_code: Optional[str] = None
