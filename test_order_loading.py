import requests
import json

def test_order_loading():
    """测试订单加载功能"""
    base_url = "http://localhost:5000"
    user_id = "test_user_001"

    print("🧪 测试订单加载功能")
    print("=" * 50)

    # 测试手动订单API
    print("\n1. 测试手动订单API:")
    try:
        response = requests.get(f"{base_url}/api/manual-orders/{user_id}?limit=10&status=all")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ 手动订单API正常")
                print(f"   订单数量: {data['count']}")
                print(f"   总收益: ${data['summary']['total_pnl']:.2f}")
                print(f"   胜率: {data['summary']['win_rate']:.1f}%")
            else:
                print(f"❌ 手动订单API返回错误: {data.get('error', '未知错误')}")
        else:
            print(f"❌ 手动订单API请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 手动订单API测试异常: {e}")

    # 测试量化订单API
    print("\n2. 测试量化订单API:")
    try:
        response = requests.get(f"{base_url}/api/quantified-orders/{user_id}?limit=10&status=all")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ 量化订单API正常")
                print(f"   订单数量: {data['count']}")
                print(f"   总收益: ${data['summary']['total_pnl']:.2f}")
                print(f"   胜率: {data['summary']['win_rate']:.1f}%")
            else:
                print(f"❌ 量化订单API返回错误: {data.get('error', '未知错误')}")
        else:
            print(f"❌ 量化订单API请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 量化订单API测试异常: {e}")

    # 测试错误的用户ID
    print("\n3. 测试错误用户ID:")
    try:
        response = requests.get(f"{base_url}/api/manual-orders/wrong_user?limit=10&status=all")
        if response.status_code == 200:
            data = response.json()
            if data['success'] and data['count'] == 0:
                print(f"✅ 错误用户ID处理正常 (返回空数据)")
            else:
                print(f"⚠️ 错误用户ID处理异常")
        else:
            print(f"❌ 错误用户ID请求失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 错误用户ID测试异常: {e}")

    print("\n" + "=" * 50)
    print("🎯 测试完成！")

if __name__ == "__main__":
    test_order_loading()
