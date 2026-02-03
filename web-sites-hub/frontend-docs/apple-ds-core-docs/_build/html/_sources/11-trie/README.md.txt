# 11-字典树（Trie）

## 💡 核心结论

### Trie本质
- **定义**：树形结构，用于高效存储和检索字符串
- **核心**：共享前缀，节省空间
- **操作**：插入O(m)、查找O(m)、前缀匹配O(m)，m为字符串长度
- **空间**：O(总字符数)，但常数大（每个节点26个指针）
- **应用**：自动补全、拼写检查、IP路由

### Trie vs 哈希表
| 特性 | Trie | 哈希表 |
|------|------|--------|
| 查找 | O(m) | O(m) |
| 前缀查询 | O(m) | O(n×m) |
| 空间 | 大 | 小 |
| 顺序遍历 | 支持 | 不支持 |

### 应用场景
- **自动补全**：输入前缀，返回所有单词
- **拼写检查**：查找相似单词
- **最长公共前缀**
- **IP路由表**
- **搜索引擎建议**

## 🌳 Trie结构

```
插入: "cat", "car", "card", "care", "dog"

       root
       /  \
      c    d
      |    |
      a    o
     /|\   |
    t r e  g
      | |
      d r
      | 
      e
```

## 🎯 基本实现

### Python实现
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

## 📚 LeetCode练习

- [208. Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/)
- [211. Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/)
- [212. Word Search II](https://leetcode.com/problems/word-search-ii/)
- [1268. Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/)

## 💻 完整代码实现

### Python 实现

```{literalinclude} trie.py
:language: python
:linenos:
```

### C++ 实现

```{literalinclude} trie.cpp
:language: cpp
:linenos:
```

