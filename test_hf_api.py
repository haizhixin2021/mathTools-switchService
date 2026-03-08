import requests
import json

def test_hf_api():
    """测试Hugging Face API端点"""
    
    # 测试直接访问HF API
    url = "https://haizhixin-mathtools.hf.space/api/generate"
    
    # 测试数据
    test_data = {
        "maxTotal": 20,
        "operationType": "addition",
        "count": 5
    }
    
    print(f"测试HF API: {url}")
    print(f"请求数据: {test_data}")
    
    try:
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30.0
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        # 尝试解析JSON
        try:
            result = response.json()
            print(f"JSON响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return True
        except ValueError:
            print(f"非JSON响应: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("测试Hugging Face API")
    print("=" * 60)
    
    success = test_hf_api()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ API测试成功")
    else:
        print("❌ API测试失败")
    print("=" * 60)
