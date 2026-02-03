# 并发与同步

## 💡 核心结论

1. **临界区问题的三个条件：互斥、进步、有限等待**
2. **锁的实现需要硬件支持（原子指令）**
3. **信号量解决同步问题，互斥锁解决互斥问题**
4. **条件变量必须与互斥锁配合使用**
5. **避免死锁的关键是破坏其四个必要条件之一**

---

## 1. 临界区问题

### 1.1 竞态条件（Race Condition）

**示例**：银行账户

```c
int balance = 1000;

// 线程1：取款500
void withdraw() {
    int temp = balance;    // 读取1000
    temp = temp - 500;     // 计算500
    balance = temp;        // 写回500
}

// 线程2：取款300
void withdraw2() {
    int temp = balance;    // 读取1000（！）
    temp = temp - 300;     // 计算700
    balance = temp;        // 写回700（！）
}

// 结果：balance = 700 或 500（错误！应该是200）
```

### 1.2 临界区解决方案要求

**三个条件**：
1. **互斥（Mutual Exclusion）**：一次只有一个进程在临界区
2. **进步（Progress）**：临界区外的进程不能阻止其他进程进入
3. **有限等待（Bounded Waiting）**：请求进入的进程不能无限等待

---

## 2. 锁机制

### 2.1 自旋锁（Spinlock）

**原理**：忙等待

```c
typedef struct {
    int locked;  // 0=未锁，1=已锁
} spinlock_t;

void spin_lock(spinlock_t *lock) {
    while (test_and_set(&lock->locked)) {
        // 忙等待（spin）
    }
}

void spin_unlock(spinlock_t *lock) {
    lock->locked = 0;
}
```

**test_and_set原子指令**：
```c
// 硬件提供的原子操作
int test_and_set(int *ptr) {
    int old = *ptr;
    *ptr = 1;
    return old;
}

// x86汇编实现
lock:
    movl $1, %eax
    xchgl %eax, (%rdi)  // 原子交换
    ret
```

**compare_and_swap（CAS）**：
```c
int compare_and_swap(int *ptr, int expected, int new_value) {
    int actual = *ptr;
    if (actual == expected) {
        *ptr = new_value;
    }
    return actual;
}

// 用CAS实现自旋锁
void spin_lock_cas(spinlock_t *lock) {
    while (compare_and_swap(&lock->locked, 0, 1) != 0) {
        // 忙等待
    }
}
```

**优缺点**：
- ✅ 简单、快速（临界区短时）
- ✅ 无上下文切换
- ❌ CPU时间浪费（忙等待）
- ❌ 优先级反转问题

### 2.2 互斥锁（Mutex）

**原理**：阻塞等待

```c
typedef struct {
    int locked;
    queue_t wait_queue;
} mutex_t;

void mutex_lock(mutex_t *lock) {
    while (test_and_set(&lock->locked)) {
        // 加入等待队列
        enqueue(&lock->wait_queue, current_thread);
        // 休眠（释放CPU）
        park();
    }
}

void mutex_unlock(mutex_t *lock) {
    lock->locked = 0;
    // 唤醒一个等待线程
    thread_t *t = dequeue(&lock->wait_queue);
    if (t) {
        unpark(t);
    }
}
```

**POSIX互斥锁**：
```c
#include <pthread.h>

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void safe_increment() {
    pthread_mutex_lock(&lock);
    count++;  // 临界区
    pthread_mutex_unlock(&lock);
}
```

### 2.3 读写锁（RWLock）

**原理**：多个读者，一个写者

```c
typedef struct {
    int readers;     // 当前读者数
    int writer;      // 是否有写者
    queue_t read_queue;
    queue_t write_queue;
} rwlock_t;

void read_lock(rwlock_t *lock) {
    while (lock->writer) {
        wait(&lock->read_queue);
    }
    lock->readers++;
}

void read_unlock(rwlock_t *lock) {
    lock->readers--;
    if (lock->readers == 0) {
        // 通知等待的写者
        signal_one(&lock->write_queue);
    }
}

void write_lock(rwlock_t *lock) {
    while (lock->writer || lock->readers > 0) {
        wait(&lock->write_queue);
    }
    lock->writer = 1;
}

void write_unlock(rwlock_t *lock) {
    lock->writer = 0;
    // 优先唤醒写者还是读者？
    if (!queue_empty(&lock->write_queue)) {
        signal_one(&lock->write_queue);
    } else {
        signal_all(&lock->read_queue);
    }
}
```

**使用场景**：读多写少

---

## 3. 信号量（Semaphore）

### 3.1 二元信号量

**原理**：计数器（0或1）

```c
typedef struct {
    int value;
    queue_t wait_queue;
} semaphore_t;

void sem_wait(semaphore_t *sem) {  // P操作
    sem->value--;
    if (sem->value < 0) {
        // 阻塞
        enqueue(&sem->wait_queue, current_thread);
        park();
    }
}

void sem_post(semaphore_t *sem) {  // V操作
    sem->value++;
    if (sem->value <= 0) {
        // 唤醒一个等待线程
        thread_t *t = dequeue(&sem->wait_queue);
        unpark(t);
    }
}
```

**用作互斥锁**：
```c
semaphore_t mutex;
sem_init(&mutex, 1);  // 初始值1

void critical_section() {
    sem_wait(&mutex);
    // 临界区
    sem_post(&mutex);
}
```

### 3.2 计数信号量

**用途**：限制资源访问数量

```c
// 限制最多N个线程同时访问
semaphore_t sem;
sem_init(&sem, N);

void access_resource() {
    sem_wait(&sem);
    // 使用资源
    sem_post(&sem);
}
```

### 3.3 经典问题：生产者-消费者

```c
#define BUFFER_SIZE 10

int buffer[BUFFER_SIZE];
int in = 0, out = 0;

semaphore_t empty;  // 空槽位数
semaphore_t full;   // 满槽位数
semaphore_t mutex;  // 互斥访问buffer

void init() {
    sem_init(&empty, BUFFER_SIZE);
    sem_init(&full, 0);
    sem_init(&mutex, 1);
}

void producer() {
    while (1) {
        int item = produce_item();
        
        sem_wait(&empty);   // 等待空槽位
        sem_wait(&mutex);   // 进入临界区
        
        buffer[in] = item;
        in = (in + 1) % BUFFER_SIZE;
        
        sem_post(&mutex);   // 离开临界区
        sem_post(&full);    // 增加满槽位
    }
}

void consumer() {
    while (1) {
        sem_wait(&full);    // 等待满槽位
        sem_wait(&mutex);   // 进入临界区
        
        int item = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        
        sem_post(&mutex);   // 离开临界区
        sem_post(&empty);   // 增加空槽位
        
        consume_item(item);
    }
}
```

### 3.4 经典问题：读者-写者

```c
int readers = 0;
semaphore_t mutex;      // 保护readers计数
semaphore_t write_lock; // 写锁

void reader() {
    while (1) {
        sem_wait(&mutex);
        readers++;
        if (readers == 1) {
            sem_wait(&write_lock);  // 第一个读者获取写锁
        }
        sem_post(&mutex);
        
        // 读取数据
        read_data();
        
        sem_wait(&mutex);
        readers--;
        if (readers == 0) {
            sem_post(&write_lock);  // 最后一个读者释放写锁
        }
        sem_post(&mutex);
    }
}

void writer() {
    while (1) {
        sem_wait(&write_lock);
        
        // 写入数据
        write_data();
        
        sem_post(&write_lock);
    }
}
```

**问题**：写者可能饥饿（读者不断）

**解决**：引入写者优先

```c
int readers = 0, writers = 0;
semaphore_t mutex, r_mutex, w_mutex;

void reader() {
    sem_wait(&r_mutex);
    sem_wait(&mutex);
    readers++;
    if (readers == 1) sem_wait(&write_lock);
    sem_post(&mutex);
    sem_post(&r_mutex);
    
    read_data();
    
    sem_wait(&mutex);
    readers--;
    if (readers == 0) sem_post(&write_lock);
    sem_post(&mutex);
}

void writer() {
    sem_wait(&w_mutex);
    writers++;
    if (writers == 1) sem_wait(&r_mutex);  // 阻止新读者
    sem_post(&w_mutex);
    
    sem_wait(&write_lock);
    write_data();
    sem_post(&write_lock);
    
    sem_wait(&w_mutex);
    writers--;
    if (writers == 0) sem_post(&r_mutex);
    sem_post(&w_mutex);
}
```

---

## 4. 条件变量（Condition Variable）

### 4.1 基本操作

```c
typedef struct {
    queue_t wait_queue;
} cond_t;

void cond_wait(cond_t *cond, mutex_t *mutex) {
    // 1. 释放锁
    mutex_unlock(mutex);
    
    // 2. 加入等待队列并休眠
    enqueue(&cond->wait_queue, current_thread);
    park();
    
    // 3. 被唤醒后重新获取锁
    mutex_lock(mutex);
}

void cond_signal(cond_t *cond) {
    // 唤醒一个等待线程
    thread_t *t = dequeue(&cond->wait_queue);
    if (t) unpark(t);
}

void cond_broadcast(cond_t *cond) {
    // 唤醒所有等待线程
    while (!queue_empty(&cond->wait_queue)) {
        thread_t *t = dequeue(&cond->wait_queue);
        unpark(t);
    }
}
```

### 4.2 生产者-消费者（条件变量版）

```c
mutex_t mutex;
cond_t not_full, not_empty;
int count = 0;
int buffer[BUFFER_SIZE];

void producer() {
    while (1) {
        int item = produce_item();
        
        pthread_mutex_lock(&mutex);
        
        while (count == BUFFER_SIZE) {
            pthread_cond_wait(&not_full, &mutex);  // 等待非满
        }
        
        buffer[count++] = item;
        pthread_cond_signal(&not_empty);  // 通知非空
        
        pthread_mutex_unlock(&mutex);
    }
}

void consumer() {
    while (1) {
        pthread_mutex_lock(&mutex);
        
        while (count == 0) {
            pthread_cond_wait(&not_empty, &mutex);  // 等待非空
        }
        
        int item = buffer[--count];
        pthread_cond_signal(&not_full);  // 通知非满
        
        pthread_mutex_unlock(&mutex);
        
        consume_item(item);
    }
}
```

**为什么用while而不是if？**
```c
// 错误：用if
if (count == 0) {
    pthread_cond_wait(&not_empty, &mutex);
}
// 唤醒后不检查，可能count仍为0（虚假唤醒）

// 正确：用while
while (count == 0) {
    pthread_cond_wait(&not_empty, &mutex);
}
// 唤醒后重新检查条件
```

---

## 5. 管程（Monitor）

**概念**：封装共享数据和同步操作

```c
class BoundedBuffer {
private:
    int buffer[SIZE];
    int count = 0;
    mutex_t mutex;
    cond_t not_full, not_empty;
    
public:
    void put(int item) {
        mutex_lock(&mutex);
        
        while (count == SIZE) {
            cond_wait(&not_full, &mutex);
        }
        
        buffer[count++] = item;
        cond_signal(&not_empty);
        
        mutex_unlock(&mutex);
    }
    
    int get() {
        mutex_lock(&mutex);
        
        while (count == 0) {
            cond_wait(&not_empty, &mutex);
        }
        
        int item = buffer[--count];
        cond_signal(&not_full);
        
        mutex_unlock(&mutex);
        return item;
    }
};
```

**Java synchronized**：
```java
class BoundedBuffer {
    private int[] buffer = new int[SIZE];
    private int count = 0;
    
    public synchronized void put(int item) throws InterruptedException {
        while (count == SIZE) {
            wait();  // 等待非满
        }
        buffer[count++] = item;
        notifyAll();
    }
    
    public synchronized int get() throws InterruptedException {
        while (count == 0) {
            wait();  // 等待非空
        }
        int item = buffer[--count];
        notifyAll();
        return item;
    }
}
```

---

## 6. 无锁编程

### 6.1 原子操作

```c
#include <stdatomic.h>

atomic_int counter = 0;

void increment() {
    atomic_fetch_add(&counter, 1);  // 原子加
}

// CAS循环
void cas_increment() {
    int old, new;
    do {
        old = atomic_load(&counter);
        new = old + 1;
    } while (!atomic_compare_exchange_weak(&counter, &old, new));
}
```

### 6.2 无锁栈

```c
typedef struct node {
    int value;
    struct node *next;
} node_t;

atomic_ptr top = NULL;

void push(int value) {
    node_t *new_node = malloc(sizeof(node_t));
    new_node->value = value;
    
    node_t *old_top;
    do {
        old_top = atomic_load(&top);
        new_node->next = old_top;
    } while (!atomic_compare_exchange_weak(&top, &old_top, new_node));
}

int pop() {
    node_t *old_top, *new_top;
    do {
        old_top = atomic_load(&top);
        if (old_top == NULL) return -1;  // 空栈
        new_top = old_top->next;
    } while (!atomic_compare_exchange_weak(&top, &old_top, new_top));
    
    int value = old_top->value;
    free(old_top);  // ABA问题！
    return value;
}
```

**ABA问题**：
```
线程1：读取top=A
线程2：pop A, pop B, push A
线程1：CAS成功（top还是A，但已经不是原来的A！）
```

**解决**：版本号
```c
typedef struct {
    node_t *ptr;
    int version;
} versioned_ptr;
```

---

## 7. 常见并发bug

### 7.1 死锁

```c
mutex_t lock1, lock2;

// 线程1
void thread1() {
    pthread_mutex_lock(&lock1);
    pthread_mutex_lock(&lock2);  // 等待线程2释放lock2
    // ...
    pthread_mutex_unlock(&lock2);
    pthread_mutex_unlock(&lock1);
}

// 线程2
void thread2() {
    pthread_mutex_lock(&lock2);
    pthread_mutex_lock(&lock1);  // 等待线程1释放lock1
    // ...
    pthread_mutex_unlock(&lock1);
    pthread_mutex_unlock(&lock2);
}
```

**解决**：锁排序
```c
void acquire_both_locks() {
    if (&lock1 < &lock2) {
        pthread_mutex_lock(&lock1);
        pthread_mutex_lock(&lock2);
    } else {
        pthread_mutex_lock(&lock2);
        pthread_mutex_lock(&lock1);
    }
}
```

### 7.2 活锁（Livelock）

```c
// 两个线程都在尝试让对方先执行
while (other_is_waiting) {
    yield();  // 无限循环
}
```

### 7.3 优先级反转

```
H: 高优先级（等待锁）
M: 中优先级（运行）
L: 低优先级（持有锁）

H等待L，但M抢占L，导致H间接等待M
```

**解决**：优先级继承

---

## 8. 性能优化

### 8.1 减少锁竞争

```c
// 粗粒度锁（高竞争）
mutex_t global_lock;

void increment_all() {
    pthread_mutex_lock(&global_lock);
    for (int i = 0; i < N; i++) {
        counters[i]++;
    }
    pthread_mutex_unlock(&global_lock);
}

// 细粒度锁（低竞争）
mutex_t locks[N];

void increment_one(int i) {
    pthread_mutex_lock(&locks[i]);
    counters[i]++;
    pthread_mutex_unlock(&locks[i]);
}
```

### 8.2 无锁数据结构

```c
// 用原子操作代替锁
atomic_int counter = 0;

void fast_increment() {
    atomic_fetch_add(&counter, 1);  // 无锁
}
```

---

## 9. 常见问题

### Q1: 自旋锁 vs 互斥锁？
**A**:
- **自旋锁**：临界区短（<微秒）、多核、不能休眠
- **互斥锁**：临界区长、单核、可以休眠

### Q2: 信号量 vs 条件变量？
**A**:
- **信号量**：计数、不需要锁、P/V操作可分离
- **条件变量**：必须与锁配合、等待特定条件

### Q3: 如何避免死锁？
**A**:
1. 锁排序
2. 超时机制
3. 尝试锁（trylock）
4. 避免嵌套锁

### Q4: volatile vs atomic？
**A**:
- **volatile**：防止编译器优化，不保证原子性
- **atomic**：保证原子性和可见性

---

## LeetCode相关题目

- [1114. 按序打印](https://leetcode.cn/problems/print-in-order/)
- [1115. 交替打印FooBar](https://leetcode.cn/problems/print-foobar-alternately/)
- [1116. 打印零与奇偶数](https://leetcode.cn/problems/print-zero-even-odd/)
- [1117. H2O生成](https://leetcode.cn/problems/building-h2o/)
- [1195. 交替打印字符串](https://leetcode.cn/problems/fizz-buzz-multithreaded/)

---

## 参考资源

- 《Operating Systems: Three Easy Pieces》- Concurrency章节
- 《The Art of Multiprocessor Programming》
- Linux源码：`kernel/locking/`
- POSIX线程编程指南

