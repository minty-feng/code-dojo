# 05-分治算法

## 💡 核心结论

### 分治本质
- **定义**：分解→递归解决→合并结果
- **三步骤**：Divide（分解）→ Conquer（解决）→ Combine（合并）
- **关键**：子问题独立、可递归、能合并
- **时间**：T(n) = aT(n/b) + f(n)，主定理分析
- **应用**：归并排序、快排、二分查找、大整数乘法

### 分治 vs 其他
| 策略 | 特点 | 典型算法 |
|------|------|----------|
| 分治 | 子问题独立 | 归并、快排 |
| 动态规划 | 子问题重叠 | 斐波那契、背包 |
| 贪心 | 局部最优 | Dijkstra、哈夫曼 |

### 经典分治问题
- **排序**：归并O(n log n)、快排O(n log n)
- **搜索**：二分O(log n)
- **矩阵**：Strassen矩阵乘法O(n^2.81)
- **大整数**：Karatsuba乘法O(n^1.58)
- **几何**：最近点对O(n log n)

## 🎯 归并排序（分治典范）

```python
def merge_sort(arr):
    # 分解
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # 递归左半
    right = merge_sort(arr[mid:])  # 递归右半
    
    # 合并
    return merge(left, right)
```

## 🔍 快速选择（第K大）

```python
def quick_select(nums, k):
    """平均O(n)找第k大元素"""
    if not nums:
        return None
    
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x > pivot]
    mid = [x for x in nums if x == pivot]
    right = [x for x in nums if x < pivot]
    
    if k <= len(left):
        return quick_select(left, k)
    elif k <= len(left) + len(mid):
        return mid[0]
    else:
        return quick_select(right, k - len(left) - len(mid))
```

## 📚 LeetCode练习

- [912. Sort an Array](https://leetcode.com/problems/sort-an-array/)
- [215. Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)
- [169. Majority Element](https://leetcode.com/problems/majority-element/)

