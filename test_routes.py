import requests
import json

def test_endpoint(url, method="GET", data=None, headers=None):
    """测试API端点"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            return {"error": f"不支持的HTTP方法: {method}"}
        
        return {
            "status_code": response.status_code,
            "response": response.text,
            "success": response.status_code < 400
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

def main():
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("开始测试API端点")
    print("=" * 60)
    
    # 测试根路径
    print("\n1. 测试根路径 GET /")
    result = test_endpoint(f"{base_url}/", "GET")
    print(f"结果: {result}")
    
    # 测试调试路由
    print("\n2. 测试调试路由 GET /debug/routes")
    result = test_endpoint(f"{base_url}/debug/routes", "GET")
    print(f"结果: {result}")
    
    # 测试登录接口
    print("\n3. 测试登录接口 POST /login")
    result = test_endpoint(f"{base_url}/login", "POST", {"code": "test"})
    print(f"结果: {result}")
    
    # 测试代理接口（不带token）
    print("\n4. 测试代理接口 POST /proxy (无token)")
    result = test_endpoint(f"{base_url}/proxy", "POST", {"inputs": {"test": "data"}})
    print(f"结果: {result}")
    
    # 测试代理接口（带token）
    print("\n5. 测试代理接口 POST /proxy (带token)")
    # 先获取token
    login_result = test_endpoint(f"{base_url}/login", "POST", {"code": "test"})
    if login_result.get("success"):
        try:
            token_data = json.loads(login_result["response"])
            token = token_data.get("access_token")
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                result = test_endpoint(f"{base_url}/proxy", "POST", {"inputs": {"test": "data"}}, headers)
                print(f"结果: {result}")
            else:
                print("无法获取token")
        except:
            print("解析token失败")
    else:
        print("登录失败，无法测试带token的代理接口")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
