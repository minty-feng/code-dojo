# 安全头配置脚本使用说明

## 概述

`apply-security-headers.sh` 脚本用于为 Nginx 配置文件自动添加安全头和文件访问限制。

## 功能

- ✅ 自动检测本地开发环境或服务器环境
- ✅ 为所有 HTTPS server 块添加安全头
- ✅ 添加文件访问限制（禁止访问隐藏文件和源码文件）
- ✅ 自动备份原配置文件
- ✅ 测试配置有效性（服务器环境）

## 使用方法

### 1. 本地开发环境

在 `web-sites-hub` 目录下运行：

```bash
cd /Users/didi/Workspace/code-dojo/web-sites-hub
./apply-security-headers.sh
```

脚本会自动检测到 `joketop.conf` 文件并使用它。

### 2. 服务器环境

在服务器上运行（需要 root 权限）：

```bash
sudo ./apply-security-headers.sh
```

脚本会自动使用 `/etc/nginx/sites-available/joketop.conf`。

### 3. 指定配置文件路径

```bash
./apply-security-headers.sh /path/to/joketop.conf
```

### 4. 查看帮助

```bash
./apply-security-headers.sh --help
```

## 添加的安全措施

### 安全头

- **Strict-Transport-Security (HSTS)**: 强制使用 HTTPS
- **X-Frame-Options**: 防止点击劫持
- **X-Content-Type-Options**: 防止 MIME 类型嗅探
- **X-XSS-Protection**: XSS 保护
- **Referrer-Policy**: 控制 referrer 信息
- **Content-Security-Policy (CSP)**: 内容安全策略，防止 XSS 攻击

### 文件访问限制

- 禁止访问隐藏文件（`.git`, `.env`, `.htaccess` 等）
- 禁止访问源码文件（`.py`, `.php`, `.sh` 等）

## 工作流程

1. **检测环境**: 自动检测是本地还是服务器环境
2. **备份配置**: 自动创建带时间戳的备份文件
3. **添加安全头**: 为所有 HTTPS server 块添加安全头
4. **添加文件限制**: 为 joketop.com 主站添加文件访问限制
5. **测试配置**: 在服务器环境测试 Nginx 配置
6. **重载配置**: 询问是否立即重载 Nginx（服务器环境）

## 注意事项

1. **备份文件**: 脚本会自动创建备份，格式为 `joketop.conf.backup.YYYYMMDD_HHMMSS`
2. **重复运行**: 如果检测到已存在安全头，脚本会跳过添加
3. **本地环境**: 在本地环境运行后，需要手动将配置部署到服务器
4. **服务器环境**: 需要 root 权限才能修改服务器配置文件

## 部署流程

### 本地开发 → 服务器部署

1. **在本地运行脚本**:
   ```bash
   cd web-sites-hub
   ./apply-security-headers.sh
   ```

2. **检查修改后的配置**:
   ```bash
   git diff joketop.conf
   ```

3. **提交更改**:
   ```bash
   git add joketop.conf
   git commit -m "添加安全头和文件访问限制"
   git push
   ```

4. **在服务器上部署**:
   ```bash
   # 拉取最新配置
   cd /path/to/web-sites-hub
   git pull
   
   # 复制配置到 Nginx
   sudo cp joketop.conf /etc/nginx/sites-available/joketop.conf
   
   # 测试并重载
   sudo nginx -t && sudo systemctl reload nginx
   ```

### 直接在服务器上运行

```bash
# 在服务器上
cd /path/to/web-sites-hub
sudo ./apply-security-headers.sh
```

## 相关文件

- `joketop.conf` - Nginx 配置文件
- `SECURITY-GUIDE.md` - 详细的安全加固指南
- `apply-security-headers.sh` - 安全头配置脚本

## 故障排除

### 问题：配置文件不存在

**解决方案**:
- 确保在正确的目录下运行脚本
- 或使用 `--help` 查看帮助信息
- 或手动指定配置文件路径

### 问题：权限不足

**解决方案**:
- 在服务器环境使用 `sudo` 运行
- 在本地环境确保有文件读写权限

### 问题：配置测试失败

**解决方案**:
- 脚本会自动恢复备份
- 检查 Nginx 配置语法: `sudo nginx -t`
- 查看错误日志: `sudo tail -f /var/log/nginx/error.log`

## 示例输出

```
🔒 应用安全头配置
==================
📍 检测到本地开发环境，使用: /Users/didi/Workspace/code-dojo/web-sites-hub/joketop.conf
配置文件: /Users/didi/Workspace/code-dojo/web-sites-hub/joketop.conf
备份文件: /Users/didi/Workspace/code-dojo/web-sites-hub/joketop.conf.backup.20241118_223045

📋 备份原配置...
✅ 备份完成: /Users/didi/Workspace/code-dojo/web-sites-hub/joketop.conf.backup.20241118_223045

✅ 安全头配置已添加

✅ 配置已更新（本地开发环境）

💡 下一步：
   1. 检查配置文件: /Users/didi/Workspace/code-dojo/web-sites-hub/joketop.conf
   2. 将更新后的配置部署到服务器
   3. 在服务器上运行: sudo nginx -t && sudo systemctl reload nginx

✅ 完成！

📋 已应用的安全措施：
   - Strict-Transport-Security (HSTS)
   - X-Frame-Options
   - X-Content-Type-Options
   - X-XSS-Protection
   - Referrer-Policy
   - Content-Security-Policy (CSP)
   - 文件访问限制
```




