# 09-backtracking (回溯)

LeetCode精选75题 - 回溯专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 全排列 | ⭐⭐ | [46](https://leetcode.cn/problems/permutations/) | [01-permutations.py](./01-permutations.py) | [01-permutations.cpp](./01-permutations.cpp) |
| 02 | 全排列II | ⭐⭐ | [47](https://leetcode.cn/problems/permutations-ii/) | [02-permutations-ii.py](./02-permutations-ii.py) | [02-permutations-ii.cpp](./02-permutations-ii.cpp) |
| 03 | 子集 | ⭐⭐ | [78](https://leetcode.cn/problems/subsets/) | [03-subsets.py](./03-subsets.py) | [03-subsets.cpp](./03-subsets.cpp) |
| 04 | 子集II | ⭐⭐ | [90](https://leetcode.cn/problems/subsets-ii/) | [04-subsets-ii.py](./04-subsets-ii.py) | [04-subsets-ii.cpp](./04-subsets-ii.cpp) |
| 05 | 组合 | ⭐⭐ | [77](https://leetcode.cn/problems/combinations/) | [05-combinations.py](./05-combinations.py) | [05-combinations.cpp](./05-combinations.cpp) |
| 06 | 组合总和 | ⭐⭐ | [39](https://leetcode.cn/problems/combination-sum/) | [06-combination-sum.py](./06-combination-sum.py) | [06-combination-sum.cpp](./06-combination-sum.cpp) |
| 07 | N皇后 | ⭐⭐⭐ | [51](https://leetcode.cn/problems/n-queens/) | [07-n-queens.py](./07-n-queens.py) | [07-n-queens.cpp](./07-n-queens.cpp) |
| 08 | 解数独 | ⭐⭐⭐ | [37](https://leetcode.cn/problems/sudoku-solver/) | [08-sudoku-solver.py](./08-sudoku-solver.py) | [08-sudoku-solver.cpp](./08-sudoku-solver.cpp) |
| 09 | 单词搜索 | ⭐⭐ | [79](https://leetcode.cn/problems/word-search/) | [09-word-search.py](./09-word-search.py) | [09-word-search.cpp](./09-word-search.cpp) |

## 🎯 核心技巧

### 排列问题
- **[全排列](./01-permutations.py)**：无重复元素的全排列
- **[全排列II](./02-permutations-ii.py)**：有重复元素的全排列，需要去重

### 子集问题
- **[子集](./03-subsets.py)**：无重复元素的子集
- **[子集II](./04-subsets-ii.py)**：有重复元素的子集，需要去重

### 组合问题
- **[组合](./05-combinations.py)**：从n个数中选k个
- **[组合总和](./06-combination-sum.py)**：可重复使用的组合

### 约束满足问题
- **[N皇后](./07-n-queens.py)**：经典约束满足问题
- **[解数独](./08-sudoku-solver.py)**：9x9数独求解
- **[单词搜索](./09-word-search.py)**：在矩阵中搜索单词

---

## 💡 解题模板

### 回溯模板
```python
def backtrack(path, choices):
    if 满足结束条件:
        result.append(path[:])
        return
    
    for choice in choices:
        if 满足选择条件:
            path.append(choice)
            backtrack(path, 更新后的choices)
            path.pop()  # 回溯
```

### 全排列模板
```python
def permute(nums):
    result = []
    
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for num in nums:
            if num not in path:
                path.append(num)
                backtrack(path)
                path.pop()
    
    backtrack([])
    return result
```

### 子集模板
```python
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result
```

---

## 📚 学习重点

1. **回溯思想**：试错 + 回退
2. **状态空间树**：理解搜索空间
3. **剪枝优化**：减少无效搜索
4. **去重技巧**：处理重复元素
5. **约束满足**：N皇后、数独等经典问题
