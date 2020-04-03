# 02-搜索算法

## 💡 核心结论

### 二分查找
- **前提**：有序数组
- **原理**：每次排除一半，O(log n)
- **关键**：左右边界、while条件、mid计算
- **变种**：查找第一个/最后一个、查找范围
- **应用**：搜索、求根、最优化问题

### 深度优先搜索（DFS）
- **策略**：一条路走到底，走不通回退
- **实现**：递归或栈
- **应用**：路径搜索、连通性、拓扑排序
- **复杂度**：O(V + E)

### 广度优先搜索（BFS）
- **策略**：逐层搜索，找最短路径
- **实现**：队列
- **应用**：最短路径、层序遍历
- **复杂度**：O(V + E)

### DFS vs BFS
| 特性 | DFS | BFS |
|------|-----|-----|
| 数据结构 | 栈/递归 | 队列 |
| 空间 | O(h) | O(w) |
| 最短路径 | ❌ | ✅ |
| 实现 | 更简洁 | 需要队列 |
| 适用 | 路径、连通性 | 最短路径、层序 |

## 🔍 二分查找

### 基本模板
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # 避免溢出
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # 未找到
```

### 左边界查找
```python
def left_bound(arr, target):
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

### 右边界查找
```python
def right_bound(arr, target):
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left - 1
```

## 🌲 DFS深度优先

### 递归实现
```python
def dfs(graph, node, visited):
    visited.add(node)
    print(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

### 栈实现
```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node)
            
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
```

## 🌊 BFS广度优先

### 队列实现
```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### 分层BFS
```python
def bfs_levels(graph, start):
    visited = set([start])
    queue = deque([start])
    level = 0
    
    while queue:
        size = len(queue)
        print(f"Level {level}:")
        
        for _ in range(size):
            node = queue.popleft()
            print(f"  {node}")
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        level += 1
```

## 📚 LeetCode练习

### 二分查找
- [704. Binary Search](https://leetcode.com/problems/binary-search/)
- [34. Find First and Last Position](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
- [69. Sqrt(x)](https://leetcode.com/problems/sqrtx/)
- [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)

### DFS/BFS
- [200. Number of Islands](https://leetcode.com/problems/number-of-islands/)
- [207. Course Schedule](https://leetcode.com/problems/course-schedule/)
- [133. Clone Graph](https://leetcode.com/problems/clone-graph/)
- [127. Word Ladder](https://leetcode.com/problems/word-ladder/)

