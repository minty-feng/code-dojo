# joketop.com 站点结构（使用子域名）

## 域名配置

### 所有子域名
- **joketop.com** - 主站导航页 (`index.html`)
- **me.joketop.com** - 个人简历 (`resume.html`)
- **blog.joketop.com** - 学习站点导航 (`learning.html`) + 文档服务
- **showcase.joketop.com** - 项目展示 (`showcase.html`) ✨
- **diary.joketop.com** - 生活日记 (`diary.html`) ✨

### 文档服务子路径（blog.joketop.com）

- `/backend` - 后端开发教程
- `/frontend` - 前端开发教程
- `/ds` - 数据结构教程
- `/algo` - 算法教程
- `/os` - 操作系统与网络教程

## 文件清单

```
/var/www/html/joketop/
├── index.html          # 主站导航
├── resume.html         # 个人简历
├── learning.html       # 学习站点导航
├── showcase.html       # 项目展示 ✨
├── diary.html          # 生活日记 ✨
├── fund.html           # 基金估值助手
├── wufu.html           # 百福迎春生成器
├── speed.html          # 全球网速测试
└── assets/
    ├── favicon.svg     # 网站图标
    ├── css/
    │   ├── main.css
    │   ├── resume.css
    │   ├── learning.css
    │   ├── showcase.css  ✨
    │   └── diary.css     ✨
    └── js/
        ├── main.js
        ├── resume.js
        ├── showcase.js   ✨
        └── diary.js      ✨
```

## Nginx 配置

配置文件：`/etc/nginx/sites-available/joketop.conf`

每个子域名都有独立的 server 块：
- **joketop.com** - 使用 `index.html`
- **me.joketop.com** - 使用 `resume.html`
- **blog.joketop.com** - 使用 `learning.html` + 文档服务
- **showcase.joketop.com** - 使用 `showcase.html` ✨
- **diary.joketop.com** - 使用 `diary.html` ✨

## DNS 配置

需要在域名服务商配置以下 DNS 记录：

| 子域名 | 类型 | 值 |
|--------|------|-----|
| joketop.com | A | 服务器 IP |
| www.joketop.com | A 或 CNAME | 服务器 IP 或 joketop.com |
| me.joketop.com | A | 服务器 IP |
| blog.joketop.com | A | 服务器 IP |
| showcase.joketop.com | A | 服务器 IP |
| diary.joketop.com | A | 服务器 IP |

## SSL 证书

使用 Let's Encrypt 一次性获取所有子域名的证书：

```bash
sudo certbot certonly --nginx --expand \
  -d joketop.com \
  -d www.joketop.com \
  -d me.joketop.com \
  -d blog.joketop.com \
  -d showcase.joketop.com \
  -d diary.joketop.com
```

## 部署流程

```bash
# 1. 本地打包
cd /Users/didi/Workspace/code-dojo/web-sites-hub/frontend-portal
./package-joketop.sh

# 2. 上传到服务器
scp joketop-*.tar.gz user@server:~

# 3. 在服务器上部署文件
sudo ./deploy-joketop.sh joketop-*.tar.gz

# 4. 配置 DNS 记录（在域名服务商后台）
# 为所有子域名添加 A 记录指向服务器 IP

# 5. 配置 Nginx 和 SSL（使用统一脚本）
cd /path/to/code-dojo/web-sites-hub/
sudo ./deploy-all-docs.sh --letsencrypt --email riseat7am@gmail.com

# 6. 验证访问
# https://joketop.com
# https://me.joketop.com
# https://blog.joketop.com
# https://showcase.joketop.com
# https://diary.joketop.com
```

## 站点功能

| 子域名 | 页面 | 功能特色 |
|--------|------|---------|
| joketop.com | 主站导航 | 所有站点的入口，炫酷动画背景 |
| me.joketop.com | 个人简历 | 完整履历展示，支持 PDF 下载 |
| blog.joketop.com | 学习站点 | 技术学习资源导航 + 5个文档服务 |
| showcase.joketop.com | 项目展示 | 精选项目、项目分类过滤 |
| diary.joketop.com | 生活日记 | 时间线设计、心情标签、照片展示 |
