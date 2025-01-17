# Electron.01.快速入门

Electron基于Chromium和Node.js，用Web技术构建跨平台桌面应用。GitHub于2013年发布，VS Code、Slack、Discord等应用都基于Electron。

## Electron架构

### 双进程模型

```
┌─────────────────────────────┐
│      主进程 (Main)          │
│    - Node.js完整API         │
│    - 创建窗口               │
│    - 生命周期管理           │
│    - 原生功能               │
└──────────┬──────────────────┘
           │ IPC通信
    ┌──────┴───────┬───────────┐
    │              │           │
┌───▼───┐   ┌─────▼─┐   ┌────▼──┐
│渲染进程│   │渲染进程│   │渲染进程│
│(网页1)│   │(网页2)│   │(网页3)│
└───────┘   └───────┘   └───────┘
```

**主进程（Main Process）：**
- 每个Electron应用只有一个
- 运行package.json的main脚本
- 可以创建多个BrowserWindow
- 可访问Node.js所有API
- 管理应用生命周期

**渲染进程（Renderer Process）：**
- 每个BrowserWindow一个渲染进程
- 运行网页代码（HTML/CSS/JS）
- 受限的Node.js API（需启用）
- 通过IPC与主进程通信

## 环境搭建

### 安装

```bash
# 创建项目
mkdir my-electron-app && cd my-electron-app
npm init -y

# 安装Electron
npm install --save-dev electron
```

### package.json

```json
{
  "name": "my-electron-app",
  "version": "1.0.0",
  "description": "My Electron App",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  },
  "devDependencies": {
    "electron": "^28.0.0"
  }
}
```

### Hello World

**main.js（主进程）：**
```javascript
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,  // 安全：禁用Node集成
            contextIsolation: true   // 安全：上下文隔离
        }
    });

    win.loadFile('index.html');
    
    // 开发工具
    // win.webContents.openDevTools();
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
```

**index.html（渲染进程）：**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hello Electron</title>
    <meta http-equiv="Content-Security-Policy" 
          content="default-src 'self'; script-src 'self'">
</head>
<body>
    <h1>Hello Electron!</h1>
    <button id="btn">Click Me</button>
    
    <script src="renderer.js"></script>
</body>
</html>
```

**renderer.js：**
```javascript
document.getElementById('btn').addEventListener('click', () => {
    alert('Button clicked!');
});
```

**preload.js（预加载脚本）：**
```javascript
const { contextBridge, ipcRenderer } = require('electron');

// 暴露安全的API到渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
    sendMessage: (message) => ipcRenderer.send('message', message),
    onReply: (callback) => ipcRenderer.on('reply', callback)
});
```

### 运行

```bash
npm start
```

## 窗口管理

### BrowserWindow选项

```javascript
const win = new BrowserWindow({
    // 尺寸
    width: 1000,
    height: 800,
    minWidth: 600,
    minHeight: 400,
    
    // 位置
    x: 100,
    y: 100,
    center: true,
    
    // 外观
    title: 'My App',
    icon: 'icon.png',
    frame: false,          // 无边框
    transparent: true,     // 透明
    resizable: true,       // 可调整大小
    movable: true,
    minimizable: true,
    maximizable: true,
    closable: true,
    
    // 显示
    show: false,           // 创建时不显示
    alwaysOnTop: false,    // 置顶
    fullscreen: false,     // 全屏
    kiosk: false,          // kiosk模式
    
    // 其他
    backgroundColor: '#fff',
    hasShadow: true,
    parent: null,          // 父窗口
    modal: false           // 模态窗口
});

// ready-to-show事件（避免闪烁）
win.once('ready-to-show', () => {
    win.show();
});
```

### 窗口方法

```javascript
// 显示/隐藏
win.show();
win.hide();

// 最大化/最小化
win.maximize();
win.minimize();
win.restore();

// 全屏
win.setFullScreen(true);

// 关闭
win.close();

// 加载URL
win.loadURL('https://example.com');
win.loadFile('index.html');

// 重新加载
win.reload();

// 打开开发者工具
win.webContents.openDevTools();
win.webContents.closeDevTools();
```

### 窗口事件

```javascript
// 最小化
win.on('minimize', () => {
    console.log('Window minimized');
});

// 最大化
win.on('maximize', () => {
    console.log('Window maximized');
});

// 关闭前
win.on('close', (event) => {
    event.preventDefault();  // 阻止关闭
    // 确认对话框
});

// 关闭后
win.on('closed', () => {
    win = null;
});

// 焦点
win.on('focus', () => {
    console.log('Window focused');
});

win.on('blur', () => {
    console.log('Window blurred');
});
```

## 应用生命周期

### 应用事件

```javascript
const { app } = require('electron');

// 准备完成
app.whenReady().then(() => {
    createWindow();
});

// 所有窗口关闭
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// 激活（macOS）
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// 退出前
app.on('before-quit', (event) => {
    // 清理工作
});

// 退出
app.on('will-quit', (event) => {
    event.preventDefault();
    // 最后的清理
});

// 退出完成
app.on('quit', () => {
    console.log('App quit');
});
```

## 菜单

### 应用菜单

```javascript
const { Menu } = require('electron');

const template = [
    {
        label: 'File',
        submenu: [
            {
                label: 'Open',
                accelerator: 'CmdOrCtrl+O',
                click: () => {
                    // 打开文件
                }
            },
            {
                label: 'Save',
                accelerator: 'CmdOrCtrl+S',
                click: () => {
                    // 保存文件
                }
            },
            { type: 'separator' },
            {
                label: 'Exit',
                role: 'quit'
            }
        ]
    },
    {
        label: 'Edit',
        submenu: [
            { role: 'undo' },
            { role: 'redo' },
            { type: 'separator' },
            { role: 'cut' },
            { role: 'copy' },
            { role: 'paste' }
        ]
    },
    {
        label: 'View',
        submenu: [
            { role: 'reload' },
            { role: 'forceReload' },
            { role: 'toggleDevTools' },
            { type: 'separator' },
            { role: 'resetZoom' },
            { role: 'zoomIn' },
            { role: 'zoomOut' },
            { type: 'separator' },
            { role: 'togglefullscreen' }
        ]
    }
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);
```

### 右键菜单

```javascript
// 渲染进程
window.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    window.electronAPI.showContextMenu();
});

// 主进程
const { Menu, ipcMain } = require('electron');

ipcMain.on('show-context-menu', (event) => {
    const template = [
        { label: 'Copy', role: 'copy' },
        { label: 'Paste', role: 'paste' },
        { type: 'separator' },
        { label: 'Custom Action', click: () => {} }
    ];
    
    const menu = Menu.buildFromTemplate(template);
    menu.popup(BrowserWindow.fromWebContents(event.sender));
});
```

## 托盘图标

```javascript
const { Tray, Menu } = require('electron');

let tray = null;

app.whenReady().then(() => {
    tray = new Tray('icon.png');
    
    const contextMenu = Menu.buildFromTemplate([
        { label: 'Show App', click: () => { win.show(); } },
        { label: 'Quit', role: 'quit' }
    ]);
    
    tray.setToolTip('My App');
    tray.setContextMenu(contextMenu);
    
    // 点击托盘
    tray.on('click', () => {
        win.isVisible() ? win.hide() : win.show();
    });
});
```

**核心：** Electron双进程架构，主进程管理应用和窗口，渲染进程运行网页，IPC实现进程间通信。

