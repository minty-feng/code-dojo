"""
DFS和BFS实现
"""

from collections import deque

# ========== DFS深度优先 ==========

def dfs_recursive(graph, start, visited=None):
    """DFS递归实现"""
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start, end=' ')
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    
    return visited


def dfs_iterative(graph, start):
    """DFS迭代实现（栈）"""
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            
            # 逆序添加邻居（保证顺序）
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result


# ========== BFS广度优先 ==========

def bfs(graph, start):
    """BFS实现（队列）"""
    visited = {start}
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result


def bfs_shortest_path(graph, start, end):
    """BFS求最短路径"""
    if start == end:
        return [start]
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    
    return None


def bfs_levels(graph, start):
    """BFS分层遍历"""
    visited = {start}
    queue = deque([start])
    levels = []
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        levels.append(current_level)
    
    return levels


# ========== 应用：岛屿数量 ==========

def num_islands(grid):
    """岛屿数量（DFS）"""
    if not grid:
        return 0
    
    m, n = len(grid), len(grid[0])
    count = 0
    
    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == '0':
            return
        
        grid[i][j] = '0'  # 标记已访问
        
        # 四个方向
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    
    return count


# ========== 应用：课程表（拓扑排序） ==========

def can_finish(num_courses, prerequisites):
    """判断能否完成所有课程（检测环）"""
    graph = [[] for _ in range(num_courses)]
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    visited = [0] * num_courses  # 0:未访问 1:访问中 2:已完成
    
    def has_cycle(node):
        if visited[node] == 1:
            return True  # 发现环
        if visited[node] == 2:
            return False
        
        visited[node] = 1
        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True
        visited[node] = 2
        return False
    
    for i in range(num_courses):
        if visited[i] == 0:
            if has_cycle(i):
                return False
    
    return True


def demo():
    """演示DFS和BFS"""
    print("=== DFS和BFS演示 ===\n")
    
    # 构建图
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    print("图结构:")
    for node, neighbors in graph.items():
        print(f"  {node}: {neighbors}")
    print()
    
    print("DFS遍历（递归）: ", end='')
    dfs_recursive(graph, 'A')
    print("\n")
    
    print("DFS遍历（迭代）:", dfs_iterative(graph, 'A'))
    print("BFS遍历:", bfs(graph, 'A'))
    print()
    
    # 最短路径
    path = bfs_shortest_path(graph, 'A', 'F')
    print(f"从A到F的最短路径: {' -> '.join(path) if path else 'None'}")
    print()
    
    # 分层遍历
    print("BFS分层遍历:")
    levels = bfs_levels(graph, 'A')
    for i, level in enumerate(levels):
        print(f"  Level {i}: {level}")
    print()
    
    # 岛屿数量
    grid = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1']
    ]
    print("岛屿数量:")
    for row in grid:
        print(f"  {row}")
    # 注意：会修改grid，这里重新创建
    grid_copy = [row[:] for row in grid]
    print(f"岛屿数量: {num_islands(grid_copy)}")


if __name__ == '__main__':
    demo()

