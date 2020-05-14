# Qt.01.环境搭建

Qt是跨平台C++图形用户界面应用程序开发框架，1991年由Qt Company开发。支持Windows、Linux、macOS、Android、iOS等平台。

## Qt简介

### 核心特性

- **跨平台**：一次编写，多平台运行
- **C++框架**：性能优秀，接近原生
- **信号与槽**：对象间通信机制
- **QML**：声明式UI语言
- **丰富组件**：GUI控件、网络、数据库、多媒体

### 应用场景

**桌面应用：**
- 办公软件
- 图形设计工具
- 开发工具（Qt Creator）
- 多媒体播放器

**嵌入式：**
- 车载系统
- 工控界面
- 医疗设备

**移动应用：**
- iOS/Android应用

### 知名应用

- VirtualBox（虚拟机）
- OBS Studio（直播录屏）
- Telegram Desktop（即时通讯）
- Autodesk Maya（3D建模）

## 环境安装

### Qt版本选择

```
Qt 5.15 LTS（长期支持）
Qt 6.x（最新版，性能提升）
```

### 安装方式

**在线安装器（推荐）：**
```bash
# 下载：https://www.qt.io/download

# Linux
chmod +x qt-unified-linux-x64-online.run
./qt-unified-linux-x64-online.run

# macOS
# 打开.dmg文件安装

# Windows
# 运行.exe安装程序
```

**选择组件：**
- Qt 5.15.2 或 Qt 6.x
- Qt Creator IDE
- MinGW（Windows）/ GCC（Linux）/ Clang（macOS）
- Qt Charts、Qt WebEngine（可选）

### 命令行安装

```bash
# Ubuntu/Debian
sudo apt install qt5-default qtcreator

# macOS
brew install qt@5
brew install qt-creator

# 环境变量
export PATH="/usr/local/opt/qt@5/bin:$PATH"
```

## Qt Creator

### 界面布局

```
┌─────────────────────────────────────┐
│ 菜单栏                              │
├──────┬──────────────────────────────┤
│      │                              │
│ 侧边栏│        编辑器区域            │
│      │                              │
│ 项目 │                              │
│ 文件 │                              │
│      │                              │
├──────┴──────────────────────────────┤
│ 输出窗口（编译信息、应用输出）      │
└─────────────────────────────────────┘
```

### 快捷键

```
Ctrl+B         编译
Ctrl+R         运行
F5             调试
Ctrl+Shift+F   全局搜索
Ctrl+K         文件定位
F2             重命名
F4             头文件/源文件切换
Ctrl+/         注释
Ctrl+Space     代码补全
```

## Hello World

### 创建项目

```
Qt Creator → 新建项目 → Qt Widgets Application
项目名称：HelloQt
基类：QMainWindow
```

**生成文件：**
```
HelloQt/
├── HelloQt.pro      # 项目配置
├── main.cpp         # 程序入口
├── mainwindow.h     # 主窗口头文件
├── mainwindow.cpp   # 主窗口实现
└── mainwindow.ui    # UI设计文件
```

### main.cpp

```cpp
#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);  // 应用程序对象
    MainWindow w;                // 主窗口
    w.show();                    // 显示窗口
    return a.exec();             // 事件循环
}
```

### mainwindow.h

```cpp
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT  // 必须宏，启用信号槽

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
```

### mainwindow.cpp

```cpp
#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}
```

## .pro文件

### 项目配置

```pro
# HelloQt.pro
QT       += core gui widgets  # 依赖模块

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = HelloQt              # 目标名称
TEMPLATE = app                # 应用程序模板

CONFIG += c++17               # C++标准

# 定义宏
DEFINES += QT_DEPRECATED_WARNINGS

# 源文件
SOURCES += \
    main.cpp \
    mainwindow.cpp

# 头文件
HEADERS += \
    mainwindow.h

# UI文件
FORMS += \
    mainwindow.ui

# 资源文件
RESOURCES += \
    resources.qrc

# 翻译文件
TRANSLATIONS += \
    HelloQt_zh_CN.ts

# 平台特定配置
win32 {
    # Windows配置
}

unix:!macx {
    # Linux配置
}

macx {
    # macOS配置
}
```

## qmake构建

### 命令行构建

```bash
# 生成Makefile
qmake HelloQt.pro

# 编译
make

# 运行
./HelloQt

# 清理
make clean

# Debug/Release
qmake CONFIG+=debug
qmake CONFIG+=release
```

### CMake构建（Qt 6推荐）

```cmake
cmake_minimum_required(VERSION 3.16)
project(HelloQt VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)  # MOC
set(CMAKE_AUTORCC ON)  # RCC
set(CMAKE_AUTOUIC ON)  # UIC

find_package(Qt6 REQUIRED COMPONENTS Core Widgets)

add_executable(HelloQt
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
)

target_link_libraries(HelloQt PRIVATE Qt6::Core Qt6::Widgets)
```

```bash
# 构建
mkdir build && cd build
cmake ..
make
```

## Qt模块

### 常用模块

```pro
# 核心
QT += core        # 核心类
QT += gui         # GUI基础
QT += widgets     # 桌面控件

# 网络
QT += network     # 网络编程

# 数据库
QT += sql         # SQL数据库

# 多媒体
QT += multimedia  # 音视频

# Web
QT += webenginewidgets  # Chromium内核

# QML
QT += qml quick   # QML/Qt Quick

# 其他
QT += xml         # XML解析
QT += concurrent  # 多线程
QT += printsupport # 打印
```

## Qt Assistant

### 帮助文档

```bash
# 启动Qt Assistant
assistant

# 常用文档
- Qt Widgets C++ Classes
- Qt Core C++ Classes
- Qt GUI C++ Classes
```

### 在线资源

- Qt官方文档：https://doc.qt.io
- Qt Wiki：https://wiki.qt.io
- Qt论坛：https://forum.qt.io

## 调试配置

### Qt Creator调试

```
断点：点击行号左侧
调试：F5启动
单步：F10（step over）、F11（step into）
变量：鼠标悬停或调试窗口
```

### 输出调试信息

```cpp
#include <QDebug>

qDebug() << "Debug message";
qInfo() << "Info message";
qWarning() << "Warning message";
qCritical() << "Critical message";

// 输出变量
int x = 42;
qDebug() << "x =" << x;

// 自定义类型输出
class Point {
public:
    int x, y;
};

QDebug operator<<(QDebug debug, const Point &p) {
    debug << "Point(" << p.x << "," << p.y << ")";
    return debug;
}
```

**核心：** Qt提供完整的跨平台GUI开发框架，信号槽机制简化对象通信，工具链完善。

