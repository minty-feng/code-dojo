# 01-Rust环境搭建与所有权

Rust是Mozilla于2010年启动的系统编程语言，2015年发布1.0版本。核心特性：内存安全、零成本抽象、并发安全。

## Rust简介

### 设计目标

- **内存安全**：无GC的内存安全，编译期检查
- **并发安全**：消除数据竞争，编译期保证
- **零成本抽象**：高级特性无运行时开销
- **性能**：接近C/C++
- **生产力**：现代工具链、包管理

### 应用场景

**系统编程：**
- 操作系统内核（Redox OS）
- 嵌入式开发
- 驱动程序

**Web后端：**
- 高性能API服务（Actix、Rocket）
- WebAssembly（Yew前端框架）
- 云原生工具

**命令行工具：**
- ripgrep（文本搜索）
- fd（文件查找）
- bat（cat替代品）
- exa（ls替代品）

**区块链：**
- Polkadot、Solana、NEAR

**游戏开发：**
- Bevy游戏引擎

### 语言特点

**优势：**
- 内存安全（无悬空指针、无数据竞争）
- 无GC（可预测性能）
- 强大类型系统（零成本抽象）
- 并发安全（Send/Sync trait）
- 现代工具链（Cargo、rustfmt、clippy）

**劣势：**
- 学习曲线陡峭（所有权、生命周期）
- 编译速度慢
- 生态尚不成熟（相比C++/Java）
- 开发速度慢（严格编译器）

## 环境安装

### rustup（推荐）

```bash
# Linux/macOS
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Windows
# 下载：https://rustup.rs
# 需要Visual Studio C++构建工具

# 验证
rustc --version
cargo --version

# 更新
rustup update

# 卸载
rustup self uninstall
```

### 工具链管理

```bash
# 查看已安装工具链
rustup show

# 安装稳定版
rustup install stable

# 安装nightly版
rustup install nightly

# 切换默认工具链
rustup default stable
rustup default nightly

# 项目级工具链
rustup override set nightly  # 当前目录

# 组件管理
rustup component add rustfmt      # 格式化工具
rustup component add clippy       # lint工具
rustup component add rust-src     # 标准库源码
rustup component add rust-analyzer  # LSP服务器

# 目标平台
rustup target list
rustup target add x86_64-pc-windows-gnu  # 交叉编译
```

## Cargo包管理

### 基本命令

```bash
# 创建项目
cargo new myproject        # 二进制项目
cargo new --lib mylib      # 库项目

# 构建
cargo build                # Debug构建
cargo build --release      # Release构建（优化）

# 运行
cargo run
cargo run --release

# 测试
cargo test

# 检查（不生成二进制，快）
cargo check

# 格式化
cargo fmt

# Lint
cargo clippy

# 文档
cargo doc --open

# 清理
cargo clean

# 更新依赖
cargo update

# 发布到crates.io
cargo publish
```

### Cargo.toml配置

```toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"       # Rust版本（2015/2018/2021）
authors = ["Your Name <you@example.com>"]
license = "MIT"

[dependencies]
serde = "1.0"          # 最新1.x版本
tokio = { version = "1.0", features = ["full"] }  # 启用特性
rand = "0.8"

[dev-dependencies]     # 仅测试/bench时用
criterion = "0.4"

[build-dependencies]   # 构建脚本依赖
cc = "1.0"

[[bin]]                # 多个二进制
name = "myapp"
path = "src/main.rs"

[profile.release]      # Release优化
opt-level = 3          # 优化级别
lto = true             # 链接时优化
codegen-units = 1      # 单一代码生成单元
```

## 开发工具

### VS Code

**必装插件：**
- rust-analyzer（官方推荐，替代rls）
- CodeLLDB（调试）
- crates（依赖版本提示）

**配置（settings.json）：**
```json
{
    "rust-analyzer.checkOnSave.command": "clippy",
    "rust-analyzer.cargo.features": "all",
    "editor.formatOnSave": true
}
```

### IntelliJ IDEA

**插件：**
- IntelliJ Rust（JetBrains官方）

**特性：**
- 智能补全
- 重构工具
- 调试器
- Cargo集成

## Hello World

### 基本程序

```rust
// main.rs
fn main() {
    println!("Hello, World!");
}
```

```bash
# 编译运行
rustc main.rs
./main

# 或使用Cargo
cargo new hello
cd hello
cargo run
```

### 项目结构

```
myproject/
├── Cargo.toml          # 项目配置
├── Cargo.lock          # 依赖锁定（自动生成）
├── src/
│   ├── main.rs         # 二进制入口
│   ├── lib.rs          # 库入口（如果是库）
│   └── bin/            # 多个二进制
│       └── another.rs
├── tests/              # 集成测试
│   └── integration_test.rs
├── benches/            # 性能测试
│   └── benchmark.rs
├── examples/           # 示例
│   └── example.rs
└── target/             # 构建产物
    ├── debug/
    └── release/
```

## 所有权系统

Rust核心特性，编译期保证内存安全，无需GC。

### 三条规则

1. **每个值都有一个所有者（owner）**
2. **同时只能有一个所有者**
3. **所有者离开作用域，值被丢弃（drop）**

### 移动（Move）

```rust
// String是堆分配，所有权会转移
let s1 = String::from("hello");
let s2 = s1;  // s1的所有权移动到s2

// println!("{}", s1);  // ❌ 编译错误：s1已失效

// 整数等基本类型是Copy，不会移动
let x = 5;
let y = x;  // x仍有效
println!("{}", x);  // ✓ OK
```

### 克隆（Clone）

```rust
// 深拷贝
let s1 = String::from("hello");
let s2 = s1.clone();  // 显式克隆

println!("{}, {}", s1, s2);  // ✓ 两者都有效
```

### Copy trait

```rust
// 实现Copy的类型：整数、浮点、布尔、字符、元组（元素都是Copy）
// 不能实现Copy的类型：String、Vec、Box等堆分配

fn main() {
    let x: i32 = 5;      // Copy
    let y = x;           // 复制，x仍有效
    
    let s1 = String::from("hello");  // 非Copy
    let s2 = s1;         // 移动，s1失效
}
```

### 函数和所有权

```rust
fn main() {
    let s = String::from("hello");
    
    takes_ownership(s);  // s的所有权移入函数
    // println!("{}", s);  // ❌ 错误：s已失效
    
    let x = 5;
    makes_copy(x);      // x是Copy，传的是副本
    println!("{}", x);  // ✓ x仍有效
}

fn takes_ownership(some_string: String) {
    println!("{}", some_string);
}  // some_string离开作用域，被drop

fn makes_copy(some_integer: i32) {
    println!("{}", some_integer);
}
```

### 返回值和所有权

```rust
fn main() {
    let s1 = gives_ownership();  // 所有权转移给s1
    
    let s2 = String::from("hello");
    let s3 = takes_and_gives_back(s2);  // s2移入，返回值移给s3
    
    // println!("{}", s2);  // ❌ s2已失效
    println!("{}", s3);  // ✓ s3有效
}

fn gives_ownership() -> String {
    let some_string = String::from("hello");
    some_string  // 返回，所有权转移
}

fn takes_and_gives_back(a_string: String) -> String {
    a_string  // 返回传入的值
}
```

## 引用和借用

不获取所有权，只借用。

### 不可变引用

```rust
fn main() {
    let s1 = String::from("hello");
    
    let len = calculate_length(&s1);  // 借用
    
    println!("'{}' 的长度是 {}", s1, len);  // s1仍有效
}

fn calculate_length(s: &String) -> usize {
    s.len()
}  // s是引用，不会drop
```

### 可变引用

```rust
fn main() {
    let mut s = String::from("hello");
    
    change(&mut s);
    
    println!("{}", s);  // "hello, world"
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}
```

### 借用规则

**核心规则：**
1. **同一时间，要么一个可变引用，要么任意数量不可变引用**
2. **引用必须总是有效（无悬空引用）**

```rust
// ❌ 错误：同时存在可变和不可变引用
let mut s = String::from("hello");
let r1 = &s;
let r2 = &s;
let r3 = &mut s;  // 错误！
println!("{}, {}, {}", r1, r2, r3);

// ✓ 正确：不可变引用的作用域结束后可变引用
let mut s = String::from("hello");
let r1 = &s;
let r2 = &s;
println!("{}, {}", r1, r2);
// r1和r2不再使用

let r3 = &mut s;  // ✓ OK
println!("{}", r3);

// ❌ 错误：多个可变引用
let mut s = String::from("hello");
let r1 = &mut s;
let r2 = &mut s;  // 错误！
println!("{}, {}", r1, r2);

// ❌ 错误：悬空引用
fn dangle() -> &String {  // 编译错误
    let s = String::from("hello");
    &s  // s离开作用域被drop，引用无效
}

// ✓ 正确：返回所有权
fn no_dangle() -> String {
    let s = String::from("hello");
    s  // 所有权移出
}
```

## 切片（Slice）

引用集合的一部分。

### 字符串切片

```rust
let s = String::from("hello world");

let hello = &s[0..5];   // "hello"
let world = &s[6..11];  // "world"

// 简写
let hello = &s[..5];    // 从开始
let world = &s[6..];    // 到结尾
let whole = &s[..];     // 全部

// 字符串字面量是切片
let s: &str = "Hello, world!";  // 类型：&str

// 函数参数用&str更通用（接受String和&str）
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }
    
    &s[..]
}

let my_string = String::from("hello world");
let word = first_word(&my_string);  // ✓ String引用

let my_string_literal = "hello world";
let word = first_word(my_string_literal);  // ✓ 字符串字面量
```

### 数组切片

```rust
let a = [1, 2, 3, 4, 5];
let slice = &a[1..3];  // &[i32]类型

assert_eq!(slice, &[2, 3]);
```

## 所有权模式总结

### 何时使用

| 场景 | 方式 | 示例 |
|------|------|------|
| 转移所有权 | 值 | `let s2 = s1;` |
| 只读访问 | 不可变引用 | `&s` |
| 修改数据 | 可变引用 | `&mut s` |
| 不确定生命周期 | 智能指针 | `Box<T>`、`Rc<T>` |

### 常见错误

```rust
// ❌ 错误1：使用已移动的值
let s1 = String::from("hello");
let s2 = s1;
println!("{}", s1);  // 错误

// ✓ 解决：克隆或借用
let s1 = String::from("hello");
let s2 = s1.clone();
println!("{}, {}", s1, s2);

// ❌ 错误2：可变引用冲突
let mut s = String::from("hello");
let r1 = &mut s;
let r2 = &mut s;  // 错误
println!("{}, {}", r1, r2);

// ✓ 解决：分开作用域
let mut s = String::from("hello");
{
    let r1 = &mut s;
}  // r1离开作用域
let r2 = &mut s;

// ❌ 错误3：悬空引用
let reference_to_nothing = dangle();

fn dangle() -> &String {
    let s = String::from("hello");
    &s  // 错误：返回局部变量的引用
}

// ✓ 解决：返回所有权
fn no_dangle() -> String {
    String::from("hello")
}
```

## 所有权的优势

### 内存安全

```rust
// C++可能的内存问题
// ❌ 悬空指针
int* ptr;
{
    int x = 42;
    ptr = &x;
}  // x销毁
// *ptr;  // 未定义行为

// Rust编译期阻止
// fn main() {
//     let r;
//     {
//         let x = 5;
//         r = &x;  // 错误：x的生命周期不够长
//     }
//     println!("{}", r);
// }
```

### 并发安全

```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];
    
    // ❌ 错误：不能在多线程间共享可变引用
    let handle = thread::spawn(|| {
        println!("{:?}", v);  // 错误：v可能被主线程drop
    });
    
    // drop(v);  // 如果允许，会导致数据竞争
    handle.join().unwrap();
}

// ✓ 正确：转移所有权
use std::thread;

fn main() {
    let v = vec![1, 2, 3];
    
    let handle = thread::spawn(move || {
        println!("{:?}", v);  // v的所有权移入闭包
    });
    
    // println!("{:?}", v);  // 错误：v已移走
    handle.join().unwrap();
}
```

## 性能

### 零成本抽象

所有权和借用在编译期检查，运行时无开销。

```rust
// 高级抽象
fn sum(numbers: &[i32]) -> i32 {
    numbers.iter().sum()
}

// 编译后等效于C的循环
// int sum = 0;
// for (int i = 0; i < len; i++) {
//     sum += numbers[i];
// }
```

### 与C++对比

| 特性 | Rust | C++ |
|------|------|-----|
| 内存安全 | 编译期保证 | 运行时易错 |
| 数据竞争 | 编译期阻止 | 运行时调试 |
| 悬空指针 | 不可能 | 容易出现 |
| 智能指针 | 内置所有权 | 需手动管理 |
| 性能 | 零成本抽象 | 零成本抽象 |

## 最佳实践

### 1. 优先借用

```rust
// ❌ 不必要的所有权转移
fn process(s: String) {
    println!("{}", s);
}

// ✓ 只读用引用
fn process(s: &str) {
    println!("{}", s);
}
```

### 2. 返回值优于可变引用

```rust
// ❌ 不够清晰
fn append(s: &mut String, suffix: &str) {
    s.push_str(suffix);
}

// ✓ 更函数式
fn append(mut s: String, suffix: &str) -> String {
    s.push_str(suffix);
    s
}
```

### 3. 使用方法链

```rust
// ✓ 清晰的所有权转移
let result = String::from("hello")
    .to_uppercase()
    .replace("HELLO", "HI");
```

### 4. 避免克隆

```rust
// ❌ 不必要的克隆
let s1 = String::from("hello");
let s2 = s1.clone();
process(&s1, &s2);

// ✓ 直接借用
let s1 = String::from("hello");
let s2 = &s1;
process(&s1, s2);
```

## 所有权高级应用

### 零拷贝字符串处理

```rust
// ❌ 多次拷贝
fn process_data(data: String) -> String {
    let trimmed = data.trim().to_string();  // 拷贝1
    let uppercase = trimmed.to_uppercase();  // 拷贝2
    uppercase
}

// ✅ 减少拷贝
fn process_data(data: &str) -> String {
    data.trim().to_uppercase()  // 仅最后结果分配
}

// ✅ 原地修改
fn process_data_inplace(mut data: String) -> String {
    data = data.trim().to_string();
    data.make_ascii_uppercase();  // 原地修改
    data
}
```

### 借用检查器工作原理

```rust
// 编译器分析示例
fn example() {
    let mut s = String::from("hello");
    
    let r1 = &s;        // 不可变借用开始
    let r2 = &s;        // OK：多个不可变借用
    println!("{} {}", r1, r2);
    // r1、r2作用域结束
    
    let r3 = &mut s;    // OK：可变借用开始
    r3.push_str(" world");
    println!("{}", r3);
    // r3作用域结束
    
} // s离开作用域，drop

// 非词法生命周期（NLL）
fn nll_example() {
    let mut s = String::from("hello");
    
    let r1 = &s;
    println!("{}", r1);
    // r1最后使用，编译器判断其生命周期到此结束
    
    let r2 = &mut s;  // OK：r1已不再使用
    r2.push_str(" world");
}
```

### 所有权与集合

```rust
// Vec所有权
let v = vec![
    String::from("a"),
    String::from("b"),
    String::from("c"),
];

// ❌ 错误：move发生
let first = v[0];  // String未实现Copy

// ✅ 方案1：克隆
let first = v[0].clone();

// ✅ 方案2：引用
let first = &v[0];

// ✅ 方案3：移除（转移所有权）
let mut v = vec![String::from("a"), String::from("b")];
let first = v.remove(0);

// ✅ 方案4：swap_remove（O(1)）
let first = v.swap_remove(0);

// HashMap所有权
use std::collections::HashMap;

let mut map = HashMap::new();
let key = String::from("color");
let value = String::from("blue");

map.insert(key, value);
// key、value所有权已转移，不可再用

// ✅ 使用引用作为键
let text = String::from("hello");
let mut map: HashMap<&str, i32> = HashMap::new();
map.insert(&text, 1);  // text仍可用
```

### 内存布局对比

```rust
// 栈分配（Copy类型）
let x: i32 = 5;     // 栈：4字节
let y = x;          // 复制4字节

// 堆分配（String）
let s1 = String::from("hello");
// 栈：ptr(8字节) + len(8字节) + capacity(8字节) = 24字节
// 堆："hello"数据

let s2 = s1;  // 仅复制栈上24字节，堆数据不复制

// Box<T>
let b = Box::new(100);
// 栈：指针8字节
// 堆：i32值4字节

// 对比
struct Point { x: i32, y: i32 }  // 栈8字节
struct Data { v: Vec<i32> }      // 栈24字节 + 堆数据
```

### Cow（写时克隆）

```rust
use std::borrow::Cow;

fn process(input: &str) -> Cow<str> {
    if input.contains("bad") {
        // 需要修改，分配新String
        Cow::Owned(input.replace("bad", "good"))
    } else {
        // 无需修改，借用原字符串
        Cow::Borrowed(input)
    }
}

let s1 = "hello world";
let result = process(s1);  // Cow::Borrowed，零拷贝

let s2 = "bad word";
let result = process(s2);  // Cow::Owned，仅在需要时分配
```

### 所有权转移模式

```rust
// 构建器模式（消耗self）
struct Config {
    host: String,
    port: u16,
}

impl Config {
    fn new() -> Self {
        Config {
            host: String::from("localhost"),
            port: 8080,
        }
    }
    
    fn host(mut self, host: String) -> Self {
        self.host = host;
        self  // 返回所有权
    }
    
    fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }
}

// 链式调用
let config = Config::new()
    .host(String::from("example.com"))
    .port(3000);

// Option的take方法
let mut opt = Some(String::from("hello"));
let s = opt.take();  // 取出值，opt变为None
assert_eq!(opt, None);
assert_eq!(s, Some(String::from("hello")));

// mem::replace
use std::mem;

let mut s = String::from("hello");
let old = mem::replace(&mut s, String::from("world"));
// s现在是"world"，old是"hello"

// mem::take（默认值替换）
let mut opt = Some(vec![1, 2, 3]);
let v = mem::take(&mut opt);  // opt变为None，v是Some(vec![1,2,3])
```

**核心：** 所有权系统通过编译期检查保证内存安全和线程安全，消除悬空指针、数据竞争等问题。

