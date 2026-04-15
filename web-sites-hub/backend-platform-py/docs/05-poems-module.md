# 诗词模块（Poems Module）

## 入库位置与使用链路

### 入库位置

- 数据库类型：SQLite（默认）
- 数据库文件：`data/app.db`
- 目标数据表：`poems`

执行命令（推荐使用项目虚拟环境）：

```bash
./.venv/bin/python scripts/poems/run.py
```

### 简繁处理规则（当前版本）

入库解析阶段会统一执行 OpenCC 转换，核心文本字段只保留简繁双字段：

- 标题：
  - `title_simplified`
  - `title_traditional`
- 作者：
  - `author_simplified`
  - `author_traditional`
- 正文：
  - `content_simplified`
  - `content_traditional`

解析输入兼容：

- 标题来源：`title` 或（宋词）`rhythmic`
- 正文来源：`content` 或 `paragraphs`

### `poems` 表字段说明（无旧字段）

- `id`：自增主键
- `title_simplified` / `title_traditional`
- `author_simplified` / `author_traditional`
- `dynasty`：朝代
- `category`：分类
- `content_simplified` / `content_traditional`
- `tags`：标签（逗号分隔字符串）
- `source`：来源标识（对应 source 配置中的 `name`）
- `source_url`：来源链接（本地源可为空）
- `created_at` / `updated_at`

唯一键约束：

- `(title_simplified, author_simplified)`

### 后端使用链路

- 爬虫入库：`scripts/poems/run.py` -> `scripts/poems/importer.py` -> `repo.upsert_poems(...)`
- 数据访问：`app/repositories/sqlalchemy_repo.py`
- 业务逻辑：`app/services/poem_service.py`
- API 暴露：`app/routers/poems.py`

### 前端使用方式

前端通过 API 获取数据，不直接读数据库：

- `GET /api/v1/poems`
- `GET /api/v1/poems/{poem_id}`
- `GET /api/v1/poems/meta/categories`
- `GET /api/v1/poems/meta/dynasties`
- `GET /api/v1/poems/favorites`（鉴权）
- `POST /api/v1/poems/favorites`（鉴权）
- `DELETE /api/v1/poems/favorites/{poem_id}`（鉴权）
- `GET /api/v1/poems/favorites/status?poem_ids=1,2,3`（鉴权）
- `POST /api/v1/poems/favorites/sync`（鉴权）

调用路径：前端页面 -> FastAPI 接口 -> `poems` / `poem_favorites` 表查询 -> JSON 返回。

## API 清单

- `GET /api/v1/poems`
- `GET /api/v1/poems/{poem_id}`
- `GET /api/v1/poems/meta/categories`
- `GET /api/v1/poems/meta/dynasties`
- `GET /api/v1/poems/favorites`（鉴权）
- `POST /api/v1/poems/favorites`（鉴权）
- `DELETE /api/v1/poems/favorites/{poem_id}`（鉴权）
- `GET /api/v1/poems/favorites/status?poem_ids=1,2,3`（鉴权）
- `POST /api/v1/poems/favorites/sync`（鉴权）

## 列表接口参数

- `keyword`：标题/作者/内容关键词
- `author`：作者关键词（简繁均可匹配）
- `tag`：标签关键词
- `category`：分类过滤
- `dynasty`：朝代过滤
- `page`：页码，从 1 开始
- `page_size`：每页条数，范围 `1..100`
- `sort`：排序方式，取值：
  - `default`
  - `title_asc`
  - `author_asc`
  - `dynasty_asc`

## 列表返回结构

```json
{
  "success": true,
  "code": "OK",
  "message": "ok",
  "data": {
    "items": [
      {
        "id": 1,
        "title_simplified": "定风波",
        "title_traditional": "定風波",
        "author_simplified": "苏轼",
        "author_traditional": "蘇軾",
        "dynasty": "宋",
        "category": "宋词",
        "content_simplified": "...",
        "content_traditional": "...",
        "tags": "",
        "source": "poet_song_0",
        "source_url": ""
      }
    ],
    "page": 1,
    "page_size": 20,
    "total": 1200
  }
}
```

## 数据导入

执行入口：`./.venv/bin/python scripts/poems/run.py`

- 默认执行顺序：抓取 -> 原始 JSON 落盘 -> 解析标准化 -> 入库（upsert）
- 原始数据目录：`data/raw/poems/`
- 执行日志文件：`data/logs/poems_pipeline.log`

### `--dry-run` 在做什么

`./.venv/bin/python scripts/poems/run.py --dry-run` 会执行：

- 抓取远程数据源（除非同时加 `--skip-crawl`）
- 解析并标准化字段（`title/author/dynasty/category/content/...`）
- 输出统计日志
- **不会写入数据库**（`inserted=0, updated=0`）

适用场景：验证网络连通、源数据结构、解析规则是否正确。

### 原始数据怎么获取

数据源由 `scripts/poems/*.yaml` 配置，常用示例：

- `scripts/poems/sources.yaml`（基础示例）
- `scripts/poems/sources.quantangshi.yaml`（全唐诗分片）
- `scripts/poems/sources.songci.yaml`（宋词分片）
- `scripts/poems/sources.yudingquantangshi.yaml`（御定全唐詩）
- `scripts/poems/sources.quantangshi.single.yaml`（全唐诗单文件）

- 推荐源数据下载地址（chinese-poetry）：
  - `https://github.com/chinese-poetry/chinese-poetry/archive/refs/heads/master.zip`
- 推荐流程：先下载并解压 `master.zip` 到本地目录（如 `data/chinese-poetry-master/`），再通过 `scripts/poems/run.py` 抓取/解析并入库

- `name`：源名称（用于日志和 raw 文件名前缀）
- `url`：远程 JSON 地址（可选）
- `local_path`：本地 JSON 文件路径（优先用于离线导入）
- `local_glob`：批量匹配本地 JSON（支持递归通配）
- `enabled`：是否启用
- `category/dynasty`：该源默认字段（解析补齐）

脚本会将每个本地源文件落盘为独立 raw 文件（避免覆盖），例如：

- `data/raw/poems/poet_tang_0__poet.tang.0__20260415072307841261.json`

示例（下载并解压到 `data/`）：

```bash
cd web-sites-hub/backend-platform-py/data
curl -L -o chinese-poetry-master.zip https://github.com/chinese-poetry/chinese-poetry/archive/refs/heads/master.zip
unzip -o chinese-poetry-master.zip
```

解压后在 `scripts/poems/sources.yaml` 里配置对应的 `local_path` 或 `local_glob`，再执行：

```bash
./.venv/bin/python scripts/poems/run.py
```

### 数据怎么更新

- 更新命令（全流程）：`./.venv/bin/python scripts/poems/run.py`
- 仅用本地已有 raw 重复导入：`./.venv/bin/python scripts/poems/run.py --skip-crawl`
- 导入策略是 **upsert**（按 `title_simplified + author_simplified`）：
  - 已存在：更新内容与元数据
  - 不存在：插入新记录
- 注意：当前已移除“每次导入前全表 normalize”步骤，避免历史数据标准化时触发唯一键冲突。

### 重复键扫描（运维脚本）

用于排查历史重复键冲突：

```bash
./.venv/bin/python scripts/poems/scan_duplicates.py --limit 200
```

输出 `duplicate_groups=0` 表示当前库不存在 `(title_simplified, author_simplified)` 重复组。

### 常用命令

1. 抓取并落盘原始数据：

```bash
./.venv/bin/python scripts/poems/run.py
```

2. 仅解析与校验，不写库：

```bash
./.venv/bin/python scripts/poems/run.py --dry-run
```

3. 基于已有原始数据重复导入：

```bash
./.venv/bin/python scripts/poems/run.py --skip-crawl
```

### 常见问题

- `ConnectTimeout`（如 `raw.githubusercontent.com` 超时）：
  - 说明当前网络无法连通数据源
  - 现在可直接改为 `local_path`/`local_glob` 使用本地 `chinese-poetry` 数据
  - 或执行 `--skip-crawl` 使用已有原始文件
- `UNIQUE constraint failed: poems.title_simplified, poems.author_simplified`：
  - 说明存在重复唯一键冲突（常见于历史脏数据）
  - 先执行 `scan_duplicates.py` 查看冲突组
  - 确认冲突后再做定向合并/清理

