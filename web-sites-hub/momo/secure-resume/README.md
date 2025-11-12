# secure-resume

secure-resume 基于 Actix Web 构建，用于保护个人简历内容。前端模板、静态资源与后端接口解耦，支持在浏览器中直接打开模板调试，也可以通过后端认证后安全访问。

Actix Web 属于 Rust 社区的高性能异步 Web 框架，特点包括 Actor 模型驱动的请求处理、零拷贝响应、灵活的中间件系统，以及与 Tokio 深度集成的异步运行时。本项目利用其 `HttpServer`、`SessionMiddleware` 等模块实现鉴权、会话和静态资源托管。

## 功能概览

- **登录与会话**  
  - `/`：未认证用户返回 `templates/auth.html`；完成邀请码验证的用户返回 `templates/resume.html`。  
  - `/api/auth`：校验邀请码（JSON `{ "code": "XXXXXXXX" }`）。成功后在 `actix-session` 会话里记录登录状态。  
  - `/api/logout`：清空会话并返回登出结果。

- **邀请码管理**  
  - `/api/generate`：一次生成最多 5 个 8 位邀请码，写入 SQLite（`invites.db`）。  
  - `/api/stats`：返回邀请码总数、已使用和可用数量。

- **前端模板与静态资源**  
  - `templates/auth.html`：登录页模板。  
  - `templates/resume.html`：完整的简历页面，可直接双击在浏览器里查看；通过后端访问时使用 Actix 提供的 `/static` 静态目录。  
  - `static/style.css`、`static/auth.js`、`static/resume.js`：样式与脚本文件。`resume.js` 只负责注销按钮，模板渲染直接写在 HTML 中。

## 系统依赖

编译 `secure-resume` 需要以下系统库：

**Ubuntu/Debian：**

```bash
sudo apt update
sudo apt install -y build-essential libsqlite3-dev pkg-config libssl-dev
```

**CentOS/RHEL：**

```bash
sudo yum install -y gcc gcc-c++ sqlite-devel pkgconfig openssl-devel
```

如果编译时提示找不到 `-lsqlite3`，请确保已安装 `libsqlite3-dev`（Ubuntu）或 `sqlite-devel`（CentOS）。

## 运行方式

### 生产部署要点

- 发布到 HTTPS 环境时设置 `SECURE_RESUME_SECURE_COOKIE=1`，生产构建会默认打开安全 Cookie、`SameSite=Strict` 以及 HSTS。
- Nginx/反向代理需要把 `Host`、`X-Real-IP`、`X-Forwarded-For`、`X-Forwarded-Proto` 传给 Actix，示例配置见 `docs/secure-resume-production.md`。
- 为避免缓存页面内容，服务端会主动返回 `Cache-Control: no-store`，CDN 需要尊重该头或按域名关闭缓存。
- 静态资源可通过 `/static/` 在 Nginx 端 alias 到部署目录（如 `/opt/secure-resume/static`），或直接由 Actix 处理。


| 场景 | 命令 |
| ---- | ---- |
| 调试运行 | `cargo run` |
| 调试构建 | `cargo build` |
| Release 构建 | `cargo build --release` |
| Release 运行 | `cargo run --release` |
| 带日志运行（Release） | `RUST_LOG=info cargo run --release` |
| 直接执行 Release 可执行文件 | `RUST_LOG=info ./target/release/secure_resume` |
| 后台运行（简易） | `RUST_LOG=info nohup ./target/release/secure_resume > secure-resume.log 2>&1 &` |

> 注意：生产环境建议使用 `systemd`、`supervisor` 或容器编排工具来管理进程、日志与重启策略。

无论是 `cargo run` 还是 `cargo run --release`，默认工作目录都是 `web-sites-hub/momo/secure-resume`。因此：

- SQLite 数据库位于 `web-sites-hub/momo/secure-resume/invites.db`
- 模板目录：`web-sites-hub/momo/secure-resume/templates`
- 静态资源目录：`web-sites-hub/momo/secure-resume/static`

脚本快捷方式：

```bash
./scripts/start-secure-resume.sh   # 启动，日志写入 secure-resume.log
./scripts/status-secure-resume.sh  # 查看运行状态及监听端口（依赖 lsof 或 netstat）
./scripts/stop-secure-resume.sh    # 停止运行中的服务（根据二进制路径查找进程）

脚本运行后日志位于 `secure-resume.log`，可用 `tail -f secure-resume.log` 查看实时输出。
```

启动后访问 `http://127.0.0.1:8080`，通过 `/api/generate` 生成邀请码即可测试登录流程。

生成邀请码示例命令：

```bash
curl -X POST http://127.0.0.1:8080/api/generate \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```

> **注意**：服务默认监听 `127.0.0.1:8080`（仅本地访问），通过 Nginx 反向代理对外提供服务。如需本地开发测试，可临时修改 `src/main.rs` 中的 `bind("127.0.0.1:8080")` 为 `bind("0.0.0.0:8080")`。

## Actix Server 专业概览

Actix Web 基于 `actix_server` 构建底层运行时。`HttpServer::new` 实际调用 `actix_server::builder()` 搭建异步服务器，核心要点如下：

- **多 worker 模型**  
  - 默认 worker 数量 = CPU 核心数（可通过 `workers(n)` 自定义）。  
  - 每个 worker 线程独立运行，负责接收连接、解析 HTTP 请求并执行业务 handler。  
  - 该模型利用多核并行提升吞吐量，同时避免阻塞（所有 handler 都应当是 `async` 或快速返回）。

- **监听与绑定**  
  - `bind("127.0.0.1:8080")` 会通过 `actix_server::ServerBuilder` 创建监听 socket（仅本地访问）。  
  - 日志 `starting server on 127.0.0.1:8080` 表示仅监听本地回环接口：  
    - 本机访问：`http://127.0.0.1:8080`  
    - 通过 Nginx 反向代理对外提供服务  
  - 可使用 `bind("0.0.0.0:8080")` 对所有网卡开放端口（开发环境），或使用多次 `bind`/`bind_openssl` 注册额外端口或开启 TLS。

- **热重启与优雅关闭**  
  - `actix_server` 支持 `graceful shutdown`，可在捕获 `SIGINT`/`SIGTERM` 时调用 `Server::stop(true)`，等待所有连接完成。  
  - 默认开启内置 watchdog，worker 崩溃会被自动重启，提升稳定性。

- **自定义构建**  
  - 复杂场景下可以直接使用 `actix_server::builder()` 组合 `ServiceFactory` 和中间件，例如接 TCP 流、Unix Domain Socket 或自定义协议。  
  - Actix Web 只是其上层封装，分享同一套运行机制。

上述特性保证 `secure-resume` 在高并发、多核环境下仍具备出色的吞吐与稳定性。

## 日志

项目启用了 `env_logger`，默认输出 INFO 级别日志。可以使用环境变量调整日志等级：

```bash
RUST_LOG=info cargo run
```

关键日志包括：

- 服务启动：`安全简历系统启动在 http://127.0.0.1:8080`
- 邀请码验证流程：记录请求 IP、邀请码状态以及数据库更新结果
- 邀请码生成：打印生成数量和具体列表
- 注销与错误：分别使用 `info!`、`warn!`、`error!` 进行标记

## 数据表结构

服务自动创建 `invites.db` 并包含以下字段：

| 字段        | 说明                |
| ----------- | ------------------- |
| `code`      | 邀请码（唯一）      |
| `used`      | 是否已使用          |
| `created_at`| 创建时间            |
| `used_at`   | 使用时间            |
| `visitor_ip`| 使用该邀请码的 IP   |

## 调试静态模板

`templates/resume.html` 使用相对路径引用 `../static/style.css` 与 `../static/resume.js`。因此：

- 直接在浏览器打开该文件即可调试样式；
- 通过 Actix 访问时，浏览器会将相对路径归一化为 `/static/...`，对应 `Files::new("/static", "./static")`。

如此既方便前端独立调试，又能保证真实环境下只在验证成功后才返回模板。

