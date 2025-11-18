#!/bin/bash
# 首次构建脚本
# 用于第一次构建 Sphinx 文档

set -e  # 遇到错误立即退出

echo "Mini Program Tutorial - Initial Build Script"
echo "================================"
echo ""

# 检查 Python 版本
echo "📋 检查 Python 环境..."
python3 --version || { echo "❌ Python3 未安装"; exit 1; }

# 检查是否在正确的目录
if [ ! -f "conf.py" ]; then
    echo "❌ 请在项目根目录下运行此脚本"
    exit 1
fi

# 创建虚拟环境（推荐）
VENV_DIR="${VENV_DIR:-venv}"
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
fi

# 激活虚拟环境
echo "🔌 激活虚拟环境..."
source "$VENV_DIR/bin/activate"

# 升级 pip
echo "📥 升级 pip..."
python3 -m pip install -q --upgrade pip

# 安装依赖
echo "📥 安装依赖..."
python3 -m pip install -q -r requirements.txt


# 清理旧的构建
echo "🧹 清理旧构建..."
rm -rf _build/html

# 构建文档
echo "🔨 构建 HTML 文档..."
python3 -m sphinx -b html . _build/html

# 验证构建结果
if [ ! -f "_build/html/index.html" ]; then
    echo "❌ 构建失败：index.html 未找到"
    exit 1
fi

echo ""
echo "✅ 构建成功！"
echo ""
echo "📊 构建统计："
HTML_COUNT=$(find _build/html -name "*.html" | wc -l)
SIZE=$(du -sh _build/html | cut -f1)
echo "  - HTML 文件数量: $HTML_COUNT"
echo "  - 构建目录大小: $SIZE"
echo ""
echo "💡 提示：构建完成后，可以使用以下脚本："
echo "  - package-nginx.sh  # 创建 Nginx 部署包"

