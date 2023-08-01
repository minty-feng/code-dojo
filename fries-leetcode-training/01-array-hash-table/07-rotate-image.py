"""
LeetCode 48. 旋转图像
https://leetcode.cn/problems/rotate-image/

给定一个n×n的二维矩阵matrix表示一个图像。请你将图像顺时针旋转90度。

数学变换：先转置再翻转

时间复杂度：O(n^2)
空间复杂度：O(1)
"""

def rotate(matrix):
    """
    旋转图像 - 先转置再翻转
    """
    n = len(matrix)
    
    # 转置矩阵
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # 翻转每一行
    for i in range(n):
        matrix[i].reverse()

# 测试
if __name__ == "__main__":
    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    print("原矩阵:")
    for row in matrix:
        print(row)
    
    rotate(matrix)
    print("旋转后:")
    for row in matrix:
        print(row)

