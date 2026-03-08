# Hugging Face API 配置指南

## 问题分析

当前遇到的405错误表明Hugging Face Space的API端点不支持POST方法，或者需要不同的请求格式。

## 解决方案

### 1. 检查Hugging Face Space的API文档

首先需要确认您的Hugging Face Space支持哪种HTTP方法和请求格式：

1. 访问您的Space页面
2. 查看API文档或示例代码
3. 确认支持的HTTP方法（GET/POST）
4. 确认请求格式和参数

### 2. 常见的Hugging Face Space API格式

#### 格式1：使用POST方法（推荐）
```
POST https://your-space.hf.space/api/predict
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "data": ["input1", "input2"]
}
```

#### 格式2：使用GET方法
```
GET https://your-space.hf.space/api/predict?param1=value1&param2=value2
Authorization: Bearer YOUR_TOKEN
```

#### 格式3：使用Gradio API
```
POST https://your-space.hf.space/run/predict
Content-Type: application/json

{
  "data": ["input1", "input2"],
  "fn_index": 0
}
```

### 3. 更新配置

根据您的Space API格式，更新 `.env` 文件中的配置：

```bash
# 如果使用不同的API端点
SPACE_URL=https://your-space.hf.space/run/predict

# 如果不需要认证，可以留空
HF_TOKEN=
```

### 4. 测试Hugging Face API

使用curl直接测试Hugging Face API：

```bash
# 测试POST方法
curl -X POST "https://your-space.hf.space/api/predict" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"data": ["test input"]}'

# 测试GET方法
curl -X GET "https://your-space.hf.space/api/predict?input=test" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. 修改代理函数（如果需要）

如果您的Space需要特殊的请求格式，可以修改 `routes/routes.py` 中的代理函数：

```python
@router.post("/proxy")
async def proxy_hf_request(
    request: ProxyRequest, 
    current_user: str = Depends(get_current_user)
):
    print(f"用户 {current_user} 正在请求 HF 服务...")
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # 根据您的Space API格式调整请求
            response = await client.post(
                SPACE_URL, 
                json={"data": [request.inputs]},  # 调整数据格式
                headers=headers, 
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, 
                detail=f"HF Error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502, 
                detail=f"Connection to HF failed: {str(e)}"
            )
```

## 当前代码的改进

最新的代码已经包含了以下改进：

1. **自动尝试不同HTTP方法**：如果POST返回405，会自动尝试GET方法
2. **详细的调试信息**：在控制台输出请求详情，便于调试
3. **更好的错误处理**：提供更详细的错误信息

## 调试步骤

### 1. 查看服务日志

重启服务后，查看控制台输出的调试信息：
```
用户 test_openid_12345 正在请求 HF 服务...
请求URL: https://haizhixin-mathtools.hf.space/api/predict
请求数据: {'test': 'data'}
尝试POST方法...
POST方法不被允许，尝试GET方法...
```

### 2. 测试不同的请求格式

```bash
# 测试1：直接调用Hugging Face API
curl -X POST "https://haizhixin-mathtools.hf.space/api/predict" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# 测试2：使用Gradio API格式
curl -X POST "https://haizhixin-mathtools.hf.space/run/predict" \
  -H "Content-Type: application/json" \
  -d '{"data": ["test input"]}'

# 测试3：使用GET方法
curl -X GET "https://haizhixin-mathtools.hf.space/api/predict?test=data"
```

### 3. 访问Space页面

直接访问您的Space页面，查看API使用说明：
```
https://haizhixin-mathtools.hf.space
```

## 常见问题

### 1. 405 Method Not Allowed
- **原因**：HTTP方法不被支持
- **解决**：检查Space支持的HTTP方法，调整代码使用正确的方法

### 2. 401 Unauthorized
- **原因**：认证失败
- **解决**：检查HF_TOKEN是否正确，或者Space是否需要认证

### 3. 404 Not Found
- **原因**：API端点不存在
- **解决**：检查SPACE_URL是否正确

### 4. 500 Internal Server Error
- **原因**：Space内部错误
- **解决**：检查Space是否正常运行，查看Space日志

## 临时测试方案

如果您暂时没有可用的Hugging Face Space，可以使用以下方法进行测试：

### 1. 使用模拟响应
修改代理函数，返回模拟数据：

```python
@router.post("/proxy")
async def proxy_hf_request(
    request: ProxyRequest, 
    current_user: str = Depends(get_current_user)
):
    print(f"用户 {current_user} 正在请求 HF 服务...")
    print(f"请求数据: {request.inputs}")
    
    # 返回模拟响应
    return {
        "status": "success",
        "message": "模拟响应 - Hugging Face API未配置",
        "received_data": request.inputs,
        "timestamp": datetime.now().isoformat()
    }
```

### 2. 使用公共API
使用其他公共API进行测试，例如：

```bash
# 在.env文件中设置
SPACE_URL=https://jsonplaceholder.typicode.com/posts
HF_TOKEN=
```

## 下一步

1. **确认Space API格式**：查看您的Hugging Face Space的API文档
2. **更新配置**：根据API格式更新 `.env` 文件
3. **测试API**：使用curl直接测试Space API
4. **调整代码**：根据需要调整代理函数的请求格式
5. **重启服务**：应用更改并测试完整流程

## 联系支持

如果问题仍然存在，可以：
- 查看Hugging Face Space的日志
- 联系Space的作者
- 在Hugging Face社区寻求帮助
