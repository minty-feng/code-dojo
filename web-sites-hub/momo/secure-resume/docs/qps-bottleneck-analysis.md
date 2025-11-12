# QPS 瓶颈分析与优化建议

## 📊 当前架构状态

### 已优化
- ✅ **模板内存缓存**：release 模式下模板已加载到内存
- ✅ **模板读取**：不再有磁盘 I/O 开销

### 当前瓶颈
- ❌ **静态资源**：所有 CSS/JS/图片都走 Actix Web（Nginx location /static/ 被注释）
- ⚠️ **SQLite 数据库**：文件数据库，并发写入有锁竞争
- ⚠️ **Session 管理**：CookieSessionStore（相对较快，但仍有开销）

## 🔍 QPS 瓶颈分析（按影响程度排序）

### 1. 静态资源服务 ⭐⭐⭐⭐⭐ **最大瓶颈**

**当前状态**：
- 所有静态资源（CSS/JS/图片）都通过 Actix Web 返回
- Nginx 的 `location ^~ /static/` 被注释

**影响**：
- **流量占比**：静态资源通常占 70-90% 的请求量
- **带宽消耗**：CSS/JS 文件较大，消耗大量带宽
- **CPU 开销**：Actix Web 需要处理每个静态文件请求
- **并发限制**：占用 Actix Web 的 worker 线程

**数据估算**：
```
假设：
- 每个页面访问：1 个 HTML + 3 个 CSS + 2 个 JS + 1 个 favicon = 7 个请求
- 静态资源占比：6/7 ≈ 86%
- 如果 QPS 是 100，那么：
  - HTML 请求：14 QPS
  - 静态资源：86 QPS（全部走 Actix Web）
```

**优化效果**：
- 启用 Nginx 静态资源服务后，可减少 **70-90%** 的 Actix Web 请求
- 静态资源可被 CDN 缓存，进一步减少源站压力

---

### 2. SQLite 数据库锁竞争 ⭐⭐⭐⭐

**当前状态**：
- 使用 SQLite 文件数据库
- 每次邀请码验证需要：
  1. 查询数据库（读锁）
  2. 更新数据库（写锁）

**影响**：
- **并发写入限制**：SQLite 同一时间只能有一个写操作
- **锁等待**：多个并发验证请求会排队等待
- **文件 I/O**：每次操作都有磁盘 I/O 开销

**代码位置**：
```rust
// verify_invite_code 函数
let db = state.db.lock().unwrap();  // Mutex 锁
// 查询 + 更新操作
```

**数据估算**：
```
SQLite 并发写入性能：
- 单次写入：~1-5ms
- 并发写入：需要排队，延迟增加
- 100 并发验证：可能需要 100-500ms 延迟
```

**优化方案**：
1. **使用连接池**：虽然 SQLite 是单文件，但可以减少锁竞争
2. **异步数据库**：使用 `sqlx` 或 `diesel` 的异步版本
3. **读写分离**：使用 WAL 模式提高并发读性能
4. **升级到 PostgreSQL/MySQL**：如果访问量很大

---

### 3. Session 管理开销 ⭐⭐⭐

**当前状态**：
- 使用 `CookieSessionStore`（基于 Cookie）
- 每次请求都需要：
  1. 解析 Cookie
  2. 验证 Session
  3. 更新 Session（如果需要）

**影响**：
- **CPU 开销**：加密/解密 Cookie
- **网络开销**：Cookie 大小（通常很小）
- **延迟**：每次请求都有 Session 处理时间

**数据估算**：
```
Session 处理时间：
- Cookie 解析：~0.1-0.5ms
- Session 验证：~0.1-0.3ms
- 总计：~0.2-0.8ms/请求
```

**优化方案**：
1. **Redis Session Store**：如果访问量很大，可考虑 Redis
2. **JWT Token**：无状态认证，减少服务器存储
3. **当前方案已足够**：对于个人简历站点，CookieSessionStore 性能足够

---

### 4. HTTP 响应传输 ⭐⭐

**当前状态**：
- HTML 响应大小：~10-50KB
- 静态资源：CSS/JS 文件可能较大

**影响**：
- **带宽限制**：取决于服务器带宽
- **传输时间**：大文件传输需要时间
- **并发连接**：每个请求占用一个连接

**优化方案**：
1. **启用 Gzip 压缩**：可减少 60-80% 传输大小
2. **HTTP/2**：多路复用，减少连接数
3. **CDN**：静态资源走 CDN，减少源站带宽

---

### 5. Actix Web Worker 线程 ⭐⭐

**当前状态**：
- 默认 worker 数量：CPU 核心数
- 每个 worker 处理一个请求

**影响**：
- **并发限制**：worker 数量限制了并发处理能力
- **阻塞风险**：如果某个请求阻塞，占用一个 worker

**优化方案**：
```rust
HttpServer::new(move || { ... })
    .workers(num_cpus::get())  // 使用 CPU 核心数
    .keep_alive(Duration::from_secs(75))  // HTTP keep-alive
```

---

## 📈 相比 CDN 的压力分析

### 当前架构（无 CDN 优化）

```
用户请求
  ↓
CDN（如果配置）
  ↓
Nginx（反向代理）
  ↓
Actix Web（处理所有请求）
  ├── HTML 页面（必须回源，需要 Session）
  ├── CSS 文件（当前也走 Actix Web）❌
  ├── JS 文件（当前也走 Actix Web）❌
  └── 图片文件（当前也走 Actix Web）❌
```

**压力点**：
- **Actix Web**：处理 100% 的请求（包括静态资源）
- **带宽**：所有流量都经过源站
- **CPU**：处理静态文件服务

### 优化后架构（启用 Nginx 静态资源 + CDN）

```
用户请求
  ↓
CDN（缓存静态资源）
  ├── HTML 页面 → 回源（需要 Session）
  ├── CSS/JS/图片 → CDN 缓存 ✅
  └── 如果 CDN 未命中 → Nginx 静态资源 ✅
       └── 如果 Nginx 未命中 → Actix Web（很少）
  ↓
Nginx
  ├── location /static/ → 直接服务静态文件 ✅
  └── location / → 代理到 Actix Web
  ↓
Actix Web（只处理动态请求）
  ├── HTML 页面
  └── API 请求
```

**压力点**：
- **Actix Web**：只处理 10-30% 的请求（HTML + API）
- **Nginx**：处理静态资源（性能更好）
- **CDN**：缓存静态资源，减少 70-90% 的回源请求

---

## 🎯 优化优先级和建议

### 立即优化（效果最显著）⭐⭐⭐⭐⭐

**1. 启用 Nginx 静态资源服务**

```nginx
# 取消注释 joketop.conf 中的配置
location ^~ /static/ {
    root /home/ubuntu/secure-resume;
    expires 7d;
    add_header Cache-Control "public, max-age=604800";
    access_log off;
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}
```

**预期效果**：
- 减少 70-90% 的 Actix Web 请求
- 提升 QPS 能力 3-10 倍
- 减少 CPU 和内存使用

---

### 中期优化（如果访问量增长）⭐⭐⭐⭐

**2. 优化 SQLite 性能**

```rust
// 使用 WAL 模式提高并发读性能
conn.pragma_update(None, "journal_mode", "WAL")?;
conn.pragma_update(None, "synchronous", "NORMAL")?;
```

**预期效果**：
- 提高并发读性能 2-5 倍
- 减少写锁竞争

**3. 启用 HTTP/2 和 Gzip**

```nginx
listen 443 ssl http2;

gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;
gzip_types text/html text/css application/javascript application/json;
```

**预期效果**：
- 减少 60-80% 传输大小
- 减少连接数（HTTP/2 多路复用）

---

### 长期优化（如果访问量很大）⭐⭐⭐

**4. 升级数据库**

- 从 SQLite 升级到 PostgreSQL 或 MySQL
- 使用连接池
- 支持更高的并发写入

**5. 使用 Redis Session Store**

- 如果 Session 成为瓶颈
- 支持分布式部署

---

## 📊 QPS 能力估算

### 当前配置（静态资源走 Actix Web）

| 组件 | 估算 QPS | 说明 |
|------|---------|------|
| Actix Web | 500-2000 | 取决于 CPU 和内存 |
| SQLite 写入 | 50-200 | 受锁竞争限制 |
| 总体 | **50-200** | 受 SQLite 写入限制 |

### 优化后（启用 Nginx 静态资源）

| 组件 | 估算 QPS | 说明 |
|------|---------|------|
| Actix Web（HTML） | 2000-10000 | 只处理 HTML 和 API |
| Nginx（静态资源） | 10000+ | 高性能静态文件服务 |
| SQLite 写入 | 50-200 | 仍然是瓶颈（如果有很多验证请求） |
| 总体 | **200-1000+** | 受 SQLite 写入限制（验证场景） |

### 进一步优化（启用 CDN）

| 组件 | 估算 QPS | 说明 |
|------|---------|------|
| Actix Web（HTML） | 2000-10000 | 只处理 HTML 和 API |
| CDN（静态资源） | 100000+ | CDN 边缘节点处理 |
| 源站总请求 | **200-1000+** | 只处理 HTML 和 API |
| 用户体验 | **100000+** | CDN 提供低延迟访问 |

---

## 🔧 实施步骤

### 第一步：启用 Nginx 静态资源服务（立即）

```bash
# 1. 取消注释 joketop.conf 中的 location ^~ /static/
# 2. 测试配置
sudo nginx -t

# 3. 重新加载 Nginx
sudo systemctl reload nginx

# 4. 验证
curl -I http://127.0.0.1/static/main.css
```

**预期效果**：立即减少 70-90% 的 Actix Web 请求

### 第二步：配置 CDN 缓存规则

在 CDN 控制台配置：
- **不缓存**：`/` 和 `/api/*`（动态内容）
- **缓存 7 天**：`/static/*`（静态资源）

**预期效果**：进一步减少 70-90% 的回源请求

### 第三步：优化 SQLite（如果验证请求很多）

```rust
// 在 init_db 函数中添加
conn.pragma_update(None, "journal_mode", "WAL")?;
conn.pragma_update(None, "synchronous", "NORMAL")?;
conn.pragma_update(None, "cache_size", "-64000")?; // 64MB 缓存
```

---

## 📝 总结

### 当前最大瓶颈

1. **静态资源走 Actix Web**（影响最大）
   - 占 70-90% 的请求量
   - 解决方案：启用 Nginx 静态资源服务

2. **SQLite 写入锁竞争**（如果验证请求多）
   - 限制并发写入能力
   - 解决方案：使用 WAL 模式，或升级数据库

### 相比 CDN 的压力

**当前**：
- 源站处理 100% 请求（包括静态资源）
- 带宽和 CPU 压力大

**优化后**：
- 源站只处理 10-30% 请求（HTML + API）
- CDN 处理 70-90% 请求（静态资源）
- 压力减少 70-90%

### 建议

1. **立即启用 Nginx 静态资源服务**（效果最显著）
2. **配置 CDN 缓存规则**（进一步优化）
3. **监控 SQLite 性能**（如果验证请求很多，再优化）

通过这些优化，QPS 能力可以提升 **3-10 倍**，源站压力减少 **70-90%**。

