# 03-异步编程与数据库

Node.js异步编程是核心特性，从回调到Promise再到async/await，不断演进。

## 异步编程演进

### 回调函数

```javascript
// 回调地狱
fs.readFile('file1.txt', 'utf8', (err, data1) => {
    if (err) return console.error(err);
    
    fs.readFile('file2.txt', 'utf8', (err, data2) => {
        if (err) return console.error(err);
        
        fs.readFile('file3.txt', 'utf8', (err, data3) => {
            if (err) return console.error(err);
            
            console.log(data1, data2, data3);
        });
    });
});
```

### Promise

```javascript
const fs = require('fs').promises;

// Promise链
fs.readFile('file1.txt', 'utf8')
    .then(data1 => {
        console.log(data1);
        return fs.readFile('file2.txt', 'utf8');
    })
    .then(data2 => {
        console.log(data2);
        return fs.readFile('file3.txt', 'utf8');
    })
    .then(data3 => {
        console.log(data3);
    })
    .catch(err => {
        console.error(err);
    });

// Promise.all（并行）
Promise.all([
    fs.readFile('file1.txt', 'utf8'),
    fs.readFile('file2.txt', 'utf8'),
    fs.readFile('file3.txt', 'utf8')
])
.then(([data1, data2, data3]) => {
    console.log(data1, data2, data3);
})
.catch(err => console.error(err));

// Promise.race（第一个完成）
Promise.race([
    fetch('url1'),
    fetch('url2')
])
.then(result => console.log(result));

// Promise.allSettled（等待全部，不管成功失败）
Promise.allSettled([
    promise1,
    promise2,
    promise3
])
.then(results => {
    results.forEach(result => {
        if (result.status === 'fulfilled') {
            console.log('成功:', result.value);
        } else {
            console.log('失败:', result.reason);
        }
    });
});
```

### async/await

```javascript
const fs = require('fs').promises;

// async函数
async function readFiles() {
    try {
        const data1 = await fs.readFile('file1.txt', 'utf8');
        const data2 = await fs.readFile('file2.txt', 'utf8');
        const data3 = await fs.readFile('file3.txt', 'utf8');
        console.log(data1, data2, data3);
    } catch (err) {
        console.error(err);
    }
}

// 并行await
async function readFilesParallel() {
    try {
        const [data1, data2, data3] = await Promise.all([
            fs.readFile('file1.txt', 'utf8'),
            fs.readFile('file2.txt', 'utf8'),
            fs.readFile('file3.txt', 'utf8')
        ]);
        console.log(data1, data2, data3);
    } catch (err) {
        console.error(err);
    }
}

// Express中使用
app.get('/users', async (req, res, next) => {
    try {
        const users = await User.find();
        res.json(users);
    } catch (err) {
        next(err);
    }
});

// 顶层await（ES2022，Node.js 14.8+）
const data = await fs.readFile('config.json', 'utf8');
```

## 事件循环

### 事件循环阶段

```
   ┌───────────────────────────┐
┌─>│           timers          │ // setTimeout、setInterval
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks     │ // 系统操作回调
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare       │ // 内部使用
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           poll            │ // I/O回调
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           check           │ // setImmediate
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
└──┤      close callbacks      │ // socket.on('close')
   └───────────────────────────┘
```

### 微任务和宏任务

```javascript
console.log('1');

setTimeout(() => console.log('2'), 0);  // 宏任务

Promise.resolve().then(() => console.log('3'));  // 微任务

process.nextTick(() => console.log('4'));  // 微任务（优先）

console.log('5');

// 输出：1 5 4 3 2
// 执行顺序：同步 → process.nextTick → Promise → setTimeout
```

### setImmediate vs setTimeout

```javascript
// setImmediate：check阶段执行
setImmediate(() => {
    console.log('immediate');
});

// setTimeout：timers阶段执行
setTimeout(() => {
    console.log('timeout');
}, 0);

// I/O回调中：setImmediate总是先执行
fs.readFile('file.txt', () => {
    setImmediate(() => console.log('immediate'));  // 先
    setTimeout(() => console.log('timeout'), 0);    // 后
});
```

## MongoDB

### Mongoose

```bash
npm install mongoose
```

```javascript
const mongoose = require('mongoose');

// 连接数据库
mongoose.connect('mongodb://localhost:27017/myapp', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

const db = mongoose.connection;
db.on('error', console.error);
db.once('open', () => console.log('MongoDB connected'));

// 定义Schema
const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        trim: true
    },
    email: {
        type: String,
        required: true,
        unique: true,
        lowercase: true
    },
    age: {
        type: Number,
        min: 0,
        max: 150
    },
    createdAt: {
        type: Date,
        default: Date.now
    }
});

// 添加方法
userSchema.methods.greet = function() {
    return `Hello, ${this.name}!`;
};

// 静态方法
userSchema.statics.findByEmail = function(email) {
    return this.findOne({ email });
};

// 创建Model
const User = mongoose.model('User', userSchema);

// CRUD操作
// 创建
const user = new User({ name: 'Alice', email: 'alice@example.com', age: 25 });
await user.save();

// 或
const user = await User.create({ name: 'Alice', email: 'alice@example.com' });

// 查询
const users = await User.find();
const user = await User.findById(id);
const user = await User.findOne({ email: 'alice@example.com' });
const users = await User.find({ age: { $gte: 18 } });

// 更新
await User.updateOne({ _id: id }, { name: 'Alice2' });
await User.findByIdAndUpdate(id, { name: 'Alice2' }, { new: true });

// 删除
await User.deleteOne({ _id: id });
await User.findByIdAndDelete(id);

// 查询链
const users = await User
    .find({ age: { $gte: 18 } })
    .sort({ createdAt: -1 })
    .limit(10)
    .select('name email');
```

## MySQL

### mysql2

```bash
npm install mysql2
```

```javascript
const mysql = require('mysql2/promise');

// 创建连接池
const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'myapp',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// 查询
const [rows] = await pool.query('SELECT * FROM users WHERE age > ?', [18]);

// 插入
const [result] = await pool.query(
    'INSERT INTO users (name, email) VALUES (?, ?)',
    ['Alice', 'alice@example.com']
);
console.log(result.insertId);

// 更新
await pool.query('UPDATE users SET name = ? WHERE id = ?', ['Alice2', 1]);

// 删除
await pool.query('DELETE FROM users WHERE id = ?', [1]);

// 事务
const connection = await pool.getConnection();
await connection.beginTransaction();

try {
    await connection.query('INSERT INTO users ...');
    await connection.query('UPDATE accounts ...');
    await connection.commit();
} catch (err) {
    await connection.rollback();
    throw err;
} finally {
    connection.release();
}
```

### Sequelize（ORM）

```bash
npm install sequelize mysql2
```

```javascript
const { Sequelize, DataTypes } = require('sequelize');

// 连接
const sequelize = new Sequelize('myapp', 'root', 'password', {
    host: 'localhost',
    dialect: 'mysql',
    logging: false
});

// 定义模型
const User = sequelize.define('User', {
    name: {
        type: DataTypes.STRING,
        allowNull: false
    },
    email: {
        type: DataTypes.STRING,
        unique: true,
        validate: {
            isEmail: true
        }
    },
    age: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    }
});

// 同步模型
await sequelize.sync();

// CRUD
const user = await User.create({ name: 'Alice', email: 'alice@example.com' });

const users = await User.findAll();
const user = await User.findByPk(1);
const user = await User.findOne({ where: { email: 'alice@example.com' } });

await User.update({ name: 'Alice2' }, { where: { id: 1 } });

await User.destroy({ where: { id: 1 } });

// 关联
const Post = sequelize.define('Post', { /* ... */ });

User.hasMany(Post);
Post.belongsTo(User);

// 查询关联
const users = await User.findAll({
    include: Post
});
```

## Redis

### ioredis

```bash
npm install ioredis
```

```javascript
const Redis = require('ioredis');

const redis = new Redis({
    host: 'localhost',
    port: 6379,
    password: 'password',
    db: 0
});

// 字符串
await redis.set('key', 'value');
const value = await redis.get('key');

// 过期时间
await redis.set('key', 'value', 'EX', 60);  // 60秒过期

// 哈希
await redis.hset('user:1', 'name', 'Alice');
await redis.hset('user:1', 'age', 25);
const name = await redis.hget('user:1', 'name');
const user = await redis.hgetall('user:1');

// 列表
await redis.lpush('list', 'item1', 'item2');
const item = await redis.rpop('list');

// 集合
await redis.sadd('set', 'member1', 'member2');
const members = await redis.smembers('set');

// 有序集合
await redis.zadd('leaderboard', 100, 'player1', 200, 'player2');
const top10 = await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES');

// Pipeline（批量操作）
const pipeline = redis.pipeline();
pipeline.set('key1', 'value1');
pipeline.set('key2', 'value2');
pipeline.get('key1');
const results = await pipeline.exec();

// 发布订阅
const subscriber = new Redis();
subscriber.subscribe('channel');
subscriber.on('message', (channel, message) => {
    console.log(`${channel}: ${message}`);
});

const publisher = new Redis();
publisher.publish('channel', 'Hello');
```

## 缓存策略

### 缓存模式

```javascript
// 查询缓存
async function getUserById(id) {
    const cacheKey = `user:${id}`;
    
    // 1. 查缓存
    const cached = await redis.get(cacheKey);
    if (cached) {
        return JSON.parse(cached);
    }
    
    // 2. 查数据库
    const user = await User.findById(id);
    
    // 3. 写缓存
    if (user) {
        await redis.set(cacheKey, JSON.stringify(user), 'EX', 3600);
    }
    
    return user;
}

// 缓存失效
async function updateUser(id, data) {
    const user = await User.findByIdAndUpdate(id, data, { new: true });
    
    // 删除缓存
    await redis.del(`user:${id}`);
    
    return user;
}

// 缓存预热
async function warmUpCache() {
    const users = await User.find().limit(100);
    const pipeline = redis.pipeline();
    
    users.forEach(user => {
        pipeline.set(
            `user:${user.id}`,
            JSON.stringify(user),
            'EX',
            3600
        );
    });
    
    await pipeline.exec();
}
```

## 异步并发控制

### 并发限制

```javascript
// ❌ 问题：同时发起1000个请求
const promises = urls.map(url => fetch(url));
const results = await Promise.all(promises);  // 可能压垮服务器

// ✅ 解决：限制并发数
async function promiseLimit(tasks, limit) {
    const results = [];
    const executing = [];
    
    for (const task of tasks) {
        const p = Promise.resolve().then(() => task());
        results.push(p);
        
        if (limit <= tasks.length) {
            const e = p.then(() => executing.splice(executing.indexOf(e), 1));
            executing.push(e);
            if (executing.length >= limit) {
                await Promise.race(executing);
            }
        }
    }
    
    return Promise.all(results);
}

// 使用
const tasks = urls.map(url => () => fetch(url));
const results = await promiseLimit(tasks, 5);  // 最多5个并发

// 或使用p-limit库
const pLimit = require('p-limit');
const limit = pLimit(5);

const promises = urls.map(url => limit(() => fetch(url)));
await Promise.all(promises);
```

### 错误处理

```javascript
// try-catch
async function getData() {
    try {
        const data = await fetchData();
        return data;
    } catch (err) {
        console.error('获取数据失败:', err);
        throw err;  // 重新抛出
    }
}

// Promise.catch
fetchData()
    .then(data => processData(data))
    .catch(err => console.error(err))
    .finally(() => console.log('完成'));

// 批量错误处理
const results = await Promise.allSettled(promises);
results.forEach((result, index) => {
    if (result.status === 'rejected') {
        console.error(`Task ${index} failed:`, result.reason);
    }
});
```

## Stream流

### 可读流

```javascript
const fs = require('fs');

// 创建可读流
const readStream = fs.createReadStream('large-file.txt', {
    encoding: 'utf8',
    highWaterMark: 64 * 1024  // 缓冲区大小64KB
});

readStream.on('data', (chunk) => {
    console.log('读取:', chunk.length, '字节');
});

readStream.on('end', () => {
    console.log('读取完成');
});

readStream.on('error', (err) => {
    console.error('错误:', err);
});

// 暂停和恢复
readStream.pause();
readStream.resume();
```

### 可写流

```javascript
const writeStream = fs.createWriteStream('output.txt');

writeStream.write('第一行\n');
writeStream.write('第二行\n');
writeStream.end('最后一行\n');

writeStream.on('finish', () => {
    console.log('写入完成');
});

writeStream.on('error', (err) => {
    console.error('错误:', err);
});
```

### 管道

```javascript
const fs = require('fs');

// 复制文件
const readStream = fs.createReadStream('source.txt');
const writeStream = fs.createWriteStream('dest.txt');

readStream.pipe(writeStream);

// 链式管道
const zlib = require('zlib');

fs.createReadStream('input.txt')
    .pipe(zlib.createGzip())
    .pipe(fs.createWriteStream('input.txt.gz'));

// HTTP响应流
app.get('/download', (req, res) => {
    const fileStream = fs.createReadStream('large-file.pdf');
    fileStream.pipe(res);
});
```

### Transform流

```javascript
const { Transform } = require('stream');

// 自定义转换流
const upperCaseTransform = new Transform({
    transform(chunk, encoding, callback) {
        this.push(chunk.toString().toUpperCase());
        callback();
    }
});

fs.createReadStream('input.txt')
    .pipe(upperCaseTransform)
    .pipe(fs.createWriteStream('output.txt'));
```

## 性能优化

### 异步并行

```javascript
// ❌ 串行（慢）
const user = await User.findById(id);
const posts = await Post.find({ userId: id });
const comments = await Comment.find({ userId: id });

// ✅ 并行（快）
const [user, posts, comments] = await Promise.all([
    User.findById(id),
    Post.find({ userId: id }),
    Comment.find({ userId: id })
]);
```

### 数据库批量操作

```javascript
// ❌ 逐条插入
for (const item of items) {
    await Model.create(item);  // N次数据库调用
}

// ✅ 批量插入
await Model.insertMany(items);  // 1次数据库调用
```

### 缓存优化

```javascript
// 缓存中间件
const cacheMiddleware = (duration) => {
    return async (req, res, next) => {
        const key = `cache:${req.url}`;
        const cached = await redis.get(key);
        
        if (cached) {
            return res.json(JSON.parse(cached));
        }
        
        res.originalJson = res.json;
        res.json = function(data) {
            redis.set(key, JSON.stringify(data), 'EX', duration);
            res.originalJson(data);
        };
        
        next();
    };
};

// 使用
app.get('/api/data', cacheMiddleware(60), async (req, res) => {
    const data = await fetchData();
    res.json(data);
});
```

**核心：** Node.js异步I/O通过事件循环实现高并发。Promise/async/await简化异步编程，数据库操作需合理使用缓存和批量操作。

