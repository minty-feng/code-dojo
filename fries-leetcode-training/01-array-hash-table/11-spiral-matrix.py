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
    螺旋矩阵 - 模拟
    """
    if not matrix or not matrix[0]:
        return []
    
    m, n = len(matrix), len(matrix[0])
    result = []
    top, bottom = 0, m - 1
    left, right = 0, n - 1
    
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

# 测试
if __name__ == "__main__":
    test_cases = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
        [[1, 2, 3]]
    ]
    
    for matrix in test_cases:
        result = spiral_order(matrix)
        print(f"矩阵: {matrix}")
        print(f"螺旋顺序: {result}\n")

