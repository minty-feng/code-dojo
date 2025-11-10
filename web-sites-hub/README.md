# Sphinx 文档统一部署

## 📁 目录结构

```
sphinx-docs/
├── joketop.conf                    # Nginx 配置文件（239行）
├── joketop-letsencrypt-temp.conf  # Let's Encrypt 临时配置（37行）
├── deploy-all-docs.sh              # 统一部署脚本（374行）
├── DEPLOY-README.md                # 部署说明
├── NGINX-CONFIG-README.md          # 配置说明
│
├── honey-backend-dojo-docs/        # Backend 文档
├── grape-frontend-dojo-docs/       # Frontend 文档
├── apple-ds-core-docs/             # 数据结构文档
├── banana-algo-core-docs/          # 算法文档
└── cookie-os-network-docs/         # 操作系统和网络文档
```

## 🚀 快速开始

### 1. 部署到服务器

```bash
# 上传文件到服务器
scp joketop.conf joketop-letsencrypt-temp.conf deploy-all-docs.sh user@server:~/sphinx-docs/

# SSH 到服务器
ssh user@server

# 部署（含 HTTPS）
cd ~/sphinx-docs
sudo ./deploy-all-docs.sh --letsencrypt --email your@email.com
```

### 2. 修改配置

```bash
# 直接编辑配置文件
vim joketop.conf

# 重新部署
sudo ./deploy-all-docs.sh --letsencrypt --email your@email.com
```

## 📋 访问地址

- **主站**: https://joketop.com
- **简历**: https://me.joketop.com
- **学习站点**: https://blog.joketop.com

**文档服务：**
- Backend: https://blog.joketop.com/backend
- Frontend: https://blog.joketop.com/frontend
- 数据结构: https://blog.joketop.com/ds
- 算法: https://blog.joketop.com/algo
- 操作系统和网络: https://blog.joketop.com/os

## 🔧 架构特点

### 配置与脚本分离

- ✅ `joketop.conf` - 独立的 Nginx 配置文件
- ✅ `deploy-all-docs.sh` - 只负责拷贝和部署
- ✅ 无 EOF heredoc，避免转义问题
- ✅ 易于维护和版本控制

### 关键优化

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
