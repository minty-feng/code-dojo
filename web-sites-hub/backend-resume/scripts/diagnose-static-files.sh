#!/bin/bash
# 诊断静态文件配置问题

echo "=========================================="
echo "  静态文件配置诊断脚本"
echo "=========================================="
echo ""

# 配置
STATIC_DIR="/home/ubuntu/backend-resume/static"
NGINX_CONFIG="/etc/nginx/sites-enabled/joketop.conf"
DOMAIN="me.joketop.com"

echo "1. 检查静态文件目录是否存在"
echo "----------------------------------------"
if [ -d "$STATIC_DIR" ]; then
    echo "✅ 目录存在: $STATIC_DIR"
    echo ""
    echo "   目录内容:"
    ls -lah "$STATIC_DIR" | head -20
else
    echo "❌ 目录不存在: $STATIC_DIR"
    echo "   请检查部署路径是否正确"
    exit 1
fi
echo ""

echo "2. 检查关键静态文件是否存在"
echo "----------------------------------------"
FILES=("main.css" "main.js" "style.css" "resume.css" "resume.js" "auth.js" "favicon.svg")
for file in "${FILES[@]}"; do
    if [ -f "$STATIC_DIR/$file" ]; then
        echo "✅ $file 存在 ($(du -h "$STATIC_DIR/$file" | cut -f1))"
    else
        echo "❌ $file 不存在"
    fi
done
echo ""

echo "3. 检查文件权限"
echo "----------------------------------------"
if [ -r "$STATIC_DIR" ]; then
    echo "✅ 目录可读: $STATIC_DIR"
else
    echo "❌ 目录不可读: $STATIC_DIR"
fi

if [ -x "$STATIC_DIR" ]; then
    echo "✅ 目录可执行（可进入）: $STATIC_DIR"
else
    echo "❌ 目录不可执行: $STATIC_DIR"
fi
echo ""

echo "4. 检查 Nginx 配置"
echo "----------------------------------------"
if [ -f "$NGINX_CONFIG" ]; then
    echo "✅ Nginx 配置文件存在: $NGINX_CONFIG"
    echo ""
    echo "   静态资源配置:"
    grep -A 10 "location.*static" "$NGINX_CONFIG" | head -15
else
    echo "❌ Nginx 配置文件不存在: $NGINX_CONFIG"
fi
echo ""

echo "5. 测试 Nginx 配置语法"
echo "----------------------------------------"
if sudo nginx -t 2>&1 | grep -q "syntax is ok"; then
    echo "✅ Nginx 配置语法正确"
else
    echo "❌ Nginx 配置语法错误:"
    sudo nginx -t
fi
echo ""

echo "6. 检查 Nginx 错误日志（最近 20 行）"
echo "----------------------------------------"
if [ -f "/var/log/nginx/me.joketop.com.error.log" ]; then
    echo "最近的错误日志:"
    sudo tail -20 /var/log/nginx/me.joketop.com.error.log | grep -i "static\|404\|permission\|denied" || echo "   无相关错误"
else
    echo "⚠️  错误日志文件不存在"
fi
echo ""

echo "7. 测试本地访问静态文件（通过 Nginx）"
echo "----------------------------------------"
echo "注意：由于 HTTP 会重定向到 HTTPS，我们测试 HTTPS 访问"
echo ""

echo "测试 CSS 文件 (HTTPS):"
STATUS=$(curl -s -k -o /dev/null -w "%{http_code}" -H "Host: $DOMAIN" https://127.0.0.1/static/main.css)
if [ "$STATUS" = "200" ]; then
    echo "✅ CSS 文件可访问 (HTTP $STATUS)"
    echo "   文件大小: $(curl -s -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.css | wc -c) bytes"
    echo "   响应头:"
    curl -I -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.css 2>&1 | head -5
else
    echo "❌ CSS 文件不可访问 (HTTP $STATUS)"
    echo "   响应头:"
    curl -I -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.css 2>&1 | head -10
fi
echo ""

echo "测试 JS 文件 (HTTPS):"
STATUS=$(curl -s -k -o /dev/null -w "%{http_code}" -H "Host: $DOMAIN" https://127.0.0.1/static/main.js)
if [ "$STATUS" = "200" ]; then
    echo "✅ JS 文件可访问 (HTTP $STATUS)"
    echo "   文件大小: $(curl -s -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.js | wc -c) bytes"
    echo "   响应头:"
    curl -I -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.js 2>&1 | head -5
else
    echo "❌ JS 文件不可访问 (HTTP $STATUS)"
    echo "   响应头:"
    curl -I -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.js 2>&1 | head -10
fi
echo ""

echo "测试 HTTP 重定向（应该返回 301）:"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Host: $DOMAIN" http://127.0.0.1/static/main.css)
if [ "$HTTP_STATUS" = "301" ] || [ "$HTTP_STATUS" = "302" ]; then
    echo "✅ HTTP 正确重定向到 HTTPS (HTTP $HTTP_STATUS)"
else
    echo "⚠️  HTTP 重定向异常 (HTTP $HTTP_STATUS)"
fi
echo ""

echo "8. 检查 Nginx 进程用户权限"
echo "----------------------------------------"
NGINX_USER=$(ps aux | grep -E "nginx: (master|worker)" | grep -v grep | head -1 | awk '{print $1}')
echo "Nginx 运行用户: $NGINX_USER"
if [ -n "$NGINX_USER" ]; then
    echo "   检查用户是否可以访问静态文件目录:"
    sudo -u "$NGINX_USER" test -r "$STATIC_DIR" && echo "   ✅ 可读" || echo "   ❌ 不可读"
    sudo -u "$NGINX_USER" test -x "$STATIC_DIR" && echo "   ✅ 可执行" || echo "   ❌ 不可执行"
fi
echo ""

echo "=========================================="
echo "  诊断完成"
echo "=========================================="
echo ""
echo "如果发现问题，请检查："
echo "  1. 文件路径是否正确: $STATIC_DIR"
echo "  2. 文件权限是否正确（Nginx 用户可读）"
echo "  3. Nginx 配置是否正确"
echo "  4. Nginx 是否已重新加载: sudo systemctl reload nginx"
echo ""

