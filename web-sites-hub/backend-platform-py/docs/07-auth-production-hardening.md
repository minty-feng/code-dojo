# 生产级认证改造清单（从当前实现到可上线）

本文是对当前认证实现的工程化升级指南，目标是：
- 不中断现有业务
- 逐步提升安全性与可运维性
- 每一步都可回滚

适用对象：后端、前端、测试、运维。

---

## 1. 当前状态与风险基线

当前实现优点：
- 注册/登录/刷新/鉴权链路完整
- access + refresh 双 token 模型已建立
- 业务接口已有统一 Bearer 鉴权依赖

当前主要风险：
1. 密码仍是明文存储与明文比对
2. refresh token 无服务端状态，难以单点吊销
3. 无会话维度的设备管理（无法精确下线某设备）
4. token 存储在 Web Storage，XSS 风险面较大
5. 审计日志不足（难以做安全追踪与风控）

---

## 2. 改造目标（分级）

### L1 基础安全（必须）

1. 密码强哈希（Argon2 或 bcrypt）
2. refresh token 轮转（rotation）
3. refresh token 服务端可吊销
4. 登录失败限流与基础风控

### L2 可运维安全（推荐）

1. 会话模型（设备、IP、UA、最近活动时间）
2. 退出当前设备、退出全部设备
3. 审计日志（登录成功/失败、refresh、注销）
4. 异常会话检测（地区突变、频繁失败）

### L3 高安全架构（按需）

1. Web 端迁移到 HttpOnly Cookie + CSRF 防护
2. 引入 BFF 或网关统一鉴权
3. 第三方登录（OAuth2/OIDC）

---

## 3. 分阶段实施计划（建议 4 个迭代）

## Phase 1：密码安全化（优先级最高）

### 目标
- 消除明文密码风险

### 后端改造
1. 用户表新增字段：
- password_hash
- password_algo（可选，便于算法迁移）

2. 注册流程：
- 使用 Argon2/bcrypt 对密码哈希
- 只写入 password_hash

3. 登录流程：
- 使用 verify 函数比对密码与 hash

4. 兼容迁移策略：
- 保留旧 password 字段一段时间
- 用户首次登录成功后自动升级为 hash 并清理明文

### 验收标准
1. 数据库中不再出现新明文密码
2. 老用户可无感迁移登录
3. 压测下登录耗时可接受

### 回滚方案
- 保留双读逻辑（hash 优先，明文兜底）直到迁移完成

---

## Phase 2：refresh token 轮转 + 会话化

### 目标
- refresh token 可吊销、可追踪、可失效

### 数据模型建议
新增会话表（示例字段）：
- id（session_id，uuid）
- user_id
- refresh_token_hash
- device_id
- user_agent
- ip
- created_at
- last_seen_at
- expires_at
- revoked_at
- replaced_by（可选，用于 rotation 链）

### 协议与行为
1. 登录成功：
- 创建会话记录
- 生成 access + refresh（refresh 可携带 jti/session_id）

2. refresh：
- 校验 refresh token
- 校验会话状态（未吊销、未过期、hash 匹配）
- 通过后签发新 refresh 并使旧 refresh 失效（rotation）

3. 异常处理：
- 检测到已失效 refresh 被复用，立即吊销该会话链

### 验收标准
1. 同一个 refresh token 不能重复成功使用
2. 用户可在后台看到自己的会话列表
3. 能按 session 粒度下线

---

## Phase 3：前端存储与传输安全升级

### 目标
- 降低 token 暴露风险

### 方案 A（渐进式）
- 保持 Bearer 方案
- access token 放内存，refresh 放 HttpOnly Cookie
- 前端不再持久化 access 到 localStorage

### 方案 B（Web 优先推荐）
- access + refresh 都用 HttpOnly Cookie
- 前端不感知 token
- 所有 API 由 cookie 自动带上
- 配套 CSRF token 防护

### Cookie 策略建议
- HttpOnly: true
- Secure: true（生产必须 HTTPS）
- SameSite: Lax（或按跨站需求设 None + Secure）
- Path 精细化（例如 refresh 仅允许刷新接口使用）

### 验收标准
1. 前端 JS 无法读取关键 token
2. CSRF 防护在跨站请求中有效
3. 现有接口兼容性明确（灰度期间支持双模式）

---

## Phase 4：审计、风控与运营能力

### 目标
- 形成可观测、可追责、可运营的认证系统

### 建议能力
1. 审计日志
- login success/fail
- refresh success/fail
- logout current/all
- sensitive profile changes

2. 安全策略
- 登录失败频控（按 IP + 用户名）
- 异常地理位置告警
- 可配置账号冻结策略

3. 运维看板
- 日活登录用户数
- 登录失败率
- refresh 失败率
- 可疑会话数

---

## 4. API 演进建议（向后兼容）

## 4.1 新增接口

1. GET /api/v1/auth/sessions
- 查看当前用户会话列表

2. DELETE /api/v1/auth/sessions/{session_id}
- 下线指定设备

3. POST /api/v1/auth/logout
- 注销当前会话

4. POST /api/v1/auth/logout-all
- 注销全部会话（保留当前可选）

## 4.2 响应字段约定

建议在登录/刷新响应中补充：
- expires_in（秒）
- refresh_expires_in（秒，可选）
- session_id

---

## 5. 数据库迁移建议

使用迁移工具（如 Alembic）按版本推进：

1. V1
- users 增加 password_hash、password_algo

2. V2
- 新建 auth_sessions
- 新建 auth_audit_logs（可选）

3. V3
- 索引优化（user_id, revoked_at, expires_at, last_seen_at）

迁移原则：
- 先加字段，后切流量
- 先双写，后单写
- 先兼容读取，后清理旧字段

---

## 6. 安全配置基线（生产）

1. JWT_SECRET
- 必须使用高强度随机值，禁止默认值

2. token 生命周期
- access 建议 10 到 30 分钟
- refresh 建议 7 到 30 天，配合 rotation

3. 传输安全
- 全站 HTTPS
- HSTS

4. CORS
- 严格白名单
- 避免任意来源

5. 依赖安全
- 定期扫描依赖漏洞
- 固定关键库版本

---

## 7. 测试计划（必须覆盖）

## 7.1 单元测试

1. 密码 hash/verify
2. token 签发与类型校验
3. refresh 轮转逻辑
4. 会话吊销逻辑

## 7.2 集成测试

1. 注册->登录->访问受保护接口
2. access 过期->refresh->重试成功
3. refresh 重放攻击被拒绝
4. 单设备下线后该设备请求失败
5. 全设备下线后全部失败

## 7.3 安全测试

1. 暴力破解限流验证
2. CSRF 用例验证（cookie 模式）
3. XSS 场景下 token 暴露面验证

---

## 8. 发布与灰度策略

1. 灰度阶段 1
- 仅上线密码 hash，保持其余逻辑不变

2. 灰度阶段 2
- 上线会话表与 refresh rotation，保留旧刷新兜底短期兼容

3. 灰度阶段 3
- 上线前端新存储策略（内存或 HttpOnly Cookie）

4. 灰度阶段 4
- 清理旧兼容路径与旧字段

每个阶段要求：
- 指标观测 24 到 72 小时
- 异常可回滚
- 提前准备回滚脚本

---

## 9. 与当前代码的最小改造切入点

可先做最小闭环（1 到 2 天）：
1. 引入 password_hash 并改造 register/login
2. 增加登录失败限流
3. 缩短 access 过期时间到 30 分钟
4. 在 docs 与 README 标注风险与新策略

随后再进入 refresh rotation 与会话体系。

---

## 10. 结论

当前项目认证链路已具备业务可用性，但要达到生产安全基线，建议按本文四阶段推进：
- 先解决密码与 refresh 可控性
- 再做会话管理与可观测
- 最后再按场景决定是否迁移到 HttpOnly Cookie/BFF

这样可以在不推倒重来的前提下，逐步完成从开发态到生产态的升级。
