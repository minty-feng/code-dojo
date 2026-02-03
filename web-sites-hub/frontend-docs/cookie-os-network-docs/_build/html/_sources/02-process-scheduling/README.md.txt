# 进程调度

## 💡 核心结论

1. **CPU密集型任务适合短作业优先，I/O密集型适合时间片轮转**
2. **优先级调度容易导致饥饿，需要老化(aging)机制**
3. **Linux CFS调度器追求完全公平，使用红黑树管理进程**
4. **实时调度优先级高于普通调度，保证响应时间**
5. **多核调度需要负载均衡，避免某些核心过载**

---

## 1. 调度算法分类

### 1.1 非抢占式调度
- 进程主动放弃CPU才能调度
- 简单，无需处理竞态条件
- 响应时间差

### 1.2 抢占式调度
- 可以强制剥夺CPU
- 响应时间好
- 需要处理同步问题

---

## 2. 经典调度算法

### 2.1 先来先服务 (FCFS)

**原理**：按到达顺序执行，非抢占式

```c
void fcfs_schedule() {
    while (!queue_empty(&ready_queue)) {
        Process *p = queue_dequeue(&ready_queue);
        run_process(p);  // 运行直到结束
    }
}
```

**特点**：
- 最简单
- 平均等待时间长
- 护航效应（Convoy Effect）：长进程阻塞短进程

**示例**：
```
进程  到达  运行
P1    0    10
P2    1     1
P3    2     1

执行顺序：P1(10) → P2(1) → P3(1)
等待时间：P1=0, P2=9, P3=10
平均等待：6.33
```

### 2.2 短作业优先 (SJF)

**原理**：选择运行时间最短的进程

```c
void sjf_schedule() {
    // 按运行时间排序
    sort_by_burst_time(&ready_queue);
    
    while (!queue_empty(&ready_queue)) {
        Process *p = queue_dequeue(&ready_queue);
        run_process(p);
    }
}
```

**特点**：
- 平均等待时间最优（理论上）
- 需要预知运行时间（实际不可能）
- 长进程可能饥饿

**示例**：
```
进程  到达  运行
P1    0    10
P2    1     1
P3    2     1

执行顺序：P2(1) → P3(1) → P1(10)
等待时间：P1=2, P2=0, P3=0
平均等待：0.67
```

### 2.3 最短剩余时间优先 (SRTF)

**SJF的抢占式版本**：

```c
void srtf_schedule() {
    Process *current = NULL;
    
    while (has_process()) {
        // 新进程到达时检查
        if (new_process_arrival()) {
            Process *new = get_new_process();
            if (!current || new->remaining < current->remaining) {
                preempt(current);
                current = new;
            }
        }
        
        run_one_tick(current);
        current->remaining--;
    }
}
```

**特点**：
- 平均等待时间最优（抢占式）
- 频繁切换，开销大
- 长进程饥饿更严重

### 2.4 时间片轮转 (Round Robin)

**原理**：每个进程执行一个时间片，然后切换

```c
#define TIME_SLICE 10  // 时间片大小（ms）

void round_robin_schedule() {
    while (!queue_empty(&ready_queue)) {
        Process *p = queue_dequeue(&ready_queue);
        
        int runtime = min(p->remaining, TIME_SLICE);
        run_for(p, runtime);
        p->remaining -= runtime;
        
        if (p->remaining > 0) {
            queue_enqueue(&ready_queue, p);  // 放回队尾
        }
    }
}
```

**时间片选择**：
- 太小：上下文切换开销大
- 太大：退化为FCFS
- 经验值：10-100ms

**示例**（时间片=4）：
```
进程  运行时间
P1    10
P2     5
P3     3

执行：P1(4) → P2(4) → P3(3) → P1(4) → P2(1) → P1(2)
```

### 2.5 优先级调度

**原理**：每个进程有优先级，优先级高的先执行

```c
struct process {
    int pid;
    int priority;  // 数字越小优先级越高
    int remaining;
};

void priority_schedule() {
    while (!empty(&ready_queue)) {
        // 选择优先级最高的进程
        Process *p = get_highest_priority(&ready_queue);
        run_process(p);
    }
}
```

**问题：饥饿**
- 低优先级进程可能永远得不到执行

**解决：老化 (Aging)**
```c
// 等待时间越长，优先级越高
void aging() {
    for (Process *p : ready_queue) {
        p->priority -= p->wait_time / 100;  // 动态提升优先级
    }
}
```

### 2.6 多级反馈队列 (MLFQ)

**原理**：多个优先级队列，动态调整优先级

```c
#define LEVELS 3
Queue queues[LEVELS];  // 优先级从0到2递减

void mlfq_schedule() {
    // 规则1：优先级高的先执行
    for (int i = 0; i < LEVELS; i++) {
        if (!empty(&queues[i])) {
            Process *p = dequeue(&queues[i]);
            
            run_for(p, time_slice[i]);
            
            // 规则2：用完时间片，降级
            if (p->remaining > 0) {
                if (i < LEVELS - 1) i++;  // 降级
                enqueue(&queues[i], p);
            }
            
            break;
        }
    }
    
    // 规则3：定期提升所有进程到最高优先级（防止饥饿）
    if (++timer % BOOST_INTERVAL == 0) {
        boost_all_to_top();
    }
}
```

**MLFQ规则**：
1. 优先级高的队列先执行
2. 新进程进入最高优先级队列
3. 进程用完时间片，降到下一级队列
4. I/O阻塞后返回，保持当前优先级
5. 定期提升所有进程（防止饥饿）

**特点**：
- 自动区分I/O密集和CPU密集
- CPU密集型会逐渐降级
- I/O密集型保持高优先级
- 响应时间好

---

## 3. Linux调度器

### 3.1 完全公平调度器 (CFS)

**核心思想**：让每个进程获得相同的CPU时间

```c
struct sched_entity {
    u64 vruntime;         // 虚拟运行时间
    u64 sum_exec_runtime; // 实际运行时间
    int weight;           // 权重（由nice值决定）
};

// 虚拟运行时间计算
vruntime += (delta_exec * NICE_0_LOAD) / weight;
```

**CFS数据结构：红黑树**
```c
struct cfs_rq {
    struct rb_root tasks_timeline;  // 红黑树根
    struct rb_node *rb_leftmost;    // 最左节点（vruntime最小）
};

// 选择下一个进程：O(1)
Process* pick_next_task_fair() {
    return rb_entry(cfs_rq->rb_leftmost, struct sched_entity, run_node);
}

// 插入进程：O(log n)
void enqueue_task_fair(Process *p) {
    rb_insert(&cfs_rq->tasks_timeline, p);
}
```

**nice值与权重**：
```c
// nice值范围：-20到19
// nice值越小，优先级越高，权重越大

static const int prio_to_weight[40] = {
    /* -20 */ 88761, 71755, 56483, 46273, 36291,
    /* -15 */ 29154, 23254, 18705, 14949, 11916,
    /* -10 */ 9548,  7620,  6100,  4904,  3906,
    /*  -5 */ 3121,  2501,  1991,  1586,  1277,
    /*   0 */ 1024,  820,   655,   526,   423,
    /*   5 */ 335,   272,   215,   172,   137,
    /*  10 */ 110,   87,    70,    56,    45,
    /*  15 */ 36,    29,    23,    18,    15,
};
```

**CFS调度示例**：
```
进程  nice  权重  实际运行  vruntime
P1     0    1024    10ms     10ms
P2    -5    3121    10ms     3.3ms
P3     5     335    10ms     30.5ms

下次调度：选择vruntime最小的P2
```

### 3.2 实时调度

**SCHED_FIFO**：先进先出，非抢占
```c
void sched_fifo() {
    while (!empty(&rt_queue)) {
        Process *p = dequeue(&rt_queue);
        run_until_block_or_yield(p);  // 运行直到阻塞或主动让出
    }
}
```

**SCHED_RR**：时间片轮转
```c
void sched_rr() {
    while (!empty(&rt_queue)) {
        Process *p = dequeue(&rt_queue);
        run_for(p, RT_TIME_SLICE);
        if (p->remaining > 0) {
            enqueue(&rt_queue, p);
        }
    }
}
```

**实时优先级**：
- 范围：1-99（数字越大优先级越高）
- 实时进程优先于普通进程
- 相同优先级按FIFO或RR调度

### 3.3 Linux调度类

```
优先级从高到低：

1. stop_sched_class      // 最高优先级（迁移线程）
2. dl_sched_class        // 截止时间调度（SCHED_DEADLINE）
3. rt_sched_class        // 实时调度（SCHED_FIFO/RR）
4. fair_sched_class      // 公平调度（SCHED_NORMAL）
5. idle_sched_class      // 空闲调度
```

---

## 4. 多核调度

### 4.1 负载均衡

**问题**：某些核心负载过重，某些核心空闲

**解决**：周期性迁移进程

```c
void load_balance() {
    // 每个tick检查
    if (need_balance()) {
        int busiest_cpu = find_busiest_cpu();
        int idle_cpu = find_idle_cpu();
        
        if (busiest_cpu != idle_cpu) {
            Process *p = pull_task(busiest_cpu);
            push_task(idle_cpu, p);
        }
    }
}

bool need_balance() {
    int max_load = get_max_cpu_load();
    int min_load = get_min_cpu_load();
    return (max_load - min_load) > THRESHOLD;
}
```

### 4.2 CPU亲和性

```c
// 绑定进程到特定CPU集合
cpu_set_t cpuset;
CPU_ZERO(&cpuset);
CPU_SET(0, &cpuset);  // 只在CPU 0上运行
CPU_SET(1, &cpuset);  // 或CPU 1
sched_setaffinity(pid, sizeof(cpuset), &cpuset);
```

**好处**：
- 减少缓存失效
- 提高缓存命中率
- 减少进程迁移

### 4.3 NUMA感知调度

```c
// Non-Uniform Memory Access
// 内存访问延迟不同

struct task_struct {
    int numa_node;  // 首选NUMA节点
};

// 优先在本地NUMA节点调度
void numa_schedule() {
    int node = task->numa_node;
    int cpu = find_idle_cpu_in_node(node);
    schedule_on_cpu(task, cpu);
}
```

---

## 5. 调度性能指标

### 5.1 吞吐量 (Throughput)
```
吞吐量 = 完成的进程数 / 时间
```

### 5.2 周转时间 (Turnaround Time)
```
周转时间 = 完成时间 - 到达时间
平均周转时间 = Σ周转时间 / 进程数
```

### 5.3 等待时间 (Waiting Time)
```
等待时间 = 周转时间 - 运行时间
```

### 5.4 响应时间 (Response Time)
```
响应时间 = 首次执行时间 - 到达时间
```

### 5.5 CPU利用率
```
CPU利用率 = (总运行时间 - 空闲时间) / 总运行时间
```

---

## 6. 实战案例

### 6.1 调度算法对比

**场景**：3个进程，时间片=2

```
进程  到达  运行
P1    0     5
P2    1     3
P3    3     1
```

**FCFS**：
```
时间线：|P1(5)|P2(3)|P3(1)|
等待：P1=0, P2=4, P3=5
平均等待：3.0
```

**SJF**：
```
时间线：|P3(1)|P2(3)|P1(5)|
等待：P1=4, P2=2, P3=0
平均等待：2.0
```

**RR (q=2)**：
```
时间线：|P1(2)|P2(2)|P1(2)|P3(1)|P2(1)|P1(1)|
等待：P1=4, P2=3, P3=2
平均等待：3.0
```

### 6.2 优先级反转问题

**场景**：
```
H：高优先级任务
M：中优先级任务
L：低优先级任务（持有锁）

1. L获得锁，运行
2. H到达，抢占L，等待锁
3. M到达，抢占L
4. M运行，H等待（优先级反转！）
```

**解决：优先级继承**
```c
void priority_inheritance() {
    // L继承H的优先级
    if (H.wait_for_lock_held_by(L)) {
        L.priority = max(L.priority, H.priority);
    }
}
```

### 6.3 CPU时间测量

```c
#include <time.h>

void measure_cpu_time() {
    clock_t start = clock();
    
    // 执行任务
    do_work();
    
    clock_t end = clock();
    double cpu_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("CPU时间: %.3f秒\n", cpu_time);
}

// 查看进程CPU使用情况
void get_process_time() {
    struct timespec ts;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts);
    printf("进程CPU时间: %ld.%09ld秒\n", ts.tv_sec, ts.tv_nsec);
}
```

---

## 7. 调度器调优

### 7.1 修改nice值

```bash
# 降低优先级（提高nice值）
nice -n 10 ./my_program

# 提高优先级（降低nice值，需要root）
nice -n -10 ./my_program

# 修改运行中进程的nice值
renice -n 5 -p 1234
```

### 7.2 设置实时优先级

```c
#include <sched.h>

void set_realtime() {
    struct sched_param param;
    param.sched_priority = 80;  // 1-99
    
    // 设置FIFO调度
    sched_setscheduler(0, SCHED_FIFO, &param);
    
    // 或设置RR调度
    sched_setscheduler(0, SCHED_RR, &param);
}
```

### 7.3 CFS调优参数

```bash
# 查看CFS参数
cat /proc/sys/kernel/sched_latency_ns        # 调度延迟
cat /proc/sys/kernel/sched_min_granularity_ns # 最小粒度
cat /proc/sys/kernel/sched_wakeup_granularity_ns # 唤醒粒度

# 修改参数
echo 24000000 > /proc/sys/kernel/sched_latency_ns
```

---

## 8. 常见问题

### Q1: 为什么Linux用CFS而不是传统优先级调度？
**A**: 
- CFS更公平，避免饥饿
- 自动平衡CPU时间
- 通过nice值灵活控制
- 红黑树实现高效

### Q2: 实时调度会导致系统卡死吗？
**A**: 
- 可能！实时进程优先级极高
- 死循环的实时进程会占满CPU
- Linux有保护机制：`/proc/sys/kernel/sched_rt_runtime_us`
- 默认实时进程最多占用95%的CPU

### Q3: 如何选择时间片大小？
**A**:
- 考虑上下文切换开销（~1-10μs）
- I/O密集：小时间片（响应快）
- CPU密集：大时间片（减少切换）
- 经验值：10-100ms

### Q4: 多核调度如何避免缓存颠簸？
**A**:
- CPU亲和性绑定
- 优先在本地核心调度
- 减少进程迁移
- NUMA感知调度

---

## 参考资源

- 《Operating Systems: Three Easy Pieces》
- Linux内核文档：Documentation/scheduler/
- Linux源码：`kernel/sched/core.c`, `kernel/sched/fair.c`
- 论文：_Completely Fair Scheduler_ (2007)

