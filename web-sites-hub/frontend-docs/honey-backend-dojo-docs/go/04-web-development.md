# 04-Go Web开发

Go标准库net/http功能完整，第三方框架生态丰富。天生高并发，适合构建高性能Web服务。

## 标准库HTTP服务器

### 基础服务器

```go
package main

import (
    "fmt"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %s!", r.URL.Path[1:])
}

func main() {
    http.HandleFunc("/", handler)
    http.ListenAndServe(":8080", nil)
}
```

### 路由和处理器

```go
// HandlerFunc
func homeHandler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Home"))
}

// Handler接口
type MyHandler struct{}

func (h *MyHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Custom handler"))
}

// 注册
http.HandleFunc("/home", homeHandler)
http.Handle("/custom", &MyHandler{})

// 自定义ServeMux
mux := http.NewServeMux()
mux.HandleFunc("/api/users", usersHandler)
mux.HandleFunc("/api/posts", postsHandler)

http.ListenAndServe(":8080", mux)
```

### 请求和响应

```go
func handler(w http.ResponseWriter, r *http.Request) {
    // 请求方法
    method := r.Method  // GET, POST, PUT, DELETE
    
    // URL参数
    id := r.URL.Query().Get("id")
    page := r.URL.Query().Get("page")
    
    // 路径参数（需第三方路由）
    // vars := mux.Vars(r)
    // id := vars["id"]
    
    // 表单数据
    r.ParseForm()
    username := r.FormValue("username")
    
    // JSON请求体
    var data struct {
        Name string `json:"name"`
        Age  int    `json:"age"`
    }
    json.NewDecoder(r.Body).Decode(&data)
    
    // 请求头
    token := r.Header.Get("Authorization")
    
    // 设置响应头
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)  // 200
    
    // JSON响应
    json.NewEncoder(w).Encode(map[string]string{
        "message": "success",
    })
}
```

## Gin框架

轻量高性能Web框架，类似Express。

### 基本使用

```go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()  // 带Logger和Recovery中间件
    
    // GET
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })
    
    // 路径参数
    r.GET("/users/:id", func(c *gin.Context) {
        id := c.Param("id")
        c.JSON(200, gin.H{"id": id})
    })
    
    // 查询参数
    r.GET("/search", func(c *gin.Context) {
        query := c.DefaultQuery("q", "default")
        page := c.Query("page")
        c.JSON(200, gin.H{"query": query, "page": page})
    })
    
    // POST JSON
    r.POST("/users", func(c *gin.Context) {
        var user struct {
            Name string `json:"name" binding:"required"`
            Age  int    `json:"age" binding:"gte=0,lte=130"`
        }
        
        if err := c.ShouldBindJSON(&user); err != nil {
            c.JSON(400, gin.H{"error": err.Error()})
            return
        }
        
        c.JSON(201, user)
    })
    
    r.Run(":8080")
}
```

### 路由分组

```go
r := gin.Default()

// API v1
v1 := r.Group("/api/v1")
{
    v1.GET("/users", listUsers)
    v1.POST("/users", createUser)
    v1.GET("/users/:id", getUser)
    v1.PUT("/users/:id", updateUser)
    v1.DELETE("/users/:id", deleteUser)
}

// API v2
v2 := r.Group("/api/v2")
{
    v2.GET("/users", listUsersV2)
}
```

### 中间件

```go
// 自定义中间件
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        
        c.Next()  // 执行后续处理器
        
        duration := time.Since(start)
        status := c.Writer.Status()
        log.Printf("%s %s %d %v", c.Request.Method, c.Request.URL.Path, status, duration)
    }
}

// 全局中间件
r.Use(Logger())
r.Use(gin.Recovery())

// 路由级中间件
r.GET("/admin", AuthRequired(), adminHandler)

// 分组中间件
admin := r.Group("/admin", AuthRequired())
{
    admin.GET("/users", listUsers)
}

// 认证中间件示例
func AuthRequired() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.JSON(401, gin.H{"error": "unauthorized"})
            c.Abort()  // 阻止后续处理器
            return
        }
        
        // 验证token
        userID, err := validateToken(token)
        if err != nil {
            c.JSON(401, gin.H{"error": "invalid token"})
            c.Abort()
            return
        }
        
        c.Set("userID", userID)  // 传递给后续处理器
        c.Next()
    }
}

func protectedHandler(c *gin.Context) {
    userID := c.GetInt("userID")
    c.JSON(200, gin.H{"userID": userID})
}
```

## 数据库操作

### database/sql（标准库）

```go
import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)

// 连接
db, err := sql.Open("mysql", "user:password@tcp(localhost:3306)/dbname")
if err != nil {
    log.Fatal(err)
}
defer db.Close()

// 配置连接池
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(5)
db.SetConnMaxLifetime(5 * time.Minute)

// 查询单行
var name string
var age int
err = db.QueryRow("SELECT name, age FROM users WHERE id = ?", 1).Scan(&name, &age)
if err == sql.ErrNoRows {
    // 未找到
}

// 查询多行
rows, err := db.Query("SELECT id, name FROM users WHERE age > ?", 18)
defer rows.Close()

for rows.Next() {
    var id int
    var name string
    rows.Scan(&id, &name)
    fmt.Println(id, name)
}

// 插入
result, err := db.Exec("INSERT INTO users (name, age) VALUES (?, ?)", "Alice", 25)
lastID, _ := result.LastInsertId()
affected, _ := result.RowsAffected()

// 事务
tx, err := db.Begin()
if err != nil {
    log.Fatal(err)
}

_, err = tx.Exec("INSERT INTO users ...")
if err != nil {
    tx.Rollback()
    return err
}

err = tx.Commit()
```

### GORM（ORM）

```go
import "gorm.io/gorm"
import "gorm.io/driver/mysql"

// 连接
dsn := "user:pass@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4"
db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})

// 定义模型
type User struct {
    ID        uint           `gorm:"primaryKey"`
    Name      string         `gorm:"size:100;not null"`
    Email     string         `gorm:"uniqueIndex"`
    Age       int
    CreatedAt time.Time
    UpdatedAt time.Time
}

// 自动迁移
db.AutoMigrate(&User{})

// 创建
user := User{Name: "Alice", Email: "alice@example.com", Age: 25}
db.Create(&user)

// 查询
var user User
db.First(&user, 1)                    // 主键查询
db.Where("name = ?", "Alice").First(&user)
db.Where("age > ?", 18).Find(&users)

// 更新
db.Model(&user).Update("age", 26)
db.Model(&user).Updates(User{Age: 26, Email: "new@example.com"})

// 删除
db.Delete(&user)

// 链式调用
db.Where("age > ?", 18).
   Order("created_at desc").
   Limit(10).
   Find(&users)
```

## RESTful API示例

```go
package main

import (
    "github.com/gin-gonic/gin"
    "gorm.io/gorm"
)

type User struct {
    gorm.Model
    Name  string `json:"name"`
    Email string `json:"email"`
}

func main() {
    r := gin.Default()
    
    // GET /api/users
    r.GET("/api/users", func(c *gin.Context) {
        var users []User
        db.Find(&users)
        c.JSON(200, users)
    })
    
    // GET /api/users/:id
    r.GET("/api/users/:id", func(c *gin.Context) {
        var user User
        if err := db.First(&user, c.Param("id")).Error; err != nil {
            c.JSON(404, gin.H{"error": "User not found"})
            return
        }
        c.JSON(200, user)
    })
    
    // POST /api/users
    r.POST("/api/users", func(c *gin.Context) {
        var user User
        if err := c.ShouldBindJSON(&user); err != nil {
            c.JSON(400, gin.H{"error": err.Error()})
            return
        }
        
        db.Create(&user)
        c.JSON(201, user)
    })
    
    // PUT /api/users/:id
    r.PUT("/api/users/:id", func(c *gin.Context) {
        var user User
        if err := db.First(&user, c.Param("id")).Error; err != nil {
            c.JSON(404, gin.H{"error": "User not found"})
            return
        }
        
        if err := c.ShouldBindJSON(&user); err != nil {
            c.JSON(400, gin.H{"error": err.Error()})
            return
        }
        
        db.Save(&user)
        c.JSON(200, user)
    })
    
    // DELETE /api/users/:id
    r.DELETE("/api/users/:id", func(c *gin.Context) {
        if err := db.Delete(&User{}, c.Param("id")).Error; err != nil {
            c.JSON(404, gin.H{"error": "User not found"})
            return
        }
        c.JSON(204, nil)
    })
    
    r.Run(":8080")
}
```

## 中间件模式

### CORS

```go
func CORS() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
        c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
        
        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(204)
            return
        }
        
        c.Next()
    }
}

r.Use(CORS())
```

### 限流

```go
import "golang.org/x/time/rate"

func RateLimiter(r rate.Limit, b int) gin.HandlerFunc {
    limiter := rate.NewLimiter(r, b)
    
    return func(c *gin.Context) {
        if !limiter.Allow() {
            c.JSON(429, gin.H{"error": "rate limit exceeded"})
            c.Abort()
            return
        }
        c.Next()
    }
}

r.Use(RateLimiter(10, 100))  // 每秒10个请求
```

## HTTP客户端

```go
import "net/http"

// GET请求
resp, err := http.Get("https://api.example.com/data")
if err != nil {
    log.Fatal(err)
}
defer resp.Body.Close()

body, err := ioutil.ReadAll(resp.Body)

// POST JSON
data := map[string]string{"key": "value"}
jsonData, _ := json.Marshal(data)

resp, err := http.Post("https://api.example.com",
    "application/json",
    bytes.NewBuffer(jsonData))

// 自定义请求
client := &http.Client{
    Timeout: 10 * time.Second,
}

req, err := http.NewRequest("PUT", url, body)
req.Header.Set("Content-Type", "application/json")
req.Header.Set("Authorization", "Bearer token")

resp, err := client.Do(req)
```

## WebSocket

```go
import "github.com/gorilla/websocket"

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool {
        return true  // 允许跨域
    },
}

func wsHandler(w http.ResponseWriter, r *http.Request) {
    // 升级HTTP到WebSocket
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Println(err)
        return
    }
    defer conn.Close()
    
    for {
        // 读取消息
        messageType, message, err := conn.ReadMessage()
        if err != nil {
            break
        }
        
        // 处理消息
        log.Printf("Received: %s", message)
        
        // 发送消息
        err = conn.WriteMessage(messageType, message)
        if err != nil {
            break
        }
    }
}

http.HandleFunc("/ws", wsHandler)
```

## gRPC

高性能RPC框架，基于HTTP/2和Protocol Buffers。

### Protocol Buffers定义

```protobuf
// user.proto
syntax = "proto3";

package user;

service UserService {
    rpc GetUser(GetUserRequest) returns (User);
    rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
}

message User {
    int64 id = 1;
    string name = 2;
    string email = 3;
}

message GetUserRequest {
    int64 id = 1;
}

message ListUsersRequest {
    int32 page = 1;
    int32 page_size = 2;
}

message ListUsersResponse {
    repeated User users = 1;
}
```

### 服务端实现

```go
// 生成代码
// protoc --go_out=. --go-grpc_out=. user.proto

type server struct {
    pb.UnimplementedUserServiceServer
}

func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    // 查询数据库
    user := &pb.User{
        Id:    req.Id,
        Name:  "Alice",
        Email: "alice@example.com",
    }
    return user, nil
}

func main() {
    lis, _ := net.Listen("tcp", ":50051")
    s := grpc.NewServer()
    pb.RegisterUserServiceServer(s, &server{})
    s.Serve(lis)
}
```

### 客户端调用

```go
conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
defer conn.Close()

client := pb.NewUserServiceClient(conn)

// 调用
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()

user, err := client.GetUser(ctx, &pb.GetUserRequest{Id: 1})
if err != nil {
    log.Fatal(err)
}

fmt.Println(user.Name)
```

## 配置管理

### Viper

统一配置管理，支持多种格式。

```go
import "github.com/spf13/viper"

func initConfig() {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath(".")
    
    // 读取配置
    if err := viper.ReadInConfig(); err != nil {
        log.Fatal(err)
    }
    
    // 环境变量
    viper.AutomaticEnv()
    
    // 默认值
    viper.SetDefault("port", 8080)
}

// 使用
port := viper.GetInt("port")
dbHost := viper.GetString("database.host")
```

### YAML配置示例

```yaml
# config.yaml
server:
  port: 8080
  host: 0.0.0.0

database:
  host: localhost
  port: 3306
  user: root
  password: secret
  dbname: mydb

redis:
  addr: localhost:6379
  password: ""
  db: 0
```

## 日志

### 标准库log

```go
import "log"

log.Println("info message")
log.Printf("formatted: %d", 42)
log.Fatal("fatal error")   // 打印后exit(1)
log.Panic("panic message") // 打印后panic

// 自定义logger
logger := log.New(os.Stdout, "[APP] ", log.LstdFlags|log.Lshortfile)
logger.Println("custom log")
```

### logrus（结构化日志）

```go
import "github.com/sirupsen/logrus"

log := logrus.New()

// 设置格式
log.SetFormatter(&logrus.JSONFormatter{})

// 设置级别
log.SetLevel(logrus.InfoLevel)

// 使用
log.WithFields(logrus.Fields{
    "user_id": 123,
    "action":  "login",
}).Info("User logged in")

log.WithError(err).Error("Failed to process")
```

### zap（高性能）

```go
import "go.uber.org/zap"

logger, _ := zap.NewProduction()
defer logger.Sync()

logger.Info("user login",
    zap.String("username", "alice"),
    zap.Int("user_id", 123),
)

// 开发环境
logger, _ := zap.NewDevelopment()
```

## 测试

### 单元测试

```go
// add_test.go
package math

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5
    if result != expected {
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}

// 表格驱动测试
func TestAddTable(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.want {
                t.Errorf("got %d, want %d", got, tt.want)
            }
        })
    }
}
```

### HTTP测试

```go
func TestHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/api/users", nil)
    w := httptest.NewRecorder()
    
    handler(w, req)
    
    if w.Code != 200 {
        t.Errorf("got %d, want 200", w.Code)
    }
}

// Gin测试
func TestGinRoute(t *testing.T) {
    r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "pong"})
    })
    
    w := httptest.NewRecorder()
    req, _ := http.NewRequest("GET", "/ping", nil)
    r.ServeHTTP(w, req)
    
    assert.Equal(t, 200, w.Code)
}
```

## 性能优化

### JSON序列化

```go
// 标准库encoding/json
json.Marshal(data)    // 通用，性能一般

// jsoniter（快2-3倍）
import jsoniter "github.com/json-iterator/go"
var json = jsoniter.ConfigCompatibleWithStandardLibrary

json.Marshal(data)

// easyjson（代码生成，快5-10倍）
// 需要生成代码：easyjson -all user.go
user.MarshalJSON()
```

### 连接池复用

```go
// HTTP客户端连接池
var client = &http.Client{
    Timeout: 10 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
    },
}
```

## 部署

### 构建

```bash
# 编译
CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# 减小体积
go build -ldflags="-s -w" -o app .

# upx压缩（可选）
upx -9 app
```

### Docker

```dockerfile
# 多阶段构建
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o app .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/app .

EXPOSE 8080
CMD ["./app"]
```

**核心：** Go天生适合Web开发，标准库强大，性能优秀。

