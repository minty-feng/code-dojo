#!/bin/bash
# Nginx 部署包脚本
# 创建适合 Nginx 部署的打包文件

set -e

echo "📦 创建 Nginx 部署包"
echo "===================="
echo ""

# 检查构建目录是否存在
if [ ! -d "_build/html" ]; then
    echo "❌ 构建目录不存在，请先运行 build.sh"
    exit 1
fi

# 生成时间戳
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="backend-docs-nginx-${TIMESTAMP}.tar.gz"

echo "📋 创建 Nginx 部署包: $PACKAGE_NAME"
echo ""

# 创建临时目录
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# 拷贝文件到临时目录
echo "📋 准备文件..."
cp -r _build/html "$TEMP_DIR/"

# 拷贝部署脚本（如果存在）
if [ -f "deploy-backend.sh" ]; then
    echo "📋 添加部署脚本..."
    cp deploy-backend.sh "$TEMP_DIR/deploy-backend.sh"
fi

# 创建部署说明文件
cat > "$TEMP_DIR/README.txt" << 'EOF'
Nginx 部署说明
==============

1. 上传打包文件到服务器

2. 运行部署脚本（自动解压和部署）：

   # HTTP 部署
   sudo bash deploy-backend.sh backend-docs-nginx-*.tar.gz

   # HTTPS 部署（Let's Encrypt 自动证书）
   sudo bash deploy-backend.sh --letsencrypt --email riseat7am@gmail.com backend-docs-nginx-*.tar.gz

   # HTTPS 部署（手动证书）
   sudo bash deploy-backend.sh --cert /path/to/cert.pem --key /path/to/key.pem backend-docs-nginx-*.tar.gz

3. 访问地址：
   HTTP:  http://blog.joketop.com/backend
   HTTPS: https://blog.joketop.com/backend（如果启用 HTTPS）

配置文件位置：
- Nginx 配置: /etc/nginx/sites-available/honey-backend-dojo
- 部署目录: /var/www/html/honey-backend-dojo
- Let's Encrypt 证书: /etc/letsencrypt/live/blog.joketop.com/

HTTPS 选项说明：
- --letsencrypt: 使用 Let's Encrypt 自动获取和续期证书（推荐）
- --cert <路径>: 指定 SSL 证书文件路径
- --key <路径>: 指定 SSL 私钥文件路径
- --email <邮箱>: Let's Encrypt 邮箱地址（必需）
- --domain <域名>: 指定域名（默认: blog.joketop.com）
- --path <路径>: 指定 URL 路径（默认: /backend）
EOF

# 打包
echo "📦 打包文件..."
cd "$TEMP_DIR"
# 使用 --format=ustar 格式避免 macOS 扩展属性警告
if [ -f "deploy-backend.sh" ]; then
    tar --format=ustar -czf "../$PACKAGE_NAME" html README.txt deploy-backend.sh
else
tar --format=ustar -czf "../$PACKAGE_NAME" html README.txt
fi

# 返回原目录
cd - > /dev/null

# 移动打包文件到当前目录
mv "$TEMP_DIR/../$PACKAGE_NAME" .

# 显示打包结果
PACKAGE_SIZE=$(du -sh "$PACKAGE_NAME" | cut -f1)
echo ""
echo "✅ Nginx 部署包创建完成！"
echo "   文件名: $PACKAGE_NAME"
echo "   文件大小: $PACKAGE_SIZE"
echo ""
echo "💡 提示："
echo "   1. 上传到服务器"
echo "   2. HTTP 部署: sudo bash deploy-backend.sh $PACKAGE_NAME"
echo "   3. HTTPS 部署: sudo bash deploy-backend.sh --letsencrypt --email riseat7am@gmail.com $PACKAGE_NAME"
echo "   4. 访问: http://blog.joketop.com/backend (或 https:// 如果启用)"

