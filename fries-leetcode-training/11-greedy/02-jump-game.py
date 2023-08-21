"""
LeetCode 55. 跳跃游戏
https://leetcode.cn/problems/jump-game/

给定一个非负整数数组nums，你最初位于数组的第一个下标。
数组中的每个元素代表你在该位置可以跳跃的最大长度。
判断你是否能够到达最后一个下标。

贪心

时间复杂度：O(n)
空间复杂度：O(1)
"""

def can_jump(nums):
    """
    跳跃游戏 - 贪心法
    
    Args:
        nums: 非负整数数组
        
    Returns:
        是否能够到达最后一个下标
    """
    max_reach = 0
    
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    
    return True


def test_can_jump():
    """测试函数"""
    # 测试用例1
    nums1 = [2, 3, 1, 1, 4]
    result1 = can_jump(nums1)
    print(f"测试1 [2,3,1,1,4]: {result1}")  # 期望: True
    
    # 测试用例2
    nums2 = [3, 2, 1, 0, 4]
    result2 = can_jump(nums2)
    print(f"测试2 [3,2,1,0,4]: {result2}")  # 期望: False
    
    # 测试用例3
    nums3 = [0]
    result3 = can_jump(nums3)
    print(f"测试3 [0]: {result3}")  # 期望: True


if __name__ == "__main__":
    test_can_jump()