# 压测脚本使用指南

## 📋 脚本说明

### 本地测试（需要两个脚本）

**原因**：本地测试时，需要区分是否经过 Nginx

#### 1. `benchmark-local.sh` - 直接访问 Actix Web

**用途**：测试 Actix Web 本身性能（优化前基准）

**测试地址**：`http://127.0.0.1:8080`（直接访问 Actix Web）

**特点**：
- 静态资源由 Actix Web 处理
- 用于建立性能基准
- 在本地或服务器上都可以运行

**使用场景**：
- 测试 Actix Web 本身性能
- 建立优化前的基准数据

**运行**：
```bash
cd /Users/didi/Workspace/code-dojo/web-sites-hub/backend-resume
./scripts/benchmark-local.sh
```

---

#### 2. `benchmark-nginx.sh` - 通过 Nginx 访问

**用途**：测试 Nginx 优化后的性能（优化后）

**测试地址**：`http://127.0.0.1` + Host 头（通过 Nginx）

**特点**：
- 静态资源由 Nginx 直接服务
- 用于测试优化效果
- **必须在服务器上运行**（需要 Nginx）

**使用场景**：
- 测试 Nginx 优化效果
- 对比优化前后性能差异

**运行**：
```bash
# 在服务器上执行
cd /home/ubuntu/code-dojo/web-sites-hub/backend-resume
./scripts/benchmark-nginx.sh
```

---

### 远程测试（一个脚本即可）

#### `benchmark-remote.sh` - 通过域名访问

**用途**：测试生产环境性能

**测试地址**：`https://me.joketop.com`（通过域名，自动经过 Nginx）

**特点**：
- 自动经过 Nginx（如果配置正确）
- 无需区分优化前后
- 同一个脚本即可测试

**使用场景**：
- 验证生产环境配置
- 测试真实网络环境下的表现

**运行**：
```bash
cd /Users/didi/Workspace/code-dojo/web-sites-hub/backend-resume
./scripts/benchmark-remote.sh
```

---

## 🔄 测试流程

### 本地测试流程（对比优化前后）

```bash
# 步骤 1：测试优化前（直接访问 Actix Web）
./scripts/benchmark-local.sh
# 记录结果：QPS、延迟等

# 步骤 2：确保 Nginx 配置已更新
# 在服务器上：
sudo nginx -t
sudo systemctl reload nginx

# 步骤 3：测试优化后（通过 Nginx）
./scripts/benchmark-nginx.sh
# 记录结果：QPS、延迟等

# 步骤 4：对比结果
# 优化前：CSS QPS ~9,500-11,000
# 优化后：CSS QPS 预期 20,000+
```

### 远程测试流程（验证生产环境）

```bash
# 直接运行（自动经过 Nginx）
./scripts/benchmark-remote.sh

# 或使用小规模测试（减少流量消耗）
# 修改脚本参数：THREADS=2 CONNECTIONS=10 DURATION=10s
```

---

## 📊 测试地址对比

| 脚本 | 测试地址 | 是否经过 Nginx | 静态资源处理 |
|------|---------|---------------|-------------|
| `benchmark-local.sh` | `http://127.0.0.1:8080` | ❌ 否 | Actix Web |
| `benchmark-nginx.sh` | `http://127.0.0.1` + Host | ✅ 是 | Nginx |
| `benchmark-remote.sh` | `https://me.joketop.com` | ✅ 是 | Nginx |

---

## ✅ 验证方法

### 验证静态资源是否走 Nginx

```bash
# 在服务器上执行
curl -I -H "Host: me.joketop.com" http://127.0.0.1/static/main.css

# 应该看到：
# Server: nginx
# Cache-Control: public, max-age=604800
```

### 验证直接访问 Actix Web

```bash
curl -I http://127.0.0.1:8080/static/main.css

# 应该看到：
# Server: Actix-Web/4.4.0
# （没有 Cache-Control: public）
```

---

## 🎯 总结

- **本地测试**：需要两个脚本
  - `benchmark-local.sh`：直接访问 Actix Web（基准）
  - `benchmark-nginx.sh`：通过 Nginx（优化后）

- **远程测试**：一个脚本即可
  - `benchmark-remote.sh`：通过域名，自动经过 Nginx

- **关键区别**：
  - 本地：`127.0.0.1:8080` vs `127.0.0.1` + Host 头
  - 远程：域名访问自动经过 Nginx

