"""
LeetCode 37. 解数独
https://leetcode.cn/problems/sudoku-solver/

编写一个程序，通过填充空格来解决数独问题。

回溯

时间复杂度：O(9^(空格数))
空间复杂度：O(1)
"""

def solve_sudoku(board):
    """
    解数独 - 回溯法
    
    Args:
        board: 9x9数独棋盘
        
    Returns:
        None (原地修改)
    """
    def is_valid(board, row, col, num):
        """检查在(row, col)放置num是否有效"""
        # 检查行
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # 检查列
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # 检查3x3宫格
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def backtrack():
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for num in '123456789':
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if backtrack():
                                return True
                            board[i][j] = '.'  # 回溯
                    return False
        return True
    
    backtrack()


def test_solve_sudoku():
    """测试函数"""
    # 测试用例
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    
    print("原始数独:")
    for row in board:
        print(row)
    
    solve_sudoku(board)
    
    print("\n解数独后:")
    for row in board:
        print(row)


if __name__ == "__main__":
    test_solve_sudoku()
