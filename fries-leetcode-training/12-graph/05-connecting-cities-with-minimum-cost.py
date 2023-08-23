"""
LeetCode 1135. 连接所有城市的最小成本
https://leetcode.cn/problems/connecting-cities-with-minimum-cost/

想象一下你是个城市基建工程师，城市中有N个城市，编号从1到N。
给你一些可选的连接，其中每个连接connect[i] = [city1, city2, cost]表示将city1和city2连接的成本为cost。

最小生成树（Kruskal算法）

时间复杂度：O(E log E)
空间复杂度：O(V)
"""

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        return True


def minimum_cost(n, connections):
    """
    连接所有城市的最小成本 - Kruskal算法
    
    Args:
        n: 城市数量
        connections: 连接列表，每个连接为[city1, city2, cost]
        
    Returns:
        最小成本，如果无法连接所有城市则返回-1
    """
    if n <= 1:
        return 0
    
    # 按成本排序
    connections.sort(key=lambda x: x[2])
    
    uf = UnionFind(n)
    total_cost = 0
    edges_used = 0
    
    for city1, city2, cost in connections:
        if uf.union(city1 - 1, city2 - 1):  # 转换为0-based索引
            total_cost += cost
            edges_used += 1
            
            if edges_used == n - 1:
                break
    
    return total_cost if edges_used == n - 1 else -1


def minimum_cost_prim(n, connections):
    """
    连接所有城市的最小成本 - Prim算法
    
    Args:
        n: 城市数量
        connections: 连接列表
        
    Returns:
        最小成本
    """
    if n <= 1:
        return 0
    
    import heapq
    
    # 构建邻接表
    graph = [[] for _ in range(n)]
    for city1, city2, cost in connections:
        graph[city1 - 1].append((city2 - 1, cost))
        graph[city2 - 1].append((city1 - 1, cost))
    
    # Prim算法
    visited = [False] * n
    heap = [(0, 0)]  # (cost, city)
    total_cost = 0
    cities_connected = 0
    
    while heap and cities_connected < n:
        cost, city = heapq.heappop(heap)
        
        if visited[city]:
            continue
        
        visited[city] = True
        total_cost += cost
        cities_connected += 1
        
        for neighbor, edge_cost in graph[city]:
            if not visited[neighbor]:
                heapq.heappush(heap, (edge_cost, neighbor))
    
    return total_cost if cities_connected == n else -1


def test_minimum_cost():
    """测试函数"""
    # 测试用例1
    n1 = 3
    connections1 = [[1, 2, 5], [1, 3, 6], [2, 3, 1]]
    result1 = minimum_cost(n1, connections1)
    result1_prim = minimum_cost_prim(n1, connections1)
    print(f"测试1 n={n1}, connections={connections1}: Kruskal={result1}, Prim={result1_prim}")  # 期望: 6
    
    # 测试用例2
    n2 = 4
    connections2 = [[1, 2, 3], [3, 4, 4]]
    result2 = minimum_cost(n2, connections2)
    result2_prim = minimum_cost_prim(n2, connections2)
    print(f"测试2 n={n2}, connections={connections2}: Kruskal={result2}, Prim={result2_prim}")  # 期望: -1


if __name__ == "__main__":
    test_minimum_cost()
