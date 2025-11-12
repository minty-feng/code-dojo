## Secure Resume 生产部署指南

### 0. 前置条件：安装 Rust 工具链

如果服务器上还没有 Rust 工具链，可以本地安装脚本：

```bash
# 1. 在本地项目目录
cd web-sites-hub/momo/secure-resume
# 2. 上传脚本到服务器
scp scripts/install-rustup.sh user@server:/tmp/

```

### 1. 架构概览

- **入口层**：CDN（可选）+ Nginx，负责 TLS 终止、静态资源缓存以及将动态请求反向代理到 Rust 服务。
- **应用层**：`secure_resume` Actix Web 服务，监听 `127.0.0.1:8080`（可按需调整），处理邀请码校验、会话管理和模板渲染。
- **数据层**：SQLite 数据库 `invites.db`，位于 `/home/ubuntu/secure-resume/invites.db`（可在部署脚本中自定义）。

### 2. 目录结构

```text
/home/ubuntu/secure-resume/
├── secure_resume            # Release 二进制
├── invites.db               # SQLite 数据库
├── templates/               # auth.html / resume.html
├── static/                  # 前端静态资源（css/js/svg）
└── secure-resume.log        # 运行日志（可选）
```

部署阶段可以通过 `rsync` 或 CI/CD 将 `target/release/secure_resume`、`templates/`、`static/` 打包同步到该目录。

### 3. 运行方式

```bash
cd /home/ubuntu/secure-resume
SECURE_RESUME_SECURE_COOKIE=1 RUST_LOG=info \
nohup ./secure_resume > secure-resume.log 2>&1 &
echo $! > secure-resume.pid        # 记录进程号，方便后续 stop
```

停止服务：

```bash
pkill -F secure-resume.pid         # 或者 kill $(cat secure-resume.pid)
rm -f secure-resume.pid
```

> 注意：nohup 方式下没有自动重启与日志轮转，长期运行仍建议切换到 systemd。

### 4. Nginx 反向代理（`joketop.conf` 摘要）

```nginx
upstream secure_resume_backend {
    keepalive 32;
    server 127.0.0.1:8080;
}

server {
    listen 443 ssl http2;
    server_name me.joketop.com;

    ssl_certificate /etc/letsencrypt/live/me.joketop.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/me.joketop.com/privkey.pem;

    # 静态资源可由 Nginx 直接服务（允许 CDN 缓存 7 天，使用 ^~ 确保优先匹配）
    location ^~ /static/ {
        root /home/ubuntu/secure-resume;
        expires 7d;
        add_header Cache-Control "public, max-age=604800";
        access_log off;
    }

    # 其余请求全部代理到 Actix
    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Connection "";
        proxy_pass http://secure_resume_backend;

        proxy_read_timeout 30s;
        proxy_send_timeout 30s;
        proxy_cache_bypass 1;
        proxy_no_cache 1;

        add_header Cache-Control "no-store, no-cache, must-revalidate" always;
        add_header Pragma "no-cache" always;
        add_header Expires "0" always;
    }
}
```

- `deploy-all-docs.sh` 会将仓库中的 `joketop.conf` 拷贝到 `/etc/nginx/sites-available/joketop.conf`，修改脚本参数即可启用 HTTPS。
- CDN 作为前置节点时，需要尊重 `no-store` 头，或在 CDN 管理台为 `me.joketop.com` 关闭缓存。

### 5. HTTPS 与 Cookie 设置

- `SECURE_RESUME_SECURE_COOKIE=1` 时，Actix 会将 Session Cookie 标记为 `Secure` + `HttpOnly` + `SameSite=Strict`，并通过 `DefaultHeaders` 强制 HSTS/安全响应头。
- 开发环境若需要通过 HTTP 访问，可临时 export `SECURE_RESUME_SECURE_COOKIE=0` 或不设置该变量（Debug 编译默认关闭 Secure 标记）。

### 6. 发布流程（示例）

```bash
# 1. 构建可执行文件
cargo build --release

# 2. 同步文件到服务器
rsync -av --delete target/release/secure_resume user@server:/home/ubuntu/secure-resume/
rsync -av templates/ user@server:/home/ubuntu/secure-resume/templates/
rsync -av static/ user@server:/home/ubuntu/secure-resume/static/

# 3. 重启服务
ssh user@server 'cd /home/ubuntu/secure-resume && pkill -F secure-resume.pid 2>/dev/null; SECURE_RESUME_SECURE_COOKIE=1 RUST_LOG=info nohup ./secure_resume > secure-resume.log 2>&1 & echo $! > secure-resume.pid'

# 4. 更新 Nginx 配置
ssh user@server 'cd /home/ubuntu/code-dojo/web-sites-hub && sudo ./deploy-all-docs.sh'
```

### 7. 运行与监控

- 健康检查：`curl -f http://127.0.0.1:8080/api/stats`
- 日志查看：`tail -f /home/ubuntu/secure-resume/secure-resume.log`
- 数据备份：定期备份 `/home/ubuntu/secure-resume/invites.db`

### 8. 安全最佳实践

- 通过防火墙限制 8080 端口只允许本机访问。
- CDN 或 Nginx 层开启速率限制、WAF，防止邀请码暴力破解。
- 建议定期轮换 `secure_resume_session` Cookie 名称或 Actix `Key`（通过持久化密钥而非随机生成）。
- 考虑将邀请码生成接口限制为管理 IP 或加密令牌。

该文档配合仓库中的 `joketop.conf` 与 `deploy-all-docs.sh` 一起使用，可实现 HTTPS、CDN 及 Rust 服务的统一部署。


