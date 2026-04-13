#!/bin/bash

# 🎮 PhD Simulator 简单部署脚本
# 专门针对 game.joketop.com.cn 域名
# 适用于已有其他服务的服务器

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置变量
DOMAIN="game.joketop.com.cn"
SITE_NAME="phd-game"
WEB_ROOT="/var/www/$SITE_NAME"
NGINX_SITE="/etc/nginx/sites-available/$SITE_NAME"

echo -e "${BLUE}🎮 PhD Simulator 部署脚本${NC}"
echo -e "${BLUE}域名: $DOMAIN${NC}"
echo -e "${BLUE}========================${NC}"

# 检查是否为root用户
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ 请不要使用root用户运行此脚本${NC}"
   exit 1
fi

# 检查系统类型
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo -e "${RED}❌ 无法检测操作系统${NC}"
    exit 1
fi

echo -e "${BLUE}📋 检测到操作系统: $OS $VER${NC}"

# 创建网站目录
create_web_directory() {
    echo -e "${YELLOW}📁 创建网站目录...${NC}"
    
    sudo mkdir -p $WEB_ROOT
    sudo chown $USER:$USER $WEB_ROOT
    
    if [[ ! -d "$WEB_ROOT" ]]; then
        echo -e "${RED}❌ 无法创建网站目录${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 网站目录创建成功: $WEB_ROOT${NC}"
}

# 安装Nginx (如果未安装)
install_nginx() {
    echo -e "${YELLOW}📦 检查/安装 Nginx...${NC}"
    
    if ! command -v nginx &> /dev/null; then
        if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
            sudo apt update
            sudo apt install -y nginx
        elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
            sudo yum install -y nginx
        else
            echo -e "${RED}❌ 不支持的操作系统: $OS${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Nginx 已安装${NC}"
    fi
}

# 创建Nginx配置
create_nginx_config() {
    echo -e "${YELLOW}⚙️ 创建 Nginx 配置...${NC}"
    
    # 创建Nginx配置文件
    sudo tee $NGINX_SITE > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    root $WEB_ROOT;
    index index.html;
    
    # 启用gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|ttf|woff|woff2|yaml)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary Accept-Encoding;
    }
    
    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # 安全头
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF
    
    echo -e "${GREEN}✅ Nginx 配置文件创建完成${NC}"
}

# 启用Nginx站点
enable_nginx_site() {
    echo -e "${YELLOW}🔗 启用 Nginx 站点...${NC}"
    
    # 创建软链接
    sudo ln -sf $NGINX_SITE /etc/nginx/sites-enabled/
    
    # 测试配置
    if sudo nginx -t; then
        sudo systemctl restart nginx
        sudo systemctl enable nginx
        echo -e "${GREEN}✅ Nginx 站点启用成功${NC}"
    else
        echo -e "${RED}❌ Nginx 配置测试失败${NC}"
        exit 1
    fi
}

# 配置防火墙
configure_firewall() {
    echo -e "${YELLOW}🔥 配置防火墙...${NC}"
    
    if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
        if command -v ufw &> /dev/null; then
            sudo ufw allow 80/tcp
            sudo ufw allow 443/tcp
            echo -e "${GREEN}✅ UFW 防火墙配置完成${NC}"
        fi
    elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
        if command -v firewall-cmd &> /dev/null; then
            sudo firewall-cmd --permanent --add-service=http
            sudo firewall-cmd --permanent --add-service=https
            sudo firewall-cmd --reload
            echo -e "${GREEN}✅ Firewalld 防火墙配置完成${NC}"
        fi
    fi
}

# 显示部署结果
show_result() {
    echo -e "\n${GREEN}🎉 部署完成！${NC}"
    echo -e "${BLUE}📋 部署信息:${NC}"
    echo -e "   域名: $DOMAIN"
    echo -e "   网站目录: $WEB_ROOT"
    echo -e "   Nginx配置: $NGINX_SITE"
    
    echo -e "\n${BLUE}📁 下一步操作:${NC}"
    echo -e "   1. 将项目文件上传到: $WEB_ROOT"
    echo -e "   2. 确保域名 $DOMAIN 解析到此服务器IP"
    echo -e "   3. 访问: http://$DOMAIN"
    
    echo -e "\n${BLUE}📊 管理命令:${NC}"
    echo -e "   重启Nginx: sudo systemctl restart nginx"
    echo -e "   查看状态: sudo systemctl status nginx"
    echo -e "   查看日志: sudo tail -f /var/log/nginx/access.log"
    
    echo -e "\n${YELLOW}⚠️  重要提醒:${NC}"
    echo -e "   - 确保域名 $DOMAIN 已解析到此服务器IP"
    echo -e "   - 上传项目文件到 $WEB_ROOT 目录"
    echo -e "   - 如果需要HTTPS，可以后续配置SSL证书"
}

# 检查域名解析
check_domain() {
    echo -e "${YELLOW}🔍 检查域名解析...${NC}"
    
    # 获取服务器公网IP
    SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "无法获取")
    
    if [[ "$SERVER_IP" != "无法获取" ]]; then
        echo -e "${BLUE}📡 服务器公网IP: $SERVER_IP${NC}"
        echo -e "${YELLOW}💡 请确保域名 $DOMAIN 解析到IP: $SERVER_IP${NC}"
    else
        echo -e "${YELLOW}⚠️  无法获取服务器公网IP${NC}"
    fi
    
    # 检查域名解析
    DOMAIN_IP=$(dig +short $DOMAIN 2>/dev/null | head -1)
    
    if [[ -n "$DOMAIN_IP" ]]; then
        echo -e "${BLUE}🌐 域名 $DOMAIN 解析到: $DOMAIN_IP${NC}"
        if [[ "$DOMAIN_IP" == "$SERVER_IP" ]]; then
            echo -e "${GREEN}✅ 域名解析正确！${NC}"
        else
            echo -e "${YELLOW}⚠️  域名解析可能不正确，请检查DNS设置${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  无法解析域名 $DOMAIN，请检查DNS设置${NC}"
    fi
}

# 主函数
main() {
    echo -e "${BLUE}🎮 开始部署 PhD Simulator 到 $DOMAIN${NC}"
    
    # 检查必要工具
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}❌ 未找到 curl 命令${NC}"
        exit 1
    fi
    
    # 执行部署步骤
    create_web_directory
    install_nginx
    create_nginx_config
    enable_nginx_site
    configure_firewall
    check_domain
    show_result
}

# 运行主函数
main "$@"
