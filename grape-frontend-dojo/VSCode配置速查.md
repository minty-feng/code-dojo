# VSCode前端开发配置速查

## 🚀 快速开始

### 纯HTML项目（30秒启动）

```bash
# 1. 创建项目目录
mkdir my-project && cd my-project

# 2. 创建index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project</title>
</head>
<body>
    <h1>Hello World!</h1>
    <script src="script.js"></script>
</body>
</html>
EOF

# 3. 启动服务器（选择一种）
npx live-server                    # 推荐
python3 -m http.server 8000        # Python
npx http-server                    # http-server
npx serve                          # serve
```

### React/Vue项目（1分钟启动）

```bash
# React + Vite
pnpm create vite my-app --template react-ts
cd my-app && pnpm install && pnpm dev

# Vue + Vite  
pnpm create vue@latest my-app
cd my-app && pnpm install && pnpm dev
```

## 📁 VSCode配置文件

### .vscode/settings.json（必备）

```json
{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": "explicit"
    },
    "editor.tabSize": 2,
    "files.eol": "\n",
    "[javascript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[vue]": {
        "editor.defaultFormatter": "Vue.volar"
    },
    "eslint.validate": [
        "javascript",
        "javascriptreact",
        "typescript",
        "typescriptreact",
        "vue"
    ]
}
```

### .vscode/launch.json（调试配置）

```json
{
    "version": "0.2.0",
    "configurations": [
        // 调试React/Vue项目
        {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome: 启动调试",
            "url": "http://localhost:5173",
            "webRoot": "${workspaceFolder}/src"
        },
        // 调试纯HTML
        {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome: 打开HTML",
            "file": "${workspaceFolder}/index.html"
        },
        // 调试当前文件
        {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome: 当前文件",
            "file": "${file}"
        },
        // 调试Node.js
        {
            "type": "node",
            "request": "launch",
            "name": "Node: 当前文件",
            "program": "${file}",
            "skipFiles": ["<node_internals>/**"]
        }
    ]
}
```

### .vscode/tasks.json（任务配置）

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Dev Server",
            "type": "shell",
            "command": "pnpm dev",
            "isBackground": true
        },
        {
            "label": "Build",
            "type": "shell",
            "command": "pnpm build",
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "Test",
            "type": "shell",
            "command": "pnpm test",
            "group": {
                "kind": "test",
                "isDefault": true
            }
        }
    ]
}
```

## 🔧 必装VSCode插件

```bash
# 基础插件
- ESLint                    # 代码检查
- Prettier                  # 代码格式化
- EditorConfig             # 统一编码风格

# HTML/CSS
- Live Server              # HTML实时预览
- Auto Rename Tag          # 自动重命名标签
- CSS Peek                 # CSS定义跳转

# JavaScript/TypeScript
- JavaScript (ES6) code snippets
- TypeScript Vue Plugin

# 框架
- ES7+ React/Redux/React-Native snippets
- Vue - Official (Volar)

# 工具
- Path Intellisense        # 路径提示
- Error Lens              # 错误提示
- GitLens                 # Git增强
- Import Cost             # 包大小提示
```

## ⚡ 常用快捷键

### 编辑
- `Cmd/Ctrl + D` - 选择下一个相同内容
- `Cmd/Ctrl + Shift + L` - 选择所有相同内容
- `Cmd/Ctrl + /` - 切换注释
- `Alt + ↑/↓` - 移动行
- `Shift + Alt + ↑/↓` - 复制行
- `Cmd/Ctrl + Shift + K` - 删除行

### 导航
- `Cmd/Ctrl + P` - 快速打开文件
- `Cmd/Ctrl + Shift + P` - 命令面板
- `Cmd/Ctrl + B` - 切换侧边栏
- `Cmd/Ctrl + J` - 切换面板
- `Ctrl + Tab` - 切换文件

### 调试
- `F5` - 开始调试
- `F9` - 切换断点
- `F10` - 单步跳过
- `F11` - 单步进入
- `Shift + F11` - 单步跳出

## 🎯 调试技巧

### Chrome DevTools
```javascript
// 1. 在代码中添加断点
debugger;

// 2. 条件断点
// 右键断点 → Edit Breakpoint → 输入条件
if (userId === 123)

// 3. 日志点
// 右键断点 → Logpoint
console.log('User:', user);
```

### VSCode调试
1. 按 `F5` 或点击左侧调试图标
2. 选择配置（Chrome/Node等）
3. 设置断点（点击行号左侧）
4. 查看变量、调用栈、断点列表

### React DevTools
```bash
# Chrome扩展安装
# 查看组件树
# 检查Props和State
# 使用Profiler分析性能
```

## 📦 项目模板

### 纯HTML模板
```
my-html-project/
├── index.html
├── css/
│   ├── reset.css
│   └── style.css
├── js/
│   └── main.js
├── images/
└── .vscode/
    ├── settings.json
    ├── launch.json
    └── tasks.json
```

### React项目模板
```
my-react-app/
├── src/
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   ├── types/
│   ├── styles/
│   ├── App.tsx
│   └── main.tsx
├── public/
├── .vscode/
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## 🐛 常见问题

### 1. Live Server不工作
```bash
# 检查端口占用
lsof -i :5500

# 更换端口
live-server --port=8080

# 重启VSCode
```

### 2. ESLint报错
```bash
# 安装依赖
pnpm add -D eslint

# 初始化配置
npx eslint --init

# 禁用某行检查
// eslint-disable-next-line
```

### 3. Prettier不格式化
```bash
# 检查默认格式化器
Cmd/Ctrl + Shift + P → Format Document With

# 设置默认格式化器
"editor.defaultFormatter": "esbenp.prettier-vscode"

# 保存时格式化
"editor.formatOnSave": true
```

### 4. 调试无法连接
```bash
# 检查端口
# 确保dev server正在运行
pnpm dev

# 检查URL是否正确
"url": "http://localhost:5173"

# 清除Chrome缓存
```

### 5. TypeScript报错
```bash
# 重启TS服务器
Cmd/Ctrl + Shift + P → TypeScript: Restart TS Server

# 检查tsconfig.json
# 安装类型定义
pnpm add -D @types/node @types/react
```

## 🔥 实用命令

### 包管理
```bash
# 查看已安装包
pnpm list
pnpm list --depth=0

# 更新依赖
pnpm update
pnpm outdated

# 清理
pnpm store prune
rm -rf node_modules && pnpm install
```

### Git命令
```bash
# 暂存和提交
git add .
git commit -m "feat: 添加新功能"

# 查看状态
git status
git log --oneline

# 分支操作
git checkout -b feature/new
git merge feature/new
```

### 项目命令
```bash
# 开发
pnpm dev

# 构建
pnpm build

# 预览
pnpm preview

# 测试
pnpm test
pnpm test:coverage

# 类型检查
pnpm type-check

# Lint
pnpm lint
pnpm lint:fix
```

## 💡 最佳实践

### 1. 代码组织
```
src/
├── components/     # 公共组件
├── pages/         # 页面组件
├── hooks/         # 自定义Hooks
├── utils/         # 工具函数
├── types/         # 类型定义
├── api/           # API接口
├── store/         # 状态管理
└── styles/        # 全局样式
```

### 2. 命名规范
```javascript
// 组件：PascalCase
Button.tsx
UserProfile.tsx

// 文件：kebab-case
user-service.ts
api-client.ts

// 变量：camelCase
const userName = 'John';
const isActive = true;

// 常量：UPPER_SNAKE_CASE
const MAX_COUNT = 100;
const API_URL = 'https://api.example.com';
```

### 3. Git提交规范
```bash
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具

# 示例
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复按钮点击无响应的问题"
```

### 4. 环境变量
```bash
# .env.development
VITE_API_URL=http://localhost:3000
VITE_APP_TITLE=My App (Dev)

# .env.production
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App
```

## 🎓 学习资源

- [MDN Web Docs](https://developer.mozilla.org/zh-CN/)
- [React官方文档](https://react.dev/)
- [Vue官方文档](https://cn.vuejs.org/)
- [TypeScript手册](https://www.typescriptlang.org/docs/)
- [VSCode文档](https://code.visualstudio.com/docs)

---

**快速启动提示**：
1. 纯HTML项目：`npx live-server`
2. React项目：`pnpm create vite`
3. Vue项目：`pnpm create vue@latest`
4. 调试：按 `F5`，选择配置
5. 格式化：`Shift + Alt + F`

