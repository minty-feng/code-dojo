#!/bin/bash
# 通过 Nginx 测试脚本（在服务器上执行）

echo "=========================================="
echo "  本地压测：通过 Nginx（优化后）"
echo "=========================================="
echo ""
echo "✅ 此脚本通过 Nginx 访问（http://127.0.0.1 + Host 头）"
echo "   静态资源由 Nginx 直接服务（优化后）"
echo "   要对比优化前效果，请先运行：./benchmark-local.sh"
echo ""

# 配置
BASE_URL="http://127.0.0.1"
HOST="me.joketop.com"
THREADS=4
CONNECTIONS=100
DURATION=30s

echo "测试配置："
echo "  - 测试目标: $BASE_URL (通过 Nginx)"
echo "  - Host 头: $HOST"
echo "  - 线程数: $THREADS"
echo "  - 并发连接: $CONNECTIONS"
echo "  - 持续时间: $DURATION"
echo ""
echo "⚠️  注意：确保 Nginx 配置已更新并重新加载"
echo ""

# 测试 1：HTML 页面（应该走 Actix Web）
echo "----------------------------------------"
echo "测试 1: HTML 页面 (/) - 通过 Nginx 代理到 Actix Web"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION \
    -H "Host: $HOST" \
    --latency \
    $BASE_URL/
echo ""

# 测试 2：静态资源 - CSS（应该走 Nginx）
echo "----------------------------------------"
echo "测试 2: 静态资源 - CSS (/static/main.css) - 应该走 Nginx"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION \
    -H "Host: $HOST" \
    --latency \
    $BASE_URL/static/main.css
echo ""

# 测试 3：静态资源 - JS（应该走 Nginx）
echo "----------------------------------------"
echo "测试 3: 静态资源 - JS (/static/main.js) - 应该走 Nginx"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION \
    -H "Host: $HOST" \
    --latency \
    $BASE_URL/static/main.js
echo ""

echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""
echo "验证方法："
echo "  # 检查响应头，应该看到 Server: nginx"
echo "  curl -I -H 'Host: me.joketop.com' http://127.0.0.1/static/main.css"
echo ""

