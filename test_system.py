#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安代理交易系统测试脚本
"""

import requests
import json
import time
import sys

# 测试配置
BASE_URL = "http://localhost:5000"
TEST_USER_ID = "test_user_001"

def test_api_endpoint(endpoint, method="GET", data=None):
    """测试API端点"""
    url = f"{BASE_URL}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"❌ 不支持的HTTP方法: {method}")
            return False

        if response.status_code == 200:
            result = response.json()
            print(f"✅ {endpoint} - 成功")
            if result.get('data'):
                print(f"   数据: {json.dumps(result['data'], indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"❌ {endpoint} - 失败 (状态码: {response.status_code})")
            print(f"   错误: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ {endpoint} - 连接失败 (请确保后端服务正在运行)")
        return False
    except Exception as e:
        print(f"❌ {endpoint} - 异常: {str(e)}")
        return False

def test_system():
    """运行系统测试"""
    print("🚀 币安代理交易系统测试开始")
    print("=" * 50)

    # 测试1: 系统状态
    print("\n📊 测试1: 系统状态检查")
    test_api_endpoint("/")

    # 测试2: 保存API配置
    print("\n🔑 测试2: API配置管理")
    api_config = {
        "user_id": TEST_USER_ID,
        "api_key": "test_api_key_123",
        "api_secret": "test_api_secret_456",
        "testnet": True
    }
    test_api_endpoint("/api/config", "POST", api_config)

    # 测试3: 获取API配置
    print("\n📋 测试3: 获取API配置")
    test_api_endpoint(f"/api/config/{TEST_USER_ID}")

    # 测试4: 测试API连接
    print("\n🔌 测试4: API连接测试")
    test_data = {"user_id": TEST_USER_ID}
    test_api_endpoint("/api/test", "POST", test_data)

    # 测试5: 获取交易记录
    print("\n📈 测试5: 交易记录")
    test_api_endpoint(f"/api/trades/{TEST_USER_ID}")

    # 测试6: 模拟交易执行
    print("\n💼 测试6: 交易执行")
    trade_data = {
        "user_id": TEST_USER_ID,
        "symbol": "BTCUSDT",
        "side": "BUY",
        "quantity": "0.001",
        "take_profit": 45000,
        "stop_loss": 42000
    }
    test_api_endpoint("/api/trade", "POST", trade_data)

    # 测试7: 数据同步
    print("\n🔄 测试7: 数据同步")
    sync_data = {"user_id": TEST_USER_ID}
    test_api_endpoint("/api/sync", "POST", sync_data)

    # 测试8: 分润计算
    print("\n💰 测试8: 分润计算")
    profit_data = {
        "user_id": TEST_USER_ID,
        "trade_id": 1,
        "total_pnl": 100.50
    }
    test_api_endpoint("/api/profit-share", "POST", profit_data)

    print("\n" + "=" * 50)
    print("🎯 系统测试完成")
    print("\n📋 测试结果说明:")
    print("- ✅ 表示测试通过")
    print("- ❌ 表示测试失败")
    print("- 某些测试可能因为缺少真实API Key而失败，这是正常的")
    print("\n💡 建议:")
    print("1. 确保后端服务正在运行 (python start_server.py)")
    print("2. 使用真实的币安API Key进行完整测试")
    print("3. 建议先在测试网络上进行测试")

def test_frontend():
    """测试前端功能"""
    print("\n🌐 前端功能测试")
    print("=" * 30)

    try:
        # 测试前端服务器
        response = requests.get("http://localhost:8080", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务器运行正常")
        else:
            print("❌ 前端服务器异常")
    except:
        print("❌ 前端服务器未启动 (请运行: python -m http.server 8080)")

    try:
        # 测试前端页面
        response = requests.get("http://localhost:8080/币安代理交易系统.html", timeout=5)
        if response.status_code == 200:
            print("✅ 前端页面可访问")
        else:
            print("❌ 前端页面不可访问")
    except:
        print("❌ 前端页面访问失败")

if __name__ == "__main__":
    print("选择测试类型:")
    print("1. 后端API测试")
    print("2. 前端功能测试")
    print("3. 完整系统测试")

    choice = input("请输入选择 (1-3): ").strip()

    if choice == "1":
        test_system()
    elif choice == "2":
        test_frontend()
    elif choice == "3":
        test_system()
        test_frontend()
    else:
        print("❌ 无效选择")
        sys.exit(1)
