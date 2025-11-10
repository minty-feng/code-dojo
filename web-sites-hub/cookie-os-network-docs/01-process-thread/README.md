# 进程与线程

## 💡 核心结论

1. **进程是资源分配单位，线程是CPU调度单位**
2. **进程间相互独立，线程共享进程资源**
3. **进程切换开销大（切换页表、刷新TLB），线程切换开销小**
4. **多进程隔离性好但通信复杂，多线程通信简单但需同步**
5. **fork创建子进程时使用写时复制(COW)优化**

---

## 1. 进程基础

### 1.1 进程控制块 (PCB)

```c
struct process_control_block {
    // 进程标识
    pid_t pid;              // 进程ID
    pid_t ppid;             // 父进程ID
    uid_t uid;              // 用户ID
    
    // 处理器状态
    struct cpu_context context;  // CPU上下文（寄存器）
    int state;              // 进程状态
    int priority;           // 优先级
    
    // 内存管理
    struct mm_struct *mm;   // 内存描述符
    void *page_table;       // 页表指针
    
    // 文件管理
    struct files_struct *files;  // 打开的文件表
    struct fs_struct *fs;        // 文件系统信息
    
    // 进程关系
    struct task_struct *parent;    // 父进程
    struct list_head children;     // 子进程链表
    struct list_head sibling;      // 兄弟进程链表
    
    // 调度信息
    long time_slice;        // 时间片
    long vruntime;          // 虚拟运行时间（CFS）
    long utime, stime;      // 用户态、内核态时间
};
```

### 1.2 进程状态转换

```
              [创建]
                ↓
     就绪 ←→ [运行] → 终止
       ↑       ↓
       └──── [阻塞]
```

**关键状态转换**：
- **就绪→运行**：被调度器选中
- **运行→就绪**：时间片用完
- **运行→阻塞**：等待I/O或事件
- **阻塞→就绪**：I/O完成或事件发生

### 1.3 进程创建：fork()

**Linux的fork实现**：
```c
// 写时复制（Copy-On-Write）
pid_t fork(void) {
    struct task_struct *p;
    
    // 1. 复制父进程的task_struct
    p = dup_task_struct(current);
    
    // 2. 子进程获得新的PID
    p->pid = alloc_pid();
    
    // 3. 页表复制（标记为只读，写时复制）
    copy_page_tables(current, p);
    
    // 4. 文件描述符引用计数+1
    copy_files(current, p);
    
    // 5. 设置返回值（父进程返回子PID，子进程返回0）
    p->context.regs.eax = 0;  // 子进程返回0
    
    // 6. 加入就绪队列
    wake_up_new_task(p);
    
    return p->pid;  // 父进程返回子PID
}
```

**写时复制的优势**：
- 避免不必要的内存复制
- fork后立即exec的场景非常高效
- 延迟复制直到真正需要时

---

## 2. 线程基础

### 2.1 进程 vs 线程

| 对比项 | 进程 | 线程 |
|--------|------|------|
| 地址空间 | 独立 | 共享 |
| 资源 | 独立 | 共享（代码、数据、文件） |
| 通信 | IPC（复杂） | 共享内存（简单） |
| 切换开销 | 大（切换页表、刷TLB） | 小（只切换上下文） |
| 健壮性 | 高（隔离） | 低（一个崩溃全崩溃） |
| 创建开销 | 大 | 小 |

### 2.2 线程模型

**1. 用户级线程（User-Level Thread）**
```
优点：
- 切换快（不需要系统调用）
- 可移植性好
- 可以在不支持线程的OS上运行

缺点：
- 一个线程阻塞，整个进程阻塞
- 无法利用多核CPU
- 内核不感知线程存在
```

**2. 内核级线程（Kernel-Level Thread）**
```
优点：
- 一个线程阻塞，其他线程可继续运行
- 充分利用多核CPU
- 内核直接调度

缺点：
- 切换开销大（需要系统调用）
- 系统资源消耗大
```

**3. 混合模型（M:N）**
```
M个用户线程映射到N个内核线程
- 结合两者优点
- 调度复杂
- Go语言的goroutine就是这种模型
```

### 2.3 线程实现

**POSIX线程（pthread）示例**：
```c
#include <pthread.h>

void* thread_function(void* arg) {
    int* value = (int*)arg;
    printf("Thread: %d\n", *value);
    return NULL;
}

int main() {
    pthread_t thread;
    int arg = 42;
    
    // 创建线程
    pthread_create(&thread, NULL, thread_function, &arg);
    
    // 等待线程结束
    pthread_join(thread, NULL);
    
    return 0;
}
```

---

## 3. 进程/线程切换

### 3.1 上下文切换流程

```c
void context_switch(struct task_struct *prev, 
                   struct task_struct *next) {
    // 1. 保存当前进程的上下文
    save_context(prev);
    
    // 2. 切换页表（进程切换才需要）
    if (prev->mm != next->mm) {
        switch_page_table(next->mm->pgd);
        flush_tlb();  // 刷新TLB
    }
    
    // 3. 切换内核栈
    switch_to(prev, next);
    
    // 4. 恢复新进程的上下文
    restore_context(next);
}
```

### 3.2 上下文内容

**需要保存的寄存器**：
```
通用寄存器：EAX, EBX, ECX, EDX, ESI, EDI
栈寄存器：ESP, EBP
程序计数器：EIP
标志寄存器：EFLAGS
段寄存器：CS, DS, SS, ES, FS, GS
```

### 3.3 切换开销

**进程切换开销**：
1. 保存/恢复寄存器：~100ns
2. 切换页表：~1μs
3. 刷新TLB：~10μs（最大）
4. 缓存失效：~10-100μs

**线程切换开销**（同进程内）：
1. 保存/恢复寄存器：~100ns
2. 无需切换页表
3. 总开销：~1-2μs

---

## 4. 进程通信 (IPC)

### 4.1 管道（Pipe）

**匿名管道**：
```c
int main() {
    int pipefd[2];
    pipe(pipefd);  // pipefd[0]读端，pipefd[1]写端
    
    if (fork() == 0) {
        // 子进程：写数据
        close(pipefd[0]);
        write(pipefd[1], "Hello", 5);
        close(pipefd[1]);
    } else {
        // 父进程：读数据
        close(pipefd[1]);
        char buf[100];
        read(pipefd[0], buf, 100);
        close(pipefd[0]);
    }
}
```

**特点**：
- 半双工（单向通信）
- 只能用于父子进程
- 缓冲区大小有限（默认64KB）

### 4.2 消息队列

```c
#include <sys/msg.h>

struct msg_buffer {
    long msg_type;
    char msg_text[100];
};

// 创建消息队列
int msgid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);

// 发送消息
struct msg_buffer msg = {1, "Hello"};
msgsnd(msgid, &msg, sizeof(msg.msg_text), 0);

// 接收消息
msgrcv(msgid, &msg, sizeof(msg.msg_text), 1, 0);
```

**特点**：
- 消息有类型，可选择性接收
- 消息持久化（不会因进程退出而消失）
- 有大小限制

### 4.3 共享内存（最快）

```c
#include <sys/shm.h>

// 创建共享内存
int shmid = shmget(IPC_PRIVATE, 1024, 0666 | IPC_CREAT);

// 映射到地址空间
char *shm = (char*)shmat(shmid, NULL, 0);

// 写入数据
strcpy(shm, "Hello");

// 分离
shmdt(shm);
```

**特点**：
- 速度最快（直接内存访问）
- 需要同步机制（信号量）
- 需要手动管理生命周期

### 4.4 信号量（Semaphore）

```c
#include <sys/sem.h>

// 创建信号量
int semid = semget(IPC_PRIVATE, 1, 0666 | IPC_CREAT);

// P操作（-1）
struct sembuf p_op = {0, -1, SEM_UNDO};
semop(semid, &p_op, 1);

// 临界区代码

// V操作（+1）
struct sembuf v_op = {0, 1, SEM_UNDO};
semop(semid, &v_op, 1);
```

### 4.5 套接字（Socket）

```c
// 服务端
int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));
listen(sockfd, 5);
int clientfd = accept(sockfd, NULL, NULL);
read(clientfd, buffer, size);

// 客户端
int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
connect(sockfd, (struct sockaddr*)&addr, sizeof(addr));
write(sockfd, data, size);
```

**特点**：
- 可跨网络
- 全双工
- 支持多种协议

### 4.6 IPC对比

| 方式 | 速度 | 通信范围 | 数据量 | 使用难度 |
|------|------|----------|--------|----------|
| 管道 | 中 | 父子进程 | 小 | 简单 |
| 消息队列 | 中 | 任意进程 | 中 | 中等 |
| 共享内存 | 快 | 任意进程 | 大 | 复杂 |
| 信号量 | - | 任意进程 | - | 中等 |
| 套接字 | 慢 | 跨机器 | 大 | 中等 |

---

## 5. 实战案例

### 5.1 生产者-消费者（共享内存+信号量）

```c
// 共享缓冲区
struct shared_buffer {
    int buffer[BUFFER_SIZE];
    int in;   // 写指针
    int out;  // 读指针
};

// 信号量
int mutex;   // 互斥访问缓冲区
int empty;   // 空槽位数量
int full;    // 满槽位数量

// 生产者
void producer() {
    while (1) {
        int item = produce_item();
        
        sem_wait(empty);   // 等待空槽位
        sem_wait(mutex);   // 进入临界区
        
        buffer[in] = item;
        in = (in + 1) % BUFFER_SIZE;
        
        sem_post(mutex);   // 离开临界区
        sem_post(full);    // 增加满槽位
    }
}

// 消费者
void consumer() {
    while (1) {
        sem_wait(full);    // 等待满槽位
        sem_wait(mutex);   // 进入临界区
        
        int item = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        
        sem_post(mutex);   // 离开临界区
        sem_post(empty);   // 增加空槽位
        
        consume_item(item);
    }
}
```

### 5.2 进程池实现

```c
#define POOL_SIZE 10

void process_pool() {
    int pipefd[2];
    pipe(pipefd);
    
    // 创建进程池
    for (int i = 0; i < POOL_SIZE; i++) {
        if (fork() == 0) {
            // 子进程：工作进程
            close(pipefd[1]);
            worker_process(pipefd[0]);
            exit(0);
        }
    }
    
    // 父进程：分发任务
    close(pipefd[0]);
    while (1) {
        Task task = get_task();
        write(pipefd[1], &task, sizeof(task));
    }
}

void worker_process(int readfd) {
    while (1) {
        Task task;
        read(readfd, &task, sizeof(task));
        process_task(&task);
    }
}
```

---

## 6. 性能优化

### 6.1 减少上下文切换

```c
// 使用线程池而非频繁创建线程
struct thread_pool {
    pthread_t threads[POOL_SIZE];
    task_queue_t queue;
    pthread_mutex_t lock;
    pthread_cond_t notify;
};

// 避免不必要的sleep
// 使用非阻塞I/O + epoll
int epollfd = epoll_create1(0);
struct epoll_event events[MAX_EVENTS];
int nfds = epoll_wait(epollfd, events, MAX_EVENTS, -1);
```

### 6.2 CPU亲和性

```c
// 绑定线程到特定CPU，减少缓存失效
cpu_set_t cpuset;
CPU_ZERO(&cpuset);
CPU_SET(0, &cpuset);  // 绑定到CPU 0
pthread_setaffinity_np(pthread_self(), sizeof(cpuset), &cpuset);
```

### 6.3 避免伪共享（False Sharing）

```c
// 错误：两个线程访问相邻数据，导致缓存行失效
struct {
    int counter1;  // 线程1访问
    int counter2;  // 线程2访问
} data;

// 正确：使用缓存行对齐
struct {
    int counter1;
    char padding[60];  // 填充到64字节（一个缓存行）
    int counter2;
} data __attribute__((aligned(64)));
```

---

## 7. 常见问题

### Q1: fork后父子进程谁先运行？
**A**: 不确定，由调度器决定。但Linux倾向于先运行子进程，因为子进程可能立即exec，避免写时复制。

### Q2: 为什么线程比进程快？
**A**: 
1. 创建快：不需要复制页表
2. 切换快：不需要切换页表和刷新TLB
3. 通信快：共享内存，无需IPC

### Q3: 什么时候用多进程，什么时候用多线程？
**A**:
- **多进程**：需要隔离、健壮性要求高、利用多核
- **多线程**：需要共享数据、频繁通信、低延迟

### Q4: 僵尸进程和孤儿进程？
**A**:
- **僵尸进程**：子进程退出，父进程未wait()，子进程PCB仍在
  - 解决：父进程调用wait()回收
- **孤儿进程**：父进程退出，子进程被init进程（PID 1）收养

---

## 8. LeetCode相关题目

- [1114. 按序打印](https://leetcode.cn/problems/print-in-order/) - 线程同步
- [1115. 交替打印FooBar](https://leetcode.cn/problems/print-foobar-alternately/) - 线程协作
- [1116. 打印零与奇偶数](https://leetcode.cn/problems/print-zero-even-odd/) - 多线程同步
- [1117. H2O生成](https://leetcode.cn/problems/building-h2o/) - 信号量应用

---

## 参考资源

- 《操作系统：精髓与设计原理》
- 《深入理解Linux内核》
- 《Unix环境高级编程》(APUE)
- Linux内核源码：`kernel/fork.c`, `kernel/sched/`

