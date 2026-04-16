# 08 服务端部署指南（仅后端）

本文只介绍后端服务部署，不包含前端发布方案。

---

## 1. 适用范围

当前项目后端技术栈：
- FastAPI + Uvicorn
- SQLAlchemy
- SQLite（默认 `data/app.db`）

说明：
- 现有实现默认使用本地 SQLite 文件，适合单机部署。
- 若要做多副本水平扩容，建议后续迁移到 PostgreSQL/MySQL，再做无状态扩展。

---

## 2. 推荐部署拓扑

生产建议（单机稳定版）：

1. `systemd` 托管 `uvicorn` 进程
2. `Nginx` 反向代理（80/443）
3. HTTPS 证书（Let's Encrypt）
4. 本机防火墙只开放 80/443

拓扑：

```text
Internet
  -> Nginx(:443, TLS)
  -> Uvicorn(:8300, localhost)
  -> SQLite(data/app.db)
```

---

## 3. 服务器准备

假设服务器系统为 Ubuntu 22.04+。

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv nginx git
```

创建运行用户（可选但推荐）：

```bash
sudo useradd -r -m -d /opt/backend-platform-py -s /usr/sbin/nologin backend
```

拉取代码（示例路径）：

```bash
sudo mkdir -p /opt/backend-platform-py
sudo chown -R $USER:$USER /opt/backend-platform-py
cd /opt/backend-platform-py
git clone <你的仓库地址> .
```

---

## 4. 安装依赖与初始化

```bash
cd /opt/backend-platform-py
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

首次启动会自动建表并注入 demo 数据，建议先手动验收一次：

```bash
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8300
```

健康检查：

```bash
curl -s http://127.0.0.1:8300/api/v1/system/health
```

---

## 5. 环境变量建议

创建环境变量文件：`/etc/backend-platform-py.env`

```bash
sudo tee /etc/backend-platform-py.env >/dev/null <<'EOF'
JWT_SECRET=replace-with-strong-random-secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=replace-with-strong-password
ADMIN_SESSION_SECRET=replace-with-strong-session-secret
ADMIN_ALLOW_REMOTE=true
ADMIN_RATE_LIMIT_MAX_REQUESTS=30
ADMIN_RATE_LIMIT_WINDOW_SECONDS=60
CORS_ALLOW_ORIGINS=https://api.example.com,https://www.example.com,https://joketop.com,https://showcase.joketop.com
EOF
```

注意：
- `JWT_SECRET` 必须替换为高强度随机值。
- 生产环境不要使用默认管理员密码。
- 如果需要通过公网域名访问 `/admin`，设置 `ADMIN_ALLOW_REMOTE=true`。
- `CORS_ALLOW_ORIGINS` 按实际域名配置，不要保留开发地址。
- 如果最终采用同域 `/api/` 反向代理，优先保留前端实际访问域名，例如 `https://joketop.com` 或 `https://showcase.joketop.com`。

---

## 6. systemd 托管

创建服务文件：`/etc/systemd/system/backend-platform-py.service`

```ini
[Unit]
Description=backend-platform-py FastAPI service
After=network.target

[Service]
Type=simple
User=backend
Group=backend
WorkingDirectory=/opt/backend-platform-py
EnvironmentFile=/etc/backend-platform-py.env
ExecStart=/opt/backend-platform-py/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8300
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

生效并启动：

```bash
sudo chown -R backend:backend /opt/backend-platform-py
sudo systemctl daemon-reload
sudo systemctl enable backend-platform-py
sudo systemctl start backend-platform-py
sudo systemctl status backend-platform-py
```

查看日志：

```bash
sudo journalctl -u backend-platform-py -f
```

---

## 7. Nginx 反向代理（详细版）

本节给出可直接用于生产的 Nginx 方案。

### 7.1 为什么需要 Nginx

1. 对外统一入口（80/443），应用端口 `8300` 只在本机可见
2. HTTPS 证书托管与自动续期更成熟
3. 可增加限流、访问控制、安全头、日志审计
4. 业务进程和网络入口解耦，便于后续扩展

### 7.2 推荐监听策略

Uvicorn 只监听本机：

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8300
```

防火墙仅开放 `80/443`，不开放 `8300`。

### 7.3 Nginx 生产配置示例

创建站点配置：`/etc/nginx/sites-available/backend-platform-py`

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=20r/s;

upstream backend_platform_py {
  server 127.0.0.1:8300;
  keepalive 64;
}

server {
  listen 80;
  server_name api.example.com;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl http2;
  server_name api.example.com;

  # certbot 会自动写入证书路径
  ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_prefer_server_ciphers on;
  ssl_session_timeout 1d;
  ssl_session_cache shared:SSL:10m;

  access_log /var/log/nginx/backend-platform-py.access.log;
  error_log /var/log/nginx/backend-platform-py.error.log warn;

  # 常用安全头
  add_header X-Frame-Options SAMEORIGIN always;
  add_header X-Content-Type-Options nosniff always;
  add_header Referrer-Policy strict-origin-when-cross-origin always;

  # 单 IP 限流（可按业务调节）
  limit_req zone=api_limit burst=40 nodelay;

  client_max_body_size 10m;
  keepalive_timeout 65;

  location / {
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    proxy_connect_timeout 5s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    proxy_pass http://backend_platform_py;
  }
}
```

### 7.4 启用与验证

```bash
sudo ln -s /etc/nginx/sites-available/backend-platform-py /etc/nginx/sites-enabled/backend-platform-py
sudo nginx -t
sudo systemctl reload nginx
```

检查是否生效：

```bash
curl -I http://api.example.com
curl -I https://api.example.com/api/v1/system/health
```

期望：
1. `http` 返回 `301` 跳转到 `https`
2. `https` 返回 `200`

### 7.5 HTTPS 证书（certbot）

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.example.com
```

验证自动续期：

```bash
sudo certbot renew --dry-run
```

### 7.6 和前端联调时的接入方式

1. 前端统一请求 `https://api.example.com`
2. 不再请求 `http://<ip>:8300`
3. 若前后端不同域名，后端 `CORS_ALLOW_ORIGINS` 必须包含前端域名

### 7.7 接入现有静态站点 Nginx（joketop 风格）

如果你已经有类似 `web-sites-hub/joketop.conf` 的静态站点配置，建议直接把后端挂到现有站点的 `/api/` 前缀下，而不是额外暴露 `8300` 或强依赖独立子域。

这样做的好处：
1. 前端可直接用相对路径 `/api/v1/...`
2. 本地开发和线上部署的前端代码可以共用一套接口拼接逻辑
3. 后续若收藏、登录态改成 Cookie，也更容易保持同站策略

下面是贴近现有主站配置的示例，保留静态文件缓存，同时为后端预留 `/api/`：

```nginx
upstream backend_platform_py {
  server 127.0.0.1:8300;
  keepalive 64;
}

server {
  listen 443 ssl http2;
  server_name joketop.com www.joketop.com;

  ssl_certificate /etc/letsencrypt/live/joketop.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/joketop.com/privkey.pem;

  root /var/www/html/joketop;
  index index.html;

  access_log /var/log/nginx/joketop.com.access.log;
  error_log /var/log/nginx/joketop.com.error.log warn;

  location ^~ /api/ {
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_connect_timeout 5s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    proxy_pass http://backend_platform_py;
  }

  location / {
    try_files $uri $uri/ =404;
  }

  location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot|pdf)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }
}
```

注意：
1. `location ^~ /api/` 要放在静态资源缓存规则之前，避免 API 被错误命中静态 location
2. `proxy_pass http://backend_platform_py;` 不带 URI，才能保留原始 `/api/v1/...` 路径
3. 如果后端管理页也走该站点，`/admin` 会随同 `/api` 外的普通路由一起经过同域访问策略评估，建议上线前确认鉴权与缓存头

### 7.8 常见问题排查

1. `502 Bad Gateway`
- 检查 Uvicorn 是否运行：`sudo systemctl status backend-platform-py`
- 检查是否监听 `127.0.0.1:8300`：`ss -lntp | grep 8300`

2. 证书申请失败
- 检查 DNS 是否解析到当前服务器
- 检查 80 端口是否放行

3. 跨域失败（CORS）
- 检查 `/etc/backend-platform-py.env` 中 `CORS_ALLOW_ORIGINS`
- 修改后重启服务：`sudo systemctl restart backend-platform-py`

4. Nginx 配置改完不生效
- 先 `sudo nginx -t`
- 再 `sudo systemctl reload nginx`

### 7.9 同域部署模板（推荐）

如果你希望前端和后端使用同一个域名（例如 `www.example.com`，或当前的 `joketop.com` / `showcase.joketop.com`），推荐把 API 挂到 `/api/` 前缀下。

优点：
1. 前端可直接使用相对路径请求（如 `/api/v1/poems`）
2. CORS 配置更简单，跨域问题更少
3. 后续若使用 Cookie 登录态，更容易控制同站策略

Nginx 示例（同域 + API 前缀）：

```nginx
upstream backend_platform_py {
  server 127.0.0.1:8300;
  keepalive 64;
}

server {
  listen 80;
  server_name www.example.com;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl http2;
  server_name www.example.com;

  ssl_certificate /etc/letsencrypt/live/www.example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/www.example.com/privkey.pem;

  # 前端静态资源目录（按你的实际路径修改）
  root /var/www/frontend;
  index index.html;

  # API 请求转发到后端
  location /api/ {
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://backend_platform_py;
  }

  # 非 SPA 站点可改成 try_files $uri $uri/ =404;
  location / {
    try_files $uri $uri/ /index.html;
  }
}
```

前端请求建议：
1. 使用相对路径：`/api/v1/system/health`
2. 不再写死 `http://ip:8300`
3. 本地开发可保留 `http://127.0.0.1:8300/api/v1`，上线后切换为同域 `/api/v1`

后端环境变量建议：
1. 同域部署时，`CORS_ALLOW_ORIGINS` 可以只保留同域 HTTPS 地址
2. 例如：`CORS_ALLOW_ORIGINS=https://www.example.com`

---

## 8. 发布与回滚流程

### 发布

```bash
cd /opt/backend-platform-py
git fetch --all
git checkout <发布分支或tag>
source .venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
sudo systemctl restart backend-platform-py
```

### 回滚

```bash
cd /opt/backend-platform-py
git checkout <上一个稳定tag>
source .venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
sudo systemctl restart backend-platform-py
```

---

## 9. 数据与备份（SQLite）

数据库文件默认在：`data/app.db`。

建议：
1. 每日定时备份
2. 备份文件保留最近 7 到 30 天
3. 定期做恢复演练

示例备份命令：

```bash
cd /opt/backend-platform-py
mkdir -p backups
sqlite3 data/app.db ".backup 'backups/app-$(date +%F-%H%M%S).db'"
```

crontab 示例（每天 03:30）：

```cron
30 3 * * * cd /opt/backend-platform-py && sqlite3 data/app.db ".backup 'backups/app-$(date +\%F-\%H\%M\%S).db'"
```

---

## 10. 上线验收清单

1. 健康检查通过：`/api/v1/system/health`
2. OpenAPI 可访问：`/docs`
3. 认证链路可用：register -> login -> users/me
4. 诗词查询可用：`/api/v1/poems`
5. 收藏接口鉴权可用：`/api/v1/poems/favorites`
6. 管理后台可访问且已修改默认密码：`/admin`
7. systemd 自动拉起生效
8. Nginx 与 HTTPS 正常
9. 日志可追踪（journalctl + nginx access/error）
10. 备份任务已启用并验证可恢复

---

## 11. 生产安全基线（最少项）

1. 更换所有默认密钥与密码
2. 仅开放 80/443，应用端口仅本机监听
3. 开启 HTTPS，禁用明文管理入口
4. 定期升级系统与依赖包
5. 开启失败登录监控和访问频率审计

---

## 12. 后续扩展建议

1. 将 SQLite 迁移到 PostgreSQL
2. 引入 Alembic 做可追踪迁移
3. 引入进程指标与告警（Prometheus/Grafana）
4. 将部署流程纳入 CI/CD（tag 发布、自动回滚）


