# 12-graph (图)

LeetCode精选75题 - 图专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 岛屿数量 | ⭐⭐ | [200](https://leetcode.cn/problems/number-of-islands/) | [01-number-of-islands.py](./01-number-of-islands.py) | [01-number-of-islands.cpp](./01-number-of-islands.cpp) |
| 02 | 课程表 | ⭐⭐ | [207](https://leetcode.cn/problems/course-schedule/) | [02-course-schedule.py](./02-course-schedule.py) | [02-course-schedule.cpp](./02-course-schedule.cpp) |
| 03 | 课程表II | ⭐⭐ | [210](https://leetcode.cn/problems/course-schedule-ii/) | [03-course-schedule-ii.py](./03-course-schedule-ii.py) | [03-course-schedule-ii.cpp](./03-course-schedule-ii.cpp) |
| 04 | 冗余连接 | ⭐⭐ | [684](https://leetcode.cn/problems/redundant-connection/) | [04-redundant-connection.py](./04-redundant-connection.py) | [04-redundant-connection.cpp](./04-redundant-connection.cpp) |
| 05 | 最小生成树 | ⭐⭐ | [1135](https://leetcode.cn/problems/connecting-cities-with-minimum-cost/) | [05-connecting-cities-with-minimum-cost.py](./05-connecting-cities-with-minimum-cost.py) | [05-connecting-cities-with-minimum-cost.cpp](./05-connecting-cities-with-minimum-cost.cpp) |
| 06 | 最短路径 | ⭐⭐ | [743](https://leetcode.cn/problems/network-delay-time/) | [06-network-delay-time.py](./06-network-delay-time.py) | [06-network-delay-time.cpp](./06-network-delay-time.cpp) |

## 🎯 核心技巧

### DFS/BFS
- **[岛屿数量](./01-number-of-islands.py)**：DFS或BFS遍历连通分量

### 拓扑排序
- **[课程表](./02-course-schedule.py)**：检测有向图是否有环
- **[课程表II](./03-course-schedule-ii.py)**：拓扑排序序列

### 并查集
- **[冗余连接](./04-redundant-connection.py)**：检测环

### 最小生成树
- **[最小生成树](./05-connecting-cities-with-minimum-cost.py)**：Kruskal算法

### 最短路径
- **[最短路径](./06-network-delay-time.py)**：Dijkstra算法

---

## 💡 解题模板

### DFS模板
```python
def dfs(grid, i, j):
    if (i < 0 or i >= len(grid) or 
        j < 0 or j >= len(grid[0]) or 
        grid[i][j] != '1'):
        return
    
    grid[i][j] = '0'  # 标记为已访问
    dfs(grid, i+1, j)
    dfs(grid, i-1, j)
    dfs(grid, i, j+1)
    dfs(grid, i, j-1)
```

### 拓扑排序模板
```python
def topological_sort(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    queue = [i for i in range(num_courses) if indegree[i] == 0]
    result = []
    
    while queue:
        course = queue.pop(0)
        result.append(course)
        
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)
    
    return result if len(result) == num_courses else []
```

### 并查集模板
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        self.parent[px] = py
        return True
```

---

## 📚 学习重点

1. **图的表示**：邻接表、邻接矩阵
2. **遍历算法**：DFS、BFS
3. **拓扑排序**：检测有向无环图
4. **并查集**：检测环、连通分量
5. **最小生成树**：Kruskal、Prim算法
6. **最短路径**：Dijkstra、Floyd算法
