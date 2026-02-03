# 03-数据结构与标准库

Python标准库功能强大，涵盖数据结构、文件处理、网络、并发等。"batteries included"理念。

## collections模块

### Counter（计数器）

```python
from collections import Counter

# 创建
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
counter = Counter(words)

print(counter)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# 常用操作
counter.most_common(2)      # [('apple', 3), ('banana', 2)]
counter['apple']            # 3
counter['orange']           # 0（不存在返回0）

# 运算
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
c1 + c2                     # Counter({'a': 4, 'b': 3})
c1 - c2                     # Counter({'a': 2})
c1 & c2                     # Counter({'a': 1, 'b': 1})（最小值）
c1 | c2                     # Counter({'a': 3, 'b': 2})（最大值）

# 应用：单词频率统计
text = "hello world hello python"
Counter(text.split()).most_common()
```

### defaultdict（默认字典）

```python
from collections import defaultdict

# 普通dict问题
d = {}
# d['key'] += 1  # KeyError

# defaultdict解决方案
d = defaultdict(int)  # 默认值0
d['key'] += 1         # OK

# 默认值类型
defaultdict(list)     # []
defaultdict(set)      # set()
defaultdict(lambda: 'default')

# 应用：分组
data = [('a', 1), ('b', 2), ('a', 3)]
grouped = defaultdict(list)
for key, value in data:
    grouped[key].append(value)
# {'a': [1, 3], 'b': [2]}
```

### deque（双端队列）

```python
from collections import deque

# 创建
dq = deque([1, 2, 3])
dq = deque(maxlen=5)  # 限定长度，自动删除旧元素

# 操作（O(1)）
dq.append(4)          # 右端添加
dq.appendleft(0)      # 左端添加
dq.pop()              # 右端删除
dq.popleft()          # 左端删除
dq.extend([5, 6])     # 右端扩展
dq.extendleft([0, -1]) # 左端扩展
dq.rotate(2)          # 右旋转2位

# 应用：滑动窗口、LRU缓存
```

### namedtuple（命名元组）

```python
from collections import namedtuple

# 定义
Point = namedtuple('Point', ['x', 'y'])
Point = namedtuple('Point', 'x y')  # 等价

# 使用
p = Point(3, 4)
p.x            # 3
p[0]           # 3
p._asdict()    # {'x': 3, 'y': 4}

# 不可变
# p.x = 5      # AttributeError

# 应用：轻量级数据类
Person = namedtuple('Person', 'name age city')
alice = Person('Alice', 25, 'Beijing')
```

### OrderedDict（有序字典）

```python
from collections import OrderedDict

# Python 3.7+普通dict也保持插入顺序
# OrderedDict额外提供：
od = OrderedDict()
od['a'] = 1
od['b'] = 2

od.move_to_end('a')   # 移动到末尾
od.popitem(last=False) # 删除第一个
```

### ChainMap（链式字典）

```python
from collections import ChainMap

# 多个字典合并视图
defaults = {'color': 'red', 'user': 'guest'}
user_prefs = {'user': 'admin'}

combined = ChainMap(user_prefs, defaults)
combined['user']   # 'admin'（优先第一个）
combined['color']  # 'red'

# 应用：配置管理（命令行 > 环境变量 > 默认值）
```

## itertools模块

无限迭代器和组合迭代器。

```python
from itertools import *

# 无限迭代器
count(10)          # 10, 11, 12, ...
cycle([1, 2, 3])   # 1, 2, 3, 1, 2, 3, ...
repeat(10, 3)      # 10, 10, 10

# 组合迭代器
chain([1, 2], [3, 4])        # 1, 2, 3, 4
zip_longest([1, 2], [3, 4, 5], fillvalue=0)  # (1,3), (2,4), (0,5)

# 过滤
islice(range(10), 2, 8, 2)   # 2, 4, 6（切片）
takewhile(lambda x: x < 5, [1,2,3,4,5,6])  # 1,2,3,4
dropwhile(lambda x: x < 5, [1,2,3,4,5,6])  # 5,6
filterfalse(lambda x: x % 2, [1,2,3,4])    # 2,4

# 分组
groupby([1,1,2,2,3], key=lambda x: x)

# 组合数学
permutations([1,2,3], 2)     # 排列：(1,2), (1,3), (2,1), ...
combinations([1,2,3], 2)     # 组合：(1,2), (1,3), (2,3)
product([1,2], [3,4])        # 笛卡尔积：(1,3), (1,4), (2,3), (2,4)

# 累积
accumulate([1,2,3,4,5])      # 1, 3, 6, 10, 15（累加）
accumulate([1,2,3,4,5], lambda x,y: x*y)  # 累乘
```

## functools模块

### 高阶函数

```python
from functools import *

# reduce（累积）
reduce(lambda x, y: x + y, [1, 2, 3, 4])  # 10

# partial（偏函数）
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
square(5)      # 25

cube = partial(power, exponent=3)
cube(5)        # 125

# lru_cache（LRU缓存）
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci(100)  # 快速计算（有缓存）
fibonacci.cache_info()  # 查看缓存统计

# wraps（保留元数据）
def decorator(func):
    @wraps(func)  # 保留原函数的__name__、__doc__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# cmp_to_key（排序转换）
sorted([3, 1, 2], key=cmp_to_key(lambda x, y: x - y))
```

## datetime模块

```python
from datetime import datetime, date, time, timedelta

# 当前时间
now = datetime.now()
today = date.today()

# 创建时间
dt = datetime(2024, 1, 1, 12, 30, 45)
d = date(2024, 1, 1)
t = time(12, 30, 45)

# 格式化
dt.strftime("%Y-%m-%d %H:%M:%S")  # "2024-01-01 12:30:45"
dt.isoformat()                     # "2024-01-01T12:30:45"

# 解析
datetime.strptime("2024-01-01", "%Y-%m-%d")

# 时间运算
tomorrow = today + timedelta(days=1)
week_ago = now - timedelta(weeks=1)
diff = dt2 - dt1  # timedelta对象

# 时间戳
dt.timestamp()                     # 秒级时间戳
datetime.fromtimestamp(1234567890) # 时间戳转datetime

# 属性
dt.year, dt.month, dt.day
dt.hour, dt.minute, dt.second
dt.weekday()   # 0=Monday
```

## pathlib模块（路径操作）

```python
from pathlib import Path

# 创建路径
p = Path('folder/file.txt')
p = Path.home() / 'documents' / 'file.txt'  # 路径拼接

# 路径信息
p.name         # 'file.txt'
p.stem         # 'file'
p.suffix       # '.txt'
p.parent       # 'folder'
p.parts        # ('folder', 'file.txt')
p.is_absolute()
p.absolute()   # 绝对路径

# 文件操作
p.exists()     # 是否存在
p.is_file()
p.is_dir()
p.stat()       # 文件信息
p.read_text()  # 读取文本
p.write_text("content")
p.read_bytes()
p.write_bytes(b"content")

# 目录操作
p.mkdir(parents=True, exist_ok=True)
p.rmdir()      # 删除空目录
p.unlink()     # 删除文件

# 遍历
for item in p.iterdir():
    print(item)

# 模式匹配
list(p.glob('*.txt'))          # 当前目录
list(p.rglob('*.txt'))         # 递归查找
```

## re模块（正则表达式）

```python
import re

# 匹配
pattern = r'\d+'
re.match(pattern, '123abc')    # 从头匹配
re.search(pattern, 'abc123')   # 任意位置
re.findall(pattern, '12 34 56')  # ['12', '34', '56']
re.finditer(pattern, '12 34')  # 迭代器

# 替换
re.sub(r'\d+', 'X', 'abc123def456')  # 'abcXdefX'
re.subn(r'\d+', 'X', 'abc123')       # ('abcX', 1)

# 分割
re.split(r'[,;]', 'a,b;c')     # ['a', 'b', 'c']

# 编译（重复使用时提高性能）
pattern = re.compile(r'\d+')
pattern.findall('12 34 56')

# 分组
match = re.search(r'(\d{4})-(\d{2})-(\d{2})', '2024-01-15')
match.group(0)  # '2024-01-15'（整个匹配）
match.group(1)  # '2024'（第一组）
match.groups()  # ('2024', '01', '15')

# 命名分组
match = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})', '2024-01-15')
match.group('year')  # '2024'

# 常用模式
r'\d'          # 数字
r'\w'          # 字母数字下划线
r'\s'          # 空白字符
r'.'           # 任意字符（除换行）
r'^'           # 行首
r'$'           # 行尾
r'*'           # 0次或多次
r'+'           # 1次或多次
r'?'           # 0次或1次
r'{n}'         # 恰好n次
r'{n,m}'       # n到m次
```

## json模块

```python
import json

# Python对象 → JSON字符串
data = {'name': 'Alice', 'age': 25, 'scores': [90, 85, 92]}
json_str = json.dumps(data, indent=2, ensure_ascii=False)

# JSON字符串 → Python对象
obj = json.loads(json_str)

# 文件操作
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('data.json', 'r') as f:
    data = json.load(f)

# 自定义序列化
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def student_encoder(obj):
    if isinstance(obj, Student):
        return {'name': obj.name, 'age': obj.age}
    raise TypeError

json.dumps(student, default=student_encoder)
```

## os和sys模块

### os模块（操作系统接口）

```python
import os

# 当前目录
os.getcwd()
os.chdir('/path')

# 环境变量
os.environ['HOME']
os.getenv('PATH', 'default')

# 文件操作
os.rename('old.txt', 'new.txt')
os.remove('file.txt')
os.mkdir('folder')
os.makedirs('a/b/c', exist_ok=True)
os.rmdir('folder')

# 路径操作
os.path.join('folder', 'file.txt')
os.path.exists('file.txt')
os.path.isfile('file.txt')
os.path.isdir('folder')
os.path.basename('/path/to/file.txt')  # 'file.txt'
os.path.dirname('/path/to/file.txt')   # '/path/to'
os.path.splitext('file.txt')           # ('file', '.txt')

# 执行命令
os.system('ls -l')

# 遍历目录
for root, dirs, files in os.walk('/path'):
    for file in files:
        print(os.path.join(root, file))
```

### sys模块（Python解释器）

```python
import sys

# 命令行参数
sys.argv  # ['script.py', 'arg1', 'arg2']

# 路径
sys.path  # 模块搜索路径
sys.executable  # Python解释器路径

# 版本
sys.version
sys.version_info  # (3, 9, 0, 'final', 0)

# 标准流
sys.stdin
sys.stdout
sys.stderr

# 退出
sys.exit(0)
```

## random模块

```python
import random

# 随机整数
random.randint(1, 10)     # [1, 10]
random.randrange(0, 10, 2)  # [0, 10)，步长2

# 随机浮点数
random.random()           # [0.0, 1.0)
random.uniform(1.0, 10.0) # [1.0, 10.0]

# 序列操作
lst = [1, 2, 3, 4, 5]
random.choice(lst)        # 随机选择一个
random.choices(lst, k=3)  # 可重复选择3个
random.sample(lst, 3)     # 不重复选择3个
random.shuffle(lst)       # 原地洗牌

# 设置种子（可复现）
random.seed(42)
```

## math模块

```python
import math

# 常数
math.pi        # 3.141592653589793
math.e         # 2.718281828459045
math.inf       # 无穷大
math.nan       # NaN

# 基本函数
math.ceil(3.2)   # 4（向上取整）
math.floor(3.8)  # 3（向下取整）
math.trunc(3.8)  # 3（截断）
math.fabs(-5.5)  # 5.5（绝对值）

# 幂和对数
math.sqrt(16)    # 4.0
math.pow(2, 3)   # 8.0
math.log(8, 2)   # 3.0（以2为底）
math.log10(100)  # 2.0
math.log2(8)     # 3.0

# 三角函数
math.sin(math.pi / 2)   # 1.0
math.cos(0)             # 1.0
math.tan(math.pi / 4)   # 1.0

# 其他
math.factorial(5)       # 120
math.gcd(12, 18)        # 6（最大公约数）
math.isnan(x)
math.isinf(x)
```

## copy模块

```python
import copy

# 浅拷贝
lst = [1, 2, [3, 4]]
shallow = lst.copy()           # 或list(lst)或lst[:]
shallow = copy.copy(lst)

lst[2][0] = 999
print(shallow)  # [1, 2, [999, 4]]（内部列表共享！）

# 深拷贝
deep = copy.deepcopy(lst)
lst[2][0] = 100
print(deep)     # [1, 2, [3, 4]]（完全独立）
```

## typing模块（类型提示）

```python
from typing import List, Dict, Set, Tuple, Optional, Union, Callable, Any

# 容器类型
def process(data: List[int]) -> Dict[str, int]:
    return {"sum": sum(data)}

# 可选类型
def find(lst: List[int], target: int) -> Optional[int]:
    return lst.index(target) if target in lst else None

# 联合类型
def parse(value: Union[int, str]) -> int:
    if isinstance(value, int):
        return value
    return int(value)

# Python 3.10+简化
def parse(value: int | str) -> int:
    pass

# 函数类型
Callback = Callable[[int, int], int]

def apply(func: Callback, a: int, b: int) -> int:
    return func(a, b)

# 泛型
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self):
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()
```

## dataclasses（数据类）

```python
from dataclasses import dataclass, field

# 自动生成__init__、__repr__、__eq__等
@dataclass
class Point:
    x: int
    y: int
    z: int = 0  # 默认值

p = Point(3, 4)
print(p)  # Point(x=3, y=4, z=0)

# 更多选项
@dataclass(frozen=True)  # 不可变
class ImmutablePoint:
    x: int
    y: int

@dataclass(order=True)  # 支持比较
class SortablePoint:
    x: int
    y: int

# 字段选项
@dataclass
class Student:
    name: str
    age: int
    scores: List[int] = field(default_factory=list)  # 可变默认值
    internal: str = field(init=False, repr=False)    # 不在__init__和__repr__中
```

## argparse（命令行参数）

```python
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

# 位置参数
parser.add_argument('filename', help='input file')

# 可选参数
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-o', '--output', default='out.txt')
parser.add_argument('-n', '--number', type=int, required=True)

# 选择参数
parser.add_argument('--mode', choices=['fast', 'slow'], default='fast')

args = parser.parse_args()
print(args.filename)
print(args.verbose)
```

## logging（日志）

```python
import logging

# 基本配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

# 日志级别
logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')

# 自定义logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('custom.log')
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('custom log')
```

## 常用模块速查

```python
# 文本处理
string         # 字符串常量和模板
textwrap       # 文本换行和填充

# 数据结构
heapq          # 堆队列
bisect         # 二分查找
array          # 数组（比list省内存）

# 数学
statistics     # 统计函数
decimal        # 精确小数
fractions      # 分数

# 文件格式
csv            # CSV文件
configparser   # INI配置文件
pickle         # 序列化

# 压缩
gzip, bz2, zipfile, tarfile

# 并发
threading      # 线程
multiprocessing # 进程
concurrent.futures  # 高级并发接口
asyncio        # 异步IO

# 网络
socket         # 底层网络
http.server    # HTTP服务器
urllib         # URL处理
requests       # HTTP库（第三方）

# 数据库
sqlite3        # SQLite
```

**核心：** Python标准库功能全面，优先使用标准库而非第三方库。

