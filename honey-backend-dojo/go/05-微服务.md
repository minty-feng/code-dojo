# 05-Go微服务实践

微服务架构将大型应用拆分为独立小服务，Go语言的轻量和并发特性使其成为微服务首选。

## 微服务架构

### 服务划分原则

```
按业务能力划分：
├── user-service      # 用户管理
├── order-service     # 订单处理
├── payment-service   # 支付
├── inventory-service # 库存
└── notification-service  # 通知

按技术边界：
├── auth-gateway      # 认证网关
├── api-gateway       # API网关
└── backend-services  # 后端服务
```

### 服务间通信

**同步通信：**
- HTTP/RESTful（简单，广泛支持）
- gRPC（高性能，类型安全）

**异步通信：**
- 消息队列（RabbitMQ、Kafka）
- 事件驱动

## API网关

### 使用Gin构建

```go
package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
    "net/http/httputil"
    "net/url"
)

type Service struct {
    Name string
    URL  string
}

var services = map[string]*Service{
    "user":    {Name: "user", URL: "http://localhost:8081"},
    "order":   {Name: "order", URL: "http://localhost:8082"},
    "product": {Name: "product", URL: "http://localhost:8083"},
}

func proxy(targetURL string) gin.HandlerFunc {
    target, _ := url.Parse(targetURL)
    proxy := httputil.NewSingleHostReverseProxy(target)
    
    return func(c *gin.Context) {
        proxy.ServeHTTP(c.Writer, c.Request)
    }
}

func main() {
    r := gin.Default()
    
    // 路由到不同服务
    r.Any("/api/users/*path", proxy(services["user"].URL))
    r.Any("/api/orders/*path", proxy(services["order"].URL))
    r.Any("/api/products/*path", proxy(services["product"].URL))
    
    r.Run(":8080")
}
```

## 服务注册与发现

### Consul

```go
import (
    "github.com/hashicorp/consul/api"
)

// 注册服务
func registerService(name, address string, port int) error {
    config := api.DefaultConfig()
    client, err := api.NewClient(config)
    if err != nil {
        return err
    }
    
    registration := &api.AgentServiceRegistration{
        ID:      name + "-" + address,
        Name:    name,
        Address: address,
        Port:    port,
        Check: &api.AgentServiceCheck{
            HTTP:                           fmt.Sprintf("http://%s:%d/health", address, port),
            Interval:                       "10s",
            Timeout:                        "3s",
            DeregisterCriticalServiceAfter: "30s",
        },
    }
    
    return client.Agent().ServiceRegister(registration)
}

// 发现服务
func discoverService(name string) (string, error) {
    config := api.DefaultConfig()
    client, err := api.NewClient(config)
    if err != nil {
        return "", err
    }
    
    services, _, err := client.Health().Service(name, "", true, nil)
    if err != nil || len(services) == 0 {
        return "", err
    }
    
    service := services[0].Service
    return fmt.Sprintf("%s:%d", service.Address, service.Port), nil
}
```

## 配置中心

### Viper + Consul

```go
import (
    "github.com/spf13/viper"
    _ "github.com/spf13/viper/remote"
)

func initConfig() error {
    viper.AddRemoteProvider("consul", "localhost:8500", "config/myapp")
    viper.SetConfigType("json")
    
    if err := viper.ReadRemoteConfig(); err != nil {
        return err
    }
    
    // 监听配置变化
    go func() {
        for {
            time.Sleep(time.Second * 5)
            err := viper.WatchRemoteConfig()
            if err != nil {
                log.Println("watch config error:", err)
            }
        }
    }()
    
    return nil
}
```

## 链路追踪

### OpenTelemetry

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/trace"
)

func initTracer() {
    // 初始化tracer（Jaeger/Zipkin）
    // ...
}

func businessLogic(ctx context.Context) error {
    tracer := otel.Tracer("myservice")
    ctx, span := tracer.Start(ctx, "businessLogic")
    defer span.End()
    
    // 添加属性
    span.SetAttributes(attribute.String("user.id", "123"))
    
    // 调用其他服务（传递context）
    callOtherService(ctx)
    
    return nil
}
```

## 熔断与限流

### hystrix-go（熔断）

```go
import "github.com/afex/hystrix-go/hystrix"

func init() {
    hystrix.ConfigureCommand("my_command", hystrix.CommandConfig{
        Timeout:               1000,  // 超时1秒
        MaxConcurrentRequests: 100,   // 最大并发
        ErrorPercentThreshold: 25,    // 错误率25%触发熔断
    })
}

func callService() (interface{}, error) {
    output := make(chan interface{}, 1)
    errors := hystrix.Go("my_command", func() error {
        // 正常逻辑
        result, err := doSomething()
        if err != nil {
            return err
        }
        output <- result
        return nil
    }, func(err error) error {
        // 降级逻辑
        output <- getDefaultValue()
        return nil
    })
    
    select {
    case out := <-output:
        return out, nil
    case err := <-errors:
        return nil, err
    }
}
```

### 令牌桶限流

```go
import "golang.org/x/time/rate"

type RateLimiter struct {
    limiter *rate.Limiter
}

func NewRateLimiter(r rate.Limit, b int) *RateLimiter {
    return &RateLimiter{
        limiter: rate.NewLimiter(r, b),
    }
}

func (rl *RateLimiter) Middleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        if !rl.limiter.Allow() {
            c.JSON(429, gin.H{"error": "too many requests"})
            c.Abort()
            return
        }
        c.Next()
    }
}

// 使用
r := gin.Default()
r.Use(NewRateLimiter(10, 100).Middleware())  // 10 req/s
```

## 消息队列

### RabbitMQ

```go
import "github.com/streadway/amqp"

// 发布消息
func publishMessage(exchange, routingKey string, body []byte) error {
    conn, _ := amqp.Dial("amqp://guest:guest@localhost:5672/")
    defer conn.Close()
    
    ch, _ := conn.Channel()
    defer ch.Close()
    
    return ch.Publish(
        exchange,
        routingKey,
        false,
        false,
        amqp.Publishing{
            ContentType: "application/json",
            Body:        body,
        },
    )
}

// 消费消息
func consumeMessages(queueName string, handler func([]byte)) error {
    conn, _ := amqp.Dial("amqp://guest:guest@localhost:5672/")
    defer conn.Close()
    
    ch, _ := conn.Channel()
    defer ch.Close()
    
    msgs, _ := ch.Consume(queueName, "", true, false, false, false, nil)
    
    for msg := range msgs {
        handler(msg.Body)
    }
    
    return nil
}
```

### Kafka

```go
import "github.com/Shopify/sarama"

// 生产者
func produceKafka(topic string, message []byte) error {
    config := sarama.NewConfig()
    config.Producer.Return.Successes = true
    
    producer, err := sarama.NewSyncProducer([]string{"localhost:9092"}, config)
    if err != nil {
        return err
    }
    defer producer.Close()
    
    msg := &sarama.ProducerMessage{
        Topic: topic,
        Value: sarama.ByteEncoder(message),
    }
    
    _, _, err = producer.SendMessage(msg)
    return err
}

// 消费者
func consumeKafka(topic string, handler func([]byte)) error {
    consumer, err := sarama.NewConsumer([]string{"localhost:9092"}, nil)
    if err != nil {
        return err
    }
    defer consumer.Close()
    
    partitionConsumer, err := consumer.ConsumePartition(topic, 0, sarama.OffsetNewest)
    if err != nil {
        return err
    }
    defer partitionConsumer.Close()
    
    for message := range partitionConsumer.Messages() {
        handler(message.Value)
    }
    
    return nil
}
```

## 服务健康检查

```go
func healthCheck() gin.HandlerFunc {
    return func(c *gin.Context) {
        // 检查数据库
        if err := db.Ping(); err != nil {
            c.JSON(503, gin.H{
                "status": "unhealthy",
                "database": "down",
            })
            return
        }
        
        // 检查Redis
        if err := redis.Ping().Err(); err != nil {
            c.JSON(503, gin.H{
                "status": "unhealthy",
                "redis": "down",
            })
            return
        }
        
        c.JSON(200, gin.H{
            "status": "healthy",
        })
    }
}

r.GET("/health", healthCheck())
```

## 分布式事务

### Saga模式

```go
type SagaStep struct {
    Action     func() error
    Compensate func() error
}

type Saga struct {
    steps []SagaStep
}

func (s *Saga) Execute() error {
    executed := []SagaStep{}
    
    for _, step := range s.steps {
        if err := step.Action(); err != nil {
            // 回滚已执行的步骤
            for i := len(executed) - 1; i >= 0; i-- {
                executed[i].Compensate()
            }
            return err
        }
        executed = append(executed, step)
    }
    
    return nil
}

// 使用
saga := &Saga{
    steps: []SagaStep{
        {
            Action:     createOrder,
            Compensate: cancelOrder,
        },
        {
            Action:     reserveInventory,
            Compensate: releaseInventory,
        },
        {
            Action:     processPayment,
            Compensate: refundPayment,
        },
    },
}

if err := saga.Execute(); err != nil {
    log.Println("Transaction failed:", err)
}
```

## 服务监控

### Prometheus + Grafana

```go
import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )
    
    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)

func init() {
    prometheus.MustRegister(httpRequestsTotal)
    prometheus.MustRegister(httpRequestDuration)
}

func prometheusMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        
        c.Next()
        
        duration := time.Since(start).Seconds()
        status := strconv.Itoa(c.Writer.Status())
        
        httpRequestsTotal.WithLabelValues(c.Request.Method, c.FullPath(), status).Inc()
        httpRequestDuration.WithLabelValues(c.Request.Method, c.FullPath()).Observe(duration)
    }
}

// 暴露metrics
r.GET("/metrics", gin.WrapH(promhttp.Handler()))
r.Use(prometheusMiddleware())
```

## 微服务项目结构

```
microservice/
├── cmd/
│   └── server/
│       └── main.go           # 程序入口
├── internal/
│   ├── handler/              # HTTP处理器
│   ├── service/              # 业务逻辑
│   ├── repository/           # 数据访问
│   └── model/                # 数据模型
├── pkg/                      # 可导出的库
│   ├── middleware/
│   └── util/
├── api/
│   └── proto/                # gRPC定义
├── config/
│   └── config.yaml
├── deployments/
│   ├── docker-compose.yml
│   └── k8s/
├── go.mod
└── README.md
```

## Docker Compose部署

```yaml
# docker-compose.yml
version: '3.8'

services:
  user-service:
    build: ./user-service
    ports:
      - "8081:8080"
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/users
    depends_on:
      - db
      - redis
  
  order-service:
    build: ./order-service
    ports:
      - "8082:8080"
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/orders
    depends_on:
      - db
      - kafka
  
  api-gateway:
    build: ./api-gateway
    ports:
      - "8080:8080"
    depends_on:
      - user-service
      - order-service
  
  db:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: postgres
  
  redis:
    image: redis:7-alpine
  
  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
  
  consul:
    image: consul:latest
    ports:
      - "8500:8500"
```

## Kubernetes部署

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: user-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## 最佳实践

1. **单一职责**：每个服务专注一个业务能力
2. **独立部署**：服务独立构建、测试、部署
3. **数据隔离**：每个服务独立数据库
4. **API网关**：统一入口，认证、限流、路由
5. **服务发现**：动态注册和发现
6. **配置中心**：集中管理配置
7. **链路追踪**：分布式追踪请求
8. **熔断降级**：防止雪崩
9. **异步通信**：解耦服务，消息队列
10. **监控告警**：Prometheus + Grafana

**核心：** 微服务提升灵活性，但增加复杂度，需完善基础设施支撑。

