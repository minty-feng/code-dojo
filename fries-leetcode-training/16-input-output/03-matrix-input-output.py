"""
03-矩阵输入输出处理

题目描述：
演示二维数组（矩阵）的输入输出处理。

输入格式：
第一行：两个整数m, n（矩阵的行数和列数）
接下来m行：每行n个整数

输出格式：
输出矩阵，每行n个整数，空格分隔

示例：
输入：
3 4
1 2 3 4
5 6 7 8
9 10 11 12

输出：
1 2 3 4
5 6 7 8
9 10 11 12
"""

def matrix_input_output():
    """矩阵输入输出处理"""
    # 读取矩阵维度
    m, n = map(int, input().split())
    
    # 读取矩阵
    matrix = []
    for i in range(m):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    # 输出矩阵
    for i in range(m):
        print(*matrix[i])
    
    return matrix

def matrix_operations(matrix):
    """矩阵操作示例"""
    m, n = len(matrix), len(matrix[0])
    
    print(f"矩阵维度: {m} x {n}")
    
    # 计算每行和
    row_sums = [sum(row) for row in matrix]
    print(f"每行和: {row_sums}")
    
    # 计算每列和
    col_sums = [sum(matrix[i][j] for i in range(m)) for j in range(n)]
    print(f"每列和: {col_sums}")
    
    # 计算总和
    total_sum = sum(sum(row) for row in matrix)
    print(f"总和: {total_sum}")

def test_cases():
    """测试用例"""
    print("=== 矩阵输入输出测试 ===")
    
    # 模拟矩阵数据
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]
    
    print("输入矩阵:")
    for row in matrix:
        print(*row)
    
    print("\n矩阵操作:")
    matrix_operations(matrix)

if __name__ == "__main__":
    # 运行测试
    test_cases()
    
    # 交互式输入（取消注释以启用）
    # matrix = matrix_input_output()
    # matrix_operations(matrix)
