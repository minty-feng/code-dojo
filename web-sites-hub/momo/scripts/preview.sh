#!/bin/bash
# 启动主站本地预览服务器

set -e

PORT=${1:-8000}

echo "🚀 启动主站预览服务器..."
echo "📍 访问地址: http://localhost:$PORT"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 检查 Python 版本
if command -v python3 &> /dev/null; then
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    python -m http.server $PORT
else
    echo "❌ 错误: 未找到 Python，请安装 Python 3"
    exit 1
fi


