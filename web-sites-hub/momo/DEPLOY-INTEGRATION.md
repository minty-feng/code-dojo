# 集成部署指南

## 部署流程（推荐）

### 一键集成部署

`deploy-joketop.sh` 脚本会自动解压 gz 包并调用 `deploy-all-docs.sh` 一起部署。

#### 1. 本地打包
```bash
cd /Users/didi/Workspace/momo
./package-joketop.sh
```

#### 2. 上传到服务器
```bash
# 上传压缩包和部署脚本
scp joketop-*.tar.gz deploy-joketop.sh user@server:/tmp/
```

#### 3. 在服务器上执行集成部署
```bash
# SSH 到服务器
ssh user@server

# 进入临时目录
cd /tmp

# 赋予执行权限
chmod +x deploy-joketop.sh

# 执行部署（会自动调用 deploy-all-docs.sh）
sudo ./deploy-joketop.sh joketop-*.tar.gz
```

部署过程中会提示：
- 是否部署文档服务（y/n）
- 是否启用 HTTPS（y/n）
- 如果启用 HTTPS，需要输入邮箱地址

### 分步部署（手动控制）

如果需要分别控制主站和文档服务的部署：

#### 1. 打包主站文件
```bash
cd /Users/didi/Workspace/momo
./package-joketop.sh
```

#### 2. 上传并部署主站
```bash
# 上传到服务器
scp joketop-*.tar.gz deploy-joketop.sh user@server:/tmp/

# SSH 到服务器
ssh user@server

# 部署主站（选择不部署文档服务）
cd /tmp
sudo ./deploy-joketop.sh joketop-*.tar.gz
# 当提示"是否现在部署文档服务？"时，选择 n
```

#### 3. 单独部署文档服务
```bash
# 在服务器上
cd /path/to/code-dojo/sphinx-docs
sudo ./deploy-all-docs.sh

# 或使用 SSL
sudo ./deploy-all-docs.sh --letsencrypt --email riseat7am@gmail.com
```

## 配置说明

### blog.joketop.com 的使用

`blog.joketop.com` 域名在两个配置中都有使用，但路径不同，不会冲突：

1. **主站配置** (`/etc/nginx/sites-available/joketop.com`)
   - 根路径 `/` → `learning.html` (学习站点导航)

2. **文档服务配置** (`/etc/nginx/sites-available/docs-code-dojo`)
   - `/backend/` → 后端文档
   - `/frontend/` → 前端文档
   - `/ds/` → 数据结构文档
   - `/algo/` → 算法文档
   - `/os/` → 操作系统文档

### 配置优先级

Nginx 会按照以下顺序匹配：
1. 精确路径匹配（如 `/backend/`）
2. 前缀匹配（如 `/`）

因此：
- `blog.joketop.com/backend/` → 文档服务
- `blog.joketop.com/frontend/` → 文档服务
- `blog.joketop.com/` → 学习站点导航

**两个配置可以共存，不会冲突！**

### 脚本路径查找

`deploy-joketop.sh` 会自动查找 `deploy-all-docs.sh` 脚本，按以下顺序尝试：
1. `../code-dojo/sphinx-docs/deploy-all-docs.sh`（相对路径）
2. `/var/www/code-dojo/sphinx-docs/deploy-all-docs.sh`（服务器常见路径）
3. 脚本所在目录的相对路径

如果找不到脚本，会跳过文档服务部署，但主站部署会正常完成。

## 验证部署

部署完成后，访问以下地址验证：

- 主站：http://joketop.com
- 简历：http://me.joketop.com
- 学习站点导航：http://blog.joketop.com
- 后端文档：http://blog.joketop.com/backend/
- 前端文档：http://blog.joketop.com/frontend/
- 数据结构文档：http://blog.joketop.com/ds/
- 算法文档：http://blog.joketop.com/algo/
- 操作系统文档：http://blog.joketop.com/os/

## 注意事项

1. **配置顺序**：先部署主站，再部署文档服务
2. **SSL 证书**：两个配置可以共享同一个 SSL 证书（如果使用同一个域名）
3. **Nginx 测试**：每次更新配置后都要运行 `nginx -t` 测试
4. **备份**：部署前会自动备份现有文件

