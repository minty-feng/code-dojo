#!/bin/bash
# 快速测试静态文件是否正常

DOMAIN="me.joketop.com"

echo "=========================================="
echo "  静态文件访问测试"
echo "=========================================="
echo ""

echo "1. 测试 CSS 文件 (HTTPS)"
echo "----------------------------------------"
curl -I -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.css 2>&1 | head -10
echo ""

echo "2. 测试 JS 文件 (HTTPS)"
echo "----------------------------------------"
curl -I -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.js 2>&1 | head -10
echo ""

echo "3. 测试实际文件内容 (CSS)"
echo "----------------------------------------"
CSS_CONTENT=$(curl -s -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.css)
if [ -n "$CSS_CONTENT" ] && [ "${CSS_CONTENT:0:5}" != "<!DOC" ] && [ "${CSS_CONTENT:0:5}" != "<html" ]; then
    echo "✅ CSS 文件内容正常（前 100 字符）:"
    echo "${CSS_CONTENT:0:100}..."
else
    echo "❌ CSS 文件内容异常（可能是 HTML 错误页面）:"
    echo "${CSS_CONTENT:0:200}"
fi
echo ""

echo "4. 测试实际文件内容 (JS)"
echo "----------------------------------------"
JS_CONTENT=$(curl -s -k -H "Host: $DOMAIN" https://127.0.0.1/static/main.js)
if [ -n "$JS_CONTENT" ] && [ "${JS_CONTENT:0:5}" != "<!DOC" ] && [ "${JS_CONTENT:0:5}" != "<html" ]; then
    echo "✅ JS 文件内容正常（前 100 字符）:"
    echo "${JS_CONTENT:0:100}..."
else
    echo "❌ JS 文件内容异常（可能是 HTML 错误页面）:"
    echo "${JS_CONTENT:0:200}"
fi
echo ""

echo "5. 测试 Favicon (SVG)"
echo "----------------------------------------"
FAVICON_STATUS=$(curl -s -k -o /dev/null -w "%{http_code}" -H "Host: $DOMAIN" https://127.0.0.1/static/favicon.svg)
FAVICON_TYPE=$(curl -s -k -I -H "Host: $DOMAIN" https://127.0.0.1/static/favicon.svg | grep -i "content-type" | head -1)
if [ "$FAVICON_STATUS" = "200" ]; then
    echo "✅ Favicon 可访问 (HTTP $FAVICON_STATUS)"
    echo "   Content-Type: $FAVICON_TYPE"
    if echo "$FAVICON_TYPE" | grep -qi "image/svg"; then
        echo "   ✅ MIME 类型正确"
    else
        echo "   ⚠️  MIME 类型可能不正确（应该是 image/svg+xml）"
    fi
else
    echo "❌ Favicon 不可访问 (HTTP $FAVICON_STATUS)"
    echo "   响应头:"
    curl -I -k -H "Host: $DOMAIN" https://127.0.0.1/static/favicon.svg 2>&1 | head -10
fi
echo ""

echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""
echo "如果看到 200 OK 和正确的 Content-Type，说明配置正常"
echo "如果看到 404 或 HTML 错误页面，请检查："
echo "  1. 文件是否存在: ls -la /home/ubuntu/backend-resume/static/"
echo "  2. 文件权限: chmod 644 /home/ubuntu/backend-resume/static/*"
echo "  3. Nginx 配置: sudo nginx -t && sudo systemctl reload nginx"
echo ""

