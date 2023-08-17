"""
LeetCode 51. N皇后
https://leetcode.cn/problems/n-queens/

按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。
n皇后问题研究的是如何将n个皇后放置在n×n的棋盘上，并且使皇后彼此之间不能相互攻击。

回溯

时间复杂度：O(N!)
空间复杂度：O(N)
"""

def solve_n_queens(n):
    """
    N皇后 - 回溯法
    
    Args:
        n: 棋盘大小
        
    Returns:
        所有解决方案
    """
    result = []
    
    def is_valid(board, row, col):
        """检查在(row, col)放置皇后是否有效"""
        # 检查列
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # 检查左上对角线
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # 检查右上对角线
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(board, row):
        if row == n:
            result.append([''.join(row) for row in board])
            return
        
        for col in range(n):
            if is_valid(board, row, col):
                board[row][col] = 'Q'
                backtrack(board, row + 1)
                board[row][col] = '.'  # 回溯
    
    board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(board, 0)
    return result


def test_solve_n_queens():
    """测试函数"""
    # 测试用例1
    n1 = 4
    result1 = solve_n_queens(n1)
    print(f"测试1 n=4:")
    for i, solution in enumerate(result1):
        print(f"解决方案 {i+1}:")
        for row in solution:
            print(row)
        print()
    
    # 测试用例2
    n2 = 1
    result2 = solve_n_queens(n2)
    print(f"测试2 n=1: {result2}")


if __name__ == "__main__":
    test_solve_n_queens()
