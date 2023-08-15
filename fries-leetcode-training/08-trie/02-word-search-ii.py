"""
LeetCode 212. 单词搜索II
https://leetcode.cn/problems/word-search-ii/

给定一个m x n二维字符网格board和一个单词（字符串）列表words，返回所有二维网格上的单词。

Trie + DFS回溯

时间复杂度：O(m*n*4^L) L为单词最大长度
空间复杂度：O(N) N为所有单词的字符总数
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word


def find_words(board, words):
    """
    单词搜索II - Trie + DFS回溯法
    
    Args:
        board: 二维字符网格
        words: 单词列表
        
    Returns:
        在网格中找到的单词列表
    """
    if not board or not board[0] or not words:
        return []
    
    # 构建Trie
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    result = []
    rows, cols = len(board), len(board[0])
    
    def dfs(row, col, node):
        char = board[row][col]
        
        # 检查当前字符是否在Trie中
        if char not in node.children:
            return
        
        node = node.children[char]
        
        # 如果找到完整单词
        if node.word:
            result.append(node.word)
            node.word = None  # 避免重复
        
        # 标记当前位置为已访问
        board[row][col] = '#'
        
        # 四个方向DFS
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                board[new_row][new_col] != '#'):
                dfs(new_row, new_col, node)
        
        # 恢复当前位置
        board[row][col] = char
    
    # 从每个位置开始搜索
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, trie.root)
    
    return result


def test_find_words():
    """测试函数"""
    # 测试用例1
    board1 = [
        ["o","a","a","n"],
        ["e","t","a","e"],
        ["i","h","k","r"],
        ["i","f","l","v"]
    ]
    words1 = ["oath","pea","eat","rain"]
    
    result1 = find_words(board1, words1)
    print(f"测试1结果: {result1}")  # 期望: ["eat","oath"]
    
    # 测试用例2
    board2 = [
        ["a","b"],
        ["c","d"]
    ]
    words2 = ["abcb"]
    
    result2 = find_words(board2, words2)
    print(f"测试2结果: {result2}")  # 期望: []


if __name__ == "__main__":
    test_find_words()
