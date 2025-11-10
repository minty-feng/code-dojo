# 配置冲突说明

## 潜在冲突

`blog.joketop.com` 域名在两个部署脚本中都有使用：

1. **deploy-all-docs.sh** (code-dojo/sphinx-docs/)
   - 用途：文档服务（Sphinx 文档）
   - 路径：`/backend`, `/frontend`, `/ds`, `/algo`, `/os`
   - 配置文件：`/etc/nginx/sites-available/docs-code-dojo`

2. **deploy-joketop.sh** (当前项目)
   - 用途：学习站点导航页面
   - 文件：`learning.html`
   - 配置文件：`/etc/nginx/sites-available/joketop.com`

## 解决方案

### 方案一：使用不同的子域名（推荐）

将学习站点导航改为使用其他子域名，例如：
- `learn.joketop.com` - 学习站点导航
- `blog.joketop.com` - 文档服务（保持不变）

**修改步骤：**
1. 修改 `nginx.conf` 中的 `blog.joketop.com` 为 `learn.joketop.com`
2. 修改 `index.html` 中的链接
3. 更新 DNS 配置

### 方案二：合并配置

将两个配置合并到一个 Nginx 配置文件中，使用不同的 location 路径：
- `blog.joketop.com/` - 学习站点导航（根路径）
- `blog.joketop.com/backend/` - 后端文档
- `blog.joketop.com/frontend/` - 前端文档
- 等等...

### 方案三：路径区分

保持 `blog.joketop.com` 用于文档服务，学习站点导航使用：
- `blog.joketop.com/learn/` - 学习站点导航

## 当前状态

- `deploy-joketop.sh` 已添加冲突检测
- 部署时会检查是否存在 `docs-code-dojo` 配置
- 如果检测到冲突，会提示用户

## 建议

**推荐使用方案一**，将学习站点导航改为 `learn.joketop.com`，避免与文档服务冲突。

