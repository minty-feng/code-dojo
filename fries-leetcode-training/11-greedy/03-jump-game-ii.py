"""
LeetCode 45. 跳跃游戏II
https://leetcode.cn/problems/jump-game-ii/

给你一个非负整数数组nums，你最初位于数组的第一个位置。
数组中的每个元素代表你在该位置可以跳跃的最大长度。
你的目标是使用最少的跳跃次数到达数组的最后一个位置。

贪心

时间复杂度：O(n)
空间复杂度：O(1)
"""

def jump(nums):
    """
    跳跃游戏II - 贪心法
    
    Args:
        nums: 非负整数数组
        
    Returns:
        最少跳跃次数
    """
    if len(nums) <= 1:
        return 0
    
    jumps = 0
    current_end = 0
    farthest = 0
    
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        
        if i == current_end:
            jumps += 1
            current_end = farthest
            
            if current_end >= len(nums) - 1:
                break
    
    return jumps


def test_jump():
    """测试函数"""
    # 测试用例1
    nums1 = [2, 3, 1, 1, 4]
    result1 = jump(nums1)
    print(f"测试1 [2,3,1,1,4]: {result1}")  # 期望: 2
    
    # 测试用例2
    nums2 = [2, 3, 0, 1, 4]
    result2 = jump(nums2)
    print(f"测试2 [2,3,0,1,4]: {result2}")  # 期望: 2
    
    # 测试用例3
    nums3 = [1, 2, 3]
    result3 = jump(nums3)
    print(f"测试3 [1,2,3]: {result3}")  # 期望: 2


if __name__ == "__main__":
    test_jump()
