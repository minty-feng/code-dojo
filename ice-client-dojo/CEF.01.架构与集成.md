# CEF.01.架构与集成

CEF（Chromium Embedded Framework）是基于Chromium的嵌入式浏览器框架，C/C++实现，性能优于Electron。

## CEF简介

### 核心特性

- **Chromium内核**：完整浏览器功能
- **多进程架构**：Browser/Renderer/GPU进程
- **C++ API**：性能优秀，灵活控制
- **跨平台**：Windows/Linux/macOS
- **离线渲染**：OSR（Off-Screen Rendering）

### 应用场景

**桌面应用：**
- 游戏内置浏览器（Steam）
- 音乐客户端（Spotify）
- 云盘客户端

**嵌入式浏览器：**
- 应用内网页展示
- HTML5 UI渲染
- Web内容预览

### CEF vs Electron

| 特性 | CEF | Electron |
|------|-----|----------|
| 语言 | C/C++ | JavaScript |
| 性能 | 优秀 | 良好 |
| 包体积 | 可定制 | 较大 |
| 学习曲线 | 陡峭 | 平缓 |
| 适用场景 | 性能敏感 | 快速开发 |

## 环境搭建

### 下载CEF

```bash
# 下载预编译版本
# https://cef-builds.spotifycdn.com/index.html

# 标准版（Standard Distribution）
cef_binary_版本号_平台_Release.tar.bz2

# 最小版（Minimal Distribution，仅头文件和库）
cef_binary_版本号_平台_minimal_Release.tar.bz2
```

### 目录结构

```
cef_binary/
├── Debug/           # Debug库
├── Release/         # Release库
├── Resources/       # 资源文件
├── include/         # 头文件
├── libcef_dll/      # 包装层
└── tests/           # 示例程序
    └── cefsimple/   # 简单示例
```

### CMake配置

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyCEFApp)

set(CMAKE_CXX_STANDARD 17)

# CEF路径
set(CEF_ROOT "${CMAKE_SOURCE_DIR}/cef_binary")

# 设置CEF变量
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CEF_ROOT}/cmake")

find_package(CEF REQUIRED)

add_subdirectory(${CEF_LIBCEF_DLL_WRAPPER_PATH} libcef_dll_wrapper)

# 添加可执行文件
add_executable(${CEF_TARGET} WIN32
    main.cpp
    simple_app.cpp
    simple_app.h
    simple_handler.cpp
    simple_handler.h
)

# 链接CEF
target_link_libraries(${CEF_TARGET} libcef_dll_wrapper ${CEF_STANDARD_LIBS})

# 设置CEF
SET_EXECUTABLE_TARGET_PROPERTIES(${CEF_TARGET})

# 复制资源
COPY_FILES("${CEF_TARGET}" "${CEF_BINARY_FILES}" "${CEF_BINARY_DIR}" "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
COPY_FILES("${CEF_TARGET}" "${CEF_RESOURCE_FILES}" "${CEF_RESOURCE_DIR}" "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
```

## CEF架构

### 进程模型

```
┌──────────────────────┐
│   Browser Process    │  主进程
│  - 创建和管理窗口   │
│  - 网络请求          │
│  - Cookie管理        │
└──────┬───────────────┘
       │
  ┌────┴────┬──────────┬──────────┐
  │         │          │          │
┌─▼──┐  ┌──▼─┐    ┌───▼┐    ┌───▼──┐
│Render│ │Render│  │GPU │    │Plugin│
│进程1 │ │进程2│   │进程│    │进程  │
└─────┘  └─────┘  └────┘    └──────┘
```

### 生命周期

```cpp
// 1. CefInitialize()      初始化
// 2. CefRunMessageLoop()   运行消息循环
// 3. CefShutdown()         清理
```

## Hello World

### simple_app.h

```cpp
#ifndef SIMPLE_APP_H_
#define SIMPLE_APP_H_

#include "include/cef_app.h"

class SimpleApp : public CefApp,
                  public CefBrowserProcessHandler {
public:
    SimpleApp() {}

    // CefApp接口
    virtual CefRefPtr<CefBrowserProcessHandler> GetBrowserProcessHandler()
        OVERRIDE {
        return this;
    }

private:
    IMPLEMENT_REFCOUNTING(SimpleApp);
};

#endif
```

### simple_handler.h

```cpp
#ifndef SIMPLE_HANDLER_H_
#define SIMPLE_HANDLER_H_

#include "include/cef_client.h"

class SimpleHandler : public CefClient,
                      public CefLifeSpanHandler {
public:
    SimpleHandler() {}

    // CefClient接口
    virtual CefRefPtr<CefLifeSpanHandler> GetLifeSpanHandler() OVERRIDE {
        return this;
    }

    // CefLifeSpanHandler接口
    virtual void OnAfterCreated(CefRefPtr<CefBrowser> browser) OVERRIDE;
    virtual bool DoClose(CefRefPtr<CefBrowser> browser) OVERRIDE;
    virtual void OnBeforeClose(CefRefPtr<CefBrowser> browser) OVERRIDE;

private:
    CefRefPtr<CefBrowser> browser_;
    
    IMPLEMENT_REFCOUNTING(SimpleHandler);
};

#endif
```

### main.cpp

```cpp
#include "include/cef_app.h"
#include "simple_app.h"
#include "simple_handler.h"

int main(int argc, char* argv[]) {
    // CEF初始化
    CefMainArgs main_args(argc, argv);
    
    CefRefPtr<SimpleApp> app(new SimpleApp);
    
    // 多进程支持
    int exit_code = CefExecuteProcess(main_args, app.get(), nullptr);
    if (exit_code >= 0) {
        return exit_code;
    }
    
    // CEF设置
    CefSettings settings;
    settings.no_sandbox = true;
    settings.log_severity = LOGSEVERITY_WARNING;
    
    CefInitialize(main_args, settings, app.get(), nullptr);
    
    // 创建浏览器窗口
    CefWindowInfo window_info;
    
    #ifdef _WIN32
        window_info.SetAsPopup(NULL, "CEF Simple");
    #endif
    
    CefBrowserSettings browser_settings;
    
    CefRefPtr<SimpleHandler> handler(new SimpleHandler());
    
    CefBrowserHost::CreateBrowser(
        window_info,
        handler,
        "https://www.google.com",
        browser_settings,
        nullptr,
        nullptr
    );
    
    // 运行消息循环
    CefRunMessageLoop();
    
    // 清理
    CefShutdown();
    
    return 0;
}
```

## JavaScript交互

### JavaScript调用C++

```cpp
// C++注册函数
class MyV8Handler : public CefV8Handler {
public:
    virtual bool Execute(const CefString& name,
                        CefRefPtr<CefV8Value> object,
                        const CefV8ValueList& arguments,
                        CefRefPtr<CefV8Value>& retval,
                        CefString& exception) OVERRIDE {
        if (name == "myFunction") {
            // 处理JavaScript调用
            CefString arg1 = arguments[0]->GetStringValue();
            retval = CefV8Value::CreateString("Result from C++");
            return true;
        }
        return false;
    }

private:
    IMPLEMENT_REFCOUNTING(MyV8Handler);
};

// 渲染进程中注册
CefRefPtr<CefV8Value> func = CefV8Value::CreateFunction("myFunction", new MyV8Handler());
CefRefPtr<CefV8Value> global = context->GetGlobal();
global->SetValue("myFunction", func, V8_PROPERTY_ATTRIBUTE_NONE);

// JavaScript调用
var result = myFunction("argument");
console.log(result);  // "Result from C++"
```

### C++调用JavaScript

```cpp
// C++执行JavaScript
CefRefPtr<CefBrowser> browser = /* ... */;
CefRefPtr<CefFrame> frame = browser->GetMainFrame();

frame->ExecuteJavaScript(
    "console.log('Called from C++');",
    frame->GetURL(),
    0
);

// 带回调
CefString code = "someFunction();";
frame->ExecuteJavaScript(code, "", 0);
```

## 最佳实践

### 资源管理

```cpp
// ✓ 使用CefRefPtr智能指针
CefRefPtr<CefBrowser> browser;

// ✓ IMPLEMENT_REFCOUNTING宏
class MyHandler : public CefClient {
    IMPLEMENT_REFCOUNTING(MyHandler);
};
```

### 线程安全

```cpp
// Browser进程线程
// - UI线程（TID_UI）
// - IO线程（TID_IO）
// - FILE线程（TID_FILE）

// 检查线程
if (!CefCurrentlyOn(TID_UI)) {
    // 错误线程
    CefPostTask(TID_UI, base::Bind(&Function));
}

// 在UI线程执行
CefPostTask(TID_UI, base::Bind(&MyClass::Method, this, arg));
```

**核心：** CEF提供完整Chromium嵌入能力，多进程架构保证稳定性，C++ API提供精细控制。

