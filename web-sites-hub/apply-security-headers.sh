#!/bin/bash
# 为所有站点添加安全头的脚本
# 支持本地开发环境和服务器环境

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 显示帮助信息
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "🔒 应用安全头配置脚本"
    echo ""
    echo "用法: $0 [配置文件路径]"
    echo ""
    echo "说明:"
    echo "  - 如果不提供参数，脚本会自动检测配置文件位置"
    echo "  - 本地开发环境: 使用 web-sites-hub/joketop.conf"
    echo "  - 服务器环境: 使用 /etc/nginx/sites-available/joketop.conf (需要 sudo)"
    echo ""
    echo "示例:"
    echo "  $0                                    # 自动检测"
    echo "  $0 /path/to/joketop.conf             # 指定配置文件"
    echo "  sudo $0                              # 服务器环境"
    exit 0
fi

# 自动检测配置文件位置
# 1. 如果提供了参数，使用参数
# 2. 如果在本地开发环境（web-sites-hub目录存在joketop.conf），使用本地配置
# 3. 否则使用服务器路径
if [ -n "$1" ]; then
    CONFIG_FILE="$1"
elif [ -f "$SCRIPT_DIR/joketop.conf" ]; then
    CONFIG_FILE="$SCRIPT_DIR/joketop.conf"
    echo "📍 检测到本地开发环境，使用: $CONFIG_FILE"
else
    CONFIG_FILE="/etc/nginx/sites-available/joketop.conf"
    echo "📍 使用服务器配置路径: $CONFIG_FILE"
    # 服务器环境需要 root 权限
    if [ "$EUID" -ne 0 ]; then 
        echo "❌ 服务器环境请使用 sudo 运行此脚本"
        exit 1
    fi
fi

# 生成备份文件名
BACKUP_DIR="$(dirname "$CONFIG_FILE")"
BACKUP_FILE="$BACKUP_DIR/joketop.conf.backup.$(date +%Y%m%d_%H%M%S)"

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在: $CONFIG_FILE"
    echo ""
    echo "💡 提示："
    echo "   1. 在本地开发环境，确保在 web-sites-hub 目录下运行"
    echo "   2. 在服务器环境，确保配置文件存在于 /etc/nginx/sites-available/joketop.conf"
    echo "   3. 或手动指定配置文件路径: $0 <config-file-path>"
    exit 1
fi

echo "🔒 应用安全头配置"
echo "=================="
echo "配置文件: $CONFIG_FILE"
echo "备份文件: $BACKUP_FILE"
echo ""

# 备份原配置
echo "📋 备份原配置..."
cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "✅ 备份完成: $BACKUP_FILE"
echo ""

# 安全头配置（添加到每个 HTTPS server 块）
SECURITY_HEADERS='
    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src '\''self'\''; script-src '\''self'\'' '\''unsafe-inline'\'' https://fonts.googleapis.com; style-src '\''self'\'' '\''unsafe-inline'\'' https://fonts.googleapis.com; font-src '\''self'\'' https://fonts.gstatic.com; img-src '\''self'\'' data: https:; connect-src '\''self'\'';" always;'

# 文件访问限制配置
FILE_RESTRICTIONS='
    
    # 禁止访问隐藏文件和敏感文件
    location ~ /\.(git|htaccess|env|DS_Store|gitignore) {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # 禁止访问源码文件（如果误上传）
    location ~ \.(py|php|rb|java|go|rs|sh)$ {
        deny all;
        access_log off;
        log_not_found off;
    }'

# 使用 Python 脚本处理配置（更可靠）
python3 << PYTHON_SCRIPT
import re
import sys
from datetime import datetime

config_file = "$CONFIG_FILE"

# 读取配置
with open(config_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 安全头配置
security_headers = '''
    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://fonts.googleapis.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self';" always;'''

# 文件访问限制
file_restrictions = '''
    
    # 禁止访问隐藏文件和敏感文件
    location ~ /\.(git|htaccess|env|DS_Store|gitignore) {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # 禁止访问源码文件（如果误上传）
    location ~ \.(py|php|rb|java|go|rs|sh)$ {
        deny all;
        access_log off;
        log_not_found off;
    }'''

# 检查是否已经添加了安全头
if "Strict-Transport-Security" in content:
    print("⚠️  检测到配置中已存在安全头，跳过添加")
    sys.exit(0)

# 为每个 HTTPS server 块添加安全头
# 匹配模式：server { ... listen 443 ... }
pattern = r'(server\s*\{[^}]*listen\s+443[^}]*ssl_protocols[^}]*ssl_prefer_server_ciphers\s+on;\s*)(?=\n)'

def add_security_headers(match):
    server_block = match.group(1)
    # 检查是否已有安全头
    if "Strict-Transport-Security" not in server_block:
        # 在 ssl_prefer_server_ciphers on; 后添加安全头
        server_block = re.sub(
            r'(ssl_prefer_server_ciphers\s+on;\s*)',
            r'\1' + security_headers + '\n',
            server_block
        )
    return server_block

content = re.sub(pattern, add_security_headers, content, flags=re.MULTILINE | re.DOTALL)

# 为 joketop.com 主站添加文件访问限制（如果还没有）
if "joketop.com www.joketop.com" in content:
    # 在 location / { 之前添加文件限制
    pattern = r'(server_name joketop\.com www\.joketop\.com;[^}]*?)(location\s+/\s*\{)'
    if "禁止访问隐藏文件" not in content:
        content = re.sub(
            pattern,
            r'\1' + file_restrictions + '\n    \2',
            content,
            flags=re.DOTALL
        )

# 写回文件
with open(config_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 安全头配置已添加")
PYTHON_SCRIPT

if [ $? -eq 0 ]; then
    echo ""
    # 检查是否在服务器环境（有nginx命令且需要root权限）
    if command -v nginx &> /dev/null && [ "$EUID" -eq 0 ]; then
        echo "🧪 测试 Nginx 配置..."
        if nginx -t; then
            echo ""
            echo "✅ 配置测试通过！"
            echo ""
            read -p "是否立即重载 Nginx 配置？(y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                systemctl reload nginx
                echo "✅ Nginx 配置已重载"
            else
                echo "💡 稍后请运行: sudo systemctl reload nginx"
            fi
        else
            echo ""
            echo "❌ 配置测试失败！"
            echo "📋 正在恢复备份..."
            cp "$BACKUP_FILE" "$CONFIG_FILE"
            echo "✅ 已恢复原配置"
            exit 1
        fi
    else
        echo "✅ 配置已更新（本地开发环境）"
        echo ""
        echo "💡 下一步："
        echo "   1. 检查配置文件: $CONFIG_FILE"
        echo "   2. 将更新后的配置部署到服务器"
        echo "   3. 在服务器上运行: sudo nginx -t && sudo systemctl reload nginx"
    fi
else
    echo "❌ 脚本执行失败"
    exit 1
fi

echo ""
echo "✅ 完成！"
echo ""
echo "📋 已应用的安全措施："
echo "   - Strict-Transport-Security (HSTS)"
echo "   - X-Frame-Options"
echo "   - X-Content-Type-Options"
echo "   - X-XSS-Protection"
echo "   - Referrer-Policy"
echo "   - Content-Security-Policy (CSP)"
echo "   - 文件访问限制"
echo ""
echo "📖 详细说明请查看: web-sites-hub/frontend-portal/SECURITY-GUIDE.md"

