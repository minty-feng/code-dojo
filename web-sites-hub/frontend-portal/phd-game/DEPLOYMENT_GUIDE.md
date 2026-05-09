# 🚀 PhD Simulator 完整部署指南

## 📋 部署方案对比

### 方案1: 单服务器部署 (推荐新手)
```
前端 + 后端 + 数据库 都在同一台服务器
```

### 方案2: 分离部署 (推荐生产)
```
前端: Nginx静态文件
后端: Python FastAPI服务器
数据库: 独立数据库服务器
```

## 🎯 方案1: 单服务器部署

### 服务器要求
- **系统**: Ubuntu 20.04+ / CentOS 7+
- **内存**: 2GB+
- **存储**: 20GB+
- **网络**: 公网IP

### 部署步骤

#### 1. 准备项目文件
```bash
# 在本地构建项目
npm run build

# 上传到服务器
scp -r dist/* user@your-server:/var/www/phd-game/
scp -r backend user@your-server:~/
```

#### 2. 在服务器上安装依赖
```bash
# 更新系统
sudo apt update  # Ubuntu
# sudo yum update  # CentOS

# 安装Python和依赖
sudo apt install python3 python3-pip python3-venv nginx
# sudo yum install python3 python3-pip nginx  # CentOS

# 创建虚拟环境
cd ~/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. 配置Nginx
```bash
sudo nano /etc/nginx/sites-available/phd-game
```

```nginx
server {
    listen 80;
    server_name game.joketop.com.cn;
    
    # 前端静态文件
    location / {
        root /var/www/phd-game;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|ttf|woff|woff2|yaml)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### 4. 启用Nginx配置
```bash
sudo ln -s /etc/nginx/sites-available/phd-game /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

#### 5. 启动后端服务
```bash
# 创建systemd服务
sudo nano /etc/systemd/system/phd-game-backend.service
```

```ini
[Unit]
Description=PhD Simulator Backend
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/backend
Environment=PATH=/home/your-username/backend/venv/bin
ExecStart=/home/your-username/backend/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl daemon-reload
sudo systemctl start phd-game-backend
sudo systemctl enable phd-game-backend

# 检查状态
sudo systemctl status phd-game-backend
```

#### 6. 配置防火墙
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 🌐 方案2: 分离部署

### 前端服务器 (Nginx)
```bash
# 只部署前端文件
scp -r dist/* user@frontend-server:/var/www/phd-game/

# Nginx配置
server {
    listen 80;
    server_name game.joketop.com.cn;
    
    root /var/www/phd-game;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 后端服务器 (Python)
```bash
# 部署后端代码
scp -r backend user@backend-server:~/

# 安装依赖
cd ~/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 启动服务
python run.py
```

### 前端配置
修改 `static/index.html` 中的 `apiBaseUrl`:
```json
{
    "apiBaseUrl": "http://backend-server-ip:8000"
}
```

## 🔧 配置说明

### 前端配置
```json
{
    "apiBaseUrl": ""  // 空字符串表示同域名
}
```

### 后端配置
```python
# backend/main.py
app = FastAPI(
    title="PhD Simulator Backend",
    description="记录玩家游戏数据的后端API",
    version="1.0.0"
)

# 配置CORS (跨域)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 数据记录流程

### 1. 游戏开始时
```javascript
// 自动调用
await gameApi.startGame();
// 记录: 玩家ID、设备信息、IP地址、时间等
```

### 2. 游戏结束时
```javascript
// 自动调用
await gameApi.endGame({
    final_hope: 75,
    final_papers: 3,
    graduation_status: "毕业",
    is_winner: true,
    slack_off_count: 5,
    // ... 其他数据
});
```

### 3. 数据存储
- **数据库**: SQLite (可升级到MySQL/PostgreSQL)
- **文件**: `backend/phd_game.db`
- **备份**: 建议定期备份数据库文件

## 🚨 生产环境注意事项

### 安全配置
```python
# 限制CORS域名
allow_origins=["https://game.joketop.com.cn"]

# 添加API认证
# 使用JWT或API Key
```

### 性能优化
```bash
# 使用gunicorn启动
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 数据库优化
# 添加索引、连接池等
```

### 监控和日志
```bash
# 查看后端日志
sudo journalctl -u phd-game-backend -f

# 查看Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🔍 故障排除

### 常见问题

#### 1. 前端无法访问后端API
```bash
# 检查后端服务状态
sudo systemctl status phd-game-backend

# 检查端口是否开放
sudo netstat -tlnp | grep :8000

# 检查防火墙
sudo ufw status
```

#### 2. 数据库连接失败
```bash
# 检查数据库文件权限
ls -la ~/backend/phd_game.db

# 重新创建数据库
rm ~/backend/phd_game.db
# 重启后端服务
```

#### 3. Nginx配置错误
```bash
# 检查配置语法
sudo nginx -t

# 查看错误日志
sudo tail -f /var/log/nginx/error.log
```

## 🎉 部署完成

### 访问地址
- 🎮 **游戏**: http://game.joketop.com.cn
- 📖 **API文档**: http://game.joketop.com.cn/docs
- 🔍 **健康检查**: http://game.joketop.com.cn/health

### 功能验证
1. 访问游戏页面
2. 开始一局游戏
3. 查看后端日志确认数据记录
4. 访问API文档测试接口

### 数据查看
```bash
# 查看数据库内容
cd ~/backend
sqlite3 phd_game.db
.tables
SELECT * FROM player_games LIMIT 5;
.quit
```

