from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routers import dashboard
import os

app = FastAPI(title="Dashboard Backend")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

# 确保static目录存在
os.makedirs(static_dir, exist_ok=True)

# 根路由重定向到index.html
@app.get("/")
async def root():
    return RedirectResponse(url="/web/index.html")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/web", StaticFiles(directory=os.path.join(static_dir, "web")), name="web")

# 注册路由
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 