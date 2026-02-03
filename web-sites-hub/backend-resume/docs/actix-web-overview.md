# Actix Web 详解

本文档介绍 Actix Web 生态的核心概念、运行机制与常用实践，可帮助在 `secure-resume` 项目中进一步扩展功能。

## 1. 架构基础

- **Actix Actor System**  
  底层使用轻量级 actor 模型管理异步任务，但在 Actix Web 中通常通过 `Service` 与 `Middleware` 抽象呈现，用户无需直接操作 actor。

- **Tokio 集成**  
  Actix Web 4.x 构建在 Tokio runtime 之上，所有异步 handler、数据库调用、IO 操作需要遵循 async/await 模式。

- **Service Factory**  
  每个 HTTP 请求会通过 `ServiceFactory` 链构建出 `Service` 实例，顺序包含：应用级中间件 → 路由 → 资源级中间件 → handler。

## 2. HttpServer 与运行时

`HttpServer::new` 实际调用 `actix_server::builder()`，流程如下：

1. **创建服务工厂**：对闭包 `App::new()` 进行封装，确保每个 worker 拥有独立的 `App` 克隆。
2. **监听端口**：`bind`/`bind_rustls`/`bind_openssl` 将监听 socket 注册到 `actix_server`。
3. **启动 worker**：默认数量为 CPU 核心数，可通过 `workers(n)` 调整。
4. **运行事件循环**：每个 worker 接收套接字连接，解析请求，执行服务链。

### Worker 线程特点

- 单线程事件循环，避免锁竞争。
- Handler 需要避免阻塞调用；若必须执行同步计算，建议配合 `web::block` 或 `spawn_blocking`。
- Worker 崩溃会自动重启（watchdog）。

## 3. 请求处理流程

```
Client -> Listener (actix_server)
       -> Worker (Tokio runtime)
       -> App 中间件栈
       -> Router 匹配 + Guard 校验
       -> 资源级中间件
       -> Handler (async fn)
       -> Response middleware
       -> Client
```

### 路由与 Guard

- `App::route("/api/auth", web::post().to(handler))`
- Guard 示例：

```rust
use actix_web::{guard, web, HttpResponse};

App::new()
    .route(
        "/healthz",
        web::route()
            .guard(guard::Head())
            .to(|| async { HttpResponse::Ok() }),
    );
```

## 4. 常用模块

| 模块 | 说明 | 典型用途 |
| ---- | ---- | -------- |
| `actix-web::web` | 路由、数据提取、响应 | `web::Json<T>`, `web::Path<T>` |
| `actix-session` | 会话与存储 | Cookie session、Redis session |
| `actix-files` | 静态资源托管 | `Files::new("/static", "./static")` |
| `actix-cors` | 跨域控制 | `Cors::default().allowed_origin(...)` |
| `actix-rt` | Tokio runtime 工具 | 定时任务、异步执行 |

## 5. 配置与环境

- **日志**：使用 `env_logger`，通过 `RUST_LOG=actix_web=info` 控制框架日志。
- **超时与限制**：
  - `App::wrap(middleware::Compress::default())` 压缩响应。
  - `HttpServer::client_timeout(...)` / `client_shutdown(...)` 控制 Keep-Alive。
- **跨域**：`App::wrap(Cors::permissive())` 或更细粒度配置。

## 6. 中间件

中间件实现 `Transform` trait，典型场景：

- 记录请求响应日志
- 统一错误处理 / 自定义响应头
- 认证与授权

示例：

```rust
use actix_web::{dev::{Service, ServiceRequest, ServiceResponse, Transform}, Error};
use futures_util::future::{ready, LocalBoxFuture, Ready};

struct LogMiddleware;

impl<S, B> Transform<S, ServiceRequest> for LogMiddleware
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type InitError = ();
    type Transform = LogMiddlewareService<S>;
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ready(Ok(LogMiddlewareService { service }))
    }
}

struct LogMiddlewareService<S> {
    service: S,
}

impl<S, B> Service<ServiceRequest> for LogMiddlewareService<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Future = LocalBoxFuture<'static, Result<Self::Response, Self::Error>>;

    fn poll_ready(&self, ctx: &mut std::task::Context<'_>) -> std::task::Poll<Result<(), Self::Error>> {
        self.service.poll_ready(ctx)
    }

    fn call(&self, req: ServiceRequest) -> Self::Future {
        println!("Incoming request: {}", req.path());
        let fut = self.service.call(req);
        Box::pin(async move {
            let res = fut.await?;
            println!("Response status: {}", res.status());
            Ok(res)
        })
    }
}
```

## 7. 数据提取与验证

Actix Web 提供多种 extractor：

- `web::Json<T>`：自动解析 JSON。
- `web::Query<T>`：URL 查询参数。
- `web::Path<T>`：路径参数。
- `web::Data<AppState>`：共享状态。

结合 `serde` 和 `validator` crate，可实现输入校验与结构化错误响应。

## 8. 测试与调试

- 使用 `actix_web::test` 模块编写单元测试：

```rust
use actix_web::{test, App};

#[actix_web::test]
async fn test_index() {
    let app = test::init_service(App::new().route("/", web::get().to(|| async { "hi" }))).await;
    let req = test::TestRequest::default().to_request();
    let resp = test::call_service(&app, req).await;
    assert!(resp.status().is_success());
}
```

- `RUST_LOG=debug` 观察内部流程；结合 `actix_web::middleware::Logger` 可配置自定义格式。

## 9. 部署建议

- 使用 `cargo build --release` 构建，结合 `RUST_LOG` 控制日志级别。
- 配合 `systemd` 或容器编排（Docker/Kubernetes）管理进程生命周期。
- 生产环境常与 Nginx/Traefik 等代理配合，实现 TLS 终止、静态缓存等功能。

## 10. 延伸阅读

- 官方文档：[https://actix.rs/](https://actix.rs/)
- Actix Web API 文档：[https://docs.rs/actix-web](https://docs.rs/actix-web)
- 示例仓库：[https://github.com/actix/examples](https://github.com/actix/examples)

通过上述概览，可以进一步在 `secure-resume` 项目中集成认证、日志、限流、API 文档等高级功能。*** End Patch*** End Patch to=functions.apply_patch

