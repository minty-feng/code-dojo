# Node.js学习路径

Node.js基于Chrome V8引擎的JavaScript运行时，事件驱动、非阻塞I/O，适合高并发Web应用。

## 学习时间线

**2022年4月 - 2023年7月（16个月）**

### 阶段一：环境搭建（2022-04）
- Node.js安装、版本管理
- npm/yarn/pnpm包管理
- 模块系统（CommonJS、ES Modules）
- 开发工具配置

### 阶段二：Express框架（2022-05）
- 路由、中间件
- RESTful API设计
- 模板引擎
- 错误处理

### 阶段三：异步编程（2022-09）
- 回调、Promise、async/await
- 事件循环原理
- MongoDB、MySQL、Redis
- Stream流处理

### 阶段四：TypeScript（2023-07）
- TypeScript基础
- 类型系统、接口
- Express类型定义
- 装饰器、工具类型

### 阶段五：实时通信和优化（2023-01）
- WebSocket、Socket.IO
- 集群模式、PM2
- 性能优化、缓存策略
- 内存和CPU优化

## 学习文档

1. **01-环境搭建.md** - Node.js安装、npm、模块系统
2. **02-Express框架.md** - 路由、中间件、RESTful API
3. **03-异步编程与数据库.md** - Promise、async/await、MongoDB、MySQL、Redis
4. **04-TypeScript集成.md** - TypeScript类型系统、Express类型定义
5. **05-WebSocket与性能优化.md** - Socket.IO、集群、性能优化

## Node.js核心特性

### 事件驱动
- **事件循环**：单线程事件循环模型
- **非阻塞I/O**：异步操作，高并发
- **回调队列**：宏任务和微任务
- **定时器**：setTimeout、setImmediate
- **EventEmitter**：事件发射器模式

### 异步编程
- **回调函数**：最基础的异步方式
- **Promise**：解决回调地狱
- **async/await**：同步风格写异步代码
- **Stream**：流式处理大数据
- **Worker Threads**：多线程支持

### 生态系统
- **npm**：最大的包仓库（200万+）
- **Express**：最流行的Web框架
- **Mongoose**：MongoDB ORM
- **Socket.IO**：WebSocket封装
- **TypeScript**：类型系统增强

## 技术栈

### Web框架
- **Express**：简洁、灵活、生态丰富
- **Koa**：现代、中间件优雅
- **Fastify**：高性能、TypeScript友好
- **NestJS**：企业级、Angular风格

### 数据库
- **MongoDB**：NoSQL、文档数据库
- **MySQL**：关系型数据库
- **PostgreSQL**：功能强大的关系型数据库
- **Redis**：缓存、会话存储

### ORM/ODM
- **Mongoose**：MongoDB ORM
- **Sequelize**：SQL ORM
- **TypeORM**：TypeScript ORM
- **Prisma**：现代ORM、类型安全

### 工具库
- **lodash**：工具函数集
- **moment/dayjs**：日期处理
- **axios**：HTTP客户端
- **joi/yup**：数据验证
- **bcrypt**：密码加密
- **jsonwebtoken**：JWT认证

## 应用场景

### Web后端
- RESTful API服务
- GraphQL服务
- 微服务架构
- BFF层

### 实时应用
- 聊天应用
- 协作编辑
- 实时通知
- 在线游戏

### 工具链
- Webpack、Vite构建工具
- ESLint、Prettier代码工具
- Jest、Mocha测试框架

### Serverless
- AWS Lambda
- Azure Functions
- Vercel Functions

## 最佳实践

### 项目结构
```
src/
├── app.ts              # Express应用
├── server.ts           # 服务器启动
├── routes/             # 路由
├── controllers/        # 控制器
├── models/             # 数据模型
├── middlewares/        # 中间件
├── services/           # 业务逻辑
├── utils/              # 工具函数
└── config/             # 配置
```

### 异步处理
- 优先使用async/await
- Promise.all并行操作
- 控制并发数量
- 统一错误处理
- 避免回调地狱

### 错误处理
- try-catch包裹异步代码
- 错误中间件统一处理
- unhandledRejection监听
- 日志记录完整错误栈

### 性能优化
- 使用集群模式
- Redis缓存热点数据
- 数据库查询优化
- 压缩响应数据
- 限流防止滥用

### 安全
- 输入验证
- SQL注入防护
- XSS防护
- CSRF防护
- 安全响应头（helmet）

## 学习资源

### 官方文档
- Node.js官网：https://nodejs.org
- Express文档：https://expressjs.com
- npm文档：https://docs.npmjs.com

### 推荐书籍
- Node.js实战
- 深入浅出Node.js
- Node.js设计模式

**核心：** Node.js通过事件循环和非阻塞I/O实现高并发，npm生态丰富，适合Web后端和实时应用开发。
