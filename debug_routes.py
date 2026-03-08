from fastapi import FastAPI
from routes import router

# 创建 FastAPI 应用
app = FastAPI()

# 添加根路径测试端点
@app.get("/")
async def root():
    routes_info = []
    for route in app.routes:
        routes_info.append({
            "path": route.path,
            "methods": getattr(route, "methods", None),
            "name": getattr(route, "name", None)
        })
    
    return {
        "message": "MathTools Switch Service is running",
        "total_routes": len(routes_info),
        "routes": routes_info
    }

# 注册路由
app.include_router(router)

# 添加调试端点来检查路由
@app.get("/debug/routes")
async def debug_routes():
    routes_info = []
    for route in app.routes:
        routes_info.append({
            "path": route.path,
            "methods": getattr(route, "methods", None),
            "name": getattr(route, "name", None)
        })
    
    return {
        "total_routes": len(routes_info),
        "routes": routes_info
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
