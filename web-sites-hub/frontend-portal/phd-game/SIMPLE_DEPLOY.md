# 🚀 超简单部署教程 - game.joketop.com.cn

## 📋 部署前准备

### 1. 本地构建项目
```bash
# 在本地项目目录执行
npm run build
```

### 2. 上传项目到服务器
```bash
# 将 dist 文件夹内容上传到服务器
scp -r dist/* user@your-server:/var/www/phd-game/
```

## 🎯 一键部署 (推荐)

### 运行部署脚本
```bash
# 1. 上传脚本到服务器
scp simple-deploy.sh user@your-server:~/

# 2. 在服务器上运行
chmod +x simple-deploy.sh
./simple-deploy.sh
```

**就这么简单！脚本会自动：**
- ✅ 创建网站目录
- ✅ 安装/配置Nginx
- ✅ 设置域名 game.joketop.com.cn
- ✅ 配置防火墙
- ✅ 检查域名解析

## 🔧 手动部署 (可选)

### 1. 创建网站目录
```bash
sudo mkdir -p /var/www/phd-game
sudo chown $USER:$USER /var/www/phd-game
```

### 2. 创建Nginx配置
```bash
sudo nano /etc/nginx/sites-available/phd-game
```

复制以下内容：
```nginx
server {
    listen 80;
    server_name game.joketop.com.cn;
    
    root /var/www/phd-game;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|ttf|woff|woff2|yaml)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 3. 启用站点
```bash
sudo ln -s /etc/nginx/sites-available/phd-game /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🌐 域名配置

### 确保域名解析
在DNS管理面板中添加记录：
```
类型: A
名称: game
值: 你的服务器IP
TTL: 300
```

### 测试域名解析
```bash
# 在服务器上测试
dig +short game.joketop.com.cn

# 或在本地测试
nslookup game.joketop.com.cn
```

## 📁 文件结构

部署完成后，服务器上的文件结构应该是：
```
/var/www/phd-game/
├── index.html
├── app.bundle.js
├── css/
├── images/
└── rulesets/
```

## 🔒 可选：配置HTTPS

### 使用Let's Encrypt免费证书
```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d game.joketop.com.cn

# 自动续期
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

## 📊 管理命令

### 查看服务状态
```bash
sudo systemctl status nginx
sudo nginx -t
```

### 重启服务
```bash
sudo systemctl restart nginx
```

### 查看日志
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 查看访问统计
```bash
sudo tail -f /var/log/nginx/access.log | grep game.joketop.com.cn
```

## 🚨 故障排除

### 常见问题

#### 1. 域名无法访问
- 检查域名解析是否正确
- 检查防火墙是否开放80端口
- 检查Nginx是否正常运行

#### 2. 页面显示404
- 检查文件是否上传到正确目录
- 检查Nginx配置文件路径
- 检查文件权限

#### 3. 静态资源加载失败
- 检查文件路径是否正确
- 检查Nginx配置中的try_files设置

### 调试命令
```bash
# 检查Nginx配置
sudo nginx -t

# 检查端口占用
sudo netstat -tlnp | grep :80

# 检查文件权限
ls -la /var/www/phd-game/

# 检查Nginx进程
ps aux | grep nginx
```

## 🎉 完成！

部署完成后，访问 `http://game.joketop.com.cn` 就能看到你的PhD Simulator游戏了！

### 特色功能
- 🎮 默认中文界面
- 🌍 支持中英文切换
- 🎉 隐藏彩蛋：连续划水10次直接毕业
- 📱 响应式设计，支持移动设备

---
