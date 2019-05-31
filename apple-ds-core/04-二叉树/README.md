# 04-二叉树

## 💡 核心结论

### 二叉树本质
- **定义**：每个节点最多有两个子节点的树结构
- **遍历**：前序、中序、后序、层序，各有应用场景
- **深度优先**：递归（前中后序）或栈实现
- **广度优先**：队列实现层序遍历
- **应用**：表达式树、文件系统、DOM树

### 遍历方式对比
| 遍历 | 顺序 | 应用 | 实现 |
|------|------|------|------|
| 前序 | 根→左→右 | 复制树、序列化 | 递归/栈 |
| 中序 | 左→根→右 | BST有序输出 | 递归/栈 |
| 后序 | 左→右→根 | 删除树、计算表达式 | 递归/栈 |
| 层序 | 逐层 | 打印层级、BFS | 队列 |

### 关键概念
- **满二叉树**：每层都满，节点数 = 2^h - 1
- **完全二叉树**：除最后一层外都满，最后一层从左到右连续
- **平衡二叉树**：左右子树高度差 ≤ 1
- **深度**：从根到节点的边数
- **高度**：从节点到叶子的最长路径

### 性质
- n个节点的二叉树高度：⌈log₂(n+1)⌉ ≤ h ≤ n
- 第i层最多有 2^(i-1) 个节点
- 深度为h的二叉树最多有 2^h - 1 个节点

## 🌳 二叉树遍历

### 递归遍历
```python
def preorder(root):    # 前序：根左右
    if not root: return
    print(root.val)
    preorder(root.left)
    preorder(root.right)

def inorder(root):     # 中序：左根右
    if not root: return
    inorder(root.left)
    print(root.val)
    inorder(root.right)

def postorder(root):   # 后序：左右根
    if not root: return
    postorder(root.left)
    postorder(root.right)
    print(root.val)
```

### 迭代遍历（重要）
```python
# 前序（栈）
def preorder_iterative(root):
    if not root: return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right: stack.append(node.right)
        if node.left: stack.append(node.left)
    return result

# 中序（栈）
def inorder_iterative(root):
    stack, result = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result

# 层序（队列）
def levelorder(root):
    if not root: return []
    queue, result = [root], []
    while queue:
        node = queue.pop(0)
        result.append(node.val)
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)
    return result
```

## 🎯 常见问题

### 树的高度/深度
```python
def height(root):
    if not root: return 0
    return 1 + max(height(root.left), height(root.right))
```

### 节点数
```python
def count_nodes(root):
    if not root: return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

### 镜像翻转
```python
def mirror(root):
    if not root: return
    root.left, root.right = root.right, root.left
    mirror(root.left)
    mirror(root.right)
```

### 路径和
```python
def has_path_sum(root, target):
    if not root: return False
    if not root.left and not root.right:
        return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))
```

## 📚 LeetCode练习

- [144. Binary Tree Preorder Traversal](https://leetcode.com/problems/binary-tree-preorder-traversal/)
- [94. Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/)
- [145. Binary Tree Postorder Traversal](https://leetcode.com/problems/binary-tree-postorder-traversal/)
- [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)
- [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
- [112. Path Sum](https://leetcode.com/problems/path-sum/)

