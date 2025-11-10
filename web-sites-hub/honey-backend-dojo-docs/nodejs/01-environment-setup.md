# 01-Node.js环境搭建

Node.js是基于Chrome V8引擎的JavaScript运行时，2009年由Ryan Dahl创建。事件驱动、非阻塞I/O，适合高并发场景。

## Node.js简介

### 设计特点

- **事件驱动**：基于事件循环处理I/O
- **非阻塞I/O**：异步操作，高并发
- **单线程**：主线程单一，Worker Threads可多线程
- **V8引擎**：JIT编译，性能优秀
- **跨平台**：Linux/Windows/macOS

### 应用场景

**Web后端：**
- RESTful API服务
- 微服务架构
- 实时应用（聊天、协作）
- BFF（Backend For Frontend）

**工具链：**
- Webpack、Vite构建工具
- ESLint、Prettier代码工具
- npm、yarn包管理

**桌面应用：**
- Electron（VS Code、Slack）

**其他：**
- 服务端渲染（Next.js、Nuxt.js）
- Serverless函数
- IoT设备

### 技术优势

**优势：**
- JavaScript全栈开发
- npm生态丰富（200万+包）
- 异步I/O高并发
- 快速开发迭代
- 活跃社区

**劣势：**
- CPU密集型任务性能差
- 回调地狱（已被Promise/async解决）
- 单线程限制（Worker Threads补充）
- 类型安全弱（TypeScript补充）

## 环境安装

### 版本选择

```bash
# 查看版本
node --version
npm --version

# LTS版本（推荐生产环境）
# Node.js 18 LTS（2022-10到2025-04）
# Node.js 20 LTS（2023-10到2026-04）

# Current版本（最新特性）
# Node.js 21（2023-10发布）
```

### 安装方式

**1. 官方安装包**
```bash
# 下载：https://nodejs.org
# LTS: 稳定版
# Current: 最新版

# 验证
node -v
npm -v
```

**2. nvm（推荐）**
```bash
# 安装nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# macOS
brew install nvm

# 安装Node.js
nvm install 18        # 安装v18
nvm install 20        # 安装v20
nvm install --lts    # 安装最新LTS

# 切换版本
nvm use 18
nvm use 20

# 设置默认版本
nvm alias default 18

# 查看已安装版本
nvm list

# 查看可用版本
nvm list-remote
```

**3. 包管理器**
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS
brew install node@18

# Windows
choco install nodejs-lts
```

## npm包管理

### 基本命令

```bash
# 初始化项目
npm init
npm init -y  # 默认配置

# 安装依赖
npm install express           # 生产依赖
npm install -D jest           # 开发依赖
npm install -g nodemon        # 全局安装

# 简写
npm i express
npm i -D jest
npm i -g nodemon

# 安装特定版本
npm install express@4.18.0
npm install express@latest

# 卸载
npm uninstall express
npm uninstall -g nodemon

# 更新
npm update
npm update express

# 查看过期包
npm outdated

# 审计安全漏洞
npm audit
npm audit fix

# 查看依赖树
npm list
npm list --depth=0

# 清理缓存
npm cache clean --force
```

### package.json

```json
{
  "name": "myapp",
  "version": "1.0.0",
  "description": "My Node.js app",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "webpack"
  },
  "keywords": ["api", "rest"],
  "author": "Your Name",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^7.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "nodemon": "^3.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### 语义化版本

```json
{
  "dependencies": {
    "express": "4.18.2",      // 精确版本
    "mongoose": "^7.0.0",     // 兼容版本（7.x.x）
    "axios": "~1.4.0",        // 补丁版本（1.4.x）
    "lodash": "*",            // 任意版本（不推荐）
    "dotenv": "latest"        // 最新版本（不推荐）
  }
}
```

## 模块系统

### CommonJS（默认）

```javascript
// 导出
// math.js
function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

module.exports = { add, subtract };

// 或
exports.add = add;
exports.subtract = subtract;

// 导入
// main.js
const math = require('./math');
console.log(math.add(2, 3));

// 解构导入
const { add, subtract } = require('./math');
console.log(add(2, 3));

// 内置模块
const fs = require('fs');
const path = require('path');
const http = require('http');
```

### ES Modules

```json
// package.json
{
  "type": "module"
}
```

```javascript
// 导出
// math.mjs 或 math.js（如果package.json设置了"type": "module"）
export function add(a, b) {
    return a + b;
}

export function subtract(a, b) {
    return a - b;
}

// 默认导出
export default function multiply(a, b) {
    return a * b;
}

// 导入
import { add, subtract } from './math.mjs';
import multiply from './math.mjs';

// 全部导入
import * as math from './math.mjs';

// 内置模块
import fs from 'fs';
import path from 'path';
```

## 开发工具

### VS Code配置

**必装插件：**
- ESLint
- Prettier
- JavaScript (ES6) code snippets
- REST Client
- npm Intellisense

**配置（.vscode/settings.json）：**
```json
{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "eslint.validate": [
        "javascript",
        "javascriptreact"
    ],
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true
    }
}
```

**调试配置（.vscode/launch.json）：**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Launch Program",
            "skipFiles": ["<node_internals>/**"],
            "program": "${workspaceFolder}/index.js"
        },
        {
            "type": "node",
            "request": "attach",
            "name": "Attach",
            "port": 9229
        }
    ]
}
```

### ESLint配置

```bash
# 安装
npm install -D eslint

# 初始化
npx eslint --init

# .eslintrc.json
{
    "env": {
        "node": true,
        "es2021": true
    },
    "extends": "eslint:recommended",
    "parserOptions": {
        "ecmaVersion": "latest"
    },
    "rules": {
        "indent": ["error", 2],
        "quotes": ["error", "single"],
        "semi": ["error", "always"]
    }
}
```

### Prettier配置

```json
// .prettierrc
{
    "semi": true,
    "singleQuote": true,
    "tabWidth": 2,
    "trailingComma": "es5",
    "printWidth": 80
}
```

## Hello World

### 基本程序

```javascript
// index.js
console.log('Hello, Node.js!');
```

```bash
# 运行
node index.js
```

### HTTP服务器

```javascript
// server.js
const http = require('http');

const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Hello, World!\n');
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
});
```

```bash
# 运行
node server.js

# 访问
curl http://localhost:3000
```

## 项目结构

### 标准布局

```
myproject/
├── package.json          # 项目配置
├── package-lock.json     # 依赖锁定
├── node_modules/         # 依赖包（.gitignore）
├── .env                  # 环境变量（.gitignore）
├── .gitignore
├── README.md
├── src/
│   ├── app.js           # 应用入口
│   ├── routes/          # 路由
│   ├── controllers/     # 控制器
│   ├── models/          # 数据模型
│   ├── middlewares/     # 中间件
│   ├── services/        # 业务逻辑
│   ├── utils/           # 工具函数
│   └── config/          # 配置
├── tests/               # 测试
└── public/              # 静态文件
    ├── css/
    ├── js/
    └── images/
```

## 常用内置模块

### fs（文件系统）

```javascript
const fs = require('fs');

// 同步读取
const data = fs.readFileSync('file.txt', 'utf8');

// 异步读取
fs.readFile('file.txt', 'utf8', (err, data) => {
    if (err) throw err;
    console.log(data);
});

// Promise版本
const fs = require('fs').promises;

async function readFile() {
    try {
        const data = await fs.readFile('file.txt', 'utf8');
        console.log(data);
    } catch (err) {
        console.error(err);
    }
}

// 写入
await fs.writeFile('output.txt', 'Hello');

// 追加
await fs.appendFile('log.txt', 'New line\n');

// 检查文件
if (fs.existsSync('file.txt')) {
    console.log('文件存在');
}

// 目录操作
await fs.mkdir('newdir', { recursive: true });
await fs.rmdir('olddir');
await fs.readdir('dir');
```

### path（路径）

```javascript
const path = require('path');

// 拼接路径
const filePath = path.join(__dirname, 'public', 'index.html');

// 解析路径
path.dirname('/home/user/file.txt');   // '/home/user'
path.basename('/home/user/file.txt');  // 'file.txt'
path.extname('/home/user/file.txt');   // '.txt'

// 绝对路径
path.resolve('file.txt');  // '/current/dir/file.txt'

// 规范化
path.normalize('/foo/bar//baz/asdf/quux/..');  // '/foo/bar/baz/asdf'
```

### process（进程）

```javascript
// 环境变量
console.log(process.env.NODE_ENV);
console.log(process.env.PORT);

// 命令行参数
console.log(process.argv);
// node app.js arg1 arg2
// ['node', '/path/to/app.js', 'arg1', 'arg2']

// 当前目录
console.log(process.cwd());

// 进程ID
console.log(process.pid);

// 退出
process.exit(0);  // 成功
process.exit(1);  // 失败

// 监听退出
process.on('exit', (code) => {
    console.log(`退出码: ${code}`);
});

// 监听未捕获异常
process.on('uncaughtException', (err) => {
    console.error('未捕获异常:', err);
    process.exit(1);
});
```

## 环境变量管理

### dotenv

```bash
npm install dotenv
```

```javascript
// .env文件
PORT=3000
DB_HOST=localhost
DB_USER=admin
DB_PASS=secret
NODE_ENV=development

// 加载
require('dotenv').config();

console.log(process.env.PORT);  // '3000'
console.log(process.env.DB_HOST);  // 'localhost'

// 不同环境
require('dotenv').config({
    path: `.env.${process.env.NODE_ENV}`
});
```

## 调试

### console调试

```javascript
console.log('普通日志');
console.error('错误日志');
console.warn('警告日志');
console.info('信息日志');

console.table([{ name: 'Alice', age: 25 }, { name: 'Bob', age: 30 }]);

console.time('操作');
// 耗时操作
console.timeEnd('操作');  // 操作: 123.456ms

console.trace('调用栈');
```

### 调试器

```bash
# Node.js内置调试器
node inspect index.js

# Chrome DevTools
node --inspect index.js
# 打开 chrome://inspect

# VS Code调试
# F5启动调试
# 断点、单步执行、变量查看
```

### nodemon热重载

```bash
# 安装
npm install -D nodemon

# package.json
{
  "scripts": {
    "dev": "nodemon index.js"
  }
}

# 运行
npm run dev

# nodemon.json配置
{
  "watch": ["src"],
  "ext": "js,json",
  "ignore": ["node_modules", "tests"],
  "exec": "node src/index.js"
}
```

## 性能监控

### 内置profiler

```bash
# CPU profile
node --prof app.js

# 生成报告
node --prof-process isolate-0x*.log > profile.txt

# 内存快照
node --heapsnapshot-signal=SIGUSR2 app.js

# 发送信号
kill -USR2 <pid>
```

### clinic.js

```bash
# 安装
npm install -g clinic

# CPU分析
clinic doctor -- node app.js

# 火焰图
clinic flame -- node app.js

# 气泡图
clinic bubbleprof -- node app.js
```

## 包管理器对比

### npm vs yarn vs pnpm

| 特性 | npm | yarn | pnpm |
|------|-----|------|------|
| 速度 | 中等 | 快 | 最快 |
| 磁盘占用 | 大 | 大 | 小（硬链接） |
| lock文件 | package-lock.json | yarn.lock | pnpm-lock.yaml |
| 离线缓存 | 有 | 有 | 有 |
| Workspaces | 支持 | 支持 | 支持 |

**yarn基本命令：**
```bash
yarn init
yarn add express
yarn add -D jest
yarn remove express
yarn install
yarn upgrade
```

**pnpm基本命令：**
```bash
pnpm init
pnpm add express
pnpm add -D jest
pnpm remove express
pnpm install
pnpm update
```

## 项目配置

### .gitignore

```
node_modules/
.env
.env.local
dist/
build/
*.log
.DS_Store
coverage/
.vscode/
```

### .npmrc

```
registry=https://registry.npmmirror.com
save-exact=true
engine-strict=true
```

### EditorConfig

```
# .editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
trim_trailing_whitespace = true
insert_final_newline = true
```

**核心：** Node.js基于V8引擎和事件循环，非阻塞I/O实现高并发。npm生态丰富，工具链完善。

