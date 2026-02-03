# 技术问答论坛使用指南

## 功能概述

这是一个技术问答论坛系统，集成了 Dify 聊天机器人，支持：

1. **帖子发布与管理** - 用户可以发布新帖，查看所有帖子
2. **自动@值班同学** - 在帖子讨论时自动通知值班的同学
3. **对话收集** - 自动收集并展示所有对话记录
4. **数据持久化** - 使用 localStorage 保存数据

## 主要功能

### 1. 帖子列表

- **帖子展示**：显示所有帖子，包括标题、作者、回复数、浏览量等
- **标签系统**：新帖子显示"新"标签，热门帖子（回复>10）显示"热门"标签
- **筛选功能**：支持按全部/最新/热门/我的筛选帖子
- **点击查看**：点击帖子可进入详情页

### 2. 帖子详情页

- **帖子信息**：显示完整的帖子标题和元信息
- **聊天机器人**：集成 Dify iframe 聊天机器人
- **自动@功能**：自动@所有在线值班的同学
- **对话记录**：实时显示所有对话内容

### 3. 值班同学管理

- **侧边栏显示**：在右侧显示所有值班同学
- **在线状态**：显示同学是否在线（绿色圆点）
- **自动通知**：在帖子讨论时自动@在线同学

### 4. 对话收集

- **自动收集**：通过 postMessage 监听自动收集对话
- **实时显示**：对话记录实时更新
- **导出功能**：可以导出对话记录为 JSON 格式

## 使用方法

### 发布新帖

1. 点击导航栏的"发布新帖"按钮
2. 输入帖子标题
3. 输入您的名字（可选，默认为"匿名用户"）
4. 系统自动创建帖子并打开详情页

### 参与讨论

1. 在帖子详情页的聊天窗口中输入问题
2. 系统自动@在线值班的同学
3. 对话内容自动记录在下方

### 查看对话记录

- 对话记录自动显示在帖子详情页下方
- 可以点击"导出记录"按钮保存对话

### 管理值班同学

在代码中修改 `onDutyUsers` 数组来管理值班同学：

```javascript
let onDutyUsers = [
    { id: 1, name: '张三', role: '前端工程师', avatar: '张', active: true },
    { id: 2, name: '李四', role: '后端工程师', avatar: '李', active: true },
    // ...
];
```

## 技术实现

### 数据存储

- 使用 `localStorage` 存储帖子列表和对话记录
- 数据结构：
  - `forum_posts`: 帖子列表
  - `forum_conversations`: 对话记录（按帖子ID索引）

### 对话收集

通过监听 `postMessage` 事件收集对话：

```javascript
window.addEventListener('message', function(event) {
    if (event.origin === 'http://agenthub.intra.xiaojukeji.com' && currentPostId) {
        handleChatMessage(event.data, currentPostId);
    }
});
```

### 自动@功能

在帖子打开时，自动@所有在线（active: true）的值班同学：

```javascript
function autoMentionOnDuty() {
    const activeUsers = onDutyUsers.filter(u => u.active);
    // 显示@标签
}
```

## 自定义配置

### 修改 Dify 聊天机器人

在 HTML 中找到 iframe 标签，修改 `src` 属性：

```html
<iframe
    id="dify-chat-iframe"
    src="http://agenthub.intra.xiaojukeji.com/chatbot/YOUR_TOKEN"
    frameborder="0"
    allow="microphone">
</iframe>
```

### 修改样式

所有样式都在 `<style>` 标签中，可以根据需要修改：
- 颜色主题：修改 `#1C64F2` 等颜色值
- 布局：调整 `grid-template-columns` 等布局属性
- 字体：修改 `font-family` 等字体属性

### 添加更多功能

可以在现有代码基础上扩展：
- 用户登录系统
- 帖子分类/标签
- 搜索功能
- 点赞/收藏功能
- 通知系统

## 注意事项

1. **数据持久化**：数据存储在浏览器 localStorage 中，清除浏览器数据会丢失
2. **跨域限制**：Dify iframe 跨域时，对话收集可能受限
3. **对话格式**：需要根据 Dify 实际的消息格式调整解析逻辑
4. **值班同学**：需要手动维护值班同学列表

## 未来改进

- [ ] 后端 API 集成（替代 localStorage）
- [ ] 用户认证系统
- [ ] 实时通知功能
- [ ] 更丰富的帖子编辑功能
- [ ] 图片上传支持
- [ ] 搜索和筛选优化
- [ ] 移动端适配优化