# 06-Rust疑难解析

Rust编译器严格，常见错误、性能陷阱、调试技巧汇总。

## 常见编译错误

### 借用检查错误

```rust
// 错误1：可变借用冲突
let mut s = String::from("hello");
let r1 = &mut s;
let r2 = &mut s;  // ❌ 错误：不能同时存在两个可变借用
println!("{}, {}", r1, r2);

// 解决：分离作用域
let mut s = String::from("hello");
{
    let r1 = &mut s;
    println!("{}", r1);
}  // r1作用域结束
let r2 = &mut s;  // ✓ OK

// 错误2：可变和不可变借用冲突
let mut s = String::from("hello");
let r1 = &s;
let r2 = &mut s;  // ❌ 错误：已有不可变借用
println!("{}, {}", r1, r2);

// 解决：利用NLL（非词法生命周期）
let mut s = String::from("hello");
let r1 = &s;
println!("{}", r1);  // r1最后使用
let r2 = &mut s;  // ✓ OK：r1不再使用
```

### 生命周期错误

```rust
// 错误：返回悬空引用
fn dangle() -> &String {
    let s = String::from("hello");
    &s  // ❌ 错误：s离开作用域
}

// 解决1：返回所有权
fn no_dangle() -> String {
    String::from("hello")
}

// 解决2：使用'static
fn static_str() -> &'static str {
    "hello"  // 字符串字面量是'static
}

// 错误：生命周期不匹配
struct Foo<'a> {
    x: &'a i32,
}

impl Foo<'_> {
    fn bad(&self) -> &i32 {
        &5  // ❌ 错误：返回临时值的引用
    }
    
    fn good(&self) -> &i32 {
        self.x  // ✓ OK：返回结构体字段
    }
}
```

### 所有权错误

```rust
// 错误：使用已移动的值
let s1 = String::from("hello");
let s2 = s1;
println!("{}", s1);  // ❌ 错误：s1已移动

// 解决：克隆或借用
let s1 = String::from("hello");
let s2 = s1.clone();
println!("{}, {}", s1, s2);  // ✓ OK

// 错误：部分移动
struct Point {
    x: String,
    y: String,
}

let p = Point {
    x: String::from("1"),
    y: String::from("2"),
};
let x = p.x;  // x移走
println!("{}", p.y);  // ✓ OK：y未移动
// println!("{:?}", p);  // ❌ 错误：p部分移动

// 解决：实现Clone或使用引用
```

### Trait错误

```rust
// 错误：trait未实现
let v = vec![1, 2, 3];
// v.sort();  // ❌ 错误：Vec<i32>未实现排序需要的Ord

// 解决：使用正确的trait
v.sort();  // ✓ OK：i32实现了Ord

// 错误：孤儿规则
// impl ToString for Vec<i32> { }  // ❌ 错误：不能为外部类型实现外部trait

// 解决：newtype模式
struct MyVec(Vec<i32>);
impl ToString for MyVec {  // ✓ OK
    fn to_string(&self) -> String {
        format!("{:?}", self.0)
    }
}
```

## 常见运行时错误

### Panic场景

```rust
// 1. 数组越界
let v = vec![1, 2, 3];
let x = v[10];  // panic!

// 解决：使用get
let x = v.get(10);  // 返回Option<&T>
match x {
    Some(val) => println!("{}", val),
    None => println!("索引越界"),
}

// 2. unwrap/expect on None/Err
let opt: Option<i32> = None;
// opt.unwrap();  // panic!

// 解决：使用match或if let
if let Some(val) = opt {
    println!("{}", val);
}

// 3. 整数溢出（debug模式panic，release模式回绕）
let x: u8 = 255;
// let y = x + 1;  // debug panic，release回绕到0

// 解决：使用checked_*方法
let y = x.checked_add(1);  // 返回Option<u8>

// 4. 除零
// let x = 10 / 0;  // panic!

// 解决：检查除数
let divisor = 0;
if divisor != 0 {
    let result = 10 / divisor;
}
```

### 死锁

```rust
use std::sync::Mutex;

// 死锁示例
let m1 = Mutex::new(1);
let m2 = Mutex::new(2);

let g1 = m1.lock().unwrap();
// let g2 = m2.lock().unwrap();  // 如果另一线程先锁m2再锁m1，死锁

// 解决1：固定加锁顺序
// 解决2：使用try_lock
match m2.try_lock() {
    Ok(g2) => {  // 获取到锁
        // 使用g1和g2
    }
    Err(_) => {  // 获取失败
        drop(g1);  // 释放m1
        // 重试或返回错误
    }
}

// 解决3：使用超时
use std::time::Duration;

let guard = m1.lock().unwrap();
// 某些实现提供timeout版本
```

## 性能陷阱

### 不必要的克隆

```rust
// ❌ 性能差：过度克隆
fn process_string(s: String) -> String {
    let upper = s.to_uppercase();  // 分配新String
    upper.clone()  // 不必要的克隆
}

// ✅ 优化：直接返回
fn process_string(s: String) -> String {
    s.to_uppercase()  // 直接返回，无额外分配
}

// ❌ 性能差：循环中克隆
let data = vec![String::from("a"); 1000];
for item in &data {
    let copy = item.clone();  // 1000次克隆
    process(copy);
}

// ✅ 优化：使用引用
for item in &data {
    process(item);  // 无克隆
}
```

### Vec预分配

```rust
// ❌ 性能差：多次重新分配
let mut v = Vec::new();
for i in 0..10000 {
    v.push(i);  // 可能多次重新分配
}

// ✅ 优化：预分配
let mut v = Vec::with_capacity(10000);
for i in 0..10000 {
    v.push(i);  // 一次分配
}

// 或使用collect
let v: Vec<i32> = (0..10000).collect();
```

### String vs &str

```rust
// ❌ 性能差：不必要的String分配
fn greet(name: String) {
    println!("Hello, {}!", name);
}

greet(String::from("Alice"));  // 总是分配

// ✅ 优化：使用&str
fn greet(name: &str) {
    println!("Hello, {}!", name);
}

greet("Alice");  // 无分配
greet(&String::from("Bob"));  // 也可接受String引用
```

### 迭代器 vs 索引

```rust
// ❌ 性能差：索引访问
let v = vec![1, 2, 3, 4, 5];
let mut sum = 0;
for i in 0..v.len() {
    sum += v[i];  // 每次都做边界检查
}

// ✅ 优化：迭代器
let sum: i32 = v.iter().sum();  // 编译器优化，无边界检查
```

### 小心Rc<RefCell<T>>

```rust
use std::rc::Rc;
use std::cell::RefCell;

// Rc<RefCell<T>>有运行时开销
let data = Rc::new(RefCell::new(vec![1, 2, 3]));

// 每次borrow都有检查开销
for _ in 0..1000 {
    let borrowed = data.borrow();  // 运行时借用检查
    // 使用borrowed
}

// 优化：减少borrow次数
{
    let mut borrowed = data.borrow_mut();
    for _ in 0..1000 {
        borrowed.push(0);  // 只borrow一次
    }
}
```

## 调试技巧

### println! 调试

```rust
// 基础打印
let x = 5;
println!("x = {}", x);

// Debug格式
let v = vec![1, 2, 3];
println!("{:?}", v);  // 单行
println!("{:#?}", v);  // 多行格式化

// dbg! 宏（显示位置）
let x = 5;
dbg!(x);  // [src/main.rs:2] x = 5

let result = dbg!(x + 1);  // 返回值
```

### 类型检查技巧

```rust
// 技巧：让编译器告诉类型
let x = vec![1, 2, 3];
let _: () = x;  // 编译错误，错误信息显示x的类型

// 使用type_name（nightly或std::any）
use std::any::type_name;

fn type_of<T>(_: &T) -> &'static str {
    type_name::<T>()
}

let x = vec![1, 2, 3];
println!("{}", type_of(&x));  // "alloc::vec::Vec<i32>"
```

### 编译器输出分析

```bash
# 查看宏展开
cargo expand

# 查看MIR（中间表示）
cargo rustc -- -Z unpretty=mir

# 查看LLVM IR
cargo rustc -- --emit=llvm-ir

# 查看汇编
cargo rustc -- --emit=asm

# 详细编译信息
cargo build -vv

# 查看依赖树
cargo tree

# 查看为什么编译某个crate
cargo build --timings
```

### Clippy警告

```bash
# 运行clippy
cargo clippy

# 严格模式
cargo clippy -- -D warnings

# 特定lint
cargo clippy -- -W clippy::pedantic

# 常见警告修复
```

```rust
// 警告：不必要的clone
let s = String::from("hello");
let s2 = s.clone();
// 如果s不再使用，直接move：let s2 = s;

// 警告：单字符字符串
"x".to_string();
// 使用：'x'.to_string() 或 String::from('x')

// 警告：len() == 0
if v.len() == 0 { }
// 使用：if v.is_empty() { }

// 警告：match可以用if let
match opt {
    Some(x) => { /* ... */ }
    None => {}
}
// 使用：if let Some(x) = opt { /* ... */ }
```

## unsafe代码

### 何时使用unsafe

```rust
// 1. 解引用裸指针
let mut num = 5;
let r1 = &num as *const i32;  // 不可变裸指针
let r2 = &mut num as *mut i32;  // 可变裸指针

unsafe {
    println!("{}", *r1);
    *r2 = 10;
}

// 2. 调用unsafe函数
unsafe fn dangerous() {}

unsafe {
    dangerous();
}

// 3. 访问可变静态变量
static mut COUNTER: u32 = 0;

unsafe {
    COUNTER += 1;
    println!("{}", COUNTER);
}

// 4. 实现unsafe trait
unsafe trait UnsafeTrait {
    fn method(&self);
}

unsafe impl UnsafeTrait for MyType {
    fn method(&self) { }
}

// 5. 访问union字段
union MyUnion {
    f1: u32,
    f2: f32,
}

let u = MyUnion { f1: 1 };
unsafe {
    println!("{}", u.f1);
}
```

### unsafe最佳实践

```rust
// ✓ 最小化unsafe块
fn foo() {
    // 安全代码
    
    unsafe {
        // 仅unsafe操作
    }
    
    // 更多安全代码
}

// ✓ 封装unsafe
pub fn safe_wrapper(data: &[i32]) -> i32 {
    assert!(!data.is_empty());
    unsafe {
        *data.get_unchecked(0)  // 已检查非空
    }
}

// ❌ 不要暴露unsafe
// pub unsafe fn dangerous_api() { }

// ✓ 文档说明安全不变量
/// # Safety
/// 调用者必须确保`ptr`是有效的、对齐的指针
pub unsafe fn read_ptr(ptr: *const i32) -> i32 {
    *ptr
}
```

## 宏调试

```rust
// 查看宏展开
// cargo expand（需要cargo-expand）

// 手动追踪
macro_rules! debug_macro {
    ($($arg:tt)*) => {
        {
            println!("展开: {}", stringify!($($arg)*));
            $($arg)*
        }
    };
}

// 编译时打印
macro_rules! show_type {
    ($t:ty) => {
        const _: () = {
            struct TypeDisplay;
            impl TypeDisplay {
                const fn type_name() -> &'static str {
                    stringify!($t)
                }
            }
        };
    };
}
```

## 依赖问题

### 版本冲突

```toml
# ❌ 错误：版本冲突
[dependencies]
crate_a = "1.0"  # 依赖 shared = "1.0"
crate_b = "2.0"  # 依赖 shared = "2.0"

# 解决：统一版本或使用补丁
[patch.crates-io]
shared = { git = "https://github.com/user/shared", branch = "fix" }
```

### 编译时间优化

```toml
# Cargo.toml
[profile.dev]
opt-level = 1  # 适度优化

[profile.dev.package."*"]
opt-level = 3  # 依赖完全优化

# 使用sccache
# export RUSTC_WRAPPER=sccache

# 增量编译（默认启用）
# export CARGO_INCREMENTAL=1

# 并行编译
# cargo build -j 8
```

## 最佳实践清单

### 所有权
- [ ] 优先借用，避免克隆
- [ ] 函数参数用&T或&mut T
- [ ] 返回值避免借用（除非明确生命周期）
- [ ] 使用Option/Result传递可能失败的值

### 性能
- [ ] Vec预分配容量
- [ ] 使用&str而非String（参数）
- [ ] 迭代器链优于多次循环
- [ ] 避免不必要的collect
- [ ] 大对象传引用或移动

### 错误处理
- [ ] 库返回Result
- [ ] 应用使用anyhow
- [ ] 避免unwrap（生产环境）
- [ ] 使用?简化错误传播

### 并发
- [ ] 优先消息传递
- [ ] 共享状态用Arc<Mutex<T>>
- [ ] 避免死锁（固定加锁顺序）
- [ ] 使用Rayon处理数据并行

### 代码质量
- [ ] 运行clippy
- [ ] 运行rustfmt
- [ ] 编写测试
- [ ] 添加文档注释
- [ ] 使用#[must_use]标记

**核心：** 编译器错误是助手，运行时错误需预防。性能优化先测量，unsafe需文档说明。

