# 客户端开发学习路径

跨平台客户端开发技术栈，涵盖Qt、Electron、CEF等主流框架。

## 学习时间线

### Qt阶段（2020年）

**2020-05 到 2020-06（2个月）**
- Qt环境搭建、Qt Creator
- 信号与槽机制
- QtWidgets控件和布局

### Electron阶段（2025年）

**2025-01 到 2025-02（2个月）**
- Electron环境搭建
- 双进程架构
- IPC进程通信

### CEF阶段（2025年）

**2025-03（1个月）**
- CEF架构原理
- JavaScript交互
- 多进程模型

### Flutter阶段（2025年）

**2025-05（1个月）**
- Flutter桌面开发
- Widget系统
- 平台集成

## 学习文档

### Qt（2020）
1. **Qt.01.环境搭建.md** - Qt安装、Qt Creator、项目配置
2. **Qt.02.信号与槽.md** - 信号槽机制、连接方式、跨线程通信
3. **Qt.03.QtWidgets基础.md** - 控件、布局、对话框、Model/View

### Electron（2025）
1. **Electron.01.快速入门.md** - 环境搭建、双进程模型、窗口管理
2. **Electron.02.进程通信.md** - IPC通信、contextBridge、原生对话框

### CEF（2025）
1. **CEF.01.架构与集成.md** - CEF架构、CMake集成、JavaScript交互

### Flutter（2025）
1. **Flutter.01.桌面开发.md** - Flutter环境、Widget、状态管理、平台集成

## 技术对比

| 框架 | 语言 | 包体积 | 性能 | 开发效率 | 适用场景 |
|------|------|--------|------|----------|----------|
| **Qt** | C++ | 中 | 优秀 | 中等 | 原生应用、嵌入式 |
| **Electron** | JavaScript | 大 | 良好 | 高 | 快速开发、Web技术栈 |
| **CEF** | C++ | 可定制 | 优秀 | 低 | 性能敏感、自定义浏览器 |
| **Flutter** | Dart | 中 | 优秀 | 高 | 跨平台一致UI、移动+桌面 |

## 核心特性

### Qt特性
- **跨平台**：一次编写，多平台编译
- **信号槽**：对象间松耦合通信
- **QML**：声明式UI语言
- **丰富组件**：GUI、网络、数据库、多媒体
- **原生性能**：C++实现，接近系统级

### Electron特性
- **Web技术**：HTML/CSS/JavaScript
- **双进程**：主进程+渲染进程
- **Node.js集成**：完整npm生态
- **跨平台**：单一代码库
- **自动更新**：electron-updater

### CEF特性
- **Chromium内核**：完整浏览器功能
- **多进程**：Browser/Renderer/GPU进程
- **C++ API**：精细控制
- **离屏渲染**：OSR模式
- **性能优秀**：接近原生浏览器

### Flutter特性
- **单一代码库**：6个平台（iOS/Android/Web/Windows/macOS/Linux）
- **热重载**：秒级UI更新
- **自绘引擎**：Skia渲染，60fps
- **Widget树**：声明式UI
- **Dart语言**：JIT开发+AOT发布

## 应用场景

### Qt适用
- 性能要求高的桌面应用
- 嵌入式系统界面
- 跨平台原生应用
- 需要硬件集成的应用

### Electron适用
- Web开发团队快速构建桌面应用
- 需要丰富npm生态
- 跨平台一致性要求高
- 快速迭代的产品

### CEF适用
- 游戏内置浏览器
- 需要自定义浏览器功能
- 性能敏感的Web渲染
- C++项目集成浏览器

### Flutter适用
- 移动端和桌面端统一UI
- 需要漂亮的自定义UI
- 快速原型开发
- 跨平台一致性要求高

## 打包分发

### Qt
```bash
# Windows
windeployqt.exe app.exe

# macOS
macdeployqt app.app

# Linux
linuxdeployqt app
```

### Electron
```bash
npm install --save-dev electron-builder

# package.json
{
  "build": {
    "appId": "com.example.app",
    "mac": {
      "category": "public.app-category.utilities"
    },
    "win": {
      "target": "nsis"
    },
    "linux": {
      "target": "AppImage"
    }
  }
}

# 打包
npm run build
```

### CEF
- 复制Release/Debug目录下的文件
- 包含libcef.dll/.so/.dylib
- Resources目录
- locales目录

### Flutter
```bash
# Windows
flutter build windows --release

# macOS
flutter build macos --release

# Linux
flutter build linux --release
```

## 学习资源

### Qt
- Qt官方文档：https://doc.qt.io
- Qt Creator IDE
- Qt Examples

### Electron
- Electron官网：https://www.electronjs.org
- Electron Fiddle（在线试验）
- electron-quick-start

### CEF
- CEF官网：https://bitbucket.org/chromiumembedded/cef
- CEF Forum
- cefclient示例

### Flutter
- Flutter官网：https://flutter.dev
- Flutter桌面文档：https://docs.flutter.dev/desktop
- Flutter Samples
- pub.dev（Dart包仓库）

## 最佳实践

### Qt
- 使用信号槽而非直接调用
- QObject父子关系管理内存
- Model/View分离数据和界面
- QML用于现代UI

### Electron
- contextBridge安全暴露API
- 禁用nodeIntegration
- 启用contextIsolation
- 使用IPC通信

### CEF
- 正确管理进程生命周期
- 使用CefRefPtr管理对象
- 注意线程安全（CefPostTask）
- 合理使用离屏渲染

### Flutter
- 使用const构造函数优化性能
- Provider管理状态
- 桌面端适配响应式布局
- Method Channel调用原生功能
- 避免Widget树过深

**核心：** Qt原生性能优秀，Electron开发效率高，CEF提供精细控制，Flutter跨平台UI一致性强。根据项目需求选择合适框架。
