"""
LeetCode 46. 全排列
https://leetcode.cn/problems/permutations/

给定一个不含重复数字的数组nums，返回其所有可能的全排列。

回溯

时间复杂度：O(n! * n)
空间复杂度：O(n)
"""

def permute(nums):
    """
    全排列 - 回溯法
    
    Args:
        nums: 不含重复数字的数组
        
    Returns:
        所有可能的全排列
    """
    result = []
    
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for num in nums:
            if num not in path:
                path.append(num)
                backtrack(path)
                path.pop()  # 回溯
    
    backtrack([])
    return result


def test_permute():
    """测试函数"""
    # 测试用例1
    nums1 = [1, 2, 3]
    result1 = permute(nums1)
    print(f"测试1 [1,2,3]: {result1}")
    # 期望: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    
    # 测试用例2
    nums2 = [0, 1]
    result2 = permute(nums2)
    print(f"测试2 [0,1]: {result2}")
    # 期望: [[0,1],[1,0]]


if __name__ == "__main__":
    test_permute()
