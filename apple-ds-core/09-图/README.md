# 09-图

## 💡 核心结论

### 图的本质
- **定义**：节点（顶点）+ 边的集合，G = (V, E)
- **分类**：有向/无向、有权/无权、连通/非连通
- **存储**：邻接矩阵O(V²)、邻接表O(V+E)
- **遍历**：DFS深度优先、BFS广度优先
- **应用**：社交网络、地图导航、依赖关系

### 存储方式对比
| 方式 | 空间 | 查边 | 遍历邻居 | 适用 |
|------|------|------|----------|------|
| 邻接矩阵 | O(V²) | O(1) | O(V) | 稠密图、需频繁查边 |
| 邻接表 | O(V+E) | O(degree) | O(degree) | 稀疏图、节省空间 |

### 图的遍历
| 算法 | 数据结构 | 空间 | 应用 |
|------|----------|------|------|
| DFS | 栈/递归 | O(V) | 路径、连通性、拓扑排序 |
| BFS | 队列 | O(V) | 最短路径、层级关系 |

### 经典算法
- **最短路径**：Dijkstra、Bellman-Ford、Floyd
- **最小生成树**：Prim、Kruskal
- **拓扑排序**：DFS、Kahn算法
- **强连通分量**：Kosaraju、Tarjan

## 🎯 图的表示

### 邻接矩阵
```python
# 无向图
graph = [
    [0, 1, 1, 0],  # 0连接1,2
    [1, 0, 0, 1],  # 1连接0,3
    [1, 0, 0, 1],  # 2连接0,3
    [0, 1, 1, 0]   # 3连接1,2
]

# 有向图
graph = [
    [0, 1, 0, 0],  # 0→1
    [0, 0, 1, 1],  # 1→2,3
    [0, 0, 0, 1],  # 2→3
    [0, 0, 0, 0]   # 3无出边
]

# 带权图
graph = [
    [0, 4, 2, 0],
    [4, 0, 0, 5],
    [2, 0, 0, 3],
    [0, 5, 3, 0]
]
```

### 邻接表
```python
# 无向图
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# 有向图
graph = {
    0: [1],
    1: [2, 3],
    2: [3],
    3: []
}

# 带权图
graph = {
    0: [(1, 4), (2, 2)],
    1: [(0, 4), (3, 5)],
    2: [(0, 2), (3, 3)],
    3: [(1, 5), (2, 3)]
}
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

### 应用：检测环
```python
def has_cycle(graph):
    visited = set()
    rec_stack = set()
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True  # 找到环
        
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False
```

## 🌊 BFS广度优先

### 最短路径
```python
from collections import deque

def shortest_path(graph, start, end):
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        node, path = queue.popleft()
        
        if node == end:
            return path
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None
```

## 🛤️ 拓扑排序

### Kahn算法（BFS）
```python
def topological_sort(graph):
    # 计算入度
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    # 入度为0的节点入队
    queue = [node for node in graph if in_degree[node] == 0]
    result = []
    
    while queue:
        node = queue.pop(0)
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == len(graph) else None
```

## 🎯 最短路径算法

### Dijkstra算法（单源最短路径）
```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_dist > distances[curr_node]:
            continue
        
        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
```

### Floyd算法（所有点对最短路径）
```python
def floyd(graph):
    n = len(graph)
    dist = [[float('inf')] * n for _ in range(n)]
    
    # 初始化
    for i in range(n):
        dist[i][i] = 0
        for j in range(n):
            if graph[i][j] != 0:
                dist[i][j] = graph[i][j]
    
    # Floyd
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    return dist
```

## 🌳 最小生成树

### Kruskal算法（并查集）
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
        if px != py:
            self.parent[px] = py
            return True
        return False

def kruskal(n, edges):
    # edges: [(weight, u, v)]
    edges.sort()  # 按权重排序
    uf = UnionFind(n)
    mst = []
    total_weight = 0
    
    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_weight += weight
    
    return mst, total_weight
```

## 📚 LeetCode练习

### 基础
- [200. Number of Islands](https://leetcode.com/problems/number-of-islands/)
- [133. Clone Graph](https://leetcode.com/problems/clone-graph/)
- [207. Course Schedule](https://leetcode.com/problems/course-schedule/)

### 进阶
- [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/)
- [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/)
- [785. Is Graph Bipartite](https://leetcode.com/problems/is-graph-bipartite/)

