# Web Sites Hub 统一管理

本项目是一个整合了个人网站、前后端服务和文档站点的统一工作区。

## 🗺️ 结构导读（先看这里）

为避免目录很多时难以快速定位，建议按下面四条主线理解本仓库：

1. **主站前端**：`frontend-portal/`  
2. **文档站集合**：`frontend-docs/`  
3. **后端能力层**：`backend-platform-py/`（当前推荐） + 其他历史/独立后端  
4. **独立项目区**：`super-app/`、`debate-competition/`、`phd-game/`、`internship-trends/`、`trending-aggregator/`

> 当前单人开发推荐主线：`frontend-portal/` + `backend-platform-py/`

## 📁 目录结构

以下路径均相对于仓库根目录（即 `web-sites-hub/` 为本工作区根）。

```text
web-sites-hub/
│
├── frontend-portal/                           # 主站前端（核心入口）
│   ├── index.html                             # joketop.com 首页
│   ├── diary.html / goals.html / poems.html   # 生活与内容页面
│   ├── showcase.html / resume.html            # 项目展示与简历页
│   ├── assets/                                # 主样式与脚本
│   ├── scripts/preview.sh                     # 本地预览（默认 8000）
│   └── package-joketop.sh                     # 打包脚本
│
├── backend-platform-py/                       # 统一单服务后端（推荐）
│   ├── app/                                   # FastAPI 应用代码（JWT/SQLAlchemy/SQLAdmin）
│   ├── docs/                                  # 后端架构与运行文档
│   ├── requirements.txt
│   └── README.md
│
├── frontend-docs/                             # 文档站点集合（blog.joketop.com/*）
│   ├── apple-ds-core-docs/
│   ├── banana-algo-core-docs/
│   ├── grape-frontend-dojo-docs/
│   ├── honey-backend-dojo-docs/
│   └── cookie-os-network-docs/
│
├── backend-diary/                             # 历史后端：Django + FastAPI 混合架构
├── backend-resume/                            # Rust 简历服务
│
├── internship-trends/                         # 独立项目（前后端）
├── trending-aggregator/                       # 独立项目（前后端）
├── super-app/                                 # 独立前端项目
├── debate-competition/                        # 独立前端项目
├── phd-game/                                  # 独立前端项目
├── siyuan-editor/                             # 独立编辑器项目
│
├── deploy-all-docs.sh                         # 统一部署脚本
├── apply-security-headers.sh                  # 安全头应用脚本
├── joketop.conf / joketop-http.conf           # Nginx 配置
├── DEPLOY-README.md
├── NGINX-CONFIG-README.md
├── APPLY-SECURITY-README.md
└── README.md
```

## 🧱 目录分组说明

- **核心主线（推荐）**
  - `frontend-portal/`：主站与业务页面
  - `backend-platform-py/`：统一单服务后端（JWT、SQLAlchemy、SQLAdmin）
  - `frontend-docs/`：文档子站构建产物
- **历史/并行后端**
  - `backend-diary/`：Django + FastAPI 混合架构（历史链路）
  - `backend-resume/`：简历服务（Rust）
- **独立项目**
  - `internship-trends/`、`trending-aggregator/`、`super-app/`、`debate-competition/`、`phd-game/`、`siyuan-editor/`
- **部署与运维**
  - `joketop.conf`、`joketop-http.conf`、`deploy-all-docs.sh`、`apply-security-headers.sh`

## 🚀 服务概览

| 服务/站点 | 域名 | 本地路径 | 部署技术 |
|----------|------|----------|---------|
| **主站** | `joketop.com` | `web-sites-hub/frontend-portal/` | 静态 HTML |
| **简历** | `me.joketop.com` | `web-sites-hub/backend-resume/` | Rust (反向代理) |
| **日记** | `diary.joketop.com` | `web-sites-hub/frontend-portal/diary.html` | 静态 HTML |
| **目标/登录** | 同日记站内 | `web-sites-hub/backend-diary/` (Django 8100) | Django + JWT |
| **文档** | `blog.joketop.com/*` | `web-sites-hub/frontend-docs/` | 静态 HTML (Alias) |

## 🧩 独立前端项目（补充）

以下项目与 `frontend-portal/` 分离，按独立工程维护：

| 项目 | 路径 | 技术栈 | 本地启动 |
|------|------|--------|---------|
| **人民公社 Super App** | `web-sites-hub/super-app/` | React 18 + TypeScript + Vite + Electron | `npm install && npm run dev` |
| **AI 大模型辩论赛** | `web-sites-hub/debate-competition/` | Vite 前端应用 | `npm install && npm run dev` |
| **PhD Simulator** | `web-sites-hub/phd-game/` | 文本模拟游戏（前端构建项目） | `npm install && npm run build && npm start` |

说明：
- `fund` 相关能力目前归入 `backend-platform-py`（`/api/v1/fund/*`）。
- `internship-trends/` 与 `trending-aggregator/` 仍为独立全栈项目（前后端分目录维护）。

## 🛠️ 快速开始

### 1. 启动前端主站预览

```bash
cd web-sites-hub/frontend-portal
./scripts/preview.sh
# 访问 http://localhost:8000
```

### 2. 启动目标页登录与日记后端（Django）

```bash
cd web-sites-hub/backend-diary
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8100
# 目标页 goals.html 登录/注册对接 http://127.0.0.1:8100/api/auth/
```

详见 `web-sites-hub/backend-diary/README.md` 与 `web-sites-hub/backend-diary/ARCHITECTURE.md`。

### 3. 部署生产环境

```bash
cd web-sites-hub
sudo ./deploy-all-docs.sh --letsencrypt --email your@email.com
```

## 📖 访问地址

- **主站**: https://joketop.com
- **简历**: https://me.joketop.com
- **学习站点**: https://blog.joketop.com

**文档子站：**
- Backend: https://blog.joketop.com/backend
- Frontend: https://blog.joketop.com/frontend
- 数据结构: https://blog.joketop.com/ds
- 算法: https://blog.joketop.com/algo
- 操作系统和网络: https://blog.joketop.com/os

## 🔧 架构特点

### 模块化分层
- **frontend-***: 所有前端资源，包括主站门户 (`portal`) 和文档 (`docs`)。
- **backend-***: 动态服务后端，按功能拆分 (`poems`, `resume`)。

### 统一配置管理

1. **使用 `^~` 修饰符** - 确保 alias location 优先匹配
2. **移除嵌套 location** - 避免路径解析问题
3. **删除全局静态资源规则** - 防止干扰 alias
4. **简化脚本** - 从 1069 行减少到 374 行（-65%）

## 📖 详细文档

- **web-sites-hub/DEPLOY-README.md** - 部署脚本使用说明
- **web-sites-hub/NGINX-CONFIG-README.md** - Nginx 配置详解
- **web-sites-hub/backend-diary/README.md** - 日记/目标后端 API 与启动
- **web-sites-hub/backend-diary/ARCHITECTURE.md** - 混合架构与目标页登录设计
- **web-sites-hub/frontend-portal/README.md** - 主站与 diary 子页说明

## 🎯 已修复的问题

- ✅ 多个 server_name 冲突
- ✅ location 块在 server 外部
- ✅ CSS 样式加载失败
- ✅ favicon 不显示
- ✅ 证书管理复杂
- ✅ 配置生成错误

## 🔒 证书管理

脚本自动处理 Let's Encrypt 证书：
- 首次部署时使用临时 HTTP 配置
- 获取证书后切换到 HTTPS 配置
- 每个域名独立证书目录

## 📝 添加新服务

1. 在 `web-sites-hub/joketop.conf` 中添加 location 块
2. 在 `web-sites-hub/deploy-all-docs.sh` 的 SERVICES 数组中添加条目
3. 重新部署

详见 `web-sites-hub/DEPLOY-README.md`。
