"""
LeetCode 47. 全排列II
https://leetcode.cn/problems/permutations-ii/

给定一个可包含重复数字的序列nums，按任意顺序返回所有不重复的全排列。

回溯 + 去重

时间复杂度：O(n! * n)
空间复杂度：O(n)
"""

def permute_unique(nums):
    """
    全排列II - 回溯 + 去重法
    
    Args:
        nums: 可包含重复数字的序列
        
    Returns:
        所有不重复的全排列
    """
    result = []
    nums.sort()  # 排序以便去重
    
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            
            # 去重：如果当前数字与前一个数字相同，且前一个数字未被使用，则跳过
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            
            path.append(nums[i])
            used[i] = True
            backtrack(path, used)
            path.pop()
            used[i] = False
    
    backtrack([], [False] * len(nums))
    return result


def test_permute_unique():
    """测试函数"""
    # 测试用例1
    nums1 = [1, 1, 2]
    result1 = permute_unique(nums1)
    print(f"测试1 [1,1,2]: {result1}")
    # 期望: [[1,1,2],[1,2,1],[2,1,1]]
    
    # 测试用例2
    nums2 = [1, 2, 3]
    result2 = permute_unique(nums2)
    print(f"测试2 [1,2,3]: {result2}")
    # 期望: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]


if __name__ == "__main__":
    test_permute_unique()
