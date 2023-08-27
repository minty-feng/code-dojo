# 14-math-geometry (数学几何)

LeetCode精选75题 - 数学几何专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 旋转图像 | ⭐⭐ | [48](https://leetcode.cn/problems/rotate-image/) | [01-rotate-image.py](./01-rotate-image.py) | [01-rotate-image.cpp](./01-rotate-image.cpp) |
| 02 | 螺旋矩阵 | ⭐⭐ | [54](https://leetcode.cn/problems/spiral-matrix/) | [02-spiral-matrix.py](./02-spiral-matrix.py) | [02-spiral-matrix.cpp](./02-spiral-matrix.cpp) |
| 03 | 矩阵置零 | ⭐⭐ | [73](https://leetcode.cn/problems/set-matrix-zeroes/) | [03-set-matrix-zeroes.py](./03-set-matrix-zeroes.py) | [03-set-matrix-zeroes.cpp](./03-set-matrix-zeroes.cpp) |

## 🎯 核心技巧

### 矩阵操作
- **[旋转图像](./01-rotate-image.py)**：数学变换，坐标映射
- **[螺旋矩阵](./02-spiral-matrix.py)**：方向控制，边界处理
- **[矩阵置零](./03-set-matrix-zeroes.py)**：原地算法

---

## 💡 解题模板

### 矩阵旋转模板
```python
def rotate_matrix(matrix):
    n = len(matrix)
    
    # 转置
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # 翻转每一行
    for i in range(n):
        matrix[i].reverse()
```

### 螺旋矩阵模板
```python
def spiral_order(matrix):
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 从左到右
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        
        # 从上到下
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        # 从右到左
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        
        # 从下到上
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result
```

---

## 📚 学习重点

1. **坐标变换**：旋转、翻转的数学公式
2. **边界控制**：螺旋遍历的边界处理
3. **原地算法**：O(1)空间复杂度
4. **数学思维**：几何变换的数学原理
