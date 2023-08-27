"""
LeetCode 73. 矩阵置零
https://leetcode.cn/problems/set-matrix-zeroes/

给定一个m x n的矩阵，如果一个元素为0，则将其所在行和列的所有元素都设为0。请使用原地算法。

原地算法

时间复杂度：O(m*n)
空间复杂度：O(1)
"""

def set_zeroes(matrix):
    """
    矩阵置零 - 原地算法
    
    Args:
        matrix: 二维矩阵（原地修改）
    """
    if not matrix or not matrix[0]:
        return
    
    m, n = len(matrix), len(matrix[0])
    
    # 使用第一行和第一列作为标记
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))
    
    # 标记需要置零的行和列
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0  # 标记第i行
                matrix[0][j] = 0  # 标记第j列
    
    # 根据标记置零
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    
    # 处理第一行和第一列
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0


def set_zeroes_extra_space(matrix):
    """
    矩阵置零 - 额外空间法
    
    Args:
        matrix: 二维矩阵（原地修改）
    """
    if not matrix or not matrix[0]:
        return
    
    m, n = len(matrix), len(matrix[0])
    
    # 记录需要置零的行和列
    zero_rows = set()
    zero_cols = set()
    
    # 找到所有0的位置
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                zero_rows.add(i)
                zero_cols.add(j)
    
    # 置零
    for i in range(m):
        for j in range(n):
            if i in zero_rows or j in zero_cols:
                matrix[i][j] = 0


def test_set_zeroes():
    """测试函数"""
    # 测试用例1
    matrix1 = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    matrix1_copy = [row[:] for row in matrix1]
    
    set_zeroes(matrix1)
    set_zeroes_extra_space(matrix1_copy)
    
    print(f"测试1 原矩阵: [[1,1,1],[1,0,1],[1,1,1]]")
    print(f"原地算法结果: {matrix1}")
    print(f"额外空间结果: {matrix1_copy}")
    print(f"期望: [[1,0,1],[0,0,0],[1,0,1]]")
    print()
    
    # 测试用例2
    matrix2 = [
        [0, 1, 2, 0],
        [3, 4, 5, 2],
        [1, 3, 1, 5]
    ]
    matrix2_copy = [row[:] for row in matrix2]
    
    set_zeroes(matrix2)
    set_zeroes_extra_space(matrix2_copy)
    
    print(f"测试2 原矩阵: [[0,1,2,0],[3,4,5,2],[1,3,1,5]]")
    print(f"原地算法结果: {matrix2}")
    print(f"额外空间结果: {matrix2_copy}")
    print(f"期望: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]")


if __name__ == "__main__":
    test_set_zeroes()
