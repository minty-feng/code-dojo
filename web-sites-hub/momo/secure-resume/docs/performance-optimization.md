# Secure Resume 源站压力优化方案

## 📊 当前压力分析

### 压力来源
1. **HTML 页面请求**：每次访问都需要回源（无法 CDN 缓存）
2. **模板文件读取**：每次请求都从磁盘读取模板文件
3. **Session 验证**：每次请求都需要查询 session
4. **静态资源**：当前也走 Actix Web（可优化）

### 性能瓶颈
- ❌ 模板文件每次 `fs::read_to_string()` - I/O 开销
- ❌ 所有请求都回源 - 带宽压力
- ❌ 单线程读取文件 - 阻塞风险

## 🚀 优化方案（按优先级排序）

### 方案 1：模板文件内存缓存 ⭐⭐⭐⭐⭐ **最高优先级**

**问题**：每次请求都从磁盘读取模板文件

**优化**：启动时加载到内存，运行时直接使用

**实现**：

```rust
// src/main.rs
use std::sync::Arc;
use once_cell::sync::Lazy;

// 启动时加载模板到内存
static AUTH_TEMPLATE_CACHED: Lazy<String> = Lazy::new(|| {
    fs::read_to_string(AUTH_TEMPLATE)
        .expect("无法读取登录模板")
});

static RESUME_TEMPLATE_CACHED: Lazy<String> = Lazy::new(|| {
    fs::read_to_string(RESUME_TEMPLATE)
        .expect("无法读取简历模板")
});

async fn index(session: Session) -> HttpResponse {
    if let Some(authenticated) = session.get::<bool>("authenticated").unwrap_or(None) {
        if authenticated {
            return no_store_response(HttpResponse::Ok())
                .content_type("text/html; charset=utf-8")
                .body(RESUME_TEMPLATE_CACHED.as_str());
        }
    }

    no_store_response(HttpResponse::Ok())
        .content_type("text/html; charset=utf-8")
        .body(AUTH_TEMPLATE_CACHED.as_str())
}
```

**性能提升**：
- ✅ 消除磁盘 I/O（每次请求节省 ~1-5ms）
- ✅ 减少系统调用
- ✅ 提高并发处理能力

**注意事项**：
- 模板更新需要重启服务（适合个人简历场景）
- 或使用文件监控自动重载（可选）

**Cargo.toml 添加依赖**：
```toml
[dependencies]
once_cell = "1.19"
```

---

### 方案 2：静态资源走 Nginx（立即启用） ⭐⭐⭐⭐⭐

**当前状态**：静态资源也走 Actix Web

**优化**：Nginx 直接服务静态资源，可被 CDN 缓存

**实现**：

```nginx
# joketop.conf
location ^~ /static/ {
    root /home/ubuntu/secure-resume;
    expires 7d;
    add_header Cache-Control "public, max-age=604800";
    access_log off;
    # 启用 gzip
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}

location / {
    proxy_pass http://secure_resume_backend;
    # ... 其他配置
}
```

**性能提升**：
- ✅ 减少 70-90% 的 Actix Web 请求（静态资源占大部分流量）
- ✅ Nginx 处理静态文件性能更好
- ✅ 可被 CDN 缓存，进一步减少源站压力

**实施步骤**：
1. 取消注释 Nginx 的 `location ^~ /static/` 配置
2. 重新加载 Nginx：`sudo systemctl reload nginx`
3. 验证：`curl -I http://127.0.0.1/static/main.css`

---

### 方案 3：优化 Actix Web 配置 ⭐⭐⭐⭐

**优化点**：

```rust
// src/main.rs
HttpServer::new(move || {
    // ... 配置
})
.bind("127.0.0.1:8080")?
.workers(num_cpus::get())  // 使用 CPU 核心数
.keep_alive(Duration::from_secs(75))  // HTTP keep-alive
.client_timeout(5000)  // 客户端超时
.client_disconnect_timeout(1000)  // 断开连接超时
.max_connection_rate(1000)  // 最大连接速率
.run()
.await
```

**Cargo.toml 添加依赖**：
```toml
[dependencies]
num_cpus = "1.16"
```

**性能提升**：
- ✅ 充分利用多核 CPU
- ✅ 减少连接建立开销
- ✅ 提高并发处理能力

---

### 方案 4：Nginx 反向代理缓存（谨慎使用） ⭐⭐⭐

**注意**：由于需要根据 session 返回不同内容，需要特殊配置

**方案 A：只缓存 auth.html（未登录页面）**

```nginx
# 只缓存未登录状态的页面
proxy_cache_path /var/cache/nginx/secure_resume 
    levels=1:2 
    keys_zone=secure_resume_cache:10m 
    max_size=100m 
    inactive=1h 
    use_temp_path=off;

# 在 server 块中
map $cookie_secure_resume_session $cache_key {
    "" $scheme$proxy_host$request_uri;  # 无 session → 可以缓存
    default "";  # 有 session → 不缓存
}

location / {
    # 只有未登录用户才缓存
    proxy_cache secure_resume_cache;
    proxy_cache_key $cache_key;
    proxy_cache_valid 200 5m;  # 缓存 5 分钟
    proxy_cache_bypass $cache_key;  # 有 session 时绕过缓存
    
    proxy_pass http://secure_resume_backend;
    # ... 其他配置
}
```

**优点**：
- ✅ 减少未登录用户的回源请求
- ✅ 大部分访问是未登录状态

**缺点**：
- ⚠️ 配置复杂，容易出错
- ⚠️ 需要仔细测试

---

### 方案 5：使用 CDN 的边缘计算功能 ⭐⭐⭐

**如果 CDN 支持（如 Cloudflare Workers、阿里云 EdgeScript）**：

```javascript
// CDN 边缘脚本示例（伪代码）
addEventListener('fetch', event => {
  const request = event.request;
  const cookie = request.headers.get('Cookie');
  
  // 如果有 session cookie，直接回源
  if (cookie && cookie.includes('secure_resume_session')) {
    return fetch(request);
  }
  
  // 无 session，尝试从缓存返回 auth.html
  return caches.match(request).then(response => {
    if (response) {
      return response;
    }
    return fetch(request).then(response => {
      // 缓存 auth.html
      if (response.status === 200) {
        caches.put(request, response.clone());
      }
      return response;
    });
  });
});
```

**优点**：
- ✅ 在 CDN 边缘处理，减少回源
- ✅ 智能缓存策略

**缺点**：
- ⚠️ 需要 CDN 支持边缘计算
- ⚠️ 配置和维护成本高

---

### 方案 6：优化数据库查询 ⭐⭐

**当前**：SQLite 查询简单，压力不大

**如果未来扩展**：
- 使用连接池
- 添加索引
- 批量查询

---

### 方案 7：HTTP/2 和压缩 ⭐⭐⭐⭐

**Nginx 配置**：

```nginx
# 启用 HTTP/2
listen 443 ssl http2;

# 启用 Brotli 压缩（如果支持）
brotli on;
brotli_comp_level 6;
brotli_types text/html text/css application/javascript image/svg+xml;

# 或使用 gzip
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;
gzip_types text/html text/css application/javascript application/json image/svg+xml;
```

**性能提升**：
- ✅ 减少传输数据量（30-70%）
- ✅ HTTP/2 多路复用，减少连接数

---

## 📈 优化效果预估

### 优化前
- HTML 请求：100% 回源，每次读取磁盘
- 静态资源：100% 回源
- 模板读取：每次 ~1-5ms 磁盘 I/O
- 并发能力：受限于磁盘 I/O

### 优化后（方案 1 + 2 + 3）

| 优化项 | 效果 | 说明 |
|--------|------|------|
| 模板缓存 | 减少 1-5ms/请求 | 消除磁盘 I/O |
| 静态资源 Nginx | 减少 70-90% 请求 | 大部分流量是静态资源 |
| 多 worker | 提升 2-8x 并发 | 取决于 CPU 核心数 |
| HTTP/2 + 压缩 | 减少 30-70% 带宽 | 取决于内容类型 |

**总体效果**：
- ✅ 源站请求减少 **70-90%**（静态资源走 Nginx）
- ✅ 响应时间减少 **1-5ms**（模板缓存）
- ✅ 并发能力提升 **2-8x**（多 worker）
- ✅ 带宽使用减少 **30-70%**（压缩）

---

## 🎯 实施建议

### 第一阶段（立即实施）⭐⭐⭐⭐⭐

1. **模板文件内存缓存**（方案 1）
   - 代码改动小
   - 效果明显
   - 风险低

2. **静态资源走 Nginx**（方案 2）
   - 配置简单
   - 效果显著
   - 风险低

### 第二阶段（性能优化）⭐⭐⭐⭐

3. **优化 Actix Web 配置**（方案 3）
   - 充分利用硬件资源

4. **启用 HTTP/2 和压缩**（方案 7）
   - 减少带宽使用

### 第三阶段（高级优化）⭐⭐⭐

5. **Nginx 反向代理缓存**（方案 4）
   - 需要仔细测试
   - 配置复杂

6. **CDN 边缘计算**（方案 5）
   - 需要 CDN 支持
   - 成本较高

---

## 🔧 实施步骤

### 步骤 1：模板文件内存缓存

```bash
# 1. 修改 Cargo.toml
cd /Users/didi/Workspace/code-dojo/web-sites-hub/momo/secure-resume
# 添加 once_cell 依赖

# 2. 修改 src/main.rs
# 使用 Lazy 静态变量缓存模板

# 3. 编译测试
cargo build --release

# 4. 部署
rsync -av target/release/secure_resume user@server:/home/ubuntu/secure-resume/
```

### 步骤 2：静态资源走 Nginx

```bash
# 1. 修改 joketop.conf
# 取消注释 location ^~ /static/ 配置

# 2. 测试配置
sudo nginx -t

# 3. 重新加载
sudo systemctl reload nginx

# 4. 验证
curl -I http://127.0.0.1/static/main.css
```

### 步骤 3：优化 Actix Web 配置

```bash
# 1. 修改 Cargo.toml
# 添加 num_cpus 依赖

# 2. 修改 src/main.rs
# 添加 workers、keep_alive 等配置

# 3. 编译部署
cargo build --release
rsync -av target/release/secure_resume user@server:/home/ubuntu/secure-resume/
```

---

## 📊 监控和验证

### 性能指标

```bash
# 1. 查看 Actix Web 请求数
tail -f /home/ubuntu/secure-resume/secure-resume.log | grep "GET /"

# 2. 查看 Nginx 访问日志
tail -f /var/log/nginx/me.joketop.com.access.log

# 3. 监控系统资源
htop
# 或
top

# 4. 测试响应时间
time curl -s http://127.0.0.1:8080/ > /dev/null
```

### 压力测试

```bash
# 使用 ab (Apache Bench)
ab -n 1000 -c 10 http://127.0.0.1:8080/

# 使用 wrk
wrk -t4 -c100 -d30s http://127.0.0.1:8080/
```

---

## ⚠️ 注意事项

1. **模板更新**：使用内存缓存后，模板更新需要重启服务
2. **测试充分**：每次优化后都要充分测试
3. **监控指标**：关注错误率、响应时间、资源使用
4. **渐进优化**：不要一次性实施所有优化，逐步验证效果

---

## 📚 参考

- [Actix Web Performance](https://actix.rs/docs/performance/)
- [Nginx Caching Guide](https://www.nginx.com/blog/nginx-caching-guide/)
- [Rust Performance Book](https://nnethercote.github.io/perf-book/)

