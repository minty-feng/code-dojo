"""
LeetCode 78. 子集
https://leetcode.cn/problems/subsets/

给你一个整数数组nums，数组中的元素互不相同。返回该数组所有可能的子集。

回溯

时间复杂度：O(2^n * n)
空间复杂度：O(n)
"""

def subsets(nums):
    """
    子集 - 回溯法
    
    Args:
        nums: 整数数组
        
    Returns:
        所有可能的子集
    """
    result = []
    
    def backtrack(start, path):
        result.append(path[:])  # 添加当前路径到结果
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()  # 回溯
    
    backtrack(0, [])
    return result


def subsets_iterative(nums):
    """
    子集 - 迭代法
    
    Args:
        nums: 整数数组
        
    Returns:
        所有可能的子集
    """
    result = [[]]
    
    for num in nums:
        # 为每个现有子集添加当前数字
        new_subsets = []
        for subset in result:
            new_subsets.append(subset + [num])
        result.extend(new_subsets)
    
    return result


def test_subsets():
    """测试函数"""
    # 测试用例1
    nums1 = [1, 2, 3]
    result1 = subsets(nums1)
    print(f"测试1 [1,2,3]: {result1}")
    # 期望: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
    
    # 测试用例2
    nums2 = [0]
    result2 = subsets(nums2)
    print(f"测试2 [0]: {result2}")
    # 期望: [[],[0]]
    
    # 测试迭代法
    result3 = subsets_iterative([1, 2])
    print(f"迭代法 [1,2]: {result3}")


if __name__ == "__main__":
    test_subsets()
