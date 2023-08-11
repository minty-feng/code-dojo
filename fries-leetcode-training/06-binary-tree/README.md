# 06-binary-tree (二叉树)

LeetCode精选75题 - 二叉树专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 二叉树的最大深度 | ⭐ | [104](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) | [01-maximum-depth-of-binary-tree.py](./01-maximum-depth-of-binary-tree.py) | [01-maximum-depth-of-binary-tree.cpp](./01-maximum-depth-of-binary-tree.cpp) |
| 02 | 路径总和 | ⭐ | [112](https://leetcode.cn/problems/path-sum/) | [02-path-sum.py](./02-path-sum.py) | [02-path-sum.cpp](./02-path-sum.cpp) |
| 03 | 二叉树的层序遍历 | ⭐⭐ | [102](https://leetcode.cn/problems/binary-tree-level-order-traversal/) | [03-binary-tree-level-order-traversal.py](./03-binary-tree-level-order-traversal.py) | [03-binary-tree-level-order-traversal.cpp](./03-binary-tree-level-order-traversal.cpp) |
| 04 | 二叉树的锯齿形层序遍历 | ⭐⭐ | [103](https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/) | [04-binary-tree-zigzag-level-order-traversal.py](./04-binary-tree-zigzag-level-order-traversal.py) | [04-binary-tree-zigzag-level-order-traversal.cpp](./04-binary-tree-zigzag-level-order-traversal.cpp) |
| 05 | 从前序与中序遍历序列构造二叉树 | ⭐⭐ | [105](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | [05-construct-binary-tree-from-preorder-and-inorder-traversal.py](./05-construct-binary-tree-from-preorder-and-inorder-traversal.py) | [05-construct-binary-tree-from-preorder-and-inorder-traversal.cpp](./05-construct-binary-tree-from-preorder-and-inorder-traversal.cpp) |
| 06 | 从中序与后序遍历序列构造二叉树 | ⭐⭐ | [106](https://leetcode.cn/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) | [06-construct-binary-tree-from-inorder-and-postorder-traversal.py](./06-construct-binary-tree-from-inorder-and-postorder-traversal.py) | [06-construct-binary-tree-from-inorder-and-postorder-traversal.cpp](./06-construct-binary-tree-from-inorder-and-postorder-traversal.cpp) |
| 07 | 二叉树的右视图 | ⭐⭐ | [199](https://leetcode.cn/problems/binary-tree-right-side-view/) | [07-binary-tree-right-side-view.py](./07-binary-tree-right-side-view.py) | [07-binary-tree-right-side-view.cpp](./07-binary-tree-right-side-view.cpp) |
| 08 | 二叉树的直径 | ⭐ | [543](https://leetcode.cn/problems/diameter-of-binary-tree/) | [08-diameter-of-binary-tree.py](./08-diameter-of-binary-tree.py) | [08-diameter-of-binary-tree.cpp](./08-diameter-of-binary-tree.cpp) |
| 09 | 翻转二叉树 | ⭐ | [226](https://leetcode.cn/problems/invert-binary-tree/) | [09-invert-binary-tree.py](./09-invert-binary-tree.py) | [09-invert-binary-tree.cpp](./09-invert-binary-tree.cpp) |

## 🎯 核心技巧

### 遍历方式
- **[二叉树的最大深度](./01-maximum-depth-of-binary-tree.py)**：递归或层序遍历
- **[路径总和](./02-path-sum.py)**：DFS递归，路径和问题
- **[翻转二叉树](./09-invert-binary-tree.py)**：递归交换左右子树

### 层序遍历
- **[二叉树的层序遍历](./03-binary-tree-level-order-traversal.py)**：BFS队列实现
- **[二叉树的锯齿形层序遍历](./04-binary-tree-zigzag-level-order-traversal.py)**：层序遍历 + 方向控制
- **[二叉树的右视图](./07-binary-tree-right-side-view.py)**：层序遍历取每层最右节点

### 树构建
- **[从前序与中序遍历序列构造二叉树](./05-construct-binary-tree-from-preorder-and-inorder-traversal.py)**：递归构建，找根节点
- **[从中序与后序遍历序列构造二叉树](./06-construct-binary-tree-from-inorder-and-postorder-traversal.py)**：递归构建，找根节点

### 树的性质
- **[二叉树的直径](./08-diameter-of-binary-tree.py)**：DFS计算左右子树高度

---

## 💡 解题模板

### DFS递归模板
```python
def dfs(root):
    if not root:
        return 0
    
    left = dfs(root.left)
    right = dfs(root.right)
    
    return max(left, right) + 1
```

### BFS层序遍历模板
```python
def level_order(root):
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.pop(0)
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

### 路径和模板
```python
def has_path_sum(root, target_sum):
    if not root:
        return False
    
    if not root.left and not root.right:
        return root.val == target_sum
    
    return (has_path_sum(root.left, target_sum - root.val) or
            has_path_sum(root.right, target_sum - root.val))
```

---

## 📚 学习重点

1. **遍历方式**：前序、中序、后序、层序遍历
2. **递归思想**：树的问题大多可以用递归解决
3. **BFS vs DFS**：层序遍历用BFS，深度问题用DFS
4. **树的构建**：根据遍历序列重建二叉树
5. **路径问题**：DFS + 回溯思想
