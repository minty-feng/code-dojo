# 故障排查指南

## 502 Bad Gateway 错误

### 错误说明

```
ResponseError: Request failed "502 Bad Gateway"
```

这个错误表示内部 npm registry (`http://npm.intra.xiaojukeji.com`) 暂时不可用。

### 解决方案

#### 方案 1：先安装其他依赖（推荐）

由于代码已经支持 AgentKit 未安装的情况（会显示占位组件），可以先安装其他依赖：

```bash
# 1. 临时移除 @didi/agent-kit（已在 package.json 中移除）
# 2. 安装其他依赖
yarn install

# 3. 启动项目测试
yarn dev

# 4. 等内部 registry 恢复后，再安装 AgentKit
yarn add @didi/agent-kit --registry=http://npm.intra.xiaojukeji.com
```

#### 方案 2：检查网络连接

```bash
# 检查是否能访问内部 registry
curl -I http://npm.intra.xiaojukeji.com

# 检查代理设置
echo $http_proxy
echo $https_proxy
```

#### 方案 3：使用 npm 替代 yarn

有时 npm 的网络处理更好：

```bash
npm install
npm install @didi/agent-kit --registry=http://npm.intra.xiaojukeji.com
```

#### 方案 4：联系内部支持

如果 registry 持续不可用：
1. 联系内部 DevOps 团队
2. 询问 registry 服务状态
3. 确认是否需要 VPN 或特殊网络配置

### 临时开发方案

即使没有安装 `@didi/agent-kit`，项目也可以运行：

1. **代码已支持**：`App.jsx` 中已添加了条件导入和占位组件
2. **功能可用**：帖子列表、帖子详情、对话记录等功能都可以正常使用
3. **占位显示**：聊天窗口会显示提示信息，说明需要安装 AgentKit

### 验证安装

安装成功后，检查：

```bash
# 检查 node_modules
ls node_modules/@didi/

# 应该能看到 agent-kit 目录
```

### 常见问题

**Q: 为什么会出现 502 错误？**
A: 内部 registry 服务可能正在维护或出现故障。

**Q: 可以跳过 AgentKit 吗？**
A: 可以，代码已经支持。项目会显示占位组件，其他功能正常。

**Q: 什么时候可以安装 AgentKit？**
A: 等内部 registry 恢复后即可安装。可以定期尝试：
```bash
yarn add @didi/agent-kit --registry=http://npm.intra.xiaojukeji.com
```

**Q: 如何知道 registry 恢复了？**
A: 可以尝试访问 registry 的网页版，或运行简单的 curl 命令测试。
