#!/usr/bin/env python3
"""
PhD Simulator 后端启动脚本
"""

import uvicorn
import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 启动 PhD Simulator 后端服务...")
    print("📖 API文档: http://localhost:8001/docs")
    print("🎮 游戏地址: http://localhost:8001")
    print("💾 数据库: phd_game.db")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
