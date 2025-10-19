# 🍇 前端道场

现代前端开发技术的学习和实践。

## 📖 目录结构

```
grape-frontend-dojo/
├── 00-环境配置.md           # 开发环境搭建、工具配置
├── 01-调试技巧.md           # 浏览器调试、性能分析
├── 02-测试技术.md           # 单元测试、E2E测试
├── 03-性能优化.md           # 性能优化最佳实践
├── html/                    # HTML核心技术
│   ├── README.md
│   ├── 01-基础标签与文档结构.md
│   ├── 02-表单元素详解.md
│   ├── 03-语义化与可访问性.md
│   └── 04-Canvas与SVG.md
├── css/                     # CSS核心技术
│   ├── README.md
│   ├── 01-选择器与优先级.md
│   ├── 02-Flexbox布局.md
│   ├── 03-Grid布局.md
│   └── 04-动画与过渡.md
├── javascript/              # JavaScript核心技术
│   ├── README.md
│   ├── 01-ES6+核心特性.md
│   └── 02-异步编程.md
├── typescript/              # TypeScript核心技术
│   ├── README.md
│   └── 01-类型系统.md
├── react/                   # React框架
│   ├── README.md
│   └── 01-Hooks核心.md
└── vue/                     # Vue框架
    ├── README.md
    └── 01-Composition API.md
```

## 🎯 学习路径

### 第一阶段：基础夯实（1-2个月）

#### HTML & CSS
- [HTML基础](./html/01-基础标签与文档结构.md) - 掌握HTML5标签和文档结构
- [表单元素](./html/02-表单元素详解.md) - 熟悉表单控件和验证
- [语义化与可访问性](./html/03-语义化与可访问性.md) - 提升代码质量和SEO
- [Canvas与SVG](./html/04-Canvas与SVG.md) - 图形绘制技术
- [CSS选择器](./css/01-选择器与优先级.md) - 精通选择器和优先级
- [Flexbox布局](./css/02-Flexbox布局.md) - 一维布局系统
- [Grid布局](./css/03-Grid布局.md) - 二维网格布局
- [CSS动画](./css/04-动画与过渡.md) - 动画和过渡效果

#### JavaScript基础
- [ES6+特性](./javascript/01-ES6+核心特性.md) - 现代JavaScript语法
- [异步编程](./javascript/02-异步编程.md) - Promise、async/await

### 第二阶段：框架进阶（2-3个月）

#### TypeScript
- [类型系统](./typescript/01-类型系统.md) - TypeScript核心类型系统

#### React生态
- [React Hooks](./react/01-Hooks核心.md) - 函数组件和Hooks
- React Router - 路由管理
- Redux/Zustand - 状态管理
- React Query - 数据获取

#### Vue生态
- [Composition API](./vue/01-Composition API.md) - Vue 3组合式API
- Vue Router - 路由系统
- Pinia - 状态管理
- VueUse - 组合式函数库

### 第三阶段：工程化实践（2-3个月）

#### 开发环境
- [环境配置](./00-环境配置.md) - Node.js、编辑器、代码规范

#### 质量保障
- [调试技巧](./01-调试技巧.md) - DevTools、断点调试
- [测试技术](./02-测试技术.md) - 单元测试、E2E测试

#### 性能优化
- [性能优化](./03-性能优化.md) - 代码优化、资源优化、监控

### 第四阶段：高级应用（持续学习）

#### 构建工具
- Vite - 下一代构建工具
- Webpack - 模块打包器
- Rollup - 库打包工具

#### 进阶主题
- 微前端架构
- SSR/SSG - 服务端渲染
- PWA - 渐进式Web应用
- WebAssembly
- 低代码平台

## 🎨 技术栈

### 核心技术
- **HTML5**：语义化标签、表单、Canvas、SVG
- **CSS3**：Flexbox、Grid、动画、响应式
- **JavaScript ES6+**：模块化、异步、函数式
- **TypeScript**：类型系统、泛型、工具类型

### 主流框架
- **React**：组件化、Hooks、状态管理、路由
- **Vue**：响应式、Composition API、Pinia
- **Next.js**：React SSR框架
- **Nuxt**：Vue SSR框架

### 工程化
- **构建工具**：Vite、Webpack、Rollup
- **包管理**：pnpm、npm、yarn
- **代码规范**：ESLint、Prettier、Husky
- **测试**：Vitest、Playwright、Testing Library

### 状态管理
- **React**：Redux Toolkit、Zustand、Jotai
- **Vue**：Pinia、Vuex

### UI框架
- **React**：Material-UI、Ant Design、Chakra UI
- **Vue**：Element Plus、Naive UI、Vuetify
- **CSS框架**：Tailwind CSS、UnoCSS

## 🚀 快速开始

### 环境准备
```bash
# 安装Node.js（推荐使用nvm）
nvm install 20
nvm use 20

# 安装pnpm
npm install -g pnpm

# 验证安装
node -v
pnpm -v
```

### 创建项目
```bash
# React + Vite
pnpm create vite my-react-app --template react-ts

# Vue + Vite
pnpm create vue@latest my-vue-app

# Next.js
pnpm create next-app my-next-app

# Nuxt
pnpm dlx nuxi init my-nuxt-app
```

## 💡 学习建议

### 学习方法
1. **理论与实践结合**：学习概念后立即动手实践
2. **项目驱动学习**：通过实际项目巩固知识
3. **阅读优秀代码**：学习开源项目的代码结构
4. **持续学习**：关注技术动态，保持学习热情

### 推荐实践项目
- **Todo List**：基础CRUD操作
- **博客系统**：路由、状态管理、API集成
- **电商网站**：复杂业务逻辑、购物车、支付
- **管理后台**：数据表格、图表、权限管理
- **社交应用**：实时通信、文件上传、用户系统

### 代码规范
- 使用TypeScript增强类型安全
- 遵循ESLint和Prettier规范
- 编写单元测试和E2E测试
- 使用语义化的Git提交信息
- 注重代码可读性和可维护性

## 🔧 常用工具

### 开发工具
- **编辑器**：VSCode、WebStorm
- **版本控制**：Git、GitHub
- **设计工具**：Figma、Sketch
- **API工具**：Postman、Insomnia

### 浏览器工具
- **Chrome DevTools**：调试、性能分析
- **React DevTools**：React组件调试
- **Vue DevTools**：Vue组件调试
- **Lighthouse**：性能评分

### 在线工具
- **CodePen/CodeSandbox**：在线代码编辑
- **Can I Use**：浏览器兼容性查询
- **Bundlephobia**：包大小分析
- **TypeScript Playground**：TS在线编译

## 📚 推荐资源

### 官方文档
- [MDN Web Docs](https://developer.mozilla.org/zh-CN/) - Web技术权威文档
- [React官方文档](https://react.dev/) - React学习资源
- [Vue官方文档](https://cn.vuejs.org/) - Vue学习资源
- [TypeScript官方文档](https://www.typescriptlang.org/) - TypeScript指南

### 学习网站
- [JavaScript.info](https://javascript.info/) - 现代JavaScript教程
- [web.dev](https://web.dev/) - Google Web开发最佳实践
- [CSS-Tricks](https://css-tricks.com/) - CSS技巧和教程
- [Frontend Masters](https://frontendmasters.com/) - 前端进阶课程

### 技术博客
- [Dan Abramov's Blog](https://overreacted.io/) - React核心开发者
- [Vue Blog](https://blog.vuejs.org/) - Vue官方博客
- [掘金](https://juejin.cn/) - 中文技术社区

### GitHub资源
- [Awesome React](https://github.com/enaqx/awesome-react)
- [Awesome Vue](https://github.com/vuejs/awesome-vue)
- [Frontend Checklist](https://github.com/thedaviddias/Front-End-Checklist)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)

## 🎯 学习目标

### 初级前端（0-1年）
- ✅ 熟练掌握HTML/CSS/JavaScript
- ✅ 理解DOM操作和事件处理
- ✅ 掌握一个主流框架（React或Vue）
- ✅ 能够独立完成中小型项目

### 中级前端（1-3年）
- ✅ 精通框架生态（路由、状态管理）
- ✅ 掌握TypeScript
- ✅ 理解工程化和构建工具
- ✅ 具备代码质量和性能优化意识
- ✅ 能够进行技术选型和架构设计

### 高级前端（3年以上）
- ✅ 深入理解框架原理
- ✅ 掌握多种技术栈
- ✅ 具备系统架构能力
- ✅ 能够解决复杂技术难题
- ✅ 具备团队协作和技术领导力

## 💪 实战项目

### 初级项目
- [ ] **计算器**：基础UI和逻辑
- [ ] **待办事项**：CRUD操作、本地存储
- [ ] **天气应用**：API调用、数据展示
- [ ] **倒计时**：定时器、状态管理

### 中级项目
- [ ] **博客系统**：Markdown编辑器、评论系统
- [ ] **电商前台**：商品列表、购物车、结算
- [ ] **音乐播放器**：播放控制、播放列表
- [ ] **在线聊天**：WebSocket、实时通信

### 高级项目
- [ ] **管理后台**：权限系统、数据可视化
- [ ] **低代码平台**：拖拽、配置、渲染
- [ ] **协同编辑器**：OT/CRDT、实时协作
- [ ] **微前端应用**：模块联邦、独立部署

## 🤝 贡献指南

欢迎贡献内容！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 🌟 总结

前端开发是一个快速发展的领域，保持学习热情和好奇心非常重要。通过系统化学习和大量实践，你将能够：

- 构建高质量的Web应用
- 解决复杂的技术问题
- 掌握现代化开发流程
- 提升用户体验
- 实现职业成长

让我们一起在前端道场中不断精进，成为优秀的前端工程师！🚀
