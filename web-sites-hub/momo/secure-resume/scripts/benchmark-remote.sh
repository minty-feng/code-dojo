#!/bin/bash
# 远程压测脚本（通过域名，自动经过 Nginx）

echo "=========================================="
echo "  远程压测：通过域名（自动经过 Nginx）"
echo "=========================================="
echo ""
echo "✅ 此脚本通过域名访问，自动经过 Nginx"
echo "   静态资源由 Nginx 直接服务（如果配置正确）"
echo "   无需区分优化前后，同一个脚本即可"
echo ""

# 配置
DOMAIN="${1:-https://me.joketop.com}"
THREADS=4
CONNECTIONS=100
DURATION=30s

echo "测试目标: $DOMAIN"
echo "测试配置："
echo "  - 线程数: $THREADS"
echo "  - 并发连接: $CONNECTIONS"
echo "  - 持续时间: $DURATION"
echo ""

# 测试 1：HTML 页面
echo "----------------------------------------"
echo "测试 1: HTML 页面 (/)"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION --latency $DOMAIN/
echo ""

# 测试 2：静态资源 - CSS
echo "----------------------------------------"
echo "测试 2: 静态资源 - CSS (/static/main.css)"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION --latency $DOMAIN/static/main.css
echo ""

# 测试 3：静态资源 - JS
echo "----------------------------------------"
echo "测试 3: 静态资源 - JS (/static/main.js)"
echo "----------------------------------------"
wrk -t$THREADS -c$CONNECTIONS -d$DURATION --latency $DOMAIN/static/main.js
echo ""

echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""
echo "注意："
echo "  - 如果静态资源走 CDN，结果会受 CDN 影响"
echo "  - 建议在 CDN 控制台清除缓存后测试"
echo "  - 或直接测试源站 IP（需要设置 Host 头）"
echo ""
echo "使用方法："
echo "  ./benchmark-remote.sh                    # 使用默认域名"
echo "  ./benchmark-remote.sh https://example.com  # 自定义域名"

