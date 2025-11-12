# Secure Resume CDN 策略分析

## 📋 页面概览

### 1. `auth.html` - 登录页面
- **路径**：`/` (未登录状态)
- **内容**：静态 HTML 模板 + JavaScript
- **功能**：邀请码验证表单
- **访问控制**：公开访问（无需登录）

### 2. `resume.html` - 简历展示页面
- **路径**：`/` (已登录状态)
- **内容**：静态 HTML 模板 + JavaScript
- **功能**：展示完整简历内容
- **访问控制**：需要登录（基于 session）

## 🔍 技术特点分析

### 动态路由逻辑

```rust
async fn index(session: Session) -> HttpResponse {
    if let Some(authenticated) = session.get::<bool>("authenticated") {
        if authenticated {
            return resume.html;  // 已登录 → 显示简历
        }
    }
    return auth.html;  // 未登录 → 显示登录页
}
```

**关键点**：
- 同一个路径 `/` 根据 session 状态返回不同内容
- 后端已设置 `Cache-Control: no-store`（禁止缓存）

### 缓存控制

```rust
fn no_store_response(mut builder: HttpResponseBuilder) -> HttpResponseBuilder {
    builder.insert_header((CACHE_CONTROL, "no-store, no-cache, must-revalidate"));
    builder.insert_header((PRAGMA, "no-cache"));
    builder.insert_header((EXPIRES, "0"));
    builder
}
```

## ❌ **结论：HTML 页面不应该使用 CDN**

### 理由 1：动态内容分发问题 ⚠️

**问题**：
- 同一个 URL (`/`) 根据用户 session 状态返回不同内容
- CDN 无法区分用户状态，会缓存第一个请求的响应
- 导致：
  - 已登录用户可能看到登录页面（如果 CDN 缓存了未登录状态）
  - 未登录用户可能看到简历页面（如果 CDN 缓存了已登录状态）

**示例场景**：
```
1. 用户 A（未登录）访问 → CDN 缓存 auth.html
2. 用户 B（已登录）访问 → CDN 返回缓存的 auth.html ❌
3. 用户 B 看到登录页面，但实际已登录，体验混乱
```

### 理由 2：安全风险 🔒

**风险**：
- 如果 CDN 缓存了 `resume.html`，未授权用户可能通过缓存访问到简历内容
- 即使设置了 `Cache-Control: no-store`，某些 CDN 可能不严格遵守
- Session 验证被绕过，安全机制失效

### 理由 3：缓存控制冲突 ⚡

**冲突**：
- 后端明确设置了 `Cache-Control: no-store`
- 使用 CDN 缓存与后端意图冲突
- 即使 CDN 支持 `no-store`，也会增加不必要的复杂性

### 理由 4：更新延迟问题 📅

**问题**：
- 页面内容更新后，需要等待 CDN 缓存过期或手动清除
- 对于需要实时性的安全应用，延迟不可接受

## ✅ **推荐方案**

### 方案 1：HTML 页面不走 CDN（当前方案）⭐ **推荐**

**配置**：
```nginx
# Nginx 配置
location / {
    # 所有请求（包括 HTML）都转发到 Actix Web
    proxy_pass http://secure_resume_backend;
    proxy_cache_bypass 1;
    proxy_no_cache 1;
    add_header Cache-Control "no-store, no-cache, must-revalidate" always;
}
```

**优点**：
- ✅ 保证动态内容正确分发
- ✅ 安全可靠，session 验证有效
- ✅ 实时更新，无缓存延迟
- ✅ 符合后端 `no-store` 设计意图

**缺点**：
- ⚠️ 所有请求都回源，增加源站压力
- ⚠️ 无法利用 CDN 的全球加速

**适用场景**：
- ✅ 访问量不大的个人简历站点
- ✅ 安全要求高的应用
- ✅ 需要实时更新的内容

### 方案 2：静态资源使用 CDN（优化方案）⭐ **推荐**

**配置**：
```nginx
# 静态资源由 CDN 缓存
location ^~ /static/ {
    root /home/ubuntu/secure-resume;
    expires 7d;
    add_header Cache-Control "public, max-age=604800";
}

# HTML 页面不走 CDN
location / {
    proxy_pass http://secure_resume_backend;
    proxy_cache_bypass 1;
    proxy_no_cache 1;
    add_header Cache-Control "no-store, no-cache, must-revalidate" always;
}
```

**优点**：
- ✅ HTML 页面动态分发，安全可靠
- ✅ 静态资源（CSS/JS/图片）利用 CDN 加速
- ✅ 减少源站带宽压力（静态资源占大部分流量）
- ✅ 平衡性能和安全性

**适用场景**：
- ✅ 当前推荐方案
- ✅ 访问量较大的站点
- ✅ 需要优化性能但保持安全

### 方案 3：CDN 配置 Vary 头（不推荐）❌

**理论方案**：
```nginx
# CDN 需要支持基于 Cookie 的缓存
add_header Vary "Cookie" always;
```

**问题**：
- ❌ 大多数 CDN 不支持基于 Cookie 的缓存
- ❌ 即使支持，配置复杂，容易出错
- ❌ 安全风险仍然存在
- ❌ 维护成本高

## 📊 性能对比

### 当前方案（HTML 不走 CDN）

| 指标 | 值 | 说明 |
|------|-----|------|
| HTML 请求 | 100% 回源 | 保证动态分发 |
| 静态资源 | 100% 回源（当前） | 可优化为 CDN |
| 首次加载 | 正常 | 取决于源站位置 |
| 安全性 | ⭐⭐⭐⭐⭐ | 完全可控 |
| 更新实时性 | ⭐⭐⭐⭐⭐ | 立即生效 |

### 优化方案（静态资源走 CDN）

| 指标 | 值 | 说明 |
|------|-----|------|
| HTML 请求 | 100% 回源 | 保证动态分发 |
| 静态资源 | CDN 缓存 | 7 天缓存 |
| 首次加载 | 较快 | HTML 回源，静态资源 CDN |
| 安全性 | ⭐⭐⭐⭐⭐ | 完全可控 |
| 更新实时性 | ⭐⭐⭐⭐⭐ | HTML 立即生效，静态资源需清除缓存 |

## 🎯 最终建议

### ✅ **HTML 页面：不使用 CDN**

**原因总结**：
1. **动态内容分发**：同一 URL 根据 session 返回不同内容
2. **安全要求**：需要实时 session 验证，不能缓存
3. **设计意图**：后端已设置 `no-store`，明确禁止缓存
4. **用户体验**：避免缓存导致的状态混乱

### ✅ **静态资源：使用 CDN（等调试通后启用）**

**原因**：
1. **性能优化**：CSS/JS/图片等静态资源适合 CDN 缓存
2. **带宽节省**：静态资源占大部分流量
3. **安全无影响**：静态资源不涉及 session 验证
4. **更新可控**：可通过版本号或清除缓存更新

### 📝 实施步骤

1. **当前阶段**（调试中）：
   - ✅ HTML 和静态资源都走 Actix Web
   - ✅ 确保功能正常

2. **优化阶段**（调试通后）：
   - ✅ 启用 Nginx 的 `location ^~ /static/` 配置
   - ✅ 静态资源由 Nginx 直接服务，可被 CDN 缓存
   - ✅ HTML 页面继续走 Actix Web，不缓存

3. **CDN 配置**：
   - ✅ 配置 CDN 不缓存 `/` 和 `/api/*`
   - ✅ 配置 CDN 缓存 `/static/*`（7 天）
   - ✅ 定期检查缓存规则

## 🔐 安全最佳实践

1. **始终设置 `no-store`**：HTML 页面和 API 响应
2. **Session 验证**：所有敏感内容必须验证 session
3. **HTTPS 强制**：所有通信使用 HTTPS
4. **CDN 白名单**：如果使用 CDN，确保支持安全头部传递

## 📚 参考

- [MDN: Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
- [OWASP: Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [Nginx: proxy_cache](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache)

