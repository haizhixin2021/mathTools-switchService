# API 测试指南

## 测试环境准备

1. **确保服务正在运行**
   ```bash
   python main.py
   ```

2. **检查服务状态**
   ```bash
   curl http://localhost:8000/
   ```

## 测试流程

### 1. 测试登录接口

**使用测试模式（推荐）**：
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}'
```

**预期响应**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 7200,
  "test_mode": true,
  "openid": "test_openid_12345"
}
```

**使用真实微信code**：
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "真实的微信登录code"}'
```

### 2. 测试代理接口

**步骤1：获取token**
```bash
# 保存token到变量
TOKEN=$(curl -s -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}' | jq -r '.access_token')
```

**步骤2：调用代理接口**
```bash
curl -X POST "http://localhost:8000/proxy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"inputs": {"your": "data"}}'
```

**完整示例**：
```bash
# 一步完成登录和代理调用
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}' | jq -r '.access_token' > token.txt

TOKEN=$(cat token.txt)

curl -X POST "http://localhost:8000/proxy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"inputs": {"test": "data"}}'
```

### 3. 使用Python测试脚本

```bash
python test_api.py
```

或者：

```bash
python test_routes.py
```

## 常见问题

### 1. 405 Method Not Allowed
- **原因**：HTTP方法不匹配
- **解决**：确保使用POST方法调用 `/login` 和 `/proxy` 接口

### 2. 401 Unauthorized
- **原因**：缺少或无效的Authorization头
- **解决**：确保在调用 `/proxy` 时提供有效的Bearer token

### 3. 400 Bad Request
- **原因**：请求体格式错误或缺少必要参数
- **解决**：检查JSON格式是否正确，确保包含 `code` 或 `inputs` 字段

### 4. 502 Bad Gateway
- **原因**：无法连接到Hugging Face服务
- **解决**：检查 `.env` 文件中的 `SPACE_URL` 和 `HF_TOKEN` 配置

## 调试技巧

### 1. 查看服务日志
服务启动时会显示所有可用的路由：
```
启动服务...
可用的路由:
  {'GET'} /
  {'POST'} /login
  {'POST'} /proxy
```

### 2. 访问API文档
FastAPI自动生成交互式API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. 使用curl的verbose模式
```bash
curl -v -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}'
```

### 4. 检查请求和响应
```bash
# 查看完整的响应头
curl -i -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}'

# 格式化JSON响应
curl -s -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}' | jq
```

## 性能测试

使用Apache Bench进行简单的性能测试：
```bash
# 安装ab工具
brew install ab  # macOS
# 或
sudo apt-get install apache2-utils  # Ubuntu

# 测试登录接口
ab -n 100 -c 10 -T "application/json" \
  -p login_data.json \
  http://localhost:8000/login

# login_data.json内容：
# {"code": "test_code"}
```

## 安全测试

### 1. 测试未授权访问
```bash
# 不带token访问代理接口
curl -X POST "http://localhost:8000/proxy" \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"test": "data"}}'
# 预期：401 Unauthorized
```

### 2. 测试无效token
```bash
# 使用无效token
curl -X POST "http://localhost:8000/proxy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token" \
  -d '{"inputs": {"test": "data"}}'
# 预期：401 Unauthorized
```

### 3. 测试过期token
```bash
# 使用过期token（需要修改TOKEN_EXPIRE_MINUTES为较小值）
# 预期：401 Unauthorized with "Token has expired"
```

## 集成测试示例

### Python脚本示例
```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_full_workflow():
    # 1. 登录获取token
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={"code": "test_code"}
    )
    
    if login_response.status_code != 200:
        print(f"登录失败: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    print(f"登录成功，获取token: {token[:20]}...")
    
    # 2. 调用代理接口
    proxy_response = requests.post(
        f"{BASE_URL}/proxy",
        headers={"Authorization": f"Bearer {token}"},
        json={"inputs": {"test": "data"}}
    )
    
    print(f"代理调用结果: {proxy_response.status_code}")
    print(f"响应: {proxy_response.text}")

if __name__ == "__main__":
    test_full_workflow()
```

## 总结

- ✅ 使用 `test_code` 进行快速测试
- ✅ 确保所有POST请求都包含正确的Content-Type头
- ✅ 调用 `/proxy` 时必须提供有效的Bearer token
- ✅ 使用API文档 (http://localhost:8000/docs) 进行交互式测试
- ✅ 检查服务日志获取详细的错误信息
