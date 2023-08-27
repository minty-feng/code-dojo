"""
LeetCode 48. 旋转图像
https://leetcode.cn/problems/rotate-image/

给定一个n×n的二维矩阵matrix表示一个图像。请你将图像顺时针旋转90度。

数学变换

时间复杂度：O(n²)
空间复杂度：O(1)
"""

def rotate_matrix(matrix):
    """
    旋转图像 - 数学变换法
    
    Args:
        matrix: n×n的二维矩阵
        
    Returns:
        None (原地修改)
    """
    n = len(matrix)
    
    # 转置矩阵
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # 翻转每一行
    for i in range(n):
        matrix[i].reverse()


def rotate_matrix_step_by_step(matrix):
    """
    旋转图像 - 分步法
    
    Args:
        matrix: n×n的二维矩阵
        
    Returns:
        None (原地修改)
    """
    n = len(matrix)
    
    # 按层旋转
    for layer in range(n // 2):
        first = layer
        last = n - 1 - layer
        
        for i in range(first, last):
            offset = i - first
            
            # 保存上边
            top = matrix[first][i]
            
            # 左边 -> 上边
            matrix[first][i] = matrix[last - offset][first]
            
            # 下边 -> 左边
            matrix[last - offset][first] = matrix[last][last - offset]
            
            # 右边 -> 下边
            matrix[last][last - offset] = matrix[i][last]
            
            # 上边 -> 右边
            matrix[i][last] = top


def test_rotate_matrix():
    """测试函数"""
    # 测试用例1: 3x3矩阵
    matrix1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    print("原始矩阵:")
    for row in matrix1:
        print(row)
    
    rotate_matrix(matrix1)
    
    print("旋转90度后:")
    for row in matrix1:
        print(row)
    # 期望: [[7,4,1],[8,5,2],[9,6,3]]
    
    print()
    
    # 测试用例2: 4x4矩阵
    matrix2 = [
        [5, 1, 9, 11],
        [2, 4, 8, 10],
        [13, 3, 6, 7],
        [15, 14, 12, 16]
    ]
    
    print("原始矩阵:")
    for row in matrix2:
        print(row)
    
    rotate_matrix(matrix2)
    
    print("旋转90度后:")
    for row in matrix2:
        print(row)


if __name__ == "__main__":
    test_rotate_matrix()
