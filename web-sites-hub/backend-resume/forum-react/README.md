# 技术问答论坛 - React + API 版本

基于 React 和 AgentHub API 构建的技术问答论坛系统。

## 功能特点

- ✅ 直接调用 AgentHub API（不使用 SDK 和 iframe）
- ✅ 流式响应支持
- ✅ 帖子发布与管理
- ✅ 自动@值班同学功能
- ✅ 对话记录收集与展示
- ✅ 数据持久化（localStorage）
- ✅ 响应式设计

## 安装依赖

```bash
# 使用内部 npm registry
yarn install
# 或
npm install
```

## 配置 API

编辑 `src/components/ChatComponent.jsx` 文件，修改以下配置：

```javascript
const API_URL = 'http://agenthub.intra.xiaojukeji.com/v1/chat-messages'
const API_KEY = 'app-GdVMAxRyH3Mj9N72piy1aAgR' // 替换为你的 API Key
```

**注意**：生产环境建议通过后端代理 API，避免在前端暴露 API Key。

## 运行项目

```bash
# 开发模式
yarn dev
# 或
npm run dev

# 构建生产版本
yarn build
# 或
npm run build

# 预览生产版本
yarn preview
# 或
npm run preview
```

## 项目结构

```
forum-react/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          # 导航栏组件
│   │   ├── PostsPage.jsx        # 帖子列表页
│   │   ├── PostDetailPage.jsx  # 帖子详情页
│   │   └── ChatComponent.jsx   # 聊天组件（直接调用 API）
│   ├── App.jsx                  # 主应用组件
│   ├── App.css                  # 主样式
│   ├── main.jsx                 # 入口文件
│   └── index.css                # 全局样式
├── index.html                   # HTML 模板
├── vite.config.js              # Vite 配置
├── package.json                # 项目配置
└── README.md                   # 说明文档
```

## 主要功能说明

### 1. API 集成

- 直接调用 AgentHub API，不使用 SDK 和 iframe
- 支持流式响应（Server-Sent Events）
- 支持自定义工具栏按钮
- 自动@值班同学功能集成到工具栏
- 通过 `inputs` 传递帖子上下文信息

### 2. 帖子管理

- 创建新帖子
- 查看帖子列表
- 帖子详情页
- 自动统计浏览量和回复数

### 3. 值班同学

- 侧边栏显示值班同学列表
- 在线状态标识
- 自动@功能

### 4. 对话收集

- 通过 API 响应收集对话
- 实时显示流式对话记录
- 支持导出对话记录

## 自定义配置

### 修改值班同学

编辑 `src/App.jsx` 中的 `onDutyUsers` 数组：

```javascript
const [onDutyUsers] = useState([
  { id: 1, name: '张三', role: '前端工程师', avatar: '张', active: true },
  // ...
])
```

### 修改聊天工具栏

编辑 `src/components/ChatComponent.jsx` 中的工具栏按钮：

```javascript
<div className="chat-toolbar">
  <button onClick={() => handleQuickPrompt('你的提示词')}>
    按钮名称
  </button>
  // ...
</div>
```

## 注意事项

1. **API Key 安全**：建议通过后端代理 AgentHub API，避免在前端暴露 API Key
2. **用户标识**：使用唯一的用户标识（如 LDAP），确保跨设备同步
3. **数据持久化**：当前使用 localStorage，生产环境建议使用后端 API
4. **流式响应**：使用 Server-Sent Events (SSE) 处理流式响应，支持实时显示对话内容
5. **错误处理**：已实现基本的错误处理和请求取消功能

## 与 iframe/SDK 版本的对比

| 特性 | iframe 版本 | SDK 版本 | API 版本 |
|------|------------|---------|---------|
| 集成方式 | iframe 嵌入 | React SDK | 直接 API 调用 |
| 样式隔离 | 完全隔离 | ShadowDOM 隔离 | 无隔离 |
| 自定义能力 | 有限 | 高度可定制 | 完全可控 |
| 对话收集 | postMessage | SDK 回调/事件 | API 响应 |
| 性能 | 独立进程 | 同进程 | 同进程 |
| 依赖 | 无 | 需要 SDK | 无 |
| 适用场景 | 简单嵌入 | 深度集成 | 完全自定义 |

## 开发建议

1. 根据实际需求调整 API 配置和请求参数
2. 实现后端 API 替代 localStorage
3. 添加用户认证系统
4. 实现实时通知功能
5. 优化移动端体验
6. 考虑添加请求重试机制
7. 优化流式响应的错误处理

## API 使用说明

### 请求格式

```javascript
POST http://agenthub.intra.xiaojukeji.com/v1/chat-messages
Headers:
  Authorization: Bearer {API_KEY}
  Content-Type: application/json
Body:
{
  "inputs": {},           // 上下文信息
  "query": "问题内容",     // 用户问题
  "response_mode": "streaming",  // 流式响应
  "conversation_id": "",  // 对话ID（可选）
  "user": "用户ID",
  "files": []            // 文件列表（可选）
}
```

### 响应格式

流式响应使用 Server-Sent Events (SSE) 格式：
- `event: message` - 消息内容
- `event: message_end` - 消息结束
- `event: error` - 错误信息

## 参考文档

- [React 文档](https://react.dev)
- [Vite 文档](https://vitejs.dev)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
