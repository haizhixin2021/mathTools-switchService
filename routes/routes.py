from fastapi import APIRouter, HTTPException, Depends, Response
import httpx
from datetime import timedelta
from models import LoginRequest, ProxyRequest
from utils import create_access_token, get_current_user
from config import WX_APP_ID, WX_APP_SECRET, HF_TOKEN, SPACE_URL, TOKEN_EXPIRE_MINUTES
import time

router = APIRouter()

# ================= 接口定义 =================

@router.get("/health")
async def health_check():
    """
    健康检查接口
    返回服务状态和基本信息
    """
    return {
        "status": "healthy",
        "service": "mathTools-switchService",
        "timestamp": int(time.time()),
        "version": "1.0.0",
        "endpoints": {
            "login": "/login",
            "proxy": "/proxy",
            "health": "/health"
        }
    }

@router.post("/login")
async def login(request: LoginRequest):
    """
    1. 用 code 换取 openid
    2. 生成 JWT Token
    """
    # 测试模式：如果code是test_code，直接返回测试token
    if request.code == "test_code":
        test_openid = "test_openid_12345"
        access_token = create_access_token(
            data={"sub": test_openid}, 
            expires_delta=timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": TOKEN_EXPIRE_MINUTES * 60,
            "test_mode": True,
            "openid": test_openid
        }
    
    # 正常模式：调用微信API
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": WX_APP_ID,
        "secret": WX_APP_SECRET,
        "js_code": request.code,
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, timeout=10.0)
        data = resp.json()
        
        if "openid" not in data:
            # 微信返回错误，可能是 code 无效或过期
            err_msg = data.get("errmsg", "Unknown WeChat Error")
            raise HTTPException(status_code=400, detail=f"WeChat login failed: {err_msg}")
        
        openid = data["openid"]
        
        # 生成 Token
        access_token = create_access_token(
            data={"sub": openid}, 
            expires_delta=timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": TOKEN_EXPIRE_MINUTES * 60
        }

@router.post("/proxy")
async def proxy_hf_request(
    request: ProxyRequest, 
    current_user: str = Depends(get_current_user)
):
    """
    1. 验证 JWT Token (自动通过 Depends 完成)
    2. 转发请求到 HF
    """
    print(f"用户 {current_user} 正在请求 HF 服务...")
    print(f"请求URL: {SPACE_URL}")
    print(f"请求内容: {request.inputs}")
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    # 从 inputs 中获取实际的请求路径和数据
    inputs = request.inputs
    path = inputs.get("path", "")
    data = inputs.get("data", {})
    method = inputs.get("method", "POST")  # 默认使用 POST 方法

    
    # 构建完整的请求 URL
    target_url = f"{SPACE_URL}{path}"

    print(f"目标URL: {target_url}")
    print(f"请求数据: {data}")
    print(f"请求方法: {method}")
    
    async with httpx.AsyncClient() as client:
        try:
            # 根据方法发送请求
            if method.upper() == "GET":
                # GET 请求使用 params
                response = await client.get(
                    target_url,
                    params=data,
                    headers=headers,
                    timeout=30.0
                )
            else:
                # POST 等其他方法使用 json
                response = await client.post(
                    target_url, 
                    json=data, 
                    headers=headers, 
                    timeout=30.0
                )
            
            response.raise_for_status()
            print(f"请求成功，状态码: {response.status_code}")
            print(f"响应Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            # 检查响应类型
            content_type = response.headers.get('content-type', '').lower()
            
            # 如果是PDF文件，直接返回二进制数据
            if 'pdf' in content_type or response.content.startswith(b'%PDF'):
                print("检测到PDF文件，返回二进制数据")
                return Response(
                    content=response.content,
                    media_type="application/pdf",
                    headers={
                        "Content-Disposition": "attachment; filename=math_problems.pdf"
                    }
                )
            
            # 尝试解析JSON响应
            try:
                return response.json()
            except ValueError as e:
                # 如果响应不是有效的JSON，返回原始响应
                print(f"JSON解析错误: {str(e)}")
                print(f"原始响应: {response.text[:200]}...")
                return {
                    "status": "success",
                    "message": "Non-JSON response from HF",
                    "raw_response": response.text[:1000],
                    "status_code": response.status_code
                }
            
        except httpx.HTTPStatusError as e:
            print(f"HTTP错误: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code, 
                detail=f"HF Error: {e.response.text}"
            )
        except httpx.RequestError as e:
            print(f"请求错误: {str(e)}")
            raise HTTPException(
                status_code=502, 
                detail=f"Connection to HF failed: {str(e)}"
            )
        except Exception as e:
            print(f"未知错误: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
