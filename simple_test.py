from fastapi import FastAPI, APIRouter

# 创建 FastAPI 应用
app = FastAPI()

# 创建简单的路由
router = APIRouter()

@router.get("/test-get")
async def test_get():
    return {"message": "GET request successful"}

@router.post("/test-post")
async def test_post():
    return {"message": "POST request successful"}

@router.post("/login")
async def login():
    return {"message": "Login endpoint working"}

@router.post("/proxy")
async def proxy():
    return {"message": "Proxy endpoint working"}

# 注册路由
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    print("启动简单测试服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
