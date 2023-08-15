"""
LeetCode 208. 实现Trie
https://leetcode.cn/problems/implement-trie-prefix-tree/

Trie（发音类似"try"）或者说前缀树是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。

Trie

时间复杂度：O(m) m为字符串长度
空间复杂度：O(ALPHABET_SIZE * N * M) N为键的数量，M为键的长度
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """
        插入单词
        
        Args:
            word: 要插入的单词
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        """
        搜索单词
        
        Args:
            word: 要搜索的单词
            
        Returns:
            是否存在该单词
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        """
        搜索前缀
        
        Args:
            prefix: 要搜索的前缀
            
        Returns:
            是否存在该前缀
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


def test_trie():
    """测试函数"""
    trie = Trie()
    
    # 插入单词
    trie.insert("apple")
    trie.insert("app")
    trie.insert("application")
    
    # 测试搜索
    print(f"搜索 'app': {trie.search('app')}")        # 期望: True
    print(f"搜索 'apple': {trie.search('apple')}")    # 期望: True
    print(f"搜索 'appl': {trie.search('appl')}")      # 期望: False
    
    # 测试前缀
    print(f"前缀 'app': {trie.starts_with('app')}")   # 期望: True
    print(f"前缀 'appl': {trie.starts_with('appl')}") # 期望: True
    print(f"前缀 'xyz': {trie.starts_with('xyz')}")   # 期望: False


if __name__ == "__main__":
    test_trie()
