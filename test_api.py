import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """测试根路径"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"根路径测试: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"根路径测试失败: {e}")
        return False

def test_login():
    """测试登录接口"""
    try:
        # 使用测试code
        payload = {
            "code": "test_code"
        }
        response = requests.post(f"{BASE_URL}/login", json=payload)
        print(f"登录接口测试: {response.status_code}")
        print(f"响应: {response.text}")
        return response.status_code, response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"登录接口测试失败: {e}")
        return None, None

def test_proxy():
    """测试代理接口（需要先登录获取token）"""
    try:
        # 先获取token
        login_payload = {"code": "test_code"}
        login_response = requests.post(f"{BASE_URL}/login", json=login_payload)
        
        if login_response.status_code != 200:
            print(f"登录失败，无法测试代理接口")
            return None
        
        token_data = login_response.json()
        token = token_data.get("access_token")
        
        if not token:
            print("无法获取token")
            return None
        
        print(f"成功获取token: {token[:20]}...")
        
        # 测试代理接口
        headers = {
            "Authorization": f"Bearer {token}"
        }
        proxy_payload = {
            "inputs": {"test": "data"}
        }
        
        response = requests.post(f"{BASE_URL}/proxy", json=proxy_payload, headers=headers)
        print(f"代理接口测试: {response.status_code}")
        print(f"响应: {response.text}")
        return response.status_code
    except Exception as e:
        print(f"代理接口测试失败: {e}")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("开始API测试")
    print("=" * 50)
    
    # 测试根路径
    print("\n1. 测试根路径:")
    test_root()
    
    # 测试登录接口
    print("\n2. 测试登录接口:")
    test_login()
    
    # 测试代理接口
    print("\n3. 测试代理接口:")
    test_proxy()
    
    print("\n" + "=" * 50)
    print("API测试完成")
    print("=" * 50)
