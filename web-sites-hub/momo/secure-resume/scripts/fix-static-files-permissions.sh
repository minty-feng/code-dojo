#!/bin/bash
# 修复静态文件权限问题

echo "=========================================="
echo "  修复静态文件权限"
echo "=========================================="
echo ""

STATIC_DIR="/home/ubuntu/secure-resume/static"
PARENT_DIR="/home/ubuntu/secure-resume"
HOME_DIR="/home/ubuntu"

# 检查 Nginx worker 用户
NGINX_USER=$(ps aux | grep "nginx: worker" | grep -v grep | head -1 | awk '{print $1}')
if [ -z "$NGINX_USER" ]; then
    # 如果找不到 worker 进程，尝试查找配置中的用户
    NGINX_USER=$(grep -E "^user" /etc/nginx/nginx.conf 2>/dev/null | awk '{print $2}' | tr -d ';')
    if [ -z "$NGINX_USER" ]; then
        NGINX_USER="www-data"  # 默认值
    fi
fi

echo "检测到 Nginx worker 用户: $NGINX_USER"
echo ""

# 方案 1：调整目录权限（推荐）
echo "方案 1：调整目录权限（推荐）"
echo "----------------------------------------"
echo "这将允许 Nginx 用户访问静态文件目录"
echo ""

# 确保父目录可执行（允许进入）
echo "1. 设置 /home/ubuntu 目录权限（允许进入）"
sudo chmod 755 "$HOME_DIR"
echo "   ✅ 完成"

echo ""
echo "2. 设置 /home/ubuntu/secure-resume 目录权限"
sudo chmod 755 "$PARENT_DIR"
echo "   ✅ 完成"

echo ""
echo "3. 设置 /home/ubuntu/secure-resume/static 目录权限"
sudo chmod 755 "$STATIC_DIR"
echo "   ✅ 完成"

echo ""
echo "4. 设置静态文件权限（可读）"
sudo chmod 644 "$STATIC_DIR"/*
echo "   ✅ 完成"

echo ""
echo "5. 验证权限"
echo "   检查目录权限:"
ls -ld "$HOME_DIR" "$PARENT_DIR" "$STATIC_DIR"
echo ""
echo "   检查文件权限（前 3 个）:"
ls -l "$STATIC_DIR" | head -5

echo ""
echo "6. 测试 Nginx 用户是否可以访问"
if sudo -u "$NGINX_USER" test -r "$STATIC_DIR/main.css"; then
    echo "   ✅ Nginx 用户 ($NGINX_USER) 可以读取文件"
else
    echo "   ❌ Nginx 用户 ($NGINX_USER) 无法读取文件"
    echo "   尝试方案 2..."
fi

echo ""
echo "=========================================="
echo "  修复完成"
echo "=========================================="
echo ""
echo "下一步："
echo "  1. 重新加载 Nginx: sudo systemctl reload nginx"
echo "  2. 测试静态文件: curl -I -k -H 'Host: me.joketop.com' https://127.0.0.1/static/main.css"
echo "  3. 如果还有问题，检查 SELinux（如果启用）:"
echo "     sudo setsebool -P httpd_read_user_content 1  # CentOS/RHEL"
echo ""

