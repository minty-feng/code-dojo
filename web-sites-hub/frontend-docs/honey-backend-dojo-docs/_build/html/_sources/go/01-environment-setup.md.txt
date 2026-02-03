# 01-Go环境搭建

## Go语言简介

Go由Google于2009年发布，Robert Griesemer、Rob Pike、Ken Thompson设计。静态类型、编译型语言，天生支持并发。

### 设计目标

- **编译速度快**：大型项目秒级编译
- **并发原生支持**：goroutine和channel
- **内存安全**：自动垃圾回收，无指针运算
- **简洁语法**：25个关键字，学习曲线平缓
- **高效执行**：接近C的性能

### 应用场景

**云原生基础设施：**
- Docker、Kubernetes容器编排
- etcd、Consul服务发现
- Prometheus监控系统

**Web后端：**
- 微服务API
- 高并发Web服务器
- RESTful/gRPC服务

**DevOps工具：**
- 命令行工具（Cobra、urfave/cli）
- 部署脚本
- 监控代理

**网络编程：**
- 代理服务器
- 负载均衡器
- VPN、隧道工具

**区块链：**
- Ethereum Go客户端（Geth）
- Hyperledger Fabric

### 语言特点

**优势：**
- 编译快，执行快（静态链接，单一可执行文件）
- 并发简单（goroutine比线程轻量1000倍）
- 内存安全（GC，无手动管理）
- 部署简单（单一二进制文件，无依赖）
- 标准库强大（HTTP、JSON、加密等）

**劣势：**
- 泛型支持晚（Go 1.18才引入）
- 错误处理冗余（if err != nil到处可见）
- 包管理演进（GOPATH → vendor → Go Modules）
- 缺少传统OOP（无继承、类）

## 安装Go

### Linux

```bash
# 下载
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz

# 解压到/usr/local
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz

# 配置环境变量（~/.bashrc或~/.zshrc）
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# 验证
go version
```

### macOS

```bash
# Homebrew
brew install go

# 验证
go version

# 环境变量（~/.zshrc）
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

### Windows

1. 下载MSI安装包：go.dev
2. 安装（自动配置PATH）
3. 验证：`go version`

## 环境配置

### GOPATH结构（Go 1.11之前）

```
$GOPATH/
├── bin/        # 可执行文件
├── pkg/        # 编译包缓存
└── src/        # 源代码
    └── github.com/
        └── username/
            └── project/
```

### Go Modules（Go 1.11+，推荐）

```bash
# 初始化模块
go mod init github.com/username/project

# 生成go.mod
module github.com/username/project

go 1.21

require (
    github.com/gin-gonic/gin v1.9.0
)

# 添加依赖
go get github.com/gin-gonic/gin

# 整理依赖
go mod tidy

# 下载依赖
go mod download

# 查看依赖图
go mod graph

# vendor目录（可选）
go mod vendor
```

## Hello World

### 基本程序

```go
// main.go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

```bash
# 运行
go run main.go

# 编译
go build main.go
./main

# 编译并安装到$GOPATH/bin
go install main.go
```

### 包和导入

```go
// math/add.go
package math

func Add(a, b int) int {  // 大写字母开头=导出（public）
    return a + b
}

func subtract(a, b int) int {  // 小写=未导出（private）
    return a - b
}

// main.go
package main

import (
    "fmt"
    "myproject/math"  // 导入本地包
    "github.com/gin-gonic/gin"  // 导入第三方包
)

func main() {
    result := math.Add(3, 4)
    fmt.Println(result)
}
```

## 开发工具

### VS Code

轻量级，Go支持优秀。

**必装插件：**
- Go（官方插件）

**配置（settings.json）：**
```json
{
    "go.useLanguageServer": true,
    "go.lintTool": "golangci-lint",
    "go.lintOnSave": "workspace",
    "go.formatTool": "goimports",
    "editor.formatOnSave": true,
    "go.testFlags": ["-v"],
    "go.coverOnSave": true
}
```

### GoLand

JetBrains专业Go IDE。

**特性：**
- 智能补全
- 重构工具
- 调试器
- 测试集成
- 数据库工具

### Vim/Neovim

轻量高效，vim-go插件强大。

```vim
" 安装vim-go
Plug 'fatih/vim-go'

" 常用命令
:GoRun          " 运行
:GoBuild        " 编译
:GoTest         " 测试
:GoCoverage     " 覆盖率
:GoDoc          " 文档
:GoFmt          " 格式化
```

## Go工具链

### go命令

```bash
# 运行
go run main.go

# 编译
go build                    # 当前目录
go build -o myapp          # 指定输出名
go build -ldflags="-s -w"  # 减小二进制大小

# 安装
go install github.com/user/tool@latest

# 获取依赖
go get github.com/gin-gonic/gin
go get -u                  # 更新依赖

# 测试
go test                    # 当前包
go test ./...              # 所有包
go test -v                 # 详细输出
go test -cover             # 覆盖率
go test -bench=.           # 基准测试

# 格式化
go fmt ./...               # 格式化所有文件
gofmt -w main.go          # 写入文件

# 代码检查
go vet ./...              # 静态分析

# 文档
go doc fmt.Println
go doc -all fmt

# 清理
go clean
go clean -modcache         # 清理模块缓存
```

### 第三方工具

```bash
# goimports：自动管理导入
go install golang.org/x/tools/cmd/goimports@latest
goimports -w main.go

# golangci-lint：综合代码检查
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
golangci-lint run

# delve：调试器
go install github.com/go-delve/delve/cmd/dlv@latest
dlv debug main.go

# air：热重载
go install github.com/cosmtrek/air@latest
air

# godoc：本地文档服务器
go install golang.org/x/tools/cmd/godoc@latest
godoc -http=:6060
```

## 项目结构

### 标准布局

```
myproject/
├── go.mod              # 模块定义
├── go.sum              # 依赖校验
├── main.go             # 程序入口
├── cmd/                # 可执行文件
│   └── server/
│       └── main.go
├── internal/           # 私有代码（不可导入）
│   ├── config/
│   └── service/
├── pkg/                # 可导入的库代码
│   └── utils/
├── api/                # API定义
│   └── proto/
├── web/                # Web资源
│   ├── static/
│   └── templates/
├── configs/            # 配置文件
├── scripts/            # 脚本
├── docs/               # 文档
├── test/               # 额外测试
└── vendor/             # 依赖（可选）
```

## 编译和交叉编译

### 编译选项

```bash
# 基本编译
go build main.go

# 优化二进制大小
go build -ldflags="-s -w" main.go
# -s：去除符号表
# -w：去除调试信息

# 静态链接（不依赖动态库）
CGO_ENABLED=0 go build -a -installsuffix cgo main.go

# 设置版本信息
go build -ldflags="-X main.version=1.0.0" main.go
```

### 交叉编译

```bash
# Linux
GOOS=linux GOARCH=amd64 go build main.go

# Windows
GOOS=windows GOARCH=amd64 go build -o app.exe main.go

# macOS
GOOS=darwin GOARCH=amd64 go build main.go

# ARM
GOOS=linux GOARCH=arm64 go build main.go

# 查看支持的平台
go tool dist list
```

## 代码规范

### 命名约定

```go
// 包名：小写，单个单词
package server

// 导出标识符：大写开头
type User struct {}
func NewUser() *User {}
const MaxSize = 100

// 未导出：小写开头
func processData() {}
var count int

// 缩写：保持一致
// URL, HTTP（全大写）或url, http（全小写）
func GetHTTPClient() {}  // ✓
func GetHttpClient() {}  // ✗

// 接口：通常以er结尾
type Reader interface {}
type Writer interface {}

// 变量：驼峰命名
var userName string
var maxRetryCount int
```

### 代码风格

```go
// gofmt自动格式化，无争议

// 缩进：tab
if condition {
    statement
}

// 大括号：K&R风格（强制）
func example() {  // ✓
    // ...
}

func example()    // ✗ 编译错误
{
    // ...
}

// 注释：包、导出类型、导出函数必须有文档注释
// Package math provides mathematical functions.
package math

// Add returns the sum of a and b.
func Add(a, b int) int {
    return a + b
}
```

## 性能分析

### pprof

```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()
    
    // 程序逻辑
}
```

```bash
# CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# 内存profile
go tool pprof http://localhost:6060/debug/pprof/heap

# goroutine
go tool pprof http://localhost:6060/debug/pprof/goroutine

# 分析二进制
go test -cpuprofile=cpu.prof -bench=.
go tool pprof cpu.prof
```

### Benchmark

```go
// benchmark测试
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(3, 4)
    }
}

// 运行
// go test -bench=. -benchmem
// 输出：ns/op（纳秒/操作）、B/op（字节/操作）、allocs/op（分配次数/操作）
```

## 常用命令速查

```bash
go version     # Go版本
go env         # 环境变量

go run         # 运行
go build       # 编译
go install     # 编译+安装
go get         # 下载依赖

go test        # 测试
go fmt         # 格式化
go vet         # 静态检查
go doc         # 文档

go mod init    # 初始化模块
go mod tidy    # 整理依赖
go mod download # 下载依赖
go mod vendor  # 创建vendor

go clean       # 清理
go generate    # 代码生成
go list        # 列出包
```

**核心：** Go工具链完整，单一命令完成大部分任务。

