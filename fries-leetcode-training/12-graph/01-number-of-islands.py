"""
LeetCode 200. 岛屿数量
https://leetcode.cn/problems/number-of-islands/

给你一个由'1'（陆地）和'0'（水）组成的二维网格，请你计算网格中岛屿的数量。
岛屿总是被水包围，并且每座岛屿只能由水平方向或竖直方向上相邻的陆地连接形成。

DFS/BFS

时间复杂度：O(m*n)
空间复杂度：O(m*n)
"""

def num_islands(grid):
    """
    岛屿数量 - DFS法
    
    Args:
        grid: 二维网格
        
    Returns:
        岛屿数量
    """
    if not grid or not grid[0]:
        return 0
    
    def dfs(i, j):
        if (i < 0 or i >= len(grid) or 
            j < 0 or j >= len(grid[0]) or 
            grid[i][j] != '1'):
            return
        
        grid[i][j] = '0'  # 标记为已访问
        
        # 四个方向DFS
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    
    return count


def num_islands_bfs(grid):
    """
    岛屿数量 - BFS法
    
    Args:
        grid: 二维网格
        
    Returns:
        岛屿数量
    """
    if not grid or not grid[0]:
        return 0
    
    from collections import deque
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    count = 0
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                queue = deque([(i, j)])
                grid[i][j] = '0'
                
                while queue:
                    x, y = queue.popleft()
                    
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < len(grid) and 
                            0 <= ny < len(grid[0]) and 
                            grid[nx][ny] == '1'):
                            grid[nx][ny] = '0'
                            queue.append((nx, ny))
                
                count += 1
    
    return count


def test_num_islands():
    """测试函数"""
    # 测试用例1
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    result1 = num_islands([row[:] for row in grid1])  # 复制一份避免修改原数组
    print(f"测试1: {result1}")  # 期望: 1
    
    # 测试用例2
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    result2 = num_islands([row[:] for row in grid2])
    print(f"测试2: {result2}")  # 期望: 3


if __name__ == "__main__":
    test_num_islands()