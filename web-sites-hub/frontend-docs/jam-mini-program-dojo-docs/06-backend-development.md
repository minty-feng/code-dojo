# 后端开发与集成

## 💡 核心结论

1. **小程序后端需要处理用户登录、数据存储、业务逻辑等**
2. **RESTful API设计要遵循REST规范，返回统一格式**
3. **JWT Token是常用的身份认证方案**
4. **数据库设计要考虑性能、扩展性和数据一致性**
5. **安全措施包括HTTPS、参数校验、SQL注入防护等**

---

## 1. 后端架构设计

### 1.1 技术选型

**Node.js + Express**：
```javascript
// 适合快速开发，生态丰富
const express = require('express')
const app = express()

app.use(express.json())
app.listen(3000)
```

**Node.js + Koa**：
```javascript
// 更轻量，支持async/await
const Koa = require('koa')
const app = new Koa()

app.use(async (ctx) => {
  ctx.body = 'Hello World'
})

app.listen(3000)
```

**Python + Flask**：
```python
# 简洁易用
from flask import Flask

app = Flask(__name__)

@app.route('/api/products')
def get_products():
    return {'list': []}
```

**Go + Gin**：
```go
// 高性能，适合高并发
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()
    r.GET("/api/products", getProducts)
    r.Run(":3000")
}
```

### 1.2 项目结构

```
backend/
├── src/
│   ├── controllers/     # 控制器
│   │   ├── user.js
│   │   └── product.js
│   ├── models/          # 数据模型
│   │   ├── user.js
│   │   └── product.js
│   ├── services/        # 业务逻辑
│   │   ├── auth.js
│   │   └── order.js
│   ├── middleware/      # 中间件
│   │   ├── auth.js
│   │   └── error.js
│   ├── utils/           # 工具函数
│   │   ├── response.js
│   │   └── validator.js
│   ├── routes/          # 路由
│   │   ├── index.js
│   │   └── api.js
│   └── app.js           # 入口文件
├── config/              # 配置文件
│   └── database.js
├── tests/               # 测试
└── package.json
```

---

## 2. 用户登录与认证

### 2.1 微信登录流程

```javascript
// controllers/auth.js
const axios = require('axios')
const jwt = require('jsonwebtoken')
const User = require('../models/user')

class AuthController {
  // 微信登录
  async wechatLogin(req, res) {
    const { code } = req.body
    
    if (!code) {
      return res.json({
        code: 400,
        message: 'code不能为空'
      })
    }
    
    try {
      // 1. 用code换取openid和session_key
      const wechatRes = await axios.get('https://api.weixin.qq.com/sns/jscode2session', {
        params: {
          appid: process.env.WECHAT_APPID,
          secret: process.env.WECHAT_SECRET,
          js_code: code,
          grant_type: 'authorization_code'
        }
      })
      
      const { openid, session_key, errcode, errmsg } = wechatRes.data
      
      if (errcode) {
        return res.json({
          code: 400,
          message: errmsg || '登录失败'
        })
      }
      
      // 2. 查询或创建用户
      let user = await User.findOne({ openid })
      
      if (!user) {
        user = await User.create({
          openid,
          sessionKey: session_key,
          createdAt: new Date()
        })
      } else {
        // 更新session_key
        user.sessionKey = session_key
        await user.save()
      }
      
      // 3. 生成JWT token
      const token = jwt.sign(
        { userId: user._id, openid },
        process.env.JWT_SECRET,
        { expiresIn: '7d' }
      )
      
      res.json({
        code: 0,
        data: {
          token,
          userId: user._id,
          userInfo: {
            nickname: user.nickname,
            avatar: user.avatar
          }
        }
      })
    } catch (error) {
      console.error('登录失败', error)
      res.json({
        code: 500,
        message: '登录失败，请重试'
      })
    }
  }
  
  // 获取用户信息
  async getUserInfo(req, res) {
    const { userId } = req.user
    
    try {
      const user = await User.findById(userId)
      
      if (!user) {
        return res.json({
          code: 404,
          message: '用户不存在'
        })
      }
      
      res.json({
        code: 0,
        data: {
          id: user._id,
          nickname: user.nickname,
          avatar: user.avatar,
          phone: user.phone
        }
      })
    } catch (error) {
      res.json({
        code: 500,
        message: '获取用户信息失败'
      })
    }
  }
  
  // 更新用户信息
  async updateUserInfo(req, res) {
    const { userId } = req.user
    const { nickname, avatar, phone } = req.body
    
    try {
      const user = await User.findById(userId)
      
      if (nickname) user.nickname = nickname
      if (avatar) user.avatar = avatar
      if (phone) user.phone = phone
      
      await user.save()
      
      res.json({
        code: 0,
        message: '更新成功'
      })
    } catch (error) {
      res.json({
        code: 500,
        message: '更新失败'
      })
    }
  }
}

module.exports = new AuthController()
```

### 2.2 JWT认证中间件

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken')
const User = require('../models/user')

async function authMiddleware(req, res, next) {
  try {
    // 从header获取token
    const token = req.headers.authorization?.replace('Bearer ', '')
    
    if (!token) {
      return res.json({
        code: 401,
        message: '未登录'
      })
    }
    
    // 验证token
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    
    // 查询用户
    const user = await User.findById(decoded.userId)
    
    if (!user) {
      return res.json({
        code: 401,
        message: '用户不存在'
      })
    }
    
    // 将用户信息挂载到request
    req.user = {
      userId: user._id,
      openid: user.openid
    }
    
    next()
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.json({
        code: 401,
        message: 'Token已过期'
      })
    }
    
    res.json({
      code: 401,
      message: 'Token无效'
    })
  }
}

module.exports = authMiddleware
```

### 2.3 路由配置

```javascript
// routes/api.js
const express = require('express')
const router = express.Router()
const authMiddleware = require('../middleware/auth')
const authController = require('../controllers/auth')

// 登录（不需要认证）
router.post('/auth/login', authController.wechatLogin)

// 需要认证的路由
router.get('/auth/user', authMiddleware, authController.getUserInfo)
router.put('/auth/user', authMiddleware, authController.updateUserInfo)

module.exports = router
```

---

## 3. API设计

### 3.1 RESTful规范

```javascript
// GET    /api/products          # 获取商品列表
// GET    /api/products/:id      # 获取商品详情
// POST   /api/products          # 创建商品
// PUT    /api/products/:id      # 更新商品
// DELETE /api/products/:id     # 删除商品
```

### 3.2 统一响应格式

```javascript
// utils/response.js
class Response {
  static success(data, message = '成功') {
    return {
      code: 0,
      message,
      data
    }
  }
  
  static error(code = 500, message = '失败', data = null) {
    return {
      code,
      message,
      data
    }
  }
  
  static pagination(list, total, page, size) {
    return {
      code: 0,
      message: '成功',
      data: {
        list,
        pagination: {
          total,
          page,
          size,
          totalPages: Math.ceil(total / size)
        }
      }
    }
  }
}

module.exports = Response
```

### 3.3 商品API示例

```javascript
// controllers/product.js
const Product = require('../models/product')
const Response = require('../utils/response')

class ProductController {
  // 获取商品列表
  async getList(req, res) {
    try {
      const { page = 1, size = 10, category, keyword } = req.query
      
      const query = {}
      if (category) query.category = category
      if (keyword) {
        query.$or = [
          { name: new RegExp(keyword, 'i') },
          { description: new RegExp(keyword, 'i') }
        ]
      }
      
      const skip = (page - 1) * size
      
      const [list, total] = await Promise.all([
        Product.find(query)
          .skip(skip)
          .limit(parseInt(size))
          .sort({ createdAt: -1 }),
        Product.countDocuments(query)
      ])
      
      res.json(Response.pagination(list, total, parseInt(page), parseInt(size)))
    } catch (error) {
      res.json(Response.error(500, '获取商品列表失败'))
    }
  }
  
  // 获取商品详情
  async getDetail(req, res) {
    try {
      const { id } = req.params
      
      const product = await Product.findById(id)
      
      if (!product) {
        return res.json(Response.error(404, '商品不存在'))
      }
      
      res.json(Response.success(product))
    } catch (error) {
      res.json(Response.error(500, '获取商品详情失败'))
    }
  }
  
  // 创建商品
  async create(req, res) {
    try {
      const product = await Product.create(req.body)
      res.json(Response.success(product, '创建成功'))
    } catch (error) {
      res.json(Response.error(500, '创建失败'))
    }
  }
  
  // 更新商品
  async update(req, res) {
    try {
      const { id } = req.params
      
      const product = await Product.findByIdAndUpdate(
        id,
        req.body,
        { new: true }
      )
      
      if (!product) {
        return res.json(Response.error(404, '商品不存在'))
      }
      
      res.json(Response.success(product, '更新成功'))
    } catch (error) {
      res.json(Response.error(500, '更新失败'))
    }
  }
  
  // 删除商品
  async delete(req, res) {
    try {
      const { id } = req.params
      
      const product = await Product.findByIdAndDelete(id)
      
      if (!product) {
        return res.json(Response.error(404, '商品不存在'))
      }
      
      res.json(Response.success(null, '删除成功'))
    } catch (error) {
      res.json(Response.error(500, '删除失败'))
    }
  }
}

module.exports = new ProductController()
```

---

## 4. 数据库设计

### 4.1 MongoDB模型设计

```javascript
// models/user.js
const mongoose = require('mongoose')

const userSchema = new mongoose.Schema({
  openid: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  sessionKey: {
    type: String
  },
  nickname: {
    type: String
  },
  avatar: {
    type: String
  },
  phone: {
    type: String
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
})

userSchema.pre('save', function(next) {
  this.updatedAt = Date.now()
  next()
})

module.exports = mongoose.model('User', userSchema)
```

```javascript
// models/product.js
const mongoose = require('mongoose')

const productSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    index: true
  },
  description: {
    type: String
  },
  price: {
    type: Number,
    required: true
  },
  originalPrice: {
    type: Number
  },
  images: [{
    type: String
  }],
  category: {
    type: String,
    index: true
  },
  stock: {
    type: Number,
    default: 0
  },
  sales: {
    type: Number,
    default: 0
  },
  status: {
    type: String,
    enum: ['on_sale', 'off_sale', 'deleted'],
    default: 'on_sale'
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
})

// 索引
productSchema.index({ name: 'text', description: 'text' })
productSchema.index({ category: 1, createdAt: -1 })

module.exports = mongoose.model('Product', productSchema)
```

```javascript
// models/order.js
const mongoose = require('mongoose')

const orderSchema = new mongoose.Schema({
  orderNo: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  items: [{
    productId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Product',
      required: true
    },
    name: String,
    price: Number,
    quantity: Number,
    image: String
  }],
  totalAmount: {
    type: Number,
    required: true
  },
  status: {
    type: String,
    enum: ['pending', 'paid', 'shipped', 'completed', 'cancelled'],
    default: 'pending',
    index: true
  },
  address: {
    name: String,
    phone: String,
    province: String,
    city: String,
    district: String,
    detail: String
  },
  createdAt: {
    type: Date,
    default: Date.now,
    index: true
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
})

module.exports = mongoose.model('Order', orderSchema)
```

### 4.2 数据库连接

```javascript
// config/database.js
const mongoose = require('mongoose')

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    })
    
    console.log('MongoDB连接成功')
  } catch (error) {
    console.error('MongoDB连接失败', error)
    process.exit(1)
  }
}

module.exports = connectDB
```

---

## 5. 业务逻辑

### 5.1 订单服务

```javascript
// services/order.js
const Order = require('../models/order')
const Product = require('../models/product')
const Response = require('../utils/response')

class OrderService {
  // 创建订单
  async createOrder(userId, items, address) {
    // 1. 验证商品库存
    for (const item of items) {
      const product = await Product.findById(item.productId)
      
      if (!product || product.stock < item.quantity) {
        throw new Error(`商品${product?.name || item.productId}库存不足`)
      }
    }
    
    // 2. 计算总价
    let totalAmount = 0
    const orderItems = []
    
    for (const item of items) {
      const product = await Product.findById(item.productId)
      const itemTotal = product.price * item.quantity
      totalAmount += itemTotal
      
      orderItems.push({
        productId: product._id,
        name: product.name,
        price: product.price,
        quantity: item.quantity,
        image: product.images[0]
      })
    }
    
    // 3. 生成订单号
    const orderNo = this.generateOrderNo()
    
    // 4. 创建订单
    const order = await Order.create({
      orderNo,
      userId,
      items: orderItems,
      totalAmount,
      address
    })
    
    // 5. 扣减库存
    for (const item of items) {
      await Product.findByIdAndUpdate(
        item.productId,
        { $inc: { stock: -item.quantity } }
      )
    }
    
    return order
  }
  
  // 生成订单号
  generateOrderNo() {
    const timestamp = Date.now()
    const random = Math.floor(Math.random() * 10000)
    return `ORDER${timestamp}${random}`
  }
  
  // 支付订单
  async payOrder(orderId) {
    const order = await Order.findById(orderId)
    
    if (!order) {
      throw new Error('订单不存在')
    }
    
    if (order.status !== 'pending') {
      throw new Error('订单状态不正确')
    }
    
    // 更新订单状态
    order.status = 'paid'
    await order.save()
    
    // 增加商品销量
    for (const item of order.items) {
      await Product.findByIdAndUpdate(
        item.productId,
        { $inc: { sales: item.quantity } }
      )
    }
    
    return order
  }
  
  // 取消订单
  async cancelOrder(orderId) {
    const order = await Order.findById(orderId)
    
    if (!order) {
      throw new Error('订单不存在')
    }
    
    if (order.status === 'completed' || order.status === 'shipped') {
      throw new Error('订单无法取消')
    }
    
    // 恢复库存
    if (order.status === 'paid') {
      for (const item of order.items) {
        await Product.findByIdAndUpdate(
          item.productId,
          { $inc: { stock: item.quantity } }
        )
      }
    }
    
    order.status = 'cancelled'
    await order.save()
    
    return order
  }
}

module.exports = new OrderService()
```

---

## 6. 安全措施

### 6.1 参数校验

```javascript
// utils/validator.js
class Validator {
  static validateRequired(value, field) {
    if (!value || (typeof value === 'string' && value.trim() === '')) {
      throw new Error(`${field}不能为空`)
    }
  }
  
  static validateNumber(value, field, min, max) {
    const num = Number(value)
    if (isNaN(num)) {
      throw new Error(`${field}必须是数字`)
    }
    if (min !== undefined && num < min) {
      throw new Error(`${field}不能小于${min}`)
    }
    if (max !== undefined && num > max) {
      throw new Error(`${field}不能大于${max}`)
    }
    return num
  }
  
  static validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!regex.test(email)) {
      throw new Error('邮箱格式不正确')
    }
  }
  
  static validatePhone(phone) {
    const regex = /^1[3-9]\d{9}$/
    if (!regex.test(phone)) {
      throw new Error('手机号格式不正确')
    }
  }
}

module.exports = Validator
```

```javascript
// middleware/validator.js
const Validator = require('../utils/validator')

function validate(schema) {
  return (req, res, next) => {
    try {
      for (const [field, rules] of Object.entries(schema)) {
        const value = req.body[field] || req.query[field]
        
        if (rules.required) {
          Validator.validateRequired(value, field)
        }
        
        if (rules.type === 'number') {
          req.body[field] = Validator.validateNumber(
            value,
            field,
            rules.min,
            rules.max
          )
        }
        
        if (rules.type === 'email') {
          Validator.validateEmail(value)
        }
        
        if (rules.type === 'phone') {
          Validator.validatePhone(value)
        }
      }
      
      next()
    } catch (error) {
      res.json({
        code: 400,
        message: error.message
      })
    }
  }
}

module.exports = validate
```

### 6.2 SQL注入防护

```javascript
// 使用参数化查询（MongoDB天然防护）
// ❌ 错误：字符串拼接
const query = `SELECT * FROM users WHERE name = '${name}'`

// ✅ 正确：参数化查询
const user = await User.findOne({ name: name })

// 对于MySQL，使用参数化查询
const query = 'SELECT * FROM users WHERE name = ?'
db.query(query, [name])
```

### 6.3 XSS防护

```javascript
// 使用xss库过滤用户输入
const xss = require('xss')

function sanitizeInput(input) {
  return xss(input, {
    whiteList: {}, // 不允许任何HTML标签
    stripIgnoreTag: true
  })
}

// 使用
const safeContent = sanitizeInput(req.body.content)
```

### 6.4 限流

```javascript
// middleware/rateLimit.js
const rateLimit = require('express-rate-limit')

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100, // 最多100次请求
  message: {
    code: 429,
    message: '请求过于频繁，请稍后再试'
  }
})

module.exports = limiter
```

### 6.5 HTTPS

```javascript
// 生产环境必须使用HTTPS
// 小程序要求所有请求必须使用HTTPS

// 使用Nginx反向代理
// server {
//   listen 443 ssl;
//   ssl_certificate /path/to/cert.pem;
//   ssl_certificate_key /path/to/key.pem;
//   
//   location / {
//     proxy_pass http://localhost:3000;
//   }
// }
```

---

## 7. 错误处理

### 7.1 全局错误处理

```javascript
// middleware/error.js
function errorHandler(err, req, res, next) {
  console.error('错误:', err)
  
  // 开发环境返回详细错误
  if (process.env.NODE_ENV === 'development') {
    return res.json({
      code: 500,
      message: err.message,
      stack: err.stack
    })
  }
  
  // 生产环境返回通用错误
  res.json({
    code: 500,
    message: '服务器错误，请稍后重试'
  })
}

module.exports = errorHandler
```

```javascript
// app.js
const errorHandler = require('./middleware/error')

app.use(errorHandler)
```

### 7.2 异步错误处理

```javascript
// 使用async/await
app.get('/api/products', async (req, res, next) => {
  try {
    const products = await Product.find()
    res.json(Response.success(products))
  } catch (error) {
    next(error) // 传递给错误处理中间件
  }
})

// 或使用express-async-errors
require('express-async-errors')

app.get('/api/products', async (req, res) => {
  const products = await Product.find()
  res.json(Response.success(products))
  // 错误会自动传递给错误处理中间件
})
```

---

## 8. 部署

### 8.1 Docker部署

```dockerfile
# Dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 3000

CMD ["node", "src/app.js"]
```

```yaml
# docker-compose.yml
version: '3'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - MONGODB_URI=mongodb://mongo:27017/miniprogram
    depends_on:
      - mongo
  
  mongo:
    image: mongo:5
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

### 8.2 PM2部署

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'miniprogram-api',
    script: './src/app.js',
    instances: 2,
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss'
  }]
}
```

```bash
# 启动
pm2 start ecosystem.config.js

# 查看状态
pm2 status

# 查看日志
pm2 logs

# 重启
pm2 restart miniprogram-api
```

---

## 9. 常见问题

### Q1: 如何处理高并发？
**A**:
1. 使用Redis缓存热点数据
2. 数据库读写分离
3. 使用消息队列处理异步任务
4. 负载均衡

### Q2: 如何保证数据一致性？
**A**:
1. 使用数据库事务
2. 分布式锁
3. 最终一致性方案

### Q3: 如何优化API性能？
**A**:
1. 数据库索引优化
2. 查询结果缓存
3. 分页查询
4. 减少数据库查询次数

---

## 参考资源

- Node.js最佳实践
- RESTful API设计指南
- MongoDB官方文档
- 小程序后端开发规范

