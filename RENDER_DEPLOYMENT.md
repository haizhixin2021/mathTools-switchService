# Render 部署指南

## 部署准备

### 1. 创建 Render 账户

1. 访问 [https://render.com](https://render.com)
2. 注册或登录账户
3. 点击 "New +" 按钮创建新服务

### 2. 创建 Web Service

1. 选择 "Web Service" 类型
2. 填写服务信息：
   - **Name**: `mathTools-switchService`
   - **Region**: 选择离用户最近的区域
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. 配置环境变量

在 Render 的 "Environment" 部分添加以下环境变量：

```
# Hugging Face 配置
HF_TOKEN=your_hugging_face_token_here
SPACE_URL=https://haizhixin-mathtools.hf.space/

# 微信小程序配置
WX_APP_ID=your_wechat_app_id_here
WX_APP_SECRET=your_wechat_app_secret_here

# JWT 配置
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production
JWT_ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=120
```

**重要提示**：
- 所有敏感信息都应该在 Render 的环境变量中配置，不要在代码中硬编码
- `JWT_SECRET` 应该使用强密码，建议使用随机生成的密钥
- 不要将 `.env` 文件提交到 Git 仓库

### 4. 连接代码仓库

1. 在 Render 的 "Connect" 部分：
   - 选择 "GitHub" 或其他 Git 提供商
   - 授权 Render 访问您的代码仓库
   - 选择正确的仓库和分支

### 5. 部署

1. 点击 "Create Web Service" 按钮
2. 等待构建和部署完成
3. 部署完成后，Render 会提供一个公网 URL

## 使用 Docker 部署（可选）

如果需要使用 Docker 部署，可以按照以下步骤：

### 1. 修改 render.yaml

使用项目根目录下的 `render.yaml` 文件：

```yaml
services:
  - type: web
    name: mathTools-switchService
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: HF_TOKEN
        sync: false
      - key: SPACE_URL
        sync: false
      - key: WX_APP_ID
        sync: false
      - key: WX_APP_SECRET
        sync: false
      - key: JWT_SECRET
        sync: false
      - key: JWT_ALGORITHM
        sync: false
        value: HS256
      - key: TOKEN_EXPIRE_MINUTES
        sync: false
        value: 120
```

### 2. 在 Render 中使用 render.yaml

1. 在创建 Web Service 时，选择 "Deploy from Dockerfile"
2. 上传或引用 `render.yaml` 文件

## 验证部署

### 1. 检查服务状态

访问 Render 提供的 URL，应该看到：
```json
{
  "message": "MathTools Switch Service is running",
  "routes": [...]
}
```

### 2. 测试登录接口

```bash
curl -X POST "https://your-app-name.onrender.com/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}'
```

### 3. 测试代理接口

```bash
# 获取token
TOKEN=$(curl -s -X POST "https://your-app-name.onrender.com/login" \
  -H "Content-Type: application/json" \
  -d '{"code": "test_code"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# 测试代理接口
curl -X POST "https://your-app-name.onrender.com/proxy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"inputs": {"count": 20, "maxTotal": 20, "copies": 1, "title": "数学口算题", "operationType": "addition", "problemType": "normal", "difficulty": "simple", "useLLM": false}}'
```

## 监控和日志

### 1. 查看部署日志

1. 登录 Render 控制台
2. 选择您的服务
3. 点击 "Logs" 标签查看实时日志

### 2. 查看服务指标

Render 提供：
- CPU 使用率
- 内存使用情况
- 响应时间
- 错误率

## 常见问题

### 1. 构建失败

**原因**：
- 依赖安装失败
- Python 版本不兼容
- 代码语法错误

**解决**：
- 检查 `requirements.txt` 中的依赖是否正确
- 确认 Python 版本兼容性
- 查看构建日志获取详细错误信息

### 2. 环境变量未生效

**原因**：
- 环境变量名称拼写错误
- 环境变量值包含特殊字符

**解决**：
- 检查环境变量名称是否正确
- 重新部署服务
- 查看服务启动日志

### 3. 服务无法访问

**原因**：
- 防火墙阻止
- DNS 解析问题
- 服务启动失败

**解决**：
- 检查 Render 控制台中的服务状态
- 查看服务日志
- 确认端口配置正确

## 性能优化

### 1. 使用付费计划

Render 免费计划限制：
- 512MB RAM
- 0.1 CPU
- 750 小时/月运行时间

如果需要更好的性能，考虑升级到付费计划。

### 2. 优化代码

- 减少不必要的依赖
- 使用异步操作
- 实现缓存机制
- 优化数据库查询

## 安全建议

1. **使用 HTTPS**：Render 自动提供 SSL 证书
2. **环境变量**：所有敏感信息都通过环境变量配置
3. **定期更新**：及时更新依赖包修复安全漏洞
4. **监控日志**：定期检查服务日志发现异常
5. **限制访问**：实现请求速率限制防止滥用

## 成本估算

Render 免费计划：
- 免费 750 小时/月
- 适合开发和测试环境
- 生产环境建议使用付费计划

## 备份和恢复

### 1. 数据备份

- 环境变量在 Render 控制台中管理
- 代码在 Git 仓库中备份
- 日志可以下载保存

### 2. 灾难恢复

- 从 Git 仓库重新部署
- 重新配置环境变量
- 验证服务功能

## 联系支持

如果遇到问题：
- Render 文档：https://render.com/docs
- Render 社区：https://community.render.com
- 支持：support@render.com

## 快速部署命令

如果您想快速部署，可以使用 Render CLI：

```bash
# 安装 Render CLI
npm install -g render-cli

# 登录
render login

# 部署
render deploy
```

祝您部署顺利！
