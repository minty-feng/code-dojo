#!/bin/bash
# 本地压测脚本 - 直接访问 Actix Web（未经过 Nginx）

echo "=========================================="
echo "  本地压测：直接访问 Actix Web"
echo "=========================================="
echo ""
echo "⚠️  注意：此脚本直接访问 http://127.0.0.1:8080"
echo "   静态资源由 Actix Web 处理（未经过 Nginx）"
echo "   要测试 Nginx 优化效果，请使用 benchmark-nginx.sh"
echo ""

BASE_URL="http://127.0.0.1:8080"
THREADS=4
CONNECTIONS=100
DURATION=30s

echo "测试配置："
echo "  - 测试目标: $BASE_URL (直接访问 Actix Web)"
echo "  - 线程数: $THREADS"
echo "  - 并发连接: $CONNECTIONS"
echo "  - 持续时间: $DURATION"
echo ""

# 测试 1：HTML 页面
echo "----------------------------------------"
echo "测试 1: HTML 页面 (/)"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION --latency $BASE_URL/
echo ""

# 测试 2：静态资源 - CSS
echo "----------------------------------------"
echo "测试 2: 静态资源 - CSS (/static/main.css)"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION --latency $BASE_URL/static/main.css
echo ""

# 测试 3：静态资源 - JS
echo "----------------------------------------"
echo "测试 3: 静态资源 - JS (/static/main.js)"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION --latency $BASE_URL/static/main.js
echo ""

echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""
echo "对比说明："
echo "  - 此测试：静态资源走 Actix Web"
echo "  - 要测试 Nginx 优化效果，运行：./benchmark-nginx.sh"
echo ""

