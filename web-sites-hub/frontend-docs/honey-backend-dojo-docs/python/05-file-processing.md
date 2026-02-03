# 05-文件与数据处理

Python在文件处理和数据处理方面功能强大，标准库和第三方库配合使用效率极高。

## 文件操作进阶

### 文件编码处理

```python
# 指定编码（避免乱码）
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 错误处理
with open('file.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# errors选项：
# 'strict'：默认，抛异常
# 'ignore'：忽略错误字符
# 'replace'：用?替代
# 'backslashreplace'：用\xNN替代
```

### 大文件处理

```python
# 逐行读取（节省内存）
with open('large_file.txt', 'r') as f:
    for line in f:  # 迭代器，不会全部加载
        process(line.strip())

# 分块读取
def read_in_chunks(file_path, chunk_size=1024):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

for chunk in read_in_chunks('large_file.bin'):
    process(chunk)
```

### CSV文件

```python
import csv

# 读取CSV
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)  # 跳过表头
    for row in reader:
        print(row)  # 列表

# DictReader（字典形式）
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])

# 写入CSV
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'age'])
    writer.writerows([['Alice', 25], ['Bob', 30]])

# DictWriter
with open('output.csv', 'w', newline='') as f:
    fieldnames = ['name', 'age']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'name': 'Alice', 'age': 25})
```

### JSON处理

```python
import json

# Python ↔ JSON类型映射
# dict → object
# list/tuple → array
# str → string
# int/float → number
# True/False → true/false
# None → null

# 自定义编码器
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class StudentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Student):
            return {'name': obj.name, 'age': obj.age}
        return super().default(obj)

json.dumps(student, cls=StudentEncoder)

# 或使用default参数
json.dumps(student, default=lambda o: o.__dict__)
```

### pickle序列化

```python
import pickle

# 序列化Python对象
data = {'key': 'value', 'number': 42}
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)

# 反序列化
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

# 序列化多个对象
with open('data.pkl', 'wb') as f:
    pickle.dump(obj1, f)
    pickle.dump(obj2, f)

with open('data.pkl', 'rb') as f:
    obj1 = pickle.load(f)
    obj2 = pickle.load(f)
```

## 数据处理

### 列表操作技巧

```python
# 去重（保持顺序）
def unique(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# 展平嵌套列表
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]  # [1,2,3,4,5,6]

# 分组（chunk）
def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

list(chunk([1,2,3,4,5,6,7], 3))  # [[1,2,3], [4,5,6], [7]]

# 滑动窗口
from collections import deque

def sliding_window(lst, n):
    window = deque(maxlen=n)
    for item in lst:
        window.append(item)
        if len(window) == n:
            yield list(window)

list(sliding_window([1,2,3,4,5], 3))  # [[1,2,3], [2,3,4], [3,4,5]]
```

### 字典操作技巧

```python
# 合并字典
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}

# Python 3.9+
merged = d1 | d2  # {'a': 1, 'b': 3, 'c': 4}

# Python 3.5+
merged = {**d1, **d2}

# 传统方法
merged = d1.copy()
merged.update(d2)

# 字典推导式过滤
d = {'a': 1, 'b': 2, 'c': 3}
filtered = {k: v for k, v in d.items() if v > 1}  # {'b': 2, 'c': 3}

# 反转字典
reversed_d = {v: k for k, v in d.items()}

# 分组
from itertools import groupby

data = [('a', 1), ('a', 2), ('b', 3), ('b', 4)]
grouped = {k: list(v) for k, v in groupby(sorted(data), key=lambda x: x[0])}
```

## 正则表达式进阶

### 常用模式

```python
import re

# 手机号
phone = r'1[3-9]\d{9}'

# 邮箱
email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# URL
url = r'https?://[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'

# IPv4
ipv4 = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# 日期
date = r'(\d{4})-(\d{2})-(\d{2})'

# 身份证
id_card = r'\d{17}[\dXx]'
```

### 贪婪vs非贪婪

```python
text = '<div>content</div>'

# 贪婪匹配（默认）
re.findall(r'<.*>', text)   # ['<div>content</div>']（尽可能长）

# 非贪婪匹配
re.findall(r'<.*?>', text)  # ['<div>', '</div>']（尽可能短）
```

### 预编译提升性能

```python
# 重复使用时编译
pattern = re.compile(r'\d+')

for text in large_list:
    pattern.findall(text)  # 比每次re.findall快
```

## 命令行工具

### subprocess

```python
import subprocess

# 执行命令
result = subprocess.run(['ls', '-l'], 
                       capture_output=True, 
                       text=True)
print(result.stdout)
print(result.returncode)

# 管道
p1 = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', 'txt'], stdin=p1.stdout, stdout=subprocess.PIPE)
output, _ = p2.communicate()

# 超时控制
try:
    result = subprocess.run(['sleep', '10'], timeout=5)
except subprocess.TimeoutExpired:
    print("Timeout!")

# 检查返回码
subprocess.run(['false'], check=True)  # 非0退出抛异常
```

### shutil（高级文件操作）

```python
import shutil

# 复制
shutil.copy('src.txt', 'dst.txt')      # 复制文件
shutil.copytree('src_dir', 'dst_dir')  # 复制目录树

# 移动
shutil.move('src', 'dst')

# 删除
shutil.rmtree('dir')  # 删除目录树

# 压缩
shutil.make_archive('archive', 'zip', 'folder')

# 解压
shutil.unpack_archive('archive.zip', 'extract_dir')

# 磁盘使用
usage = shutil.disk_usage('/')
print(f"Total: {usage.total / 1e9:.2f} GB")
print(f"Used: {usage.used / 1e9:.2f} GB")
print(f"Free: {usage.free / 1e9:.2f} GB")
```

## 数据序列化格式对比

| 格式 | 可读性 | 大小 | 速度 | 跨语言 | 场景 |
|------|-------|------|------|--------|------|
| JSON | 高 | 中 | 中 | 是 | 配置、API |
| pickle | 低 | 小 | 快 | 否（仅Python） | 缓存、临时存储 |
| CSV | 高 | 大 | 慢 | 是 | 表格数据 |
| XML | 高 | 大 | 慢 | 是 | 配置、文档 |
| YAML | 高 | 中 | 慢 | 是 | 配置文件 |
| Protocol Buffers | 低 | 小 | 快 | 是 | RPC、大数据 |

**选择：**
- 配置文件：JSON或YAML
- API数据：JSON
- Python内部：pickle
- 表格数据：CSV或Pandas
- 高性能：Protocol Buffers或MessagePack

## glob模式匹配

```python
import glob

# 匹配文件
glob.glob('*.txt')              # 当前目录所有txt
glob.glob('**/*.py', recursive=True)  # 递归查找py文件
glob.glob('[0-9]*.txt')         # 数字开头的txt

# pathlib更现代
from pathlib import Path

list(Path('.').glob('*.txt'))
list(Path('.').rglob('*.py'))   # 递归
```

## 性能对比

### 数据结构选择

```python
import timeit

# 查找性能（10000元素）
# list.index: ~500μs
# set.in: ~0.1μs（5000倍提升）

# 添加性能（10000次）
# list.append: ~500μs
# deque.append: ~300μs
# set.add: ~600μs

# 遍历性能（100000元素）
# for in list: ~5ms
# for in tuple: ~5ms（几乎相同）
# for in generator: ~3ms（省内存）
```

### 字符串拼接

```python
# 慢（O(n²)）
s = ""
for i in range(10000):
    s += str(i)  # 每次创建新字符串

# 快（O(n)）
s = "".join(str(i) for i in range(10000))

# f-string也高效
items = ['a', 'b', 'c']
result = f"{items[0]}, {items[1]}, {items[2]}"
```

## 实用脚本模板

### 文件批量处理

```python
#!/usr/bin/env python3
from pathlib import Path

def process_files(directory, pattern='*.txt'):
    """批量处理文件"""
    for file_path in Path(directory).rglob(pattern):
        process_file(file_path)

def process_file(file_path):
    """处理单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 处理content
        result = content.upper()
    
    # 写入新文件
    output_path = file_path.with_suffix('.processed.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

if __name__ == '__main__':
    process_files('/path/to/files')
```

### 数据清洗脚本

```python
import csv
import re

def clean_data(input_file, output_file):
    """清洗CSV数据"""
    with open(input_file, 'r') as fin, \
         open(output_file, 'w', newline='') as fout:
        
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            # 清洗数据
            row['name'] = row['name'].strip().title()
            row['email'] = row['email'].lower()
            row['age'] = int(row['age']) if row['age'].isdigit() else 0
            
            # 验证
            if validate_row(row):
                writer.writerow(row)

def validate_row(row):
    """验证数据"""
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return (row['name'] and
            row['age'] > 0 and
            re.match(email_pattern, row['email']))
```

### 日志分析脚本

```python
import re
from collections import Counter
from datetime import datetime

def analyze_log(log_file):
    """分析访问日志"""
    ip_counter = Counter()
    status_counter = Counter()
    
    # 日志格式：IP - - [时间] "请求" 状态 大小
    pattern = r'(\d+\.\d+\.\d+\.\d+).*\[(.+?)\].*" (\d{3})'
    
    with open(log_file, 'r') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                ip, timestamp, status = match.groups()
                ip_counter[ip] += 1
                status_counter[status] += 1
    
    # 统计
    print("Top 10 IPs:")
    for ip, count in ip_counter.most_common(10):
        print(f"  {ip}: {count}")
    
    print("\nStatus codes:")
    for status, count in status_counter.most_common():
        print(f"  {status}: {count}")

analyze_log('access.log')
```

## 数据分析基础

### NumPy基础

```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
rand = np.random.rand(3, 3)

# 数组操作
arr + 10       # 向量化操作
arr * 2
arr ** 2
arr > 3        # 布尔索引

# 统计
arr.sum()
arr.mean()
arr.std()
arr.min()
arr.max()

# 索引和切片
arr[0]
arr[1:4]
arr[[0, 2, 4]]  # 花式索引
arr[arr > 3]    # 布尔索引

# 形状操作
arr.reshape(5, 1)
arr.flatten()
arr.T  # 转置
```

### Pandas基础

```python
import pandas as pd

# 创建DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['Beijing', 'Shanghai', 'Guangzhou']
})

# 读取文件
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')

# 查看数据
df.head()      # 前5行
df.tail()      # 后5行
df.info()      # 信息
df.describe()  # 统计摘要

# 选择数据
df['name']     # 列
df[['name', 'age']]  # 多列
df.loc[0]      # 行（标签）
df.iloc[0]     # 行（位置）
df.loc[0, 'name']  # 单元格

# 过滤
df[df['age'] > 25]
df[(df['age'] > 25) & (df['city'] == 'Beijing')]

# 排序
df.sort_values('age')
df.sort_values(['city', 'age'], ascending=[True, False])

# 分组统计
df.groupby('city')['age'].mean()
df.groupby('city').agg({'age': ['mean', 'min', 'max']})

# 新增列
df['adult'] = df['age'] >= 18
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 60, 100], 
                         labels=['child', 'adult', 'senior'])

# 保存
df.to_csv('output.csv', index=False)
df.to_excel('output.xlsx', index=False)
```

## Web抓取

### requests

```python
import requests

# GET请求
response = requests.get('https://api.example.com/data')
print(response.status_code)  # 200
print(response.text)         # 响应文本
data = response.json()       # JSON解析

# POST请求
data = {'key': 'value'}
response = requests.post('https://api.example.com', json=data)

# 请求头
headers = {'User-Agent': 'MyApp/1.0'}
response = requests.get(url, headers=headers)

# 超时
response = requests.get(url, timeout=5)

# Session（保持连接）
session = requests.Session()
session.get(url1)
session.get(url2)  # 复用连接
```

### BeautifulSoup（HTML解析）

```python
from bs4 import BeautifulSoup

html = '''
<html>
    <body>
        <div class="content">
            <h1>Title</h1>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
        </div>
    </body>
</html>
'''

soup = BeautifulSoup(html, 'html.parser')

# 查找
soup.find('h1').text          # 'Title'
soup.find('div', class_='content')
soup.find_all('p')            # 所有p标签
soup.select('.content p')     # CSS选择器

# 遍历
for p in soup.find_all('p'):
    print(p.text)

# 提取属性
link = soup.find('a')
link['href']  # 链接地址
```

## 数据库操作

### SQLite

```python
import sqlite3

# 连接
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    )
''')

# 插入
cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 25))
conn.commit()

# 批量插入
users = [('Bob', 30), ('Charlie', 35)]
cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users)
conn.commit()

# 查询
cursor.execute('SELECT * FROM users WHERE age > ?', (20,))
rows = cursor.fetchall()  # 所有结果
row = cursor.fetchone()   # 单条结果

# 关闭
cursor.close()
conn.close()

# 使用with自动管理
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    # 自动commit和close
```

## 配置文件

### ConfigParser（INI格式）

```python
import configparser

# 读取
config = configparser.ConfigParser()
config.read('config.ini')

value = config['section']['key']
value = config.get('section', 'key', fallback='default')

# 写入
config['NEW_SECTION'] = {'key': 'value'}
with open('config.ini', 'w') as f:
    config.write(f)
```

### YAML（需要PyYAML）

```python
import yaml

# 读取
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 写入
data = {'name': 'Alice', 'scores': [90, 85, 92]}
with open('output.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False)
```

## 最佳实践

1. **with管理文件**：自动关闭
2. **pathlib操作路径**：比os.path更清晰
3. **json处理API数据**：通用格式
4. **csv处理表格数据**：简单高效
5. **正则预编译**：重复使用时
6. **生成器处理大文件**：逐行读取
7. **pandas处理结构化数据**：功能强大
8. **subprocess执行命令**：捕获输出
9. **logging记录日志**：不用print调试
10. **类型提示**：大型项目必备

**核心：** 选择合适的工具处理不同类型的数据，标准库优先。

