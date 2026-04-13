"""
🎮 PhD Simulator 后端主程序

这个模块是FastAPI应用的主入口，负责:
- 创建和配置FastAPI应用实例
- 设置CORS跨域访问策略
- 挂载静态文件服务
- 注册API路由
- 初始化数据库
- 提供健康检查和根路径访问

🔗 主要功能:
- 游戏数据API服务 (/api/*)
- 静态文件服务 (前端游戏文件)
- 健康检查端点 (/health)
- API文档自动生成 (/docs)

📡 网络配置:
- 监听地址: 0.0.0.0 (所有网络接口)
- 默认端口: 8001
- 支持热重载 (开发环境)
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from models.database import create_tables
from api.game_api import router as game_router

# 🗄️ 应用启动事件
# 在应用启动时自动执行数据库初始化
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 📊 创建数据库表结构
    create_tables()
    print("✅ 数据库表创建完成")
    yield

# 🚀 创建FastAPI应用实例
app = FastAPI(
    title="PhD Simulator Backend",           # 📱 应用标题
    description="记录玩家游戏数据的后端API",  # 📝 应用描述
    version="1.0.0",                         # 🏷️ 版本号
    lifespan=lifespan                        # 🔄 生命周期管理
)

# 🌐 配置CORS跨域访问策略
# 允许前端从不同域名访问后端API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 🌍 允许所有来源 (生产环境应该限制具体域名)
    allow_credentials=True,       # 🔐 允许携带认证信息
    allow_methods=["*"],          # 📡 允许所有HTTP方法
    allow_headers=["*"],          # 📋 允许所有请求头
)

# 🔗 注册API路由
# 将所有游戏相关的API端点注册到应用
app.include_router(game_router, prefix="/api", tags=["game"])
print("✅ API路由已注册: /api/*")

# 📁 挂载静态文件服务
# 将前端构建后的文件作为静态资源提供服务
if os.path.exists("../dist"):
    # 🎮 将 /static 路径映射到前端静态文件目录
    app.mount("/static", StaticFiles(directory="../dist"), name="static")
    print("✅ 静态文件服务已挂载: /static -> ../dist")
    
    # 🎮 添加对根路径下静态资源的支持
    from fastapi.responses import FileResponse
    from fastapi import HTTPException
    
    @app.get("/{file_path:path}")
    async def serve_static_files(file_path: str):
        # 如果是API路径，跳过
        if file_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 尝试从dist目录提供文件
        file_path_full = f"../dist/{file_path}"
        if os.path.exists(file_path_full) and os.path.isfile(file_path_full):
            return FileResponse(file_path_full)
        
        # 如果文件不存在，返回index.html（支持SPA路由）
        index_path = "../dist/index.html"
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        raise HTTPException(status_code=404, detail="File not found")
    
elif os.path.exists("../static"):
    # 🎮 备用：如果dist目录不存在，使用static目录
    app.mount("/static", StaticFiles(directory="../static"), name="static")
    print("✅ 静态文件服务已挂载: /static -> ../static")
else:
    print("⚠️ 静态文件目录未找到，仅提供API服务")

# 🏠 根路径访问
# 提供API服务的基本信息或前端文件
@app.get("/")
async def root():
    # 检查是否有前端文件
    if os.path.exists("../static/index.html"):
        from fastapi.responses import FileResponse
        return FileResponse("../static/index.html")
    elif os.path.exists("../dist/index.html"):
        from fastapi.responses import FileResponse
        return FileResponse("../dist/index.html")
    else:
        # 如果没有前端文件，返回API信息
        return {
            "message": "PhD Simulator Backend API",
            "docs": "/docs",                    # 📖 API文档链接
            "health": "/health",                # 🔍 健康检查链接
            "api_endpoints": "/api/*"           # 🌐 API端点路径
        }

# 🔍 健康检查端点
# 用于监控系统检查后端服务是否正常运行
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",                # ✅ 服务状态
        "service": "PhD Simulator Backend", # 🏷️ 服务名称
        "version": "1.0.0"                  # 🏷️ 版本信息
    }



# 🚀 主程序入口
# 当直接运行此文件时启动开发服务器
if __name__ == "__main__":
    import uvicorn
    
    # 🌐 启动开发服务器
    uvicorn.run(
        app,                    # 🚀 FastAPI应用实例
        host="0.0.0.0",        # 🌍 监听所有网络接口
        port=8001              # 🔌 监听端口
    )
