#!/bin/bash
# 启动主站本地预览服务器

set -e

PORT=${1:-8000}

echo "🚀 启动主站预览服务器..."
echo "📍 访问地址: http://localhost:$PORT"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 切换到项目根目录（本地直接 serve 源码树，子项目入口为各自的 dist/）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# 检查 Python 版本
if command -v python3 &> /dev/null; then
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    python -m http.server $PORT
else
    echo "❌ 错误: 未找到 Python，请安装 Python 3"
    exit 1
fi


