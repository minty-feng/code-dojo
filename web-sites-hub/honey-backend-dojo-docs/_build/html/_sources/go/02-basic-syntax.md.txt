# 02-Go基础语法

Go语法简洁，吸收C系语言优点，去除冗余特性。25个关键字，学习成本低。

## 数据类型

### 基本类型

```go
// 整型
int8, int16, int32, int64
uint8, uint16, uint32, uint64
int                    // 32或64位（取决于平台）
uint                   // 无符号int
byte                   // uint8别名
rune                   // int32别名，表示Unicode码点

// 浮点型
float32, float64

// 复数
complex64, complex128

// 布尔型
bool                   // true或false

// 字符串
string                 // UTF-8编码，不可变
```

### 类型零值

Go变量声明后自动初始化为零值（无未定义行为）。

```go
var i int        // 0
var f float64    // 0.0
var b bool       // false
var s string     // ""（空字符串）
var p *int       // nil
var slice []int  // nil
var m map[string]int  // nil
var ch chan int  // nil
var fn func()    // nil
```

### 类型转换

```go
// 必须显式转换（无隐式转换）
var i int = 42
var f float64 = float64(i)
var u uint = uint(i)

// 字符串转换
import "strconv"

i, err := strconv.Atoi("123")     // 字符串→int
s := strconv.Itoa(123)            // int→字符串
f, err := strconv.ParseFloat("3.14", 64)
s := strconv.FormatFloat(3.14, 'f', 2, 64)
```

## 变量声明

### 四种方式

```go
// 1. var声明
var name string = "Alice"
var age int = 25

// 2. 类型推断
var name = "Alice"  // 自动推断为string

// 3. 短变量声明（函数内）
name := "Alice"     // 最常用
age := 25

// 4. 批量声明
var (
    name string = "Alice"
    age  int    = 25
    city string
)
```

### 常量

```go
const Pi = 3.14159
const MaxSize = 100

// 批量常量
const (
    Red   = 0
    Green = 1
    Blue  = 2
)

// iota（自增）
const (
    _  = iota  // 0，跳过
    KB = 1 << (10 * iota)  // 1024
    MB                      // 1048576
    GB                      // 1073741824
)

const (
    Monday = iota + 1  // 1
    Tuesday            // 2
    Wednesday          // 3
)
```

## 基本语法

### 控制结构

```go
// if（无需括号）
if x > 0 {
    // ...
} else if x < 0 {
    // ...
} else {
    // ...
}

// if with初始化
if err := doSomething(); err != nil {
    return err
}
// err作用域仅在if块内

// switch（无需break，自动break）
switch x {
case 1:
    // ...
case 2, 3:  // 多个条件
    // ...
default:
    // ...
}

// switch with初始化
switch err := doSomething(); err {
case nil:
    // ...
default:
    return err
}

// switch无表达式（替代if-else链）
switch {
case x > 0:
    // ...
case x < 0:
    // ...
default:
    // ...
}

// fallthrough（显式穿透）
switch x {
case 1:
    fmt.Println("one")
    fallthrough  // 继续执行case 2
case 2:
    fmt.Println("two")
}

// for循环（唯一循环语句）
for i := 0; i < 10; i++ {
    // ...
}

// while风格
for condition {
    // ...
}

// 无限循环
for {
    // ...
    break
}

// range遍历
for i, v := range slice {
    // i是索引，v是值
}

for k, v := range map {
    // k是键，v是值
}

for i := range slice {
    // 仅索引
}

for _, v := range slice {
    // 忽略索引（_是空标识符）
}

// 标签和goto（少用）
Loop:
for {
    for {
        break Loop  // 跳出外层循环
    }
}
```

## 函数

### 函数定义

```go
// 基本函数
func add(a int, b int) int {
    return a + b
}

// 简化参数
func add(a, b int) int {
    return a + b
}

// 多返回值
func swap(a, b int) (int, int) {
    return b, a
}

x, y := swap(1, 2)

// 命名返回值
func divide(a, b int) (result int, err error) {
    if b == 0 {
        err = errors.New("division by zero")
        return  // 返回result和err的当前值
    }
    result = a / b
    return
}

// 可变参数
func sum(nums ...int) int {
    total := 0
    for _, num := range nums {
        total += num
    }
    return total
}

sum(1, 2, 3, 4, 5)
nums := []int{1, 2, 3}
sum(nums...)  // 展开切片
```

### 函数类型和闭包

```go
// 函数类型
type Operation func(int, int) int

func apply(op Operation, a, b int) int {
    return op(a, b)
}

apply(func(a, b int) int { return a + b }, 3, 4)

// 闭包
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

c := counter()
c()  // 1
c()  // 2
```

### defer延迟执行

```go
// defer按LIFO顺序执行
func example() {
    defer fmt.Println("3")
    defer fmt.Println("2")
    fmt.Println("1")
}
// 输出：1 2 3

// 常用于资源清理
func readFile() error {
    f, err := os.Open("file.txt")
    if err != nil {
        return err
    }
    defer f.Close()  // 函数返回前自动关闭
    
    // 读取文件
    return nil
}

// defer参数立即求值
func deferTest() {
    x := 1
    defer fmt.Println(x)  // 立即求值：1
    x = 2
    // 输出：1（不是2）
}
```

## 数据结构

### 数组

固定长度，值类型。

```go
// 声明
var arr [5]int              // [0, 0, 0, 0, 0]
arr := [5]int{1, 2, 3, 4, 5}
arr := [...]int{1, 2, 3}    // 自动计算长度

// 访问
arr[0] = 10
len(arr)  // 5

// 数组是值类型
arr2 := arr  // 复制整个数组
```

### 切片（slice）

动态数组，引用类型，最常用。

```go
// 创建
var s []int                  // nil切片
s := []int{1, 2, 3}
s := make([]int, 5)          // 长度5，容量5
s := make([]int, 5, 10)      // 长度5，容量10

// 切片数组
arr := [5]int{1, 2, 3, 4, 5}
s := arr[1:4]                // [2, 3, 4]
s := arr[:3]                 // [1, 2, 3]
s := arr[2:]                 // [3, 4, 5]

// 操作
s = append(s, 6)             // 追加元素
s = append(s, 7, 8, 9)       // 追加多个
s = append(s1, s2...)        // 合并切片
copy(dst, src)               // 复制
len(s)                       // 长度
cap(s)                       // 容量

// 删除元素
s = append(s[:i], s[i+1:]...)  // 删除索引i
s = s[:len(s)-1]               // 删除最后一个
s = s[1:]                      // 删除第一个
```

### 映射（map）

哈希表，引用类型。

```go
// 创建
var m map[string]int         // nil map（不能写入）
m := map[string]int{}        // 空map
m := make(map[string]int)
m := map[string]int{"a": 1, "b": 2}

// 操作
m["key"] = value             // 添加/更新
value := m["key"]            // 读取
value, ok := m["key"]        // 检查存在性
if ok {
    // key存在
}

delete(m, "key")             // 删除
len(m)                       // 元素个数

// 遍历（无序）
for k, v := range m {
    fmt.Println(k, v)
}

for k := range m {  // 仅键
    // ...
}
```

### 结构体（struct）

```go
// 定义
type Person struct {
    Name string
    Age  int
    City string
}

// 创建
p1 := Person{"Alice", 25, "Beijing"}
p2 := Person{Name: "Bob", Age: 30}  // 字段名初始化
p3 := Person{Name: "Charlie"}       // 未指定字段为零值
var p4 Person                       // 零值初始化

// 访问
p1.Name = "Alice2"
age := p1.Age

// 结构体指针
p := &Person{Name: "Alice"}
p.Age = 25  // 自动解引用（无需p->Age）

// 匿名字段（嵌入）
type Student struct {
    Person        // 匿名字段，继承Person的字段
    StudentID string
}

s := Student{Person: Person{Name: "Alice"}, StudentID: "123"}
s.Name  // 直接访问Person.Name

// 标签（tag）
type User struct {
    Name  string `json:"name" db:"user_name"`
    Email string `json:"email" validate:"required,email"`
}
```

## 指针

Go有指针但无指针运算，更安全。

```go
// 指针声明
var p *int
p = &x  // 取地址

// 解引用
*p = 10

// new分配内存
p := new(int)  // 返回*int，值为0

// 指针vs值
func modifyValue(x int) {
    x = 100  // 不影响原变量
}

func modifyPointer(p *int) {
    *p = 100  // 修改原变量
}

x := 1
modifyValue(x)
fmt.Println(x)  // 1

modifyPointer(&x)
fmt.Println(x)  // 100
```

## 方法

Go无类，用方法为类型添加行为。

```go
type Rectangle struct {
    Width, Height float64
}

// 值接收者
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// 指针接收者（可修改）
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}

r := Rectangle{Width: 10, Height: 5}
r.Area()    // 50
r.Scale(2)  // Width=20, Height=10

// 任意类型都可定义方法
type MyInt int

func (m MyInt) IsEven() bool {
    return m%2 == 0
}

var x MyInt = 10
x.IsEven()  // true
```

**选择：** 需要修改或大对象用指针接收者，否则用值接收者。

## 接口

隐式实现，鸭子类型。

```go
// 接口定义
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// 组合接口
type ReadWriter interface {
    Reader
    Writer
}

// 实现接口（无需显式声明）
type File struct {}

func (f *File) Read(p []byte) (int, error) {
    // 实现Read，File就实现了Reader接口
    return 0, nil
}

// 空接口（任意类型）
interface{}  // 或 any（Go 1.18+）

func Print(v interface{}) {
    fmt.Println(v)
}

Print(42)
Print("hello")
Print([]int{1, 2, 3})

// 类型断言
var i interface{} = "hello"
s := i.(string)              // "hello"
s, ok := i.(string)          // "hello", true（安全断言）
n, ok := i.(int)             // 0, false

// 类型switch
switch v := i.(type) {
case int:
    fmt.Printf("int: %d\n", v)
case string:
    fmt.Printf("string: %s\n", v)
default:
    fmt.Printf("unknown type\n")
}
```

## 错误处理

Go使用多返回值处理错误，无异常机制。

```go
import "errors"

// 返回错误
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// 使用
result, err := divide(10, 0)
if err != nil {
    log.Fatal(err)  // 处理错误
}

// 自定义错误
type MyError struct {
    Code    int
    Message string
}

func (e *MyError) Error() string {
    return fmt.Sprintf("code %d: %s", e.Code, e.Message)
}

// errors.Is（Go 1.13+）
var ErrNotFound = errors.New("not found")

if errors.Is(err, ErrNotFound) {
    // 错误匹配
}

// errors.As（类型转换）
var myErr *MyError
if errors.As(err, &myErr) {
    fmt.Println(myErr.Code)
}

// 错误包装
return fmt.Errorf("failed to process: %w", err)
```

## 并发基础

### goroutine

轻量级线程，栈初始2KB，可创建百万级。

```go
// 启动goroutine
go func() {
    fmt.Println("goroutine")
}()

go processData()

// 匿名函数闭包
for i := 0; i < 5; i++ {
    go func(n int) {  // 参数传递，避免闭包陷阱
        fmt.Println(n)
    }(i)
}

// 等待goroutine（用sync.WaitGroup）
import "sync"

var wg sync.WaitGroup

for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(n int) {
        defer wg.Done()
        fmt.Println(n)
    }(i)
}

wg.Wait()  // 等待所有goroutine完成
```

### channel

goroutine间通信，类型安全的管道。

```go
// 创建channel
ch := make(chan int)       // 无缓冲
ch := make(chan int, 10)   // 缓冲大小10

// 发送和接收
ch <- 42      // 发送
value := <-ch // 接收

// 关闭channel
close(ch)

// 接收检查关闭
value, ok := <-ch
if !ok {
    // channel已关闭
}

// range遍历（直到关闭）
for value := range ch {
    fmt.Println(value)
}

// select多路复用
select {
case msg1 := <-ch1:
    fmt.Println("ch1:", msg1)
case msg2 := <-ch2:
    fmt.Println("ch2:", msg2)
case ch3 <- value:
    fmt.Println("sent to ch3")
case <-time.After(time.Second):
    fmt.Println("timeout")
default:
    fmt.Println("no communication")
}
```

## 包和可见性

```go
// 包声明（每个文件）
package main

// 导入
import "fmt"
import (
    "fmt"
    "os"
)

// 别名
import f "fmt"
f.Println("hello")

// 点导入（不推荐）
import . "fmt"
Println("hello")  // 直接使用

// 仅初始化
import _ "image/png"  // 执行init函数

// 可见性：大写=导出（public），小写=未导出（private）
type PublicStruct struct {
    ExportedField   int   // 导出
    unexportedField int   // 未导出
}
```

## init函数

包初始化时自动执行，可有多个。

```go
var config Config

func init() {
    // 包初始化
    loadConfig()
}

func init() {
    // 可以有多个init
    setupDatabase()
}

// 执行顺序：
// 1. 导入包的init
// 2. 当前包变量初始化
// 3. 当前包init
// 4. main函数
```

## 类型系统

### 类型定义

```go
// type定义新类型
type MyInt int

var x MyInt = 10
var y int = 10
// x = y  // 错误！不同类型

// type别名（Go 1.9+）
type MyInt2 = int

var a MyInt2 = 10
var b int = 10
a = b  // OK，相同类型
```

### 类型嵌入

```go
// 嵌入结构体
type Engine struct {
    Power int
}

func (e *Engine) Start() {
    fmt.Println("Engine started")
}

type Car struct {
    Engine        // 嵌入，继承Engine的字段和方法
    Brand string
}

car := Car{Engine: Engine{Power: 200}, Brand: "Toyota"}
car.Power       // 200（提升字段）
car.Start()     // "Engine started"（提升方法）

// 嵌入接口
type ReadWriter struct {
    Reader
    Writer
}
```

## 常见陷阱

```go
// 1. range循环变量陷阱
for i, v := range slice {
    go func() {
        fmt.Println(i, v)  // 错误！闭包捕获变量，值可能变化
    }()
}

// 正确：传参
for i, v := range slice {
    go func(i, v int) {
        fmt.Println(i, v)
    }(i, v)
}

// 2. slice共享底层数组
arr := []int{1, 2, 3, 4, 5}
s1 := arr[0:2]  // [1, 2]
s2 := arr[1:3]  // [2, 3]
s1[1] = 999     // s2[0]也变成999（共享数组）

// 3. map并发读写panic
m := make(map[string]int)
go func() { m["key"] = 1 }()  // 写
go func() { _ = m["key"] }()  // 读（panic！）

// 使用sync.Map或加锁

// 4. nil map不能写入
var m map[string]int  // nil
// m["key"] = 1  // panic
m = make(map[string]int)  // 必须初始化

// 5. slice作为函数参数
func modify(s []int) {
    s[0] = 999  // 影响原slice（引用类型）
    s = append(s, 100)  // 不影响原slice（可能重新分配）
}
```

## 最佳实践

1. **短变量声明**：函数内优先用`:=`
2. **错误处理**：每个error都检查
3. **defer清理资源**：文件、锁、连接
4. **指针接收者**：修改对象或大对象
5. **命名返回值**：复杂函数增强可读性
6. **channel通信**：不要通过共享内存通信，通过通信共享内存
7. **select处理多channel**：超时、取消、多路复用
8. **空接口慎用**：丧失类型安全
9. **gofmt格式化**：自动化，无争议
10. **接口小而专注**：io.Reader只有一个方法

**核心：** Go追求简洁和并发，利用goroutine和channel构建高并发系统。

