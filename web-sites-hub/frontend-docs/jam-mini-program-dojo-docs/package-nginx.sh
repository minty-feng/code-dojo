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
PACKAGE_NAME="miniprogram-docs-nginx-${TIMESTAMP}.tar.gz"

echo "📋 创建 Nginx 部署包: $PACKAGE_NAME"
echo ""

# 创建临时目录
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# 拷贝文件到临时目录
echo "📋 准备文件..."
cp -r _build/html "$TEMP_DIR/"

# 拷贝部署脚本（如果存在）
if [ -f "deploy-miniprogram.sh" ]; then
    echo "📋 添加部署脚本..."
    cp deploy-miniprogram.sh "$TEMP_DIR/deploy-miniprogram.sh"
fi

# 创建部署说明文件
cat > "$TEMP_DIR/README.txt" << 'EOF'
Nginx 部署说明
==============

1. 上传打包文件到服务器

2. 运行部署脚本（自动解压和部署）：

   sudo bash deploy-miniprogram.sh miniprogram-docs-nginx-*.tar.gz

3. 配置 Nginx（使用统一脚本）：

   # HTTP 部署
   sudo bash deploy-all-docs.sh

   # HTTPS 部署（Let's Encrypt 自动证书）
   sudo bash deploy-all-docs.sh --letsencrypt --email riseat7am@gmail.com

4. 访问地址：
   HTTP:  http://blog.joketop.com/miniprogram
   HTTPS: https://blog.joketop.com/miniprogram（如果启用 HTTPS）

配置文件位置：
- Nginx 配置: /etc/nginx/sites-available/docs-code-dojo (统一配置)
- 部署目录: /var/www/html/jam-miniprogram-dojo
- Let's Encrypt 证书: /etc/letsencrypt/live/blog.joketop.com/

注意：
- Nginx 配置由统一脚本 deploy-all-docs.sh 管理
- 部署脚本 deploy-miniprogram.sh 只负责解压和拷贝文件
EOF

# 打包
echo "📦 打包文件..."
cd "$TEMP_DIR"
# 使用 --format=ustar 格式避免 macOS 扩展属性警告
if [ -f "deploy-miniprogram.sh" ]; then
    tar --format=ustar -czf "../$PACKAGE_NAME" html README.txt deploy-miniprogram.sh
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
echo "   2. 解压部署: sudo bash deploy-miniprogram.sh $PACKAGE_NAME"
echo "   3. 配置 Nginx: sudo bash deploy-all-docs.sh [--letsencrypt --email your@email.com]"
echo "   4. 访问: http://blog.joketop.com/miniprogram (或 https:// 如果启用)"

