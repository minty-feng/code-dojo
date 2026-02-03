# 10-并查集（Union-Find）

## 💡 核心结论

### 并查集本质
- **定义**：维护元素分组，支持快速合并和查询
- **核心操作**：union（合并）、find（查找）
- **时间复杂度**：接近O(1)（α(n)，阿克曼函数的反函数）
- **空间复杂度**：O(n)
- **应用**：连通性问题、最小生成树、动态连通性

### 两大优化
1. **路径压缩**：查找时将路径上所有节点直接连到根
2. **按秩合并**：小树合并到大树，保持树的平衡

### 优化效果
| 优化 | 时间复杂度 |
|------|-----------|
| 无优化 | O(n) |
| 只路径压缩 | O(log n) |
| 只按秩合并 | O(log n) |
| 两者结合 | O(α(n)) ≈ O(1) |

### 应用场景（重要）
- **连通性问题**：判断两点是否连通
- **最小生成树**：Kruskal算法
- **动态连通性**：动态添加边
- **朋友圈问题**：社交网络分组
- **岛屿数量**：DFS的替代方案

## 🎯 基本实现

### 简单版本
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        """查找根节点"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]
    
    def union(self, x, y):
        """合并两个集合"""
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[px] = py
            return True
        return False
    
    def connected(self, x, y):
        """判断是否连通"""
        return self.find(x) == self.find(y)
```

### 完整版本（按秩合并）
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # 连通分量数
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        # 按秩合并
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        
        self.count -= 1
        return True
    
    def get_count(self):
        """获取连通分量数"""
        return self.count
```

## 📚 经典问题

### 1. 岛屿数量
```python
def num_islands(grid):
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    uf = UnionFind(m * n)
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                for di, dj in [(0,1), (1,0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == '1':
                        uf.union(i * n + j, ni * n + nj)
    
    # 统计连通分量
    return sum(1 for i in range(m) for j in range(n) 
               if grid[i][j] == '1' and uf.find(i * n + j) == i * n + j)
```

### 2. 朋友圈数量
```python
def find_circle_num(is_connected):
    n = len(is_connected)
    uf = UnionFind(n)
    
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j] == 1:
                uf.union(i, j)
    
    return uf.get_count()
```

### 3. 冗余连接
```python
def find_redundant_connection(edges):
    """找到使图成环的最后一条边"""
    n = len(edges)
    uf = UnionFind(n + 1)
    
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    
    return []
```

## 📚 LeetCode练习

- [200. Number of Islands](https://leetcode.com/problems/number-of-islands/)
- [547. Number of Provinces](https://leetcode.com/problems/number-of-provinces/)
- [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/)
- [721. Accounts Merge](https://leetcode.com/problems/accounts-merge/)
- [1319. Number of Operations to Make Network Connected](https://leetcode.com/problems/number-of-operations-to-make-network-connected/)

## 💻 完整代码实现

### Python 实现

```{literalinclude} union_find.py
:language: python
:linenos:
```

### C++ 实现

```{literalinclude} union_find.cpp
:language: cpp
:linenos:
```

