# backend-platform-py Style Guide

本文件用于统一后端项目的命名与格式规范，避免后期扩展时出现风格割裂。默认适用于 `router / service / repository / schema / database / scripts` 全部层级。

## 1. 总体原则

- 约定优于配置：已有结构优先复用，不引入新的平行风格。
- 命名语义优先：名称直接表达业务含义，避免缩写和歧义。
- 前后端契约稳定：对外 API 一旦发布，非必要不破坏兼容。
- 单一职责：router 只处理协议，service 只处理业务，repository 只处理数据访问。

## 2. 目录与文件命名

- 目录统一使用小写蛇形：`app/routers`、`app/services`。
- Python 文件统一 `snake_case.py`，例如：`poem_service.py`、`sqlalchemy_repo.py`。
- 路由文件按业务域命名：`poems.py`、`users.py`、`auth.py`。
- Schema 文件按业务域命名：`poems.py` 或 `poem.py`（项目内保持一种）。
- 脚本目录固定为：`scripts/<domain>/`，例如：`scripts/poems/`。

## 3. Python 命名规范

- 类名：`PascalCase`，例如：`PoemModel`、`PoemQuery`。
- 函数/方法/变量：`snake_case`，例如：`list_poems`、`page_size`。
- 常量：`UPPER_SNAKE_CASE`，例如：`DEFAULT_PAGE_SIZE`。
- 布尔变量使用可读前缀：`is_`、`has_`、`can_`。

## 4. 数据库命名规范

### 4.1 表名

- 表名统一复数小写蛇形：`users`、`contents`、`poems`。
- 中间表使用 `<left>_<right>`：`poems_tags`。

### 4.2 字段名

- 字段统一小写蛇形：`created_at`、`updated_at`、`author_name`。
- 主键固定 `id`（除明确自然主键场景）。
- 外键统一 `<target>_id`，例如：`poem_id`、`user_id`。
- 时间字段统一：
  - 创建时间：`created_at`
  - 更新时间：`updated_at`
  - 删除标记（软删可选）：`deleted_at`

### 4.3 通用字段建议

- 内容实体建议包含：`id`, `title`, `author`, `category`, `source`, `created_at`, `updated_at`。
- 需要幂等导入的实体，增加唯一约束（如 `title + author`）或 `source_uid`。

## 5. API 路径与命名规范

- API 前缀统一：`/api/v1`。
- 资源路径统一使用复数名词：`/poems`、`/users`。
- 路径不使用动词，动作通过 HTTP 方法表达：
  - `GET /poems`：列表
  - `GET /poems/{id}`：详情
  - `POST /poems`：创建
  - `PUT /poems/{id}`：全量更新
  - `PATCH /poems/{id}`：部分更新
  - `DELETE /poems/{id}`：删除
- 扩展查询统一用 query 参数：`/poems?keyword=...&category=...`。

## 6. 接口参数与返回格式

### 6.1 Query 参数

- 分页参数统一：`page`（从 1 开始）、`page_size`。
- 搜索参数统一：`keyword`。
- 排序参数统一：`sort_by` + `order`（`asc`/`desc`）。

### 6.2 响应结构

保持项目现有统一响应包装：

```json
{
  "success": true,
  "code": "OK",
  "message": "ok",
  "data": {}
}
```

- 列表接口 `data` 使用：

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 0
}
```

## 7. Schema 命名规范（Pydantic）

- 入参模型后缀：`CreateRequest`、`UpdateRequest`、`QueryRequest`。
- 出参模型后缀：`Response`、`Item`。
- 分页出参可使用：`PoemListResponse`（内部含 `items/page/page_size/total`）。
- 字段名与数据库字段保持一致（除非明确需要别名映射）。

## 8. 错误码与异常规范

- 业务错误码统一大写蛇形：`POEM_NOT_FOUND`、`INVALID_PAGE_SIZE`。
- 错误码命名建议：`<DOMAIN>_<REASON>`。
- `message` 给用户可读信息，`code` 给程序稳定识别，不混用。

## 9. Repository / Service / Router 边界

- `router`：参数解析、调用 service、返回响应。
- `service`：业务规则、数据编排、事务边界（必要时）。
- `repository`：仅负责 CRUD，不包含业务判断。
- `repository` 返回字典结构时，键名必须稳定且统一。

## 10. 爬虫脚本命名与数据落地规范

- 目录固定：`scripts/poems/`。
- 文件职责建议：
  - `spider.py`：抓取原始数据
  - `parser.py`：清洗/标准化
  - `importer.py`：入库（upsert）
  - `run.py`：统一入口
- 原始数据落盘目录：`data/raw/poems/`（便于追溯与重放）。
- 清洗后字段统一为：
  - `title`, `author`, `dynasty`, `category`, `content`, `source`, `source_url`

## 11. 文档与注释规范

- 对外文档（`docs/`）优先中文，接口示例可中英混排。
- 函数注释写“做什么 + 输入输出约束”，避免重复代码表意。
- 对复杂逻辑仅补充必要注释，不写冗余注释。

## 12. 版本与兼容策略

- 破坏性变更必须升级 API 版本（如 `v1 -> v2`）。
- 非破坏性新增字段优先“向后兼容”，避免影响旧前端。
- 删除字段前需至少经历一个过渡版本。

---

如有新模块加入，先对照本文件命名再落代码；若确需例外，请在对应模块 README 记录原因与范围。
