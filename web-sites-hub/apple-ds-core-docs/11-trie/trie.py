"""
字典树（Trie）实现
"""

class TrieNode:
    """Trie节点"""
    
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """字典树实现"""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """插入单词"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        """查找完整单词"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        """查找前缀"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def get_all_words_with_prefix(self, prefix):
        """获取所有以prefix开头的单词"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        result = []
        self._dfs(node, prefix, result)
        return result
    
    def _dfs(self, node, path, result):
        """DFS收集所有单词"""
        if node.is_end:
            result.append(path)
        
        for char, child in node.children.items():
            self._dfs(child, path + char, result)
    
    def delete(self, word):
        """删除单词"""
        def delete_helper(node, word, index):
            if index == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False
            
            should_delete = delete_helper(node.children[char], word, index + 1)
            
            if should_delete:
                del node.children[char]
                return not node.is_end and len(node.children) == 0
            
            return False
        
        delete_helper(self.root, word, 0)


def demo():
    """演示Trie操作"""
    print("=== 字典树演示 ===\n")
    
    trie = Trie()
    
    # 插入单词
    words = ["cat", "car", "card", "care", "dog", "dodge"]
    print(f"插入单词: {words}\n")
    for word in words:
        trie.insert(word)
    
    # 查找
    print("查找:")
    test_words = ["cat", "can", "car", "card"]
    for word in test_words:
        found = trie.search(word)
        print(f"  {word}: {'✅找到' if found else '❌未找到'}")
    
    # 前缀查找
    print("\n前缀查找:")
    prefixes = ["ca", "do", "da"]
    for prefix in prefixes:
        found = trie.starts_with(prefix)
        print(f"  {prefix}: {'✅存在' if found else '❌不存在'}")
    
    # 自动补全
    print("\n自动补全:")
    prefix = "car"
    words = trie.get_all_words_with_prefix(prefix)
    print(f"  以'{prefix}'开头的单词: {words}")


if __name__ == '__main__':
    demo()

