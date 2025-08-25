#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本
"""

print("🚀 Python测试开始...")

try:
    import requests
    print("✅ requests库已安装")

    # 测试币安API
    print("🔍 测试币安API...")
    response = requests.get("https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT", timeout=10)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ BTC价格: ${data['price']}")
        print("🎉 币安API测试成功！")
    else:
        print(f"❌ API请求失败: {response.status_code}")

except ImportError:
    print("❌ requests库未安装")
except Exception as e:
    print(f"❌ 测试失败: {e}")

print("🏁 测试完成")
