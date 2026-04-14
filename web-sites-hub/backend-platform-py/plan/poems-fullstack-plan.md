# 古诗词模块前后端与数据计划（Poems Fullstack Plan）

本文档基于最初开发计划整理，并结合当前项目实际实现状态更新，作为后续迭代与验收基线。

## 1. 项目目标

- 将 `frontend-portal/poems.html` 升级为真实前后端分离页面
- 在 `backend-platform-py` 建立独立诗词领域（模型/仓储/服务/路由）
- 建立可重复执行的诗词数据管道（抓取/解析/入库/更新）
- 支持简体与繁体双内容存储与前端切换展示

## 2. 范围说明

### 2.1 后端范围

- 诗词领域模型：`PoemModel`
- 诗词接口：列表、详情、分类
- 数据管道：`scripts/poems/` 全链路
- 文档：接口、导入、字段、简繁规则

### 2.2 前端范围

- `poems.html` 从后端 API 拉取主数据
- 保留最小 fallback 兜底能力
- 支持简繁切换（默认简体）

### 2.3 本期不做

- `poem_tags` 多对多结构（先用 `tags` 文本字段）
- 复杂推荐/搜索排序算法
- 后台任务调度系统（先以命令脚本驱动）

## 3. 后端开发计划（backend-platform-py）

## Phase 1：诗词领域建模（已完成）

### 建模与约束

- 独立表：`poems`
- 主字段：
  - `id, title, author, dynasty, category`
  - `content_simplified, content_traditional`
  - `tags, source, source_url, created_at, updated_at`
- 索引：
  - `title`、`author`、`category` 普通索引
  - `(title, author)` 唯一约束（防重核心）

### 迁移策略

- 通过 `init_db()` + 兼容迁移逻辑确保老库可升级
- 不写死诗词种子数据，避免内容污染

## Phase 2：仓储/服务/路由（已完成）

### 仓储层

`app/repositories/sqlalchemy_repo.py` 已提供：

- `list_poems(keyword, category, dynasty, page, page_size)`
- `get_poem(poem_id)`
- `list_poem_categories()`
- `upsert_poems(items)`

说明：

- 已加入“批内去重 + 库内 upsert”，避免唯一索引冲突
- 返回导入统计含 `deduplicated`

### 服务层

`app/services/poem_service.py`：

- 分页参数校验
- 统一调用仓储层
- 错误处理规范化

### 路由层

`app/routers/poems.py` 并挂载到 `main.py`：

- `GET /api/v1/poems`
- `GET /api/v1/poems/{poem_id}`
- `GET /api/v1/poems/meta/categories`

可选下一步：

- `GET /api/v1/poems/random?limit=10`

## Phase 3：响应契约与文档（已完成）

- 沿用统一响应包装：`success/code/message/data`
- 分页结构：
  - `data: { items, page, page_size, total }`
- 文档现状：
  - `docs/05-poems-module.md`（模块主文档）
  - `README.md`（快速使用与命令）

## 4. 数据管道计划（爬虫/解析/入库）

## Phase 4：脚本结构（已完成）

目录：

- `scripts/poems/spider.py`
- `scripts/poems/parser.py`
- `scripts/poems/importer.py`
- `scripts/poems/run.py`
- `scripts/poems/sources.yaml`
- `data/raw/poems/`（原始文件归档）
- `data/logs/poems_pipeline.log`（执行日志）

## Phase 5：采集策略（已调整并落地）

原计划是远程采集；当前已升级为“本地优先 + 远程兼容”：

- 支持 `sources.yaml` 配置：
  - `url`（远程）
  - `local_path`（本地单文件）
  - `local_glob`（本地批量）
- 当前默认使用本地 `chinese-poetry` 数据导入
- 网络超时时可持续使用本地源，不阻塞流程

## Phase 6：入库策略（已完成）

### upsert 规则

- 业务主键：`(title, author)`
- 已存在：更新正文与元数据（分类/标签/来源/更新时间）
- 不存在：插入新记录

### 简繁规则

- 解析阶段统一生成：
  - `content_simplified`
  - `content_traditional`
- 原文简/繁都可自动补齐另一种

### 输出统计

- `total / inserted / updated / deduplicated`
- 失败原因通过日志输出（source 级别）

### 常用命令（当前实现）

```bash
python scripts/poems/run.py
python scripts/poems/run.py --dry-run
python scripts/poems/run.py --skip-crawl
```

后续可扩展参数：

- `--limit`（限制导入数量）
- `--full`（全量模式开关）
- `--timeout-seconds` / `--max-retries`

## 5. 前端改造计划（frontend-portal/poems.html）

## Phase 7：前端 API 化（部分完成）

已完成：

- 主数据来自后端 API（`/api/v1/poems`）
- 保留 fallback 兜底
- 适配后端统一返回结构（`data.items`）
- 增加简繁切换（读取双内容字段）

建议下一步：

- 抽离内联脚本到 `assets/js/poems.js`
- 增加关键词搜索、分类筛选、分页/加载更多

## Phase 8：联调与容错（部分完成）

已完成：

- 后端 CORS 配置
- API 不可用时前端 fallback

待增强：

- 页面 toast 级提示
- API Base URL 环境变量化（dev/prod）

## 6. 验收标准

- `/docs` 可见 poems 接口，分页过滤可用
- `data/app.db` 的 `poems` 表存在真实诗词数据
- `poems.html` 在线时由 API 驱动渲染
- 后端离线时页面可降级显示
- `scripts/poems/run.py` 可重复执行并增量更新
- 简繁双字段入库与前端切换可用

## 7. 建议实施顺序（后续迭代）

1. 补 `random` 等扩展接口
2. 前端脚本拆分与交互增强（搜索/筛选/分页）
3. 扩展 `sources.yaml` 到批量全量导入
4. 增加数据质量统计（重复率、空字段率）
5. 补充自动化测试（API + 导入脚本）

## 8. 关联文档

- `style.md`（命名与规范）
- `docs/05-poems-module.md`（模块说明与操作）
- `README.md`（快速启动）
