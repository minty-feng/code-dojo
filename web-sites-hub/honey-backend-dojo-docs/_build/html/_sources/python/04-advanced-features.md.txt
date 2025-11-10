# 04-Python高级特性

Python的高级特性包括装饰器、生成器、上下文管理器、元类等。掌握这些特性可编写更优雅的代码。

## 装饰器深入

### 函数装饰器

```python
# 基本装饰器
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

# 等价于：add = logger(add)

# 保留元数据
from functools import wraps

def logger(func):
    @wraps(func)  # 保留func的__name__、__doc__等
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 带参数的装饰器

```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}")

greet("Alice")  # 打印3次
```

### 类装饰器

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello")

say_hello()  # Call 1...
say_hello()  # Call 2...
```

### 常用内置装饰器

```python
class MyClass:
    def __init__(self):
        self._value = 0
    
    # property：将方法变为属性
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        if val < 0:
            raise ValueError("Value must be positive")
        self._value = val
    
    @value.deleter
    def value(self):
        del self._value
    
    # classmethod：类方法
    @classmethod
    def from_string(cls, s):
        return cls()
    
    # staticmethod：静态方法
    @staticmethod
    def validate(val):
        return val > 0

# 使用
obj = MyClass()
obj.value = 10  # 调用setter
print(obj.value)  # 调用getter
```

## 生成器高级用法

### 生成器函数

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 使用
gen = fibonacci()
[next(gen) for _ in range(10)]  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# send方法（协程）
def coroutine():
    value = None
    while True:
        value = yield value  # 接收发送的值
        value = value * 2 if value else 0

gen = coroutine()
next(gen)      # 启动生成器
gen.send(5)    # 10
gen.send(10)   # 20
```

### yield from

```python
def generator1():
    yield 1
    yield 2

def generator2():
    yield 3
    yield 4

def combined():
    yield from generator1()  # 委托
    yield from generator2()

list(combined())  # [1, 2, 3, 4]

# 递归生成器
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # 递归展开
        else:
            yield item

list(flatten([1, [2, [3, 4]], 5]))  # [1, 2, 3, 4, 5]
```

## 上下文管理器

### with语句

```python
# 基本用法
with open('file.txt') as f:
    content = f.read()
# 自动调用f.close()

# 多个资源
with open('in.txt') as fin, open('out.txt', 'w') as fout:
    fout.write(fin.read())
```

### 自定义上下文管理器

```python
# 方法1：__enter__和__exit__
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        print(f"Elapsed: {self.end - self.start:.4f}s")
        return False  # 不抑制异常

with Timer():
    time.sleep(1)

# 方法2：contextmanager装饰器
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"Elapsed: {end - start:.4f}s")

with timer():
    time.sleep(1)
```

## 描述符

实现属性访问的底层机制。

```python
class Descriptor:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Must be positive")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Person:
    age = Descriptor('age')  # 描述符
    
    def __init__(self, age):
        self.age = age

p = Person(25)
p.age = 30  # 调用__set__
print(p.age)  # 调用__get__
```

## 元类

类的类，控制类的创建。

```python
# type创建类
MyClass = type('MyClass', (), {'x': 10})

# 自定义元类
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    pass

s1 = Singleton()
s2 = Singleton()
s1 is s2  # True（单例）
```

## 函数式编程

### map/filter/reduce

```python
# map：映射
list(map(lambda x: x**2, [1, 2, 3, 4]))  # [1, 4, 9, 16]

# filter：过滤
list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))  # [2, 4]

# reduce：归约
from functools import reduce
reduce(lambda x, y: x + y, [1, 2, 3, 4])  # 10
```

### 闭包

```python
def outer(x):
    def inner(y):
        return x + y  # 访问外部变量
    return inner

add5 = outer(5)
add5(3)  # 8
add5(10)  # 15

# 工厂函数
def make_multiplier(n):
    return lambda x: x * n

times3 = make_multiplier(3)
times3(10)  # 30
```

### 柯里化

```python
# 普通函数
def add(x, y, z):
    return x + y + z

# 柯里化
def curry_add(x):
    def add_y(y):
        def add_z(z):
            return x + y + z
        return add_z
    return add_y

curry_add(1)(2)(3)  # 6

# 使用partial部分应用
from functools import partial

add3 = partial(add, 1, 2)
add3(3)  # 6
```

## 魔法方法

### 运算符重载

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __len__(self):
        return 2
    
    def __getitem__(self, index):
        return [self.x, self.y][index]
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2      # Vector(4, 6)
v3 * 2            # Vector(8, 12)
v3[0]             # 8
```

### 容器协议

```python
class MyList:
    def __init__(self):
        self.data = []
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        self.data[index] = value
    
    def __delitem__(self, index):
        del self.data[index]
    
    def __contains__(self, item):
        return item in self.data
    
    def __iter__(self):
        return iter(self.data)

lst = MyList()
len(lst)
lst[0]
0 in lst
for item in lst:
    pass
```

## 并发编程基础

### threading

```python
import threading

def worker(name):
    print(f"Worker {name} started")
    time.sleep(1)
    print(f"Worker {name} finished")

# 创建线程
t = threading.Thread(target=worker, args=('A',))
t.start()
t.join()  # 等待结束

# 线程锁
lock = threading.Lock()

def safe_increment():
    with lock:  # 自动获取和释放锁
        global count
        count += 1

# 多个线程
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### multiprocessing

```python
from multiprocessing import Process, Pool, Queue

# 创建进程
def worker(name):
    print(f"Process {name}")

p = Process(target=worker, args=('A',))
p.start()
p.join()

# 进程池
def square(x):
    return x ** 2

with Pool(4) as pool:
    results = pool.map(square, range(10))
    print(results)

# 进程间通信
def producer(queue):
    for i in range(5):
        queue.put(i)

def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(item)

q = Queue()
p1 = Process(target=producer, args=(q,))
p2 = Process(target=consumer, args=(q,))
```

### concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# 线程池
with ThreadPoolExecutor(max_workers=4) as executor:
    # submit提交单个任务
    future = executor.submit(pow, 2, 10)
    result = future.result()  # 1024
    
    # map批量处理
    results = executor.map(lambda x: x**2, range(10))
    
    # as_completed（完成即处理）
    futures = [executor.submit(task, i) for i in range(10)]
    for future in as_completed(futures):
        print(future.result())

# 进程池（CPU密集型）
with ProcessPoolExecutor() as executor:
    results = executor.map(cpu_intensive_task, data)
```

## asyncio（异步编程）

### 协程基础

```python
import asyncio

# 定义协程
async def hello():
    print("Hello")
    await asyncio.sleep(1)  # 异步等待
    print("World")

# 运行协程
asyncio.run(hello())

# 并发执行
async def task(name, delay):
    await asyncio.sleep(delay)
    print(f"Task {name} done")

async def main():
    # 并发3个任务
    await asyncio.gather(
        task('A', 1),
        task('B', 2),
        task('C', 3)
    )

asyncio.run(main())
```

### async/await模式

```python
# 异步HTTP请求（需要aiohttp）
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# 异步文件操作（需要aiofiles）
import aiofiles

async def read_file(filename):
    async with aiofiles.open(filename, 'r') as f:
        return await f.read()

# 创建任务
async def main():
    task1 = asyncio.create_task(fetch(url1))
    task2 = asyncio.create_task(fetch(url2))
    
    result1 = await task1
    result2 = await task2

# 超时控制
async def with_timeout():
    try:
        result = await asyncio.wait_for(slow_task(), timeout=5.0)
    except asyncio.TimeoutError:
        print("Timeout!")
```

## 性能优化

### 列表vs生成器

```python
# 列表：立即计算，占用内存
squares_list = [x**2 for x in range(1000000)]  # ~4MB

# 生成器：惰性求值，节省内存
squares_gen = (x**2 for x in range(1000000))   # ~200字节

# 仅需遍历一次，用生成器
sum(x**2 for x in range(1000000))
```

### 字符串拼接

```python
import timeit

# 慢（每次创建新字符串）
def slow_concat(n):
    s = ""
    for i in range(n):
        s += str(i)
    return s

# 快（一次性分配）
def fast_concat(n):
    return "".join(str(i) for i in range(n))

# 性能对比（n=10000）
# slow: ~50ms
# fast: ~2ms（25倍提升）
```

### 集合查找

```python
# list查找：O(n)
lst = list(range(10000))
5000 in lst  # 遍历查找

# set查找：O(1)
s = set(range(10000))
5000 in s    # 哈希查找

# 频繁查找，list转set
lst = [1, 2, 3, 4, 5]
s = set(lst)
```

### 局部变量优化

```python
# 慢（每次查找全局）
def slow():
    for i in range(1000000):
        result = math.sqrt(i)

# 快（局部变量查找更快）
def fast():
    sqrt = math.sqrt  # 局部化
    for i in range(1000000):
        result = sqrt(i)
```

## slots优化内存

```python
# 普通类（使用__dict__）
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 1000000个对象约占用~300MB

# 使用__slots__
class PointSlots:
    __slots__ = ['x', 'y']  # 固定属性
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 1000000个对象约占用~150MB（节省50%）

# 缺点：不能动态添加属性
p = PointSlots(1, 2)
# p.z = 3  # AttributeError
```

## 内存管理

### 垃圾回收

```python
import gc

# 手动触发GC
gc.collect()

# 禁用/启用GC
gc.disable()
gc.enable()

# 查看引用计数
import sys
x = []
sys.getrefcount(x)  # 引用计数

# 查看内存占用
sys.getsizeof(x)    # 字节数
```

### 弱引用

```python
import weakref

class MyClass:
    pass

obj = MyClass()
ref = weakref.ref(obj)  # 弱引用

ref() is obj    # True
del obj
ref()           # None（对象已被回收）

# WeakValueDictionary（缓存）
cache = weakref.WeakValueDictionary()
obj = MyClass()
cache['key'] = obj  # 对象可被GC回收
```

## 实用技巧

### 解包技巧

```python
# 变量交换
a, b = b, a

# 多值返回
def stats(data):
    return min(data), max(data), sum(data)

minimum, maximum, total = stats([1, 2, 3, 4, 5])

# 扩展解包
a, *middle, b = [1, 2, 3, 4, 5]  # a=1, middle=[2,3,4], b=5

# 字典解包
d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, **d1}  # {'c': 3, 'a': 1, 'b': 2}

# 函数参数解包
args = [1, 2, 3]
kwargs = {'a': 1, 'b': 2}
func(*args, **kwargs)
```

### 链式比较

```python
# 优雅的范围判断
1 < x < 10
a == b == c
x != y != z
```

### enumerate和zip

```python
# enumerate（索引和值）
for i, value in enumerate(['a', 'b', 'c'], start=1):
    print(i, value)  # 1 a, 2 b, 3 c

# zip（并行迭代）
names = ['Alice', 'Bob']
ages = [25, 30]
for name, age in zip(names, ages):
    print(name, age)

# 转置矩阵
matrix = [[1, 2, 3], [4, 5, 6]]
transposed = list(zip(*matrix))  # [(1, 4), (2, 5), (3, 6)]
```

### 海象运算符（:=，Python 3.8+）

```python
# 赋值表达式
if (n := len(data)) > 10:
    print(f"Large dataset: {n} items")

# 避免重复计算
while (line := file.readline()):
    process(line)

# 列表推导式
[y for x in data if (y := transform(x)) > 0]
```

## 性能分析

### cProfile

```python
import cProfile
import pstats

# 分析函数
cProfile.run('slow_function()')

# 保存结果
cProfile.run('slow_function()', 'profile.stats')

# 分析结果
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # 打印前10项
```

### line_profiler

```bash
# 安装
pip install line_profiler

# 使用
@profile
def slow_function():
    # ...

# 运行
kernprof -l -v script.py
```

### memory_profiler

```bash
# 安装
pip install memory_profiler

# 使用
@profile
def memory_intensive():
    # ...

# 运行
python -m memory_profiler script.py
```

## 最佳实践

1. **生成器代替列表**：大数据处理
2. **set查找**：频繁检查成员关系
3. **局部化全局变量**：循环内部
4. **join拼接字符串**：替代+=
5. **__slots__节省内存**：大量小对象
6. **lru_cache缓存**：重复计算
7. **with管理资源**：文件、锁、数据库连接
8. **类型提示**：提高可维护性
9. **asyncio异步**：IO密集型任务
10. **profile指导优化**：测量后优化

**核心：** Python强调简洁和可读性，性能优化基于profiling数据。

