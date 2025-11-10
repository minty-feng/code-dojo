# 05-WebSocket与性能优化

WebSocket实现双向实时通信，性能优化涵盖事件循环、内存管理、集群等方面。

## WebSocket

### Socket.IO

```bash
npm install socket.io
```

**服务端：**
```javascript
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: '*'
    }
});

// 连接事件
io.on('connection', (socket) => {
    console.log('用户连接:', socket.id);
    
    // 接收消息
    socket.on('message', (data) => {
        console.log('收到消息:', data);
        
        // 回复客户端
        socket.emit('message', { text: 'Server received' });
        
        // 广播给所有客户端
        io.emit('message', data);
        
        // 广播给除自己外的所有客户端
        socket.broadcast.emit('message', data);
    });
    
    // 加入房间
    socket.on('join', (room) => {
        socket.join(room);
        io.to(room).emit('message', `${socket.id} joined ${room}`);
    });
    
    // 离开房间
    socket.on('leave', (room) => {
        socket.leave(room);
    });
    
    // 房间内广播
    socket.on('room-message', (room, data) => {
        io.to(room).emit('message', data);
    });
    
    // 断开连接
    socket.on('disconnect', () => {
        console.log('用户断开:', socket.id);
    });
});

server.listen(3000);
```

**客户端：**
```javascript
const socket = io('http://localhost:3000');

// 连接事件
socket.on('connect', () => {
    console.log('已连接:', socket.id);
});

// 发送消息
socket.emit('message', { text: 'Hello' });

// 接收消息
socket.on('message', (data) => {
    console.log('收到:', data);
});

// 加入房间
socket.emit('join', 'room1');

// 断开连接
socket.on('disconnect', () => {
    console.log('连接断开');
});
```

### ws（原生WebSocket）

```bash
npm install ws
```

```javascript
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
    console.log('新连接');
    
    // 接收消息
    ws.on('message', (message) => {
        console.log('收到:', message.toString());
        
        // 发送消息
        ws.send('Server received: ' + message);
    });
    
    // 广播
    wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(message);
        }
    });
    
    ws.on('close', () => {
        console.log('连接关闭');
    });
    
    ws.on('error', (error) => {
        console.error('错误:', error);
    });
});

// 心跳检测
setInterval(() => {
    wss.clients.forEach((ws) => {
        if (!ws.isAlive) {
            return ws.terminate();
        }
        
        ws.isAlive = false;
        ws.ping();
    });
}, 30000);

wss.on('connection', (ws) => {
    ws.isAlive = true;
    ws.on('pong', () => {
        ws.isAlive = true;
    });
});
```

## 性能优化

### 集群模式

```javascript
const cluster = require('cluster');
const os = require('os');
const express = require('express');

if (cluster.isMaster) {
    const numCPUs = os.cpus().length;
    console.log(`主进程 ${process.pid} 启动`);
    console.log(`启动 ${numCPUs} 个工作进程`);
    
    // 创建工作进程
    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }
    
    // 工作进程退出时重启
    cluster.on('exit', (worker, code, signal) => {
        console.log(`工作进程 ${worker.process.pid} 退出`);
        cluster.fork();
    });
} else {
    // 工作进程运行Express
    const app = express();
    
    app.get('/', (req, res) => {
        res.send(`进程 ${process.pid} 处理请求`);
    });
    
    app.listen(3000, () => {
        console.log(`工作进程 ${process.pid} 启动`);
    });
}
```

### PM2

```bash
npm install -g pm2

# 启动
pm2 start app.js

# 集群模式
pm2 start app.js -i max  # 使用所有CPU核心
pm2 start app.js -i 4    # 4个实例

# 监控
pm2 list
pm2 monit

# 日志
pm2 logs
pm2 logs app

# 重启
pm2 restart app
pm2 reload app  # 0秒停机重启

# 停止
pm2 stop app
pm2 delete app

# 配置文件（ecosystem.config.js）
module.exports = {
    apps: [{
        name: 'myapp',
        script: './dist/index.js',
        instances: 'max',
        exec_mode: 'cluster',
        env: {
            NODE_ENV: 'development'
        },
        env_production: {
            NODE_ENV: 'production'
        }
    }]
};

# 使用配置
pm2 start ecosystem.config.js --env production
```

### 内存优化

```javascript
// ❌ 内存泄漏：全局变量积累
const cache = {};
app.get('/user/:id', (req, res) => {
    cache[req.params.id] = { /* 大对象 */ };  // 永不释放
});

// ✅ 使用LRU缓存
const LRU = require('lru-cache');
const cache = new LRU({
    max: 500,  // 最多500项
    ttl: 1000 * 60 * 5  // 5分钟过期
});

// ❌ 闭包陷阱
function createHandler() {
    const largeData = new Array(1000000);  // 大数组
    return () => {
        // 闭包持有largeData引用，无法释放
    };
}

// ✅ 及时清理
function createHandler() {
    let largeData = new Array(1000000);
    return () => {
        const result = processData(largeData);
        largeData = null;  // 清理引用
        return result;
    };
}

// 监控内存
setInterval(() => {
    const usage = process.memoryUsage();
    console.log({
        rss: `${Math.round(usage.rss / 1024 / 1024)} MB`,
        heapTotal: `${Math.round(usage.heapTotal / 1024 / 1024)} MB`,
        heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)} MB`,
        external: `${Math.round(usage.external / 1024 / 1024)} MB`
    });
}, 60000);
```

### CPU优化

```javascript
// ❌ CPU密集任务阻塞事件循环
app.get('/heavy', (req, res) => {
    const result = heavyComputation();  // 阻塞其他请求
    res.json({ result });
});

// ✅ 使用Worker Threads
const { Worker } = require('worker_threads');

app.get('/heavy', (req, res) => {
    const worker = new Worker('./heavy-task.js');
    
    worker.on('message', (result) => {
        res.json({ result });
    });
    
    worker.on('error', (err) => {
        res.status(500).json({ error: err.message });
    });
    
    worker.postMessage({ data: req.body });
});

// heavy-task.js
const { parentPort } = require('worker_threads');

parentPort.on('message', ({ data }) => {
    const result = heavyComputation(data);
    parentPort.postMessage(result);
});
```

### 缓存策略

```javascript
// 1. 内存缓存（单机）
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 });

app.get('/api/data', async (req, res) => {
    const cacheKey = 'data';
    
    let data = cache.get(cacheKey);
    if (data) {
        return res.json({ data, cached: true });
    }
    
    data = await fetchData();
    cache.set(cacheKey, data);
    res.json({ data, cached: false });
});

// 2. Redis缓存（分布式）
async function getCached(key, fetcher, ttl = 3600) {
    const cached = await redis.get(key);
    if (cached) {
        return JSON.parse(cached);
    }
    
    const data = await fetcher();
    await redis.set(key, JSON.stringify(data), 'EX', ttl);
    return data;
}

// 使用
const user = await getCached(
    `user:${id}`,
    () => User.findById(id),
    3600
);

// 3. HTTP缓存头
app.get('/static-data', (req, res) => {
    res.set('Cache-Control', 'public, max-age=3600');
    res.json({ data });
});
```

### 压缩响应

```javascript
const compression = require('compression');

app.use(compression({
    filter: (req, res) => {
        if (req.headers['x-no-compression']) {
            return false;
        }
        return compression.filter(req, res);
    },
    level: 6  // 压缩级别 0-9
}));
```

### 数据库优化

```javascript
// ❌ N+1查询
const posts = await Post.find();
for (const post of posts) {
    post.author = await User.findById(post.userId);  // N次查询
}

// ✅ 使用populate（Mongoose）
const posts = await Post.find().populate('author');

// ✅ 批量查询
const posts = await Post.find();
const userIds = [...new Set(posts.map(p => p.userId))];
const users = await User.find({ _id: { $in: userIds } });
const userMap = new Map(users.map(u => [u.id, u]));
posts.forEach(post => {
    post.author = userMap.get(post.userId);
});

// 索引优化
userSchema.index({ email: 1 });  // 单字段索引
userSchema.index({ name: 1, age: -1 });  // 复合索引

// 查询投影
const users = await User.find().select('name email');  // 只返回部分字段

// 分页
const page = 1;
const limit = 20;
const users = await User.find()
    .skip((page - 1) * limit)
    .limit(limit);
```

## 性能监控

### 内置性能API

```javascript
const { performance } = require('perf_hooks');

const start = performance.now();
await someOperation();
const end = performance.now();
console.log(`耗时: ${end - start}ms`);

// 性能标记
performance.mark('start-fetch');
await fetch('url');
performance.mark('end-fetch');
performance.measure('fetch-duration', 'start-fetch', 'end-fetch');

const measure = performance.getEntriesByName('fetch-duration')[0];
console.log(`Fetch耗时: ${measure.duration}ms`);
```

### APM工具

```javascript
// New Relic
require('newrelic');

// AppDynamics
require('appdynamics');

// Datadog
const tracer = require('dd-trace').init();

// 自定义追踪
const span = tracer.startSpan('operation');
await operation();
span.finish();
```

## 最佳实践

### 异步错误处理

```javascript
// ✓ 统一错误处理
process.on('unhandledRejection', (reason, promise) => {
    console.error('未处理的Promise拒绝:', reason);
    // 记录日志、发送告警
});

process.on('uncaughtException', (err) => {
    console.error('未捕获的异常:', err);
    process.exit(1);  // 退出进程
});

// ✓ 优雅关闭
process.on('SIGTERM', async () => {
    console.log('收到SIGTERM信号');
    
    server.close(() => {
        console.log('HTTP服务器关闭');
    });
    
    await mongoose.connection.close();
    console.log('数据库连接关闭');
    
    process.exit(0);
});
```

### 连接池

```javascript
// MongoDB连接池
mongoose.connect('mongodb://localhost/myapp', {
    maxPoolSize: 10,  // 最大连接数
    minPoolSize: 2,   // 最小连接数
    serverSelectionTimeoutMS: 5000
});

// MySQL连接池
const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'myapp',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});
```

### 限流

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,  // 15分钟
    max: 100,  // 最多100个请求
    message: '请求过于频繁，请稍后再试'
});

app.use('/api/', limiter);

// 按IP限流
const ipLimiter = rateLimit({
    windowMs: 60 * 1000,
    max: 5,
    standardHeaders: true,
    legacyHeaders: false
});

app.post('/api/login', ipLimiter, loginHandler);
```

**核心：** WebSocket实现双向实时通信。性能优化关注事件循环、内存泄漏、数据库查询、缓存策略和集群部署。

