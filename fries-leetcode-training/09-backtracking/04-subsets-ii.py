"""
LeetCode 90. 子集II
https://leetcode.cn/problems/subsets-ii/

给你一个整数数组nums，其中可能包含重复元素，请你返回该数组所有可能的子集。

回溯 + 去重

时间复杂度：O(2^n * n)
空间复杂度：O(n)
"""

def subsets_with_dup(nums):
    """
    子集II - 回溯 + 去重法
    
    Args:
        nums: 可能包含重复元素的整数数组
        
    Returns:
        所有可能的子集
    """
    result = []
    nums.sort()  # 排序以便去重
    
    def backtrack(start, path):
        result.append(path[:])  # 添加当前路径到结果
        
        for i in range(start, len(nums)):
            # 去重：如果当前数字与前一个数字相同，且不是第一次选择，则跳过
            if i > start and nums[i] == nums[i-1]:
                continue
            
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()  # 回溯
    
    backtrack(0, [])
    return result


def test_subsets_with_dup():
    """测试函数"""
    # 测试用例1
    nums1 = [1, 2, 2]
    result1 = subsets_with_dup(nums1)
    print(f"测试1 [1,2,2]: {result1}")
    # 期望: [[],[1],[1,2],[1,2,2],[2],[2,2]]
    
    # 测试用例2
    nums2 = [0]
    result2 = subsets_with_dup(nums2)
    print(f"测试2 [0]: {result2}")
    # 期望: [[],[0]]


if __name__ == "__main__":
    test_subsets_with_dup()
