from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

# 创建 FastAPI 应用
app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加根路径测试端点
@app.get("/")
async def root():
    routes_list = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes_list.append({
                "path": route.path,
                "methods": list(route.methods) if route.methods else []
            })
    
    return {
        "message": "MathTools Switch Service is running",
        "routes": routes_list
    }

# 注册路由，确保没有前缀
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # 生产环境请使用 gunicorn 或设置 host=0.0.0.0
    print("启动服务...")
    print("可用的路由:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            print(f"  {route.methods} {route.path}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
