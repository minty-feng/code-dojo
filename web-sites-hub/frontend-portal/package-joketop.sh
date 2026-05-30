#!/bin/bash

# 打包脚本 - 将项目文件打包成 gz 压缩包
# 使用方法: ./package-joketop.sh

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
PACKAGE_NAME="joketop-$(date +%Y%m%d-%H%M%S).tar.gz"
EXCLUDE_FILE=".package-exclude"

# 版本号：优先环境变量 ASSETS_VERSION，否则直接使用当天日期，用于 CDN 缓存更新
if [ -n "$ASSETS_VERSION" ]; then
    VERSION="$ASSETS_VERSION"
else
    VERSION=$(date +%Y%m%d)
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  开始打包 joketop 项目${NC}"
echo -e "${GREEN}========================================${NC}"

# 获取当前目录
CURRENT_DIR=$(pwd)
echo -e "${YELLOW}当前目录: ${GREEN}$CURRENT_DIR${NC}"

# 检查是否在项目根目录
if [ ! -f "index.html" ]; then
    echo -e "${YELLOW}错误: 请在项目根目录执行此脚本${NC}"
    exit 1
fi

# 明确指定要打包的文件和目录
echo -e "${YELLOW}正在打包文件...${NC}"
echo -e "${YELLOW}包含的文件：${NC}"
echo -e "${YELLOW}  - HTML 文件: index.html, resume.html, learning.html, showcase.html, snippets.html, diary.html, speed.html, fund.html, invisiblechars.html, wufu.html, poems.html, timeline.html, goals.html, tianya.html, journal.html, ganwu.html, plans.html, calendar.html, figures.html, aihistory.html${NC}"
echo -e "${YELLOW}  - 资源文件: assets/ (css, js, favicon.svg)${NC}"
echo -e "${YELLOW}  - 子项目目录: phd-game/, super-app/, debate-competition/, internship-trends/ (均不带 dist 层级)${NC}"
echo ""

# 创建临时目录结构
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# 复制需要打包的文件（统一目录结构：子项目路径不带 dist）
echo -e "${YELLOW}准备文件...${NC}"
if ! ./scripts/prepare-preview-site.sh "$TEMP_DIR"; then
    echo -e "${YELLOW}✗ 准备文件失败，已中止打包${NC}"
    exit 1
fi

# 统一注入版本号到 HTML（替换 ?v=xxx 为 ?v=$VERSION，触发 CDN 更新）
echo -e "${YELLOW}注入版本号 v=${GREEN}$VERSION${NC}"
for f in $TEMP_DIR/*.html; do
    [ -f "$f" ] && sed -i.bak "s/?v=[0-9a-zA-Z]*/?v=$VERSION/g" "$f" && rm -f "${f}.bak"
done

# JS 压缩（使用 terser，需 npm 环境）
if command -v npx &>/dev/null; then
    echo -e "${YELLOW}压缩 JS 文件...${NC}"
    JS_COUNT=$(find "$TEMP_DIR/assets" -type f -name "*.js" | wc -l | tr -d ' ')

    if [ "$JS_COUNT" -eq 0 ]; then
        echo -e "  ${YELLOW}⚠ 未找到 JS 文件，跳过压缩${NC}"
    else
        SUCCESS_COUNT=0
        FAILED_COUNT=0
        while IFS= read -r -d '' f; do
            if npx --yes terser "$f" -c -m -o "$f"; then
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
                echo -e "  ${GREEN}✓${NC} ${f#$TEMP_DIR/}"
            else
                FAILED_COUNT=$((FAILED_COUNT + 1))
                echo -e "  ${YELLOW}⚠ 压缩失败${NC} ${f#$TEMP_DIR/}"
            fi
        done < <(find "$TEMP_DIR/assets" -type f -name "*.js" -print0)
        echo -e "${YELLOW}JS 压缩结果:${NC} 成功 ${GREEN}$SUCCESS_COUNT${NC} / 失败 ${YELLOW}$FAILED_COUNT${NC}"
    fi
else
    echo -e "${YELLOW}提示: 未检测到 npx，跳过 JS 压缩。安装 Node.js 后可用 terser 压缩。${NC}"
fi

# 检查关键文件是否存在
MISSING_FILES=()
[ ! -f "$TEMP_DIR/index.html" ] && MISSING_FILES+=("index.html")
[ ! -f "$TEMP_DIR/resume.html" ] && MISSING_FILES+=("resume.html")
[ ! -f "$TEMP_DIR/learning.html" ] && MISSING_FILES+=("learning.html")
[ ! -f "$TEMP_DIR/showcase.html" ] && MISSING_FILES+=("showcase.html")
[ ! -f "$TEMP_DIR/snippets.html" ] && MISSING_FILES+=("snippets.html")
[ ! -f "$TEMP_DIR/diary.html" ] && MISSING_FILES+=("diary.html")
[ ! -f "$TEMP_DIR/speed.html" ] && MISSING_FILES+=("speed.html")
[ ! -f "$TEMP_DIR/fund.html" ] && MISSING_FILES+=("fund.html")
[ ! -f "$TEMP_DIR/wufu.html" ] && MISSING_FILES+=("wufu.html")
[ ! -f "$TEMP_DIR/poems.html" ] && MISSING_FILES+=("poems.html")
[ ! -f "$TEMP_DIR/timeline.html" ] && MISSING_FILES+=("timeline.html")
[ ! -f "$TEMP_DIR/goals.html" ] && MISSING_FILES+=("goals.html")
[ ! -f "$TEMP_DIR/tianya.html" ] && MISSING_FILES+=("tianya.html")
[ ! -f "$TEMP_DIR/journal.html" ] && MISSING_FILES+=("journal.html")
[ ! -f "$TEMP_DIR/invisiblechars.html" ] && MISSING_FILES+=("invisiblechars.html")
[ ! -f "$TEMP_DIR/plans.html" ] && MISSING_FILES+=("plans.html")
[ ! -f "$TEMP_DIR/calendar.html" ] && MISSING_FILES+=("calendar.html")
[ ! -f "$TEMP_DIR/figures.html" ] && MISSING_FILES+=("figures.html")
[ ! -f "$TEMP_DIR/aihistory.html" ] && MISSING_FILES+=("aihistory.html")
[ ! -d "$TEMP_DIR/assets" ] && MISSING_FILES+=("assets/")
[ ! -f "$TEMP_DIR/assets/favicon.svg" ] && MISSING_FILES+=("assets/favicon.svg")
[ ! -d "$TEMP_DIR/phd-game" ] && MISSING_FILES+=("phd-game/")
[ ! -d "$TEMP_DIR/super-app" ] && MISSING_FILES+=("super-app/")
[ ! -d "$TEMP_DIR/debate-competition" ] && MISSING_FILES+=("debate-competition/")
[ ! -d "$TEMP_DIR/internship-trends" ] && MISSING_FILES+=("internship-trends/")

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${YELLOW}警告: 以下文件不存在: ${MISSING_FILES[*]}${NC}"
fi

# 打包文件（只打包明确指定的文件）
cd $TEMP_DIR
tar -czf "$(pwd)/../$PACKAGE_NAME" .
cd - > /dev/null
mv "$TEMP_DIR/../$PACKAGE_NAME" .

# 检查打包是否成功
if [ $? -eq 0 ]; then
    # 获取文件大小
    FILE_SIZE=$(du -h $PACKAGE_NAME | cut -f1)
    
    # 列出打包的文件
    echo -e "${GREEN}✓ 打包成功！${NC}"
    echo -e "${YELLOW}打包的文件列表：${NC}"
    tar -tzf $PACKAGE_NAME | head -20
    FILE_COUNT=$(tar -tzf $PACKAGE_NAME | wc -l)
    echo -e "${YELLOW}... (共 $FILE_COUNT 个文件)${NC}"
    echo ""
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  文件信息${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "  文件名: ${GREEN}$PACKAGE_NAME${NC}"
    echo -e "  资源版本: ${GREEN}v=$VERSION${NC}"
    echo -e "  文件大小: ${GREEN}$FILE_SIZE${NC}"
    echo -e "  文件数量: ${GREEN}$FILE_COUNT${NC}"
    echo -e "  文件位置: ${GREEN}$(pwd)/$PACKAGE_NAME${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}下一步：${NC}"
    echo ""
    echo -e "${YELLOW}【方式 A】仅更新主站静态（joketop.com / showcase 等 HTML）${NC}"
    echo -e "  1. 上传到服务器:"
    echo -e "     scp $PACKAGE_NAME deploy-joketop.sh ../joketop.conf tencent-ubuntu-1:~/web-deploy"
    echo -e "  2. 登录并部署:"
    echo -e "     ssh tencent-ubuntu-1"
    echo -e "     cd ~/web-deploy"
    echo -e "     sudo ./deploy-joketop.sh $PACKAGE_NAME"
    echo -e "     sudo cp joketop.conf /etc/nginx/sites-available/joketop.conf"
    echo -e "     sudo ln -sf /etc/nginx/sites-available/joketop.conf /etc/nginx/sites-enabled/joketop.conf"
    echo -e "     sudo nginx -t && sudo systemctl reload nginx"
    echo ""
    echo -e "${YELLOW}【方式 B】全站集成部署（推荐：静态 + Nginx 多域名配置）${NC}"
    echo -e "  1. 上传打包文件与部署脚本:"
    echo -e "     scp $PACKAGE_NAME deploy-joketop.sh deploy-all-joketop.sh tencent-ubuntu-1:~/web-deploy"
    echo -e "     # deploy-all-joketop.sh 会调用 web-sites-hub/deploy-joketop-nginx.sh"
    echo -e "  2. 登录并一键部署:"
    echo -e "     ssh tencent-ubuntu-1"
    echo -e "     cd ~/web-deploy"
    echo -e "     chmod +x deploy-all-joketop.sh"
    echo -e "     sudo ./deploy-all-joketop.sh $PACKAGE_NAME"
    echo -e "  3. 首次部署或续期证书:"
    echo -e "     sudo ./deploy-all-joketop.sh $PACKAGE_NAME --letsencrypt --email your@email.com"
    echo ""
    echo -e "${YELLOW}【方式 C】仅更新 Nginx 配置（未改静态文件时）${NC}"
    echo -e "     cd ~/code-dojo/web-sites-hub   # 或服务器上的 web-sites-hub 路径"
    echo -e "     sudo ./deploy-joketop-nginx.sh"
    echo -e "     sudo ./deploy-joketop-nginx.sh --letsencrypt --email your@email.com"
    echo ""
    echo -e "${YELLOW}【可选】安全头加固${NC}"
    echo -e "     cd ~/code-dojo/web-sites-hub"
    echo -e "     sudo ./apply-security-headers.sh"
    echo ""
    echo -e "${YELLOW}说明:${NC}"
    echo -e "  - deploy-joketop.sh 只解压到 /var/www/html/joketop；方式 A 会额外拷贝 joketop.conf 并重载 nginx"
    echo -e "  - deploy-all-joketop.sh = deploy-joketop.sh + deploy-joketop-nginx.sh"
    echo -e "  - 若改了 joketop.conf，需跑 deploy-joketop-nginx.sh 或 deploy-all-joketop.sh"
else
    echo -e "${YELLOW}✗ 打包失败！${NC}"
    exit 1
fi

# 清理临时文件（临时目录会在 trap 中自动清理）

echo -e "${GREEN}打包完成！${NC}"

