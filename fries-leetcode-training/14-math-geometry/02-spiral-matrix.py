"""
LeetCode 54. 螺旋矩阵
https://leetcode.cn/problems/spiral-matrix/

给你一个m行n列的矩阵matrix，请按照顺时针螺旋顺序，返回矩阵中的所有元素。

模拟

时间复杂度：O(m*n)
空间复杂度：O(1)
"""

def spiral_order(matrix):
    """
    螺旋矩阵 - 模拟法
    
    Args:
        matrix: 二维矩阵
        
    Returns:
        螺旋顺序的元素列表
    """
    if not matrix or not matrix[0]:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 从左到右
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        
        # 从上到下
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        # 从右到左
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        
        # 从下到上
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result


def spiral_order_dfs(matrix):
    """
    螺旋矩阵 - DFS法
    
    Args:
        matrix: 二维矩阵
        
    Returns:
        螺旋顺序的元素列表
    """
    if not matrix or not matrix[0]:
        return []
    
    m, n = len(matrix), len(matrix[0])
    visited = [[False] * n for _ in range(m)]
    result = []
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
    direction = 0
    x, y = 0, 0
    
    for _ in range(m * n):
        result.append(matrix[x][y])
        visited[x][y] = True
        
        # 计算下一个位置
        next_x = x + directions[direction][0]
        next_y = y + directions[direction][1]
        
        # 如果下一个位置越界或已访问，改变方向
        if (next_x < 0 or next_x >= m or 
            next_y < 0 or next_y >= n or 
            visited[next_x][next_y]):
            direction = (direction + 1) % 4
            next_x = x + directions[direction][0]
            next_y = y + directions[direction][1]
        
        x, y = next_x, next_y
    
    return result


def test_spiral_order():
    """测试函数"""
    # 测试用例1
    matrix1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    result1 = spiral_order(matrix1)
    result1_dfs = spiral_order_dfs(matrix1)
    print(f"测试1 {matrix1}: Simulate={result1}, DFS={result1_dfs}")  # 期望: [1,2,3,6,9,8,7,4,5]
    
    # 测试用例2
    matrix2 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]
    result2 = spiral_order(matrix2)
    result2_dfs = spiral_order_dfs(matrix2)
    print(f"测试2 {matrix2}: Simulate={result2}, DFS={result2_dfs}")  # 期望: [1,2,3,4,8,12,11,10,9,5,6,7]
    
    # 测试用例3
    matrix3 = [[1]]
    result3 = spiral_order(matrix3)
    result3_dfs = spiral_order_dfs(matrix3)
    print(f"测试3 {matrix3}: Simulate={result3}, DFS={result3_dfs}")  # 期望: [1]


if __name__ == "__main__":
    test_spiral_order()
