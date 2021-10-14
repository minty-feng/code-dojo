# 03-错误处理、泛型与Trait

Rust错误处理显式明确，泛型实现零成本抽象，Trait定义共享行为。

## 错误处理

Rust无异常机制，错误分两类：可恢复（Result<T, E>）和不可恢复（panic!）。

### panic!

不可恢复错误，程序终止。

```rust
// 主动panic
panic!("crash and burn");

// 数组越界等会panic
let v = vec![1, 2, 3];
v[99];  // panic!

// panic时的行为
// 1. 展开（unwind）：清理栈（默认）
// 2. 中止（abort）：直接终止，OS清理

// Cargo.toml设置：
// [profile.release]
// panic = 'abort'
```

### Result<T, E>

可恢复错误。

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}

use std::fs::File;

// 基本使用
let f = File::open("hello.txt");

let f = match f {
    Ok(file) => file,
    Err(error) => {
        panic!("打开文件失败: {:?}", error);
    },
};

// 匹配不同错误
use std::io::ErrorKind;

let f = File::open("hello.txt");

let f = match f {
    Ok(file) => file,
    Err(error) => match error.kind() {
        ErrorKind::NotFound => match File::create("hello.txt") {
            Ok(fc) => fc,
            Err(e) => panic!("创建文件失败: {:?}", e),
        },
        other_error => panic!("打开文件失败: {:?}", other_error),
    },
};

// 简化版（闭包）
let f = File::open("hello.txt").unwrap_or_else(|error| {
    if error.kind() == ErrorKind::NotFound {
        File::create("hello.txt").unwrap_or_else(|error| {
            panic!("创建文件失败: {:?}", error);
        })
    } else {
        panic!("打开文件失败: {:?}", error);
    }
});
```

### unwrap和expect

```rust
// unwrap：Ok返回值，Err则panic
let f = File::open("hello.txt").unwrap();

// expect：自定义panic消息
let f = File::open("hello.txt").expect("无法打开hello.txt");
```

### 传播错误

```rust
use std::io;
use std::fs::File;
use std::io::Read;

// 手动传播
fn read_username_from_file() -> Result<String, io::Error> {
    let f = File::open("hello.txt");

    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    let mut s = String::new();

    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
}

// ? 运算符（简化）
fn read_username_from_file() -> Result<String, io::Error> {
    let mut f = File::open("hello.txt")?;  // 错误自动返回
    let mut s = String::new();
    f.read_to_string(&mut s)?;
    Ok(s)
}

// 链式调用
fn read_username_from_file() -> Result<String, io::Error> {
    let mut s = String::new();
    File::open("hello.txt")?.read_to_string(&mut s)?;
    Ok(s)
}

// 更简洁
fn read_username_from_file() -> Result<String, io::Error> {
    std::fs::read_to_string("hello.txt")
}

// ? 用于Option
fn last_char_of_first_line(text: &str) -> Option<char> {
    text.lines().next()?.chars().last()
}
```

### 自定义错误类型

```rust
use std::fmt;

#[derive(Debug)]
enum MyError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
}

impl fmt::Display for MyError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            MyError::Io(err) => write!(f, "IO错误: {}", err),
            MyError::Parse(err) => write!(f, "解析错误: {}", err),
        }
    }
}

impl std::error::Error for MyError {}

// From trait自动转换
impl From<std::io::Error> for MyError {
    fn from(err: std::io::Error) -> Self {
        MyError::Io(err)
    }
}

impl From<std::num::ParseIntError> for MyError {
    fn from(err: std::num::ParseIntError) -> Self {
        MyError::Parse(err)
    }
}

// 使用
fn process() -> Result<i32, MyError> {
    let file_content = std::fs::read_to_string("number.txt")?;  // IO错误自动转换
    let number: i32 = file_content.trim().parse()?;  // 解析错误自动转换
    Ok(number)
}
```

### anyhow和thiserror

```rust
// anyhow：应用程序错误（简单）
use anyhow::{Context, Result};

fn read_config() -> Result<String> {
    let content = std::fs::read_to_string("config.toml")
        .context("读取配置文件失败")?;
    Ok(content)
}

// thiserror：库错误（定义错误类型）
use thiserror::Error;

#[derive(Error, Debug)]
enum DataError {
    #[error("IO错误: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("解析错误: {0}")]
    Parse(#[from] std::num::ParseIntError),
    
    #[error("无效数据: {0}")]
    Invalid(String),
}
```

## 泛型

### 函数泛型

```rust
// 找最大值（具体类型）
fn largest_i32(list: &[i32]) -> i32 {
    let mut largest = list[0];
    for &item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

// 泛型版本
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];
    for &item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

let number_list = vec![34, 50, 25, 100, 65];
let result = largest(&number_list);

let char_list = vec!['y', 'm', 'a', 'q'];
let result = largest(&char_list);
```

### 结构体泛型

```rust
struct Point<T> {
    x: T,
    y: T,
}

let integer = Point { x: 5, y: 10 };
let float = Point { x: 1.0, y: 4.0 };

// 多个类型参数
struct Point<T, U> {
    x: T,
    y: U,
}

let both_integer = Point { x: 5, y: 10 };
let both_float = Point { x: 1.0, y: 4.0 };
let integer_and_float = Point { x: 5, y: 4.0 };
```

### 枚举泛型

```rust
enum Option<T> {
    Some(T),
    None,
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

### 方法泛型

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

// 只为特定类型实现
impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}

// 方法上的额外泛型
impl<T, U> Point<T, U> {
    fn mixup<V, W>(self, other: Point<V, W>) -> Point<T, W> {
        Point {
            x: self.x,
            y: other.y,
        }
    }
}

let p1 = Point { x: 5, y: 10.4 };
let p2 = Point { x: "Hello", y: 'c' };
let p3 = p1.mixup(p2);  // Point { x: 5, y: 'c' }
```

### 零成本抽象

泛型编译期单态化（monomorphization），运行时无开销。

```rust
// 泛型代码
let integer = Some(5);
let float = Some(5.0);

// 编译后等效于
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

let integer = Option_i32::Some(5);
let float = Option_f64::Some(5.0);
```

## Trait

定义共享行为，类似接口。

### 定义和实现

```rust
pub trait Summary {
    fn summarize(&self) -> String;
}

pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

pub struct Tweet {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub retweet: bool,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}

// 使用
let tweet = Tweet {
    username: String::from("horse_ebooks"),
    content: String::from("of course, as you probably already know, people"),
    reply: false,
    retweet: false,
};

println!("1 new tweet: {}", tweet.summarize());
```

### 默认实现

```rust
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")  // 默认实现
    }
}

// 使用默认实现
impl Summary for NewsArticle {}

let article = NewsArticle { /* ... */ };
println!("{}", article.summarize());  // "(Read more...)"

// 默认实现可调用其他方法
pub trait Summary {
    fn summarize_author(&self) -> String;

    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}
```

### Trait作为参数

```rust
// Trait bound语法
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

// impl Trait语法糖
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}

// 多个trait
pub fn notify(item: &(impl Summary + Display)) {
    // ...
}

pub fn notify<T: Summary + Display>(item: &T) {
    // ...
}

// where子句（复杂约束）
fn some_function<T, U>(t: &T, u: &U) -> i32
    where T: Display + Clone,
          U: Clone + Debug
{
    // ...
}
```

### 返回Trait

```rust
// 返回实现了trait的类型
fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("horse_ebooks"),
        content: String::from("of course, as you probably already know, people"),
        reply: false,
        retweet: false,
    }
}

// ❌ 错误：不能返回不同类型
fn returns_summarizable(switch: bool) -> impl Summary {
    if switch {
        NewsArticle { /* ... */ }
    } else {
        Tweet { /* ... */ }  // 错误：类型不一致
    }
}
```

### 有条件的实现

```rust
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
}

// 只为实现了Display + PartialOrd的类型实现
impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("最大值是 x = {}", self.x);
        } else {
            println!("最大值是 y = {}", self.y);
        }
    }
}
```

### Blanket实现

```rust
// 为所有实现了Display的类型实现ToString
impl<T: Display> ToString for T {
    // ...
}

// 因此任何Display类型都有to_string方法
let s = 3.to_string();
```

### 常用Trait

```rust
// Clone：深拷贝
#[derive(Clone)]
struct MyStruct;

// Copy：栈拷贝（只能是简单类型）
#[derive(Copy, Clone)]
struct Point { x: i32, y: i32 }

// Debug：调试输出
#[derive(Debug)]
struct Rectangle { width: u32, height: u32 }
println!("{:?}", rect);

// Display：用户友好输出
use std::fmt;

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

// PartialEq, Eq：相等比较
#[derive(PartialEq, Eq)]
struct Person { name: String }

// PartialOrd, Ord：排序
#[derive(PartialOrd, Ord)]
struct Priority(i32);

// Default：默认值
#[derive(Default)]
struct Config {
    name: String,
    count: i32,
}
let config = Config::default();

// From/Into：类型转换
impl From<i32> for MyType {
    fn from(n: i32) -> Self {
        MyType(n)
    }
}

let my_type: MyType = 5.into();
```

## 生命周期

确保引用有效，编译期检查。

### 基本语法

```rust
// 函数签名中的生命周期
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// 使用
let string1 = String::from("abcd");
let string2 = "xyz";

let result = longest(string1.as_str(), string2);
println!("最长的字符串是 {}", result);

// 生命周期含义：
// 返回值的生命周期与参数中较短的相同
```

### 结构体生命周期

```rust
struct ImportantExcerpt<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().expect("Could not find a '.'");
    let i = ImportantExcerpt { part: first_sentence };
}
```

### 生命周期省略规则

编译器自动推断生命周期的规则：

```rust
// 规则1：每个引用参数都有独立生命周期
fn foo<'a, 'b>(x: &'a i32, y: &'b i32)

// 规则2：只有一个输入生命周期，赋给所有输出
fn foo<'a>(x: &'a i32) -> &'a i32

// 规则3：方法中，返回值生命周期赋给&self
impl<'a> ImportantExcerpt<'a> {
    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention please: {}", announcement);
        self.part  // 返回值生命周期等于&self
    }
}
```

### 静态生命周期

```rust
// 'static：整个程序运行期间
let s: &'static str = "I have a static lifetime.";

// 所有字符串字面量都是'static
```

## 高级Trait

### 关联类型

```rust
pub trait Iterator {
    type Item;  // 关联类型

    fn next(&mut self) -> Option<Self::Item>;
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        // ...
    }
}

// vs 泛型
pub trait Iterator<T> {
    fn next(&mut self) -> Option<T>;
}

// 关联类型：只能有一个实现
// 泛型：可以有多个实现（如Iterator<String>和Iterator<i32>）
```

### 运算符重载

```rust
use std::ops::Add;

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

assert_eq!(
    Point { x: 1, y: 0 } + Point { x: 2, y: 3 },
    Point { x: 3, y: 3 }
);
```

### Deref trait

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

let x = 5;
let y = MyBox(x);

assert_eq!(5, *y);  // *y -> *(y.deref())
```

### Drop trait

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer { data: String::from("my stuff") };
    let d = CustomSmartPointer { data: String::from("other stuff") };
    println!("创建了CustomSmartPointers");
}  // 离开作用域，先drop d，再drop c

// 提前drop
drop(c);  // 显式调用std::mem::drop
```

## 最佳实践

### 错误处理

```rust
// ✓ 库：返回Result，让调用者决定
pub fn read_file(path: &str) -> Result<String, io::Error> {
    std::fs::read_to_string(path)
}

// ✓ 应用：合适位置处理错误
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let content = read_file("config.toml")?;
    // ...
    Ok(())
}

// ❌ 避免：过度unwrap
let file = File::open("file.txt").unwrap();  // 生产代码少用

// ✓ 合理panic：逻辑错误、不可恢复错误
if index > MAX_INDEX {
    panic!("索引越界: {}", index);
}
```

### 泛型使用

```rust
// ✓ 简洁约束
fn print<T: Display>(t: T) {
    println!("{}", t);
}

// ✓ 复杂约束用where
fn complex<T, U>(t: T, u: U)
where
    T: Display + Clone,
    U: Debug + Clone,
{
    // ...
}
```

### Trait设计

```rust
// ✓ 小而专注
trait Read {
    fn read(&mut self, buf: &mut [u8]) -> Result<usize>;
}

// ✓ 提供默认实现
trait Logger {
    fn log(&self, message: &str) {
        println!("[LOG] {}", message);
    }
}

// ✓ 使用关联类型简化
trait Container {
    type Item;
    fn get(&self, index: usize) -> Option<&Self::Item>;
}
```

**核心：** 错误处理显式、泛型零成本、Trait灵活强大，是Rust类型系统的核心。

