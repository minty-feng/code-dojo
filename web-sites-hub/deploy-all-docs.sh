#!/bin/bash
# 统一文档部署脚本
# 用于同时部署多个文档服务到 Nginx

set -e

# 配置变量
DOMAIN="blog.joketop.com"
JOKETOP_DEPLOY_DIR="/var/www/html/joketop"
NGINX_SITES_AVAILABLE="/etc/nginx/sites-available"
NGINX_SITES_ENABLED="/etc/nginx/sites-enabled"
NGINX_CONF_FILE="$NGINX_SITES_AVAILABLE/joketop.conf"
# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NGINX_CONF_TEMPLATE="$SCRIPT_DIR/joketop.conf"
NGINX_CONF_TEMPLATE_HTTP="$SCRIPT_DIR/joketop-http.conf"
NGINX_LETSENCRYPT_TEMP="$SCRIPT_DIR/joketop-letsencrypt-temp.conf"


# 服务配置数组
# 格式: "路径:部署目录:服务名称"
declare -a SERVICES=(
    "/backend:/var/www/html/honey-backend-dojo:Backend Tutorial"
    "/frontend:/var/www/html/grape-frontend-dojo:Frontend Tutorial"
    "/ds:/var/www/html/apple-ds-core:Data Structures Tutorial"
    "/algo:/var/www/html/banana-algo-core:Algorithms Tutorial"
    "/os:/var/www/html/cookie-os-network:OS & Network Tutorial"
    "/miniprogram:/var/www/html/jam-miniprogram-dojo:Mini Program Tutorial"
)

# HTTPS 配置
# 取值说明：
#   http         - 默认仅部署 HTTP
#   letsencrypt  - 请求自动获取证书
#   manual       - 手动指定证书
#   https        - 证书就绪，部署 HTTPS
ENABLE_HTTPS="http"
SSL_CERT_PATH=""
SSL_KEY_PATH=""
LETSENCRYPT_EMAIL=""

ensure_nginx_ready() {
    echo "   🔎 检查 Nginx 环境..."
    if ! command -v nginx >/dev/null 2>&1; then
        echo "   📥 未检测到 Nginx，正在安装..."
        if command -v apt-get >/dev/null 2>&1; then
            apt-get update
            apt-get install -y nginx
        elif command -v yum >/dev/null 2>&1; then
            yum install -y nginx
        else
            echo "❌ 无法自动安装 Nginx，请先手动安装后重试"
            exit 1
        fi
    else
        echo "   ✅ 已检测到 Nginx"
    fi

    for nginx_dir in "$NGINX_SITES_AVAILABLE" "$NGINX_SITES_ENABLED"; do
        if [ ! -d "$nginx_dir" ]; then
            echo "   📁 创建目录: $nginx_dir"
            mkdir -p "$nginx_dir"
        fi
    done

    if [ ! -d "/var/log/nginx" ]; then
        echo "   📁 创建目录: /var/log/nginx"
        mkdir -p /var/log/nginx
    fi
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --letsencrypt)
            ENABLE_HTTPS="letsencrypt"
            shift
            ;;
        --email)
            LETSENCRYPT_EMAIL="$2"
            shift 2
            ;;
        --cert)
            ENABLE_HTTPS="manual"
            SSL_CERT_PATH="$2"
            shift 2
            ;;
        --key)
            SSL_KEY_PATH="$2"
            shift 2
            ;;
        --help)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --letsencrypt          使用 Let's Encrypt 自动获取 SSL 证书"
            echo "  --email EMAIL          Let's Encrypt 邮箱地址（必需）"
            echo "  --cert CERT_PATH       手动指定 SSL 证书路径"
            echo "  --key KEY_PATH         手动指定 SSL 私钥路径"
            echo "  --help                 显示此帮助信息"
            echo ""
            echo "示例:"
            echo "  # HTTP 部署"
            echo "  sudo $0"
            echo ""
            echo "  # HTTPS 部署（Let's Encrypt）"
            echo "  sudo $0 --letsencrypt --email your@email.com"
            echo ""
            echo "  # HTTPS 部署（手动证书）"
            echo "  sudo $0 --cert /path/to/cert.pem --key /path/to/key.pem"
            exit 0
            ;;
        *)
            echo "❌ 未知参数: $1"
            echo "使用 --help 查看帮助信息"
            exit 1
            ;;
    esac
done

# 检查是否以 root 权限运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用 sudo 运行此脚本"
    exit 1
fi

echo ""
echo "=========================================="
echo "  📦 统一文档部署脚本"
echo "=========================================="
echo ""

# 检查服务目录是否存在
echo "📋 步骤 1/6: 检查服务目录..."
for service_config in "${SERVICES[@]}"; do
    IFS=':' read -r path deploy_dir service_name <<< "$service_config"
    if [ ! -d "$deploy_dir" ]; then
        echo "⚠️  警告: 目录不存在: $deploy_dir (路径: $path)"
    else
        echo "   ✅ 找到: $service_name ($path) -> $deploy_dir"
    fi
done
echo ""

# Let's Encrypt 配置
if [ "$ENABLE_HTTPS" = "letsencrypt" ]; then
    echo "📋 步骤 2/6: 配置 SSL 证书..."
    if [ -z "$LETSENCRYPT_EMAIL" ]; then
        echo "❌ 使用 --letsencrypt 时必须提供 --email 参数"
        exit 1
    fi

    ensure_nginx_ready
    
    echo "   📧 邮箱: $LETSENCRYPT_EMAIL"
    
    # 检查 certbot 是否安装
    if ! command -v certbot &> /dev/null; then
        echo "   📥 正在安装 certbot..."
        if command -v apt-get &> /dev/null; then
            apt-get update
            apt-get install -y certbot python3-certbot-nginx
        elif command -v yum &> /dev/null; then
            yum install -y certbot python3-certbot-nginx
        else
            echo "❌ 无法自动安装 certbot，请手动安装"
            exit 1
        fi
    else
        echo "   ✅ certbot 已安装"
    fi
    
    echo "   🔧 部署临时 HTTP 配置（用于 Let's Encrypt 验证）..."
    
    # 检查临时配置文件是否存在
    if [ ! -f "$NGINX_LETSENCRYPT_TEMP" ]; then
        echo "❌ 错误: Let's Encrypt 临时配置不存在: $NGINX_LETSENCRYPT_TEMP"
        exit 1
    fi
    
    # 拷贝临时配置文件（只包含 HTTP，因为证书还不存在）
    cp "$NGINX_LETSENCRYPT_TEMP" "$NGINX_CONF_FILE"
    
    # 创建符号链接并测试
    ln -sf "$NGINX_CONF_FILE" "$NGINX_SITES_ENABLED/joketop.conf"
    
    
    echo "   🧪 测试 Nginx 配置..."
    if nginx -t 2>&1 | grep -q "successful"; then
        echo "   ✅ 配置测试通过"
        echo "   🔄 重新加载 Nginx..."
        systemctl reload nginx || systemctl restart nginx
    else
        echo "❌ Nginx 配置测试失败"
        exit 1
    fi
    
    echo ""
    echo "📋 步骤 3/6: 获取 SSL 证书..."

    # 获取证书（只为已有证书的域名扩展，或只为 blog.joketop.com）
    
    # 需要证书的域名列表
    CERT_DOMAINS=("blog.joketop.com" "showcase.joketop.com" "diary.joketop.com")
    
    echo "   🔐 检查并获取证书..."
    for domain in "${CERT_DOMAINS[@]}"; do
        if [ -f "/etc/letsencrypt/live/$domain/fullchain.pem" ]; then
            echo "   ✅ $domain 证书已存在"
        else
            echo "   📜 正在为 $domain 获取证书..."
            if certbot certonly --nginx -d "$domain" --non-interactive --agree-tos --email "$LETSENCRYPT_EMAIL" 2>&1 | tee /tmp/certbot-$domain.log; then
                echo "   ✅ $domain 证书获取成功"
            else
                echo "   ⚠️  $domain 证书获取失败"
                # 检查是否是 DNS 问题
                if grep -q "no valid A records found\|DNS problem" /tmp/certbot-$domain.log 2>/dev/null; then
                    echo "      原因：DNS 记录未配置，请先配置 DNS 后重新运行"
                fi
            fi
        fi
    done
    
    echo ""
    echo "   💡 提示: joketop.com, www.joketop.com, me.joketop.com 需要先配置 DNS 记录才能获取证书"
    
    # Certbot 可能会修改其他配置文件，需要清理并确保使用统一配置
    echo "   🧹 清理可能的配置冲突..."
    ln -sf "$NGINX_CONF_FILE" "$NGINX_SITES_ENABLED/joketop.conf"
    rm -f "$NGINX_SITES_ENABLED/docs-code-dojo"
    rm -f "$NGINX_SITES_ENABLED/joketop.com"
  
    
    echo ""
    echo "📋 步骤 4/6: 检查证书状态..."
    
    # 检查所有需要 HTTPS 的域名的证书
    MISSING_CERTS=()
    REQUIRED_CERT_DOMAINS=("blog.joketop.com" "showcase.joketop.com" "diary.joketop.com")
    
    for domain in "${REQUIRED_CERT_DOMAINS[@]}"; do
        if [ -f "/etc/letsencrypt/live/$domain/fullchain.pem" ]; then
            echo "   ✅ $domain 证书存在"
        else
            echo "   ❌ $domain 证书不存在"
            MISSING_CERTS+=("$domain")
        fi
    done
    
    # 如果有缺失的证书，提示用户
    if [ ${#MISSING_CERTS[@]} -gt 0 ]; then
        echo ""
        echo "   ⚠️  以下域名的证书不存在："
        for domain in "${MISSING_CERTS[@]}"; do
            echo "      - $domain"
        done
        echo ""
        echo "   需要先配置 DNS 并获取证书："
        for domain in "${MISSING_CERTS[@]}"; do
            echo "      sudo certbot certonly --nginx -d $domain --email $LETSENCRYPT_EMAIL"
        done
        echo ""
        echo "   或者修改 joketop.conf，将缺失证书的域名改为 HTTP 配置"
        exit 1
    fi
    
    ENABLE_HTTPS="https"
    echo "   ✅ 所有证书都已就绪，将部署 HTTPS 配置"
    echo ""
fi

# 手动 HTTPS 配置检查
if [ "$ENABLE_HTTPS" = "manual" ]; then
    if [ -z "$SSL_CERT_PATH" ] || [ -z "$SSL_KEY_PATH" ]; then
        echo "❌ 使用 --cert/--key 时必须同时提供证书和私钥路径"
        exit 1
    fi
    if [ ! -f "$SSL_CERT_PATH" ] || [ ! -f "$SSL_KEY_PATH" ]; then
        echo "❌ SSL 证书文件不存在"
        echo "   证书: $SSL_CERT_PATH"
        echo "   私钥: $SSL_KEY_PATH"
        exit 1
    fi
    ENABLE_HTTPS="https"
fi

# 部署 Nginx 配置
echo "📋 步骤 5/6: 部署 Nginx 配置..."

# 检查部署目录是否存在
echo "   🔍 检查部署目录..."
if [ ! -d "$JOKETOP_DEPLOY_DIR" ]; then
    echo "❌ 错误: 部署目录不存在: $JOKETOP_DEPLOY_DIR"
    echo "   请先运行 deploy-joketop.sh 部署文件"
    echo "   示例: sudo ./deploy-joketop.sh joketop-*.tar.gz"
    exit 1
fi

ensure_nginx_ready

# 检查关键文件是否存在
if [ ! -f "$JOKETOP_DEPLOY_DIR/index.html" ]; then
    echo "❌ 错误: index.html 不存在: $JOKETOP_DEPLOY_DIR/index.html"
    echo "   请先运行 deploy-joketop.sh 部署文件"
    exit 1
fi

if [ ! -f "$JOKETOP_DEPLOY_DIR/resume.html" ]; then
    echo "   ⚠️  警告: resume.html 不存在"
fi

if [ ! -f "$JOKETOP_DEPLOY_DIR/learning.html" ]; then
    echo "   ⚠️  警告: learning.html 不存在"
fi

if [ ! -f "$JOKETOP_DEPLOY_DIR/showcase.html" ]; then
    echo "   ⚠️  警告: showcase.html 不存在"
fi

if [ ! -f "$JOKETOP_DEPLOY_DIR/diary.html" ]; then
    echo "   ⚠️  警告: diary.html 不存在"
fi

echo "   ✅ 部署目录检查通过"
echo ""

# 检查配置文件模板是否存在
SELECTED_TEMPLATE="$NGINX_CONF_TEMPLATE_HTTP"
if [ "$ENABLE_HTTPS" = "https" ]; then
    SELECTED_TEMPLATE="$NGINX_CONF_TEMPLATE"
fi

if [ ! -f "$SELECTED_TEMPLATE" ]; then
    echo "❌ 错误: Nginx 配置模板不存在: $SELECTED_TEMPLATE"
    exit 1
fi

echo "   📄 拷贝 Nginx 配置文件..."
cp "$SELECTED_TEMPLATE" "$NGINX_CONF_FILE"
echo "   ✅ 配置文件已拷贝到 $NGINX_CONF_FILE"
echo ""

# 确保只使用统一配置文件（删除其他冲突的配置）
echo "📋 步骤 6/6: 应用配置并重启服务..."
echo "   🔗 配置符号链接..."
# 强制创建统一配置的符号链接
ln -sf "$NGINX_CONF_FILE" "$NGINX_SITES_ENABLED/joketop.conf"
# 删除旧的符号链接（如果存在）
rm -f "$NGINX_SITES_ENABLED/docs-code-dojo"
rm -f "$NGINX_SITES_ENABLED/joketop.com"


# 测试 Nginx 配置
echo "   🧪 测试 Nginx 配置..."
if nginx -t 2>&1 | grep -q "successful"; then
    echo "   ✅ 配置测试通过"
    
    # 重启 Nginx
    echo "   🔄 重新加载 Nginx..."
    systemctl reload nginx || systemctl restart nginx
    echo "   ✅ Nginx 已重启"
    
    echo ""
    echo "=========================================="
    echo "  ✅ 部署完成！"
    echo "=========================================="
    echo ""
    echo "📋 文档服务列表:"
    for service_config in "${SERVICES[@]}"; do
        IFS=':' read -r path deploy_dir service_name <<< "$service_config"
        if [ -d "$deploy_dir" ]; then
            if [ "$ENABLE_HTTPS" = "https" ]; then
                echo "   ✅ $service_name: https://$DOMAIN$path"
            else
                echo "   ✅ $service_name: http://$DOMAIN$path"
            fi
        else
            if [ "$ENABLE_HTTPS" = "https" ]; then
                echo "   ⚠️  $service_name: https://$DOMAIN$path (目录不存在: $deploy_dir)"
            else
                echo "   ⚠️  $service_name: http://$DOMAIN$path (目录不存在: $deploy_dir)"
            fi
        fi
    done
    echo ""
    echo "📋 joketop.com 站点:"
    if [ "$ENABLE_HTTPS" = "https" ]; then
        # HTTPS 配置
        echo "   ✅ 主站: https://joketop.com"
        echo "   ✅ 简历: https://me.joketop.com"
        echo "   ✅ 学习站点: https://blog.joketop.com"
        echo "   ✅ 项目展示: https://showcase.joketop.com"
        echo "   ✅ 生活日记: https://diary.joketop.com"
    else
        # HTTP 配置
        echo "   ⚠️  主站: http://joketop.com (需要配置 DNS 和证书)"
        echo "   ⚠️  简历: http://me.joketop.com (需要配置 DNS 和证书)"
        echo "   ⚠️  学习站点: http://blog.joketop.com (需要配置 DNS 和证书)"
        echo "   ⚠️  项目展示: http://showcase.joketop.com (需要配置 DNS 和证书)"
        echo "   ⚠️  生活日记: http://diary.joketop.com (需要配置 DNS 和证书)"
    fi
    echo ""
    
    # 检查文件是否存在
    echo "📋 文件检查:"
    if [ -f "$JOKETOP_DEPLOY_DIR/index.html" ]; then
        echo "   ✅ index.html 存在"
    else
        echo "   ❌ index.html 不存在"
    fi
    if [ -f "$JOKETOP_DEPLOY_DIR/resume.html" ]; then
        echo "   ✅ resume.html 存在"
    else
        echo "   ❌ resume.html 不存在"
    fi
    if [ -f "$JOKETOP_DEPLOY_DIR/learning.html" ]; then
        echo "   ✅ learning.html 存在"
    else
        echo "   ❌ learning.html 不存在"
    fi
    if [ -f "$JOKETOP_DEPLOY_DIR/showcase.html" ]; then
        echo "   ✅ showcase.html 存在"
    else
        echo "   ❌ showcase.html 不存在"
    fi
    if [ -f "$JOKETOP_DEPLOY_DIR/diary.html" ]; then
        echo "   ✅ diary.html 存在"
    else
        echo "   ❌ diary.html 不存在"
    fi
    echo ""
    
    # DNS 配置提示
    if [ "$ENABLE_HTTPS" = "http" ]; then
        echo "💡 DNS 配置提示:"
        echo "   需要在域名服务商配置以下 DNS 记录："
        echo "   - joketop.com → A 记录 → 服务器 IP"
        echo "   - www.joketop.com → A 记录或 CNAME → joketop.com"
        echo "   - me.joketop.com → A 记录 → 服务器 IP"
        echo "   - blog.joketop.com → A 记录 → 服务器 IP（已配置）"
        echo "   - showcase.joketop.com → A 记录 → 服务器 IP"
        echo "   - diary.joketop.com → A 记录 → 服务器 IP"
        echo ""
        echo "💡 配置完 DNS 后，运行以下命令获取所有域名的证书："
        echo "   sudo certbot certonly --nginx --expand \\"
        echo "     -d joketop.com -d www.joketop.com \\"
        echo "     -d me.joketop.com -d blog.joketop.com \\"
        echo "     -d showcase.joketop.com -d diary.joketop.com"
        echo ""
    fi
else
    echo "❌ Nginx 配置测试失败"
    exit 1
fi
