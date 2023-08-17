"""
LeetCode 79. 单词搜索
https://leetcode.cn/problems/word-search/

给定一个m x n二维字符网格board和一个字符串单词word。
如果word存在于网格中，返回true；否则，返回false。

DFS回溯

时间复杂度：O(m*n*4^L) L为单词长度
空间复杂度：O(L)
"""

def exist(board, word):
    """
    单词搜索 - DFS回溯法
    
    Args:
        board: 二维字符网格
        word: 要搜索的单词
        
    Returns:
        是否存在该单词
    """
    if not board or not board[0] or not word:
        return False
    
    rows, cols = len(board), len(board[0])
    
    def dfs(row, col, index):
        if index == len(word):
            return True
        
        if (row < 0 or row >= rows or col < 0 or col >= cols or 
            board[row][col] != word[index]):
            return False
        
        # 标记当前位置为已访问
        temp = board[row][col]
        board[row][col] = '#'
        
        # 四个方向搜索
        found = (dfs(row + 1, col, index + 1) or
                dfs(row - 1, col, index + 1) or
                dfs(row, col + 1, index + 1) or
                dfs(row, col - 1, index + 1))
        
        # 恢复当前位置
        board[row][col] = temp
        
        return found
    
    # 从每个位置开始搜索
    for i in range(rows):
        for j in range(cols):
            if dfs(i, j, 0):
                return True
    
    return False


def test_exist():
    """测试函数"""
    # 测试用例1
    board1 = [
        ["A","B","C","E"],
        ["S","F","C","S"],
        ["A","D","E","E"]
    ]
    word1 = "ABCCED"
    result1 = exist(board1, word1)
    print(f"测试1 word='ABCCED': {result1}")  # 期望: True
    
    # 测试用例2
    board2 = [
        ["A","B","C","E"],
        ["S","F","C","S"],
        ["A","D","E","E"]
    ]
    word2 = "SEE"
    result2 = exist(board2, word2)
    print(f"测试2 word='SEE': {result2}")  # 期望: True
    
    # 测试用例3
    word3 = "ABCB"
    result3 = exist(board1, word3)
    print(f"测试3 word='ABCB': {result3}")  # 期望: False


if __name__ == "__main__":
    test_exist()
