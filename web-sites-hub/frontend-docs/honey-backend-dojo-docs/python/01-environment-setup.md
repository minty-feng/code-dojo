# 01-Python环境搭建

## Python简介

Python由Guido van Rossum于1991年创建，设计哲学强调代码可读性。语法简洁清晰，学习曲线平缓，生态系统丰富。

### 应用场景

**Web开发：**
- Django、Flask、FastAPI等框架
- 后端API、全栈应用、微服务

**数据科学：**
- NumPy、Pandas、Matplotlib数据分析
- Jupyter Notebook交互式计算
- 机器学习、深度学习

**自动化：**
- 脚本编写、任务调度
- 运维自动化、测试自动化
- 爬虫、数据采集

**人工智能：**
- TensorFlow、PyTorch深度学习框架
- scikit-learn机器学习
- OpenCV计算机视觉、NLTK自然语言处理

**其他领域：**
- 科学计算（SciPy）
- 游戏开发（Pygame）
- 桌面应用（PyQt、Tkinter）
- 嵌入式脚本（MicroPython）

### 语言特点

**优势：**
- 语法简洁：相比Java/C++代码量少50%-70%
- 开发效率高：动态类型、丰富标准库
- 跨平台：Linux/Windows/macOS无缝运行
- 生态强大：PyPI拥有30万+第三方库
- 多范式：面向对象、函数式、过程式

**劣势：**
- 性能较低：解释型语言，比C++慢10-100倍
- GIL限制：多线程无法利用多核（CPU密集型）
- 类型检查：运行时才发现类型错误
- 移动端弱：iOS/Android支持有限

**适合：** 快速开发、数据处理、原型验证  
**不适合：** 性能极致、底层系统、移动应用

## Python版本

Python 2已于2020年停止支持，Python 3是唯一选择。

- **Python 3.7**：2018年发布，数据类、async/await增强
- **Python 3.8**：2019年发布，海象运算符、位置参数
- **Python 3.9**：2020年发布，字典合并、类型提示增强
- **Python 3.10**：2021年发布，模式匹配、更好的错误信息
- **Python 3.11**：2022年发布，性能提升25%

学习环境：Python 3.9+，生产环境：Python 3.9或3.10。

## 安装Python

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 验证
python3 --version
pip3 --version

# 设置默认Python3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```

### macOS

```bash
# Homebrew
brew install python3

# 验证
python3 --version
pip3 --version

# 添加到PATH（通常自动完成）
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
```

### Windows

1. 下载官方安装包：python.org
2. 安装时勾选"Add Python to PATH"
3. 验证：`python --version`

## 虚拟环境

虚拟环境隔离项目依赖，避免版本冲突。

### venv（内置）

```bash
# 创建虚拟环境
python3 -m venv myenv

# 激活
source myenv/bin/activate       # Linux/macOS
myenv\Scripts\activate          # Windows

# 安装包
pip install requests

# 导出依赖
pip freeze > requirements.txt

# 安装依赖
pip install -r requirements.txt

# 退出
deactivate
```

### virtualenv

```bash
# 安装
pip install virtualenv

# 创建
virtualenv myenv

# 使用同venv
```

### conda（数据科学）

```bash
# 创建环境
conda create -n myenv python=3.9

# 激活
conda activate myenv

# 安装包
conda install numpy pandas

# 退出
conda deactivate
```

## 包管理

### pip

```bash
# 安装包
pip install package_name
pip install package==1.0.0      # 指定版本
pip install package>=1.0.0      # 版本范围

# 升级
pip install --upgrade package

# 卸载
pip uninstall package

# 列出已安装
pip list
pip show package                # 详细信息

# 搜索
pip search keyword

# 导出/导入依赖
pip freeze > requirements.txt
pip install -r requirements.txt
```

### requirements.txt

```
# 精确版本
requests==2.28.0
numpy==1.23.0

# 版本范围
flask>=2.0.0,<3.0.0

# 最新版本
pandas

# 从git安装
git+https://github.com/user/repo.git

# 本地包
-e ./local_package
```

## 开发工具

### PyCharm

JetBrains出品，专业Python IDE。

**特性：**
- 智能代码补全
- 调试器
- 集成测试
- 数据库工具
- 虚拟环境管理

**快捷键：**
- `Cmd/Ctrl + /`：注释
- `Shift + F10`：运行
- `Shift + F9`：调试
- `Cmd/Ctrl + B`：跳转定义
- `Cmd/Ctrl + Alt + L`：格式化

### VS Code

轻量级，插件丰富。

**必装插件：**
- Python（微软官方）
- Pylance（类型检查）
- Python Docstring Generator
- autoDocstring

**配置（.vscode/settings.json）：**
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true
}
```

### Jupyter Notebook

交互式编程环境，适合数据分析。

```bash
# 安装
pip install jupyter

# 启动
jupyter notebook

# 或JupyterLab
pip install jupyterlab
jupyter lab
```

## 代码规范

### PEP 8风格指南

```python
# 命名规范
class MyClass:              # 大驼峰
    pass

def my_function():          # 下划线
    pass

my_variable = 10            # 下划线
MY_CONSTANT = 100           # 全大写

_private_var = 1            # 单下划线：内部使用
__private_var = 2           # 双下划线：名称改写

# 缩进：4空格
if condition:
    do_something()

# 空行：函数间2行，类间2行，方法间1行
class MyClass:
    
    def method1(self):
        pass
    
    def method2(self):
        pass


def function():
    pass

# 行长度：最多79字符
long_variable_name = (first_part +
                      second_part +
                      third_part)

# 导入顺序：标准库、第三方库、本地模块
import os
import sys

import requests
import numpy

from mypackage import mymodule
```

### 代码质量工具

```bash
# pylint：代码检查
pip install pylint
pylint myfile.py

# flake8：风格检查
pip install flake8
flake8 myfile.py

# black：自动格式化
pip install black
black myfile.py

# isort：导入排序
pip install isort
isort myfile.py

# mypy：类型检查
pip install mypy
mypy myfile.py
```

## Hello World

### 基本程序

```python
# hello.py
print("Hello, World!")
```

```bash
# 运行
python hello.py

# 或直接
python -c "print('Hello')"
```

### 带函数的程序

```python
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
```

## 调试工具

### pdb（内置调试器）

```python
import pdb

def buggy_function():
    x = 10
    pdb.set_trace()  # 设置断点
    y = x * 2
    return y

# 运行会在断点处暂停
# 常用命令：
# n：下一行
# s：步入函数
# c：继续执行
# p variable：打印变量
# q：退出
```

### 断点调试（Python 3.7+）

```python
def function():
    x = 10
    breakpoint()  # 替代pdb.set_trace()
    return x
```

## 项目结构

### 标准项目结构

```
myproject/
├── README.md
├── requirements.txt
├── setup.py
├── mypackage/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/
│   ├── __init__.py
│   ├── test_module1.py
│   └── test_module2.py
├── docs/
│   └── conf.py
└── scripts/
    └── run.py
```

### 包管理（setup.py）

```python
from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
        'numpy>=1.23.0',
    ],
    python_requires='>=3.9',
)
```

### pyproject.toml（现代方式）

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
dependencies = [
    "requests>=2.28.0",
    "numpy>=1.23.0",
]
requires-python = ">=3.9"

[project.optional-dependencies]
dev = ["pytest", "black", "flake8"]
```

## 常用工具

### IPython

增强的交互式Shell。

```bash
# 安装
pip install ipython

# 启动
ipython

# 特性：
# - 自动补全
# - 魔法命令：%timeit, %run, %debug
# - 历史记录：_（上一结果）
# - 系统命令：!ls
```

### Poetry（依赖管理）

现代Python包管理工具。

```bash
# 安装
pip install poetry

# 创建项目
poetry new myproject

# 添加依赖
poetry add requests

# 安装依赖
poetry install

# 运行
poetry run python script.py

# 发布
poetry publish
```

## 性能分析

### timeit

```python
import timeit

# 测试代码执行时间
timeit.timeit('[i for i in range(1000)]', number=10000)

# 魔法命令（IPython/Jupyter）
%timeit [i for i in range(1000)]
```

### cProfile

```python
import cProfile

def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total

# 性能分析
cProfile.run('slow_function()')
```

```bash
# 命令行分析
python -m cProfile script.py
```

## Python特性速览

### 动态类型

```python
x = 10          # int
x = "hello"     # str，类型可变
```

### 强类型

```python
"3" + 4         # TypeError（不会自动转换）
int("3") + 4    # 7（需显式转换）
```

### 缩进敏感

```python
if True:
    print("Yes")  # 缩进4空格
print("Done")     # 不缩进
```

### 一切皆对象

```python
# 函数是对象
def func():
    pass

x = func        # 函数赋值
type(func)      # <class 'function'>

# 类是对象
class MyClass:
    pass

type(MyClass)   # <class 'type'>
```

## Python之禅

```python
import this

# The Zen of Python, by Tim Peters
# 
# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Complex is better than complicated.
# ...
```

**核心理念：**
- 优雅胜于丑陋
- 明确胜于隐晦
- 简单胜于复杂
- 可读性很重要

