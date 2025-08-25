import requests
import json

def test_invalid_parameters():
    """测试无效参数处理"""
    base_url = "http://localhost:5000"
    user_id = "test_user_001"

    print("🧪 测试无效参数处理")
    print("=" * 50)

    # 测试1: 无效limit参数
    print("\n1. 测试无效limit参数:")
    try:
        response = requests.get(f"{base_url}/api/manual-orders/{user_id}?limit=invalid&status=all", timeout=10)
        print(f"状态码: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ 无效limit参数处理正确: {data.get('error', '未知错误')}")
        else:
            print(f"❌ 无效limit参数处理异常: 期望400，实际{response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

    # 测试2: 无效status参数
    print("\n2. 测试无效status参数:")
    try:
        response = requests.get(f"{base_url}/api/manual-orders/{user_id}?limit=10&status=invalid", timeout=10)
        print(f"状态码: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ 无效status参数处理正确: {data.get('error', '未知错误')}")
        else:
            print(f"❌ 无效status参数处理异常: 期望400，实际{response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

    # 测试3: 超出范围的limit参数
    print("\n3. 测试超出范围的limit参数:")
    try:
        response = requests.get(f"{base_url}/api/manual-orders/{user_id}?limit=2000&status=all", timeout=10)
        print(f"状态码: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ 超出范围limit参数处理正确: {data.get('error', '未知错误')}")
        else:
            print(f"❌ 超出范围limit参数处理异常: 期望400，实际{response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

    # 测试4: 负数limit参数
    print("\n4. 测试负数limit参数:")
    try:
        response = requests.get(f"{base_url}/api/manual-orders/{user_id}?limit=-1&status=all", timeout=10)
        print(f"状态码: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ 负数limit参数处理正确: {data.get('error', '未知错误')}")
        else:
            print(f"❌ 负数limit参数处理异常: 期望400，实际{response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

    # 测试5: 量化订单API的无效参数
    print("\n5. 测试量化订单API无效参数:")
    try:
        response = requests.get(f"{base_url}/api/quantified-orders/{user_id}?limit=invalid&status=all", timeout=10)
        print(f"状态码: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ 量化订单API无效参数处理正确: {data.get('error', '未知错误')}")
        else:
            print(f"❌ 量化订单API无效参数处理异常: 期望400，实际{response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

    print("\n" + "=" * 50)
    print("🎯 无效参数处理测试完成！")

if __name__ == "__main__":
    test_invalid_parameters()
