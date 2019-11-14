# 02-Python基础语法

Python语法简洁优雅，强调可读性。动态类型，强类型，缩进敏感。

## 数据类型

### 数字类型

```python
# 整数（无大小限制）
x = 10
big_num = 123456789012345678901234567890

# 浮点数
y = 3.14
sci = 1.23e-4  # 科学计数法

# 复数
z = 3 + 4j
z.real         # 3.0
z.imag         # 4.0

# 布尔值
flag = True
result = False

# 类型转换
int("10")      # 10
float("3.14")  # 3.14
str(100)       # "100"
bool(0)        # False
bool(1)        # True
```

### 字符串

```python
# 创建
s1 = 'single'
s2 = "double"
s3 = '''multi
line'''
s4 = """another
multi line"""

# f-string（Python 3.6+，推荐）
name = "Alice"
age = 25
msg = f"My name is {name}, age {age}"
msg = f"{name.upper()}"          # 表达式
msg = f"{age:03d}"                # 格式化：025

# 索引和切片
s = "Python"
s[0]           # 'P'
s[-1]          # 'n'
s[0:2]         # 'Py'
s[::2]         # 'Pto'（步长2）
s[::-1]        # 'nohtyP'（反转）

# 常用方法
s.upper()      # 大写
s.lower()      # 小写
s.strip()      # 去空格
s.split(',')   # 分割
','.join(['a', 'b'])  # 拼接
s.replace('old', 'new')
s.startswith('Py')
s.endswith('on')
s.find('th')   # 查找位置
'Py' in s      # 包含判断
```

### 列表（list）

可变有序序列。

```python
# 创建
lst = [1, 2, 3, 4, 5]
empty = []
mixed = [1, "two", 3.0, True]

# 列表推导式
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# 访问
lst[0]         # 1
lst[-1]        # 5
lst[1:3]       # [2, 3]

# 修改
lst[0] = 10
lst.append(6)      # 尾部添加
lst.insert(0, 0)   # 指定位置插入
lst.extend([7, 8]) # 合并列表
lst.remove(3)      # 删除第一个3
lst.pop()          # 删除并返回最后一个
lst.pop(0)         # 删除并返回指定位置
del lst[0]         # 删除指定位置
lst.clear()        # 清空

# 查询
len(lst)       # 长度
3 in lst       # 是否包含
lst.index(3)   # 查找索引
lst.count(3)   # 计数

# 排序
lst.sort()              # 原地排序
sorted(lst)             # 返回新列表
lst.reverse()           # 反转
reversed(lst)           # 返回迭代器
```

### 元组（tuple）

不可变有序序列。

```python
# 创建
t = (1, 2, 3)
single = (1,)      # 单元素需要逗号
empty = ()

# 解包
a, b, c = t
a, *rest, c = (1, 2, 3, 4, 5)  # rest=[2,3,4]

# 不可修改
# t[0] = 10      # TypeError
```

### 字典（dict）

键值对，哈希表实现。

```python
# 创建
d = {'name': 'Alice', 'age': 25}
d2 = dict(name='Bob', age=30)
empty = {}

# 字典推导式
squares = {x: x**2 for x in range(5)}

# 访问
d['name']              # 'Alice'
d.get('name')          # 'Alice'
d.get('city', 'Beijing')  # 默认值

# 修改
d['name'] = 'Bob'
d['city'] = 'Shanghai'  # 添加新键
del d['age']            # 删除
d.pop('name')           # 删除并返回
d.clear()               # 清空

# 查询
'name' in d             # 是否包含键
len(d)                  # 键值对数量

# 遍历
for key in d:
    print(key, d[key])

for key, value in d.items():
    print(key, value)

for key in d.keys():
    print(key)

for value in d.values():
    print(value)

# Python 3.9+合并
d1 = {'a': 1}
d2 = {'b': 2}
merged = d1 | d2       # {'a': 1, 'b': 2}
d1 |= d2               # 就地合并
```

### 集合（set）

无序不重复元素。

```python
# 创建
s = {1, 2, 3, 4, 5}
empty = set()  # 注意：{}是空字典

# 集合推导式
even = {x for x in range(10) if x % 2 == 0}

# 操作
s.add(6)       # 添加
s.remove(3)    # 删除（不存在抛异常）
s.discard(3)   # 删除（不存在不报错）
s.pop()        # 删除任意元素

# 集合运算
a = {1, 2, 3}
b = {2, 3, 4}
a | b          # 并集：{1, 2, 3, 4}
a & b          # 交集：{2, 3}
a - b          # 差集：{1}
a ^ b          # 对称差：{1, 4}

# 判断
2 in a
a.issubset(b)
a.issuperset(b)
```

## 运算符

### 算术运算符

```python
+  -  *  /     # 加减乘除
//             # 整除：5 // 2 = 2
%              # 取模：5 % 2 = 1
**             # 幂：2 ** 3 = 8

# 复合赋值
+=  -=  *=  /=  //=  %=  **=
```

### 比较运算符

```python
==  !=  >  <  >=  <=

# 链式比较
1 < x < 10     # 等价于：1 < x and x < 10
a == b == c    # 等价于：a == b and b == c
```

### 逻辑运算符

```python
and  or  not

# 短路求值
result = a and b or c
```

### 位运算符

```python
&  |  ^  ~     # 与或异或取反
<<  >>         # 左移右移
```

### 成员运算符

```python
x in lst       # 是否在序列中
x not in lst
```

### 身份运算符

```python
x is y         # 是否同一对象（内存地址）
x is not y

# is vs ==
a = [1, 2, 3]
b = [1, 2, 3]
a == b         # True（值相同）
a is b         # False（不同对象）

x = None
x is None      # True（None单例，用is）
```

## 控制结构

### 条件语句

```python
# if-elif-else
if x > 0:
    print("positive")
elif x < 0:
    print("negative")
else:
    print("zero")

# 三元运算符
result = "even" if x % 2 == 0 else "odd"

# Python 3.10+模式匹配
match value:
    case 1:
        print("one")
    case 2 | 3:
        print("two or three")
    case [x, y]:
        print(f"list of {x} and {y}")
    case {"name": n}:
        print(f"dict with name {n}")
    case _:
        print("default")
```

### 循环语句

```python
# for循环（遍历序列）
for i in range(5):
    print(i)

for item in [1, 2, 3]:
    print(item)

for i, item in enumerate(['a', 'b', 'c']):
    print(i, item)  # 索引和值

for k, v in {'a': 1, 'b': 2}.items():
    print(k, v)

# while循环
while condition:
    # ...
    break      # 跳出循环
    continue   # 跳过本次迭代

# for-else / while-else
for item in lst:
    if item == target:
        break
else:
    print("not found")  # 未break时执行
```

### 推导式

```python
# 列表推导式
[x**2 for x in range(10)]
[x for x in range(10) if x % 2 == 0]
[x if x > 0 else 0 for x in data]

# 字典推导式
{x: x**2 for x in range(5)}

# 集合推导式
{x % 10 for x in range(100)}

# 生成器表达式（节省内存）
gen = (x**2 for x in range(1000000))  # 不立即计算
```

## 函数

### 函数定义

```python
def greet(name):
    return f"Hello, {name}"

# 默认参数
def power(x, n=2):
    return x ** n

power(3)       # 9
power(3, 3)    # 27

# 可变参数
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3, 4)  # 10

# 关键字参数
def info(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")

info(name="Alice", age=25)

# 混合参数
def func(a, b=2, *args, **kwargs):
    pass
```

### Lambda表达式

```python
# 匿名函数
add = lambda x, y: x + y
add(3, 4)      # 7

# 常用于高阶函数
numbers = [1, 2, 3, 4, 5]
list(map(lambda x: x**2, numbers))
list(filter(lambda x: x % 2 == 0, numbers))

# 排序
students = [('Alice', 25), ('Bob', 20)]
sorted(students, key=lambda x: x[1])  # 按年龄排序
```

### 函数注解（类型提示）

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

# 复杂类型
from typing import List, Dict, Optional, Union

def process(data: List[int]) -> Dict[str, int]:
    return {"sum": sum(data)}

def find(lst: List[int], target: int) -> Optional[int]:
    return lst.index(target) if target in lst else None

# 变量注解
age: int = 25
names: List[str] = ["Alice", "Bob"]
```

## 常见陷阱

```python
# 1. 可变默认参数
def append_to(element, lst=[]):  # 危险！
    lst.append(element)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2]（共享同一列表！）

# 正确做法
def append_to(element, lst=None):
    if lst is None:
        lst = []
    lst.append(element)
    return lst

# 2. 列表乘法陷阱
matrix = [[0] * 3] * 3  # 危险！3行共享同一列表
matrix[0][0] = 1        # 所有行的[0]都变成1

# 正确
matrix = [[0] * 3 for _ in range(3)]

# 3. 循环变量泄漏
for i in range(10):
    pass
print(i)  # 9（i仍可访问）

# 4. is vs ==
a = 1000
b = 1000
a == b    # True（值相同）
a is b    # False（不同对象）

# 小整数缓存（-5到256）
x = 10
y = 10
x is y    # True（共享对象）

# 5. 字符串拼接性能
# 慢
s = ""
for x in lst:
    s += str(x)  # 每次创建新字符串

# 快
s = "".join(str(x) for x in lst)
```

## 异常处理

### try-except

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("division by zero")
except (TypeError, ValueError) as e:
    print(f"error: {e}")
except Exception as e:
    print(f"general error: {e}")
else:
    print("no exception")  # 无异常时执行
finally:
    print("cleanup")       # 总是执行
```

### 抛出异常

```python
raise ValueError("invalid value")
raise TypeError("wrong type")

# 自定义异常
class CustomError(Exception):
    pass

raise CustomError("something wrong")
```

### 上下文管理器

```python
# with语句自动清理资源
with open('file.txt', 'r') as f:
    content = f.read()
# 自动调用f.close()

# 多个资源
with open('in.txt') as fin, open('out.txt', 'w') as fout:
    fout.write(fin.read())
```

## 面向对象基础

### 类定义

```python
class Person:
    # 类变量
    species = "Human"
    
    def __init__(self, name, age):
        # 实例变量
        self.name = name
        self.age = age
    
    # 实例方法
    def greet(self):
        return f"Hi, I'm {self.name}"
    
    # 类方法
    @classmethod
    def from_birth_year(cls, name, birth_year):
        return cls(name, 2024 - birth_year)
    
    # 静态方法
    @staticmethod
    def is_adult(age):
        return age >= 18
    
    # 特殊方法
    def __str__(self):
        return f"Person({self.name}, {self.age})"
    
    def __repr__(self):
        return f"Person('{self.name}', {self.age})"

# 使用
p = Person("Alice", 25)
print(p.greet())
p2 = Person.from_birth_year("Bob", 1995)
```

### 继承

```python
class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)  # 调用父类构造
        self.student_id = student_id
    
    def greet(self):  # 重写
        return f"Hi, I'm student {self.name}"

# 多继承
class A:
    def method(self):
        print("A")

class B:
    def method(self):
        print("B")

class C(A, B):
    pass

C().method()  # "A"（MRO：方法解析顺序）
C.__mro__     # 查看MRO
```

## 迭代器和生成器

### 迭代器

```python
# 可迭代对象
lst = [1, 2, 3]
it = iter(lst)

next(it)       # 1
next(it)       # 2
next(it)       # 3
next(it)       # StopIteration

# 自定义迭代器
class Counter:
    def __init__(self, max):
        self.max = max
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.max:
            self.current += 1
            return self.current
        raise StopIteration

for i in Counter(5):
    print(i)
```

### 生成器

```python
# 生成器函数
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)

# 生成器表达式
gen = (x**2 for x in range(1000000))  # 惰性求值，节省内存

# 对比
lst = [x**2 for x in range(1000000)]  # 立即计算，占用内存
```

## 装饰器

函数修饰符，元编程利器。

```python
# 函数装饰器
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()  # 自动计时

# 带参数的装饰器
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet():
    print("Hello")

greet()  # 打印3次

# 类装饰器
@property
def name(self):
    return self._name

@name.setter
def name(self, value):
    self._name = value
```

## 常用内置函数

```python
# 数学
abs(-5)        # 绝对值
max(1, 2, 3)   # 最大值
min(1, 2, 3)   # 最小值
sum([1, 2, 3]) # 求和
round(3.14159, 2)  # 四舍五入

# 序列
len([1, 2, 3]) # 长度
sorted([3, 1, 2])  # 排序
reversed([1, 2, 3]) # 反转
enumerate(['a', 'b'])  # (索引, 值)元组
zip([1, 2], ['a', 'b'])  # [(1, 'a'), (2, 'b')]

# 高阶函数
map(lambda x: x**2, [1, 2, 3])
filter(lambda x: x > 0, [-1, 0, 1, 2])
reduce(lambda x, y: x + y, [1, 2, 3, 4])  # from functools

# 类型判断
type(x)
isinstance(x, int)
isinstance(x, (int, float))  # 多个类型

# 对象
id(x)          # 内存地址
dir(x)         # 属性和方法列表
hasattr(x, 'attr')
getattr(x, 'attr', default)
setattr(x, 'attr', value)

# 其他
all([True, True])   # 全部为真
any([False, True])  # 任一为真
eval("1 + 2")       # 执行表达式
exec("x = 10")      # 执行语句
```

## 文件操作

```python
# 读文件
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()          # 全部内容
    
with open('file.txt', 'r') as f:
    lines = f.readlines()       # 行列表
    
with open('file.txt', 'r') as f:
    for line in f:              # 逐行读取（节省内存）
        print(line.strip())

# 写文件
with open('file.txt', 'w') as f:
    f.write("Hello\n")
    f.writelines(['line1\n', 'line2\n'])

# 追加
with open('file.txt', 'a') as f:
    f.write("append\n")

# 二进制
with open('file.bin', 'rb') as f:
    data = f.read()
```

## 模块和包

### 导入模块

```python
# 导入整个模块
import math
math.sqrt(16)

# 导入别名
import numpy as np
np.array([1, 2, 3])

# 导入特定函数
from math import sqrt, pi
sqrt(16)

# 导入所有（不推荐）
from math import *

# 相对导入
from . import module
from .. import parent_module
```

### 创建模块

```python
# mymodule.py
def function():
    pass

class MyClass:
    pass

# 使用
import mymodule
mymodule.function()
```

### 包结构

```
mypackage/
├── __init__.py      # 标记为包
├── module1.py
└── subpackage/
    ├── __init__.py
    └── module2.py
```

## 最佳实践

1. **用f-string格式化**：清晰易读
2. **列表推导式**：简洁高效
3. **with管理资源**：自动清理
4. **类型提示**：提高可维护性
5. **避免可变默认参数**：用None+判断
6. **is判断None**：`x is None`，不用`x == None`
7. **join拼接字符串**：比`+=`快
8. **生成器处理大数据**：惰性求值
9. **异常具体化**：捕获具体异常，不滥用`except Exception`
10. **遵循PEP 8**：代码一致性

**核心：** Python追求简洁和可读性，充分利用语言特性。

