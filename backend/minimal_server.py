#!/usr/bin/env python3
"""
最小化的后端服务 - 用于快速测试
"""

import os
import sys
import secrets
import json
import asyncio
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

# 设置环境变量（如果不存在）
if not os.getenv("SECRET_KEY"):
    os.environ["SECRET_KEY"] = secrets.token_urlsafe(32)

app = FastAPI(
    title="永续合约预测系统",
    version="1.0.0",
    description="基于AI的加密货币永续合约价格预测系统"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# 导入交易所API模块
try:
    from exchange_api import get_market_data, cleanup_market_manager
    USE_REAL_API = True
    print("✅ 真实交易所API已启用")
except ImportError:
    USE_REAL_API = False
    print("⚠️  使用模拟数据（请安装aiohttp: pip install aiohttp）")

    # 模拟市场数据（备用）
    mock_market_data = {
        "BTCUSDT": {
            "binance": {"price": 43250.50, "change_percent_24h": 2.45, "volume_24h": 28500000},
            "okx": {"price": 43255.20, "change_percent_24h": 2.48, "volume_24h": 15200000},
            "bybit": {"price": 43248.80, "change_percent_24h": 2.42, "volume_24h": 12800000},
            "coinbase": {"price": 43260.10, "change_percent_24h": 2.51, "volume_24h": 8900000},
            "kraken": {"price": 43245.30, "change_percent_24h": 2.40, "volume_24h": 5600000}
        },
        "ETHUSDT": {
            "binance": {"price": 2580.75, "change_percent_24h": 1.85, "volume_24h": 18500000},
            "okx": {"price": 2582.20, "change_percent_24h": 1.88, "volume_24h": 12200000},
            "bybit": {"price": 2579.90, "change_percent_24h": 1.82, "volume_24h": 9800000},
            "coinbase": {"price": 2583.50, "change_percent_24h": 1.92, "volume_24h": 7200000},
            "kraken": {"price": 2578.60, "change_percent_24h": 1.79, "volume_24h": 4100000}
        }
    }

@app.get("/")
async def root():
    """根路径"""
    return {"message": "永续合约预测系统后端服务", "status": "running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "services": {
            "api": "healthy",
            "database": "healthy",
            "cache": "healthy"
        },
        "version": "1.0.0"
    }

@app.get("/api/market/data/{symbol}")
async def get_market_data_endpoint(symbol: str):
    """获取市场数据"""
    try:
        if USE_REAL_API:
            # 使用真实交易所API
            data = await get_market_data(symbol.upper())
            if not data:
                raise HTTPException(status_code=404, detail="无法获取交易对数据")
        else:
            # 使用模拟数据
            if symbol.upper() not in mock_market_data:
                raise HTTPException(status_code=404, detail="交易对不存在")
            data = mock_market_data[symbol.upper()]

        return {
            "success": True,
            "data": data,
            "symbol": symbol.upper(),
            "timestamp": "2024-12-19T10:30:00Z",
            "source": "real_api" if USE_REAL_API else "mock_data"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取市场数据失败: {str(e)}")

@app.post("/api/auth/register")
async def register(user_data: dict):
    """用户注册（简化版）"""
    try:
        print(f"注册请求数据: {user_data}")  # 调试日志
        return {
            "success": True,
            "message": "注册成功",
            "access_token": "demo_token_" + secrets.token_urlsafe(16),
            "user": {
                "id": 1,
                "username": user_data.get("username", "demo_user"),
                "email": user_data.get("email", "demo@example.com"),
                "membership_level": "trial"
            }
        }
    except Exception as e:
        print(f"注册错误: {e}")  # 调试日志
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")

@app.post("/api/auth/login")
async def login(login_data: dict):
    """用户登录（简化版）"""
    try:
        print(f"登录请求数据: {login_data}")  # 调试日志
        email = login_data.get("email", "")
        password = login_data.get("password", "")

        # 演示账号验证
        if email == "demo@example.com" and password == "demo123":
            return {
                "success": True,
                "access_token": "demo_token_" + secrets.token_urlsafe(16),
                "user": {
                    "id": 1,
                    "username": "demo_user",
                    "email": "demo@example.com",
                    "membership_level": "trial"
                }
            }

        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    except Exception as e:
        print(f"登录错误: {e}")  # 调试日志
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

@app.post("/api/prediction/predict")
async def make_prediction(prediction_data: dict):
    """AI预测（简化版）"""
    import random

    symbol = prediction_data.get("symbol", "BTCUSDT")
    timeframes = prediction_data.get("timeframes", ["1m", "5m", "15m", "1h"])

    predictions = {}
    for timeframe in timeframes:
        direction = random.choice(["up", "down"])
        probability = random.uniform(60, 90)
        confidence = random.uniform(0.6, 0.9)

        predictions[timeframe] = {
            "direction": direction,
            "probability": round(probability, 1),
            "confidence": round(confidence, 2),
            "reasoning": f"基于技术分析，预计{symbol}在{timeframe}时间框架内将{'上涨' if direction == 'up' else '下跌'}"
        }

    return {
        "success": True,
        "predictions": predictions,
        "quota_remaining": 45
    }

@app.get("/api/user/profile")
async def get_user_profile():
    """获取用户信息（简化版）"""
    return {
        "success": True,
        "user": {
            "id": 1,
            "username": "demo_user",
            "email": "demo@example.com",
            "membership_level": "trial",
            "quota_remaining": 45,
            "quota_total": 50
        }
    }

# WebSocket端点
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # 获取并发送初始数据
        if USE_REAL_API:
            initial_btc_data = await get_market_data("BTCUSDT")
            initial_eth_data = await get_market_data("ETHUSDT")
            initial_data = {
                "type": "initial_data",
                "data": {
                    "BTCUSDT": initial_btc_data,
                    "ETHUSDT": initial_eth_data
                }
            }
        else:
            initial_data = {
                "type": "initial_data",
                "data": mock_market_data
            }

        await websocket.send_text(json.dumps(initial_data))

        # 保持连接并发送实时更新
        while True:
            await asyncio.sleep(5)  # 每5秒更新一次

            if USE_REAL_API:
                # 获取真实数据
                try:
                    btc_data = await get_market_data("BTCUSDT")
                    eth_data = await get_market_data("ETHUSDT")
                    update_data = {
                        "type": "market_update",
                        "data": {
                            "BTCUSDT": btc_data,
                            "ETHUSDT": eth_data
                        },
                        "source": "real_api"
                    }
                except Exception as e:
                    print(f"实时数据获取失败: {e}")
                    continue
            else:
                # 模拟价格变化
                for symbol in mock_market_data:
                    for exchange in mock_market_data[symbol]:
                        # 添加小幅随机变化
                        current_price = mock_market_data[symbol][exchange]["price"]
                        change = (secrets.randbelow(200) - 100) / 10000  # ±0.5%
                        mock_market_data[symbol][exchange]["price"] = current_price * (1 + change)

                # 发送市场更新
                update_data = {
                    "type": "market_update",
                    "data": mock_market_data,
                    "source": "mock_data"
                }

            await websocket.send_text(json.dumps(update_data))

    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 应用生命周期事件
@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    print("🚀 永续合约预测系统启动中...")
    if USE_REAL_API:
        print("📡 正在初始化交易所API连接...")
        # 测试连接
        try:
            test_data = await get_market_data("BTCUSDT")
            if test_data:
                print("✅ 交易所API连接成功")
            else:
                print("⚠️  交易所API连接失败，将使用备用数据")
        except Exception as e:
            print(f"⚠️  交易所API初始化错误: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理"""
    print("🔄 正在关闭系统...")
    if USE_REAL_API:
        try:
            await cleanup_market_manager()
            print("✅ 交易所API连接已关闭")
        except:
            pass
    print("👋 系统已关闭")

if __name__ == "__main__":
    print("🚀 启动永续合约预测系统...")
    print("📍 服务地址:")
    print("  - API: http://localhost:8000")
    print("  - 文档: http://localhost:8000/docs")
    print("  - 健康检查: http://localhost:8000/health")
    print("  - WebSocket: ws://localhost:8000/ws")
    print("\n💡 演示账号: demo@example.com / demo123")
    if USE_REAL_API:
        print("📡 真实交易所API已启用")
    else:
        print("⚠️  使用模拟数据（安装aiohttp后可启用真实API）")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
