#!/bin/bash
# joketop 项目部署脚本
# 用于解压和部署 joketop 项目到指定目录

set -e

# 配置变量
DEPLOY_DIR="/var/www/html/joketop"

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请使用 sudo 运行此脚本"
    exit 1
fi

# 检查参数
if [ -z "$1" ]; then
    echo "用法: $0 <打包文件.tar.gz>"
    echo ""
    echo "示例:"
    echo "  sudo ./deploy-joketop.sh joketop-20241105-195319.tar.gz"
    exit 1
fi

PACKAGE_FILE="$1"

# 检查打包文件是否存在
if [ ! -f "$PACKAGE_FILE" ]; then
    echo "❌ 打包文件不存在: $PACKAGE_FILE"
    exit 1
fi

echo "🚀 joketop 项目部署脚本"
echo "=================="
echo "部署目录: $DEPLOY_DIR"
echo "打包文件: $PACKAGE_FILE"
echo ""

# 创建部署目录
echo "📁 创建部署目录..."
mkdir -p "$DEPLOY_DIR"

# 解压文件
echo "📦 解压文件..."
tar -xzf "$PACKAGE_FILE" -C "$DEPLOY_DIR" 2>/dev/null || {
    tar -xzf "$PACKAGE_FILE" -C "$DEPLOY_DIR"
}

# 设置权限
echo "🔐 设置文件权限..."
chown -R www-data:www-data "$DEPLOY_DIR" 2>/dev/null || chown -R nginx:nginx "$DEPLOY_DIR" 2>/dev/null || true
chmod -R 755 "$DEPLOY_DIR"

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 部署信息:"
echo "   - 部署目录: $DEPLOY_DIR"
echo "   - 访问地址: http://joketop.com"
echo ""
echo "💡 提示: Nginx 配置由统一脚本 deploy-joketop-nginx.sh 管理"
echo ""
echo "   配置 Nginx (HTTP):"
echo "   sudo ./deploy-joketop-nginx.sh"
echo ""
echo "   配置 Nginx (HTTPS):"
echo "   sudo ./deploy-joketop-nginx.sh --letsencrypt --email riseat7am@gmail.com"
