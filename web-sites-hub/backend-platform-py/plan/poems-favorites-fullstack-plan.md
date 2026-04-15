# 收藏前后端联动执行方案

## 1. 目标与范围

- 目标：将诗词收藏从前端 `localStorage` 升级为登录用户维度的后端持久化，支持跨设备同步、幂等操作与渐进迁移。
- 范围内：
  - 后端：数据库模型、Repository/Service/Router、鉴权接入、接口文档。
  - 前端：收藏状态改造、本地到服务端迁移、乐观更新与失败回滚。
  - 联调：接口验收、兼容性验证、回归测试。
- 范围外（后续迭代）：
  - 收藏夹分组、批量操作、收藏备注、消息通知。

## 2. 现状与问题

- 当前收藏存于 `poem.js` 的 `localStorage`（`poems-favorites-v1`）。
- key 基于 `title + author`，存在文本变体和简繁切换漂移风险。
- 无用户隔离、无跨端同步、无后端审计与统计能力。

## 3. 设计原则

- 关系建模正确：收藏是 `user` 与 `poem` 的多对多关系，不放入 `poems` 表单字段。
- 幂等优先：重复收藏/取消不报错，确保前端重试安全。
- 渐进迁移：先兼容老数据，再切新 key，最后收敛到服务端真相。
- 用户体验优先：乐观更新，失败回滚，不阻塞页面渲染。
- 与现有架构一致：遵循 `router -> service -> repository` + `ok()` 统一响应。

## 4. 数据库方案

### 4.1 新增表 `poem_favorites`

字段：

- `id`：主键
- `user_id`：用户 ID（索引）
- `poem_id`：诗词 ID（索引）
- `created_at`：首次收藏时间
- `updated_at`：最近状态变化时间
- `deleted_at`：软删除时间（null = 当前已收藏）
- 唯一约束：`UNIQUE(user_id, poem_id)`

### 4.2 约束与索引

- 索引建议：
  - `(user_id, deleted_at, updated_at)`：我的收藏分页
  - `(user_id, poem_id)`：单条关系查找
- 软删除可支持未来恢复收藏、审计与增量同步。

## 5. 后端接口契约

统一前缀：`/api/v1/poems/favorites`，全部需要 Bearer Token。

### 5.1 获取收藏列表

- `GET /api/v1/poems/favorites`
- 入参：`page`, `page_size`, `sort`
- 出参：`items/page/page_size/total`，每项包含 `poem_id` + `poem` 摘要字段

### 5.2 收藏一首诗（幂等）

- `POST /api/v1/poems/favorites`
- body：`{ "poem_id": 123 }`
- 语义：已收藏返回成功，不重复插入

### 5.3 取消收藏（幂等）

- `DELETE /api/v1/poems/favorites/{poem_id}`
- 语义：未收藏也返回成功

### 5.4 批量查询收藏状态

- `GET /api/v1/poems/favorites/status?poem_ids=1,2,3`
- 出参：`map`，key 为 `poem_id` 字符串，value 为布尔值

### 5.5 首次迁移同步

- `POST /api/v1/poems/favorites/sync`
- body：`{ "poem_ids": [1,2,3] }`
- 语义：将本地收藏并入服务端并返回最终收藏集合

## 6. 分层实现方案（按现有代码组织）

### 6.1 `app/core/database.py`

- 新增 `PoemFavoriteModel`
- 在 `init_db()` 阶段通过 `create_all` 自动建表

### 6.2 `app/repositories/sqlalchemy_repo.py`

新增方法：

- `add_poem_favorite(user_id, poem_id)`
- `remove_poem_favorite(user_id, poem_id)`
- `list_poem_favorites(user_id, page, page_size, sort)`
- `get_poem_favorite_status_map(user_id, poem_ids)`
- `sync_poem_favorites(user_id, poem_ids)`

实现要点：

- `POST`：存在且 `deleted_at` 非空则恢复；存在且 active 则 no-op；不存在则插入
- `DELETE`：active 记录置 `deleted_at=now()`；无记录 no-op
- `LIST`：仅返回 `deleted_at is null` 记录

### 6.3 `app/services/poem_service.py`

新增业务方法，负责：

- 参数校验（`page/page_size/sort/poem_ids`）
- 用户解析（通过 `username` 获取 `user_id`）
- `poem_id` 存在性校验（不存在抛 `POEM_NOT_FOUND`）
- 编排仓储调用并返回接口结构

### 6.4 `app/routers/poems.py`

新增路由：

- `GET /favorites`
- `POST /favorites`
- `DELETE /favorites/{poem_id}`
- `GET /favorites/status`
- `POST /favorites/sync`

全部接入 `Depends(get_current_username)`，响应统一 `ok(...)`。

### 6.5 `app/schemas/poems.py`

新增请求模型：

- `PoemFavoriteCreateRequest`
- `PoemFavoriteSyncRequest`

## 7. 前端改造方案（`frontend-portal/assets/js/poem.js`）

### 7.1 状态结构升级

- 新存储 key：`poems-favorites-v2`
- 收藏 key 从 `title__author` 改为 `poem.id`
- 保留 `poems-favorites-v1` 一次性迁移并落迁移标记

### 7.2 初始化流程

1. 读取 v2 本地缓存并渲染（快速首屏）
2. 执行旧版迁移（v1 -> v2）
3. 若未登录：本地模式继续
4. 若已登录：
   - 调用 `/favorites/sync` 上传本地 ids
   - 调用 `/favorites` 拉服务端最终状态
   - 覆盖本地缓存为服务端镜像

### 7.3 心形点击流程（乐观更新）

- 先本地切换 UI + 写入缓存
- 登录态下异步发 `POST/DELETE`
- 失败时回滚本地并提示同步失败

### 7.4 列表状态优化

- 首选：列表接口直接返回 `is_favorite`（后续迭代）
- 当前：调用 `/favorites/status` 批量回填当前页心形状态

## 8. 执行阶段与里程碑

### Phase 1（后端基础，0.5-1 天）

- 建表 + 三核心接口（list/add/remove）
- Swagger 可调通
- 核心手测通过

### Phase 2（前端联动，0.5 天）

- key 升级、乐观更新、失败回滚
- 登录态对接收藏接口
- 收藏页切服务端数据

### Phase 3（迁移与优化，0.5 天）

- `sync` 接口 + 本地迁移收口
- `status` 批量接口 + 列表性能优化
- 文档补齐与回归测试

## 9. 测试与验收标准

### 9.1 功能验收

- 登录用户收藏后刷新仍保留
- 同账号跨端可见一致
- 重复收藏/取消不报错（幂等）
- 简繁切换不影响收藏状态

### 9.2 接口验收

- 缺鉴权返回 401
- 诗词不存在返回 404 + 业务码
- 分页参数非法返回 400
- `status` 对非法输入可控失败

### 9.3 回归点

- 词云、检索、分页、详情链路无回归
- 收藏导出/清空按钮与新状态一致

## 10. 风险与应对

- 风险：旧 key 无 `poem_id`
  - 应对：迁移仅处理含 `id` 的条目；其余忽略
- 风险：并发点击状态抖动
  - 应对：按钮短暂禁用或请求排队
- 风险：服务端失败导致状态不一致
  - 应对：失败回滚 + 启动时服务端重拉校准
- 风险：SQLite 分页性能下降
  - 应对：补组合索引并按 `updated_at desc` 分页

## 11. 回滚方案

- 后端回滚：下线路由，不动主业务表
- 前端回滚：继续使用本地缓存模式
- 数据安全：收藏关系独立，不污染 `poems` 主数据

## 12. 交付清单

- 代码文件：
  - `app/core/database.py`
  - `app/repositories/sqlalchemy_repo.py`
  - `app/services/poem_service.py`
  - `app/routers/poems.py`
  - `app/schemas/poems.py`
  - `frontend-portal/assets/js/poem.js`
- 文档文件：
  - `docs/05-poems-module.md`
  - `README.md`
- 验收材料：
  - 接口验收用例清单
  - 前端手测清单
