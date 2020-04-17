# 04-递归与回溯

## 💡 核心结论

### 递归本质
- **定义**：函数调用自己，将大问题分解为小问题
- **三要素**：递归边界、递归规则、返回值
- **关键**：明确函数定义，相信递归，不要跳进递归
- **代价**：栈空间O(递归深度)，可能栈溢出
- **优化**：记忆化、尾递归、改迭代

### 回溯本质
- **定义**：暴力搜索 + 剪枝，试探所有可能
- **模板**：选择→递归→撤销选择
- **关键**：路径、选择列表、结束条件
- **剪枝**：提前排除不可能的分支
- **应用**：全排列、组合、子集、N皇后

### 递归 vs 迭代
| 特性 | 递归 | 迭代 |
|------|------|------|
| 代码 | 简洁优雅 | 相对复杂 |
| 空间 | O(递归深度) | O(1) |
| 性能 | 函数调用开销 | 更快 |
| 适用 | 树、分治、回溯 | 简单循环 |

### 回溯模板（背下来）
```python
result = []

def backtrack(路径, 选择列表):
    if 满足结束条件:
        result.add(路径)
        return
    
    for 选择 in 选择列表:
        做选择
        backtrack(路径, 新选择列表)
        撤销选择
```

## 🎯 经典递归问题

### 1. 阶乘
```python
def factorial(n):
    if n <= 1:  # 递归边界
        return 1
    return n * factorial(n - 1)  # 递归规则
```

### 2. 斐波那契
```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

### 3. 二叉树遍历
```python
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)
```

### 4. 汉诺塔
```python
def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk from {source} to {target}")
        return
    
    hanoi(n - 1, source, auxiliary, target)
    print(f"Move disk from {source} to {target}")
    hanoi(n - 1, auxiliary, target, source)
```

## 🔙 回溯算法

### 1. 全排列
```python
def permute(nums):
    result = []
    
    def backtrack(path, choices):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(choices)):
            # 做选择
            path.append(choices[i])
            # 递归
            backtrack(path, choices[:i] + choices[i+1:])
            # 撤销选择
            path.pop()
    
    backtrack([], nums)
    return result
```

### 2. 组合
```python
def combine(n, k):
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result
```

### 3. 子集
```python
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        result.append(path[:])  # 每个状态都是一个子集
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result
```

### 4. N皇后
```python
def solve_n_queens(n):
    result = []
    board = [['.'] * n for _ in range(n)]
    
    def is_valid(row, col):
        # 检查列
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # 检查左上对角线
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # 检查右上对角线
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(row):
        if row == n:
            result.append([''.join(row) for row in board])
            return
        
        for col in range(n):
            if is_valid(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
    
    backtrack(0)
    return result
```

### 5. 括号生成
```python
def generate_parenthesis(n):
    result = []
    
    def backtrack(path, left, right):
        if len(path) == 2 * n:
            result.append(path)
            return
        
        if left < n:
            backtrack(path + '(', left + 1, right)
        if right < left:
            backtrack(path + ')', left, right + 1)
    
    backtrack('', 0, 0)
    return result
```

## 🎯 剪枝优化

### 1. 提前返回
```python
def backtrack(path):
    if 当前路径不可能产生解:
        return  # 剪枝
    
    if 找到解:
        result.append(path)
        return
    
    for choice in choices:
        backtrack(...)
```

### 2. 去重
```python
def permute_unique(nums):
    nums.sort()  # 先排序
    result = []
    used = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            # 剪枝：跳过重复元素
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
    
    backtrack([])
    return result
```

## 📚 LeetCode练习

### 递归
- [509. Fibonacci Number](https://leetcode.com/problems/fibonacci-number/)
- [344. Reverse String](https://leetcode.com/problems/reverse-string/)
- [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)

### 回溯
- [46. Permutations](https://leetcode.com/problems/permutations/)
- [77. Combinations](https://leetcode.com/problems/combinations/)
- [78. Subsets](https://leetcode.com/problems/subsets/)
- [51. N-Queens](https://leetcode.com/problems/n-queens/)
- [22. Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)
- [39. Combination Sum](https://leetcode.com/problems/combination-sum/)

## 💡 解题技巧

### 递归三问
1. 递归函数的定义是什么？
2. 递归的终止条件是什么？
3. 递归如何缩小问题规模？

### 回溯三步
1. 路径：已做的选择
2. 选择列表：当前可以做的选择
3. 结束条件：到达决策树底层

### 优化方向
1. 剪枝：提前排除无效分支
2. 去重：避免重复计算
3. 记忆化：存储子问题结果
4. 改DP：自底向上

