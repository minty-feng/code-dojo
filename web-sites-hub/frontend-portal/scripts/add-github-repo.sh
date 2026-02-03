#!/bin/bash
# 快速将 GitHub 仓库的 Markdown 文章集成到 Sphinx 博客

set -e

echo "🚀 Sphinx + GitHub 文章集成工具"
echo "================================"
echo ""

# 检查是否在博客目录
if [ ! -f "conf.py" ]; then
    echo "❌ 错误: 请在 blog 目录下运行此脚本"
    exit 1
fi

# 检查是否已安装依赖
if ! python3 -c "import sphinx" 2>/dev/null; then
    echo "📦 安装 Sphinx 依赖..."
    pip install -r ../requirements.txt
fi

# 1. 添加 GitHub 仓库
read -p "GitHub 仓库 URL (例如: https://github.com/user/repo): " REPO_URL
read -p "本地目录名 (默认: content/github-repo): " DIR_NAME
DIR_NAME=${DIR_NAME:-content/github-repo}

echo ""
echo "📚 添加 GitHub 仓库..."

# 创建 content 目录
mkdir -p content

# 检查是否已存在
if [ -d "$DIR_NAME" ]; then
    echo "⚠️  目录已存在，是否更新？(y/n)"
    read -r UPDATE
    if [ "$UPDATE" = "y" ]; then
        cd "$DIR_NAME"
        git pull origin main || git pull origin master
        cd ../..
    fi
else
    # 添加为子模块或直接克隆
    echo "选择添加方式:"
    echo "1) Git 子模块 (推荐，便于同步)"
    echo "2) 直接克隆"
    read -p "选择 (1/2): " METHOD
    
    if [ "$METHOD" = "1" ]; then
        git submodule add "$REPO_URL" "$DIR_NAME"
        git submodule update --init --recursive
    else
        git clone "$REPO_URL" "$DIR_NAME"
    fi
fi

# 2. 查找 Markdown 文件
echo ""
echo "🔍 查找 Markdown 文件..."
MD_FILES=$(find "$DIR_NAME" -name "*.md" -type f | head -10)

if [ -z "$MD_FILES" ]; then
    echo "⚠️  未找到 Markdown 文件"
else
    echo "找到以下文件:"
    echo "$MD_FILES" | nl
fi

# 3. 更新 conf.py
echo ""
echo "⚙️  更新 conf.py..."

# 检查是否已添加路径
if ! grep -q "content_path" conf.py; then
    cat >> conf.py << 'EOF'

# 支持 GitHub 仓库内容
import os
import sys
content_path = os.path.abspath('content')
sys.path.insert(0, content_path)
EOF
    echo "✅ 已添加内容路径配置"
else
    echo "ℹ️  内容路径已配置"
fi

# 4. 更新 index.rst
echo ""
echo "📝 更新 index.rst..."

# 询问是否自动添加
read -p "是否自动添加到 index.rst？(y/n): " AUTO_ADD

if [ "$AUTO_ADD" = "y" ]; then
    # 查找第一个 README.md 或 index.md
    FIRST_FILE=$(find "$DIR_NAME" -name "README.md" -o -name "index.md" | head -1)
    
    if [ -n "$FIRST_FILE" ]; then
        # 转换为相对路径（去掉 .md 扩展名）
        REL_PATH="${FIRST_FILE%.md}"
        REL_PATH="${REL_PATH#./}"
        
        # 添加到 index.rst
        if ! grep -q "$REL_PATH" index.rst; then
            # 在 toctree 中添加
            sed -i.bak "/^\.\. toctree::/a\\
   $REL_PATH" index.rst
            echo "✅ 已添加到 index.rst"
        else
            echo "ℹ️  文件已在 index.rst 中"
        fi
    else
        echo "⚠️  未找到 README.md 或 index.md，请手动添加到 index.rst"
    fi
fi

# 5. 构建测试
echo ""
echo "🏗️  构建测试..."
make clean > /dev/null 2>&1 || true

if make html > /dev/null 2>&1; then
    echo "✅ 构建成功！"
    echo ""
    echo "📋 预览站点:"
    echo "   cd _build/html && python3 -m http.server 8000"
    echo ""
    echo "🌐 访问: http://localhost:8000"
else
    echo "⚠️  构建失败，请检查错误信息"
    echo "运行 'make html' 查看详细错误"
fi

echo ""
echo "✅ 完成！"
echo ""
echo "📖 更多信息请查看: docs/SPHINX_GITHUB_GUIDE.md"







