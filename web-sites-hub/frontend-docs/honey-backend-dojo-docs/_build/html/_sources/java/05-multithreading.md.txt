# 05-Java多线程编程

多线程是Java的核心特性，JVM级别支持，API丰富。合理使用多线程可充分利用多核CPU。

## 线程创建

### 方式1：继承Thread类

```java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running: " + Thread.currentThread().getName());
    }
}

// 使用
MyThread t = new MyThread();
t.start();  // 启动线程（不是t.run()！）
```

### 方式2：实现Runnable接口（推荐）

```java
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Runnable running");
    }
}

// 使用
Thread t = new Thread(new MyRunnable());
t.start();

// Lambda（Java 8+）
new Thread(() -> System.out.println("Lambda thread")).start();
```

### 方式3：实现Callable接口

支持返回值和抛出异常。

```java
import java.util.concurrent.*;

public class MyCallable implements Callable<Integer> {
    @Override
    public Integer call() throws Exception {
        Thread.sleep(1000);
        return 42;
    }
}

// 使用
ExecutorService executor = Executors.newSingleThreadExecutor();
Future<Integer> future = executor.submit(new MyCallable());

Integer result = future.get();  // 阻塞等待结果
executor.shutdown();
```

## 线程状态

```
NEW（新建）
  ↓ start()
RUNNABLE（可运行）
  ↓ 获取锁/IO完成
RUNNING（运行）
  ↓ sleep/wait/阻塞IO
BLOCKED/WAITING/TIMED_WAITING（阻塞/等待）
  ↓ run()结束
TERMINATED（终止）
```

### 线程控制

```java
Thread t = new Thread(() -> {
    try {
        Thread.sleep(1000);  // 休眠1秒
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
});

t.start();                  // 启动
t.join();                   // 等待线程结束
t.interrupt();              // 中断线程
boolean alive = t.isAlive(); // 是否存活
```

## 线程同步

### synchronized关键字

Java最基本的同步机制，保证互斥访问。

```java
public class Counter {
    private int count = 0;
    
    // 同步方法
    public synchronized void increment() {
        count++;
    }
    
    // 同步块
    public void decrement() {
        synchronized (this) {
            count--;
        }
    }
    
    // 静态同步方法（锁类对象）
    public static synchronized void staticMethod() {
        // ...
    }
}
```

**锁对象：**
- 实例方法：锁this
- 静态方法：锁Class对象
- 同步块：锁指定对象

### Lock接口

比synchronized更灵活，可中断、可超时、可尝试获取。

```java
import java.util.concurrent.locks.*;

public class Counter {
    private int count = 0;
    private Lock lock = new ReentrantLock();
    
    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();  // 必须在finally中释放
        }
    }
    
    // 尝试获取锁
    public boolean tryIncrement() {
        if (lock.tryLock()) {
            try {
                count++;
                return true;
            } finally {
                lock.unlock();
            }
        }
        return false;
    }
    
    // 超时获取
    public boolean incrementWithTimeout() throws InterruptedException {
        if (lock.tryLock(1, TimeUnit.SECONDS)) {
            try {
                count++;
                return true;
            } finally {
                lock.unlock();
            }
        }
        return false;
    }
}
```

### ReadWriteLock

读写分离锁，读多写少场景性能优于普通锁。

```java
import java.util.concurrent.locks.*;

public class Cache {
    private Map<String, Object> cache = new HashMap<>();
    private ReadWriteLock rwLock = new ReentrantReadWriteLock();
    private Lock readLock = rwLock.readLock();
    private Lock writeLock = rwLock.writeLock();
    
    // 读操作（多个线程可同时读）
    public Object get(String key) {
        readLock.lock();
        try {
            return cache.get(key);
        } finally {
            readLock.unlock();
        }
    }
    
    // 写操作（独占）
    public void put(String key, Object value) {
        writeLock.lock();
        try {
            cache.put(key, value);
        } finally {
            writeLock.unlock();
        }
    }
}
```

## 线程通信

### wait/notify

Object类的方法，必须在synchronized块中使用。

```java
public class ProducerConsumer {
    private Queue<Integer> queue = new LinkedList<>();
    private int capacity = 10;
    
    public synchronized void produce(int item) throws InterruptedException {
        while (queue.size() == capacity) {
            wait();  // 队列满，等待
        }
        queue.add(item);
        System.out.println("Produced: " + item);
        notifyAll();  // 通知消费者
    }
    
    public synchronized int consume() throws InterruptedException {
        while (queue.isEmpty()) {
            wait();  // 队列空，等待
        }
        int item = queue.poll();
        System.out.println("Consumed: " + item);
        notifyAll();  // 通知生产者
        return item;
    }
}
```

### Condition

Lock配套的等待/通知机制，比wait/notify更灵活。

```java
import java.util.concurrent.locks.*;

public class BoundedBuffer {
    private Queue<Integer> queue = new LinkedList<>();
    private int capacity = 10;
    private Lock lock = new ReentrantLock();
    private Condition notFull = lock.newCondition();
    private Condition notEmpty = lock.newCondition();
    
    public void put(int item) throws InterruptedException {
        lock.lock();
        try {
            while (queue.size() == capacity) {
                notFull.await();  // 等待不满
            }
            queue.add(item);
            notEmpty.signal();  // 通知不空
        } finally {
            lock.unlock();
        }
    }
    
    public int take() throws InterruptedException {
        lock.lock();
        try {
            while (queue.isEmpty()) {
                notEmpty.await();  // 等待不空
            }
            int item = queue.poll();
            notFull.signal();  // 通知不满
            return item;
        } finally {
            lock.unlock();
        }
    }
}
```

## 线程池

线程创建销毁开销大，线程池复用线程，提高性能。

### Executors工厂方法

```java
import java.util.concurrent.*;

// 固定线程数
ExecutorService executor = Executors.newFixedThreadPool(5);

// 单线程
ExecutorService single = Executors.newSingleThreadExecutor();

// 缓存线程池（自动扩缩容）
ExecutorService cached = Executors.newCachedThreadPool();

// 定时任务
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(2);

// 提交任务
executor.submit(() -> System.out.println("Task"));
Future<Integer> future = executor.submit(() -> 42);

// 关闭
executor.shutdown();  // 不接受新任务，等待已提交任务完成
executor.shutdownNow();  // 尝试中断所有任务
```

### ThreadPoolExecutor

手动配置线程池参数，更灵活。

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    5,                      // 核心线程数
    10,                     // 最大线程数
    60L,                    // 空闲线程存活时间
    TimeUnit.SECONDS,       // 时间单位
    new LinkedBlockingQueue<>(100),  // 工作队列
    Executors.defaultThreadFactory(),  // 线程工厂
    new ThreadPoolExecutor.CallerRunsPolicy()  // 拒绝策略
);

// 拒绝策略：
// - AbortPolicy：抛异常（默认）
// - CallerRunsPolicy：调用线程执行
// - DiscardPolicy：丢弃
// - DiscardOldestPolicy：丢弃最老任务
```

### CompletableFuture（Java 8+）

异步编程增强，支持链式调用和组合。

```java
import java.util.concurrent.CompletableFuture;

// 异步执行
CompletableFuture<Void> future = CompletableFuture.runAsync(() -> {
    System.out.println("Async task");
});

// 异步计算
CompletableFuture<Integer> compute = CompletableFuture.supplyAsync(() -> {
    return 42;
});

// 链式调用
CompletableFuture<String> result = CompletableFuture.supplyAsync(() -> "Hello")
    .thenApply(s -> s + " World")       // 转换
    .thenApply(String::toUpperCase)     // 再转换
    .exceptionally(ex -> "Error");      // 异常处理

// 组合多个Future
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(() -> 10);
CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(() -> 20);

CompletableFuture<Integer> combined = f1.thenCombine(f2, (a, b) -> a + b);
Integer sum = combined.get();  // 30

// 等待所有完成
CompletableFuture.allOf(f1, f2).join();

// 等待任一完成
CompletableFuture.anyOf(f1, f2).join();
```

## 并发集合

### ConcurrentHashMap

线程安全的HashMap，分段锁实现，性能优于Hashtable。

```java
import java.util.concurrent.ConcurrentHashMap;

ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 原子操作
map.putIfAbsent("key", 1);
map.computeIfPresent("key", (k, v) -> v + 1);
map.merge("key", 1, Integer::sum);  // 原子计数

// 不需要额外同步
```

### CopyOnWriteArrayList

写时复制，适合读多写少。

```java
import java.util.concurrent.CopyOnWriteArrayList;

CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();

// 写操作：复制整个数组
list.add("item");  // 加锁，复制数组，添加元素

// 读操作：无锁，快照读取
for (String item : list) {  // 不会ConcurrentModificationException
    // ...
}
```

### BlockingQueue

阻塞队列，线程安全，支持阻塞操作。

```java
import java.util.concurrent.*;

BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(10);

// 生产者
new Thread(() -> {
    try {
        for (int i = 0; i < 20; i++) {
            queue.put(i);  // 队列满时阻塞
        }
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}).start();

// 消费者
new Thread(() -> {
    try {
        while (true) {
            Integer item = queue.take();  // 队列空时阻塞
            System.out.println("Consumed: " + item);
        }
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}).start();
```

## 原子类

### AtomicInteger

无锁线程安全的整数，基于CAS（Compare-And-Swap）。

```java
import java.util.atomic.AtomicInteger;

AtomicInteger count = new AtomicInteger(0);

// 原子操作
count.incrementAndGet();  // ++count
count.decrementAndGet();  // --count
count.addAndGet(5);       // count += 5
count.compareAndSet(5, 10);  // CAS

// 性能：无锁 > synchronized
```

### 其他原子类

```java
AtomicLong               // 长整型
AtomicBoolean            // 布尔型
AtomicReference<T>       // 引用类型
AtomicIntegerArray       // 整数数组
AtomicReferenceArray<T>  // 引用数组
LongAdder                // 高并发计数（比AtomicLong更快）
```

## 常见并发问题

### 死锁

```java
// ❌ 死锁示例
Object lock1 = new Object();
Object lock2 = new Object();

new Thread(() -> {
    synchronized (lock1) {
        Thread.sleep(100);
        synchronized (lock2) {  // 等待lock2
            // ...
        }
    }
}).start();

new Thread(() -> {
    synchronized (lock2) {
        Thread.sleep(100);
        synchronized (lock1) {  // 等待lock1（死锁！）
            // ...
        }
    }
}).start();

// ✅ 解决：固定加锁顺序
synchronized (lock1) {
    synchronized (lock2) {
        // 两个线程都按相同顺序加锁
    }
}
```

### 线程安全问题

```java
// ❌ 非线程安全
public class UnsafeCounter {
    private int count = 0;
    
    public void increment() {
        count++;  // 非原子：读-改-写
    }
}

// ✅ 同步方法
public synchronized void increment() {
    count++;
}

// ✅ 原子类
private AtomicInteger count = new AtomicInteger(0);
public void increment() {
    count.incrementAndGet();
}

// ✅ volatile（仅可见性，不保证原子性）
private volatile boolean flag = false;
public void setFlag() {
    flag = true;  // 简单赋值可用volatile
}
```

## volatile关键字

保证可见性和有序性，但不保证原子性。

```java
public class VolatileExample {
    private volatile boolean running = true;
    
    public void run() {
        while (running) {  // 其他线程修改running立即可见
            // ...
        }
    }
    
    public void stop() {
        running = false;  // 修改对所有线程可见
    }
}
```

**使用场景：**
- 状态标志
- 双重检查锁的单例
- 读多写少的变量

**注意：** `i++` 等复合操作即使用volatile也不是线程安全的。

## ThreadLocal

线程局部变量，每个线程独立副本。

```java
public class ThreadLocalExample {
    private static ThreadLocal<Integer> threadLocal = ThreadLocal.withInitial(() -> 0);
    
    public static void main(String[] args) {
        new Thread(() -> {
            threadLocal.set(10);
            System.out.println("Thread 1: " + threadLocal.get());  // 10
        }).start();
        
        new Thread(() -> {
            threadLocal.set(20);
            System.out.println("Thread 2: " + threadLocal.get());  // 20
        }).start();
    }
}
```

**使用场景：**
- 数据库连接
- 用户Session
- SimpleDateFormat（非线程安全，用ThreadLocal包装）

**注意：** 线程池环境必须手动清理，否则内存泄漏。

```java
try {
    threadLocal.set(value);
    // 使用
} finally {
    threadLocal.remove();  // 清理
}
```

## 最佳实践

### 线程池配置

```java
// CPU密集型：线程数 = CPU核心数 + 1
int cpuCount = Runtime.getRuntime().availableProcessors();
ExecutorService cpuBound = Executors.newFixedThreadPool(cpuCount + 1);

// IO密集型：线程数 = 2 * CPU核心数
ExecutorService ioBound = Executors.newFixedThreadPool(cpuCount * 2);

// 自定义线程池（推荐）
ThreadPoolExecutor custom = new ThreadPoolExecutor(
    10, 20, 60L, TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(1000),
    new ThreadFactory() {
        private AtomicInteger count = new AtomicInteger(0);
        @Override
        public Thread newThread(Runnable r) {
            Thread t = new Thread(r);
            t.setName("Worker-" + count.incrementAndGet());
            t.setDaemon(false);
            return t;
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy()
);
```

### 并发编程原则

1. **优先使用并发集合**：ConcurrentHashMap > Hashtable
2. **优先使用线程池**：复用线程，避免频繁创建
3. **最小化锁范围**：只锁必要的代码
4. **避免嵌套锁**：易死锁
5. **用final减少可见性问题**：不变对象天然线程安全
6. **优先无锁方案**：原子类 > synchronized
7. **读写分离**：ReadWriteLock适合读多写少
8. **CompletableFuture异步**：替代手动线程管理
9. **ThreadLocal注意清理**：线程池环境避免泄漏
10. **充分测试**：并发Bug难复现

**核心：** 能不用多线程就不用；必须用就用高层API；手写就加倍小心。

## 并发工具类

### CountDownLatch

等待多个线程完成。

```java
CountDownLatch latch = new CountDownLatch(3);

for (int i = 0; i < 3; i++) {
    new Thread(() -> {
        // 执行任务
        System.out.println("Task done");
        latch.countDown();  // 计数减1
    }).start();
}

latch.await();  // 等待计数归0
System.out.println("All tasks completed");
```

### CyclicBarrier

多线程同步点，所有线程到达后一起继续。

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads reached barrier");
});

for (int i = 0; i < 3; i++) {
    new Thread(() -> {
        System.out.println("Thread waiting at barrier");
        barrier.await();  // 等待其他线程
        System.out.println("Thread continues");
    }).start();
}
```

### Semaphore

信号量，控制同时访问的线程数。

```java
Semaphore semaphore = new Semaphore(3);  // 最多3个线程

new Thread(() -> {
    try {
        semaphore.acquire();  // 获取许可
        // 访问资源
        Thread.sleep(1000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    } finally {
        semaphore.release();  // 释放许可
    }
}).start();
```

**应用：** 限流、连接池、资源访问控制。

