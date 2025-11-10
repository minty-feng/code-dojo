# 07-AVL树

## 💡 核心结论

### AVL树本质
- **定义**：严格平衡的二叉搜索树，左右子树高度差≤1
- **性能**：所有操作严格O(log n)，查询最快
- **平衡因子**：BF = 左子树高度 - 右子树高度，范围[-1, 0, 1]
- **核心**：通过旋转维持平衡，保证树高度为O(log n)
- **代价**：插入删除时旋转次数多于红黑树

### AVL vs 红黑树（重要对比）
| 特性 | AVL树 | 红黑树 |
|------|--------|--------|
| 平衡标准 | 高度差≤1 | 最长≤2倍最短 |
| 平衡度 | 更严格 | 较宽松 |
| 查询 | 更快 | 稍慢 |
| 插入删除 | 较慢（旋转多） | 更快 |
| 使用场景 | **查询密集** | **插入删除密集** |
| 实际应用 | Windows NT | Linux、STL |

### 四种旋转情况（必须记住）
1. **LL（左左）**：右旋
2. **RR（右右）**：左旋
3. **LR（左右）**：先左旋左子树，再右旋根
4. **RL（右左）**：先右旋右子树，再左旋根

```
判断方法：
- 看插入路径：根→左→左 = LL
- 看平衡因子：根BF=2，左子BF=1 = LL
```

### 旋转原理
- **目的**：降低树高度，保持BST性质
- **次数**：插入最多2次旋转，删除最多O(log n)次
- **关键**：旋转不改变中序遍历结果（仍然有序）

## 🔄 四种旋转详解

### LL型（右旋）
```
      z(BF=2)              y
     /                    / \
    y(BF=1)      =>      x   z
   /
  x

右旋z节点
```

### RR型（左旋）
```
  z(BF=-2)                 y
   \                      / \
    y(BF=-1)      =>     z   x
     \
      x

左旋z节点
```

### LR型（先左旋再右旋）
```
    z(BF=2)          z             y
   /                /             / \
  y(BF=-1)   =>    y      =>     x   z
   \              /
    x            x

先左旋y，再右旋z
```

### RL型（先右旋再左旋）
```
  z(BF=-2)        z               y
   \               \             / \
    y(BF=1)  =>     y      =>   z   x
   /                 \
  x                   x

先右旋y，再左旋z
```

## 📊 性能分析

### 树高度保证
```
设 N(h) 为高度h的AVL树最少节点数
N(h) = N(h-1) + N(h-2) + 1（类似斐波那契）

结论：n个节点的AVL树
高度h ≈ 1.44 log₂(n)
```

### 操作次数统计
```
插入1000个元素（随机顺序）：
- BST可能退化：高度1000，查找O(n)
- AVL保持平衡：高度~14，查找O(log n)
- 平均旋转次数：~0.5次/插入
```

## 🎯 实现要点

### 更新高度
```python
def update_height(node):
    if not node:
        return 0
    left_height = node.left.height if node.left else 0
    right_height = node.right.height if node.right else 0
    node.height = 1 + max(left_height, right_height)
```

### 计算平衡因子
```python
def get_balance(node):
    if not node:
        return 0
    left_height = node.left.height if node.left else 0
    right_height = node.right.height if node.right else 0
    return left_height - right_height
```

### 插入后调整
```python
def insert(root, val):
    # 1. BST插入
    if not root:
        return AVLNode(val)
    
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    
    # 2. 更新高度
    root.height = 1 + max(
        root.left.height if root.left else 0,
        root.right.height if root.right else 0
    )
    
    # 3. 获取平衡因子
    balance = get_balance(root)
    
    # 4. 四种情况调整
    # LL
    if balance > 1 and val < root.left.val:
        return right_rotate(root)
    
    # RR
    if balance < -1 and val > root.right.val:
        return left_rotate(root)
    
    # LR
    if balance > 1 and val > root.left.val:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    
    # RL
    if balance < -1 and val < root.right.val:
        root.right = right_rotate(root.right)
        return left_rotate(root)
    
    return root
```

## 💡 使用建议

### 何时使用AVL
- 查询操作远多于插入删除
- 需要严格的O(log n)保证
- 对查询性能要求极高

### 何时不用AVL
- 频繁插入删除（用红黑树）
- 数据量小（直接用数组）
- 不需要有序（用哈希表）

## 📚 LeetCode练习

AVL树实现本身较复杂，LeetCode中较少直接考察，但理解AVL树有助于：
- 理解平衡树概念
- BST相关题目
- 系统设计选型

## 💻 完整代码实现

### Python 实现

```{literalinclude} avl_tree.py
:language: python
:linenos:
```

### C++ 实现

```{literalinclude} avl_tree.cpp
:language: cpp
:linenos:
```

