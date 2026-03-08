# mathTools-switchService

## 项目介绍

mathTools-switchService 是一个基于 FastAPI 构建的中转服务，主要用于连接微信小程序和 Hugging Face 的 API 服务。该服务提供了用户认证和请求转发功能，确保只有合法用户能够访问 Hugging Face 服务。

## 核心功能

1. **微信小程序登录验证**：通过微信小程序的 code 换取 openid
2. **JWT Token 生成与验证**：为用户生成安全的访问令牌
3. **请求转发**：将经过验证的请求转发到 Hugging Face 的 API 服务

## 技术栈

- FastAPI：构建高性能 API
- httpx：发送异步 HTTP 请求
- pyjwt：JWT Token 处理
- python-dotenv：环境变量管理
- uvicorn：ASGI 服务器

## 安装步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd mathTools-switchService
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置环境变量**

项目提供了 `.env.example` 文件作为配置模板。复制该文件并重命名为 `.env`：

```bash
cp .env.example .env
```

然后编辑 `.env` 文件，填入你的实际配置值：

```
# Hugging Face 配置
HF_TOKEN=your_hugging_face_token_here
SPACE_URL=https://your-space-url.hf.space/api/predict

# 微信小程序配置
WX_APP_ID=your_wechat_app_id_here
WX_APP_SECRET=your_wechat_app_secret_here

# JWT 配置
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production
JWT_ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=120
```

**注意**：
- 切勿将 `.env` 文件提交到版本控制系统
- 已在 `.gitignore` 中添加了 `.env` 文件，确保敏感信息不会泄露

## API 接口

### 1. 登录接口

**POST /login**

**请求体**：
```json
{
  "code": "微信小程序登录 code"
}
```

**测试模式**：
使用 `code: "test_code"` 可以进行测试，无需真实的微信登录code：
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}'
```

**响应**：
```json
{
  "access_token": "JWT 令牌",
  "token_type": "bearer",
  "expires_in": 7200,
  "test_mode": true,
  "openid": "test_openid_12345"
}
```

### 2. 代理请求接口

**POST /proxy**

**请求头**：
```
Authorization: Bearer <access_token>
```

**请求体**：
```json
{
  "inputs": {"key": "value"}  // 传递给 Hugging Face 的数据
}
```

**响应**：
```json
// Hugging Face API 的返回数据
```

## 运行服务

```bash
python main.py
```

服务将在 `http://0.0.0.0:8000` 上运行。

## 生产环境部署

建议在生产环境中使用 Gunicorn 作为 WSGI 服务器，并配置适当的安全措施：

```bash
pip install gunicorn

# 启动服务
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## 安全注意事项

1. 切勿在代码中硬编码敏感信息，应使用环境变量
2. 在生产环境中使用强密码作为 JWT_SECRET
3. 定期更新依赖包以修复安全漏洞
4. 考虑添加请求速率限制以防止滥用

## 项目结构

```
mathTools-switchService/
├── config/           # 配置文件目录
│   ├── __init__.py
│   └── config.py     # 配置参数定义
├── models/           # 数据模型目录
│   ├── __init__.py
│   └── models.py     # Pydantic 数据模型
├── utils/            # 工具函数目录
│   ├── __init__.py
│   └── utils.py      # 工具函数定义
├── routes/           # 路由处理目录
│   ├── __init__.py
│   └── routes.py     # API 路由定义
├── main.py           # 应用入口
├── requirements.txt  # 依赖包列表
├── .env.example      # 环境变量示例文件
├── .gitignore        # Git 忽略文件
└── readme.md         # 项目说明
```

## 许可证

MIT License

