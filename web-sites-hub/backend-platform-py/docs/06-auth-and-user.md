# 认证与用户模块全解（Auth + Users）

本文面向前后端联调与后续演进，完整说明本项目当前登录体系：
- 登录/注册/刷新的接口与调用顺序
- token 是如何生成的
- token 当前保存在什么位置
- 其他受保护接口如何正确调用
- token 与 cookie 的区别
- 当前主流认证方案对比

---

## 1. 当前实现总览

当前项目采用 JWT Bearer 认证，核心特征：
- 登录成功返回一对 token：`access_token` + `refresh_token`
- 受保护接口通过 `Authorization: Bearer <access_token>` 访问
- access 过期后，用 refresh 调用刷新接口获取新 access
- 用户信息接口由依赖层统一从 Bearer token 中解析当前用户

相关实现文件：
- `app/routers/auth.py`
- `app/services/auth_service.py`
- `app/core/security.py`
- `app/dependencies.py`
- `app/routers/users.py`

---

## 2. 接口清单

### 2.1 认证接口

1. `POST /api/v1/auth/register`
2. `POST /api/v1/auth/login`
3. `POST /api/v1/auth/refresh`

### 2.2 用户接口

1. `GET /api/v1/users/me`（鉴权）
2. `PUT /api/v1/users/me`（鉴权）

---

## 3. 登录/注册/刷新流程

### 3.1 注册

请求：

```json
{
  "username": "demo_user",
  "password": "demo123456",
  "nickname": "Demo",
  "avatar": "🍉"
}
```

行为：
- 校验用户名非空、不能包含空格
- 检查用户名是否已存在
- 创建用户（当前版本密码为明文存储，见后文风险说明）
- 直接返回 token 对（注册即登录）

成功响应（示例）：

```json
{
  "success": true,
  "code": "OK",
  "message": "register success",
  "data": {
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "bearer"
  }
}
```

### 3.2 登录

请求：

```json
{
  "username": "demo_user",
  "password": "demo123456"
}
```

行为：
- 查询用户
- 比对密码
- 返回 `access_token` + `refresh_token`

### 3.3 刷新 access token

请求：

```json
{
  "refresh_token": "..."
}
```

行为：
- 校验 refresh token 签名、过期时间、token 类型
- 从 `sub` 提取 username
- 重新签发新的 access token

成功响应（示例）：

```json
{
  "success": true,
  "code": "OK",
  "message": "refresh success",
  "data": {
    "access_token": "...",
    "token_type": "bearer"
  }
}
```

---

## 4. token 是怎么生成的

### 4.1 签发逻辑

token 由 `app/core/security.py` 统一签发：
- `create_access_token(username)`
- `create_refresh_token(username)`

内部会调用 `_create_token(...)` 生成 JWT Payload，包含：
- `sub`: 用户名
- `type`: `access` 或 `refresh`
- `iat`: 签发时间（Unix 时间戳）
- `exp`: 过期时间（Unix 时间戳）

签名算法与密钥来自配置：
- `jwt_algorithm`：默认 `HS256`
- `jwt_secret`：默认读取环境变量 `JWT_SECRET`，未设置时使用默认值

### 4.2 过期时间

配置位置：`app/core/config.py`
- `access_token_exp_minutes`：默认 60 分钟
- `refresh_token_exp_days`：默认 14 天

### 4.3 校验逻辑

`decode_token(token, expected_type)` 会做：
- JWT 解码与签名校验
- 过期校验（过期返回 `TOKEN_EXPIRED`）
- 结构校验（`sub/type` 是否存在）
- 类型校验（例如 access 接口拒绝 refresh token）

---

## 5. token 目前保存在哪里

当前前端（`frontend-portal/assets/js/poem.js`）采用 Web Storage，未使用 Cookie：

读取顺序：
1. `localStorage`
2. `sessionStorage`

access token key 兼容：
- `authToken`
- `access_token`
- `accessToken`

refresh token key 兼容：
- `refresh_token`
- `refreshToken`

写入策略：
- 登录/注册成功后写入 `localStorage`

清理策略：
- 退出登录时清理 local + session 的全部兼容 key

说明：
- 当前不会通过 `Set-Cookie` 下发 token
- 当前请求默认通过 `Authorization` 头发送 token

---

## 6. 受保护接口如何使用

### 6.1 鉴权头格式

```text
Authorization: Bearer <access_token>
```

### 6.2 示例：获取当前用户

```bash
curl -s "http://127.0.0.1:8300/api/v1/users/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### 6.3 示例：更新用户资料

```bash
curl -s -X PUT "http://127.0.0.1:8300/api/v1/users/me" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{"nickname":"新昵称","bio":"新的签名"}'
```

### 6.4 示例：调用诗词收藏接口

```bash
curl -s "http://127.0.0.1:8300/api/v1/poems/favorites?page=1&page_size=20" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### 6.5 常见失败场景

1. 未带 token：`UNAUTHORIZED`（Missing bearer token）
2. token 过期：`TOKEN_EXPIRED`
3. token 非法或签名不对：`UNAUTHORIZED`（Invalid token）
4. token 类型错误（拿 refresh 调业务接口）：`UNAUTHORIZED`（Invalid token type）

---

## 7. token 与 cookie 的区别

### 7.1 token（Bearer）

特点：
- 前端主动保存（localStorage/sessionStorage/内存）
- 每次请求手动放到 `Authorization` 头
- API 服务更容易跨域/跨端复用（Web、App、小程序）

风险点：
- 若存 localStorage，XSS 成功后 token 可能被读走

### 7.2 cookie（会话或 JWT 放 cookie）

特点：
- 浏览器自动携带 cookie
- 可设置 `HttpOnly`（前端 JS 不能读取）降低 token 被 XSS 直接窃取风险
- 常结合 `SameSite`、`Secure` 做站点级防护

风险点：
- 需要重点防 CSRF（尤其 SameSite=None 场景）
- 跨域与子域策略配置复杂度更高

### 7.3 本项目当前状态

- 当前是 Bearer token 模式
- 当前没有 `HttpOnly Cookie` 登录态
- 当前前端不依赖 cookie

---

## 8. 主流认证方案对比（2026 常见）

### 方案 A：Session + Cookie（服务端会话）

适用：
- 传统 Web 单体、同域部署

优点：
- 服务端可随时失效会话
- cookie 可配 `HttpOnly`

缺点：
- 扩容需要会话共享（Redis 等）
- 前后端分离跨域场景更复杂

### 方案 B：JWT Access + Refresh（本项目当前路线）

适用：
- 前后端分离、多端接入、网关化 API

优点：
- 无状态，扩展性好
- 接入端统一用 Bearer

缺点：
- 吊销与强制下线需要额外机制（黑名单/版本号）
- token 存储策略需要严格防 XSS

### 方案 C：OAuth2 / OIDC（第三方身份）

适用：
- 需要 Google/GitHub/企业 SSO 登录

优点：
- 标准化程度高
- 易接入第三方身份体系

缺点：
- 协议复杂度较高
- 需要处理授权码流程、回调与状态安全

### 方案 D：BFF（Backend For Frontend）+ HttpOnly Cookie

适用：
- 高安全 Web 场景

优点：
- 前端通常不直接持有 access token
- 能显著降低 token 暴露面

缺点：
- 架构复杂度更高
- 前后端协作成本上升

### 方案 E：API Key / mTLS（服务到服务）

适用：
- 机器间调用、内部服务通信

说明：
- 一般不用于用户登录
- 常与用户态认证并存

---

## 9. 本项目后续建议（按优先级）

1. 密码改为强哈希存储

2. 增加 refresh token 轮转与撤销

3. 增加登录设备与会话管理

4. 考虑 Web 端升级到 HttpOnly Cookie + CSRF 防护

5. 增加认证审计日志

已补充生产级方案文档：`docs/07-auth-production-hardening.md`。

---

## 10. 一条完整联调路径（可直接执行）

```bash
# 1) 注册
curl -s -X POST "http://127.0.0.1:8300/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"auth_demo","password":"demo1234","nickname":"AuthDemo","avatar":"🐟"}'

# 2) 登录取 access_token
ACCESS_TOKEN=$(curl -s -X POST "http://127.0.0.1:8300/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"auth_demo","password":"demo1234"}' | jq -r '.data.access_token')

# 3) 访问 users/me
curl -s "http://127.0.0.1:8300/api/v1/users/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 4) refresh 获取新 access_token
REFRESH_TOKEN=$(curl -s -X POST "http://127.0.0.1:8300/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"auth_demo","password":"demo1234"}' | jq -r '.data.refresh_token')

curl -s -X POST "http://127.0.0.1:8300/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH_TOKEN\"}"
```

---

