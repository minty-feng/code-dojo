# 02-Express框架

Express是Node.js最流行的Web框架，简洁灵活，中间件机制强大。

## 基础使用

### 安装和启动

```bash
npm install express
```

```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello Express!');
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

### 路由

```javascript
// GET请求
app.get('/users', (req, res) => {
    res.json({ users: [] });
});

// POST请求
app.post('/users', (req, res) => {
    res.status(201).json({ message: 'Created' });
});

// PUT请求
app.put('/users/:id', (req, res) => {
    const { id } = req.params;
    res.json({ message: `Updated user ${id}` });
});

// DELETE请求
app.delete('/users/:id', (req, res) => {
    res.status(204).send();
});

// 路由参数
app.get('/users/:id', (req, res) => {
    const { id } = req.params;
    res.json({ id });
});

// 多个参数
app.get('/users/:userId/posts/:postId', (req, res) => {
    const { userId, postId } = req.params;
    res.json({ userId, postId });
});

// 查询参数
app.get('/search', (req, res) => {
    const { q, page = 1, limit = 10 } = req.query;
    res.json({ q, page, limit });
    // /search?q=keyword&page=2&limit=20
});

// 正则路由
app.get(/.*fly$/, (req, res) => {
    res.send('ends with fly');
});
```

### Router模块化

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.json({ users: [] });
});

router.post('/', (req, res) => {
    res.status(201).json({ message: 'Created' });
});

router.get('/:id', (req, res) => {
    res.json({ id: req.params.id });
});

module.exports = router;

// app.js
const usersRouter = require('./routes/users');
app.use('/api/users', usersRouter);
// GET /api/users → router.get('/')
// GET /api/users/123 → router.get('/:id')
```

## 中间件

### 内置中间件

```javascript
// 解析JSON请求体
app.use(express.json());

// 解析URL编码数据
app.use(express.urlencoded({ extended: true }));

// 静态文件
app.use(express.static('public'));
app.use('/static', express.static('public'));
```

### 自定义中间件

```javascript
// 日志中间件
const logger = (req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();  // 调用下一个中间件
};

app.use(logger);

// 认证中间件
const authMiddleware = (req, res, next) => {
    const token = req.headers.authorization;
    
    if (!token) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    
    // 验证token
    try {
        const user = verifyToken(token);
        req.user = user;  // 添加到req对象
        next();
    } catch (err) {
        res.status(401).json({ error: 'Invalid token' });
    }
};

// 应用到特定路由
app.get('/protected', authMiddleware, (req, res) => {
    res.json({ user: req.user });
});

// 错误处理中间件（4个参数）
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});
```

### 第三方中间件

```javascript
// morgan：日志
const morgan = require('morgan');
app.use(morgan('combined'));

// cors：跨域
const cors = require('cors');
app.use(cors());

// helmet：安全头
const helmet = require('helmet');
app.use(helmet());

// compression：压缩
const compression = require('compression');
app.use(compression());

// express-validator：验证
const { body, validationResult } = require('express-validator');

app.post('/users',
    body('email').isEmail(),
    body('password').isLength({ min: 6 }),
    (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        // 处理请求
    }
);
```

## 请求和响应

### Request对象

```javascript
app.get('/api/data', (req, res) => {
    // 查询参数
    const { page, limit } = req.query;
    
    // 路由参数
    const { id } = req.params;
    
    // 请求体
    const { name, email } = req.body;
    
    // 请求头
    const token = req.get('Authorization');
    const userAgent = req.get('User-Agent');
    
    // 其他属性
    console.log(req.method);      // GET
    console.log(req.url);         // /api/data?page=1
    console.log(req.path);        // /api/data
    console.log(req.hostname);    // example.com
    console.log(req.ip);          // 客户端IP
    console.log(req.protocol);    // http/https
});
```

### Response对象

```javascript
app.get('/api/data', (req, res) => {
    // 发送文本
    res.send('Hello');
    
    // 发送JSON
    res.json({ message: 'Success' });
    
    // 设置状态码
    res.status(404).send('Not Found');
    res.status(201).json({ message: 'Created' });
    
    // 设置响应头
    res.set('Content-Type', 'application/json');
    res.set({
        'Content-Type': 'text/html',
        'X-Custom-Header': 'value'
    });
    
    // 重定向
    res.redirect('/new-url');
    res.redirect(301, '/permanent-redirect');
    
    // 发送文件
    res.sendFile('/path/to/file.pdf');
    
    // 下载文件
    res.download('/path/to/file.pdf', 'filename.pdf');
    
    // 渲染模板
    res.render('index', { title: 'Home' });
});
```

## 模板引擎

### EJS

```bash
npm install ejs
```

```javascript
// 设置模板引擎
app.set('view engine', 'ejs');
app.set('views', './views');

// 渲染
app.get('/', (req, res) => {
    res.render('index', {
        title: 'Home',
        users: ['Alice', 'Bob']
    });
});
```

```html
<!-- views/index.ejs -->
<!DOCTYPE html>
<html>
<head>
    <title><%= title %></title>
</head>
<body>
    <h1><%= title %></h1>
    <ul>
        <% users.forEach(user => { %>
            <li><%= user %></li>
        <% }); %>
    </ul>
</body>
</html>
```

### Pug（原Jade）

```bash
npm install pug
```

```javascript
app.set('view engine', 'pug');
```

```pug
//- views/index.pug
doctype html
html
  head
    title= title
  body
    h1= title
    ul
      each user in users
        li= user
```

## RESTful API示例

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// 模拟数据库
let users = [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' }
];

// GET /api/users
app.get('/api/users', (req, res) => {
    res.json(users);
});

// GET /api/users/:id
app.get('/api/users/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
});

// POST /api/users
app.post('/api/users', (req, res) => {
    const { name, email } = req.body;
    const newUser = {
        id: users.length + 1,
        name,
        email
    };
    users.push(newUser);
    res.status(201).json(newUser);
});

// PUT /api/users/:id
app.put('/api/users/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }
    
    const { name, email } = req.body;
    user.name = name || user.name;
    user.email = email || user.email;
    
    res.json(user);
});

// DELETE /api/users/:id
app.delete('/api/users/:id', (req, res) => {
    const index = users.findIndex(u => u.id === parseInt(req.params.id));
    if (index === -1) {
        return res.status(404).json({ error: 'User not found' });
    }
    
    users.splice(index, 1);
    res.status(204).send();
});

app.listen(3000);
```

## 错误处理

### 同步错误

```javascript
app.get('/sync-error', (req, res) => {
    throw new Error('Sync error');  // 自动捕获
});
```

### 异步错误

```javascript
// ❌ 错误：异步错误未捕获
app.get('/async-error', (req, res) => {
    setTimeout(() => {
        throw new Error('Async error');  // 不会被捕获
    }, 100);
});

// ✅ 正确：使用next
app.get('/async-error', (req, res, next) => {
    setTimeout(() => {
        next(new Error('Async error'));
    }, 100);
});

// ✅ Promise错误
app.get('/promise-error', (req, res, next) => {
    doAsyncWork()
        .then(result => res.json(result))
        .catch(next);  // 传递给错误处理中间件
});

// ✅ async/await
app.get('/async-await', async (req, res, next) => {
    try {
        const result = await doAsyncWork();
        res.json(result);
    } catch (err) {
        next(err);
    }
});

// 或使用包装器
const asyncHandler = fn => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/users', asyncHandler(async (req, res) => {
    const users = await User.find();
    res.json(users);
}));
```

### 错误处理中间件

```javascript
// 404处理
app.use((req, res, next) => {
    res.status(404).json({ error: 'Not Found' });
});

// 错误处理（放在所有路由后）
app.use((err, req, res, next) => {
    console.error(err.stack);
    
    // 根据环境返回错误详情
    const errorResponse = {
        error: err.message
    };
    
    if (process.env.NODE_ENV === 'development') {
        errorResponse.stack = err.stack;
    }
    
    res.status(err.status || 500).json(errorResponse);
});
```

## 最佳实践

### 项目结构

```
src/
├── app.js              # Express应用配置
├── server.js           # 服务器启动
├── routes/             # 路由
│   ├── index.js
│   ├── users.js
│   └── posts.js
├── controllers/        # 控制器
│   ├── userController.js
│   └── postController.js
├── models/             # 数据模型
│   ├── User.js
│   └── Post.js
├── middlewares/        # 中间件
│   ├── auth.js
│   ├── validator.js
│   └── errorHandler.js
├── services/           # 业务逻辑
│   └── userService.js
├── utils/              # 工具函数
│   └── logger.js
└── config/             # 配置
    └── database.js
```

### 环境配置

```javascript
// config/config.js
module.exports = {
    development: {
        port: 3000,
        db: {
            host: 'localhost',
            port: 27017,
            name: 'myapp_dev'
        }
    },
    production: {
        port: process.env.PORT || 8080,
        db: {
            host: process.env.DB_HOST,
            port: process.env.DB_PORT,
            name: process.env.DB_NAME
        }
    }
};

const env = process.env.NODE_ENV || 'development';
const config = require('./config')[env];
```

### 路由控制器分离

```javascript
// controllers/userController.js
exports.getUsers = async (req, res, next) => {
    try {
        const users = await User.find();
        res.json(users);
    } catch (err) {
        next(err);
    }
};

exports.createUser = async (req, res, next) => {
    try {
        const user = await User.create(req.body);
        res.status(201).json(user);
    } catch (err) {
        next(err);
    }
};

// routes/users.js
const router = require('express').Router();
const controller = require('../controllers/userController');

router.get('/', controller.getUsers);
router.post('/', controller.createUser);

module.exports = router;
```

**核心：** Express通过中间件机制构建灵活Web应用，路由清晰，扩展性强。

