# 05-二叉搜索树（BST）

## 💡 核心结论

### BST本质
- **定义**：左子树所有节点 < 根 < 右子树所有节点
- **性能**：平均O(log n)，最坏O(n)（退化成链表）
- **中序遍历**：得到有序序列（BST的重要性质）
- **查找效率**：通过比较可以排除一半节点
- **局限**：可能不平衡，需要AVL树或红黑树改进

### 关键操作
| 操作 | 平均 | 最坏 | 关键点 |
|------|------|------|--------|
| 查找 | O(log n) | O(n) | 比较大小决定方向 |
| 插入 | O(log n) | O(n) | 找到位置后O(1)插入 |
| 删除 | O(log n) | O(n) | 三种情况分别处理 |
| 最小/最大 | O(log n) | O(n) | 一直往左/右 |

### 删除节点三种情况
1. **叶子节点**：直接删除
2. **一个子节点**：用子节点替换
3. **两个子节点**：用后继节点（右子树最小）替换

### BST vs 数组 vs 链表
| 操作 | BST | 有序数组 | 链表 |
|------|-----|----------|------|
| 查找 | O(log n) | O(log n) | O(n) |
| 插入 | O(log n) | O(n) | O(1)* |
| 删除 | O(log n) | O(n) | O(1)* |
| 有序遍历 | O(n) | O(n) | O(n log n) |

*已知位置

### 应用场景
- 动态有序数据维护
- 范围查询（findMin, findMax, floor, ceiling）
- 数据库索引（B树、B+树是BST的扩展）
- 文件系统

## 🔍 查找操作

### 递归查找
```python
def search(root, val):
    if not root or root.val == val:
        return root
    if val < root.val:
        return search(root.left, val)
    return search(root.right, val)
```

### 迭代查找（推荐）
```python
def search_iterative(root, val):
    while root and root.val != val:
        if val < root.val:
            root = root.left
        else:
            root = root.right
    return root
```

## ➕ 插入操作

### 递归插入
```python
def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root
```

## ➖ 删除操作（最复杂）

### 删除步骤
```python
def delete(root, val):
    if not root:
        return None
    
    # 查找节点
    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:
        # 找到要删除的节点
        
        # 情况1：叶子节点或只有一个子节点
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        
        # 情况2：有两个子节点
        # 找右子树的最小节点（后继）
        successor = find_min(root.right)
        root.val = successor.val
        # 删除后继节点
        root.right = delete(root.right, successor.val)
    
    return root

def find_min(root):
    while root.left:
        root = root.left
    return root
```

## 📚 LeetCode练习

- [700. Search in a BST](https://leetcode.com/problems/search-in-a-binary-search-tree/)
- [701. Insert into a BST](https://leetcode.com/problems/insert-into-a-binary-search-tree/)
- [450. Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/)
- [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/)
- [230. Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

## 💻 完整代码实现

### Python 实现

```{literalinclude} bst.py
:language: python
:linenos:
```

### C++ 实现

```{literalinclude} bst.cpp
:language: cpp
:linenos:
```

