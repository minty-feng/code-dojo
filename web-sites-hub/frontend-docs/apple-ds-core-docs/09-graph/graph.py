"""
图的实现和基本算法
"""

from collections import deque, defaultdict


class Graph:
    """图的邻接表实现"""
    
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v, weight=1):
        """添加边"""
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def dfs(self, start):
        """深度优先遍历"""
        visited = set()
        result = []
        
        def dfs_helper(node):
            visited.add(node)
            result.append(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    dfs_helper(neighbor)
        
        dfs_helper(start)
        return result
    
    def bfs(self, start):
        """广度优先遍历"""
        visited = {start}
        queue = deque([start])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def has_cycle(self):
        """检测有向图是否有环"""
        visited = set()
        rec_stack = set()
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False
    
    def topological_sort(self):
        """拓扑排序（Kahn算法）"""
        in_degree = {node: 0 for node in self.graph}
        for node in self.graph:
            for neighbor, _ in self.graph[node]:
                in_degree[neighbor] += 1
        
        queue = [node for node in self.graph if in_degree[node] == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            for neighbor, _ in self.graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result if len(result) == len(self.graph) else None


def dijkstra(graph, start):
    """Dijkstra最短路径算法"""
    import heapq
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
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


def demo():
    """演示图操作"""
    print("=== 图演示 ===\n")
    
    # 创建无向图
    g = Graph(directed=False)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)
    
    print("DFS遍历:", g.dfs(0))
    print("BFS遍历:", g.bfs(0))
    
    # 有向图
    print("\n=== 拓扑排序 ===\n")
    dag = Graph(directed=True)
    dag.add_edge(5, 2)
    dag.add_edge(5, 0)
    dag.add_edge(4, 0)
    dag.add_edge(4, 1)
    dag.add_edge(2, 3)
    dag.add_edge(3, 1)
    
    print("拓扑排序:", dag.topological_sort())
    
    # Dijkstra
    print("\n=== Dijkstra最短路径 ===\n")
    graph_dict = {
        0: [(1, 4), (2, 2)],
        1: [(2, 1), (3, 5)],
        2: [(3, 3)],
        3: []
    }
    distances = dijkstra(graph_dict, 0)
    print("从节点0到各节点的最短距离:", distances)


if __name__ == '__main__':
    demo()

