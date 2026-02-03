# 02-栈与队列

## 💡 核心结论

### 栈（Stack）
- **特性**：LIFO（后进先出），只能在栈顶操作
- **操作**：push、pop、peek 全部O(1)
- **实现**：数组栈（缓存友好）或链式栈（动态大小）
- **应用**：函数调用、表达式求值、括号匹配、撤销操作
- **关键**：限制访问顺序，强制后进先出

### 队列（Queue）
- **特性**：FIFO（先进先出），队尾入队头出
- **操作**：enqueue、dequeue、front 全部O(1)
- **循环队列**：用模运算实现，需要一个空位区分满和空
- **应用**：任务调度、BFS、消息队列、打印队列
- **关键**：公平性，先到先服务

### 实现对比
| 实现方式 | 优点 | 缺点 |
|---------|------|------|
| 数组栈/队列 | 缓存友好、实现简单 | 需要扩容或固定大小 |
| 链式栈/队列 | 动态大小、无需扩容 | 指针开销、缓存不友好 |

## 📚 栈（Stack）

### 特点
- **LIFO**（Last In First Out）后进先出
- 只能在栈顶操作
- 主要操作：push、pop、peek

### 应用场景
- 函数调用栈
- 表达式求值
- 括号匹配
- 浏览器历史记录（后退）
- 撤销操作

### 时间复杂度
| 操作 | 复杂度 |
|------|--------|
| push | O(1) |
| pop | O(1) |
| peek | O(1) |
| search | O(n) |

## 🎯 队列（Queue）

### 特点
- **FIFO**（First In First Out）先进先出
- 队尾入队，队头出队
- 主要操作：enqueue、dequeue、front

### 应用场景
- 任务调度
- 广度优先搜索（BFS）
- 消息队列
- 打印队列
- 操作系统进程调度

### 循环队列
```
[front] [1] [2] [3] [4] [rear]
         ↑              ↑
       front          rear

当rear到末尾时，从头开始
[3] [4] [rear] [front] [1] [2]
         ↑              ↑
       rear          front
```

### 时间复杂度
| 操作 | 复杂度 |
|------|--------|
| enqueue | O(1) |
| dequeue | O(1) |
| front | O(1) |
| search | O(n) |

## 🔧 栈的实现方式

### 数组栈
优点：
- 实现简单
- 缓存友好

缺点：
- 需要预分配空间或动态扩容
- 扩容时需要拷贝

### 链式栈
优点：
- 动态大小
- 无需扩容

缺点：
- 额外指针开销
- 缓存不友好

## 🔧 队列的实现方式

### 数组队列（循环队列）
- 使用模运算实现循环
- 需要一个空位区分满和空
- front == rear：队列为空
- (rear + 1) % capacity == front：队列满

### 链式队列
- 维护head和tail指针
- 无需考虑满的情况
- 动态大小

## 💡 经典问题

### 用栈实现括号匹配
```python
def is_valid(s):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in s:
        if char in pairs:
            stack.append(char)
        elif not stack or pairs[stack.pop()] != char:
            return False
    
    return not stack

# 测试
print(is_valid("()[]{}"))  # True
print(is_valid("([)]"))    # False
```

### 用栈计算后缀表达式
```python
def eval_rpn(tokens):
    stack = []
    
    for token in tokens:
        if token in ['+', '-', '*', '/']:
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            else: stack.append(int(a / b))
        else:
            stack.append(int(token))
    
    return stack[0]

# 测试: ["2", "1", "+", "3", "*"] = (2 + 1) * 3 = 9
print(eval_rpn(["2", "1", "+", "3", "*"]))  # 9
```

### 用队列实现BFS
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        print(node, end=' ')
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# 测试
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
bfs(graph, 'A')  # A B C D E F
```

### 单调栈
```python
def next_greater_element(nums):
    """找每个元素右边第一个比它大的元素"""
    result = [-1] * len(nums)
    stack = []  # 单调递减栈
    
    for i in range(len(nums)):
        while stack and nums[i] > nums[stack[-1]]:
            index = stack.pop()
            result[index] = nums[i]
        stack.append(i)
    
    return result

# 测试
print(next_greater_element([2, 1, 2, 4, 3]))  # [4, 2, 4, -1, -1]
```

## 📚 LeetCode练习

### 栈
- [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)
- [155. Min Stack](https://leetcode.com/problems/min-stack/)
- [150. Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)
- [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)

### 队列
- [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/)
- [622. Design Circular Queue](https://leetcode.com/problems/design-circular-queue/)
- [225. Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/)

## 💡 最佳实践

1. **选择合适的实现**
   - 大小固定 → 数组实现
   - 大小动态 → 链表实现

2. **异常处理**
   - 检查空栈/空队列
   - 检查满队列

3. **性能优化**
   - 循环队列避免元素移动
   - 使用数组实现提高缓存命中

4. **代码质量**
   - 封装良好
   - 接口清晰
   - 异常安全

## 💻 完整代码实现

### Python 实现

#### 栈实现

```{literalinclude} stack.py
:language: python
:linenos:
```

#### 队列实现

```{literalinclude} queue.py
:language: python
:linenos:
```

### C++ 实现

#### 栈实现

```{literalinclude} stack.cpp
:language: cpp
:linenos:
```

#### 队列实现

```{literalinclude} queue.cpp
:language: cpp
:linenos:
```

