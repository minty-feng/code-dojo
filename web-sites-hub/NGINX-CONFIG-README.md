# Nginx 配置管理说明

## 📁 文件说明

### 1. `joketop.conf` - Nginx 正式配置文件
这是生产环境使用的完整 Nginx 配置文件，包含了所有域名和服务的 HTTPS 配置：
- `joketop.com` - 主站
- `me.joketop.com` - 简历页面
- `blog.joketop.com` - 学习站点（包含所有文档服务）

**特点：**
- 完整的 HTTPS 配置（包括 HTTP 到 HTTPS 的重定向）
- 所有服务路由都已配置好
- SSL 证书路径固定指向 `/etc/letsencrypt/live/`

### 2. `joketop-letsencrypt-temp.conf` - Let's Encrypt 临时配置
这是获取 SSL 证书时使用的临时 HTTP 配置文件：
- 只包含 `.well-known/acme-challenge/` location
- 用于 Let's Encrypt 域名验证
- 证书获取成功后会被 `joketop.conf` 替换

### 3. `deploy-joketop-nginx.sh` - 部署脚本
完全简化的部署脚本，**不包含任何配置生成代码**：
- 检查服务目录
- Let's Encrypt 证书管理
- 拷贝 Nginx 配置文件到正确位置
- 重启 Nginx 服务

**简化效果：**
- 旧版本：1069 行（包含大量 EOF 和配置生成代码）
- 新版本：374 行（**减少 65%，完全不使用 EOF**）

## 🔧 修改配置

### 方法1: 直接修改配置文件（推荐）

```bash
# 编辑配置文件
vim web-sites-hub/joketop.conf

# 测试配置
sudo nginx -t

# 应用配置
sudo ./deploy-joketop-nginx.sh
```

### 方法2: 修改后手动拷贝

```bash
# 编辑配置
vim web-sites-hub/joketop.conf

# 手动拷贝到 Nginx 目录
sudo cp joketop.conf /etc/nginx/sites-available/joketop.conf
sudo ln -sf /etc/nginx/sites-available/joketop.conf /etc/nginx/sites-enabled/joketop.conf

# 测试并重启
sudo nginx -t
sudo systemctl reload nginx
```

## 📝 添加新的服务路由

在 `joketop.conf` 的 `blog.joketop.com` server 块中添加新的 location：

```nginx
# 新服务
location /newservice/ {
    alias /var/www/html/newservice/;
    index index.html;
    try_files $uri $uri/ $uri/index.html =404;

    location ~ /\.(git|htaccess|env|DS_Store) {
        deny all;
        access_log off;
        log_not_found off;
    }
}

location = /newservice {
    return 301 $scheme://$server_name/newservice/;
}
```

然后运行 `sudo ./deploy-joketop-nginx.sh` 应用配置。

## 🔐 证书管理

脚本会自动处理 Let's Encrypt 证书：

```bash
# 获取证书并部署
sudo ./deploy-joketop-nginx.sh --letsencrypt --email riseat7am@gmail.com
```

## 📊 配置文件结构

```
joketop.conf
├── joketop.com (HTTP → HTTPS 重定向)
├── joketop.com (HTTPS)
├── me.joketop.com (HTTP → HTTPS 重定向)
├── me.joketop.com (HTTPS)
├── blog.joketop.com (HTTP → HTTPS 重定向)
└── blog.joketop.com (HTTPS)
    ├── / (learning.html)
    ├── /backend/
    ├── /frontend/
    ├── /ds/
    ├── /algo/
    └── /os/
```

## ⚠️  注意事项

1. 修改 `joketop.conf` 后，需要运行 `deploy-joketop-nginx.sh` 或手动拷贝到 `/etc/nginx/sites-available/`
2. 证书路径已经在配置文件中固定，如果证书位置变化需要修改配置文件
3. 所有服务路由都在 `blog.joketop.com` 的 server 块内
4. 配置文件使用 HTTPS 配置，如果证书不存在，Nginx 将无法启动

## 🚀 快速部署流程

```bash
# 1. 修改配置（如果需要）
vim web-sites-hub/joketop.conf

# 2. 部署（包含证书管理）
cd web-sites-hub
sudo ./deploy-joketop-nginx.sh --letsencrypt --email riseat7am@gmail.com

# 3. 验证
curl -I https://blog.joketop.com
```

