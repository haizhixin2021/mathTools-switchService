from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

# 创建 FastAPI 应用
app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建路由
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Server is running"}

@router.post("/login")
async def login():
    return {"message": "Login endpoint", "status": "success"}

@router.post("/proxy")
async def proxy():
    return {"message": "Proxy endpoint", "status": "success"}

# 注册路由
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    print("启动测试服务器...")
    print("可用的路由:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            print(f"  {route.methods} {route.path}")
    uvicorn.run(app, host="0.0.0.0", port=8002)
