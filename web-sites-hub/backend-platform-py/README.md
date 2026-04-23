# backend-platform-py

单服务（Monolith）后端模板，面向单人开发场景。

特点：
- 只启动一个服务，降低部署与运维复杂度
- 代码按业务域拆分，边界清晰（router / service / repository / schema）
- 统一响应结构、统一错误码、统一日志入口
- 使用 SQLAlchemy + SQLite 持久化数据（默认 `data/app.db`）
- 后续可按模块平滑拆分成多服务

## 目录结构

```text
backend-platform-py/
├── app/
│   ├── main.py
│   ├── core/
│   ├── routers/
│   ├── services/
│   ├── repositories/
│   └── schemas/
├── docs/
├── requirements.txt
└── README.md
```

## 快速启动

Python 版本要求：`3.12.x`

```bash
cd /Users/didi/Workspace/code-dojo/web-sites-hub/backend-platform-py
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8300
```

启动后会自动：
- 创建数据库文件：`backend-platform-py/data/app.db`
- 自动建表
- 自动注入初始演示数据（demo 用户、content、fund）

访问地址：
- OpenAPI: `http://127.0.0.1:8300/docs`
- 健康检查: `http://127.0.0.1:8300/api/v1/system/health`
- 管理后台: `http://127.0.0.1:8300/admin`

## 认证方式（JWT）

1. 新用户可先调用 `POST /api/v1/auth/register` 注册并获取 `access_token` 与 `refresh_token`
2. 已有用户调用 `POST /api/v1/auth/login` 获取 `access_token` 与 `refresh_token`
3. 访问受保护接口时带上请求头：

```text
Authorization: Bearer <access_token>
```

4. access token 过期后，调用 `POST /api/v1/auth/refresh` 刷新

## 已包含的业务域

- `auth`：注册、登录、刷新 token（JWT）
- `users`：用户信息查询与更新
- `content`：内容（诗词/文章）查询
- `fund`：基金查询与 CSV 导出占位
- `market`：行情辅助（`GET /api/v1/market/gold/quote`，可选 `GOLDAPI_IO_TOKEN` 对接 goldapi.io）
- `diary`：日记创建与查询
- `poems`：诗词列表、详情、分类查询
- `system`：健康检查、版本信息

更多设计说明见 `docs/`，推荐阅读：

- `docs/01-architecture.md`
- `docs/02-api-design.md`
- `docs/03-error-code.md`
- `docs/04-runbook.md`
- `docs/05-poems-module.md`
- `docs/06-auth-and-user.md`
- `docs/07-auth-production-hardening.md`
- `docs/08-server-deployment.md`
- `docs/09-fund-gold-desk.md`（基金占位、`fund.html` 黄金专题、`/market/gold/quote`）

## 诗词模块 API

- `GET /api/v1/poems?page=1&page_size=20&keyword=&author=&tag=&category=&dynasty=&sort=`
- `GET /api/v1/poems/{poem_id}`
- `GET /api/v1/poems/meta/categories`
- `GET /api/v1/poems/meta/dynasties`
- `GET /api/v1/poems/favorites`（需 Bearer Token）
- `POST /api/v1/poems/favorites`（需 Bearer Token）
- `DELETE /api/v1/poems/favorites/{poem_id}`（需 Bearer Token）
- `GET /api/v1/poems/favorites/status?poem_ids=1,2,3`（需 Bearer Token）
- `POST /api/v1/poems/favorites/sync`（需 Bearer Token）

## Gold xlsx 入库脚本

将 `data/gold_price_since_1978.xlsx` 与 `data/gold-premiums.xlsx` 导入 `data/app.db`：

```bash
cd web-sites-hub/backend-platform-py
python scripts/gold/import_xlsx.py
```

说明：
- 会自动按文件名创建/覆盖两张表（如 `gold_price_since_1978`、`gold_premiums`）
- Excel 首个非空行作为表头，列名自动规范化
- 每次重跑会覆盖目标表，适合重复导入

列表接口返回结构：

```json
{
  "success": true,
  "code": "OK",
  "message": "ok",
  "data": {
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 0
  }
}
```

## 诗词爬虫与入库

首次使用：

```bash
pip install -r requirements.txt
python scripts/poems/run.py
```

常用参数：

```bash
python scripts/poems/run.py --dry-run
python scripts/poems/run.py --skip-crawl
python scripts/poems/run.py --config scripts/poems/sources.yaml
```

说明：

- `--dry-run`：执行抓取和解析，但不写数据库
- `--skip-crawl`：跳过网络抓取，直接使用 `data/raw/poems/` 现有 JSON 导入
- 执行日志输出到：`data/logs/poems_pipeline.log`
- 数据源配置文件：`scripts/poems/sources.yaml`
- 数据源支持 `url`（远程）和 `local_path`/`local_glob`（本地）；已默认切到本地 `data/chinese-poetry-master`

## SQLAdmin 管理后台

- 入口：`/admin`
- 已注册数据模型：Users / Contents / Funds / Diary Entries / Poems / Poem Favorites
- 可执行查看、搜索、增删改查，便于单人开发期间的运营与调试
- 访问后台需要管理员账号密码（默认：`admin / admin123`）
- 默认仅允许本机访问 `/admin`（`127.0.0.1` / `::1` / `localhost`）；如需公网域名访问，设置 `ADMIN_ALLOW_REMOTE=true`
- 已启用访问频率限制：默认每个来源 `30` 次 / `60` 秒（超限返回 429）

可通过环境变量覆盖默认管理员配置：

```bash
export ADMIN_USERNAME=your_admin
export ADMIN_PASSWORD=your_strong_password
export ADMIN_SESSION_SECRET=your_session_secret
export ADMIN_ALLOW_REMOTE=true
export ADMIN_RATE_LIMIT_MAX_REQUESTS=30
export ADMIN_RATE_LIMIT_WINDOW_SECONDS=60
```
