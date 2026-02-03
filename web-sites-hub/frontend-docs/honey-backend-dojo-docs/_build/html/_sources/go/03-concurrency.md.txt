# 03-Go并发编程

并发是Go的杀手级特性。goroutine极轻量，channel类型安全，select优雅多路复用。

## goroutine深入

### 特性对比

| 特性 | 线程（Thread） | goroutine |
|------|---------------|-----------|
| 栈大小 | 1-2MB | 2KB起步，动态扩展 |
| 创建开销 | ~1-2ms | ~1μs |
| 调度 | OS内核调度 | Go运行时调度（M:N） |
| 切换成本 | 高（内核态切换） | 低（用户态） |
| 数量上限 | 几千 | 百万级 |

### goroutine调度模型（GMP）

```
G：goroutine
M：系统线程（Machine）
P：处理器（Processor），逻辑CPU

调度模型：M:N
- 多个goroutine（G）映射到少量线程（M）
- P控制G在M上执行
- 默认P数量=CPU核心数
```

### 创建和控制

```go
// 创建
go func() {
    fmt.Println("goroutine")
}()

// 等待（WaitGroup）
import "sync"

var wg sync.WaitGroup

for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(n int) {
        defer wg.Done()
        process(n)
    }(i)
}

wg.Wait()

// 限制并发数（worker pool）
func worker Pool(tasks <-chan Task, results chan<- Result) {
    const numWorkers = 5
    var wg sync.WaitGroup
    
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for task := range tasks {
                results <- process(task)
            }
        }()
    }
    
    wg.Wait()
    close(results)
}
```

## channel详解

### 无缓冲channel

发送阻塞直到接收，接收阻塞直到发送。同步通信。

```go
ch := make(chan int)

// 发送（阻塞）
go func() {
    ch <- 42
}()

// 接收（阻塞）
value := <-ch

// 应用：同步点
done := make(chan struct{})
go func() {
    work()
    done <- struct{}{}  // 信号
}()
<-done  // 等待完成
```

### 缓冲channel

缓冲满才阻塞发送，缓冲空才阻塞接收。异步通信。

```go
ch := make(chan int, 3)

ch <- 1  // 不阻塞
ch <- 2
ch <- 3
// ch <- 4  // 阻塞（缓冲满）

<-ch     // 1
<-ch     // 2
// 现在可以再发送2个
```

### 单向channel

限制channel操作方向，增强类型安全。

```go
// 只发送channel
func send(ch chan<- int) {
    ch <- 42
    // <-ch  // 编译错误
}

// 只接收channel
func receive(ch <-chan int) {
    value := <-ch
    // ch <- 42  // 编译错误
}

// 函数参数自动转换
ch := make(chan int)
go send(ch)     // chan int → chan<- int
receive(ch)     // chan int → <-chan int
```

### select多路复用

```go
select {
case msg := <-ch1:
    fmt.Println("ch1:", msg)
case msg := <-ch2:
    fmt.Println("ch2:", msg)
case ch3 <- value:
    fmt.Println("sent to ch3")
default:
    fmt.Println("no ready channel")
}

// 超时模式
select {
case result := <-ch:
    fmt.Println(result)
case <-time.After(time.Second):
    fmt.Println("timeout")
}

// 取消模式
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

select {
case <-ch:
    // 正常处理
case <-ctx.Done():
    fmt.Println("cancelled")
}

// for-select循环
for {
    select {
    case msg := <-ch:
        process(msg)
    case <-quit:
        return
    }
}
```

## sync包

### Mutex（互斥锁）

```go
import "sync"

type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

### RWMutex（读写锁）

```go
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) string {
    c.mu.RLock()         // 读锁（多个goroutine可同时读）
    defer c.mu.RUnlock()
    return c.data[key]
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()          // 写锁（独占）
    defer c.mu.Unlock()
    c.data[key] = value
}
```

### Once（单次执行）

```go
var once sync.Once
var instance *Singleton

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{}  // 仅执行一次
    })
    return instance
}
```

### Pool（对象池）

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)  // 创建新对象
    },
}

func process() {
    buf := bufferPool.Get().(*bytes.Buffer)  // 获取
    defer bufferPool.Put(buf)                // 归还
    
    buf.Reset()  // 重置
    buf.WriteString("data")
    // 使用buf
}
```

### Map（并发安全map）

```go
var m sync.Map

// 操作
m.Store("key", "value")          // 存储
value, ok := m.Load("key")       // 读取
m.Delete("key")                  // 删除
value, loaded := m.LoadOrStore("key", "value")  // 读取或存储
m.Range(func(key, value interface{}) bool {
    fmt.Println(key, value)
    return true  // 继续遍历
})
```

### Cond（条件变量）

```go
var (
    mu    sync.Mutex
    cond  = sync.NewCond(&mu)
    ready bool
)

// 等待
go func() {
    cond.L.Lock()
    for !ready {  // 循环检查（防止虚假唤醒）
        cond.Wait()
    }
    cond.L.Unlock()
    // 开始工作
}()

// 通知
cond.L.Lock()
ready = true
cond.Signal()     // 唤醒一个
// cond.Broadcast()  // 唤醒所有
cond.L.Unlock()
```

## context包

传递截止时间、取消信号、请求作用域值。

```go
import "context"

// 创建context
ctx := context.Background()           // 根context
ctx := context.TODO()                 // 临时context

// WithCancel：取消信号
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

go func() {
    <-ctx.Done()
    fmt.Println("cancelled")
}()

cancel()  // 取消

// WithTimeout：超时
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

select {
case <-time.After(10 * time.Second):
    fmt.Println("work done")
case <-ctx.Done():
    fmt.Println("timeout:", ctx.Err())
}

// WithDeadline：截止时间
deadline := time.Now().Add(5 * time.Second)
ctx, cancel := context.WithDeadline(context.Background(), deadline)

// WithValue：传递值（少用，仅请求作用域数据）
ctx := context.WithValue(context.Background(), "userID", 123)
userID := ctx.Value("userID").(int)
```

### context使用模式

```go
// HTTP服务器
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()  // 请求的context
    
    // 调用其他服务
    result, err := callService(ctx, data)
    if err != nil {
        // 处理错误
    }
}

func callService(ctx context.Context, data Data) (Result, error) {
    select {
    case result := <-doWork(data):
        return result, nil
    case <-ctx.Done():
        return Result{}, ctx.Err()  // 请求取消或超时
    }
}
```

## 并发模式

### Worker Pool

```go
func workerPool(jobs <-chan int, results chan<- int) {
    const numWorkers = 5
    
    for i := 0; i < numWorkers; i++ {
        go worker(i, jobs, results)
    }
}

func worker(id int, jobs <-chan int, results chan<- int) {
    for job := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, job)
        time.Sleep(time.Second)
        results <- job * 2
    }
}

// 使用
jobs := make(chan int, 100)
results := make(chan int, 100)

go workerPool(jobs, results)

// 发送任务
for i := 1; i <= 10; i++ {
    jobs <- i
}
close(jobs)

// 接收结果
for i := 1; i <= 10; i++ {
    <-results
}
```

### Fan-out/Fan-in

```go
// Fan-out：分发任务到多个goroutine
func fanOut(input <-chan int) []<-chan int {
    const numWorkers = 3
    channels := make([]<-chan int, numWorkers)
    
    for i := 0; i < numWorkers; i++ {
        channels[i] = worker(input)
    }
    
    return channels
}

// Fan-in：合并多个channel
func fanIn(channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup
    
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for val := range c {
                out <- val
            }
        }(ch)
    }
    
    go func() {
        wg.Wait()
        close(out)
    }()
    
    return out
}
```

### Pipeline

```go
// 生成器
func gen(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

// 平方
func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

// 组合pipeline
nums := gen(1, 2, 3, 4, 5)
squared := square(nums)

for n := range squared {
    fmt.Println(n)  // 1, 4, 9, 16, 25
}
```

### 超时和取消

```go
// 超时模式
func doWithTimeout(timeout time.Duration) error {
    done := make(chan struct{})
    
    go func() {
        work()
        done <- struct{}{}
    }()
    
    select {
    case <-done:
        return nil
    case <-time.After(timeout):
        return errors.New("timeout")
    }
}

// 取消模式
func doWithCancel(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            // 执行工作
            if finished {
                return nil
            }
        }
    }
}
```

## 原子操作

```go
import "sync/atomic"

var count int64

// 原子操作
atomic.AddInt64(&count, 1)       // 原子加
atomic.LoadInt64(&count)         // 原子读
atomic.StoreInt64(&count, 100)   // 原子写
atomic.SwapInt64(&count, 200)    // 原子交换
atomic.CompareAndSwapInt64(&count, 200, 300)  // CAS

// Value（原子值）
var config atomic.Value

// 存储
config.Store(Config{Timeout: 5})

// 读取
cfg := config.Load().(Config)
```

## 并发安全数据结构

### 线程安全Map

```go
type SafeMap struct {
    mu sync.RWMutex
    data map[string]interface{}
}

func NewSafeMap() *SafeMap {
    return &SafeMap{
        data: make(map[string]interface{}),
    }
}

func (m *SafeMap) Set(key string, value interface{}) {
    m.mu.Lock()
    defer m.mu.Unlock()
    m.data[key] = value
}

func (m *SafeMap) Get(key string) (interface{}, bool) {
    m.mu.RLock()
    defer m.mu.RUnlock()
    value, ok := m.data[key]
    return value, ok
}

// 或使用sync.Map（高并发读多写少）
var m sync.Map
m.Store("key", "value")
value, ok := m.Load("key")
```

### 线程安全Slice

```go
type SafeSlice struct {
    mu   sync.Mutex
    data []int
}

func (s *SafeSlice) Append(val int) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.data = append(s.data, val)
}

func (s *SafeSlice) Get(i int) int {
    s.mu.Lock()
    defer s.mu.Unlock()
    return s.data[i]
}
```

## 常见并发问题

### 竞态条件

```go
// ❌ 竞态条件
var count int

func increment() {
    count++  // 非原子：读-改-写
}

for i := 0; i < 1000; i++ {
    go increment()
}
// count结果不确定（<1000）

// ✅ 使用互斥锁
var (
    count int
    mu    sync.Mutex
)

func increment() {
    mu.Lock()
    count++
    mu.Unlock()
}

// ✅ 使用原子操作
var count int64

func increment() {
    atomic.AddInt64(&count, 1)
}

// ✅ 使用channel
counter := make(chan int)
go func() {
    count := 0
    for range counter {
        count++
    }
}()

for i := 0; i < 1000; i++ {
    counter <- 1
}
```

### 死锁

```go
// ❌ 死锁：互相等待
ch := make(chan int)
ch <- 42  // 阻塞（无接收者）
<-ch

// ✅ 使用goroutine
ch := make(chan int)
go func() {
    ch <- 42
}()
<-ch

// ❌ 所有goroutine都sleep
func main() {
    var wg sync.WaitGroup
    wg.Add(1)
    go func() {
        wg.Wait()  // 等待自己（死锁）
    }()
    wg.Wait()
}
```

### goroutine泄漏

```go
// ❌ 泄漏：channel永远不关闭
func leak() {
    ch := make(chan int)
    go func() {
        for val := range ch {  // 永远阻塞
            process(val)
        }
    }()
    // ch从未关闭，goroutine永远不退出
}

// ✅ 使用done channel
func noLeak() {
    ch := make(chan int)
    done := make(chan struct{})
    
    go func() {
        for {
            select {
            case val := <-ch:
                process(val)
            case <-done:
                return  // 退出goroutine
            }
        }
    }()
    
    // 清理
    close(done)
}

// ✅ 使用context
func noLeak2(ctx context.Context) {
    ch := make(chan int)
    
    go func() {
        for {
            select {
            case val := <-ch:
                process(val)
            case <-ctx.Done():
                return
            }
        }
    }()
}
```

## 并发工具

### errgroup

```go
import "golang.org/x/sync/errgroup"

func process Files(files []string) error {
    g, ctx := errgroup.WithContext(context.Background())
    
    for _, file := range files {
        file := file  // 捕获循环变量
        g.Go(func() error {
            return processFile(ctx, file)
        })
    }
    
    // 等待所有goroutine，返回第一个错误
    return g.Wait()
}
```

### singleflight

防止缓存击穿，同时只执行一次。

```go
import "golang.org/x/sync/singleflight"

var g singleflight.Group

func getValue(key string) (string, error) {
    value, err, _ := g.Do(key, func() (interface{}, error) {
        // 耗时操作（如数据库查询）
        return fetchFromDB(key)
    })
    return value.(string), err
}

// 多个goroutine同时调用getValue("同一key")
// 只有第一个真正执行，其他等待并共享结果
```

### 限流（rate limiting）

```go
import "golang.org/x/time/rate"

// 令牌桶算法
limiter := rate.NewLimiter(10, 100)  // 每秒10个，桶容量100

// 等待许可
if err := limiter.Wait(ctx); err != nil {
    return err
}

// 尝试获取（非阻塞）
if !limiter.Allow() {
    return errors.New("rate limit exceeded")
}
```

## 性能优化

### 减少锁竞争

```go
// ❌ 粗粒度锁
type Counter struct {
    mu    sync.Mutex
    count map[string]int
}

func (c *Counter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count[key]++
}

// ✅ 细粒度锁（分段锁）
type ShardedCounter struct {
    shards [16]struct {
        mu    sync.Mutex
        count map[string]int
    }
}

func (c *ShardedCounter) Inc(key string) {
    shard := &c.shards[hash(key)%16]
    shard.mu.Lock()
    shard.count[key]++
    shard.mu.Unlock()
}
```

### channel vs mutex

```go
// channel：通信和同步
// mutex：保护共享数据

// CPU密集型：mutex（开销小）
// IO密集型：channel（清晰）

// 简单计数：atomic
// 复杂状态：mutex
// 消息传递：channel
```

## 并发测试

### 竞态检测

```bash
# 编译时启用竞态检测器
go build -race

# 测试时检测
go test -race

# 运行时检测
go run -race main.go
```

### 压力测试

```go
func TestConcurrent(t *testing.T) {
    const numGoroutines = 100
    const numIterations = 1000
    
    var wg sync.WaitGroup
    for i := 0; i < numGoroutines; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for j := 0; j < numIterations; j++ {
                operation()
            }
        }()
    }
    wg.Wait()
}
```

## 最佳实践

1. **channel传递所有权**：发送后不再访问
2. **关闭channel的发送方关闭**：接收方不关闭
3. **用select避免阻塞**：加default或timeout
4. **context传递取消信号**：优于done channel
5. **defer解锁**：确保锁释放
6. **读多写少用RWMutex**：提升性能
7. **原子操作简单计数**：比mutex轻量
8. **避免goroutine泄漏**：确保退出路径
9. **竞态检测常开**：测试和开发环境
10. **小心闭包捕获变量**：循环中传参

**核心：** Don't communicate by sharing memory; share memory by communicating.

