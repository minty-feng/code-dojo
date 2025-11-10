# 05-异步编程

Rust异步编程通过async/await提供零成本异步抽象，Tokio是最流行的异步运行时。

## 异步基础

### async/await

```rust
// 异步函数
async fn hello() {
    println!("hello");
}

// 返回Future
fn hello() -> impl Future<Output = ()> {
    async {
        println!("hello");
    }
}

// 调用异步函数
#[tokio::main]
async fn main() {
    hello().await;  // await等待Future完成
}
```

### Future trait

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

// Future定义
trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

enum Poll<T> {
    Ready(T),     // 完成
    Pending,      // 未完成
}
```

## Tokio运行时

### 安装配置

```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

### 基本使用

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    println!("Hello");
    sleep(Duration::from_secs(1)).await;
    println!("World");
}

// 多线程运行时（默认）
#[tokio::main]

// 单线程运行时
#[tokio::main(flavor = "current_thread")]

// 手动创建运行时
use tokio::runtime::Runtime;

fn main() {
    let runtime = Runtime::new().unwrap();
    runtime.block_on(async {
        println!("Hello from async");
    });
}
```

## 异步任务

### 创建任务

```rust
use tokio::task;

#[tokio::main]
async fn main() {
    // 启动异步任务
    let handle = task::spawn(async {
        println!("async task");
        42
    });

    // 等待任务完成
    let result = handle.await.unwrap();
    println!("Result: {}", result);
}

// 多个任务并发
#[tokio::main]
async fn main() {
    let handle1 = task::spawn(async { 1 });
    let handle2 = task::spawn(async { 2 });

    let result1 = handle1.await.unwrap();
    let result2 = handle2.await.unwrap();

    println!("{} + {} = {}", result1, result2, result1 + result2);
}
```

### join和select

```rust
use tokio::join;

async fn task1() -> u32 {
    1
}

async fn task2() -> u32 {
    2
}

#[tokio::main]
async fn main() {
    // join：等待所有任务完成
    let (r1, r2) = join!(task1(), task2());
    println!("Results: {} {}", r1, r2);
}

// select：等待第一个完成
use tokio::select;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let task1 = async {
        sleep(Duration::from_secs(1)).await;
        "task1"
    };

    let task2 = async {
        sleep(Duration::from_millis(500)).await;
        "task2"
    };

    select! {
        result = task1 => println!("{} finished first", result),
        result = task2 => println!("{} finished first", result),
    }
}
```

## 异步I/O

### 文件I/O

```rust
use tokio::fs::File;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 读文件
    let mut file = File::open("foo.txt").await?;
    let mut contents = String::new();
    file.read_to_string(&mut contents).await?;
    println!("{}", contents);

    // 写文件
    let mut file = File::create("bar.txt").await?;
    file.write_all(b"hello world").await?;

    Ok(())
}

// 一次性读写
use tokio::fs;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let contents = fs::read_to_string("foo.txt").await?;
    fs::write("bar.txt", b"hello").await?;
    Ok(())
}
```

### 网络I/O

```rust
use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncReadExt, AsyncWriteExt};

// TCP服务器
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;

    loop {
        let (socket, _) = listener.accept().await?;
        tokio::spawn(async move {
            handle_client(socket).await;
        });
    }
}

async fn handle_client(mut socket: TcpStream) {
    let mut buf = [0; 1024];

    loop {
        let n = match socket.read(&mut buf).await {
            Ok(n) if n == 0 => return,  // 连接关闭
            Ok(n) => n,
            Err(e) => {
                eprintln!("failed to read from socket: {:?}", e);
                return;
            }
        };

        if let Err(e) = socket.write_all(&buf[0..n]).await {
            eprintln!("failed to write to socket: {:?}", e);
            return;
        }
    }
}

// TCP客户端
use tokio::net::TcpStream;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut stream = TcpStream::connect("127.0.0.1:8080").await?;

    stream.write_all(b"hello").await?;

    let mut buf = [0; 1024];
    let n = stream.read(&mut buf).await?;
    println!("Received: {}", String::from_utf8_lossy(&buf[..n]));

    Ok(())
}
```

## 异步通道

### mpsc

多生产者单消费者。

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        for i in 0..10 {
            if tx.send(i).await.is_err() {
                println!("receiver dropped");
                return;
            }
        }
    });

    while let Some(i) = rx.recv().await {
        println!("got = {}", i);
    }
}
```

### oneshot

单次通信。

```rust
use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        if let Err(_) = tx.send(3) {
            println!("receiver dropped");
        }
    });

    match rx.await {
        Ok(v) => println!("got = {:?}", v),
        Err(_) => println!("sender dropped"),
    }
}
```

### broadcast

广播。

```rust
use tokio::sync::broadcast;

#[tokio::main]
async fn main() {
    let (tx, mut rx1) = broadcast::channel(16);
    let mut rx2 = tx.subscribe();

    tokio::spawn(async move {
        assert_eq!(rx1.recv().await.unwrap(), 10);
        assert_eq!(rx1.recv().await.unwrap(), 20);
    });

    tokio::spawn(async move {
        assert_eq!(rx2.recv().await.unwrap(), 10);
        assert_eq!(rx2.recv().await.unwrap(), 20);
    });

    tx.send(10).unwrap();
    tx.send(20).unwrap();
}
```

## 异步同步原语

### Mutex

```rust
use tokio::sync::Mutex;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let data = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let data = Arc::clone(&data);
        handles.push(tokio::spawn(async move {
            let mut lock = data.lock().await;
            *lock += 1;
        }));
    }

    for handle in handles {
        handle.await.unwrap();
    }

    println!("Result: {}", *data.lock().await);  // 10
}
```

### RwLock

```rust
use tokio::sync::RwLock;

#[tokio::main]
async fn main() {
    let lock = RwLock::new(5);

    // 读锁
    {
        let r1 = lock.read().await;
        let r2 = lock.read().await;
        println!("{} {}", *r1, *r2);
    }

    // 写锁
    {
        let mut w = lock.write().await;
        *w += 1;
    }
}
```

### Semaphore

```rust
use tokio::sync::Semaphore;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    let semaphore = Arc::new(Semaphore::new(3));
    let mut handles = vec![];

    for i in 0..10 {
        let permit = semaphore.clone().acquire_owned().await.unwrap();
        handles.push(tokio::spawn(async move {
            println!("Task {} started", i);
            tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
            drop(permit);  // 释放许可
            println!("Task {} finished", i);
        }));
    }

    for handle in handles {
        handle.await.unwrap();
    }
}
```

## Stream

异步迭代器。

```rust
use tokio_stream::{self as stream, StreamExt};

#[tokio::main]
async fn main() {
    let mut stream = stream::iter(vec![1, 2, 3]);

    while let Some(v) = stream.next().await {
        println!("got = {}", v);
    }
}

// 从channel创建
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;

#[tokio::main]
async fn main() {
    let (tx, rx) = mpsc::channel(10);
    let mut stream = ReceiverStream::new(rx);

    tokio::spawn(async move {
        for i in 0..5 {
            tx.send(i).await.unwrap();
        }
    });

    while let Some(v) = stream.next().await {
        println!("got = {}", v);
    }
}

// map、filter等操作
use tokio_stream::{self as stream, StreamExt};

#[tokio::main]
async fn main() {
    let stream = stream::iter(1..=10)
        .filter(|x| x % 2 == 0)
        .map(|x| x * 2);

    tokio::pin!(stream);

    while let Some(v) = stream.next().await {
        println!("got = {}", v);  // 4, 8, 12, 16, 20
    }
}
```

## HTTP服务器（Axum）

```rust
use axum::{
    routing::{get, post},
    http::StatusCode,
    Json, Router,
};
use serde::{Deserialize, Serialize};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/users", post(create_user));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();
        
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "Hello, World!"
}

async fn create_user(
    Json(payload): Json<CreateUser>,
) -> (StatusCode, Json<User>) {
    let user = User {
        id: 1337,
        username: payload.username,
    };

    (StatusCode::CREATED, Json(user))
}

#[derive(Deserialize)]
struct CreateUser {
    username: String,
}

#[derive(Serialize)]
struct User {
    id: u64,
    username: String,
}
```

## 异步与同步对比

| 特性 | 同步 | 异步 |
|------|------|------|
| 阻塞 | 阻塞线程 | 不阻塞，切换任务 |
| 并发 | 线程并发 | 任务并发 |
| 开销 | 线程栈（MB） | 任务（字节级） |
| 适用场景 | CPU密集 | I/O密集 |
| 复杂度 | 简单 | 较复杂 |

## 性能优化

### 减少分配

```rust
// ❌ 每次分配
async fn process(data: Vec<u8>) {
    // ...
}

// ✓ 使用引用
async fn process(data: &[u8]) {
    // ...
}
```

### 批量操作

```rust
// ❌ 逐个发送
for item in items {
    tx.send(item).await?;
}

// ✓ 批量发送
tx.send_batch(items).await?;
```

### 使用缓冲

```rust
// ❌ 无缓冲channel
let (tx, rx) = mpsc::channel(1);

// ✓ 有缓冲
let (tx, rx) = mpsc::channel(1024);
```

## 常见陷阱

### 阻塞运行时

```rust
// ❌ 错误：阻塞异步运行时
#[tokio::main]
async fn main() {
    tokio::spawn(async {
        std::thread::sleep(Duration::from_secs(10));  // 阻塞整个线程！
    });
}

// ✓ 正确：使用异步sleep
tokio::spawn(async {
    tokio::time::sleep(Duration::from_secs(10)).await;
});

// ✓ CPU密集任务用spawn_blocking
tokio::spawn(async {
    tokio::task::spawn_blocking(|| {
        // 耗时计算
    }).await.unwrap();
});
```

### 忘记await

```rust
// ❌ 错误：忘记await
async fn process() {
    do_something();  // Future未执行！
}

// ✓ 正确
async fn process() {
    do_something().await;
}
```

### 无限Future

```rust
// ❌ 错误：无限递归
async fn infinite() {
    infinite().await;  // 栈溢出
}

// ✓ 使用循环
async fn process_loop() {
    loop {
        process_item().await;
    }
}
```

## 最佳实践

### 选择运行时

```rust
// ✓ I/O密集：Tokio
#[tokio::main]
async fn main() {
    // ...
}

// ✓ 嵌入式：async-std
use async_std::task;

fn main() {
    task::block_on(async {
        // ...
    });
}

// ✓ 浏览器：wasm-bindgen-futures
```

### 错误处理

```rust
// ✓ 使用Result
async fn fetch() -> Result<String, reqwest::Error> {
    let resp = reqwest::get("https://example.com").await?;
    let body = resp.text().await?;
    Ok(body)
}

// ✓ 组合Future
use futures::future;

async fn fetch_all() -> Result<Vec<String>, reqwest::Error> {
    let urls = vec!["url1", "url2", "url3"];
    let futures: Vec<_> = urls.iter().map(|url| fetch(url)).collect();
    future::try_join_all(futures).await
}
```

### 超时和取消

```rust
use tokio::time::{timeout, Duration};

// 超时
async fn with_timeout() -> Result<(), Box<dyn std::error::Error>> {
    let result = timeout(Duration::from_secs(5), slow_operation()).await?;
    Ok(result)
}

// 取消（Drop Future）
let handle = tokio::spawn(async {
    // ...
});

handle.abort();  // 取消任务
```

### 资源清理

```rust
// ✓ 使用Drop
struct Connection {
    // ...
}

impl Drop for Connection {
    fn drop(&mut self) {
        // 清理资源
    }
}

// ✓ 异步清理
async fn cleanup(conn: Connection) {
    conn.close().await;
}
```

## Pin和Unpin

异步函数内部状态不能移动。

```rust
use std::pin::Pin;

// 自动实现Unpin（可移动）
struct MyStruct;

// 手动标记!Unpin（不可移动）
use std::marker::PhantomPinned;

struct NotUnpin {
    data: String,
    _pin: PhantomPinned,
}

// Pin API
fn needs_pin(data: Pin<&mut MyStruct>) {
    // ...
}
```

**核心：** 异步编程通过零成本抽象实现高效I/O。Tokio是主流异步运行时，提供完整的异步生态系统。

