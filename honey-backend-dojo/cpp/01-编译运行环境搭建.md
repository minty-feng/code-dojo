# 01-编译运行环境搭建

## 编译器选择

### GCC (GNU Compiler Collection)
GCC是GNU项目开发的编译器套件，是目前最广泛使用的C++编译器之一。支持多种平台，包括Linux、Windows、macOS等，完全开源免费。

**主要特点：**
- 开源免费，遵循GPL许可证
- 跨平台支持，可在多种操作系统上运行
- 功能完整，支持C++11/14/17/20标准
- 社区活跃，文档丰富
- 性能优秀，生成的代码质量高

**适用场景：**
- Linux系统开发的首选
- 开源项目开发
- 需要跨平台兼容的项目
- 学习和研究用途

**安装方式：**
- Linux系统通常默认安装，可通过包管理器更新
- Windows系统需要安装MinGW或MSYS2
- macOS可通过Homebrew安装：`brew install gcc`

**基本使用：**
```bash
g++ -o program source.cpp
```

### Clang
Clang是LLVM项目的前端编译器，以其优秀的错误信息和警告信息而闻名。被设计为GCC的替代品，在错误诊断方面表现突出。

**主要特点：**
- 错误信息更加友好和详细
- 编译速度快，内存占用少
- 模块化设计，易于扩展
- 与LLVM工具链集成良好
- 支持静态分析和代码检查

**适用场景：**
- macOS和iOS开发
- 需要详细错误信息的开发
- 静态分析和代码检查
- 学习和调试用途

**安装方式：**
- macOS系统默认使用Clang
- Linux系统可通过包管理器安装
- Windows系统需要安装LLVM

**基本使用：**
```bash
clang++ -o program source.cpp
```

### MSVC (Microsoft Visual C++)
MSVC是微软开发的C++编译器，主要针对Windows平台优化，与Visual Studio集成度很高。

**主要特点：**
- Windows平台性能优化
- 与Visual Studio深度集成
- 调试工具功能强大
- 支持Windows特有的API和库
- 企业级支持和文档

**适用场景：**
- Windows平台开发
- 企业级应用开发
- 需要Windows API支持的项目
- 商业软件开发

**安装方式：**
- 通过Visual Studio Community（免费版）安装
- 包含完整的开发环境

**基本使用：**
```bash
cl /EHsc source.cpp
```

## 开发环境配置

### Visual Studio Code
VS Code是微软开发的轻量级代码编辑器，通过插件可以变成功能强大的IDE。C++开发需要安装相应的插件。

**推荐插件：**
- C/C++ Extension Pack：包含C++语言支持、调试器、IntelliSense等
- CMake Tools：CMake项目支持
- GitLens：Git集成增强

**配置文件说明：**
- `tasks.json`：定义编译任务
- `launch.json`：配置调试器
- `c_cpp_properties.json`：设置编译器路径和包含目录

**配置文件示例（.vscode/目录下）：**

**tasks.json** - 编译任务配置：
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "type": "shell",
            "label": "C++: g++ build active file",
            "command": "/usr/bin/g++",
            "args": [
                "-std=c++17",
                "-g",
                "-Wall",
                "-Wextra",
                "${file}",
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}"
            ],
            "options": {
                "cwd": "${fileDirname}"
            },
            "problemMatcher": ["$gcc"],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```

**launch.json** - 调试器配置：
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "C++: g++ Debug",
            "type": "cppdbg",
            "request": "launch",
            "program": "${fileDirname}/${fileBasenameNoExtension}",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "C++: g++ build active file",
            "miDebuggerPath": "/usr/bin/gdb"
        }
    ]
}
```

**c_cpp_properties.json** - IntelliSense配置：
```json
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "/usr/include",
                "/usr/local/include"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/g++",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "gcc-x64"
        }
    ],
    "version": 4
}
```

**优势：**
- 轻量级，启动速度快
- 插件生态丰富
- 跨平台支持
- 免费使用

**适用场景：**
- 轻量级开发
- 跨平台开发
- 插件定制需求
- 学习和个人项目

### CLion
CLion是JetBrains开发的C++ IDE，专为C++开发设计，功能强大且专业。

**主要功能：**
- 智能代码补全和重构
- 强大的调试器
- 代码分析和检查
- 版本控制集成

**优势：**
- 专业的C++开发工具
- 智能提示和错误检查
- 重构功能强大
- 支持远程开发

**缺点：**
- 商业软件，需要付费
- 资源占用较大

**适用场景：**
- 专业C++开发
- 大型项目开发
- 需要强大调试功能
- 团队协作开发

### Visual Studio
Visual Studio是微软的集成开发环境，功能最为全面，特别适合Windows平台开发。

**主要功能：**
- 完整的开发工具链
- 强大的调试器
- 性能分析工具
- 团队协作功能
- 丰富的扩展

**优势：**
- 功能最全面
- Windows平台优化
- 企业级支持
- 调试功能强大

**缺点：**
- 仅支持Windows平台
- 资源占用大
- 学习曲线较陡

**适用场景：**
- Windows平台开发
- 企业级应用
- 需要完整工具链
- 团队开发

## 编译选项

### 基本编译选项

**基本编译命令：**
```bash
# 基本编译
g++ -o program source.cpp

# 指定C++标准
g++ -std=c++17 -o program source.cpp

# 开启所有警告
g++ -Wall -Wextra -o program source.cpp

# 开启优化
g++ -O2 -o program source.cpp

# 调试信息
g++ -g -o program source.cpp
```

**选项说明：**
- `-o program`：指定输出文件名
- `-std=c++17`：指定使用的C++标准版本
- `-Wall`：开启所有常见警告
- `-Wextra`：开启额外警告
- `-O2`：开启二级优化
- `-g`：生成调试信息

### 常用编译标志

**标准相关：**
- `-std=c++11`：使用C++11标准
- `-std=c++14`：使用C++14标准
- `-std=c++17`：使用C++17标准
- `-std=c++20`：使用C++20标准

**警告相关：**
- `-Wall`：开启所有常见警告
- `-Wextra`：开启额外警告
- `-Werror`：将警告视为错误
- `-Wno-unused`：忽略未使用变量警告

**优化相关：**
- `-O0`：无优化（调试用）
- `-O1`：基本优化
- `-O2`：推荐优化级别
- `-O3`：激进优化
- `-Os`：优化代码大小

**调试相关：**
- `-g`：生成调试信息
- `-ggdb`：生成GDB调试信息
- `-DDEBUG`：定义DEBUG宏

## 调试工具

### GDB (GNU Debugger)
GDB是GNU项目开发的调试器，是Linux系统上最常用的调试工具。

**基本使用：**
```bash
gdb ./program
```

**常用命令：**
- `break main`：在main函数设置断点
- `break filename:line`：在指定文件的指定行设置断点
- `run`：运行程序
- `run arg1 arg2`：带参数运行程序
- `print variable`：打印变量值
- `info locals`：显示所有局部变量
- `step`：单步执行（进入函数）
- `next`：单步执行（不进入函数）
- `continue`：继续执行
- `quit`：退出GDB

**使用场景：**
- 调试程序逻辑错误
- 查看变量值变化
- 分析程序崩溃原因
- 性能分析

### LLDB (LLVM Debugger)
LLDB是LLVM项目开发的调试器，是macOS和iOS开发的主要调试工具。

**基本使用：**
```bash
lldb ./program
```

**常用命令：**
- `breakpoint set -n main`：在main函数设置断点
- `run`：运行程序
- `frame variable`：显示当前帧的变量
- `step`：单步执行
- `next`：单步执行（不进入函数）
- `continue`：继续执行

**优势：**
- 与Clang集成良好
- 支持多种语言
- 脚本化支持

### Valgrind (内存检查)
Valgrind是内存调试和性能分析工具，主要用于检测内存泄漏和内存错误。

**内存泄漏检查：**
```bash
valgrind --leak-check=full ./program
```

**内存错误检查：**
```bash
valgrind --tool=memcheck ./program
```

**性能分析：**
```bash
valgrind --tool=callgrind ./program
```

**主要功能：**
- 检测内存泄漏
- 检测内存访问错误
- 性能分析
- 缓存分析

## 构建系统

### Make
Make是最经典的构建工具，通过Makefile定义编译规则和依赖关系。

**Makefile基本结构：**
```makefile
target: dependencies
    command
```

**示例Makefile：**
```makefile
CC = g++
CFLAGS = -Wall -Wextra -std=c++17
TARGET = program
SOURCES = main.cpp utils.cpp

$(TARGET): $(SOURCES)
    $(CC) $(CFLAGS) -o $(TARGET) $(SOURCES)

clean:
    rm -f $(TARGET)

.PHONY: clean
```

**优势：**
- 简单易学
- 广泛支持
- 依赖管理
- 增量编译

### CMake
CMake是跨平台的构建系统生成器，可以生成各种构建系统的文件。

**CMakeLists.txt示例：**
```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)

add_executable(program main.cpp utils.cpp)

target_include_directories(program PRIVATE include)
target_link_libraries(program PRIVATE some_library)
```

**使用步骤：**
```bash
mkdir build
cd build
cmake ..
make
```

**优势：**
- 跨平台支持
- 模块化设计
- 依赖管理
- IDE集成

### 包管理

**vcpkg：**
- 微软开源包管理器
- 支持Windows、Linux、macOS
- 与Visual Studio集成良好
- 支持CMake集成

**Conan：**
- C++包管理器
- 支持多种构建系统
- 依赖解析
- 版本管理

**Hunter：**
- CMake包管理器
- 轻量级
- CMake原生支持

## 版本控制

### Git基础
Git是分布式版本控制系统，是现代软件开发的标准工具。

**基本操作：**
```bash
git init                    # 初始化仓库
git add .                   # 添加所有文件
git commit -m "message"     # 提交更改
git branch                  # 查看分支
git checkout branch-name    # 切换分支
git merge branch-name       # 合并分支
```

**工作流程：**
1. 创建或克隆仓库
2. 创建分支进行开发
3. 提交更改
4. 合并到主分支
5. 推送到远程仓库

### .gitignore配置

**C++项目.gitignore：**
```
# 编译产物
*.o
*.exe
*.out
build/
bin/

# IDE文件
.vscode/
.idea/
*.vcxproj
*.sln

# 系统文件
.DS_Store
Thumbs.db
```

## 代码格式化

### Clang-format
Clang-format是代码格式化工具，可以自动格式化C++代码。

**配置文件：**
```yaml
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
```

**使用方式：**
```bash
clang-format -i *.cpp
```

**支持的风格：**
- Google：Google C++风格
- LLVM：LLVM项目风格
- Chromium：Chromium项目风格
- Mozilla：Mozilla项目风格

### 代码检查

**Clang-tidy：**
- 静态代码分析工具
- 检查代码风格和潜在问题
- 可配置规则
- IDE集成支持

**Cppcheck：**
- 开源代码质量检查工具
- 检测内存泄漏、缓冲区溢出等问题
- 支持多种检查模式
- 轻量级

**PVS-Studio：**
- 商业代码分析工具
- 功能强大
- 支持多种编译器
- 详细的错误报告

**SonarQube：**
- 代码质量管理平台
- 支持多种语言
- 持续集成支持
- 团队协作功能

## 实用编译技巧

### 推荐编译命令组合

```bash
# 开发阶段（快速编译，便于调试）
g++ -std=c++17 -g -Wall -Wextra -o program source.cpp

# 发布阶段（优化性能）
g++ -std=c++17 -O2 -DNDEBUG -o program source.cpp

# 严格检查（捕获所有潜在问题）
g++ -std=c++17 -Wall -Wextra -Werror -pedantic -o program source.cpp

# 性能优化（针对当前CPU）
g++ -std=c++17 -O3 -march=native -flto -o program source.cpp
```

**参数说明：**
- `-std=c++17`：使用C++17标准
- `-g`：生成调试信息
- `-Wall -Wextra`：开启所有警告
- `-Werror`：将警告视为错误
- `-O2/-O3`：优化级别
- `-DNDEBUG`：禁用assert
- `-march=native`：针对当前CPU优化
- `-flto`：链接时优化
