# 11 Diary 模块：前端梳理与后端下线记录

> 状态：**已彻底移除** backend-platform-py 中的 diary 能力（2026-05）  
> 公开 API、ORM 模型、`diary_entries` 表、SQLAdmin 视图均已删除。

生活站前端（`diary.joketop.com` 静态页）**从未**调用 `/api/v1/diary/*`，下线无影响。

---

## 1. 已从 backend-platform-py 删除

| 项 | 说明 |
|----|------|
| HTTP | `GET/POST /api/v1/diary/entries` |
| 代码 | `routers/diary.py`、`services/diary_service.py`、`schemas/diary.py`、repo 方法 |
| ORM | `DiaryEntryModel` |
| Admin | SQLAdmin「Diary Entry」 |
| SQLite | 启动时 `DROP TABLE IF EXISTS diary_entries`（`init_db`） |

---

## 2. 全仓库结论：无前端对接 :8300 diary API

`frontend-portal` 内无任何 `fetch` 指向 `/api/v1/diary/entries`。

---

## 3. diary.joketop.com 页面（静态，仍保留）

| 页面 | 调 API |
|------|--------|
| `diary.html`、`journal.html` 等 | 否（静态 HTML / `diary.js` 仅 UI） |
| `goals.html` | 指向本地 `:8100` Django 规划，与 backend-platform-py 无关 |

Nginx：`diary.joketop.com` **无** `/api/` 反代。

---

## 4. 若将来恢复动态日记

1. 选定页面（如 `journal.html`）
2. 配置 `/api/` 网关
3. 重新建表 + JWT，参考 `docs/07-auth-production-hardening.md`

---

## 5. 变更记录

| 日期 | 说明 |
|------|------|
| 2026-05-31 | 梳理前端；确认无 `/api/v1/diary/entries` 调用 |
| 2026-05-31 | 移除公开 diary API |
| 2026-05-31 | 删除测试数据；移除 `diary_entries` 表与 Admin |
