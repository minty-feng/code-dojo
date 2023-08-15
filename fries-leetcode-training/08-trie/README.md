# 08-trie (字典树)

LeetCode精选75题 - 字典树专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 实现Trie | ⭐⭐ | [208](https://leetcode.cn/problems/implement-trie-prefix-tree/) | [01-implement-trie.py](./01-implement-trie.py) | [01-implement-trie.cpp](./01-implement-trie.cpp) |
| 02 | 单词搜索II | ⭐⭐⭐ | [212](https://leetcode.cn/problems/word-search-ii/) | [02-word-search-ii.py](./02-word-search-ii.py) | [02-word-search-ii.cpp](./02-word-search-ii.cpp) |
| 03 | 添加与搜索单词 | ⭐⭐ | [211](https://leetcode.cn/problems/design-add-and-search-words-data-structure/) | [03-design-add-and-search-words-data-structure.py](./03-design-add-and-search-words-data-structure.py) | [03-design-add-and-search-words-data-structure.cpp](./03-design-add-and-search-words-data-structure.cpp) |

## 🎯 核心技巧

### Trie基本操作
- **[实现Trie](./01-implement-trie.py)**：插入、搜索、前缀搜索
- **[添加与搜索单词](./03-design-add-and-search-words-data-structure.py)**：支持通配符搜索

### Trie + DFS
- **[单词搜索II](./02-word-search-ii.py)**：Trie + 回溯搜索

---

## 💡 解题模板

### Trie节点定义
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
```

---

## 📚 学习重点

1. **Trie结构**：多叉树存储字符串
2. **前缀搜索**：高效的前缀匹配
3. **DFS + Trie**：在矩阵中搜索单词
4. **通配符处理**：支持'.'通配符
