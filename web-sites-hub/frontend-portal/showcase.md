# 项目展示清单 (Showcase Record)

本文档记录 `showcase.html` 中展示的所有项目及其状态。

## 🌟 精选项目 (Featured)

| 项目名称 | 描述 | 技术栈 | 链接/状态 |
|---------|------|-------|----------|
| **分布式任务调度系统** | 高性能分布式任务调度系统，支持定时任务、延迟队列、优先级调度。 | Go, Redis, Docker, K8s | [GitHub](#) |
| **实时数据可视化平台** | 企业级实时数据监控与可视化平台，支持插件化扩展。 | React, TS, WebSocket, D3 | [Demo](#) |

## 📂 全部项目 (All Projects)

### 工具 (Tools)

| 项目名称 | 描述 | 技术栈 | 链接/状态 |
|---------|------|-------|----------|
| **CLI 工具集** | 日常开发工具集合，包含代码生成、文件处理等实用命令。 | Node.js, Commander | [GitHub](#) |
| **基金估值助手** | 实时追踪基金净值，智能辅助投资决策。 | Python, FastAPI, Vanilla JS | [`fund.html`](fund.html) |
| **全球网速测试** | 集成 Speedtest, Fast, Cloudflare 等主流测速工具。 | HTML5, Utility | [`speed.html`](speed.html) |

### Web 应用 (Web Apps)

| 项目名称 | 描述 | 技术栈 | 链接/状态 |
|---------|------|-------|----------|
| **代码片段管理** | 个人代码片段收藏与语法高亮展示。 | C++, 算法 | [`/snippets`](/snippets) |
| **百福迎春生成器** | 定制专属福字，自动生成百福图鉴。 | HTML5, CSS3, Vanilla JS | [`wufu.html`](wufu.html) |

### Monorepo 子应用（先在各目录执行 `yarn build`）

与子目录 `dist/` 对应；`prepare-preview-site.sh` 铺平发布后链接为 `{项目名}/index.html`。

| 项目名称 | 描述 | 技术栈 | 链接/状态 |
|---------|------|-------|----------|
| **AI 与大模型简史** | 里程碑时间线与专题筛选（与 `showcase.html` 同页卡片一致）。 | Timeline, Vanilla | [`aihistory.html`](aihistory.html) |
| **phd-game / PhD Simulator** | 博士生模拟文字策略游戏。 | TypeScript, Webpack, YAML | [`phd-game/dist/index.html`](phd-game/dist/index.html) |
| **super-app / 人民公社** | 综合门户式多模块应用。 | React, Vite, TypeScript | [`super-app/dist/index.html`](super-app/dist/index.html) |
| **debate-competition / AI 大模型辩论赛** | 中外模型按席次轮番发言、当前发言人高亮。 | React, Vite | [`debate-competition/dist/index.html`](debate-competition/dist/index.html) |
| **internship-trends / 实习趋势数据站** | 实习校招榜单、公司与趋势可视化。 | React, Vite, Recharts | [`internship-trends/dist/index.html`](internship-trends/dist/index.html) |

## 📅 更新日志

- **2026-05-29**: 移除占位项目卡片（API 网关服务、Markdown 编辑器、健康追踪 App、微服务框架）；移除「文件检索平台」；不可见字符页增加主题切换。
- **2026-04-28**: `showcase.html` 与本文档补充 **debate-competition**、**internship-trends**，Monorepo 表集中记录 phd-game、super-app、debate-competition、internship-trends、`aihistory`。
- **2026-02-03**: 新增「全球网速测试」 (`speed.html`)。
- **2026-02-03**: 新增「百福迎春生成器」 (`wufu.html`)。
- **2025-05-20**: 新增「基金估值助手」 (`fund.html`)。
