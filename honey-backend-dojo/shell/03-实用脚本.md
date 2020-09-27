# 03-Shell实用脚本

Shell脚本在运维自动化、日志分析、批量处理等场景中不可或缺。掌握常用脚本模式可快速解决实际问题。

## 系统管理脚本

### 系统监控

```bash
#!/bin/bash
# 系统资源监控

echo "=== CPU使用率 ==="
top -bn1 | grep "Cpu(s)" | awk '{print "CPU使用:", 100-$8"%"}'

echo ""
echo "=== 内存使用 ==="
free -h | awk 'NR==2{printf "使用: %s/%s (%.2f%%)\n", $3, $2, $3*100/$2}'

echo ""
echo "=== 磁盘使用 ==="
df -h | awk '$NF=="/"{printf "使用: %s/%s (%s)\n", $3, $2, $5}'

echo ""
echo "=== Top 5进程（CPU） ==="
ps aux | sort -rn -k3 | head -6 | awk 'NR>1{printf "%-10s %5s%% %s\n", $1, $3, $11}'

echo ""
echo "=== Top 5进程（内存） ==="
ps aux | sort -rn -k4 | head -6 | awk 'NR>1{printf "%-10s %5s%% %s\n", $1, $4, $11}'
```

### 服务监控和自动重启

```bash
#!/bin/bash
# 监控服务，挂了就重启

SERVICE="nginx"
RESTART_CMD="systemctl start nginx"
LOG_FILE="/var/log/service_monitor.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

if ! systemctl is-active --quiet $SERVICE; then
    log "ERROR: $SERVICE is down, restarting..."
    $RESTART_CMD
    
    sleep 3
    
    if systemctl is-active --quiet $SERVICE; then
        log "SUCCESS: $SERVICE restarted"
    else
        log "FAILED: $SERVICE restart failed"
        # 发送告警
        echo "$SERVICE restart failed" | mail -s "Alert" admin@example.com
    fi
else
    log "OK: $SERVICE is running"
fi
```

### 磁盘空间告警

```bash
#!/bin/bash
# 磁盘使用率超过阈值告警

THRESHOLD=80
EMAIL="admin@example.com"

df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{print $5 " " $1}' | while read output; do
    usage=$(echo $output | awk '{print $1}' | sed 's/%//g')
    partition=$(echo $output | awk '{print $2}')
    
    if [ $usage -ge $THRESHOLD ]; then
        echo "WARNING: $partition 使用率 $usage%" | \
            mail -s "磁盘空间告警" $EMAIL
    fi
done
```

## 日志分析脚本

### Nginx访问日志分析

```bash
#!/bin/bash
# 分析Nginx访问日志

LOG_FILE="${1:-/var/log/nginx/access.log}"

if [ ! -f "$LOG_FILE" ]; then
    echo "日志文件不存在: $LOG_FILE"
    exit 1
fi

echo "====== Nginx日志分析 ======"
echo "日志文件: $LOG_FILE"
echo "日志行数: $(wc -l < $LOG_FILE)"
echo ""

# Top 10 IP
echo "=== Top 10 IP地址 ==="
awk '{print $1}' $LOG_FILE | sort | uniq -c | sort -rn | head -10 | \
    awk '{printf "%15s  %8d 次\n", $2, $1}'
echo ""

# Top 10 URL
echo "=== Top 10 访问URL ==="
awk '{print $7}' $LOG_FILE | sort | uniq -c | sort -rn | head -10 | \
    awk '{printf "%8d  %s\n", $1, $2}'
echo ""

# 状态码统计
echo "=== HTTP状态码统计 ==="
awk '{print $9}' $LOG_FILE | sort | uniq -c | sort -rn | \
    awk '{printf "%3s: %8d 次\n", $2, $1}'
echo ""

# 每小时流量
echo "=== 每小时请求数 ==="
awk '{print substr($4, 14, 2)}' $LOG_FILE | sort | uniq -c | \
    awk '{printf "%s时: %8d 次\n", $2, $1}'
echo ""

# 流量带宽（假设日志格式包含字节数）
echo "=== 总流量 ==="
total_bytes=$(awk '{sum += $10} END {print sum}' $LOG_FILE)
total_mb=$(echo "scale=2; $total_bytes/1024/1024" | bc)
echo "${total_mb} MB"
```

### 错误日志监控

```bash
#!/bin/bash
# 监控应用错误日志

LOG_FILE="/var/log/app/error.log"
LAST_CHECK="/tmp/last_error_check"
ALERT_EMAIL="admin@example.com"

# 记录上次检查时间
if [ -f "$LAST_CHECK" ]; then
    last_time=$(cat "$LAST_CHECK")
else
    last_time=$(date -d "1 hour ago" +%s)
fi

current_time=$(date +%s)
echo $current_time > "$LAST_CHECK"

# 提取时间范围内的错误
new_errors=$(awk -v start=$last_time -v end=$current_time '
    {
        # 解析日志时间戳（格式需调整）
        if ($0 ~ /ERROR|FATAL/) print
    }
' $LOG_FILE)

if [ -n "$new_errors" ]; then
    error_count=$(echo "$new_errors" | wc -l)
    
    {
        echo "发现 $error_count 条新错误:"
        echo ""
        echo "$new_errors"
    } | mail -s "应用错误告警" $ALERT_EMAIL
fi
```

## 备份脚本

### MySQL备份

```bash
#!/bin/bash
# MySQL数据库备份

DB_USER="backup_user"
DB_PASS="password"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# 创建备份目录
mkdir -p $BACKUP_DIR

# 获取所有数据库
databases=$(mysql -u$DB_USER -p$DB_PASS -e "SHOW DATABASES;" | grep -Ev "(Database|information_schema|performance_schema|mysql)")

# 备份每个数据库
for db in $databases; do
    echo "备份数据库: $db"
    mysqldump -u$DB_USER -p$DB_PASS \
        --single-transaction \
        --routines \
        --triggers \
        $db | gzip > $BACKUP_DIR/${db}_${DATE}.sql.gz
    
    if [ $? -eq 0 ]; then
        echo "✓ $db 备份成功"
    else
        echo "✗ $db 备份失败"
    fi
done

# 删除旧备份
echo "清理 $RETENTION_DAYS 天前的备份..."
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "备份完成: $(date)"
```

### 文件同步备份

```bash
#!/bin/bash
# 使用rsync同步备份

SOURCE="/var/www/html"
DEST="/backup/www"
REMOTE_HOST="backup-server"
REMOTE_USER="backup"
LOG_FILE="/var/log/backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "开始备份..."

# 本地备份
rsync -avz --delete \
    --exclude='*.log' \
    --exclude='cache/' \
    $SOURCE/ $DEST/

if [ $? -eq 0 ]; then
    log "本地备份成功"
else
    log "本地备份失败"
    exit 1
fi

# 远程备份
rsync -avz --delete \
    -e "ssh -p 22" \
    $SOURCE/ ${REMOTE_USER}@${REMOTE_HOST}:/backup/www/

if [ $? -eq 0 ]; then
    log "远程备份成功"
else
    log "远程备份失败"
    exit 1
fi

log "备份完成"
```

## 批量处理脚本

### 批量重命名

```bash
#!/bin/bash
# 批量重命名文件

# 示例：将所有.txt改为.bak
for file in *.txt; do
    mv "$file" "${file%.txt}.bak"
done

# 添加前缀
for file in *; do
    mv "$file" "prefix_$file"
done

# 替换字符
for file in *; do
    newname=$(echo "$file" | sed 's/old/new/g')
    mv "$file" "$newname"
done

# 按日期重命名图片
counter=1
for file in *.jpg; do
    date=$(stat -c %y "$file" | cut -d' ' -f1)
    mv "$file" "${date}_$(printf %03d $counter).jpg"
    ((counter++))
done
```

### 批量转换格式

```bash
#!/bin/bash
# 批量转换图片格式

if ! command -v convert &> /dev/null; then
    echo "需要安装ImageMagick: apt install imagemagick"
    exit 1
fi

# PNG转JPG
for file in *.png; do
    convert "$file" "${file%.png}.jpg"
    echo "转换: $file → ${file%.png}.jpg"
done

# 调整大小
for file in *.jpg; do
    convert "$file" -resize 800x600 "resized_$file"
done

# 批量压缩
for file in *.jpg; do
    convert "$file" -quality 80 "compressed_$file"
done
```

### 批量下载

```bash
#!/bin/bash
# 批量下载文件

URLS_FILE="urls.txt"
DOWNLOAD_DIR="downloads"

mkdir -p $DOWNLOAD_DIR

while IFS= read -r url; do
    # 跳过空行和注释
    [[ -z "$url" || "$url" =~ ^# ]] && continue
    
    filename=$(basename "$url")
    echo "下载: $filename"
    
    wget -q -P $DOWNLOAD_DIR "$url"
    
    if [ $? -eq 0 ]; then
        echo "✓ $filename 下载成功"
    else
        echo "✗ $filename 下载失败"
    fi
    
    sleep 1  # 避免请求过快
done < "$URLS_FILE"
```

## 部署脚本

### 应用部署

```bash
#!/bin/bash
# 简单的应用部署脚本

set -euo pipefail

APP_NAME="myapp"
DEPLOY_DIR="/opt/$APP_NAME"
BACKUP_DIR="/backup/$APP_NAME"
GIT_REPO="https://github.com/user/myapp.git"
BRANCH="main"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# 备份当前版本
if [ -d "$DEPLOY_DIR" ]; then
    log "备份当前版本..."
    timestamp=$(date +%Y%m%d_%H%M%S)
    tar czf "$BACKUP_DIR/${APP_NAME}_${timestamp}.tar.gz" -C $(dirname $DEPLOY_DIR) $(basename $DEPLOY_DIR)
fi

# 拉取最新代码
if [ -d "$DEPLOY_DIR/.git" ]; then
    log "更新代码..."
    cd $DEPLOY_DIR
    git pull origin $BRANCH
else
    log "克隆代码..."
    git clone -b $BRANCH $GIT_REPO $DEPLOY_DIR
    cd $DEPLOY_DIR
fi

# 安装依赖
log "安装依赖..."
if [ -f "package.json" ]; then
    npm install --production
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 构建
log "构建应用..."
if [ -f "Makefile" ]; then
    make build
elif [ -f "package.json" ]; then
    npm run build
fi

# 重启服务
log "重启服务..."
systemctl restart $APP_NAME

# 健康检查
sleep 3
if systemctl is-active --quiet $APP_NAME; then
    log "✓ 部署成功"
else
    log "✗ 服务启动失败，回滚..."
    # 回滚逻辑
    exit 1
fi
```

### Docker部署

```bash
#!/bin/bash
# Docker容器部署

set -euo pipefail

IMAGE_NAME="myapp"
CONTAINER_NAME="myapp-container"
TAG="latest"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# 拉取最新镜像
log "拉取镜像: $IMAGE_NAME:$TAG"
docker pull $IMAGE_NAME:$TAG

# 停止旧容器
if docker ps -a | grep -q $CONTAINER_NAME; then
    log "停止旧容器..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# 启动新容器
log "启动容器..."
docker run -d \
    --name $CONTAINER_NAME \
    --restart=always \
    -p 8080:8080 \
    -v /data:/app/data \
    -e ENV=production \
    $IMAGE_NAME:$TAG

# 健康检查
sleep 3
if docker ps | grep -q $CONTAINER_NAME; then
    log "✓ 容器启动成功"
else
    log "✗ 容器启动失败"
    docker logs $CONTAINER_NAME
    exit 1
fi

# 清理旧镜像
log "清理未使用的镜像..."
docker image prune -f
```

## 工具函数库

### 通用工具函数

```bash
#!/bin/bash
# utils.sh - 通用工具函数库

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# 日志函数
LOG_FILE="/var/log/script.log"

log() {
    local level=$1
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

log_info() {
    log "INFO" "$@"
}

log_error() {
    log "ERROR" "$@"
}

# 检查命令是否存在
require_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "需要安装 $1"
        exit 1
    fi
}

# 检查是否root
require_root() {
    if [ $EUID -ne 0 ]; then
        print_error "需要root权限"
        exit 1
    fi
}

# 确认提示
confirm() {
    read -p "$1 [y/N]: " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

# 重试函数
retry() {
    local max_attempts=$1
    shift
    local cmd="$@"
    local attempt=1
    
    until $cmd; do
        if [ $attempt -ge $max_attempts ]; then
            print_error "重试 $max_attempts 次后失败"
            return 1
        fi
        print_warn "失败，$attempt/$max_attempts，5秒后重试..."
        sleep 5
        ((attempt++))
    done
}

# 进度条
progress_bar() {
    local current=$1
    local total=$2
    local width=50
    local percent=$((current * 100 / total))
    local completed=$((width * current / total))
    
    printf "\r["
    printf "%${completed}s" | tr ' ' '='
    printf "%$((width-completed))s" | tr ' ' '-'
    printf "] %d%%" $percent
    
    if [ $current -eq $total ]; then
        echo ""
    fi
}

# 使用示例
# source utils.sh
# require_command git
# if confirm "继续吗?"; then
#     log_info "用户确认"
# fi
```

## 定时任务配置

### Crontab示例

```bash
# 编辑crontab
crontab -e

# 每天凌晨2点备份
0 2 * * * /scripts/backup.sh

# 每小时检查服务
0 * * * * /scripts/monitor.sh

# 每5分钟清理日志
*/5 * * * * /scripts/cleanup.sh

# 每周日凌晨3点重启
0 3 * * 0 /sbin/reboot

# 每月1号执行
0 0 1 * * /scripts/monthly.sh

# 工作日每天9点
0 9 * * 1-5 /scripts/workday.sh
```

### systemd timer

```bash
# /etc/systemd/system/backup.service
[Unit]
Description=Backup Service

[Service]
Type=oneshot
ExecStart=/scripts/backup.sh

# /etc/systemd/system/backup.timer
[Unit]
Description=Backup Timer

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target

# 启用
systemctl enable backup.timer
systemctl start backup.timer

# 查看状态
systemctl list-timers
```

## 调试和优化

### Shell脚本性能分析

```bash
# time命令
time ./script.sh

# 详细统计
/usr/bin/time -v ./script.sh

# 逐行计时
PS4='+ $(date "+%s.%N")\011 '
set -x
commands
set +x

# 查找慢命令
bash -x script.sh 2>&1 | grep -E '^\+.*[0-9]{2}\.[0-9]+' | sort -k2 -rn
```

### 错误处理最佳实践

```bash
#!/bin/bash

set -euo pipefail  # 严格模式

# 捕获错误
trap 'echo "错误发生在第 $LINENO 行"' ERR

# 清理函数
cleanup() {
    echo "清理临时文件..."
    rm -f /tmp/tempfile.*
}

trap cleanup EXIT  # 退出时清理

# 检查依赖
for cmd in git wget curl; do
    if ! command -v $cmd &> /dev/null; then
        echo "缺少命令: $cmd"
        exit 1
    fi
done

# 主逻辑
main() {
    # ...
}

main "$@"
```

**核心：** Shell脚本重在实用和可维护，清晰的日志、完善的错误处理比追求技巧更重要。

