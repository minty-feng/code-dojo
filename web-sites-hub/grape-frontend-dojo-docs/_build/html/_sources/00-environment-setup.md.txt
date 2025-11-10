# 00-环境配置

## 📋 学习目标
- 配置现代前端开发环境
- 掌握常用开发工具
- 理解Node.js版本管理
- 配置编辑器和插件

## 🔧 Node.js环境

### 安装Node.js
```bash
# 方式1：官网下载安装
# https://nodejs.org/

# 方式2：使用nvm（推荐）
# macOS/Linux
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Windows
# 下载nvm-windows: https://github.com/coreybutler/nvm-windows

# 安装指定版本
nvm install 20
nvm install 18

# 切换版本
nvm use 20

# 查看已安装版本
nvm list

# 设置默认版本
nvm alias default 20
```

### npm配置
```bash
# 查看配置
npm config list

# 设置镜像源（淘宝镜像）
npm config set registry https://registry.npmmirror.com

# 还原官方源
npm config set registry https://registry.npmjs.org

# 全局安装路径
npm config get prefix

# 缓存路径
npm config get cache

# 清理缓存
npm cache clean --force
```

### 包管理器

#### pnpm（推荐）
```bash
# 安装pnpm
npm install -g pnpm

# 设置镜像
pnpm config set registry https://registry.npmmirror.com

# 创建项目
pnpm create vite my-app
pnpm create vue@latest

# 安装依赖
pnpm install
pnpm add react
pnpm add -D typescript

# 运行脚本
pnpm dev
pnpm build
```

#### Yarn
```bash
# 安装Yarn
npm install -g yarn

# 设置镜像
yarn config set registry https://registry.npmmirror.com

# 使用
yarn install
yarn add react
yarn dev
```

## 📝 编辑器配置

### VSCode配置

#### 必装插件
```json
{
    "extensions": [
        // 通用
        "editorconfig.editorconfig",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        
        // HTML/CSS
        "bradlc.vscode-tailwindcss",
        "ecmel.vscode-html-css",
        
        // JavaScript/TypeScript
        "ms-vscode.vscode-typescript-next",
        "dsznajder.es7-react-js-snippets",
        
        // Vue
        "Vue.volar",
        "Vue.vscode-typescript-vue-plugin",
        
        // 工具
        "formulahendry.auto-rename-tag",
        "christian-kohler.path-intellisense",
        "usernamehw.errorlens"
    ]
}
```

#### settings.json
```json
{
    // 编辑器
    "editor.fontSize": 14,
    "editor.tabSize": 2,
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": "explicit"
    },
    "editor.bracketPairColorization.enabled": true,
    "editor.guides.bracketPairs": true,
    "editor.inlineSuggest.enabled": true,
    "editor.minimap.enabled": true,
    
    // 文件
    "files.autoSave": "onFocusChange",
    "files.eol": "\n",
    "files.associations": {
        "*.css": "css",
        "*.scss": "scss",
        "*.jsx": "javascriptreact",
        "*.tsx": "typescriptreact"
    },
    
    // Prettier
    "[javascript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[javascriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[typescriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[vue]": {
        "editor.defaultFormatter": "Vue.volar"
    },
    "[json]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[html]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[css]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    
    // ESLint
    "eslint.validate": [
        "javascript",
        "javascriptreact",
        "typescript",
        "typescriptreact",
        "vue"
    ],
    "eslint.format.enable": true,
    
    // TypeScript
    "typescript.updateImportsOnFileMove.enabled": "always",
    "typescript.preferences.importModuleSpecifier": "relative",
    
    // JavaScript
    "javascript.updateImportsOnFileMove.enabled": "always",
    
    // Emmet
    "emmet.includeLanguages": {
        "javascript": "javascriptreact",
        "typescript": "typescriptreact"
    },
    
    // 终端
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.defaultProfile.osx": "zsh"
}
```

#### launch.json（调试配置）
```json
{
    "version": "0.2.0",
    "configurations": [
        // Chrome调试 - React/Vue项目
        {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome: 启动调试",
            "url": "http://localhost:5173",
            "webRoot": "${workspaceFolder}/src",
            "sourceMaps": true,
            "sourceMapPathOverrides": {
                "webpack:///src/*": "${webRoot}/*"
            }
        },
        // Chrome调试 - 纯HTML
        {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome: 打开HTML",
            "file": "${workspaceFolder}/index.html",
            "preLaunchTask": "Start Live Server"
        },
        // 附加到已运行的Chrome
        {
            "type": "chrome",
            "request": "attach",
            "name": "Chrome: 附加调试",
            "port": 9222,
            "webRoot": "${workspaceFolder}"
        },
        // Node.js调试
        {
            "type": "node",
            "request": "launch",
            "name": "Node: 当前文件",
            "program": "${file}",
            "skipFiles": ["<node_internals>/**"],
            "console": "integratedTerminal"
        },
        // Jest测试调试
        {
            "type": "node",
            "request": "launch",
            "name": "Jest: 当前测试",
            "program": "${workspaceFolder}/node_modules/.bin/jest",
            "args": ["${file}", "--runInBand"],
            "console": "integratedTerminal",
            "internalConsoleOptions": "neverOpen"
        },
        // Vitest测试调试
        {
            "type": "node",
            "request": "launch",
            "name": "Vitest: 当前测试",
            "runtimeExecutable": "pnpm",
            "runtimeArgs": ["test", "--run", "${file}"],
            "console": "integratedTerminal"
        }
    ]
}
```

#### tasks.json（任务配置）
```json
{
    "version": "2.0.0",
    "tasks": [
        // 启动开发服务器
        {
            "label": "Dev Server",
            "type": "shell",
            "command": "pnpm dev",
            "isBackground": true,
            "problemMatcher": {
                "pattern": {
                    "regexp": ".",
                    "file": 1,
                    "location": 2,
                    "message": 3
                },
                "background": {
                    "activeOnStart": true,
                    "beginsPattern": ".",
                    "endsPattern": "Local:.*"
                }
            }
        },
        // 启动Live Server（纯HTML）
        {
            "label": "Start Live Server",
            "type": "shell",
            "command": "npx live-server --port=5500 --no-browser",
            "isBackground": true,
            "problemMatcher": {
                "pattern": {
                    "regexp": ".",
                    "file": 1,
                    "location": 2,
                    "message": 3
                },
                "background": {
                    "activeOnStart": true,
                    "beginsPattern": ".",
                    "endsPattern": "Serving.*"
                }
            }
        },
        // 构建项目
        {
            "label": "Build",
            "type": "shell",
            "command": "pnpm build",
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        // 运行测试
        {
            "label": "Test",
            "type": "shell",
            "command": "pnpm test",
            "group": {
                "kind": "test",
                "isDefault": true
            }
        },
        // ESLint检查
        {
            "label": "ESLint",
            "type": "shell",
            "command": "pnpm eslint src --ext .js,.jsx,.ts,.tsx",
            "problemMatcher": ["$eslint-stylish"]
        },
        // 格式化代码
        {
            "label": "Format",
            "type": "shell",
            "command": "pnpm prettier --write src"
        }
    ]
}
```

## 🎨 代码规范

### ESLint配置
```bash
# 安装ESLint
pnpm add -D eslint

# 初始化配置
npx eslint --init
```

#### .eslintrc.js
```javascript
module.exports = {
    env: {
        browser: true,
        es2021: true,
        node: true
    },
    extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:react/recommended', // React项目
        'plugin:vue/vue3-recommended', // Vue项目
        'prettier' // 必须放在最后
    ],
    parser: '@typescript-eslint/parser',
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: {
            jsx: true
        }
    },
    plugins: [
        '@typescript-eslint',
        'react',
        'vue'
    ],
    rules: {
        'no-console': 'warn',
        'no-debugger': 'error',
        '@typescript-eslint/no-unused-vars': 'warn',
        '@typescript-eslint/no-explicit-any': 'warn'
    }
};
```

### Prettier配置

#### .prettierrc
```json
{
    "semi": true,
    "singleQuote": true,
    "tabWidth": 2,
    "trailingComma": "es5",
    "printWidth": 100,
    "arrowParens": "avoid",
    "endOfLine": "lf"
}
```

#### .prettierignore
```
node_modules
dist
build
.next
coverage
*.min.js
*.min.css
```

### EditorConfig

#### .editorconfig
```ini
root = true

[*]
charset = utf-8
indent_style = space
indent_size = 2
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
```

## 🔍 Git配置

### .gitignore
```
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Production
build/
dist/
.next/
out/

# Misc
.DS_Store
*.log
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
```

### Git Hooks（使用husky）
```bash
# 安装husky
pnpm add -D husky

# 初始化
npx husky-init

# 添加pre-commit hook
echo "npx lint-staged" > .husky/pre-commit
```

#### lint-staged配置
```json
{
    "lint-staged": {
        "*.{js,jsx,ts,tsx}": [
            "eslint --fix",
            "prettier --write"
        ],
        "*.{css,scss,less}": [
            "prettier --write"
        ],
        "*.vue": [
            "eslint --fix",
            "prettier --write"
        ]
    }
}
```

## 🌐 纯HTML项目配置

### 快速启动

#### 方式1：Live Server（推荐）
```bash
# 安装live-server（全局）
npm install -g live-server

# 在项目目录启动
cd my-html-project
live-server

# 指定端口
live-server --port=8080

# 不自动打开浏览器
live-server --no-browser

# 使用npx（无需全局安装）
npx live-server
```

#### 方式2：http-server
```bash
# 安装
npm install -g http-server

# 启动
http-server
http-server -p 8080

# 使用npx
npx http-server
```

#### 方式3：Python SimpleHTTPServer
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### 方式4：Node.js serve
```bash
# 安装
npm install -g serve

# 启动
serve .
serve -p 5000

# 使用npx
npx serve
```

### 纯HTML项目结构
```
my-html-project/
├── index.html          # 主页
├── about.html          # 其他页面
├── css/
│   ├── style.css      # 样式文件
│   └── reset.css      # 重置样式
├── js/
│   ├── main.js        # 主JS文件
│   └── utils.js       # 工具函数
├── images/            # 图片资源
├── fonts/             # 字体文件
└── lib/               # 第三方库
    └── jquery.min.js
```

### VSCode纯HTML项目配置

#### .vscode/settings.json
```json
{
    "liveServer.settings.port": 5500,
    "liveServer.settings.root": "/",
    "liveServer.settings.CustomBrowser": "chrome",
    "liveServer.settings.AdvanceCustomBrowserCmdLine": "",
    "liveServer.settings.NoBrowser": false,
    "liveServer.settings.ignoreFiles": [
        ".vscode/**",
        "**/*.scss",
        "**/*.sass"
    ]
}
```

#### .vscode/launch.json（HTML调试）
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "打开 index.html",
            "file": "${workspaceFolder}/index.html"
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "使用Live Server调试",
            "url": "http://localhost:5500",
            "webRoot": "${workspaceFolder}",
            "preLaunchTask": "Start Live Server"
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "当前HTML文件",
            "file": "${file}"
        }
    ]
}
```

#### .vscode/tasks.json（HTML任务）
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start Live Server",
            "type": "shell",
            "command": "npx live-server --port=5500 --no-browser",
            "isBackground": true,
            "problemMatcher": {
                "pattern": {
                    "regexp": ".",
                    "file": 1,
                    "location": 2,
                    "message": 3
                },
                "background": {
                    "activeOnStart": true,
                    "beginsPattern": "Serving",
                    "endsPattern": "http://127.0.0.1:5500"
                }
            }
        },
        {
            "label": "Open in Browser",
            "type": "shell",
            "command": "open",
            "args": ["http://localhost:5500"],
            "windows": {
                "command": "start"
            },
            "linux": {
                "command": "xdg-open"
            }
        }
    ]
}
```

### 示例：完整的HTML模板
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="页面描述">
    <title>我的HTML项目</title>
    
    <!-- 重置样式 -->
    <link rel="stylesheet" href="css/reset.css">
    <!-- 主样式 -->
    <link rel="stylesheet" href="css/style.css">
    
    <!-- 图标 -->
    <link rel="icon" href="favicon.ico" type="image/x-icon">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="index.html">首页</a></li>
                <li><a href="about.html">关于</a></li>
                <li><a href="contact.html">联系</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <h1>欢迎</h1>
        <p>这是一个纯HTML项目模板</p>
    </main>
    
    <footer>
        <p>&copy; 2024 我的网站</p>
    </footer>
    
    <!-- JavaScript -->
    <script src="js/main.js"></script>
</body>
</html>
```

### 使用VSCode Live Server

1. **安装插件**
   - 在VSCode中搜索"Live Server"
   - 安装"Live Server by Ritwick Dey"

2. **启动方式**
   - 右键HTML文件 → "Open with Live Server"
   - 点击底部状态栏的"Go Live"按钮
   - 快捷键：`Alt + L, Alt + O`（Mac: `Cmd + L, Cmd + O`）

3. **停止服务器**
   - 点击底部状态栏的"Port: 5500"
   - 快捷键：`Alt + L, Alt + C`

4. **配置热重载**
   - 修改HTML/CSS/JS文件后自动刷新浏览器
   - 无需手动刷新

### 常见问题

#### 端口被占用
```bash
# 查看端口占用
lsof -i :5500  # Mac/Linux
netstat -ano | findstr :5500  # Windows

# 更换端口
live-server --port=8080
```

#### CORS问题
```bash
# live-server默认允许CORS
live-server --cors

# http-server需要指定
http-server --cors
```

#### 自动刷新不工作
- 检查浏览器控制台是否有WebSocket连接错误
- 确保没有浏览器插件阻止WebSocket
- 重启Live Server

## 📦 项目初始化

### React项目
```bash
# Vite + React
pnpm create vite my-react-app --template react-ts
cd my-react-app
pnpm install
pnpm dev

# Next.js
pnpm create next-app my-next-app
cd my-next-app
pnpm dev
```

### Vue项目
```bash
# Vite + Vue
pnpm create vue@latest my-vue-app
cd my-vue-app
pnpm install
pnpm dev

# Nuxt 3
pnpm dlx nuxi init my-nuxt-app
cd my-nuxt-app
pnpm install
pnpm dev
```

### 项目结构
```
my-project/
├── src/
│   ├── assets/         # 静态资源
│   ├── components/     # 组件
│   ├── hooks/          # 自定义Hooks
│   ├── utils/          # 工具函数
│   ├── types/          # TypeScript类型
│   ├── styles/         # 样式文件
│   ├── api/            # API接口
│   ├── store/          # 状态管理
│   ├── router/         # 路由配置
│   └── App.tsx         # 根组件
├── public/             # 公共资源
├── tests/              # 测试文件
├── .env                # 环境变量
├── .eslintrc.js        # ESLint配置
├── .prettierrc         # Prettier配置
├── tsconfig.json       # TypeScript配置
├── vite.config.ts      # Vite配置
└── package.json        # 项目配置
```

## 🌐 浏览器工具

### Chrome DevTools
- Elements：查看和修改DOM
- Console：调试JavaScript
- Sources：断点调试
- Network：网络请求监控
- Performance：性能分析
- Application：存储、缓存查看

### React DevTools
```bash
# Chrome扩展
# https://chrome.google.com/webstore/detail/react-developer-tools/

# 功能
- 组件树查看
- Props和State检查
- Profiler性能分析
```

### Vue DevTools
```bash
# Chrome扩展
# https://chrome.google.com/webstore/detail/vuejs-devtools/

# 功能
- 组件树查看
- Vuex状态管理
- 路由信息
- 性能分析
```

## 🛠️ 实用工具

### 在线工具
- **代码格式化**：[Prettier Playground](https://prettier.io/playground/)
- **正则测试**：[RegExr](https://regexr.com/)
- **包大小分析**：[Bundlephobia](https://bundlephobia.com/)
- **Can I Use**：[浏览器兼容性查询](https://caniuse.com/)
- **TypeScript Playground**：[在线TS编译](https://www.typescriptlang.org/play)

### 命令行工具
```bash
# 快速启动服务
npx serve dist

# 代码质量检查
npx eslint src/

# 依赖更新
npx npm-check-updates
npx npm-check-updates -u

# 包分析
npx depcheck        # 检查未使用依赖
npx size-limit      # 包大小限制
```

## 💡 最佳实践

### 1. 版本管理
- 使用nvm管理Node版本
- 在项目中指定Node版本（.nvmrc）
- 锁定依赖版本（package-lock.json）

### 2. 代码规范
- 统一使用ESLint + Prettier
- 配置编辑器自动格式化
- 使用Git Hooks强制检查

### 3. 环境变量
```bash
# .env.development
VITE_API_URL=http://localhost:3000
VITE_APP_TITLE=My App (Dev)

# .env.production
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App
```

### 4. TypeScript配置
```json
{
    "compilerOptions": {
        "target": "ES2020",
        "module": "ESNext",
        "lib": ["ES2020", "DOM", "DOM.Iterable"],
        "jsx": "react-jsx",
        "strict": true,
        "moduleResolution": "bundler",
        "esModuleInterop": true,
        "skipLibCheck": true,
        "baseUrl": ".",
        "paths": {
            "@/*": ["src/*"]
        }
    },
    "include": ["src"],
    "exclude": ["node_modules"]
}
```

## 📚 参考资料
- [Node.js官网](https://nodejs.org/)
- [pnpm文档](https://pnpm.io/)
- [VSCode文档](https://code.visualstudio.com/docs)
- [ESLint规则](https://eslint.org/docs/rules/)
- [Prettier配置](https://prettier.io/docs/en/options.html)


