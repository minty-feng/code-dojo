#!/usr/bin/env bash
# 打包完成后打印部署提示
# 用法: print_deploy_hints <package_name> [with-data|no-data]
# 可选环境变量: DEPLOY_SSH_HOST, DEPLOY_REMOTE_DIR

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
    echo -e "  vim deploy/config/backend-platform-py.env   # JWT_SECRET / ADMIN_* / CORS"
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
    echo -e "  curl -s http://127.0.0.1:8300/api/v1/invite/stats"
    echo -e "  # 写库测试（应 success:true 或业务错误，不应 500）"
    echo -e "  curl -s -X POST http://127.0.0.1:8300/api/v1/invite/generate -H 'Content-Type: application/json' -d '{}'"
    echo -e "  # 外网（简历 / API）"
    echo -e "  curl -s https://me.joketop.com/api/v1/resume/status"
    echo -e "  curl -s https://showcase.joketop.com/api/v1/snippets?page=1&page_size=3"
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
    echo -e "  - 环境变量 deploy/config/backend-platform-py.env 勿提交真实密钥"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}打包完成！${NC}"
}
