# VS Code 代码编辑器

## 核心功能
- **智能代码补全**：基于AI的代码建议和自动完成
- **调试支持**：内置调试器，支持多种语言
- **Git集成**：内置Git支持，可视化版本控制
- **扩展生态**：丰富的插件系统
- **多语言支持**：支持几乎所有编程语言

## 基础操作
```bash
# 命令行启动
code .                       # 打开当前目录
code file.txt               # 打开指定文件
code -n file.txt            # 在新窗口中打开
code -r file.txt            # 在现有窗口中打开
code --diff file1 file2     # 比较两个文件
code --wait file.txt        # 等待文件关闭后返回

# 工作区操作
code -w project/           # 打开工作区
code --new-window          # 新窗口
code --reuse-window        # 重用窗口
code --goto file:line:column # 跳转到指定位置
```

## 快捷键速查
```bash
# 文件操作
Ctrl+N                      # 新建文件
Ctrl+O                      # 打开文件
Ctrl+S                      # 保存文件
Ctrl+Shift+S               # 另存为
Ctrl+W                      # 关闭文件
Ctrl+Shift+T               # 重新打开关闭的文件

# 编辑操作
Ctrl+Z                      # 撤销
Ctrl+Y                      # 重做
Ctrl+X                      # 剪切
Ctrl+C                      # 复制
Ctrl+V                      # 粘贴
Ctrl+A                      # 全选
Ctrl+D                      # 选择下一个相同单词
Ctrl+Shift+L               # 选择所有相同单词

# 查找替换
Ctrl+F                      # 查找
Ctrl+H                      # 替换
Ctrl+Shift+F               # 全局查找
Ctrl+Shift+H               # 全局替换
F3                         # 查找下一个
Shift+F3                   # 查找上一个

# 导航
Ctrl+G                      # 跳转到行
Ctrl+P                      # 快速打开文件
Ctrl+Shift+P               # 命令面板
Ctrl+`                      # 打开终端
Ctrl+Shift+`               # 新建终端
```

## 多光标编辑
```bash
# 多光标操作
Alt+Click                   # 添加光标
Ctrl+Alt+Up/Down           # 上下添加光标
Ctrl+Shift+L               # 选择所有相同单词
Ctrl+F2                    # 选择所有相同单词
Shift+Alt+I                # 在每行末尾添加光标
Ctrl+U                      # 撤销光标操作
```

## 代码折叠
```bash
# 折叠操作
Ctrl+Shift+[               # 折叠代码块
Ctrl+Shift+]               # 展开代码块
Ctrl+K Ctrl+0              # 折叠所有
Ctrl+K Ctrl+J              # 展开所有
Ctrl+K Ctrl+1              # 折叠第1级
Ctrl+K Ctrl+2              # 折叠第2级
```

## 分屏和布局
```bash
# 分屏操作
Ctrl+\                      # 分割编辑器
Ctrl+1/2/3                 # 切换到第1/2/3个编辑器
Ctrl+Shift+PgUp/PgDown     # 移动编辑器
Ctrl+K Ctrl+Left/Right     # 移动编辑器组
Ctrl+K Ctrl+W              # 关闭所有编辑器
Ctrl+K Ctrl+Shift+W        # 关闭所有编辑器组
```

## Git集成
```bash
# Git操作
Ctrl+Shift+G               # 打开源代码管理
Ctrl+Enter                 # 提交更改
Ctrl+Shift+Enter           # 提交并推送
Ctrl+Shift+P, Git: Add    # 添加文件
Ctrl+Shift+P, Git: Commit # 提交更改
Ctrl+Shift+P, Git: Push   # 推送更改
Ctrl+Shift+P, Git: Pull   # 拉取更改

# Git快捷键
Alt+Left/Right             # 在更改间导航
Ctrl+Shift+P, Git: Checkout # 切换分支
Ctrl+Shift+P, Git: Merge  # 合并分支
```

## 调试功能
```bash
# 调试操作
F5                         # 开始调试
F9                         # 切换断点
F10                        # 单步跳过
F11                        # 单步进入
Shift+F11                  # 单步跳出
Ctrl+Shift+F5              # 重启调试
Shift+F5                   # 停止调试
Ctrl+Shift+F5              # 重启调试会话
```

## 终端集成
```bash
# 终端操作
Ctrl+`                      # 切换终端
Ctrl+Shift+`               # 新建终端
Ctrl+Shift+C               # 复制终端内容
Ctrl+Shift+V               # 粘贴到终端
Ctrl+Up/Down               # 滚动终端
Ctrl+PageUp/PageDown       # 切换终端标签
```

## 扩展管理
```bash
# 扩展操作
Ctrl+Shift+X               # 打开扩展面板
Ctrl+Shift+P, Extensions: Install # 安装扩展
Ctrl+Shift+P, Extensions: Uninstall # 卸载扩展
Ctrl+Shift+P, Extensions: Enable # 启用扩展
Ctrl+Shift+P, Extensions: Disable # 禁用扩展
```

## 设置和配置
```bash
# 设置操作
Ctrl+,                     # 打开设置
Ctrl+Shift+P, Preferences: Open Settings # 打开设置
Ctrl+Shift+P, Preferences: Open Keyboard Shortcuts # 键盘快捷键
Ctrl+Shift+P, Preferences: Open User Settings # 用户设置
Ctrl+Shift+P, Preferences: Open Workspace Settings # 工作区设置
```

## 工作区管理
```bash
# 工作区操作
Ctrl+K Ctrl+O             # 打开文件夹
Ctrl+K Ctrl+S             # 保存工作区
Ctrl+K Ctrl+A             # 添加文件夹到工作区
Ctrl+K Ctrl+R             # 重新加载窗口
Ctrl+K Ctrl+W             # 关闭工作区
```

## 代码格式化
```bash
# 格式化操作
Shift+Alt+F               # 格式化文档
Ctrl+K Ctrl+F             # 格式化选中内容
Ctrl+Shift+P, Format Document # 格式化文档
Ctrl+Shift+P, Format Selection # 格式化选中内容
```

## 智能功能
```bash
# 代码补全
Ctrl+Space                # 触发建议
Ctrl+Shift+Space         # 触发参数提示
Ctrl+I                    # 触发建议
Tab                       # 接受建议
Esc                       # 关闭建议

# 重构操作
F2                        # 重命名符号
Ctrl+Shift+R             # 重构菜单
Ctrl+.                    # 快速修复
Ctrl+Shift+.              # 显示修复建议
```

## 文件管理
```bash
# 文件操作
Ctrl+Shift+E              # 打开资源管理器
Ctrl+K Ctrl+R             # 显示文件路径
Ctrl+K Ctrl+P             # 复制文件路径
Ctrl+K Ctrl+O             # 在文件管理器中显示
Ctrl+K Ctrl+N             # 新建文件夹
Ctrl+K Ctrl+Delete        # 删除文件
```

## 搜索功能
```bash
# 搜索操作
Ctrl+Shift+F              # 全局搜索
Ctrl+Shift+J              # 切换搜索详细信息
Ctrl+Shift+C              # 切换大小写敏感
Ctrl+Shift+R              # 切换正则表达式
Ctrl+Shift+W              # 切换全词匹配
```

## 代码导航
```bash
# 导航操作
Ctrl+T                    # 转到符号
Ctrl+Shift+O             # 转到文件中的符号
Ctrl+G                    # 转到行
Ctrl+P                    # 快速打开
Ctrl+Shift+P             # 命令面板
F12                       # 转到定义
Alt+F12                   # 查看定义
Shift+F12                 # 查看引用
```

## 实用扩展推荐
```bash
# 必装扩展
GitLens                    # Git增强
Prettier                   # 代码格式化
ESLint                     # JavaScript代码检查
Python                     # Python支持
Thunder Client             # API测试
Live Server                # 本地服务器
Bracket Pair Colorizer     # 括号配对着色
Auto Rename Tag            # 自动重命名标签
Path Intellisense          # 路径智能提示
Material Icon Theme        # 图标主题
```

## 配置文件
```json
// settings.json
{
    "editor.fontSize": 14,
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true
    },
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "terminal.integrated.fontSize": 14,
    "git.enableSmartCommit": true,
    "git.confirmSync": false,
    "workbench.colorTheme": "Material Theme",
    "workbench.iconTheme": "material-icon-theme"
}
```

```json
// keybindings.json
[
    {
        "key": "ctrl+shift+f",
        "command": "workbench.action.findInFiles"
    },
    {
        "key": "ctrl+shift+h",
        "command": "workbench.action.replaceInFiles"
    },
    {
        "key": "ctrl+shift+`",
        "command": "workbench.action.terminal.new"
    }
]
```

## 调试配置
```json
// launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Node.js",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/app.js",
            "console": "integratedTerminal"
        },
        {
            "name": "Attach to Process",
            "type": "node",
            "request": "attach",
            "port": 9229
        },
        {
            "name": "Launch Python",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```

## 任务配置
```json
// tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "npm install",
            "type": "shell",
            "command": "npm install",
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "npm start",
            "type": "shell",
            "command": "npm start",
            "group": "build",
            "isBackground": true
        }
    ]
}
```

## 代码片段
```json
// snippets/javascript.json
{
    "Console Log": {
        "prefix": "cl",
        "body": [
            "console.log('$1');"
        ],
        "description": "Console log"
    },
    "Function": {
        "prefix": "fn",
        "body": [
            "function ${1:name}(${2:params}) {",
            "    $3",
            "}"
        ],
        "description": "Function declaration"
    }
}
```

## 工作区配置
```json
// .vscode/settings.json
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true
    },
    "files.exclude": {
        "**/node_modules": true,
        "**/.git": true,
        "**/.DS_Store": true
    },
    "search.exclude": {
        "**/node_modules": true,
        "**/dist": true
    }
}
```

## 实用技巧
```bash
# 快速打开最近文件
Ctrl+R                      # 打开最近文件
Ctrl+Shift+P, File: Open Recent # 打开最近文件菜单

# 快速切换标签
Ctrl+Tab                    # 切换标签
Ctrl+PageUp/PageDown        # 切换标签

# 快速选择
Ctrl+L                      # 选择当前行
Ctrl+Shift+K                # 删除当前行
Ctrl+Shift+Up/Down          # 移动行
Alt+Up/Down                 # 移动行
```

## 性能优化
```bash
# 禁用不需要的功能
"editor.minimap.enabled": false
"editor.suggest.enabled": false
"editor.quickSuggestions": false
"editor.parameterHints.enabled": false

# 文件监控排除
"files.watcherExclude": {
    "**/node_modules/**": true,
    "**/dist/**": true
}

# 搜索排除
"search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.git": true
}
```

