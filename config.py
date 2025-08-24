#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安代理交易系统配置文件
"""

import os
from datetime import timedelta

class Config:
    """基础配置类"""

    # 应用配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

    # 数据库配置
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'trading_system.db'

    # 币安API配置
    BINANCE_MAINNET_URL = "https://fapi.binance.com"
    BINANCE_TESTNET_URL = "https://testnet.binancefuture.com"
    BINANCE_WS_MAINNET_URL = "wss://fstream.binance.com"
    BINANCE_WS_TESTNET_URL = "wss://stream.binancefuture.com"

    # API请求配置
    REQUEST_TIMEOUT = 30  # 秒
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # 秒

    # 交易配置
    DEFAULT_LEVERAGE = 10
    DEFAULT_QUANTITY_USDT = 100  # 默认100 USDT
    MAX_LEVERAGE = 125
    MIN_QUANTITY_USDT = 10

    # 分润配置
    PLATFORM_SHARE_RATIO = 0.7  # 平台70%
    USER_SHARE_RATIO = 0.3      # 用户30%

    # 风险控制
    MAX_POSITION_SIZE_USDT = 1000  # 最大仓位1000 USDT
    MAX_DAILY_TRADES = 50          # 每日最大交易次数
    STOP_LOSS_PERCENTAGE = 0.05    # 默认止损5%
    TAKE_PROFIT_PERCENTAGE = 0.10  # 默认止盈10%

    # 定时任务配置
    SYNC_INTERVAL_MINUTES = 5      # 数据同步间隔
    CLEANUP_INTERVAL_HOURS = 24    # 数据清理间隔

    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'trading_system.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5

    # 安全配置
    API_KEY_ENCRYPTION_KEY = os.environ.get('API_KEY_ENCRYPTION_KEY') or 'your-encryption-key'
    SESSION_TIMEOUT = timedelta(hours=24)
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=30)

    # 支持的交易对
    SUPPORTED_SYMBOLS = [
        'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT',
        'XRPUSDT', 'DOGEUSDT', 'AVAXUSDT', 'DOTUSDT', 'LINKUSDT',
        'MATICUSDT', 'LTCUSDT', 'BCHUSDT', 'UNIUSDT', 'ATOMUSDT'
    ]

    # 交易对配置
    SYMBOL_CONFIGS = {
        'BTCUSDT': {
            'min_qty': 0.001,
            'step_size': 0.001,
            'max_leverage': 125,
            'default_leverage': 10
        },
        'ETHUSDT': {
            'min_qty': 0.01,
            'step_size': 0.01,
            'max_leverage': 125,
            'default_leverage': 10
        },
        'BNBUSDT': {
            'min_qty': 0.01,
            'step_size': 0.01,
            'max_leverage': 125,
            'default_leverage': 10
        },
        'ADAUSDT': {
            'min_qty': 1,
            'step_size': 1,
            'max_leverage': 125,
            'default_leverage': 10
        },
        'SOLUSDT': {
            'min_qty': 0.1,
            'step_size': 0.1,
            'max_leverage': 125,
            'default_leverage': 10
        },
        'XRPUSDT': {
            'min_qty': 1,
            'step_size': 1,
            'max_leverage': 125,
            'default_leverage': 10
        },
        'DOGEUSDT': {
            'min_qty': 1,
            'step_size': 1,
            'max_leverage': 125,
            'default_leverage': 10
        },
        'AVAXUSDT': {
            'min_qty': 0.1,
            'step_size': 0.1,
            'max_leverage': 125,
            'default_leverage': 10
        }
    }

    # 错误消息
    ERROR_MESSAGES = {
        'INVALID_API_KEY': '无效的API Key',
        'INSUFFICIENT_BALANCE': '余额不足',
        'INVALID_SYMBOL': '无效的交易对',
        'INVALID_QUANTITY': '无效的数量',
        'LEVERAGE_TOO_HIGH': '杠杆过高',
        'POSITION_TOO_LARGE': '仓位过大',
        'DAILY_LIMIT_EXCEEDED': '超过每日交易限制',
        'API_CONNECTION_FAILED': 'API连接失败',
        'ORDER_EXECUTION_FAILED': '订单执行失败',
        'SYNC_FAILED': '数据同步失败'
    }

    # 成功消息
    SUCCESS_MESSAGES = {
        'API_CONFIG_SAVED': 'API配置保存成功',
        'API_CONNECTION_SUCCESS': 'API连接成功',
        'ORDER_PLACED': '订单下单成功',
        'DATA_SYNCED': '数据同步成功',
        'PROFIT_CALCULATED': '分润计算成功'
    }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

    # 生产环境安全设置
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_KEY_ENCRYPTION_KEY = os.environ.get('API_KEY_ENCRYPTION_KEY')

    if not SECRET_KEY:
        raise ValueError("生产环境必须设置SECRET_KEY环境变量")

    if not API_KEY_ENCRYPTION_KEY:
        raise ValueError("生产环境必须设置API_KEY_ENCRYPTION_KEY环境变量")

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # 使用内存数据库
    DEBUG = True

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """获取配置"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    return config.get(config_name, config['default'])
