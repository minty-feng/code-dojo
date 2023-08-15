"""
LeetCode 211. 添加与搜索单词
https://leetcode.cn/problems/design-add-and-search-words-data-structure/

请你设计一个数据结构，支持添加新单词和查找字符串是否与任何先前添加的字符串匹配。

Trie + 通配符处理

时间复杂度：O(m) 添加，O(m) 搜索（m为字符串长度）
空间复杂度：O(ALPHABET_SIZE * N * M) N为键的数量，M为键的长度
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    
    def add_word(self, word):
        """
        添加单词
        
        Args:
            word: 要添加的单词
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        """
        搜索单词（支持'.'通配符）
        
        Args:
            word: 要搜索的单词
            
        Returns:
            是否存在该单词
        """
        def dfs(node, index):
            if index == len(word):
                return node.is_end
            
            char = word[index]
            
            if char == '.':
                # 通配符，尝试所有子节点
                for child in node.children.values():
                    if dfs(child, index + 1):
                        return True
                return False
            else:
                # 普通字符
                if char not in node.children:
                    return False
                return dfs(node.children[char], index + 1)
        
        return dfs(self.root, 0)


def test_word_dictionary():
    """测试函数"""
    word_dict = WordDictionary()
    
    # 添加单词
    word_dict.add_word("bad")
    word_dict.add_word("dad")
    word_dict.add_word("mad")
    
    # 测试搜索
    print(f"搜索 'pad': {word_dict.search('pad')}")    # 期望: False
    print(f"搜索 'bad': {word_dict.search('bad')}")    # 期望: True
    print(f"搜索 '.ad': {word_dict.search('.ad')}")    # 期望: True
    print(f"搜索 'b..': {word_dict.search('b..')}")   # 期望: True
    print(f"搜索 'b.x': {word_dict.search('b.x')}")    # 期望: False


if __name__ == "__main__":
    test_word_dictionary()
