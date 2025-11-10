# 02-Rust基础语法

Rust语法简洁现代，吸收函数式和面向对象优点。强类型系统，编译期保证安全。

## 变量和可变性

### 变量声明

```rust
// 不可变变量（默认）
let x = 5;
// x = 6;  // ❌ 错误：不可变

// 可变变量
let mut y = 5;
y = 6;  // ✓ OK

// 类型注解
let z: i32 = 5;

// 模式匹配解构
let (a, b) = (1, 2);
let [first, second] = [10, 20];
```

### 常量

```rust
// 常量：类型必须注解，命名全大写
const MAX_POINTS: u32 = 100_000;  // 下划线提高可读性
const PI: f64 = 3.14159;

// 常量vs不可变变量
// 1. 常量不能用mut
// 2. 常量必须注解类型
// 3. 常量只能是常量表达式，不能是运行时计算
// 4. 常量可在任意作用域声明，包括全局
```

### 遮蔽（Shadowing）

```rust
let x = 5;
let x = x + 1;  // 遮蔽，x=6
{
    let x = x * 2;  // 内层遮蔽，x=12
    println!("{}", x);  // 12
}
println!("{}", x);  // 6

// 遮蔽可改变类型
let spaces = "   ";
let spaces = spaces.len();  // ✓ OK，类型从&str变为usize

// mut不能改变类型
let mut spaces = "   ";
// spaces = spaces.len();  // ❌ 错误：类型不匹配
```

## 数据类型

### 标量类型

```rust
// 整数
i8, i16, i32, i64, i128, isize  // 有符号
u8, u16, u32, u64, u128, usize  // 无符号

let a: u8 = 255;
let b: i32 = -42;
let c = 98_222;       // 98222
let d = 0xff;         // 255（十六进制）
let e = 0o77;         // 63（八进制）
let f = 0b1111_0000;  // 240（二进制）
let g = b'A';         // 65（字节，仅u8）

// 浮点数
f32, f64  // 默认f64

let x = 2.0;       // f64
let y: f32 = 3.0;  // f32

// 布尔
let t = true;
let f: bool = false;

// 字符（4字节Unicode）
let c = 'z';
let emoji = '😻';
let chinese = '中';
```

### 复合类型

```rust
// 元组：固定长度，不同类型
let tup: (i32, f64, u8) = (500, 6.4, 1);

let (x, y, z) = tup;  // 解构
let five_hundred = tup.0;  // 索引访问

// 单元类型（空元组）
let unit = ();  // 类型：()，函数无返回值时返回

// 数组：固定长度，相同类型
let a = [1, 2, 3, 4, 5];
let a: [i32; 5] = [1, 2, 3, 4, 5];  // 类型：[i32; 5]
let a = [3; 5];  // [3, 3, 3, 3, 3]

let first = a[0];
let second = a[1];

// 数组越界检查（运行时）
// let element = a[10];  // panic!
```

## 函数

### 函数定义

```rust
// 基本函数
fn greet() {
    println!("Hello!");
}

// 参数（必须类型注解）
fn greet(name: &str) {
    println!("Hello, {}!", name);
}

// 多参数
fn add(x: i32, y: i32) -> i32 {
    x + y  // 表达式，无分号
}

// 返回值（必须类型注解）
fn five() -> i32 {
    5  // 隐式返回
}

fn plus_one(x: i32) -> i32 {
    x + 1  // ✓ 表达式
    // x + 1;  // ❌ 语句，返回()
}

// 提前返回
fn check(x: i32) -> i32 {
    if x < 0 {
        return 0;  // 提前返回
    }
    x
}

// 无返回值（返回()）
fn print_num(x: i32) {
    println!("{}", x);
}

// 发散函数（永不返回）
fn infinite_loop() -> ! {
    loop {
        println!("forever");
    }
}

fn exit_program() -> ! {
    std::process::exit(0);
}
```

### 语句和表达式

```rust
// 语句：不返回值
let x = 5;

// 表达式：返回值
5
x + 1
{
    let x = 3;
    x + 1  // 表达式，返回4
}

// if是表达式
let number = if condition { 5 } else { 6 };

// 块是表达式
let y = {
    let x = 3;
    x + 1  // 返回4
};
```

## 控制流

### if表达式

```rust
let number = 6;

if number < 5 {
    println!("条件为真");
} else if number == 5 {
    println!("等于5");
} else {
    println!("条件为假");
}

// if是表达式
let condition = true;
let number = if condition { 5 } else { 6 };

// ❌ 错误：类型必须一致
// let number = if condition { 5 } else { "six" };
```

### loop循环

```rust
// 无限循环
loop {
    println!("again!");
}

// 返回值
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;  // 返回20
    }
};

// 循环标签
'outer: loop {
    loop {
        break 'outer;  // 跳出外层循环
    }
}
```

### while循环

```rust
let mut number = 3;

while number != 0 {
    println!("{}!", number);
    number -= 1;
}

println!("LIFTOFF!");
```

### for循环

```rust
// 遍历集合
let a = [10, 20, 30, 40, 50];

for element in a {
    println!("{}", element);
}

// 范围
for number in 1..4 {  // 1, 2, 3
    println!("{}", number);
}

for number in 1..=4 {  // 1, 2, 3, 4（包含）
    println!("{}", number);
}

// 倒序
for number in (1..4).rev() {  // 3, 2, 1
    println!("{}", number);
}

// 带索引
for (i, value) in a.iter().enumerate() {
    println!("{}: {}", i, value);
}
```

## 结构体

### 定义和实例化

```rust
// 定义
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

// 实例化
let user1 = User {
    email: String::from("user@example.com"),
    username: String::from("user123"),
    active: true,
    sign_in_count: 1,
};

// 访问
println!("{}", user1.email);

// 可变
let mut user1 = User { /* ... */ };
user1.email = String::from("new@example.com");

// 字段初始化简写
fn build_user(email: String, username: String) -> User {
    User {
        email,     // 同名简写
        username,
        active: true,
        sign_in_count: 1,
    }
}

// 结构体更新语法
let user2 = User {
    email: String::from("another@example.com"),
    ..user1  // 其余字段从user1复制（移动所有权）
};
```

### 元组结构体

```rust
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

let black = Color(0, 0, 0);
let origin = Point(0, 0, 0);

// 访问
println!("{}", black.0);
```

### 单元结构体

```rust
struct AlwaysEqual;

let subject = AlwaysEqual;
```

### 方法

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    // 方法（&self）
    fn area(&self) -> u32 {
        self.width * self.height
    }
    
    // 可变方法
    fn double(&mut self) {
        self.width *= 2;
        self.height *= 2;
    }
    
    // 获取所有权（少见）
    fn consume(self) -> u32 {
        self.width * self.height
    }
    
    // 关联函数（无self）
    fn square(size: u32) -> Rectangle {
        Rectangle {
            width: size,
            height: size,
        }
    }
    
    // 多个参数
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

// 使用
let rect = Rectangle { width: 30, height: 50 };
println!("面积：{}", rect.area());

let sq = Rectangle::square(10);  // 关联函数用::调用
```

## 枚举

### 定义

```rust
// 基本枚举
enum IpAddrKind {
    V4,
    V6,
}

let four = IpAddrKind::V4;
let six = IpAddrKind::V6;

// 带数据的枚举
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1);
let loopback = IpAddr::V6(String::from("::1"));

// 复杂枚举
enum Message {
    Quit,                       // 无数据
    Move { x: i32, y: i32 },    // 匿名结构体
    Write(String),              // 单个String
    ChangeColor(i32, i32, i32), // 三个i32
}

// 枚举也可以有方法
impl Message {
    fn call(&self) {
        // ...
    }
}

let m = Message::Write(String::from("hello"));
m.call();
```

### Option枚举

```rust
// 标准库定义（无需导入）
enum Option<T> {
    Some(T),
    None,
}

let some_number = Some(5);
let some_string = Some("a string");
let absent_number: Option<i32> = None;

// 必须处理None
// let x: i32 = some_number;  // ❌ 错误：类型不匹配

// 正确处理
if let Some(x) = some_number {
    println!("{}", x);
}

match some_number {
    Some(x) => println!("{}", x),
    None => println!("无值"),
}
```

## match表达式

### 基本用法

```rust
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }  // match是表达式
}

// 绑定值
enum UsState {
    Alabama,
    Alaska,
    // ...
}

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState),
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("州: {:?}", state);
            25
        }
    }
}
```

### 匹配Option

```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}

let five = Some(5);
let six = plus_one(five);
let none = plus_one(None);
```

### 通配符和_

```rust
let dice_roll = 9;

match dice_roll {
    3 => add_fancy_hat(),
    7 => remove_fancy_hat(),
    other => move_player(other),  // 绑定其他值
}

match dice_roll {
    3 => add_fancy_hat(),
    7 => remove_fancy_hat(),
    _ => (),  // 忽略其他值
}
```

## if let

简化只匹配一个模式的match。

```rust
let config_max = Some(3u8);

// match版本
match config_max {
    Some(max) => println!("最大值: {}", max),
    _ => (),
}

// if let简化版
if let Some(max) = config_max {
    println!("最大值: {}", max);
}

// 带else
if let Some(max) = config_max {
    println!("最大值: {}", max);
} else {
    println!("无值");
}
```

## 模式匹配

### 解构

```rust
// 解构结构体
struct Point {
    x: i32,
    y: i32,
}

let p = Point { x: 0, y: 7 };

let Point { x: a, y: b } = p;  // a=0, b=7
let Point { x, y } = p;  // 简写

match p {
    Point { x, y: 0 } => println!("在x轴上: {}", x),
    Point { x: 0, y } => println!("在y轴上: {}", y),
    Point { x, y } => println!("({}, {})", x, y),
}

// 解构枚举
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

match msg {
    Message::Quit => {},
    Message::Move { x, y } => {},
    Message::Write(text) => {},
    Message::ChangeColor(r, g, b) => {},
}

// 解构元组
let ((feet, inches), Point { x, y }) = ((3, 10), Point { x: 3, y: -10 });
```

### 守卫（Guard）

```rust
let num = Some(4);

match num {
    Some(x) if x < 5 => println!("小于5: {}", x),
    Some(x) => println!("{}", x),
    None => (),
}

// 多个模式
let x = 4;
let y = false;

match x {
    4 | 5 | 6 if y => println!("yes"),  // (4 | 5 | 6) && y
    _ => println!("no"),
}
```

### @绑定

```rust
enum Message {
    Hello { id: i32 },
}

let msg = Message::Hello { id: 5 };

match msg {
    Message::Hello { id: id_variable @ 3..=7 } => {
        println!("ID在范围内: {}", id_variable);
    }
    Message::Hello { id: 10..=12 } => {
        println!("ID在另一范围");
    }
    Message::Hello { id } => {
        println!("其他ID: {}", id);
    }
}
```

## Vector

动态数组。

```rust
// 创建
let v: Vec<i32> = Vec::new();
let v = vec![1, 2, 3];  // 宏

// 添加
let mut v = Vec::new();
v.push(5);
v.push(6);
v.push(7);

// 访问
let v = vec![1, 2, 3, 4, 5];

let third = &v[2];  // 索引（可能panic）
let third = v.get(2);  // Option<&T>（安全）

match v.get(2) {
    Some(third) => println!("第三个元素: {}", third),
    None => println!("无此元素"),
}

// 遍历
let v = vec![100, 32, 57];
for i in &v {
    println!("{}", i);
}

// 可变遍历
let mut v = vec![100, 32, 57];
for i in &mut v {
    *i += 50;
}

// 存储不同类型（用枚举）
enum SpreadsheetCell {
    Int(i32),
    Float(f64),
    Text(String),
}

let row = vec![
    SpreadsheetCell::Int(3),
    SpreadsheetCell::Text(String::from("blue")),
    SpreadsheetCell::Float(10.12),
];
```

## String

```rust
// 创建
let s = String::new();
let s = "initial contents".to_string();
let s = String::from("initial contents");

// 更新
let mut s = String::from("foo");
s.push_str("bar");  // "foobar"
s.push('!');        // "foobar!"

// 拼接
let s1 = String::from("Hello, ");
let s2 = String::from("world!");
let s3 = s1 + &s2;  // s1被移动，s2仍可用

// format!宏（推荐）
let s1 = String::from("tic");
let s2 = String::from("tac");
let s3 = String::from("toe");
let s = format!("{}-{}-{}", s1, s2, s3);  // 不获取所有权

// 索引（❌ 不支持）
let s1 = String::from("hello");
// let h = s1[0];  // 错误

// 切片（小心，可能panic）
let hello = "Здравствуйте";
let s = &hello[0..4];  // "Зд"（每个字母2字节）

// 遍历
for c in "नमस्ते".chars() {
    println!("{}", c);
}

for b in "नमस्ते".bytes() {
    println!("{}", b);
}
```

## HashMap

```rust
use std::collections::HashMap;

// 创建
let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);

// 从Vec创建
let teams = vec![String::from("Blue"), String::from("Yellow")];
let initial_scores = vec![10, 50];
let scores: HashMap<_, _> = teams.iter().zip(initial_scores.iter()).collect();

// 访问
let team_name = String::from("Blue");
let score = scores.get(&team_name);  // Option<&V>

match scores.get(&team_name) {
    Some(score) => println!("{}", score),
    None => println!("无此队伍"),
}

// 遍历
for (key, value) in &scores {
    println!("{}: {}", key, value);
}

// 更新
scores.insert(String::from("Blue"), 25);  // 覆盖

// 仅当不存在时插入
scores.entry(String::from("Blue")).or_insert(50);

// 基于旧值更新
let text = "hello world wonderful world";
let mut map = HashMap::new();

for word in text.split_whitespace() {
    let count = map.entry(word).or_insert(0);
    *count += 1;
}

println!("{:?}", map);  // {"hello": 1, "world": 2, "wonderful": 1}
```

## 类型别名

```rust
type Kilometers = i32;

let x: i32 = 5;
let y: Kilometers = 5;

// x和y是同一类型
```

## 迭代器

### 基本用法

```rust
let v = vec![1, 2, 3, 4, 5];

// for循环自动调用into_iter
for item in v {
    println!("{}", item);  // v被消耗
}

// 三种迭代器
let v = vec![1, 2, 3];

// iter()：不可变引用
for item in v.iter() {
    println!("{}", item);  // item是&i32
}

// iter_mut()：可变引用
for item in v.iter_mut() {
    *item += 1;
}

// into_iter()：获取所有权
for item in v.into_iter() {
    println!("{}", item);  // item是i32，v被消耗
}
```

### 迭代器适配器

```rust
let v = vec![1, 2, 3, 4, 5];

// map：转换
let doubled: Vec<i32> = v.iter().map(|x| x * 2).collect();

// filter：过滤
let evens: Vec<&i32> = v.iter().filter(|x| *x % 2 == 0).collect();

// chain：连接
let v1 = vec![1, 2, 3];
let v2 = vec![4, 5, 6];
let combined: Vec<i32> = v1.iter().chain(v2.iter()).cloned().collect();

// zip：配对
let names = vec!["Alice", "Bob"];
let ages = vec![25, 30];
let pairs: Vec<_> = names.iter().zip(ages.iter()).collect();
// [("Alice", 25), ("Bob", 30)]

// enumerate：带索引
for (i, val) in v.iter().enumerate() {
    println!("{}: {}", i, val);
}

// take：取前N个
let first_three: Vec<&i32> = v.iter().take(3).collect();

// skip：跳过前N个
let skip_two: Vec<&i32> = v.iter().skip(2).collect();

// fold：累积
let sum = v.iter().fold(0, |acc, x| acc + x);

// any/all
let has_even = v.iter().any(|x| x % 2 == 0);
let all_positive = v.iter().all(|x| *x > 0);

// find：查找第一个
let found = v.iter().find(|&&x| x > 3);  // Some(&4)
```

### 性能技巧

```rust
// ❌ 低效：多次collect
let v = vec![1, 2, 3, 4, 5];
let doubled: Vec<i32> = v.iter().map(|x| x * 2).collect();
let filtered: Vec<i32> = doubled.iter().filter(|x| *x > 4).cloned().collect();

// ✅ 高效：链式调用
let result: Vec<i32> = v.iter()
    .map(|x| x * 2)
    .filter(|x| *x > 4)
    .cloned()
    .collect();

// ❌ 低效：重复遍历
let sum: i32 = v.iter().sum();
let count = v.iter().count();

// ✅ 高效：一次遍历
let (sum, count) = v.iter().fold((0, 0), |(sum, count), x| {
    (sum + x, count + 1)
});
```

## 闭包

### 语法和捕获

```rust
// 完整语法
let add = |x: i32, y: i32| -> i32 { x + y };

// 类型推断
let add = |x, y| x + y;

// 单表达式
let square = |x| x * x;

// 捕获环境
let factor = 2;
let multiply = |x| x * factor;  // 捕获factor

// 三种捕获方式
let s = String::from("hello");

// 1. 不可变借用（Fn）
let print = || println!("{}", s);
print();
println!("{}", s);  // s仍可用

// 2. 可变借用（FnMut）
let mut s = String::from("hello");
let mut append = || s.push_str(" world");
append();
// println!("{}", s);  // 错误：s被可变借用

// 3. 获取所有权（FnOnce）
let s = String::from("hello");
let consume = move || {
    let _s = s;  // s移入闭包
};
consume();
// consume();  // 错误：FnOnce只能调用一次
```

### 闭包作为参数

```rust
// 接受闭包
fn apply<F>(f: F, x: i32) -> i32
where
    F: Fn(i32) -> i32,
{
    f(x)
}

let result = apply(|x| x * 2, 5);  // 10

// 返回闭包
fn make_adder(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x + n
}

let add_five = make_adder(5);
println!("{}", add_five(3));  // 8
```

## 高级模式匹配

### 范围匹配

```rust
let x = 5;

match x {
    1..=5 => println!("1到5"),
    6..=10 => println!("6到10"),
    _ => println!("其他"),
}

// 字符范围
let c = 'c';
match c {
    'a'..='j' => println!("前10个字母"),
    'k'..='z' => println!("后面的字母"),
    _ => println!("其他"),
}
```

### 解构嵌套

```rust
enum Color {
    Rgb(u8, u8, u8),
    Hsv(u8, u8, u8),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(Color),
}

let msg = Message::ChangeColor(Color::Rgb(0, 160, 255));

match msg {
    Message::ChangeColor(Color::Rgb(r, g, b)) => {
        println!("RGB({}, {}, {})", r, g, b);
    }
    Message::ChangeColor(Color::Hsv(h, s, v)) => {
        println!("HSV({}, {}, {})", h, s, v);
    }
    Message::Move { x, y } => {
        println!("Move to ({}, {})", x, y);
    }
    _ => {}
}
```

### 模式中的引用

```rust
let s = Some(String::from("hello"));

// ❌ 所有权移动
match s {
    Some(text) => println!("{}", text),
    None => (),
}
// println!("{:?}", s);  // 错误：s已被move

// ✅ 使用ref
let s = Some(String::from("hello"));
match s {
    Some(ref text) => println!("{}", text),  // text是&String
    None => (),
}
println!("{:?}", s);  // OK

// ✅ 匹配引用
let s = Some(String::from("hello"));
match &s {
    Some(text) => println!("{}", text),  // text是&String
    None => (),
}
println!("{:?}", s);  // OK
```

### 多模式和守卫组合

```rust
let num = Some(4);

match num {
    Some(x) if x < 5 => println!("小于5: {}", x),
    Some(x @ 1..=5) => println!("1到5: {}", x),
    Some(x @ 10 | x @ 20) => println!("10或20: {}", x),
    Some(x) => println!("其他: {}", x),
    None => (),
}
```

## Ranges

```rust
// 范围类型
let r1 = 1..5;        // 1,2,3,4
let r2 = 1..=5;       // 1,2,3,4,5
let r3 = ..5;         // 0,1,2,3,4
let r4 = 1..;         // 1,2,3,...（无限）
let r5 = ..;          // 完整范围

// 范围迭代
for i in 1..5 {
    println!("{}", i);
}

// 范围索引
let s = "hello";
let slice = &s[1..4];  // "ell"

// 范围包含判断
let r = 1..10;
println!("{}", r.contains(&5));  // true

// 范围作为迭代器
let sum: i32 = (1..=100).sum();  // 5050
```

## 宏基础

```rust
// vec! 宏展开
let v = vec![1, 2, 3];
// 等价于：
let mut temp = Vec::new();
temp.push(1);
temp.push(2);
temp.push(3);
let v = temp;

// println! 是宏
println!("Hello");           // 无参数
println!("x = {}", x);       // 格式化
println!("x = {x}");         // 捕获变量（Rust 2021）
println!("{:?}", v);         // Debug格式
println!("{:#?}", v);        // 漂亮打印

// dbg! 宏（调试）
let x = 5;
dbg!(x);  // 打印：[src/main.rs:2] x = 5

let result = dbg!(x + 1);  // 返回值
```

**核心：** Rust语法简洁，类型系统完备，模式匹配功能丰富。所有权是理解其他特性的基础。

