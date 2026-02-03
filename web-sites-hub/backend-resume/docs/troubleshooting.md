# Secure Resume 故障排查指南

## 问题：CDN 缓存导致静态资源或页面未更新

**症状**：直接访问源站正常，但通过 CDN 访问时显示旧内容或样式未生效

**快速诊断**：
```bash
# 1. 直接访问源站（绕过 CDN）
curl -H "Host: me.joketop.com" http://服务器IP/static/main.css

# 2. 通过 CDN 访问
curl https://me.joketop.com/static/main.css

# 3. 对比内容是否一致
```

**解决方案**：

### 方案 1：清除 CDN 缓存（推荐）

如果使用 EO DNS 或其他 CDN 服务：

1. **登录 CDN 控制台**
   - 找到 `me.joketop.com` 的缓存配置
   - 执行"清除缓存"或"刷新缓存"操作

2. **清除特定路径缓存**
   - 清除 `/static/*` 路径的缓存
   - 清除 `/` 路径的缓存（如果 HTML 也被缓存）

3. **等待缓存过期**
   - 检查 CDN 的缓存时间设置
   - 等待 TTL 过期后自动更新

### 方案 2：配置 CDN 不缓存特定路径

在 CDN 控制台中配置缓存规则：

- **不缓存路径**：
  - `/` - 主页面（动态内容）
  - `/api/*` - API 接口（动态内容）
  
- **缓存路径**（可选，等调试通后再启用）：
  - `/static/*` - 静态资源（CSS/JS/图片）

### 方案 3：临时绕过 CDN 测试

**方法 A：修改本地 hosts 文件**

```bash
# 在本地机器上执行
# 1. 获取服务器 IP（从 SSH 连接信息或服务器管理面板）
# 2. 编辑 hosts 文件

# Mac/Linux
sudo vim /etc/hosts

# Windows
# 以管理员身份编辑 C:\Windows\System32\drivers\etc\hosts

# 添加一行（替换 SERVER_IP 为实际服务器 IP）
SERVER_IP me.joketop.com
```

**方法 B：直接通过 IP 访问（需要配置 Nginx SNI）**

```bash
# 在服务器上检查 Nginx 是否支持 SNI
curl -k -H "Host: me.joketop.com" https://服务器IP/
```

### 方案 4：修改 DNS 记录临时指向源站

1. **在 DNS 控制台修改 CNAME 记录**
   - 将 `me` 的 CNAME 从 `me.joketop.com.eo.dnse2.com.` 改为 A 记录
   - 指向服务器 IP 地址
   - 等待 DNS 传播（通常几分钟到几小时）

2. **测试完成后恢复 CDN**
   - 测试确认正常后，改回 CNAME 记录
   - 配置 CDN 缓存规则

### 验证步骤

```bash
# 1. 清除浏览器缓存
# 浏览器中按 Ctrl+Shift+Delete (Windows) 或 Cmd+Shift+Delete (Mac)
# 清除缓存和 Cookie

# 2. 无痕模式测试
# 打开浏览器无痕/隐私模式访问 https://me.joketop.com

# 3. 检查响应头
curl -I https://me.joketop.com/static/main.css
# 查看 Cache-Control、CDN-Cache-Status 等头部

# 4. 对比源站和 CDN 的响应
# 源站
curl -H "Host: me.joketop.com" http://服务器IP/static/main.css > source.css

# CDN
curl https://me.joketop.com/static/main.css > cdn.css

# 对比
diff source.css cdn.css
```

---

## 问题：访问 me.joketop.com 显示 Nginx 默认页面

**快速排查脚本：**

```bash
# 上传并运行检查脚本
cd /home/ubuntu/code-dojo/web-sites-hub/backend-resume
chmod +x scripts/check-nginx-config.sh
./scripts/check-nginx-config.sh
```

### 1. 检查 Nginx 配置是否正确加载

```bash
# 测试配置文件语法
sudo nginx -t

# 查看当前生效的配置
sudo nginx -T | grep -A 20 "server_name me.joketop.com"
```

**预期结果**：应该看到 `location /` 中有 `proxy_pass http://secure_resume_backend;`

### 2. 检查配置是否已部署

```bash
# 检查配置文件是否存在
ls -la /etc/nginx/sites-enabled/joketop.conf

# 检查符号链接是否正确
readlink -f /etc/nginx/sites-enabled/joketop.conf

# 如果配置已更新但未生效，重新加载 Nginx
sudo systemctl reload nginx
# 或
sudo nginx -s reload
```

### 3. 检查 secure-resume 服务是否运行

```bash
# 检查进程是否运行
ps aux | grep secure_resume

# 检查端口是否监听
sudo netstat -tlnp | grep 8080
# 或
sudo ss -tlnp | grep 8080
# 或
sudo lsof -i :8080
```

**预期结果**：应该看到 `127.0.0.1:8080` 在监听

### 4. 测试服务是否可访问

```bash
# 直接测试后端服务
curl -v http://127.0.0.1:8080/

# 测试 API
curl http://127.0.0.1:8080/api/stats
```

**预期结果**：应该返回 HTML 或 JSON 响应，而不是连接拒绝

### 5. 检查 Nginx 错误日志

```bash
# 查看错误日志
sudo tail -f /var/log/nginx/me.joketop.com.error.log

# 查看访问日志
sudo tail -f /var/log/nginx/me.joketop.com.access.log
```

**常见错误**：
- `connect() failed (111: Connection refused)` - 后端服务未启动
- `upstream not found` - upstream 配置错误
- `502 Bad Gateway` - 后端服务无响应

### 6. 检查 upstream 配置

```bash
# 查看 upstream 定义
sudo nginx -T | grep -A 5 "upstream secure_resume_backend"
```

**预期结果**：
```nginx
upstream secure_resume_backend {
    keepalive 32;
    server 127.0.0.1:8080;
}
```

### 7. 检查防火墙

```bash
# 检查本地端口是否可访问（应该可以，因为是 127.0.0.1）
curl http://127.0.0.1:8080/

# 检查防火墙规则（8080 应该只允许本地访问）
sudo ufw status | grep 8080
```

### 8. 完整排查流程

```bash
# 1. 检查服务状态
cd /home/ubuntu/secure-resume
ps aux | grep secure_resume || echo "服务未运行"

# 2. 如果服务未运行，启动服务
SECURE_RESUME_SECURE_COOKIE=1 RUST_LOG=info nohup ./secure_resume > secure-resume.log 2>&1 &
echo $! > secure-resume.pid

# 3. 等待几秒后检查
sleep 2
curl http://127.0.0.1:8080/api/stats

# 4. 检查 Nginx 配置
sudo nginx -t

# 5. 重新加载 Nginx
sudo systemctl reload nginx

# 6. 测试访问
curl -H "Host: me.joketop.com" http://127.0.0.1/
```

### 9. 常见问题及解决方案

#### 问题 1：配置已更新但仍显示 Nginx 默认页面

**症状**：配置文件中 `location /` 已正确配置 `proxy_pass`，但访问仍显示默认页面

**可能原因及解决**：

1. **Nginx 配置未重新加载**
   ```bash
   # 重新加载配置（推荐，不中断服务）
   sudo systemctl reload nginx
   
   # 或重启（会短暂中断）
   sudo systemctl restart nginx
   ```

2. **有其他配置文件覆盖**
   ```bash
   # 检查所有启用的配置
   ls -la /etc/nginx/sites-enabled/
   
   # 检查是否有 default_server
   sudo nginx -T | grep -B 5 "default_server"
   
   # 检查 conf.d 目录
   ls -la /etc/nginx/conf.d/
   ```

3. **CDN 缓存了旧响应**
   - 清除浏览器缓存（Ctrl+Shift+Delete）
   - 在 CDN 控制台清除缓存
   - 使用无痕模式访问测试

4. **server_name 匹配问题**
   ```bash
   # 检查 server_name 是否正确
   sudo nginx -T | grep -A 5 "server_name me.joketop.com"
   
   # 测试直接访问（绕过 CDN）
   curl -H "Host: me.joketop.com" http://127.0.0.1/ -v
   ```

5. **配置文件优先级问题**
   ```bash
   # 确保 joketop.conf 是唯一匹配的配置
   sudo nginx -T | grep -B 2 "listen.*443" | grep "server_name\|listen"
   
   # 如果有多个配置，检查加载顺序
   ls -la /etc/nginx/sites-enabled/ | sort
   ```

**完整排查流程：**
```bash
# 1. 确认配置已更新
sudo nginx -T | grep -A 20 "server_name me.joketop.com" | grep -A 15 "location /"

# 2. 确认 upstream 存在
sudo nginx -T | grep -A 3 "upstream secure_resume_backend"

# 3. 测试后端服务
curl http://127.0.0.1:8080/api/stats

# 4. 重新加载 Nginx
sudo systemctl reload nginx

# 5. 测试通过 Nginx 访问
curl -H "Host: me.joketop.com" http://127.0.0.1/ -v

# 6. 查看错误日志
sudo tail -20 /var/log/nginx/me.joketop.com.error.log
```

#### 问题 2：显示 Nginx 默认页面（配置未更新）

**原因**：`location /` 配置为静态文件而非反向代理

**解决**：确保 `location /` 中有 `proxy_pass http://secure_resume_backend;`

#### 问题 3：502 Bad Gateway

**原因**：后端服务未启动或端口不匹配

**解决**：
```bash
# 检查服务是否运行
ps aux | grep secure_resume

# 检查端口
sudo lsof -i :8080

# 如果未运行，启动服务
cd /home/ubuntu/secure-resume
SECURE_RESUME_SECURE_COOKIE=1 RUST_LOG=info ./secure_resume
```

#### 问题 4：连接超时

**原因**：防火墙阻止或服务监听地址错误

**解决**：
- 确保服务监听 `127.0.0.1:8080`（不是 `0.0.0.0:8080`）
- 检查防火墙规则

#### 问题 5：CSS/JS 静态资源未加载

**症状**：页面显示正常但样式未生效，浏览器控制台显示 404 错误

**排查步骤：**

```bash
# 1. 检查静态文件是否存在
ls -la /home/ubuntu/secure-resume/static/

# 2. 检查文件权限
ls -la /home/ubuntu/secure-resume/static/*.css
ls -la /home/ubuntu/secure-resume/static/*.js

# 3. 测试 Nginx 是否能访问静态文件
curl -I http://127.0.0.1/static/main.css
curl -I http://127.0.0.1/static/resume.css

# 4. 检查 Nginx 错误日志
sudo tail -20 /var/log/nginx/me.joketop.com.error.log | grep static

# 5. 检查 location /static/ 配置
sudo nginx -T | grep -A 10 "location /static/"
```

**常见原因及解决：**

1. **文件不存在**
   ```bash
   # 确保文件已同步到服务器
   ls -la /home/ubuntu/secure-resume/static/main.css
   ls -la /home/ubuntu/secure-resume/static/resume.css
   ```

2. **文件权限问题**
   ```bash
   # 确保 Nginx 可以读取文件
   sudo chmod -R 644 /home/ubuntu/secure-resume/static/*
   sudo chown -R www-data:www-data /home/ubuntu/secure-resume/static/
   ```

3. **Nginx 路径配置问题**
   ```bash
   # 检查配置中的路径
   sudo nginx -T | grep -A 5 "location /static/"
   
   # 确保目录存在
   ls -ld /home/ubuntu/secure-resume/static/
   ```

   **配置说明**：
   - 使用 `root` 时：`location /static/` + `root /home/ubuntu/secure-resume` → 查找 `/home/ubuntu/secure-resume/static/main.css`
   - 使用 `alias` 时：`location /static/` + `alias /home/ubuntu/secure-resume/static/` → 查找 `/home/ubuntu/secure-resume/static/main.css`
   - 推荐使用 `root`，更简单可靠

4. **location 优先级问题**
   - 确保 `location /static/` 在 `location /` 之前
   - 使用 `^~` 前缀确保优先匹配：
     ```nginx
     location ^~ /static/ {
         root /home/ubuntu/secure-resume;
         expires 7d;
         add_header Cache-Control "public, max-age=604800";
     }
     ```

#### 问题 6：配置更新后不生效

**解决**：
```bash
# 测试配置
sudo nginx -t

# 重新加载（不中断服务）
sudo systemctl reload nginx

# 或重启（会短暂中断）
sudo systemctl restart nginx
```

### 10. 验证配置正确的完整检查清单

- [ ] `sudo nginx -t` 通过
- [ ] `/etc/nginx/sites-enabled/joketop.conf` 存在且正确
- [ ] `upstream secure_resume_backend` 指向 `127.0.0.1:8080`
- [ ] `location /` 中有 `proxy_pass http://secure_resume_backend;`
- [ ] `secure_resume` 进程正在运行
- [ ] 端口 8080 正在监听 `127.0.0.1:8080`
- [ ] `curl http://127.0.0.1:8080/api/stats` 返回 JSON
- [ ] Nginx 错误日志无异常
- [ ] 已执行 `sudo systemctl reload nginx`

### 11. 快速修复命令

如果确认是配置问题，可以快速修复：

```bash
# 1. 更新配置文件（如果已修改）
cd /home/ubuntu/code-dojo/web-sites-hub
sudo cp joketop.conf /etc/nginx/sites-available/joketop.conf
sudo ln -sf /etc/nginx/sites-available/joketop.conf /etc/nginx/sites-enabled/joketop.conf

# 2. 测试配置
sudo nginx -t

# 3. 重新加载
sudo systemctl reload nginx

# 4. 检查服务
curl http://127.0.0.1:8080/api/stats
```

