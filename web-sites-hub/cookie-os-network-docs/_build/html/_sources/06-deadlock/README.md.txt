# 死锁处理

## 💡 核心结论

1. **死锁四大必要条件：互斥、占有并等待、非抢占、循环等待**
2. **破坏任意一个条件即可预防死锁**
3. **银行家算法是安全性检查的经典算法**
4. **死锁检测需要资源分配图，查找环**
5. **实际系统多采用鸵鸟策略（忽略死锁）**

---

## 1. 死锁定义

**死锁（Deadlock）**：多个进程永久等待对方持有的资源

### 1.1 经典例子

```c
mutex_t lock_A, lock_B;

// 进程1
void process1() {
    lock(lock_A);
    sleep(1);         // 等待，让进程2获得lock_B
    lock(lock_B);     // 死锁：等待进程2释放lock_B
    // ...
    unlock(lock_B);
    unlock(lock_A);
}

// 进程2
void process2() {
    lock(lock_B);
    sleep(1);         // 等待，让进程1获得lock_A
    lock(lock_A);     // 死锁：等待进程1释放lock_A
    // ...
    unlock(lock_A);
    unlock(lock_B);
}
```

**结果**：
```
进程1持有A，等待B
进程2持有B，等待A
↓
死锁！
```

---

## 2. 死锁四大条件

### 2.1 互斥（Mutual Exclusion）

**定义**：资源同时只能被一个进程使用

```c
mutex_t lock;

// 互斥访问临界区
void critical_section() {
    lock(lock);
    // 只有一个进程能进入
    unlock(lock);
}
```

### 2.2 占有并等待（Hold and Wait）

**定义**：进程持有资源的同时等待其他资源

```c
void process() {
    lock(resource1);    // 持有resource1
    // ...
    lock(resource2);    // 等待resource2
}
```

### 2.3 非抢占（No Preemption）

**定义**：资源不能被强制抢占，只能主动释放

```c
// 进程持有锁后，其他进程不能强制夺走
lock(lock);
// 必须由进程自己释放
unlock(lock);
```

### 2.4 循环等待（Circular Wait）

**定义**：存在进程环路，每个进程等待下一个进程的资源

```
P1 → R1 → P2 → R2 → P3 → R3 → P1
(P1等R1，R1被P2持有，P2等R2，R2被P3持有，P3等R3，R3被P1持有)
```

---

## 3. 死锁预防

**原理**：破坏四大条件之一

### 3.1 破坏互斥条件

**方法**：资源共享（不现实）

```c
// 只读资源可以共享
int shared_data;  // 多个进程可同时读取

// 但某些资源必须互斥
mutex_t printer;  // 打印机不能共享
```

**结论**：通常无法破坏（资源本质决定）

### 3.2 破坏占有并等待

**方法1**：一次性申请所有资源

```c
void process() {
    // 一次性获取所有需要的锁
    lock_all(lock_A, lock_B, lock_C);
    
    // 使用资源
    
    unlock_all(lock_A, lock_B, lock_C);
}
```

**缺点**：
- 资源利用率低
- 可能导致饥饿
- 难以预知所有需要的资源

**方法2**：申请资源前释放已持有的资源

```c
void process() {
    while (1) {
        lock(lock_A);
        
        if (trylock(lock_B) == SUCCESS) {
            // 成功获取两个锁
            break;
        } else {
            // 失败，释放已持有的锁
            unlock(lock_A);
            // 等待后重试
            sleep(random());
        }
    }
    
    // 使用资源
    unlock(lock_B);
    unlock(lock_A);
}
```

### 3.3 破坏非抢占条件

**方法**：允许抢占

```c
void process() {
    lock(lock_A);
    
    if (trylock(lock_B) == FAILED) {
        // lock_B被占用，释放lock_A
        unlock(lock_A);
        // 等待后重试
        wait_and_retry();
    }
    
    // 使用资源
    unlock(lock_B);
    unlock(lock_A);
}
```

**问题**：
- 实现复杂
- 可能导致活锁
- 某些资源不能抢占（如打印机）

### 3.4 破坏循环等待（最常用）

**方法**：资源排序，按序申请

```c
// 给锁分配全局顺序
#define LOCK_A_ID 1
#define LOCK_B_ID 2
#define LOCK_C_ID 3

void lock_in_order(mutex_t *lock1, int id1, 
                  mutex_t *lock2, int id2) {
    if (id1 < id2) {
        lock(lock1);
        lock(lock2);
    } else {
        lock(lock2);
        lock(lock1);
    }
}

// 使用
void process() {
    lock_in_order(&lock_A, LOCK_A_ID, &lock_B, LOCK_B_ID);
    // ...
    unlock(lock_B);
    unlock(lock_A);
}
```

**Linux内核示例**：
```c
// 两个inode锁，按地址排序
if (inode1 < inode2) {
    mutex_lock(&inode1->i_mutex);
    mutex_lock(&inode2->i_mutex);
} else {
    mutex_lock(&inode2->i_mutex);
    mutex_lock(&inode1->i_mutex);
}
```

---

## 4. 死锁避免

**原理**：动态检查资源分配安全性

### 4.1 银行家算法

**概念**：类比银行贷款，确保系统处于安全状态

```c
// 系统状态
int available[M];           // 可用资源
int max[N][M];             // 最大需求
int allocation[N][M];      // 已分配
int need[N][M];            // 还需要 = max - allocation

// 安全性检查
bool is_safe() {
    int work[M];
    bool finish[N];
    
    // 初始化
    for (int i = 0; i < M; i++) {
        work[i] = available[i];
    }
    for (int i = 0; i < N; i++) {
        finish[i] = false;
    }
    
    // 查找安全序列
    while (true) {
        bool found = false;
        
        for (int i = 0; i < N; i++) {
            if (!finish[i] && need[i] <= work) {
                // 进程i可以完成
                for (int j = 0; j < M; j++) {
                    work[j] += allocation[i][j];
                }
                finish[i] = true;
                found = true;
            }
        }
        
        if (!found) break;
    }
    
    // 检查是否所有进程都能完成
    for (int i = 0; i < N; i++) {
        if (!finish[i]) return false;
    }
    return true;
}

// 资源请求
bool request_resources(int process, int request[M]) {
    // 1. 检查请求是否超过需求
    if (request > need[process]) {
        return false;
    }
    
    // 2. 检查资源是否足够
    if (request > available) {
        return false;  // 等待
    }
    
    // 3. 试探性分配
    available -= request;
    allocation[process] += request;
    need[process] -= request;
    
    // 4. 安全性检查
    if (is_safe()) {
        return true;  // 安全，分配成功
    } else {
        // 不安全，回滚
        available += request;
        allocation[process] -= request;
        need[process] += request;
        return false;
    }
}
```

**示例**：
```
3个进程，3种资源(A=10, B=5, C=7)

进程  Max      Allocation  Need      Available
     A B C     A B C       A B C     A B C
P0   7 5 3     0 1 0       7 4 3     3 3 2
P1   3 2 2     2 0 0       1 2 2
P2   9 0 2     3 0 2       6 0 0

安全序列：P1 → P0 → P2
1. P1完成，释放(2,0,0)，可用(5,3,2)
2. P0完成，释放(0,1,0)，可用(5,4,2)
3. P2完成，释放(3,0,2)，可用(8,4,4)
```

**缺点**：
- 进程数和资源类型固定
- 需要预知最大需求
- 实现复杂
- 很少使用

---

## 5. 死锁检测

**原理**：允许死锁发生，定期检测并恢复

### 5.1 资源分配图

```
进程 → 资源：请求边
资源 → 进程：分配边

死锁 ⇔ 图中有环
```

**示例**：
```
P1 → R1 → P2 → R2 → P1
(有环，死锁)

P1 → R1 → P2 → R2
          ↓
         P3
(无环，无死锁)
```

### 5.2 检测算法

```c
struct process {
    int id;
    int request[M];    // 请求的资源
    int allocation[M]; // 已分配的资源
};

bool detect_deadlock() {
    int available[M];
    bool finish[N];
    
    // 初始化
    calculate_available(available);
    for (int i = 0; i < N; i++) {
        finish[i] = (allocation[i] == 0);  // 无资源的进程已完成
    }
    
    // 查找可完成的进程
    while (true) {
        bool found = false;
        
        for (int i = 0; i < N; i++) {
            if (!finish[i] && request[i] <= available) {
                // 进程i可以完成
                for (int j = 0; j < M; j++) {
                    available[j] += allocation[i][j];
                }
                finish[i] = true;
                found = true;
            }
        }
        
        if (!found) break;
    }
    
    // 检查是否有进程未完成
    for (int i = 0; i < N; i++) {
        if (!finish[i]) {
            return true;  // 检测到死锁
        }
    }
    return false;
}
```

**检测频率**：
- 每次资源请求时检测（开销大）
- 定期检测（如每小时）
- CPU利用率低时检测

---

## 6. 死锁恢复

### 6.1 进程终止

**方法1**：终止所有死锁进程
```c
void recover_terminate_all() {
    for (Process *p : deadlocked_processes) {
        kill(p);
    }
}
```

**方法2**：逐个终止直到解除死锁
```c
void recover_terminate_one() {
    while (detect_deadlock()) {
        Process *victim = select_victim();
        kill(victim);
    }
}
```

**选择受害者**：
- 优先级最低
- 执行时间最短
- 持有资源最少
- 已使用CPU时间最少

### 6.2 资源抢占

```c
void recover_preempt() {
    while (detect_deadlock()) {
        // 1. 选择受害者
        Process *victim = select_victim();
        
        // 2. 回滚到安全状态
        rollback(victim);
        
        // 3. 抢占资源
        Resource *res = preempt_resource(victim);
        
        // 4. 分配给等待的进程
        allocate(res, waiting_process);
    }
}
```

**回滚策略**：
- 完全回滚：回到初始状态
- 部分回滚：回到某个检查点
- 饥饿问题：同一进程多次被选为受害者

---

## 7. 实际系统策略

### 7.1 鸵鸟策略

**原理**：忽略死锁（假装不存在）

```c
// 大多数操作系统的做法
if (system_hang) {
    reboot();  // 重启解决一切问题
}
```

**理由**：
- 死锁很少发生
- 预防和检测开销大
- 性能优先于绝对正确性

**使用场景**：
- Linux、Windows桌面系统
- UNIX系统

### 7.2 超时机制

```c
bool lock_with_timeout(mutex_t *lock, int timeout_ms) {
    int elapsed = 0;
    
    while (!trylock(lock)) {
        sleep(10);
        elapsed += 10;
        
        if (elapsed >= timeout_ms) {
            return false;  // 超时，可能死锁
        }
    }
    
    return true;
}

void safe_operation() {
    if (lock_with_timeout(&lock_A, 1000)) {
        if (lock_with_timeout(&lock_B, 1000)) {
            // 成功获取两个锁
            critical_section();
            unlock(lock_B);
        }
        unlock(lock_A);
    } else {
        // 超时，放弃操作
        log("可能发生死锁");
    }
}
```

---

## 8. 实战案例

### 8.1 哲学家就餐问题

**问题**：5个哲学家，5根筷子，需要两根筷子才能吃饭

```c
// 死锁版本
void philosopher(int i) {
    while (1) {
        think();
        
        pick_up(chopstick[i]);       // 拿起左边筷子
        pick_up(chopstick[(i+1)%5]); // 拿起右边筷子
        
        eat();
        
        put_down(chopstick[(i+1)%5]);
        put_down(chopstick[i]);
    }
}
// 如果所有人同时拿起左边筷子 → 死锁
```

**解决方案1**：最多4人同时拿筷子
```c
semaphore_t room = 4;  // 最多4人

void philosopher(int i) {
    while (1) {
        think();
        
        sem_wait(&room);  // 进入房间
        pick_up(chopstick[i]);
        pick_up(chopstick[(i+1)%5]);
        
        eat();
        
        put_down(chopstick[(i+1)%5]);
        put_down(chopstick[i]);
        sem_post(&room);  // 离开房间
    }
}
```

**解决方案2**：奇数先左后右，偶数先右后左
```c
void philosopher(int i) {
    while (1) {
        think();
        
        if (i % 2 == 0) {
            pick_up(chopstick[i]);
            pick_up(chopstick[(i+1)%5]);
        } else {
            pick_up(chopstick[(i+1)%5]);
            pick_up(chopstick[i]);
        }
        
        eat();
        
        put_down(chopstick[(i+1)%5]);
        put_down(chopstick[i]);
    }
}
```

### 8.2 数据库死锁

```sql
-- 事务1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- 锁定账户1
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- 等待账户2
COMMIT;

-- 事务2
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE id = 2;   -- 锁定账户2
UPDATE accounts SET balance = balance + 50 WHERE id = 1;   -- 等待账户1
COMMIT;

-- 死锁！
```

**MySQL死锁检测**：
```c
// MySQL自动检测死锁并回滚其中一个事务
void detect_and_recover() {
    if (detect_cycle_in_wait_graph()) {
        Transaction *victim = select_victim();
        rollback(victim);
        return ERROR_DEADLOCK;
    }
}
```

---

## 9. 常见问题

### Q1: 死锁和饥饿的区别？
**A**:
- **死锁**：互相等待，永远无法继续
- **饥饿**：一直得不到资源，但系统仍在运行

### Q2: 如何调试死锁？
**A**:
1. `ps aux` 查看进程状态（D状态）
2. `pstack` 查看调用栈
3. `gdb` 附加进程查看锁状态
4. 使用死锁检测工具（如Helgrind）

### Q3: 为什么数据库能自动处理死锁？
**A**:
- 数据库维护等待图
- 定期检测环
- 选择代价小的事务回滚
- 应用层可以重试

### Q4: 多线程程序如何避免死锁？
**A**:
1. 锁排序（最重要）
2. 使用`trylock`
3. 超时机制
4. 减少锁的持有时间
5. 使用无锁数据结构

---

## 10. 调试工具

### 10.1 Linux工具

```bash
# 查看进程状态
ps aux | grep D  # D状态可能是死锁

# 查看线程栈
pstack <pid>

# 查看锁信息
cat /proc/<pid>/status

# 使用gdb
gdb -p <pid>
(gdb) info threads
(gdb) thread apply all bt
```

### 10.2 Valgrind Helgrind

```bash
# 死锁检测
valgrind --tool=helgrind ./program

# 输出示例
==12345== Thread #1: lock order "0x12345 before 0x67890" violated
==12345== Thread #2: lock order "0x67890 before 0x12345"
```

### 10.3 死锁检测代码

```c
#define MAX_LOCKS 100

struct lock_info {
    pthread_t thread;
    void *lock_addr;
    const char *file;
    int line;
};

lock_info held_locks[MAX_LOCKS];
int lock_count = 0;

void record_lock(void *lock) {
    held_locks[lock_count++] = {
        pthread_self(), lock, __FILE__, __LINE__
    };
    
    // 检测环
    if (detect_cycle()) {
        fprintf(stderr, "Deadlock detected!\n");
        print_lock_graph();
        abort();
    }
}
```

---

## 参考资源

- 《Operating Systems: Three Easy Pieces》- Deadlock章节
- 《Database System Concepts》- 事务和并发控制
- Linux源码：`kernel/locking/lockdep.c`（死锁检测）
- 《Art of Multiprocessor Programming》

