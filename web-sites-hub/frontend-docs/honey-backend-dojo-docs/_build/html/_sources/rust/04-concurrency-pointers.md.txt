# 04-并发与智能指针

Rust通过所有权系统实现无数据竞争的并发，智能指针提供灵活内存管理。

## 智能指针

智能指针是实现了`Deref`和`Drop` trait的数据结构，拥有所指数据。

### Box<T>

堆分配，最简单的智能指针。

```rust
// 基本使用
let b = Box::new(5);
println!("{}", b);

// 应用场景1：递归类型
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));

// 应用场景2：大数据转移所有权（避免栈拷贝）
let large_data = Box::new([0; 1000000]);

// 应用场景3：Trait对象
trait Draw {
    fn draw(&self);
}

let objects: Vec<Box<dyn Draw>> = vec![/* ... */];
```

### Deref trait

解引用强制转换。

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

// 使用
let x = 5;
let y = MyBox::new(x);

assert_eq!(5, *y);  // *y -> *(y.deref())

// 解引用强制转换
fn hello(name: &str) {
    println!("Hello, {}!", name);
}

let m = MyBox::new(String::from("Rust"));
hello(&m);  // &MyBox<String> -> &String -> &str
```

### Drop trait

自动清理资源。

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
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };
    println!("Created CustomSmartPointers.");
}  // d先drop，然后c

// 提前drop
let c = CustomSmartPointer { data: String::from("some data") };
println!("Created.");
drop(c);  // 显式drop
println!("Dropped before end.");
```

### Rc<T>

引用计数，单线程多所有者。

```rust
use std::rc::Rc;

enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use List::{Cons, Nil};

let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
println!("count after creating a = {}", Rc::strong_count(&a));  // 1

let b = Cons(3, Rc::clone(&a));  // 引用计数+1
println!("count after creating b = {}", Rc::strong_count(&a));  // 2

{
    let c = Cons(4, Rc::clone(&a));
    println!("count after creating c = {}", Rc::strong_count(&a));  // 3
}

println!("count after c goes out of scope = {}", Rc::strong_count(&a));  // 2

// ❌ Rc不能修改
// let value = Rc::get_mut(&mut a).unwrap();
```

### RefCell<T>

内部可变性，运行时借用检查。

```rust
use std::cell::RefCell;

let data = RefCell::new(5);

*data.borrow_mut() += 1;  // 可变借用
println!("{}", *data.borrow());  // 6

// 违反借用规则会panic（运行时）
let a = RefCell::new(5);
let b = a.borrow_mut();
// let c = a.borrow_mut();  // panic!：已有可变借用
```

### Rc<RefCell<T>>

多所有者+可变性。

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use List::{Cons, Nil};

let value = Rc::new(RefCell::new(5));

let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));
let b = Cons(Rc::new(RefCell::new(3)), Rc::clone(&a));
let c = Cons(Rc::new(RefCell::new(4)), Rc::clone(&a));

*value.borrow_mut() += 10;  // 修改共享值

println!("a = {:?}", a);
println!("b = {:?}", b);
println!("c = {:?}", c);
```

### 循环引用和Weak<T>

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

#[derive(Debug)]
struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

let leaf = Rc::new(Node {
    value: 3,
    parent: RefCell::new(Weak::new()),
    children: RefCell::new(vec![]),
});

println!(
    "leaf strong = {}, weak = {}",
    Rc::strong_count(&leaf),
    Rc::weak_count(&leaf),
);

{
    let branch = Rc::new(Node {
        value: 5,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![Rc::clone(&leaf)]),
    });

    *leaf.parent.borrow_mut() = Rc::downgrade(&branch);

    println!(
        "branch strong = {}, weak = {}",
        Rc::strong_count(&branch),
        Rc::weak_count(&branch),
    );

    println!(
        "leaf strong = {}, weak = {}",
        Rc::strong_count(&leaf),
        Rc::weak_count(&leaf),
    );
}

println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
```

## 并发

### 线程

```rust
use std::thread;
use std::time::Duration;

// 创建线程
let handle = thread::spawn(|| {
    for i in 1..10 {
        println!("spawned thread: {}", i);
        thread::sleep(Duration::from_millis(1));
    }
});

for i in 1..5 {
    println!("main thread: {}", i);
    thread::sleep(Duration::from_millis(1));
}

handle.join().unwrap();  // 等待线程结束

// move闭包
let v = vec![1, 2, 3];

let handle = thread::spawn(move || {
    println!("vector: {:?}", v);  // v所有权移入
});

handle.join().unwrap();
```

### 消息传递

Channel：多生产者单消费者。

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    let val = String::from("hi");
    tx.send(val).unwrap();
    // println!("{}", val);  // ❌ val已被move
});

let received = rx.recv().unwrap();  // 阻塞接收
println!("Got: {}", received);

// 尝试接收（非阻塞）
match rx.try_recv() {
    Ok(val) => println!("Got: {}", val),
    Err(_) => println!("No message"),
}

// 多生产者
let (tx, rx) = mpsc::channel();

let tx1 = tx.clone();
thread::spawn(move || {
    tx.send(String::from("hi from thread")).unwrap();
});

thread::spawn(move || {
    tx1.send(String::from("hi from another thread")).unwrap();
});

for received in rx {
    println!("Got: {}", received);
}
```

### 共享状态

Mutex：互斥锁。

```rust
use std::sync::Mutex;

let m = Mutex::new(5);

{
    let mut num = m.lock().unwrap();  // 获取锁
    *num = 6;
}  // 离开作用域，自动释放锁

println!("m = {:?}", m);

// 多线程共享
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());  // 10
```

### Arc<T>

原子引用计数，线程安全的Rc。

```rust
use std::sync::Arc;
use std::thread;

let data = Arc::new(vec![1, 2, 3]);
let mut handles = vec![];

for _ in 0..10 {
    let data = Arc::clone(&data);
    let handle = thread::spawn(move || {
        println!("{:?}", data);
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}
```

### Send和Sync trait

编译器自动实现，标记线程安全。

```rust
// Send：可以在线程间转移所有权
// Sync：可以在线程间共享引用

// 几乎所有类型都是Send
// Rc<T>不是Send（单线程）
// RefCell<T>不是Send（单线程）

// 几乎所有类型都是Sync
// RefCell<T>不是Sync
// Rc<T>不是Sync

// 手动实现（不安全，谨慎）
// unsafe impl Send for MyType {}
// unsafe impl Sync for MyType {}
```

## 无畏并发

Rust通过类型系统在编译期消除数据竞争。

### 数据竞争

三个条件同时满足才会发生：
1. 两个或多个指针同时访问同一数据
2. 至少一个指针写数据
3. 没有同步机制

Rust编译器阻止同时满足这三个条件。

```rust
// ❌ 编译错误：数据竞争
let mut data = vec![1, 2, 3];

thread::spawn(|| {
    data.push(4);  // 错误：闭包借用了可变引用
});

data.push(5);  // 错误：主线程也在用

// ✅ 正确：用Mutex同步
let data = Arc::new(Mutex::new(vec![1, 2, 3]));

let data_clone = Arc::clone(&data);
thread::spawn(move || {
    let mut d = data_clone.lock().unwrap();
    d.push(4);
});

let mut d = data.lock().unwrap();
d.push(5);
```

### 并发模式

```rust
// 模式1：消息传递
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

// 生产者
thread::spawn(move || {
    for i in 0..10 {
        tx.send(i).unwrap();
    }
});

// 消费者
for received in rx {
    println!("{}", received);
}

// 模式2：共享状态
use std::sync::{Arc, Mutex};

let data = Arc::new(Mutex::new(0));

// Worker线程
let mut handles = vec![];
for _ in 0..10 {
    let data = Arc::clone(&data);
    handles.push(thread::spawn(move || {
        let mut num = data.lock().unwrap();
        *num += 1;
    }));
}

// 等待所有线程
for h in handles {
    h.join().unwrap();
}

// 模式3：线程池
use std::sync::{mpsc, Arc, Mutex};

struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Job>,
}

type Job = Box<dyn FnOnce() + Send + 'static>;

struct Worker {
    id: usize,
    thread: thread::JoinHandle<()>,
}

impl ThreadPool {
    fn new(size: usize) -> ThreadPool {
        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender }
    }

    fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        self.sender.send(job).unwrap();
    }
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || loop {
            let job = receiver.lock().unwrap().recv().unwrap();
            println!("Worker {} got a job", id);
            job();
        });

        Worker { id, thread }
    }
}
```

## 智能指针对比

| 类型 | 所有权 | 线程安全 | 可变性 | 用途 |
|------|--------|----------|--------|------|
| Box<T> | 单一 | 是 | 可变 | 堆分配 |
| Rc<T> | 多个 | 否 | 不可变 | 单线程共享 |
| Arc<T> | 多个 | 是 | 不可变 | 多线程共享 |
| RefCell<T> | 单一 | 否 | 可变 | 内部可变性 |
| Mutex<T> | 多个 | 是 | 可变 | 线程安全可变 |
| RwLock<T> | 多个 | 是 | 可变 | 读写锁 |

## 常见模式

### 单例模式

```rust
use std::sync::OnceLock;

static INSTANCE: OnceLock<Config> = OnceLock::new();

struct Config {
    value: String,
}

fn get_config() -> &'static Config {
    INSTANCE.get_or_init(|| Config {
        value: String::from("config value"),
    })
}
```

### 线程安全的计数器

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

static COUNTER: AtomicUsize = AtomicUsize::new(0);

fn increment() {
    COUNTER.fetch_add(1, Ordering::SeqCst);
}

fn get_count() -> usize {
    COUNTER.load(Ordering::SeqCst);
}
```

### 读写锁

```rust
use std::sync::RwLock;

let lock = RwLock::new(5);

// 读锁（可多个）
{
    let r1 = lock.read().unwrap();
    let r2 = lock.read().unwrap();
    println!("{}, {}", r1, r2);
}

// 写锁（独占）
{
    let mut w = lock.write().unwrap();
    *w += 1;
}
```

## 最佳实践

### 智能指针选择

```rust
// ✓ 默认用Box
let data = Box::new(MyStruct::new());

// ✓ 单线程多所有者用Rc
let shared = Rc::new(data);

// ✓ 多线程共享用Arc
let shared = Arc::new(data);

// ✓ 内部可变性用RefCell（单线程）
let cell = RefCell::new(data);

// ✓ 多线程可变用Mutex
let mutex = Arc::new(Mutex::new(data));
```

### 并发选择

```rust
// ✓ 任务间独立：消息传递
let (tx, rx) = mpsc::channel();

// ✓ 共享状态：Mutex
let counter = Arc::new(Mutex::new(0));

// ✓ 读多写少：RwLock
let data = Arc::new(RwLock::new(vec![]));

// ✓ 简单标志：AtomicBool
use std::sync::atomic::AtomicBool;
let flag = Arc::new(AtomicBool::new(false));
```

### 避免死锁

```rust
// ❌ 死锁：互相等待
let mutex1 = Arc::new(Mutex::new(0));
let mutex2 = Arc::new(Mutex::new(0));

// 线程1
let m1 = mutex1.clone();
let m2 = mutex2.clone();
thread::spawn(move || {
    let _g1 = m1.lock().unwrap();
    thread::sleep(Duration::from_millis(10));
    let _g2 = m2.lock().unwrap();  // 等待mutex2
});

// 线程2
let m1 = mutex1.clone();
let m2 = mutex2.clone();
thread::spawn(move || {
    let _g2 = m2.lock().unwrap();
    thread::sleep(Duration::from_millis(10));
    let _g1 = m1.lock().unwrap();  // 等待mutex1（死锁）
});

// ✓ 解决：固定加锁顺序
// 总是先锁mutex1，再锁mutex2
```

### 错误处理

```rust
// ✓ 处理lock失败
match mutex.lock() {
    Ok(guard) => { /* use guard */ },
    Err(poisoned) => {
        // Mutex中毒（持有者panic）
        let guard = poisoned.into_inner();  // 恢复
    }
}

// ✓ 处理join失败
match handle.join() {
    Ok(_) => println!("线程正常结束"),
    Err(e) => eprintln!("线程panic: {:?}", e),
}
```

**核心：** 所有权系统+类型系统实现无畏并发，编译期消除数据竞争。智能指针灵活管理内存，结合并发原语构建安全并发程序。

