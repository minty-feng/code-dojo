# 安装指南

## 问题：npm registry 502 错误

如果遇到内部 npm registry 502 错误，可以使用以下解决方案：

## 方案一：使用混合 Registry（推荐）

已配置 `.npmrc` 使用混合 registry：
- 通用包（react, vite 等）从公共 registry 安装
- `@didi/agent-kit` 从内部 registry 安装

直接运行：
```bash
yarn install
```

## 方案二：临时使用公共 Registry

如果内部 registry 完全不可用，可以临时修改 `.npmrc`：

```bash
# 编辑 .npmrc，注释掉内部 registry
registry=https://registry.npmjs.org/
# @didi:registry=https://registry.npmjs.org/
```

**注意**：这样 `@didi/agent-kit` 可能无法安装，需要：
1. 手动从内部 registry 下载包
2. 或使用本地包路径
3. 或等待内部 registry 恢复

## 方案三：分步安装

先安装通用依赖，`@didi/agent-kit` 稍后处理：

```bash
# 1. 临时修改 package.json，移除 @didi/agent-kit
# 2. 安装其他依赖
yarn install

# 3. 等内部 registry 恢复后，再安装 @didi/agent-kit
yarn add @didi/agent-kit --registry=http://npm.intra.xiaojukeji.com
```

## 方案四：使用 npm 替代 yarn

有时 npm 的网络处理更好：

```bash
npm install
```

## 方案五：检查网络和代理

如果在内网环境，可能需要配置代理：

```bash
# 检查代理设置
echo $http_proxy
echo $https_proxy

# 如果需要设置代理
export http_proxy=http://your-proxy:port
export https_proxy=http://your-proxy:port
```

## 验证安装

安装成功后，检查 `node_modules` 目录：

```bash
ls node_modules/@didi/
```

应该能看到 `agent-kit` 目录。

## 如果 @didi/agent-kit 无法安装

如果 `@didi/agent-kit` 确实无法安装，可以：

1. **联系内部支持**：询问内部 npm registry 状态
2. **使用本地包**：如果有同事已经安装，可以复制 `node_modules/@didi/agent-kit`
3. **临时移除**：先开发其他功能，稍后再集成 AgentKit

## 开发模式（无 AgentKit）

如果暂时无法安装 `@didi/agent-kit`，可以：

1. 在 `src/App.jsx` 中注释掉 AgentKit 相关代码
2. 使用占位组件替代
3. 先完成其他功能开发

示例占位代码：

```javascript
// 临时占位组件
const AgentKitPlaceholder = () => (
  <div style={{ padding: '20px', background: '#f0f0f0', borderRadius: '8px' }}>
    <p>AgentKit 组件（需要安装 @didi/agent-kit）</p>
  </div>
)
```
