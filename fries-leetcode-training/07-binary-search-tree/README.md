# 07-binary-search-tree (二叉搜索树)

LeetCode精选75题 - 二叉搜索树专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 验证二叉搜索树 | ⭐⭐ | [98](https://leetcode.cn/problems/validate-binary-search-tree/) | [01-validate-binary-search-tree.py](./01-validate-binary-search-tree.py) | [01-validate-binary-search-tree.cpp](./01-validate-binary-search-tree.cpp) |
| 02 | 二叉搜索树中第K小的元素 | ⭐⭐ | [230](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/) | [02-kth-smallest-element-in-a-bst.py](./02-kth-smallest-element-in-a-bst.py) | [02-kth-smallest-element-in-a-bst.cpp](./02-kth-smallest-element-in-a-bst.cpp) |
| 03 | 二叉搜索树的最近公共祖先 | ⭐ | [235](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/) | [03-lowest-common-ancestor-of-a-binary-search-tree.py](./03-lowest-common-ancestor-of-a-binary-search-tree.py) | [03-lowest-common-ancestor-of-a-binary-search-tree.cpp](./03-lowest-common-ancestor-of-a-binary-search-tree.cpp) |
| 04 | 将有序数组转换为二叉搜索树 | ⭐ | [108](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/) | [04-convert-sorted-array-to-binary-search-tree.py](./04-convert-sorted-array-to-binary-search-tree.py) | [04-convert-sorted-array-to-binary-search-tree.cpp](./04-convert-sorted-array-to-binary-search-tree.cpp) |

## 🎯 核心技巧

### BST性质
- **[验证二叉搜索树](./01-validate-binary-search-tree.py)**：中序遍历递增性
- **[二叉搜索树中第K小的元素](./02-kth-smallest-element-in-a-bst.py)**：中序遍历找第k个
- **[二叉搜索树的最近公共祖先](./03-lowest-common-ancestor-of-a-binary-search-tree.py)**：利用BST性质

### BST构建
- **[将有序数组转换为二叉搜索树](./04-convert-sorted-array-to-binary-search-tree.py)**：递归构建平衡BST

---

## 💡 解题模板

### BST验证模板
```python
def is_valid_bst(root):
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))
```

### BST中序遍历模板
```python
def inorder_traversal(root):
    result = []
    
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    
    inorder(root)
    return result
```

---

## 📚 学习重点

1. **BST性质**：左子树 < 根 < 右子树
2. **中序遍历**：BST的中序遍历是递增序列
3. **递归构建**：利用BST性质递归构建
4. **最近公共祖先**：利用BST性质简化查找
