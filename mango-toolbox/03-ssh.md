# SSH 安全连接工具

## 核心概念
- **SSH(Secure Shell)**：加密的网络传输协议，用于安全登录和文件传输
- **密钥对**：公钥和私钥，用于身份验证，比密码更安全
- **端口转发**：将本地端口转发到远程主机，实现隧道功能
- **跳板机**：通过中间主机连接到目标主机

## 基础连接
```bash
# 基本连接
ssh user@hostname              # 使用用户名和主机名连接
ssh user@192.168.1.100         # 使用IP地址连接
ssh -p 2222 user@hostname       # 指定端口连接
ssh -v user@hostname            # 详细输出模式
ssh -vvv user@hostname          # 最详细的调试输出

# 使用密钥连接
ssh -i ~/.ssh/id_rsa user@hostname # 使用指定私钥
ssh -i ~/.ssh/id_rsa -p 2222 user@hostname # 指定端口和密钥

# 连接选项
ssh -X user@hostname            # 启用X11转发
ssh -Y user@hostname            # 启用可信X11转发
ssh -C user@hostname            # 启用压缩
ssh -o StrictHostKeyChecking=no user@hostname # 跳过主机验证
```

## 密钥管理
```bash
# 生成密钥对
ssh-keygen                     # 交互式生成密钥
ssh-keygen -t rsa -b 4096      # 生成4096位RSA密钥
ssh-keygen -t ed25519          # 生成ED25519密钥(推荐)
ssh-keygen -t ecdsa -b 521     # 生成521位ECDSA密钥
ssh-keygen -f ~/.ssh/my_key    # 指定密钥文件名

# 密钥管理
ssh-add ~/.ssh/id_rsa          # 添加私钥到ssh-agent
ssh-add -l                     # 列出已加载的密钥
ssh-add -D                     # 删除所有密钥
ssh-add -d ~/.ssh/id_rsa       # 删除指定密钥

# 复制公钥到服务器
ssh-copy-id user@hostname       # 复制公钥到服务器
ssh-copy-id -i ~/.ssh/id_rsa.pub user@hostname # 复制指定公钥
ssh-copy-id -p 2222 user@hostname # 指定端口复制

# 手动复制公钥
cat ~/.ssh/id_rsa.pub | ssh user@hostname "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## SSH配置文件
```bash
# ~/.ssh/config 配置文件
Host myserver
    HostName 192.168.1.100
    User admin
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
    ForwardAgent yes

Host *.example.com
    User deploy
    IdentityFile ~/.ssh/deploy_key
    Port 2222

Host jump
    HostName jump.example.com
    User jumpuser
    IdentityFile ~/.ssh/jump_key

Host target
    HostName target.example.com
    User targetuser
    ProxyJump jump
    IdentityFile ~/.ssh/target_key
```

## 端口转发
```bash
# 本地端口转发
ssh -L 8080:localhost:80 user@hostname # 本地8080转发到远程80
ssh -L 8080:192.168.1.100:80 user@hostname # 转发到其他主机
ssh -L 8080:localhost:80 -L 9090:localhost:90 user@hostname # 多个端口转发

# 远程端口转发
ssh -R 8080:localhost:80 user@hostname # 远程8080转发到本地80
ssh -R 8080:192.168.1.100:80 user@hostname # 转发到其他主机

# 动态端口转发(SOCKS代理)
ssh -D 1080 user@hostname       # 创建SOCKS代理
ssh -D 1080 -N user@hostname    # 后台运行代理

# 后台运行转发
ssh -f -N -L 8080:localhost:80 user@hostname # 后台运行本地转发
ssh -f -N -R 8080:localhost:80 user@hostname # 后台运行远程转发
```

## 跳板机和多跳连接
```bash
# 跳板机连接
ssh -J jump@jump.host user@target.host # 通过跳板机连接
ssh -o ProxyJump=jump@jump.host user@target.host # 使用ProxyJump选项

# 多跳连接
ssh -J user1@host1,user2@host2 user3@host3 # 多级跳转
ssh -J jump1@host1 -J jump2@host2 user@target # 多个跳板机

# 配置文件中的跳板机
Host target
    HostName target.example.com
    User targetuser
    ProxyJump jump@jump.example.com
    IdentityFile ~/.ssh/target_key
```

## 文件传输
```bash
# SCP文件复制
scp file.txt user@hostname:/path/ # 复制文件到远程
scp user@hostname:/path/file.txt ./ # 从远程复制文件
scp -r dir/ user@hostname:/path/ # 递归复制目录
scp -P 2222 file.txt user@hostname:/path/ # 指定端口
scp -i ~/.ssh/id_rsa file.txt user@hostname:/path/ # 使用密钥

# RSYNC同步
rsync -avz file.txt user@hostname:/path/ # 同步文件
rsync -avz --delete dir/ user@hostname:/path/ # 同步目录(删除多余文件)
rsync -avz -e "ssh -p 2222" file.txt user@hostname:/path/ # 指定SSH选项
rsync -avz --exclude="*.log" dir/ user@hostname:/path/ # 排除文件

# SFTP交互式传输
sftp user@hostname              # 启动SFTP会话
sftp -P 2222 user@hostname      # 指定端口
sftp -i ~/.ssh/id_rsa user@hostname # 使用密钥

# SFTP批处理
echo "put file.txt" | sftp user@hostname
echo -e "put file.txt\nquit" | sftp user@hostname
```

## 高级选项
```bash
# 连接选项
ssh -o StrictHostKeyChecking=no user@hostname # 跳过主机验证
ssh -o UserKnownHostsFile=/dev/null user@hostname # 不保存主机密钥
ssh -o ConnectTimeout=10 user@hostname # 连接超时10秒
ssh -o ServerAliveInterval=60 user@hostname # 每60秒发送保活包
ssh -o ServerAliveCountMax=3 user@hostname # 最多发送3个保活包
ssh -o Compression=yes user@hostname # 启用压缩
ssh -o LogLevel=DEBUG user@hostname # 调试模式

# 保持连接
ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 user@hostname
ssh -o TCPKeepAlive=yes user@hostname # TCP保活

# 连接复用
ssh -o ControlMaster=auto -o ControlPath=~/.ssh/master-%r@%h:%p user@hostname
ssh -o ControlPersist=10m user@hostname # 连接保持10分钟
```

## 批量操作
```bash
# 并行SSH执行
parallel-ssh -h hosts.txt "uptime" # 并行执行命令
parallel-ssh -i -h hosts.txt "sudo systemctl restart nginx" # 交互式执行
parallel-ssh -O StrictHostKeyChecking=no -h hosts.txt "command" # 设置SSH选项

# 批量执行脚本
for host in host1 host2 host3; do
    echo "Executing on $host..."
    ssh user@$host "command"
done

# 使用expect自动化
#!/usr/bin/expect
spawn ssh user@hostname
expect "password:"
send "password\r"
expect "$ "
send "command\r"
expect "$ "
send "exit\r"
```

## 安全配置
```bash
# 服务器端配置 /etc/ssh/sshd_config
Port 2222                      # 更改默认端口
PermitRootLogin no             # 禁用root登录
PasswordAuthentication no      # 禁用密码认证
PubkeyAuthentication yes       # 启用公钥认证
AuthorizedKeysFile .ssh/authorized_keys # 公钥文件位置
MaxAuthTries 3                # 最大认证尝试次数
MaxSessions 2                 # 最大会话数
ClientAliveInterval 300        # 客户端保活间隔
ClientAliveCountMax 2          # 客户端保活次数

# 限制用户和IP
AllowUsers user1 user2         # 允许的用户
AllowGroups sshusers           # 允许的用户组
AllowUsers user@192.168.1.*   # 限制IP范围
DenyUsers baduser              # 拒绝的用户
DenyGroups badgroup            # 拒绝的用户组

# 重启SSH服务
sudo systemctl restart sshd    # 重启SSH服务
sudo service ssh restart       # 旧版本重启命令
```

## 故障排查
```bash
# 测试连接
ssh -T git@github.com           # 测试GitHub连接
ssh -T git@gitlab.com          # 测试GitLab连接
ssh -o ConnectTimeout=5 user@hostname # 测试连接超时

# 查看SSH日志
tail -f /var/log/auth.log       # 查看认证日志
journalctl -u ssh -f            # 使用journalctl查看日志
tail -f /var/log/secure         # CentOS/RHEL系统

# 检查SSH服务状态
systemctl status ssh            # 查看SSH服务状态
systemctl restart ssh           # 重启SSH服务
ss -tlnp | grep :22             # 检查SSH端口监听

# 验证密钥
ssh-keygen -lf ~/.ssh/id_rsa.pub # 查看公钥指纹
ssh-keygen -y -f ~/.ssh/id_rsa   # 从私钥生成公钥
ssh-keygen -c -f ~/.ssh/id_rsa   # 修改密钥注释

# 网络问题诊断
ping hostname                    # 测试网络连通性
telnet hostname 22              # 测试端口连通性
nc -zv hostname 22              # 使用netcat测试端口
```

## 实用脚本
```bash
#!/bin/bash
# SSH批量执行脚本
HOSTS="host1 host2 host3"
USER="admin"
COMMAND="uptime"

for host in $HOSTS; do
    echo "Executing on $host..."
    ssh -o ConnectTimeout=5 $USER@$host "$COMMAND"
    if [ $? -eq 0 ]; then
        echo "Success on $host"
    else
        echo "Failed on $host"
    fi
done
```

```bash
#!/bin/bash
# SSH隧道管理脚本
case "$1" in
    start)
        ssh -f -N -L 8080:localhost:80 user@hostname
        echo "Tunnel started"
        ;;
    stop)
        pkill -f "ssh.*-L 8080:localhost:80"
        echo "Tunnel stopped"
        ;;
    status)
        if pgrep -f "ssh.*-L 8080:localhost:80" > /dev/null; then
            echo "Tunnel is running"
        else
            echo "Tunnel is not running"
        fi
        ;;
esac
```

## 性能优化
```bash
# 连接复用配置
Host *
    ControlMaster auto
    ControlPath ~/.ssh/master-%r@%h:%p
    ControlPersist 10m
    ServerAliveInterval 60
    ServerAliveCountMax 3

# 压缩传输
ssh -C user@hostname            # 启用压缩
ssh -o Compression=yes user@hostname # 配置文件启用压缩

# 禁用DNS反向解析
ssh -o GSSAPIAuthentication=no user@hostname
# 在配置文件中添加
Host *
    GSSAPIAuthentication no
```

## 常用别名
```bash
# ~/.bashrc 或 ~/.zshrc
alias ssh-prod="ssh user@prod-server"
alias ssh-dev="ssh user@dev-server"
alias ssh-jump="ssh -J jump@jump.host"
alias ssh-tunnel="ssh -L 8080:localhost:8080 user@host"
alias ssh-mysql="ssh -L 3306:localhost:3306 user@host"
alias ssh-postgres="ssh -L 5432:localhost:5432 user@host"
```

## 密钥轮换
```bash
# 生成新密钥
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new -C "new-key-$(date +%Y%m%d)"

# 复制新公钥到服务器
ssh-copy-id -i ~/.ssh/id_ed25519_new.pub user@hostname

# 测试新密钥
ssh -i ~/.ssh/id_ed25519_new user@hostname

# 更新配置文件
# 在 ~/.ssh/config 中更新 IdentityFile

# 删除旧密钥
ssh-add -d ~/.ssh/id_rsa
rm ~/.ssh/id_rsa*
```