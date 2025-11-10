# 统一文档部署脚本使用说明

## 概述

`deploy-all-docs.sh` 是一个统一的部署脚本，可以同时部署多个文档服务到 Nginx，无需单独部署每个服务。

## 核心文件

1. **joketop.conf** - Nginx 配置文件（239行）
   - 包含所有域名和服务的 HTTPS 配置
   - 可直接编辑，无需处理 shell 转义

2. **joketop-letsencrypt-temp.conf** - Let's Encrypt 临时配置（37行）
   - 用于证书获取时的 HTTP 验证
   - 一般不需要修改

3. **deploy-all-docs.sh** - 部署脚本（374行）
   - 完全无 EOF，简洁高效
   - 只负责拷贝配置和重启服务

## 功能特点

- ✅ 配置和脚本分离，易于维护
- ✅ 统一管理所有文档服务
- ✅ 支持 HTTP 和 HTTPS 部署
- ✅ 支持 Let's Encrypt 自动证书
- ✅ 简单易用，一个命令完成所有部署

## 使用方法

### 1. HTTP 部署

```bash
sudo ./deploy-all-docs.sh
```

### 2. HTTPS 部署（Let's Encrypt）

```bash
sudo ./deploy-all-docs.sh --letsencrypt --email riseat7am@gmail.com
```

### 3. HTTPS 部署（手动证书）

```bash
sudo ./deploy-all-docs.sh --cert /path/to/cert.pem --key /path/to/key.pem
```

## 修改配置

### 添加新服务

编辑 `joketop.conf` 文件，在 blog.joketop.com 的 HTTPS server 块中添加新的 location：

```nginx
# New Service
location ^~ /newservice/ {
    alias /var/www/html/newservice/;
    index index.html;
    try_files $uri $uri/ $uri/index.html =404;
}

location = /newservice {
    return 301 $scheme://$server_name/newservice/;
}
```

**注意事项：**
- 必须使用 `^~` 修饰符（优先匹配，避免被正则拦截）
- location 块必须在 `server { }` 内部
- alias 路径必须以 `/` 结尾

### 修改服务目录

同时需要更新 `deploy-all-docs.sh` 中的 `SERVICES` 数组：

```bash
declare -a SERVICES=(
    "/backend:/var/www/html/honey-backend-dojo:Backend Tutorial"
    "/newservice:/var/www/html/newservice:New Service"
    ...
)
```

## 部署流程

脚本执行6个步骤：

1. **步骤 1/6: 检查服务目录** - 验证所有服务目录是否存在
2. **步骤 2/6: 配置 SSL 证书** - 安装 certbot，创建临时配置
3. **步骤 3/6: 获取 SSL 证书** - 使用 Let's Encrypt 获取证书
4. **步骤 4/6: 检查证书状态** - 验证证书是否成功获取
5. **步骤 5/6: 部署 Nginx 配置** - 拷贝 `joketop.conf` 到 Nginx 目录
6. **步骤 6/6: 应用配置并重启服务** - 测试配置并重启 Nginx

## 注意事项

1. ✅ 需要 root 权限运行（使用 `sudo`）
2. ✅ 配置文件已优化，使用 `^~` 修饰符确保正确匹配
3. ✅ 如果使用 Let's Encrypt，确保域名 DNS 已正确配置
4. ✅ 脚本会自动创建符号链接到 `/etc/nginx/sites-enabled/joketop.conf`
5. ✅ 不再生成配置，直接拷贝 `joketop.conf`

## 故障排除

### 配置测试失败

```bash
# 手动测试 Nginx 配置
sudo nginx -t

# 查看详细错误信息
sudo nginx -T
```

### 服务无法访问

1. 检查服务目录是否存在
2. 检查目录权限
3. 查看 Nginx 错误日志：`sudo tail -f /var/log/nginx/error.log`

### 证书问题

```bash
# 检查 Let's Encrypt 证书
sudo certbot certificates

# 手动续期证书
sudo certbot renew
```

## 与单独部署脚本的区别

- **统一部署脚本**：一个脚本管理所有服务，配置简单，适合统一管理
- **单独部署脚本**：每个服务有独立的脚本，适合单独部署和更新

## 推荐使用场景

- ✅ 首次部署所有服务
- ✅ 需要统一管理所有服务
- ✅ 批量更新配置
- ✅ 简化部署流程

