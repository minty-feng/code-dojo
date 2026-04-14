# 诗词模块（Poems Module）

## 入库位置与使用链路

### 入库位置

- 数据库类型：SQLite（当前默认）
- 数据库文件：`data/app.db`
- 目标数据表：`poems`
- 内容字段：
  - `content_simplified`：简体正文（默认 API `content` 使用该字段）
  - `content_traditional`：繁体正文

执行命令：

```bash
python scripts/poems/run.py
```

会将抓取并解析后的诗词数据写入 `data/app.db` 的 `poems` 表。

### 简繁处理规则（已实现）

入库前在解析阶段会统一执行简繁双向转换（基于 OpenCC）：

- 输入原文来自源字段：`content` 或 `paragraphs`
- 输出并入库：
  - `content_simplified`：转换后的简体正文
  - `content_traditional`：转换后的繁体正文

处理逻辑：

- 如果原文是繁体，`content_simplified` 会被转换为简体，`content_traditional` 保持繁体语义
- 如果原文是简体，`content_traditional` 会被补齐为繁体，`content_simplified` 保持简体语义
- API 兼容字段 `content` 默认返回 `content_simplified`

### `poems` 表字段说明

- `id`：自增主键
- `title`：兼容字段，默认存简体标题
- `title_simplified`：简体标题
- `title_traditional`：繁体标题
- `author`：作者名
- `dynasty`：朝代（如 唐/宋）
- `category`：分类（如 古诗/宋词）
- `content_simplified`：简体正文（前端默认展示）
- `content_traditional`：繁体正文（前端可切换展示）
- `tags`：标签，逗号分隔字符串
- `source`：来源标识（对应 `sources.yaml` 中 `name`）
- `source_url`：来源链接（本地源可为空）
- `created_at`：记录创建时间
- `updated_at`：记录更新时间

### 后端使用链路

- 爬虫入库：`scripts/poems/run.py` -> `scripts/poems/importer.py` -> `repo.upsert_poems(...)`
- 数据访问：`app/repositories/sqlalchemy_repo.py`
- 业务逻辑：`app/services/poem_service.py`
- API 暴露：`app/routers/poems.py`

### 前端使用方式

前端通过后端 API 获取数据，不直接读数据库文件：

- `GET /api/v1/poems`
- `GET /api/v1/poems/{poem_id}`
- `GET /api/v1/poems/meta/categories`

调用路径是：前端页面 -> FastAPI 接口 -> `poems` 表查询 -> 返回 JSON。

### 快速验证

1. 先执行入库：

```bash
python scripts/poems/run.py --skip-crawl
```

2. 启动后端：

```bash
uvicorn app.main:app --reload --port 8300
```

3. 验证数据：

- 打开 `http://127.0.0.1:8300/docs` 调用 `GET /api/v1/poems`
- 或在 `http://127.0.0.1:8300/admin` 查看 `Poems` 表数据

## API 清单

- `GET /api/v1/poems`
- `GET /api/v1/poems/{poem_id}`
- `GET /api/v1/poems/meta/categories`

## 列表接口参数

- `keyword`：标题/作者/内容关键词
- `category`：分类过滤
- `dynasty`：朝代过滤
- `page`：页码，从 1 开始
- `page_size`：每页条数，范围 `1..100`

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
        "title": "定风波",
        "author": "苏轼",
        "dynasty": "宋",
        "category": "宋词",
        "content": "...",
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

执行入口：`python scripts/poems/run.py`

- 默认执行顺序：抓取 -> 原始 JSON 落盘 -> 解析标准化 -> 入库（upsert）
- 原始数据目录：`data/raw/poems/`
- 执行日志文件：`data/logs/poems_pipeline.log`

### `--dry-run` 在做什么

`python scripts/poems/run.py --dry-run` 会执行：

- 抓取远程数据源（除非同时加 `--skip-crawl`）
- 解析并标准化字段（`title/author/dynasty/category/content/...`）
- 输出统计日志
- **不会写入数据库**（`inserted=0, updated=0`）

适用场景：验证网络连通、源数据结构、解析规则是否正确。

### 原始数据怎么获取

数据源由 `scripts/poems/sources.yaml` 配置：

- `name`：源名称（用于日志和 raw 文件名前缀）
- `url`：远程 JSON 地址（可选）
- `local_path`：本地 JSON 文件路径（优先用于离线导入）
- `local_glob`：批量匹配本地 JSON（支持递归通配）
- `enabled`：是否启用
- `category/dynasty`：该源默认字段（解析补齐）

脚本会将每个源抓取结果存为时间戳文件，例如：

- `data/raw/poems/poet_tang_0__20260414103022.json`

### 数据怎么更新

- 更新命令（全流程）：`python scripts/poems/run.py`
- 仅用本地已有 raw 重复导入：`python scripts/poems/run.py --skip-crawl`
- 导入策略是 **upsert**（按 `title + author`）：
  - 已存在：更新内容与元数据
  - 不存在：插入新记录
- 正文转换规则：
  - 若原文为繁体，自动生成简体并保留繁体
  - 若原文为简体，自动补齐繁体

### 常用命令

1. 抓取并落盘原始数据：

```bash
python scripts/poems/run.py
```

2. 仅解析与校验，不写库：

```bash
python scripts/poems/run.py --dry-run
```

3. 基于已有原始数据重复导入：

```bash
python scripts/poems/run.py --skip-crawl
```

### 常见问题

- `ConnectTimeout`（如 `raw.githubusercontent.com` 超时）：
  - 说明当前网络无法连通数据源
  - 现在可直接改为 `local_path`/`local_glob` 使用本地 `chinese-poetry` 数据
  - 或执行 `--skip-crawl` 使用已有原始文件

