# 01-array-hash-table (数组与哈希表)

LeetCode精选75题 - 数组与哈希表专题

## 📝 题目列表

| 编号 | 题目 | 难度 | LeetCode | Python | C++ |
|------|------|------|----------|--------|-----|
| 01 | 两数之和 | ⭐ | [1](https://leetcode.cn/problems/two-sum/) | ✅ | ✅ |
| 02 | 三数之和 | ⭐⭐ | [15](https://leetcode.cn/problems/3sum/) | ✅ | ✅ |
| 03 | 四数之和 | ⭐⭐ | [18](https://leetcode.cn/problems/4sum/) | ✅ | ✅ |
| 04 | 最长连续序列 | ⭐⭐ | [128](https://leetcode.cn/problems/longest-consecutive-sequence/) | ✅ | ✅ |
| 05 | 字母异位词分组 | ⭐⭐ | [49](https://leetcode.cn/problems/group-anagrams/) | ✅ | ✅ |
| 06 | 乘积最大子数组 | ⭐⭐ | [152](https://leetcode.cn/problems/maximum-product-subarray/) | ✅ | ✅ |
| 07 | 旋转图像 | ⭐⭐ | [48](https://leetcode.cn/problems/rotate-image/) | ✅ | ✅ |
| 08 | 寻找重复数 | ⭐⭐ | [287](https://leetcode.cn/problems/find-the-duplicate-number/) | ✅ | ✅ |
| 09 | 缺失的第一个正数 | ⭐⭐⭐ | [41](https://leetcode.cn/problems/first-missing-positive/) | ✅ | ✅ |
| 10 | 除自身以外数组的乘积 | ⭐⭐ | [238](https://leetcode.cn/problems/product-of-array-except-self/) | ✅ | ✅ |
| 11 | 螺旋矩阵 | ⭐⭐ | [54](https://leetcode.cn/problems/spiral-matrix/) | ✅ | ✅ |

## 🎯 核心技巧

### 哈希表应用
- **两数之和**：用哈希表存储已遍历元素
- **字母异位词**：字符串排序或字符计数
- **最长连续序列**：Set去重 + 连续性检查

### 数组技巧
- **三数之和**：排序 + 双指针
- **旋转图像**：数学变换

### 原地算法
- **缺失正数**：数组本身作为哈希表
- **寻找重复数**：快慢指针（Floyd判圈）

---

## 💡 解题模板

### 两数之和模板
```python
def two_sum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        if target - num in hash_map:
            return [hash_map[target - num], i]
        hash_map[num] = i
    return []
```

### 三数之和模板
```python
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # 去重
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result
```

---

## 📚 学习重点

1. **哈希表**：快速查找，空间换时间
2. **双指针**：有序数组的经典技巧
3. **原地算法**：O(1)空间复杂度
4. **数学思维**：旋转、螺旋等几何变换
