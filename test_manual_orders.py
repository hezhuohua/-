#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动订单功能测试脚本
测试新增的手动订单API和数据库功能
"""

import requests
import json
import sqlite3
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:5000"
TEST_USER_ID = "test_user_001"

def test_database_structure():
    """测试数据库结构是否包含order_type字段"""
    print("🔍 测试数据库结构...")

    try:
        conn = sqlite3.connect("trading_system.db")
        cursor = conn.cursor()

        # 检查trade_records表结构
        cursor.execute("PRAGMA table_info(trade_records)")
        columns = cursor.fetchall()

        order_type_exists = any(col[1] == 'order_type' for col in columns)

        if order_type_exists:
            print("✅ order_type字段已存在")
        else:
            print("❌ order_type字段不存在")

        conn.close()
        return order_type_exists

    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_manual_order_api():
    """测试手动订单API"""
    print("\n🔍 测试手动订单API...")

    try:
        # 测试获取手动订单
        response = requests.get(f"{BASE_URL}/api/manual-orders/{TEST_USER_ID}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 手动订单API调用成功")
                print(f"   订单数量: {data.get('count', 0)}")
                print(f"   总收益: ${data.get('summary', {}).get('total_pnl', 0):.2f}")
                return True
            else:
                print(f"❌ API返回错误: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ API调用失败: {e}")
        return False

def test_quantified_order_api():
    """测试量化订单API"""
    print("\n🔍 测试量化订单API...")

    try:
        # 测试获取量化订单
        response = requests.get(f"{BASE_URL}/api/quantified-orders/{TEST_USER_ID}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 量化订单API调用成功")
                print(f"   订单数量: {data.get('count', 0)}")
                print(f"   总收益: ${data.get('summary', {}).get('total_pnl', 0):.2f}")
                return True
            else:
                print(f"❌ API返回错误: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ API调用失败: {e}")
        return False

def test_trade_execution():
    """测试交易执行API（手动下单）"""
    print("\n🔍 测试手动下单功能...")

    try:
        # 模拟手动下单请求
        trade_data = {
            "user_id": TEST_USER_ID,
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": "0.001",
            "order_type": "manual",  # 新增：指定为手动订单
            "take_profit": 45000,
            "stop_loss": 42000
        }

        response = requests.post(f"{BASE_URL}/api/trade", json=trade_data)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 手动下单API调用成功")
                print(f"   订单ID: {data.get('data', {}).get('order_id')}")
                print(f"   订单类型: {data.get('data', {}).get('order_type')}")
                return True
            else:
                print(f"❌ 下单失败: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 下单API调用失败: {e}")
        return False

def add_test_data():
    """添加测试数据到数据库"""
    print("\n🔍 添加测试数据...")

    try:
        conn = sqlite3.connect("trading_system.db")
        cursor = conn.cursor()

        # 添加手动订单测试数据
        manual_order = {
            'user_id': TEST_USER_ID,
            'order_id': f"MANUAL{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'symbol': 'ETHUSDT',
            'side': 'SELL',
            'price': 2680.5,
            'quantity': 0.01,
            'status': 'FILLED',
            'order_type': 'manual',  # 手动订单
            'take_profit': 2650,
            'stop_loss': 2700,
            'pnl': -5.25,
            'executed_at': datetime.now().isoformat()
        }

        cursor.execute('''
            INSERT INTO trade_records
            (user_id, order_id, symbol, side, price, quantity, status, order_type, take_profit, stop_loss, pnl, executed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            manual_order['user_id'],
            manual_order['order_id'],
            manual_order['symbol'],
            manual_order['side'],
            manual_order['price'],
            manual_order['quantity'],
            manual_order['status'],
            manual_order['order_type'],
            manual_order['take_profit'],
            manual_order['stop_loss'],
            manual_order['pnl'],
            manual_order['executed_at']
        ))

        # 添加量化订单测试数据
        quantified_order = {
            'user_id': TEST_USER_ID,
            'order_id': f"AI{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'price': 43250.0,
            'quantity': 0.001,
            'status': 'FILLED',
            'order_type': 'quantified',  # 量化订单
            'take_profit': 44000,
            'stop_loss': 42800,
            'pnl': 25.50,
            'executed_at': datetime.now().isoformat()
        }

        cursor.execute('''
            INSERT INTO trade_records
            (user_id, order_id, symbol, side, price, quantity, status, order_type, take_profit, stop_loss, pnl, executed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            quantified_order['user_id'],
            quantified_order['order_id'],
            quantified_order['symbol'],
            quantified_order['side'],
            quantified_order['price'],
            quantified_order['quantity'],
            quantified_order['status'],
            quantified_order['order_type'],
            quantified_order['take_profit'],
            quantified_order['stop_loss'],
            quantified_order['pnl'],
            quantified_order['executed_at']
        ))

        conn.commit()
        conn.close()
        print("✅ 测试数据添加成功")
        return True

    except Exception as e:
        print(f"❌ 添加测试数据失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试手动订单功能")
    print("=" * 50)

    # 测试数据库结构
    db_ok = test_database_structure()

    # 添加测试数据
    if db_ok:
        add_test_data()

    # 测试API功能
    manual_api_ok = test_manual_order_api()
    quantified_api_ok = test_quantified_order_api()
    trade_api_ok = test_trade_execution()

    # 总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"   数据库结构: {'✅ 通过' if db_ok else '❌ 失败'}")
    print(f"   手动订单API: {'✅ 通过' if manual_api_ok else '❌ 失败'}")
    print(f"   量化订单API: {'✅ 通过' if quantified_api_ok else '❌ 失败'}")
    print(f"   交易执行API: {'✅ 通过' if trade_api_ok else '❌ 失败'}")

    if all([db_ok, manual_api_ok, quantified_api_ok, trade_api_ok]):
        print("\n🎉 所有测试通过！手动订单功能已完善")
    else:
        print("\n⚠️ 部分测试失败，请检查相关功能")

if __name__ == "__main__":
    main()
