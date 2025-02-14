# Electron.02.进程通信

Electron通过IPC（Inter-Process Communication）实现主进程和渲染进程间通信。

## IPC通信方式

### 渲染进程 → 主进程

**单向发送（ipcRenderer.send）：**

```javascript
// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    sendMessage: (msg) => ipcRenderer.send('message', msg)
});

// renderer.js
document.getElementById('btn').addEventListener('click', () => {
    window.electronAPI.sendMessage('Hello from renderer');
});

// main.js
const { ipcMain } = require('electron');

ipcMain.on('message', (event, msg) => {
    console.log('Received:', msg);
});
```

**请求-响应（ipcRenderer.invoke）：**

```javascript
// preload.js
contextBridge.exposeInMainWorld('electronAPI', {
    getData: () => ipcRenderer.invoke('get-data')
});

// renderer.js
const button = document.getElementById('btn');
button.addEventListener('click', async () => {
    const data = await window.electronAPI.getData();
    console.log('Data:', data);
});

// main.js
ipcMain.handle('get-data', async (event) => {
    return { name: 'Alice', age: 25 };
});
```

### 主进程 → 渲染进程

```javascript
// main.js
const { BrowserWindow } = require('electron');

const win = BrowserWindow.getAllWindows()[0];

// 发送消息
win.webContents.send('update', { count: 10 });

// preload.js
contextBridge.exposeInMainWorld('electronAPI', {
    onUpdate: (callback) => ipcRenderer.on('update', callback)
});

// renderer.js
window.electronAPI.onUpdate((event, data) => {
    console.log('Update:', data);
});
```

### 渲染进程间通信

```javascript
// 通过主进程中转
// renderer1.js
window.electronAPI.sendToOther({ message: 'Hello' });

// main.js
ipcMain.on('send-to-other', (event, data) => {
    const allWindows = BrowserWindow.getAllWindows();
    allWindows.forEach(win => {
        if (win.webContents !== event.sender) {
            win.webContents.send('message-from-other', data);
        }
    });
});

// renderer2.js
window.electronAPI.onMessageFromOther((event, data) => {
    console.log('Received:', data);
});
```

## contextBridge

### 安全暴露API

```javascript
// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    // 文件操作
    readFile: (path) => ipcRenderer.invoke('read-file', path),
    writeFile: (path, data) => ipcRenderer.invoke('write-file', path, data),
    
    // 对话框
    showOpenDialog: () => ipcRenderer.invoke('show-open-dialog'),
    
    // 系统信息
    getSystemInfo: () => ipcRenderer.invoke('get-system-info'),
    
    // 事件监听
    onProgress: (callback) => {
        ipcRenderer.on('progress', (event, value) => callback(value));
    }
});

// main.js
const fs = require('fs').promises;
const { dialog } = require('electron');
const os = require('os');

ipcMain.handle('read-file', async (event, path) => {
    return await fs.readFile(path, 'utf8');
});

ipcMain.handle('write-file', async (event, path, data) => {
    await fs.writeFile(path, data);
    return { success: true };
});

ipcMain.handle('show-open-dialog', async (event) => {
    const result = await dialog.showOpenDialog({
        properties: ['openFile'],
        filters: [
            { name: 'Text Files', extensions: ['txt'] },
            { name: 'All Files', extensions: ['*'] }
        ]
    });
    return result.filePaths;
});

ipcMain.handle('get-system-info', () => {
    return {
        platform: process.platform,
        arch: process.arch,
        cpus: os.cpus().length,
        memory: os.totalmem()
    };
});
```

## 原生对话框

### 文件对话框

```javascript
const { dialog } = require('electron');

// 打开文件
const result = await dialog.showOpenDialog({
    properties: ['openFile', 'multiSelections'],
    filters: [
        { name: 'Images', extensions: ['jpg', 'png', 'gif'] },
        { name: 'Videos', extensions: ['mkv', 'avi', 'mp4'] },
        { name: 'All Files', extensions: ['*'] }
    ],
    defaultPath: app.getPath('documents')
});

if (!result.canceled) {
    console.log('Selected files:', result.filePaths);
}

// 保存文件
const result = await dialog.showSaveDialog({
    defaultPath: 'untitled.txt',
    filters: [
        { name: 'Text Files', extensions: ['txt'] }
    ]
});

if (!result.canceled) {
    fs.writeFileSync(result.filePath, content);
}
```

### 消息框

```javascript
// 信息框
dialog.showMessageBox({
    type: 'info',
    title: 'Information',
    message: 'This is an info message',
    buttons: ['OK']
});

// 错误框
dialog.showErrorBox('Error', 'Something went wrong');

// 确认框
const result = await dialog.showMessageBox({
    type: 'question',
    buttons: ['Yes', 'No', 'Cancel'],
    title: 'Confirm',
    message: 'Do you want to save changes?',
    defaultId: 0,
    cancelId: 2
});

if (result.response === 0) {
    // Yes
} else if (result.response === 1) {
    // No
}
```

## 实战案例：文件编辑器

**main.js：**
```javascript
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const fs = require('fs').promises;

let mainWindow;
let currentFile = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 900,
        height: 700,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true
        }
    });

    mainWindow.loadFile('index.html');
}

// 打开文件
ipcMain.handle('open-file', async () => {
    const result = await dialog.showOpenDialog({
        properties: ['openFile'],
        filters: [{ name: 'Text', extensions: ['txt', 'md'] }]
    });

    if (!result.canceled) {
        const filePath = result.filePaths[0];
        const content = await fs.readFile(filePath, 'utf8');
        currentFile = filePath;
        return { filePath, content };
    }
    
    return null;
});

// 保存文件
ipcMain.handle('save-file', async (event, content) => {
    if (currentFile) {
        await fs.writeFile(currentFile, content);
        return { success: true };
    } else {
        const result = await dialog.showSaveDialog({
            filters: [{ name: 'Text', extensions: ['txt'] }]
        });
        
        if (!result.canceled) {
            await fs.writeFile(result.filePath, content);
            currentFile = result.filePath;
            return { success: true };
        }
    }
    
    return { success: false };
});

app.whenReady().then(createWindow);
```

**preload.js：**
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('fileAPI', {
    openFile: () => ipcRenderer.invoke('open-file'),
    saveFile: (content) => ipcRenderer.invoke('save-file', content)
});
```

**renderer.js：**
```javascript
const textarea = document.getElementById('editor');
const openBtn = document.getElementById('open');
const saveBtn = document.getElementById('save');

openBtn.addEventListener('click', async () => {
    const result = await window.fileAPI.openFile();
    if (result) {
        textarea.value = result.content;
        document.title = result.filePath;
    }
});

saveBtn.addEventListener('click', async () => {
    const content = textarea.value;
    const result = await window.fileAPI.saveFile(content);
    if (result.success) {
        alert('File saved');
    }
});
```

**核心：** IPC通过contextBridge安全暴露API，主进程和渲染进程通过事件或invoke/handle模式通信。

