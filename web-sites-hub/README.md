# Web Sites Hub 统一管理

本项目是一个整合了个人网站、前后端服务和文档站点的统一工作区。

## 📁 目录结构

以下路径均相对于仓库根目录（即 `web-sites-hub/` 为本工作区根）。

```
web-sites-hub/
│
├── frontend-portal/                           # 个人网站主入口 (Static HTML/JS)
│   ├── index.html                             # joketop.com 主页
│   ├── diary.html                             # 生活门户（六栏入口）
│   ├── journal.html                           # 日记
│   ├── timeline.html                          # 时光轴
│   ├── tianya.html                            # 天涯
│   ├── poems.html                             # 诗词
│   ├── goals.html                             # 目标（需后端登录）
│   ├── ganwu.html                             # 感悟
│   ├── learning.html                          # 学习笔记聚合页 (blog.joketop.com)
│   ├── showcase.html                          # 项目展示页
│   ├── resume.html                            # 简历页
│   ├── wufu.html                              # 五福
│   ├── fund.html                              # 基金
│   ├── speed.html                             # 测速
│   ├── assets/
│   │   ├── css/                               # 主样式 (main.css, diary.css 等)
│   │   └── js/                                # 主脚本 (main.js 等)
│   ├── scripts/
│   │   └── preview.sh                         # 本地预览 (默认 8000)
│   ├── package-joketop.sh                     # 打包与版本注入
│   └── README.md
│
├── frontend-docs/                             # 静态文档站点集合
│   ├── apple-ds-core-docs/                    # 数据结构 → blog.joketop.com/ds
│   ├── banana-algo-core-docs/                 # 算法 → blog.joketop.com/algo
│   ├── honey-backend-dojo-docs/               # 后端 → blog.joketop.com/backend
│   ├── grape-frontend-dojo-docs/              # 前端 → blog.joketop.com/frontend
│   └── cookie-os-network-docs/                # OS与网络 → blog.joketop.com/os
│
├── backend-diary/                             # 日记/目标后端 (Django 8100 + FastAPI 8200)
│   ├── manage.py                              # Django 入口
│   ├── django_app/                            # 认证、目标、提醒、事件等 (端口 8100)
│   ├── fastapi_app/                           # 数据查询服务 (端口 8200)
│   ├── app.py                                 # 单机 FastAPI 演示 (端口 5000)
│   ├── ARCHITECTURE.md                        # 混合架构与目标页登录说明
│   ├── README.md
│   └── scripts/
│       ├── run-all.sh                         # 同时启动 Django + FastAPI
│       └── run.sh                             # 仅 Django
│
├── backend-resume/                            # 安全简历服务 (Rust Actix-web)
│   └── src/
│
├── internship-trends/                         # 实习趋势/面试趋势 (独立项目)
│   ├── frontend/                              # 前端 (Vite + React/TS)
│   └── README.md
│
├── trending-aggregator/                       # 热点聚合 (独立项目)
│   ├── frontend/                              # Vue 前端
│   └── backend/                               # Node 后端
│
├── deploy-all-docs.sh                         # 统一 Nginx 部署脚本
├── apply-security-headers.sh                  # 安全头应用脚本
├── joketop.conf                               # Nginx 核心配置
├── DEPLOY-README.md                           # 部署详细说明
├── NGINX-CONFIG-README.md                     # Nginx 配置说明
├── APPLY-SECURITY-README.md                   # 安全头说明（如有）
└── README.md                                  # 本文件
```

## 🚀 服务概览

| 服务/站点 | 域名 | 本地路径 | 部署技术 |
|----------|------|----------|---------|
| **主站** | `joketop.com` | `web-sites-hub/frontend-portal/` | 静态 HTML |
| **简历** | `me.joketop.com` | `web-sites-hub/backend-resume/` | Rust (反向代理) |
| **日记** | `diary.joketop.com` | `web-sites-hub/frontend-portal/diary.html` | 静态 HTML |
| **目标/登录** | 同日记站内 | `web-sites-hub/backend-diary/` (Django 8100) | Django + JWT |
| **文档** | `blog.joketop.com/*` | `web-sites-hub/frontend-docs/` | 静态 HTML (Alias) |

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
