# 🚀 PhD Simulator 后端启动指南

## 📋 概述

本文档详细介绍了 PhD Simulator 后端服务的三种启动方式，适用于不同的部署环境和需求场景。

## 🎯 启动方式概览

| 启动方式 | 适用场景 | 特点 | 复杂度 |
|----------|----------|------|--------|
| **开发启动** | 本地开发、功能测试 | 热重载、调试友好 | ⭐ |
| **systemd服务** | 生产环境、服务器部署 | 开机自启、进程监控 | ⭐⭐ |
| **gunicorn** | 高并发生产环境 | 多进程、负载均衡 | ⭐⭐⭐ |

---

## 🛠️ 方式1: 开发环境启动

### 📝 适用场景
- 本地开发和调试
- 功能测试和验证
- 小规模部署
- 需要热重载功能

### 🔧 启动步骤

#### 1. 进入后端目录
```bash
cd backend
```

#### 2. 激活虚拟环境
```bash
# 创建虚拟环境（如果不存在）
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 启动服务
```bash
python run.py
```

### 🌟 启动特点
- **热重载**: 代码修改后自动重启服务
- **详细日志**: 实时显示启动信息和状态
- **调试友好**: 支持断点和调试工具
- **单进程**: 适合开发和测试环境

### 📊 启动输出示例
```
🚀 启动 PhD Simulator 后端服务...
📖 API文档: http://localhost:8000/docs
🎮 游戏地址: http://localhost:8000
💾 数据库: phd_game.db
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 🔍 访问地址
- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **游戏页面**: http://localhost:8000

### ⚠️ 注意事项
- 仅适用于开发和测试环境
- 不支持开机自启
- 进程崩溃后需要手动重启
- 不适合生产环境使用

---

## 🚀 方式2: systemd 服务启动

### 📝 适用场景
- 生产环境部署
- 服务器长期运行
- 需要开机自启
- 进程监控和管理

### 🔧 部署步骤

#### 1. 创建 systemd 服务文件
```bash
sudo nano /etc/systemd/system/phd-game-backend.service
```

#### 2. 服务配置内容
```ini
[Unit]
Description=PhD Simulator Backend Service
Documentation=https://github.com/your-repo/phd-game
After=network.target
Wants=network.target

[Service]
Type=simple
User=your-username
Group=your-username
WorkingDirectory=/home/your-username/backend
Environment=PATH=/home/your-username/backend/venv/bin
Environment=PYTHONPATH=/home/your-username/backend
ExecStart=/home/your-username/backend/venv/bin/python run.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
SyslogIdentifier=phd-game-backend

# 安全设置
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/your-username/backend

[Install]
WantedBy=multi-user.target
```

#### 3. 启动和管理服务
```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start phd-game-backend

# 设置开机自启
sudo systemctl enable phd-game-backend

# 查看服务状态
sudo systemctl status phd-game-backend

# 重启服务
sudo systemctl restart phd-game-backend

# 停止服务
sudo systemctl stop phd-game-backend

# 重新加载服务配置
sudo systemctl reload phd-game-backend
```

#### 4. 查看服务日志
```bash
# 查看实时日志
sudo journalctl -u phd-game-backend -f

# 查看最近的日志
sudo journalctl -u phd-game-backend -n 100

# 查看特定时间的日志
sudo journalctl -u phd-game-backend --since "2024-01-01 00:00:00"

# 查看错误日志
sudo journalctl -u phd-game-backend -p err
```

### 🌟 启动特点
- **开机自启**: 服务器重启后自动启动服务
- **进程监控**: systemd 自动监控进程状态
- **自动重启**: 进程崩溃后自动重启
- **日志管理**: 通过 journalctl 查看系统日志
- **服务管理**: 标准的 Linux 服务管理方式

### 🔍 服务状态检查
```bash
# 检查服务状态
sudo systemctl status phd-game-backend

# 检查端口是否监听
sudo netstat -tlnp | grep :8000
# 或者使用 ss 命令
sudo ss -tlnp | grep :8000

# 检查进程
ps aux | grep "python run.py"
```

### ⚠️ 注意事项
- 需要 root 权限创建服务文件
- 确保用户权限和路径配置正确
- 虚拟环境路径必须绝对路径
- 建议配置日志轮转和监控

---

## 🚀 方式3: gunicorn 高性能启动

### 📝 适用场景
- 高并发生产环境
- 需要负载均衡
- 性能要求高
- 大规模部署

### 🔧 部署步骤

#### 1. 安装 gunicorn
```bash
cd backend
source venv/bin/activate
pip install gunicorn
```

#### 2. 创建 gunicorn 配置文件
```bash
nano gunicorn.conf.py
```

配置文件内容：
```python
# gunicorn.conf.py
import multiprocessing

# 服务器配置
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1  # 推荐配置
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# 进程配置
preload_app = True
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None

# 日志配置
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 超时配置
timeout = 30
keepalive = 2
graceful_timeout = 30

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
```

#### 3. 启动服务
```bash
# 使用配置文件启动
gunicorn -c gunicorn.conf.py main:app

# 或者直接命令行启动
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 30
```

#### 4. 创建 systemd 服务（推荐）
```ini
[Unit]
Description=PhD Simulator Backend (Gunicorn)
After=network.target

[Service]
Type=notify
User=your-username
Group=your-username
WorkingDirectory=/home/your-username/backend
Environment=PATH=/home/your-username/backend/venv/bin
ExecStart=/home/your-username/backend/venv/bin/gunicorn -c gunicorn.conf.py main:app
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 🌟 启动特点
- **多进程**: 支持多个工作进程
- **负载均衡**: 自动分发请求到不同进程
- **高性能**: 适合高并发场景
- **进程管理**: 主进程监控工作进程
- **配置灵活**: 支持详细的配置选项

### 📊 性能调优参数
```bash
# 工作进程数 (推荐: CPU核心数 * 2 + 1)
-w 4

# 工作进程类型
-k uvicorn.workers.UvicornWorker

# 绑定地址和端口
--bind 0.0.0.0:8000

# 超时设置
--timeout 30

# 最大请求数
--max-requests 1000

# 预加载应用
--preload
```

### 🔍 监控和调试
```bash
# 查看进程状态
ps aux | grep gunicorn

# 查看端口监听
netstat -tlnp | grep :8000

# 查看 gunicorn 状态
curl http://localhost:8000/health

# 查看工作进程
gunicorn --version
```

---

## 🔧 环境配置

### 📁 目录结构
```
backend/
├── main.py              # FastAPI 应用主文件
├── run.py               # 开发启动脚本
├── gunicorn.conf.py     # gunicorn 配置文件
├── requirements.txt     # Python 依赖
├── phd_game.db         # SQLite 数据库
└── STARTUP_GUIDE.md    # 本文档
```

### 🌍 环境变量
```bash
# 数据库配置
export DATABASE_URL="sqlite:///./phd_game.db"

# 服务配置
export HOST="0.0.0.0"
export PORT="8000"

# 日志级别
export LOG_LEVEL="info"

# 开发模式
export DEBUG="true"
```

### 📝 配置文件示例
```python
# config.py
import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./phd_game.db")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

---

## 🚨 故障排除

### ❌ 常见问题

#### 1. 端口被占用
```bash
# 检查端口占用
sudo netstat -tlnp | grep :8000

# 杀死占用进程
sudo kill -9 <PID>

# 或者使用不同端口
python run.py --port 8001
```

#### 2. 权限问题
```bash
# 检查文件权限
ls -la backend/

# 修复权限
chmod +x backend/run.py
chown -R your-username:your-username backend/
```

#### 3. 虚拟环境问题
```bash
# 重新创建虚拟环境
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. 数据库问题
```bash
# 检查数据库文件
ls -la phd_game.db

# 重新创建数据库
rm phd_game.db
python -c "from models.database import create_tables; create_tables()"
```

### 🔍 日志分析
```bash
# 查看应用日志
tail -f backend/app.log

# 查看系统日志
sudo journalctl -u phd-game-backend -f

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/error.log
```

---

## 📊 性能监控

### 📈 监控指标
- **响应时间**: API 请求响应时间
- **并发数**: 同时处理的请求数
- **错误率**: 请求失败的比例
- **资源使用**: CPU、内存、磁盘使用情况

### 🛠️ 监控工具
```bash
# 系统资源监控
htop
iotop
nethogs

# 网络连接监控
netstat -an | grep :8000
ss -s

# 进程监控
ps aux | grep python
```

---

## 💡 最佳实践

### 🚀 开发环境
- 使用 `python run.py` 启动
- 启用热重载功能
- 设置详细的日志级别
- 使用 SQLite 数据库

### 🏭 生产环境
- 使用 systemd 管理服务
- 配置日志轮转
- 设置监控和告警
- 使用 gunicorn 多进程

### 🔒 安全配置
- 限制 CORS 域名
- 配置防火墙规则
- 使用 HTTPS
- 定期更新依赖

---

## 🎉 总结

本文档详细介绍了三种后端启动方式：

1. **开发启动**: 简单直接，适合开发和测试
2. **systemd 服务**: 稳定可靠，适合生产环境
3. **gunicorn**: 高性能，适合高并发场景

根据实际需求选择合适的启动方式，确保服务的稳定性和性能。

---

## 📚 相关文档

- [部署指南](../DEPLOYMENT_GUIDE.md)
- [API 文档](http://localhost:8000/docs)
- [后端 README](README.md)
- [快速部署脚本](../quick-deploy.sh)

---

