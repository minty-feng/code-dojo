"""
NC109 岛屿数量
https://www.nowcoder.com/practice/0c9664d1554e466aa107d899418e8145

给一个01矩阵，1代表是陆地，0代表海洋，如果两个1相邻，那么这两个1属于同一个岛。
我们只考虑上下左右为相邻。岛屿: 相邻陆地可以组成一个岛屿。

解法1：DFS
解法2：BFS  
解法3：并查集

时间复杂度：O(n*m)
空间复杂度：O(n*m)
"""

def num_islands_dfs(grid):
    """
    方法1：DFS深度优先搜索
    """
    if not grid or not grid[0]:
        return 0
    
    m, n = len(grid), len(grid[0])
    count = 0
    
    def dfs(i, j):
        # 边界检查
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == '0':
            return
        
        # 标记已访问
        grid[i][j] = '0'
        
        # 四个方向搜索
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

def num_islands_bfs(grid):
    """
    方法2：BFS广度优先搜索
    """
    if not grid or not grid[0]:
        return 0
    
    from collections import deque
    
    m, n = len(grid), len(grid[0])
    count = 0
    
    def bfs(i, j):
        queue = deque([(i, j)])
        grid[i][j] = '0'
        
        while queue:
            x, y = queue.popleft()
            
            # 四个方向
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == '1':
                    grid[nx][ny] = '0'
                    queue.append((nx, ny))
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                bfs(i, j)
    
    return count

# 测试
if __name__ == "__main__":
    grid = [
        ['1', '1', '0', '0', '0'],
        ['0', '1', '0', '1', '1'],
        ['0', '0', '0', '1', '1'],
        ['0', '0', '0', '0', '0'],
        ['0', '0', '1', '1', '1']
    ]
    
    # 需要复制grid因为会修改
    grid_copy = [row[:] for row in grid]
    
    count = num_islands_dfs(grid_copy)
    print(f"岛屿数量: {count}")

