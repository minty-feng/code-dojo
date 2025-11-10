# 06-Go性能优化

Go性能已很优秀，但仍有优化空间。理解runtime、内存分配、并发模型是优化关键。

## 性能分析工具

### pprof

CPU和内存分析，定位瓶颈。

```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    // 启动pprof HTTP服务
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()
    
    // 程序逻辑
}
```

**使用：**
```bash
# CPU profile（采样30秒）
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# 内存profile
go tool pprof http://localhost:6060/debug/pprof/heap

# goroutine
go tool pprof http://localhost:6060/debug/pprof/goroutine

# 阻塞profile
go tool pprof http://localhost:6060/debug/pprof/block

# 互斥锁profile
go tool pprof http://localhost:6060/debug/pprof/mutex

# 交互式命令
(pprof) top          # 前10个耗时函数
(pprof) list funcName # 查看函数代码
(pprof) web          # 生成调用图（需graphviz）
```

### Benchmark

```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}

func BenchmarkConcat(b *testing.B) {
    b.ResetTimer()  // 重置计时器（排除初始化）
    for i := 0; i < b.N; i++ {
        concat("hello", "world")
    }
}

func BenchmarkWithSetup(b *testing.B) {
    data := setupData()  // 准备数据
    b.ResetTimer()
    
    for i := 0; i < b.N; i++ {
        process(data)
    }
}
```

```bash
# 运行benchmark
go test -bench=. -benchmem

# 输出示例
BenchmarkAdd-8      1000000000    0.25 ns/op    0 B/op    0 allocs/op
# 8核，10亿次，每次0.25ns，0字节分配，0次分配

# 比较优化前后
go test -bench=. -benchmem > old.txt
# 修改代码
go test -bench=. -benchmem > new.txt
benchcmp old.txt new.txt
```

### trace

分析goroutine调度、GC、系统调用。

```go
import "runtime/trace"

func main() {
    f, _ := os.Create("trace.out")
    defer f.Close()
    
    trace.Start(f)
    defer trace.Stop()
    
    // 程序逻辑
}
```

```bash
# 生成trace
go run main.go

# 查看trace
go tool trace trace.out
# 浏览器打开，查看goroutine、GC、系统调用时间线
```

## 内存优化

### 减少内存分配

```go
// ❌ 每次都分配
func processItems(items []int) []int {
    result := []int{}  // 零长度slice
    for _, item := range items {
        result = append(result, item*2)  // 可能多次扩容
    }
    return result
}

// ✅ 预分配容量
func processItems(items []int) []int {
    result := make([]int, 0, len(items))  // 预分配
    for _, item := range items {
        result = append(result, item*2)
    }
    return result
}

// ✅ 原地修改（无需新slice）
func processItems(items []int) {
    for i := range items {
        items[i] *= 2
    }
}
```

### 字符串拼接

```go
// ❌ +拼接（每次都创建新字符串）
func concat(strs []string) string {
    result := ""
    for _, s := range strs {
        result += s  // O(n²)时间，大量分配
    }
    return result
}

// ✅ strings.Builder
func concat(strs []string) string {
    var builder strings.Builder
    builder.Grow(estimatedSize)  // 预分配
    for _, s := range strs {
        builder.WriteString(s)
    }
    return builder.String()
}

// ✅ bytes.Buffer（类似）
func concat(strs []string) string {
    var buf bytes.Buffer
    for _, s := range strs {
        buf.WriteString(s)
    }
    return buf.String()
}

// ✅ strings.Join（简单场景）
result := strings.Join(strs, "")
```

### 对象池（sync.Pool）

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func processData(data []byte) {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()  // 重置
        bufferPool.Put(buf)  // 归还
    }()
    
    buf.Write(data)
    // 使用buf
}
```

### 避免逃逸到堆

```go
// ❌ 逃逸到堆
func createUser(name string) *User {
    u := User{Name: name}  // 逃逸
    return &u
}

// ✅ 栈分配（值返回）
func createUser(name string) User {
    return User{Name: name}
}

// 查看逃逸分析
// go build -gcflags="-m" main.go
```

## 并发优化

### goroutine池

```go
// ❌ 无限制创建
for i := 0; i < 10000; i++ {
    go process(i)  // 创建1万个goroutine
}

// ✅ worker pool
func workerPool(jobs <-chan Job, results chan<- Result) {
    const numWorkers = 10
    var wg sync.WaitGroup
    
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }
    
    wg.Wait()
    close(results)
}
```

### 减少锁竞争

```go
// ❌ 粗粒度锁
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Inc() {
    c.mu.Lock()
    c.count++
    c.mu.Unlock()
}

// ✅ 原子操作（无锁）
type Counter struct {
    count int64
}

func (c *Counter) Inc() {
    atomic.AddInt64(&c.count, 1)
}

// ✅ 分段锁（高并发）
type ShardedMap struct {
    shards [16]struct {
        mu   sync.RWMutex
        data map[string]interface{}
    }
}

func (m *ShardedMap) Set(key string, value interface{}) {
    shard := &m.shards[hash(key)%16]
    shard.mu.Lock()
    shard.data[key] = value
    shard.mu.Unlock()
}
```

### channel vs mutex

```go
// Benchmark对比
func BenchmarkMutex(b *testing.B) {
    var mu sync.Mutex
    counter := 0
    
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            mu.Lock()
            counter++
            mu.Unlock()
        }
    })
}

func BenchmarkChannel(b *testing.B) {
    ch := make(chan int, 100)
    go func() {
        counter := 0
        for range ch {
            counter++
        }
    }()
    
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            ch <- 1
        }
    })
}

// 结果：mutex通常快2-5倍（简单场景）
// channel优势：解耦、更清晰
```

## CPU优化

### 避免不必要的反射

```go
// ❌ 反射（慢10-100倍）
func sumReflect(slice interface{}) int {
    v := reflect.ValueOf(slice)
    sum := 0
    for i := 0; i < v.Len(); i++ {
        sum += int(v.Index(i).Int())
    }
    return sum
}

// ✅ 直接类型断言
func sumDirect(slice []int) int {
    sum := 0
    for _, v := range slice {
        sum += v
    }
    return sum
}
```

### 内联优化

```go
// 小函数自动内联
func add(a, b int) int {
    return a + b
}

// 查看内联决策
// go build -gcflags="-m=2" main.go

// 禁止内联（调试用）
//go:noinline
func noInline(a, b int) int {
    return a + b
}
```

### 循环优化

```go
// ❌ 重复计算
for i := 0; i < len(slice); i++ {
    // len(slice)每次都调用
}

// ✅ 缓存长度
n := len(slice)
for i := 0; i < n; i++ {
    // ...
}

// ✅ range（编译器优化）
for i, v := range slice {
    // ...
}
```

## I/O优化

### 缓冲I/O

```go
// ❌ 无缓冲
file, _ := os.Open("file.txt")
scanner := bufio.NewScanner(file)
for scanner.Scan() {
    line := scanner.Text()
    // 处理每行
}

// ✅ 指定缓冲大小
file, _ := os.Open("file.txt")
reader := bufio.NewReaderSize(file, 1024*1024)  // 1MB缓冲
scanner := bufio.NewScanner(reader)
```

### 批量操作

```go
// ❌ 逐条插入
for _, item := range items {
    db.Exec("INSERT INTO table VALUES (?)", item)
}

// ✅ 批量插入
tx, _ := db.Begin()
stmt, _ := tx.Prepare("INSERT INTO table VALUES (?)")
for _, item := range items {
    stmt.Exec(item)
}
tx.Commit()
```

## 编译优化

### 编译选项

```bash
# 默认优化
go build

# 禁用优化（调试）
go build -gcflags="-N -l"

# 内联级别
go build -gcflags="-l=4"  # 更激进的内联

# 逃逸分析详情
go build -gcflags="-m -m"

# 减小二进制大小
go build -ldflags="-s -w"
# -s: 去除符号表
# -w: 去除调试信息
```

### 代码生成

```go
//go:generate stringer -type=Status
type Status int

const (
    Pending Status = iota
    Running
    Completed
)

// 生成String()方法
// go generate
```

## GC优化

### 减少GC压力

```go
// ❌ 频繁分配小对象
func process() {
    for i := 0; i < 1000000; i++ {
        obj := &MyStruct{}  // 100万次分配
        use(obj)
    }
}

// ✅ 复用对象
var pool = sync.Pool{
    New: func() interface{} {
        return &MyStruct{}
    },
}

func process() {
    for i := 0; i < 1000000; i++ {
        obj := pool.Get().(*MyStruct)
        use(obj)
        pool.Put(obj)
    }
}
```

### 调整GC参数

```go
import "runtime/debug"

// 设置GC百分比（默认100）
debug.SetGCPercent(200)  // 降低GC频率，增加内存占用

// 手动触发GC（少用）
runtime.GC()

// 查看GC统计
var m runtime.MemStats
runtime.ReadMemStats(&m)
fmt.Printf("Alloc = %v MB", m.Alloc/1024/1024)
fmt.Printf("TotalAlloc = %v MB", m.TotalAlloc/1024/1024)
fmt.Printf("NumGC = %v\n", m.NumGC)
```

## JSON优化

### 标准库 vs 第三方

```go
// 标准库encoding/json
import "encoding/json"

// jsoniter（兼容，快2-3倍）
import jsoniter "github.com/json-iterator/go"
var json = jsoniter.ConfigCompatibleWithStandardLibrary

// easyjson（代码生成，快5-10倍）
//go:generate easyjson -all user.go
type User struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}
// 自动生成MarshalJSON/UnmarshalJSON

// sonic（字节跳动，AVX2加速）
import "github.com/bytedance/sonic"
```

### 流式解析

```go
// ❌ 一次性读取大JSON
var data LargeData
json.Unmarshal(largeJSON, &data)

// ✅ 流式解析
decoder := json.NewDecoder(reader)
for {
    var item Item
    if err := decoder.Decode(&item); err == io.EOF {
        break
    }
    process(item)
}
```

## 数据库优化

### 连接池

```go
db, _ := sql.Open("mysql", dsn)

// 配置连接池
db.SetMaxOpenConns(25)              // 最大连接数
db.SetMaxIdleConns(5)               // 最大空闲连接
db.SetConnMaxLifetime(5*time.Minute)// 连接最大生命周期
db.SetConnMaxIdleTime(10*time.Minute)// 空闲连接最大时间
```

### 预编译语句

```go
// ❌ 每次都Prepare
for _, user := range users {
    db.Exec("INSERT INTO users (name) VALUES (?)", user.Name)
}

// ✅ 复用Prepare
stmt, _ := db.Prepare("INSERT INTO users (name) VALUES (?)")
defer stmt.Close()

for _, user := range users {
    stmt.Exec(user.Name)
}
```

## 网络优化

### HTTP连接池

```go
var client = &http.Client{
    Timeout: 10 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
        // 启用HTTP/2
        ForceAttemptHTTP2: true,
    },
}
```

### gRPC连接复用

```go
// 复用连接
conn, _ := grpc.Dial(address, grpc.WithInsecure())
defer conn.Close()

client := pb.NewServiceClient(conn)

// 多次调用复用同一连接
for i := 0; i < 1000; i++ {
    client.Call(ctx, req)
}
```

## 实战案例

### 优化前

```go
func processUsers(userIDs []int) ([]User, error) {
    var users []User
    
    for _, id := range userIDs {
        // 逐个查询数据库
        var user User
        db.QueryRow("SELECT * FROM users WHERE id = ?", id).Scan(&user)
        users = append(users, user)
    }
    
    return users, nil
}
```

### 优化后

```go
func processUsers(userIDs []int) ([]User, error) {
    // 1. 批量查询
    placeholders := strings.Repeat("?,", len(userIDs))
    placeholders = placeholders[:len(placeholders)-1]
    
    query := fmt.Sprintf("SELECT * FROM users WHERE id IN (%s)", placeholders)
    
    args := make([]interface{}, len(userIDs))
    for i, id := range userIDs {
        args[i] = id
    }
    
    rows, err := db.Query(query, args...)
    if err != nil {
        return nil, err
    }
    defer rows.Close()
    
    // 2. 预分配容量
    users := make([]User, 0, len(userIDs))
    
    for rows.Next() {
        var user User
        rows.Scan(&user)
        users = append(users, user)
    }
    
    return users, nil
}
```

**性能提升：10-100倍（取决于网络延迟）**

## 性能清单

**内存：**
- [ ] 预分配slice容量
- [ ] 使用sync.Pool复用对象
- [ ] 字符串拼接用strings.Builder
- [ ] 减少堆分配（避免逃逸）
- [ ] 大对象传指针，小对象传值

**并发：**
- [ ] 限制goroutine数量（worker pool）
- [ ] 简单计数用atomic
- [ ] 读多写少用sync.RWMutex
- [ ] 减少锁粒度（分段锁）

**CPU：**
- [ ] 避免反射（热路径）
- [ ] 缓存重复计算
- [ ] 批量处理代替逐个

**I/O：**
- [ ] 缓冲I/O
- [ ] 批量数据库操作
- [ ] 连接池复用
- [ ] HTTP keep-alive

**其他：**
- [ ] 用benchmark验证
- [ ] pprof定位瓶颈
- [ ] 选择快速JSON库
- [ ] 启用编译优化

**核心：** 先测量，后优化。过早优化是万恶之源。

