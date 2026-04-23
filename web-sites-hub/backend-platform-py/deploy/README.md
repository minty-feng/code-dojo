# backend-platform-py deploy

提供一套最小可用的后端部署模板，目标是：

- 本地一键打包后端代码
- 服务器快速解包并通过目录内脚本启动 `uvicorn`
- 与主站统一 Nginx 配置协作

## 目录说明

```text
deploy/
├── config/
│   └── backend-platform-py.env.example
├── package-backend-platform-py-no-data.sh
├── package-backend-platform-py.sh
└── start-backend-platform-py.sh
```

## 1. 本地打包

在 `backend-platform-py` 根目录执行：

```bash
./deploy/package-backend-platform-py.sh
```

如需打一个不包含 `data/` 的发布包（线上保留已有数据库文件）：

```bash
./deploy/package-backend-platform-py-no-data.sh
```

产物示例：

```text
backend-platform-py-20260416-213000.tar.gz
```

## 2. 服务器解包

```bash
sudo mkdir -p /opt/backend-platform-py
sudo tar -xzf backend-platform-py-20260416-213000.tar.gz -C /opt/backend-platform-py --strip-components=1
```

## 3. 准备环境变量

```bash
cp deploy/config/backend-platform-py.env.example deploy/config/backend-platform-py.env
vim deploy/config/backend-platform-py.env
```

至少修改：

- `JWT_SECRET`
- `ADMIN_PASSWORD`
- `ADMIN_SESSION_SECRET`
- `CORS_ALLOW_ORIGINS`

## 4. 启动后端

```bash
cd /opt/backend-platform-py
./deploy/start-backend-platform-py.sh
```

脚本会：

- 启动前校验项目根目录下 `.venv`
- 自动激活 `.venv` 后再启动服务
- 优先加载 `deploy/config/backend-platform-py.env`
- 使用 `nohup` 后台启动 `uvicorn`
- 把日志写到项目根目录 `backend-platform-py.log`

首次启动前请先准备虚拟环境并安装依赖：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

如线上机器访问默认 PyPI 慢，可先手动安装依赖：

```bash
source .venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

默认监听：

- `127.0.0.1:8300`

启动成功后可检查：

```bash
curl http://127.0.0.1:8300/api/v1/system/health
tail -f backend-platform-py.log
```

## 5. 配置 nginx

本项目不再单独维护后端 Nginx 站点配置。

统一在 `web-sites-hub/joketop.conf` 中配置同域 `/api/` 反向代理：

```nginx
location ^~ /api/ {
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://backend_platform_py;
}
```

也就是说：

- `deploy/` 目录只负责后端打包、启动、环境变量
- 对外入口统一由 `joketop.conf` 管理
- 前端页面与后端 API 共享同一域名，通过 `/api/` 转发给 `127.0.0.1:8300`

## 6. `window.POEMS_API.baseUrl` 是怎么来的

前端诗词页按下面顺序决定接口地址：

1. 先读取 `frontend-portal/assets/js/poem.config.js` 里的 `window.POEMS_API.baseUrl`
2. 如果该值为空：
   - 本地 `localhost` / `127.0.0.1` / `file:` 预览时，自动用 `http://127.0.0.1:8300/api/v1`
   - 线上域名访问时，自动用当前域名下的 `/api/v1`

所以：

- 你不写 `baseUrl` 也可以
- 只要 nginx 把 `/api/` 转发给后端，诗词页就能直接访问同域接口
- 如果以后要切到 `https://api.xxx.com/api/v1`，只要改 `poem.config.js` 即可
