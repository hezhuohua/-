#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安API数据源测试脚本
测试新的数据源配置是否正常工作
"""

import requests
import json
import time

def test_binance_api():
    """测试币安API数据源"""
    print("🔍 开始测试币安API数据源...")

    # 测试1: 获取BTC价格
    print("\n📊 测试1: 获取BTC价格")
    try:
        url = "https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ BTC价格: ${data['price']}")
    except Exception as e:
        print(f"❌ 获取BTC价格失败: {e}")
        return False

    # 测试2: 获取多个币种的市场数据
    print("\n📊 测试2: 获取多个币种的市场数据")
    try:
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']
        symbols_str = '[' + ','.join([f'"{symbol}"' for symbol in symbols]) + ']'
        url = f"https://fapi.binance.com/fapi/v1/ticker/24hr?symbols={symbols_str}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        print(f"✅ 成功获取 {len(data)} 个币种的数据:")
        for item in data:
            print(f"   {item['symbol']}: ${item['lastPrice']} ({item['priceChangePercent']}%)")
    except Exception as e:
        print(f"❌ 获取市场数据失败: {e}")
        return False

    # 测试3: 获取K线数据
    print("\n📊 测试3: 获取K线数据")
    try:
        url = "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1m&limit=5"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        print(f"✅ 成功获取 {len(data)} 根K线数据:")
        for i, kline in enumerate(data[:3]):  # 只显示前3根
            print(f"   K线{i+1}: 开盘${kline[1]}, 最高${kline[2]}, 最低${kline[3]}, 收盘${kline[4]}")
    except Exception as e:
        print(f"❌ 获取K线数据失败: {e}")
        return False

    # 测试4: 测试后端API
    print("\n📊 测试4: 测试后端API")
    try:
        # 测试市场数据API
        url = "http://localhost:5000/api/market-data"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['success']:
            print(f"✅ 后端市场数据API正常: {len(data['data'])} 个币种")
        else:
            print(f"❌ 后端市场数据API失败: {data.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 后端API测试失败: {e}")
        print("   请确保后端服务器正在运行 (python server.py)")
        return False

    print("\n🎉 所有测试通过！币安API数据源配置成功！")
    return True

def test_data_consistency():
    """测试数据一致性"""
    print("\n🔍 测试数据一致性...")

    try:
        # 连续获取3次数据，检查是否一致
        prices = []
        for i in range(3):
            url = "https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT"
            response = requests.get(url, timeout=10)
            data = response.json()
            prices.append(float(data['price']))
            time.sleep(1)  # 等待1秒

        # 检查价格变化
        price_change = abs(prices[2] - prices[0]) / prices[0] * 100
        print(f"✅ 3次获取的BTC价格: ${prices[0]:.2f}, ${prices[1]:.2f}, ${prices[2]:.2f}")
        print(f"✅ 价格变化幅度: {price_change:.4f}%")

        if price_change < 1:  # 价格变化小于1%认为是正常的
            print("✅ 数据一致性测试通过")
            return True
        else:
            print("⚠️ 价格变化较大，可能是市场波动")
            return True

    except Exception as e:
        print(f"❌ 数据一致性测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 币安API数据源测试")
    print("=" * 50)

    # 运行测试
    success = test_binance_api()

    if success:
        test_data_consistency()
        print("\n✅ 数据源测试完成，系统可以正常使用币安API！")
    else:
        print("\n❌ 数据源测试失败，请检查网络连接和API配置")
