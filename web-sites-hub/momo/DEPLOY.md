# 部署指南

## 服务器部署方案

### 1. 文件结构

将以下文件上传到服务器：

```
/var/www/joketop.com/
├── index.html          # 主站导航页
├── resume.html         # 简历页面（me.joketop.com）
├── learning.html       # 博客/学习站点页面（blog.joketop.com）
├── assets/
│   ├── css/
│   │   ├── main.css
│   │   ├── resume.css
│   │   └── learning.css
│   └── js/
│       ├── main.js
│       └── resume.js
└── README.md
```

### 2. Nginx 配置

创建 `/etc/nginx/sites-available/joketop.com`：

```nginx
# 主站 - joketop.com
server {
    listen 80;
    server_name joketop.com www.joketop.com;
    root /var/www/joketop.com;
    index index.html;

    # 日志
    access_log /var/log/nginx/joketop.com.access.log;
    error_log /var/log/nginx/joketop.com.error.log;

    location / {
        try_files $uri $uri/ =404;
    }

    # 静态资源缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}

# 简历子域名 - me.joketop.com
server {
    listen 80;
    server_name me.joketop.com;
    root /var/www/joketop.com;
    index resume.html;

    access_log /var/log/nginx/me.joketop.com.access.log;
    error_log /var/log/nginx/me.joketop.com.error.log;

    location / {
        try_files $uri $uri/ /resume.html;
    }

    # 静态资源缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
```

### 3. 部署步骤

#### 步骤 1：创建目录并设置权限

```bash
# 创建目录
sudo mkdir -p /var/www/joketop.com
sudo chown -R $USER:$USER /var/www/joketop.com

# 设置权限
sudo chmod -R 755 /var/www/joketop.com
```

#### 步骤 2：上传文件

**方式一：使用 scp**
```bash
# 在本地项目目录执行
scp -r * user@your-server-ip:/var/www/joketop.com/
```

**方式二：使用 rsync（推荐）**
```bash
# 在本地项目目录执行
rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '.DS_Store' \
    ./ user@your-server-ip:/var/www/joketop.com/
```

**方式三：使用 Git**
```bash
# 在服务器上
cd /var/www/joketop.com
git clone https://github.com/your-username/your-repo.git .
```

#### 步骤 3：配置 Nginx

```bash
# 复制配置文件
sudo cp /path/to/joketop.com.conf /etc/nginx/sites-available/joketop.com

# 创建符号链接
sudo ln -s /etc/nginx/sites-available/joketop.com /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl reload nginx
```

#### 步骤 4：配置 SSL（Let's Encrypt）

```bash
# 安装 certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx

# 为主站配置 SSL
sudo certbot --nginx -d joketop.com -d www.joketop.com

# 为简历子域名配置 SSL
sudo certbot --nginx -d me.joketop.com

# 为博客子域名配置 SSL
sudo certbot --nginx -d blog.joketop.com

# 自动续期测试
sudo certbot renew --dry-run
```

### 4. DNS 配置

在域名管理后台添加以下 DNS 记录：

```
类型    名称    值（IP地址或CNAME）
A       @       你的服务器IP
A       www     你的服务器IP
A       me      你的服务器IP
A       blog    你的服务器IP
```

或者使用 CNAME：

```
类型    名称    值
A       @       你的服务器IP
CNAME   www     joketop.com
CNAME   me      joketop.com
CNAME   blog    joketop.com
```

### 5. 自动化部署脚本

创建 `deploy.sh`：

```bash
#!/bin/bash

# 配置
SERVER_USER="your-username"
SERVER_HOST="your-server-ip"
SERVER_PATH="/var/www/joketop.com"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始部署...${NC}"

# 同步文件
echo -e "${GREEN}同步文件到服务器...${NC}"
rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '.DS_Store' \
    --exclude '*.md' \
    ./ $SERVER_USER@$SERVER_HOST:$SERVER_PATH/

# 检查同步是否成功
if [ $? -eq 0 ]; then
    echo -e "${GREEN}文件同步成功！${NC}"
    
    # 在服务器上执行命令
    echo -e "${GREEN}设置文件权限...${NC}"
    ssh $SERVER_USER@$SERVER_HOST "sudo chown -R www-data:www-data $SERVER_PATH && sudo chmod -R 755 $SERVER_PATH"
    
    echo -e "${GREEN}部署完成！${NC}"
else
    echo -e "${RED}部署失败！${NC}"
    exit 1
fi
```

使用方式：
```bash
chmod +x deploy.sh
./deploy.sh
```

### 6. 使用 Docker 部署（可选）

创建 `Dockerfile`：

```dockerfile
FROM nginx:alpine

# 复制文件
COPY . /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    restart: unless-stopped
```

### 7. 验证部署

部署完成后，访问以下地址验证：

- 主站：https://joketop.com
- 简历：https://me.joketop.com
- 博客：https://blog.joketop.com

### 8. 常见问题

**问题 1：403 Forbidden**
```bash
# 检查文件权限
sudo chown -R www-data:www-data /var/www/joketop.com
sudo chmod -R 755 /var/www/joketop.com
```

**问题 2：502 Bad Gateway**
```bash
# 检查 Nginx 配置
sudo nginx -t
sudo systemctl status nginx
```

**问题 3：SSL 证书问题**
```bash
# 重新申请证书
sudo certbot --nginx -d joketop.com -d www.joketop.com -d me.joketop.com -d blog.joketop.com --force-renewal
```

### 9. 性能优化

**启用 HTTP/2**
在 Nginx 配置中添加：
```nginx
listen 443 ssl http2;
```

**启用 Brotli 压缩**
```bash
sudo apt install nginx-module-brotli
```

**CDN 配置**
考虑使用 Cloudflare 等 CDN 服务加速静态资源。

### 10. 监控和维护

**查看访问日志**
```bash
tail -f /var/log/nginx/joketop.com.access.log
```

**查看错误日志**
```bash
tail -f /var/log/nginx/joketop.com.error.log
```

**定期备份**
```bash
# 创建备份脚本
tar -czf backup-$(date +%Y%m%d).tar.gz /var/www/joketop.com
```

