"""
LeetCode 213. 打家劫舍II
https://leetcode.cn/problems/house-robber-ii/

你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。
这个地方所有的房屋都围成一圈，这意味着第一个房屋和最后一个房屋是紧挨着的。

动态规划

时间复杂度：O(n)
空间复杂度：O(1)
"""

def rob(nums):
    """
    打家劫舍II - 动态规划法
    
    Args:
        nums: 每间房屋的现金数量（环形）
        
    Returns:
        能偷窃到的最高金额
    """
    if not nums:
        return 0
    
    if len(nums) == 1:
        return nums[0]
    
    if len(nums) == 2:
        return max(nums[0], nums[1])
    
    # 情况1：不偷第一个房子
    def rob_linear(houses):
        if not houses:
            return 0
        
        prev2 = houses[0]
        prev1 = max(houses[0], houses[1]) if len(houses) > 1 else houses[0]
        
        for i in range(2, len(houses)):
            current = max(prev1, prev2 + houses[i])
            prev2 = prev1
            prev1 = current
        
        return prev1
    
    # 分别计算两种情况
    case1 = rob_linear(nums[1:])  # 不偷第一个房子
    case2 = rob_linear(nums[:-1])  # 不偷最后一个房子
    
    return max(case1, case2)


def test_rob():
    """测试函数"""
    # 测试用例1
    nums1 = [2, 3, 2]
    result1 = rob(nums1)
    print(f"测试1 [2,3,2]: {result1}")  # 期望: 3
    
    # 测试用例2
    nums2 = [1, 2, 3, 1]
    result2 = rob(nums2)
    print(f"测试2 [1,2,3,1]: {result2}")  # 期望: 4
    
    # 测试用例3
    nums3 = [1, 2, 3]
    result3 = rob(nums3)
    print(f"测试3 [1,2,3]: {result3}")  # 期望: 3


if __name__ == "__main__":
    test_rob()
