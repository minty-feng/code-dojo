# Web Sites Hub 统一管理

本项目是一个整合了个人网站、前后端服务和文档站点的统一工作区。

## 📁 目录结构

```
web-sites-hub/
│
├── frontend-portal/                # 个人网站主入口 (Static HTML/JS)
│   ├── index.html                  # joketop.com 主页
│   ├── learning.html               # 学习笔记聚合页
│   ├── showcase.html               # 项目展示页
│   ├── resume.html                 # 简历页
│   ├── diary.html                  # 生活门户 (含时光轴、诗词等子模块)
│   └── scripts/
│       └── preview.sh              # 本地预览脚本
│
├── frontend-docs/                  # 静态文档站点集合
│   ├── apple-ds-core-docs/         # 数据结构教程
│   ├── banana-algo-core-docs/      # 算法教程
│   ├── honey-backend-dojo-docs/    # 后端教程
│   ├── grape-frontend-dojo-docs/   # 前端教程
│   └── cookie-os-network-docs/     # OS与网络教程
│
├── backend-poems/                  # 诗词服务 (Python FastAPI)
│   ├── main.py                     # API 入口
│   └── requirements.txt
│
├── backend-resume/                 # 安全简历服务 (Rust Actix-web)
│   └── src/
│
├── deploy-all-docs.sh              # 统一 Nginx 部署脚本
├── joketop.conf                    # Nginx 核心配置文件
├── DEPLOY-README.md                # 部署详细说明
└── NGINX-CONFIG-README.md          # Nginx 配置说明
```

## 🚀 服务概览

| 服务/站点 | 域名 | 本地对应目录 | 部署技术 |
|----------|------|-------------|---------|
| **主站** | `joketop.com` | `frontend-portal/` | 静态 HTML |
| **简历** | `me.joketop.com` | `backend-resume/` | Rust (反向代理) |
| **日记** | `diary.joketop.com` | `frontend-portal/diary.html` | 静态 HTML |
| **诗词** | (内部 API) | `backend-poems/` | Python FastAPI (端口 8080) |
| **文档** | `blog.joketop.com/*` | `frontend-docs/` | 静态 HTML (Alias) |

## 🛠️ 快速开始

### 1. 启动前端主站预览

```bash
cd frontend-portal
./scripts/preview.sh
# 访问 http://localhost:8000
```

### 2. 启动诗词后端服务

```bash
cd backend-poems
pip install -r requirements.txt
python main.py
# 服务运行在 http://localhost:8080
```

### 3. 部署生产环境

```bash
# 执行统一部署脚本
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

- **DEPLOY-README.md** - 部署脚本使用说明
- **NGINX-CONFIG-README.md** - Nginx 配置详解

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

1. 在 `joketop.conf` 中添加 location 块
2. 在 `deploy-all-docs.sh` 的 SERVICES 数组中添加条目
3. 重新部署

详见 `DEPLOY-README.md`。
