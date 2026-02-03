# 🦀 Rust 开发

Rust是Mozilla主导开发的系统编程语言，2015年发布1.0版本。核心特性：内存安全、零成本抽象、并发安全。

## 学习时间线

**2021年7月 - 2022年3月（9个月）**

### 阶段一：所有权系统（2021-07）
- 环境搭建、工具链
- 所有权、借用、生命周期
- 引用规则、切片

### 阶段二：基础语法（2021-08）
- 数据类型、变量、函数
- 控制流、模式匹配
- 结构体、枚举
- Vector、String、HashMap

### 阶段三：类型系统（2021-10）
- 错误处理（Result、Option、?运算符）
- 泛型、Trait
- 生命周期注解
- 关联类型、运算符重载

### 阶段四：并发编程（2021-12）
- 智能指针（Box、Rc、Arc、RefCell、Mutex）
- 线程、消息传递
- 共享状态、Send/Sync trait
- 无畏并发原理

### 阶段五：异步编程（2022-02）
- async/await、Future
- Tokio运行时
- 异步I/O、Stream
- 异步通道、同步原语

## 学习文档

1. **01-环境搭建与所有权.md** - Rust环境、所有权系统、借用规则
2. **02-基础语法.md** - 数据类型、控制流、结构体、枚举、集合
3. **03-错误处理与Trait.md** - Result/Option、泛型、Trait、生命周期
4. **04-并发与智能指针.md** - 智能指针、线程、Channel、Mutex、Arc
5. **05-异步编程.md** - async/await、Tokio、异步I/O、HTTP服务器

## Rust核心特性

### 内存安全
- **所有权系统**：每个值有唯一所有者
- **借用检查**：编译期保证引用有效性
- **无GC**：零运行时开销
- **消除悬空指针**：编译器阻止
- **消除数据竞争**：类型系统保证

### 零成本抽象
- **泛型单态化**：编译期展开
- **Trait对象**：动态分发可选
- **迭代器**：编译为循环
- **闭包**：零开销捕获
- **性能接近C**：无运行时

### 并发安全
- **Send trait**：可跨线程转移
- **Sync trait**：可跨线程共享
- **编译期检查**：消除数据竞争
- **类型系统保证**：无需运行时检查
- **消息传递/共享状态**：两种并发模式

### 工具链
- **Cargo**：构建工具、包管理
- **rustfmt**：代码格式化
- **clippy**：Lint工具
- **rust-analyzer**：LSP服务器
- **rustup**：工具链管理

## 应用场景

### 系统编程
- 操作系统内核（Redox OS）
- 嵌入式开发
- 驱动程序
- 文件系统

### 命令行工具
- ripgrep（文本搜索）
- fd（文件查找）
- bat（cat替代）
- exa（ls替代）
- delta（diff工具）

### Web后端
- Actix Web（高性能）
- Axum（现代框架、Tower生态、异步支持）
- Rocket（类型安全）
- Warp（函数式风格）

### WebAssembly
- Yew（前端框架）
- trunk（构建工具）
- wasm-bindgen（JS互操作）

### 区块链
- Polkadot、Solana、NEAR
- Substrate框架

### 游戏开发
- Bevy游戏引擎
- Amethyst引擎

## 技术栈

### Web开发
- **框架**：Axum、Actix Web、Rocket
- **ORM**：Diesel、SeaORM、sqlx
- **序列化**：serde、serde_json
- **HTTP客户端**：reqwest、hyper
- **模板**：askama、tera

### 异步生态
- **运行时**：Tokio、async-std
- **工具**：tokio-util、futures
- **HTTP**：hyper、reqwest
- **WebSocket**：tokio-tungstenite

### 数据处理
- **JSON**：serde_json
- **YAML**：serde_yaml
- **TOML**：toml
- **CSV**：csv
- **正则**：regex

### 测试
- **单元测试**：内置#[test]
- **属性测试**：proptest、quickcheck
- **模拟**：mockall
- **基准测试**：criterion

## 学习资源

### 官方文档
- The Rust Programming Language（官方书）
- Rust by Example
- Rustonomicon（高级内容）
- Async Book（异步编程）

### 在线资源
- docs.rs（库文档）
- crates.io（包仓库）
- Rust Playground（在线运行）
- cheats.rs（速查表）

### 推荐书籍
- Programming Rust
- Rust for Rustaceans
- Zero To Production In Rust

## 常用Crate

### 基础工具
```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1", features = ["full"] }
anyhow = "1.0"
thiserror = "1.0"
```

### Web服务器
```toml
[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
tower = "0.4"
```

### 数据库
```toml
[dependencies]
sqlx = { version = "0.7", features = ["runtime-tokio", "postgres"] }
diesel = { version = "2.1", features = ["postgres"] }
```

## 最佳实践

### 代码组织
```
src/
├── main.rs          # 二进制入口
├── lib.rs           # 库入口
├── bin/             # 多个二进制
├── models/          # 数据模型
├── handlers/        # 处理器
└── utils/           # 工具函数
```

### 错误处理
```rust
// 库：返回具体错误类型
pub enum MyError {
    Io(std::io::Error),
    Parse(ParseError),
}

// 应用：使用anyhow
fn main() -> anyhow::Result<()> {
    // ...
}
```

### 所有权规则
- 默认不可变
- 优先借用，避免克隆
- 可变引用独占
- 生命周期尽量简单
- 返回所有权优于可变引用

### 并发原则
- Send/Sync由编译器保证
- 优先消息传递
- 共享状态用Arc<Mutex<T>>
- 读多写少用Arc<RwLock<T>>
- 原子操作用Atomic*

### 异步建议
- 避免阻塞运行时
- CPU密集用spawn_blocking
- I/O密集用async
- 使用超时机制
- 正确处理取消

## 编译优化

### Cargo.toml配置
```toml
[profile.release]
opt-level = 3          # 最高优化
lto = true             # 链接时优化
codegen-units = 1      # 单一代码生成单元
strip = true           # 去除符号
panic = 'abort'        # 减小二进制

[profile.dev]
opt-level = 1          # 开发时适度优化

[profile.dev.package."*"]
opt-level = 3          # 依赖完全优化
```

### 性能分析
```bash
# CPU profile
cargo build --release
perf record ./target/release/app
perf report

# 内存分析
valgrind --tool=massif ./target/release/app

# Benchmark
cargo bench
```

## 交叉编译

```bash
# 安装目标
rustup target add x86_64-pc-windows-gnu

# 编译
cargo build --target x86_64-pc-windows-gnu

# 支持的目标
rustup target list
```

## 常见陷阱

### 1. 所有权移动
```rust
// ❌ 错误
let s1 = String::from("hello");
let s2 = s1;
println!("{}", s1);  // 错误：s1已移动

// ✓ 正确
let s1 = String::from("hello");
let s2 = s1.clone();
println!("{}", s1);
```

### 2. 借用冲突
```rust
// ❌ 错误
let mut v = vec![1, 2, 3];
let r = &v[0];
v.push(4);  // 错误：已有不可变借用
println!("{}", r);

// ✓ 正确
let mut v = vec![1, 2, 3];
{
    let r = &v[0];
    println!("{}", r);
}
v.push(4);
```

### 3. 生命周期
```rust
// ❌ 错误
fn dangle() -> &String {
    let s = String::from("hello");
    &s  // 错误：返回局部变量引用
}

// ✓ 正确
fn no_dangle() -> String {
    String::from("hello")
}
```

## 项目实践

### CLI工具
- 使用clap解析参数
- anyhow处理错误
- env_logger日志

### Web服务
- Axum框架
- Tokio运行时
- sqlx数据库
- tower中间件

### 性能优化
- 减少克隆
- 使用&str而非String
- 预分配容量
- 避免不必要的分配
- 使用迭代器

## 学习心得

1. **所有权核心**：内存安全和并发安全的基础
2. **编译器严格**：编译通过基本无运行时错误
3. **类型系统完备**：泛型、Trait、生命周期
4. **零成本抽象**：高级特性无性能损失
5. **异步高效**：Tokio生态完善
6. **工具链优秀**：Cargo、rustfmt、clippy
7. **性能接近C**：适合系统编程
8. **社区活跃**：crates.io包丰富
9. **文档完善**：docs.rs质量高
10. **安全第一**：编译期消除大部分bug

**核心：** Rust通过所有权系统和类型系统在编译期保证内存安全和并发安全，实现零成本抽象和高性能。
