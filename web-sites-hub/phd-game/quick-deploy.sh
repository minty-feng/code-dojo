#!/bin/bash

# 🚀 PhD Simulator 一键部署脚本
# 支持传统部署和Docker部署两种方式

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# 配置变量
PROJECT_NAME="phd-game"
DEFAULT_PORT=3000

echo -e "${BLUE}🎮 PhD Simulator 一键部署脚本${NC}"
echo -e "${BLUE}================================${NC}"

# 检查Docker是否可用
check_docker() {
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# 显示部署选项
show_options() {
    echo -e "\n${YELLOW}请选择部署方式:${NC}"
    echo -e "1. ${GREEN}传统部署${NC} - 直接在服务器上安装和配置"
    echo -e "2. ${GREEN}Docker部署${NC} - 使用容器化部署 (推荐)"
    echo -e "3. ${GREEN}退出${NC}"
    
    read -p "请输入选择 (1-3): " choice
    
    case $choice in
        1)
            echo -e "\n${BLUE}🚀 开始传统部署...${NC}"
            traditional_deploy
            ;;
        2)
            if check_docker; then
                echo -e "\n${BLUE}🐳 开始Docker部署...${NC}"
                docker_deploy
            else
                echo -e "\n${RED}❌ Docker未安装，请先安装Docker和Docker Compose${NC}"
                echo -e "${YELLOW}💡 安装命令:${NC}"
                echo -e "   curl -fsSL https://get.docker.com | sh"
                echo -e "   sudo usermod -aG docker \$USER"
                echo -e "   sudo curl -L \"https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose"
                echo -e "   sudo chmod +x /usr/local/bin/docker-compose"
                exit 1
            fi
            ;;
        3)
            echo -e "\n${BLUE}👋 退出部署${NC}"
            exit 0
            ;;
        *)
            echo -e "\n${RED}❌ 无效选择，请重新运行脚本${NC}"
            exit 1
            ;;
    esac
}

# 传统部署
traditional_deploy() {
    echo -e "\n${YELLOW}📋 传统部署配置${NC}"
    
    # 获取端口
    read -p "请输入应用端口 (默认: $DEFAULT_PORT): " port
    port=${port:-$DEFAULT_PORT}
    
    # 获取域名
    read -p "请输入域名 (留空使用IP访问): " domain
    
    # 检查是否使用HTTPS
    read -p "是否启用HTTPS? (y/N): " enable_https
    enable_https=${enable_https:-N}
    
    echo -e "\n${BLUE}📋 部署配置确认:${NC}"
    echo -e "   端口: $port"
    echo -e "   域名: ${domain:-"使用IP访问"}"
    echo -e "   HTTPS: ${enable_https^^}"
    
    read -p "确认开始部署? (y/N): " confirm
    if [[ ${confirm^^} != "Y" ]]; then
        echo -e "\n${YELLOW}⚠️  部署已取消${NC}"
        exit 0
    fi
    
    # 执行传统部署
    echo -e "\n${YELLOW}🚀 开始传统部署...${NC}"
    
    # 设置环境变量
    export PORT=$port
    
    # 运行部署脚本
    if [[ -f "deploy.sh" ]]; then
        chmod +x deploy.sh
        ./deploy.sh
    else
        echo -e "${RED}❌ 未找到 deploy.sh 脚本${NC}"
        exit 1
    fi
    
    # 配置域名和HTTPS
    if [[ -n "$domain" ]]; then
        configure_domain "$domain" "$port"
        
        if [[ ${enable_https^^} == "Y" ]]; then
            configure_https "$domain"
        fi
    fi
    
    show_traditional_result "$port"
}

# Docker部署
docker_deploy() {
    echo -e "\n${YELLOW}📋 Docker部署配置${NC}"
    
    # 获取端口
    read -p "请输入应用端口 (默认: $DEFAULT_PORT): " port
    port=${port:-$DEFAULT_PORT}
    
    # 获取域名
    read -p "请输入域名 (留空使用IP访问): " domain
    
    # 检查是否使用HTTPS
    read -p "是否启用HTTPS? (y/N): " enable_https
    enable_https=${enable_https:-N}
    
    echo -e "\n${BLUE}📋 部署配置确认:${NC}"
    echo -e "   端口: $port"
    echo -e "   域名: ${domain:-"使用IP访问"}"
    echo -e "   HTTPS: ${enable_https^^}"
    
    read -p "确认开始部署? (y/N): " confirm
    if [[ ${confirm^^} != "Y" ]]; then
        echo -e "\n${YELLOW}⚠️  部署已取消${NC}"
        exit 0
    fi
    
    # 执行Docker部署
    echo -e "\n${YELLOW}🐳 开始Docker部署...${NC}"
    
    # 检查必要文件
    if [[ ! -f "Dockerfile" ]] || [[ ! -f "docker-compose.yml" ]]; then
        echo -e "${RED}❌ 缺少Docker配置文件${NC}"
        exit 1
    fi
    
    # 修改端口配置
    sed -i "s/3000:3000/$port:3000/" docker-compose.yml
    
    # 配置域名
    if [[ -n "$domain" ]]; then
        sed -i "s/server_name _;/server_name $domain;/" nginx.conf
    fi
    
    # 配置HTTPS
    if [[ ${enable_https^^} == "Y" ]]; then
        setup_ssl_certificates "$domain"
    else
        # 禁用HTTPS，只使用HTTP
        sed -i '/listen 443/d' nginx.conf
        sed -i '/ssl_/d' nginx.conf
        sed -i '/return 301/d' nginx.conf
    fi
    
    # 构建并启动
    echo -e "\n${YELLOW}🔨 构建Docker镜像...${NC}"
    docker-compose build
    
    echo -e "\n${YELLOW}🚀 启动服务...${NC}"
    docker-compose up -d
    
    # 等待服务启动
    echo -e "\n${YELLOW}⏳ 等待服务启动...${NC}"
    sleep 10
    
    # 检查服务状态
    if docker-compose ps | grep -q "Up"; then
        echo -e "\n${GREEN}✅ Docker部署成功！${NC}"
        show_docker_result "$port" "$domain" "$enable_https"
    else
        echo -e "\n${RED}❌ Docker部署失败，请检查日志${NC}"
        docker-compose logs
        exit 1
    fi
}

# 配置域名
configure_domain() {
    local domain=$1
    local port=$2
    
    echo -e "\n${YELLOW}🌐 配置域名: $domain${NC}"
    
    # 创建Nginx配置
    sudo tee /etc/nginx/sites-available/$PROJECT_NAME > /dev/null << EOF
server {
    listen 80;
    server_name $domain;

    location / {
        proxy_pass http://localhost:$port;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
    
    # 启用站点
    sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
    
    # 测试并重启Nginx
    if sudo nginx -t; then
        sudo systemctl restart nginx
        echo -e "${GREEN}✅ 域名配置完成${NC}"
    else
        echo -e "${RED}❌ Nginx配置失败${NC}"
        exit 1
    fi
}

# 配置HTTPS
configure_https() {
    local domain=$1
    
    echo -e "\n${YELLOW}🔒 配置HTTPS: $domain${NC}"
    
    # 检查certbot
    if ! command -v certbot &> /dev/null; then
        echo -e "${YELLOW}📦 安装Certbot...${NC}"
        if [[ -f /etc/debian_version ]]; then
            sudo apt install -y certbot python3-certbot-nginx
        elif [[ -f /etc/redhat-release ]]; then
            sudo yum install -y certbot python3-certbot-nginx
        fi
    fi
    
    # 获取证书
    echo -e "\n${YELLOW}🔐 获取SSL证书...${NC}"
    sudo certbot --nginx -d $domain --non-interactive --agree-tos --email admin@$domain
    
    echo -e "${GREEN}✅ HTTPS配置完成${NC}"
}

# 设置SSL证书
setup_ssl_certificates() {
    local domain=$1
    
    echo -e "\n${YELLOW}🔐 设置SSL证书: $domain${NC}"
    
    # 创建SSL目录
    mkdir -p ssl
    
    # 检查是否有现有证书
    if [[ -f "ssl/cert.pem" ]] && [[ -f "ssl/key.pem" ]]; then
        echo -e "${GREEN}✅ 发现现有SSL证书${NC}"
        return 0
    fi
    
    # 生成自签名证书 (开发环境)
    echo -e "${YELLOW}📝 生成自签名SSL证书...${NC}"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=CN/ST=State/L=City/O=Organization/CN=$domain"
    
    echo -e "${GREEN}✅ SSL证书生成完成${NC}"
    echo -e "${YELLOW}⚠️  注意：这是自签名证书，浏览器会显示警告${NC}"
    echo -e "${YELLOW}💡 生产环境建议使用Let's Encrypt证书${NC}"
}

# 显示传统部署结果
show_traditional_result() {
    local port=$1
    
    echo -e "\n${GREEN}🎉 传统部署完成！${NC}"
    echo -e "${BLUE}📋 部署信息:${NC}"
    echo -e "   应用名称: $PROJECT_NAME"
    echo -e "   应用端口: $port"
    echo -e "   应用目录: /var/www/$PROJECT_NAME"
    
    echo -e "\n${BLUE}🔗 访问地址:${NC}"
    echo -e "   本地访问: http://localhost:$port"
    echo -e "   外部访问: http://$(curl -s ifconfig.me):$port"
    
    echo -e "\n${BLUE}📊 管理命令:${NC}"
    echo -e "   查看状态: pm2 status"
    echo -e "   查看日志: pm2 logs $PROJECT_NAME"
    echo -e "   重启应用: pm2 restart $PROJECT_NAME"
}

# 显示Docker部署结果
show_docker_result() {
    local port=$1
    local domain=$2
    local enable_https=$3
    
    echo -e "\n${GREEN}🎉 Docker部署完成！${NC}"
    echo -e "${BLUE}📋 部署信息:${NC}"
    echo -e "   应用名称: $PROJECT_NAME"
    echo -e "   应用端口: $port"
    echo -e "   域名: ${domain:-"使用IP访问"}"
    echo -e "   HTTPS: ${enable_https^^}"
    
    echo -e "\n${BLUE}🔗 访问地址:${NC}"
    if [[ -n "$domain" ]]; then
        if [[ ${enable_https^^} == "Y" ]]; then
            echo -e "   应用: https://$domain"
        else
            echo -e "   应用: http://$domain"
        fi
    else
        echo -e "   应用: http://localhost:$port"
        echo -e "   外部访问: http://$(curl -s ifconfig.me):$port"
    fi
    
    echo -e "\n${BLUE}📊 管理命令:${NC}"
    echo -e "   查看状态: docker-compose ps"
    echo -e "   查看日志: docker-compose logs -f"
    echo -e "   重启服务: docker-compose restart"
    echo -e "   停止服务: docker-compose stop"
    echo -e "   启动服务: docker-compose start"
}

# 主函数
main() {
    # 检查系统
    if [[ $EUID -eq 0 ]]; then
        echo -e "${RED}❌ 请不要使用root用户运行此脚本${NC}"
        exit 1
    fi
    
    # 检查必要工具
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}❌ 未找到 curl 命令${NC}"
        exit 1
    fi
    
    # 显示部署选项
    show_options
}

# 运行主函数
main "$@"
