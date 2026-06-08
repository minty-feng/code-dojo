#!/usr/bin/env bash
# 打包完成后打印部署提示
# 用法: print_deploy_hints <package_name> [with-data|no-data]
# 可选环境变量: DEPLOY_SSH_HOST, DEPLOY_REMOTE_DIR

GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
NC="${NC:-\033[0m}"
print_admin_api_key_hint() {
    local new_key
    new_key="$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")"

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ADMIN_API_KEY（新生成，请按需使用）${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "  ${YELLOW}保护 /invite/list|stats|generate，写入服务器 env：${NC}"
    echo ""
    echo -e "  ADMIN_API_KEY=${GREEN}${new_key}${NC}"
    echo ""
    echo -e "  ${YELLOW}服务器操作示例：${NC}"
    echo -e "  vim deploy/backend-platform-py.env"
    echo -e "  # 将 ADMIN_API_KEY= 一行改为上面的值，然后 restart"
    echo ""
    echo -e "  ${YELLOW}验证：${NC}"
    echo -e "  curl -s http://127.0.0.1:8300/api/v1/invite/stats -H 'X-Admin-Key: ${new_key}'"
    echo ""
    echo -e "  ${YELLOW}说明：${NC}"
    echo -e "  - 首次部署或怀疑泄露时，用上面新 Key"
    echo -e "  - 线上已配置且有效的 Key 无需每次打包更换"
    echo -e "  - 勿将真实 Key 提交到 Git"
    echo -e "${GREEN}========================================${NC}"
}

print_deploy_hints() {
    local package_name="$1"
    local mode="${2:-no-data}"
    local remote_host="${DEPLOY_SSH_HOST:-tencent-ubuntu-1}"
    local remote_dir="${DEPLOY_REMOTE_DIR:-~/backend-platform-py}"

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  下一步${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""

    if [ "$mode" = "with-data" ]; then
        echo -e "${YELLOW}【推荐场景】首次部署 / 需要同步本地 data/app.db${NC}"
        echo -e "  ${YELLOW}日常代码更新请用: ./deploy/package-backend-platform-py-no-data.sh${NC}"
        echo ""
    else
        echo -e "${YELLOW}【推荐场景】日常代码更新（保留线上 data/app.db 与邀请码）${NC}"
        echo ""
    fi

    echo -e "${YELLOW}【1】本地上传${NC}"
    echo -e "  scp $package_name ${remote_host}:~"
    echo ""

    echo -e "${YELLOW}【2】服务器解压更新${NC}"
    echo -e "  ssh ${remote_host}"
    echo -e "  cd ${remote_dir}"
    echo -e "  ./deploy/start-backend-platform-py.sh stop"
    echo -e "  tar -xzf ~/$package_name -C /tmp"
    if [ "$mode" = "with-data" ]; then
        echo -e "  # ⚠ 会覆盖线上 data/，确认后再执行："
        echo -e "  rsync -a --delete /tmp/backend-platform-py/ ${remote_dir}/"
    else
        echo -e "  rsync -a /tmp/backend-platform-py/app/ ${remote_dir}/app/"
        echo -e "  rsync -a /tmp/backend-platform-py/deploy/ ${remote_dir}/deploy/"
        echo -e "  rsync -a /tmp/backend-platform-py/requirements.txt ${remote_dir}/"
        echo -e "  # 不覆盖 data/ 与 .venv"
    fi
    echo ""

    echo -e "${YELLOW}【3】首次部署还需准备环境（已做过可跳过）${NC}"
    echo -e "  cd ${remote_dir}"
    echo -e "  python3.12 -m venv .venv"
    echo -e "  source .venv/bin/activate"
    echo -e "  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"
    echo -e "  vim deploy/backend-platform-py.env   # JWT_SECRET / ADMIN_* / CORS / ADMIN_API_KEY"
    echo ""

    print_admin_api_key_hint

    echo ""

    echo -e "${YELLOW}【4】确认 data/ 可写并重启${NC}"
    echo -e "  sudo chown -R \$(whoami):\$(whoami) ${remote_dir}/data"
    echo -e "  chmod 755 ${remote_dir}/data"
    echo -e "  chmod 664 ${remote_dir}/data/app.db 2>/dev/null || true"
    echo -e "  ./deploy/start-backend-platform-py.sh restart"
    echo -e "  tail -f backend-platform-py.log"
    echo ""

    echo -e "${YELLOW}【5】验证服务${NC}"
    echo -e "  # 本机"
    echo -e "  curl -s http://127.0.0.1:8300/api/v1/system/health"
    echo -e "  curl -s http://127.0.0.1:8300/api/v1/invite/stats -H 'X-Admin-Key: \$ADMIN_API_KEY'"
    echo -e "  curl -s -X POST http://127.0.0.1:8300/api/v1/invite/generate -H 'Content-Type: application/json' -H 'X-Admin-Key: \$ADMIN_API_KEY' -d '{}'"
    echo -e "  # 外网（简历 / API）"
    echo -e "  curl -s https://me.joketop.com/api/v1/resume/status"
    echo -e "  curl -s https://showcase.joketop.com/api/v1/snippets?page=1&page_size=3"
    echo -e "  # 安全巡检（只读，不写库）"
    echo -e "  ./deploy/verify-api-security.sh --base https://joketop.com"
    echo -e "  ./deploy/verify-api-security.sh --base http://127.0.0.1:8300 --rate-limit-burst 15"
    echo ""

    echo -e "${YELLOW}【6】若改了 Nginx（web-sites-hub/joketop.conf）${NC}"
    echo -e "  scp ../joketop.conf ${remote_host}:~/web-deploy/   # 或服务器上的 web-sites-hub 路径"
    echo -e "  sudo cp joketop.conf /etc/nginx/sites-available/joketop.conf"
    echo -e "  sudo ln -sf /etc/nginx/sites-available/joketop.conf /etc/nginx/sites-enabled/joketop.conf"
    echo -e "  sudo nginx -t && sudo systemctl reload nginx"
    echo ""

    echo -e "${YELLOW}说明:${NC}"
    if [ "$mode" = "with-data" ]; then
        echo -e "  - 本包含 data/，会覆盖线上 SQLite；日常请用 no-data 包"
    else
        echo -e "  - 本包不含 data/，线上 app.db 与邀请码数据会保留"
    fi
    echo -e "  - stop 无效时: kill \$(pgrep -f 'uvicorn app.main:app') && ./deploy/start-backend-platform-py.sh start"
    echo -e "  - 依赖变更后: source .venv/bin/activate && pip install -r requirements.txt"
    echo -e "  - 管理后台: https://me.joketop.com/admin （需 ADMIN_ALLOW_REMOTE=true）"
    echo -e "  - 环境变量 deploy/backend-platform-py.env 勿提交真实密钥"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}打包完成！${NC}"
}
