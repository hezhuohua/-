import requests
import json

def debug_parameter_handling():
    """调试参数处理机制"""
    base_url = "http://localhost:5000"
    user_id = "test_user_001"

    print("🔍 调试参数处理机制")
    print("=" * 50)

    # 测试1: 检查Flask如何处理无效参数
    print("\n1. 测试Flask参数处理:")
    try:
        response = requests.get(f"{base_url}/api/manual-orders/{user_id}?limit=invalid&status=all", timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

    # 测试2: 检查type=int的行为
    print("\n2. 测试type=int行为:")
    test_cases = [
        "limit=abc",
        "limit=123.45",
        "limit=-1",
        "limit=0",
        "limit=1001"
    ]

    for test_case in test_cases:
        try:
            response = requests.get(f"{base_url}/api/manual-orders/{user_id}?{test_case}&status=all", timeout=10)
            print(f"{test_case}: HTTP {response.status_code}")
        except Exception as e:
            print(f"{test_case}: 错误 - {e}")

    print("\n" + "=" * 50)
    print("🎯 参数处理调试完成！")

if __name__ == "__main__":
    debug_parameter_handling()
