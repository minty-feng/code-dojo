#!/bin/bash

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PACKAGE_NAME="backend-platform-py-$(date +%Y%m%d-%H%M%S).tar.gz"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  打包 backend-platform-py${NC}"
echo -e "${GREEN}========================================${NC}"

if [ ! -f "app/main.py" ] || [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}错误: 请在 backend-platform-py 根目录执行此脚本${NC}"
    exit 1
fi

echo -e "${YELLOW}准备打包文件...${NC}"
mkdir -p "$TEMP_DIR/backend-platform-py"

cp -r app "$TEMP_DIR/backend-platform-py/"
cp -r docs "$TEMP_DIR/backend-platform-py/"
cp -r scripts "$TEMP_DIR/backend-platform-py/"
cp -r deploy "$TEMP_DIR/backend-platform-py/"
cp -r data "$TEMP_DIR/backend-platform-py/" 2>/dev/null || true
cp requirements.txt README.md style.md "$TEMP_DIR/backend-platform-py/" 2>/dev/null || true

echo -e "${YELLOW}生成压缩包...${NC}"
tar -czf "$PACKAGE_NAME" -C "$TEMP_DIR" backend-platform-py

FILE_SIZE=$(du -h "$PACKAGE_NAME" | cut -f1)
FILE_COUNT=$(tar -tzf "$PACKAGE_NAME" | wc -l | tr -d ' ')

echo -e "${GREEN}✓ 打包成功${NC}"
echo -e "  文件名: ${GREEN}$PACKAGE_NAME${NC}"
echo -e "  文件大小: ${GREEN}$FILE_SIZE${NC}"
echo -e "  文件数量: ${GREEN}$FILE_COUNT${NC}"
echo -e "  当前路径: ${GREEN}$(pwd)/$PACKAGE_NAME${NC}"
