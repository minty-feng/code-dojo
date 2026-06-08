# 10 API 安全加固（接口保护 + 限流）

本文描述 `backend-platform-py` 的 API 安全分级、已落地的 P0 改造，以及后续迭代计划。

相关文档：
- 认证深度改造：`07-auth-production-hardening.md`
- 部署与环境变量：`08-server-deployment.md`
- 自动化巡检：`deploy/verify-api-security.sh`

---

## 1. 背景与风险基线

2026-05 外网巡检发现：

| 问题 | 影响 |
|------|------|
| `GET /api/v1/invite/list` 无鉴权 | 任意人可枚举全部邀请码明文 |
| `GET /api/v1/invite/stats`、`POST /invite/generate` 无鉴权 | 池状态泄露 / 任意造码 |
| `POST /auth/login`、`/auth/register` 无限流 | 暴力破解、刷注册 |
| `POST /invite/verify`、`/resume/auth` 无限流 | 邀请码暴力猜测 |
| Nginx 反代后 `request.client.host` 为 127.0.0.1 | 按 IP 限流失效（已在 P0 修复） |

公开读接口（snippets、poems、content、market 等）**刻意保持无 JWT**，供 portal 同域 `/api/` 直接访问。

---

## 2. 接口分级

| 级别 | 代表接口 | 策略 |
|------|----------|------|
| L0 公开只读 | `/snippets`、`/poems` 列表、`/system/health` | 不限 JWT；**GET 目录限流 120/min/IP** |
| L1 公开 + 风控 | `/auth/login`、`/auth/register`、`/invite/verify`、`/resume/auth` | **IP 滑动窗口限流** |
| L2 用户 JWT | `/users/me`、`/poems/favorites/*` | Bearer access token |
| L3 运维密钥 | `/invite/list`、`/invite/stats`、`/invite/generate` | **`X-Admin-Key` 请求头** |
| L4 页面 Session | `/resume` 页面 | SessionMiddleware + 邀请码验证 |

---

## 3. P0 已落地（当前版本）

### 3.1 Invite 管理接口 — `X-Admin-Key`

受保护路由：
- `GET /api/v1/invite/list`
- `GET /api/v1/invite/stats`
- `POST /api/v1/invite/generate`

请求示例：

```bash
curl -s "https://joketop.com/api/v1/invite/stats" \
  -H "X-Admin-Key: YOUR_ADMIN_API_KEY"
```

未带 Key 或 Key 错误 → `403 FORBIDDEN`。  
服务端未配置 `ADMIN_API_KEY` → `503 ADMIN_KEY_NOT_CONFIGURED`（防止误以为已保护）。

实现：`app/dependencies.py` → `require_admin_api_key`

`POST /api/v1/invite/generate` 另设 **IP 限流**（独立 `invite_generate` 桶，配额与 verify 相同，默认 5/min），在 Admin Key 校验之前生效，减轻暴力猜 Key 的压力。

### 3.2 Auth 登录/注册限流

路径（POST）：
- `/api/v1/auth/login`
- `/api/v1/auth/register`

默认：**10 次 / 60 秒 / IP**（可 env 覆盖）。

超限 → `429 TOO_MANY_REQUESTS`。

### 3.3 邀请码验证限流

路径（POST）：
- `/api/v1/invite/verify`
- `/api/v1/resume/auth`

默认：**5 次 / 60 秒 / IP**（共用 `invite_verify` 桶）。

### 3.4 客户端 IP 解析

`app/core/rate_limit.py` → `get_client_ip()`  
优先读取 `X-Forwarded-For`（首段）、`X-Real-IP`，与 Nginx 反代配置一致。

Admin 面板限流逻辑已统一到同一模块。

### 3.5 公开目录限流（poems / snippets）

路径（GET，共用 `catalog` 桶）：
- `/api/v1/poems` 及子路径（列表、详情、meta、wordcloud 等）
- `/api/v1/snippets` 及子路径

默认：**120 次 / 60 秒 / IP**。

**为何优先于 diary：** 前者外网公开、数据量大（全库诗词 + 代码片段），易被爬虫批量拉取；diary 几乎无数据且访问量低，鉴权可后置。

正常浏览（诗词页首开约 5 个 GET、snippets 列表 + 点选详情）远低于配额；脚本化翻页爬库会在约 2 分钟/page 时被 429 拦住。

---

## 4. 环境变量

在 `deploy/backend-platform-py.env` 中配置（**勿提交真实值**）：

```bash
# P0 — invite 管理（必填，生产）
ADMIN_API_KEY=replace-with-long-random-string

# P0 — 限流开关与配额
RATE_LIMIT_ENABLED=true
AUTH_RATE_LIMIT_MAX_REQUESTS=10
AUTH_RATE_LIMIT_WINDOW_SECONDS=60
INVITE_VERIFY_RATE_LIMIT_MAX_REQUESTS=5
INVITE_VERIFY_RATE_LIMIT_WINDOW_SECONDS=60

# 公开目录（GET /poems*、/snippets*）
CATALOG_RATE_LIMIT_MAX_REQUESTS=120
CATALOG_RATE_LIMIT_WINDOW_SECONDS=60

# 已有 — Admin 面板
ADMIN_RATE_LIMIT_MAX_REQUESTS=30
ADMIN_RATE_LIMIT_WINDOW_SECONDS=60
```

生成随机 Key：

```bash
./deploy/generate-admin-api-key.sh
# 或打包时自动提示：./deploy/package-backend-platform-py-no-data.sh
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 5. 部署与验证

### 5.1 部署步骤

1. 在服务器 `deploy/backend-platform-py.env` 写入 `ADMIN_API_KEY`
2. 打包部署并重启：`./deploy/start-backend-platform-py.sh restart`
3. 运行安全巡检：

```bash
./deploy/verify-api-security.sh --base https://joketop.com --rate-limit-burst 15
```

### 5.2 P0 验收标准

| 检查项 | 期望 |
|--------|------|
| 无 Key 访问 `/invite/list` | HTTP 403 |
| 带正确 `X-Admin-Key` | HTTP 200 |
| 连续 12 次错误 login | 至少 1 次 HTTP 429 |
| `/users/me` 无 Token | HTTP 401（保持） |
| `/snippets` | HTTP 200（保持公开） |

### 5.3 运维常用命令

```bash
# 查看邀请码池（需 Admin Key）
curl -s "http://127.0.0.1:8300/api/v1/invite/stats" \
  -H "X-Admin-Key: $ADMIN_API_KEY"

# 手动补码
curl -s -X POST "http://127.0.0.1:8300/api/v1/invite/generate" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: $ADMIN_API_KEY" \
  -d '{}'
```

---

## 6. 上线后必做（安全响应）

P0 只**阻止新的未授权访问**，无法撤销已被扫走的邀请码。

建议立即：
1. 登录服务器，用 Admin Key 调用 `GET /invite/list`
2. 作废或标记所有 **未使用且可能泄露** 的 key（或清空后 `generate` 补池）
3. 轮换 `ADMIN_API_KEY`（若怀疑泄露）

---

## 7. 后续迭代（P1 / P2）

| 优先级 | 项 | 说明 |
|--------|-----|------|
| ~~P1~~ | ~~公开读接口宽松全局限流~~ | ✅ poems/snippets GET 120/min |
| ~~P2~~ | ~~Diary~~ | ✅ 已彻底移除（API + 表 + Admin） |
| P1 | Nginx `limit_req_zone` | 网关层第一道防线 |
| P1 | market / fund 读接口限流 | 可选；gold 已有上游节流 |
| P2 | 密码 Argon2/bcrypt | 见 `07-auth-production-hardening.md` Phase 1 |
| P2 | refresh 会话化 + rotation | Phase 2 |
| P3 | Redis 共享限流桶 | 多 worker / 多机部署时 |

---

## 8. 代码索引

| 文件 | 职责 |
|------|------|
| `app/core/rate_limit.py` | 滑动窗口、IP 解析、429 响应 |
| `app/core/config.py` | 限流与 Admin Key 配置 |
| `app/dependencies.py` | `require_admin_api_key` |
| `app/routers/invite.py` | 管理接口挂载鉴权 |
| `app/main.py` | Auth / invite verify 限流中间件 |
| `deploy/verify-api-security.sh` | 自动化回归巡检 |

---

## 9. 结论

P0 以最小改动关闭最高风险面：**invite 管理密钥化 + auth/verify 限流 + 反代 IP 修复**。  
公开内容 API 行为不变；深度认证改造继续按 `07-auth-production-hardening.md` 分阶段推进。
