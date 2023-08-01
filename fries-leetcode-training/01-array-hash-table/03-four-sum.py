"""
LeetCode 18. 四数之和
https://leetcode.cn/problems/4sum/

给你一个由n个整数组成的数组nums，和一个目标值target。
请你找出并返回满足下述全部条件且不重复的四元组[nums[a], nums[b], nums[c], nums[d]]：
- 0 <= a, b, c, d < n
- a、b、c和d互不相同
- nums[a] + nums[b] + nums[c] + nums[d] == target

双指针 + 排序

时间复杂度：O(n³)
空间复杂度：O(1)
"""

def four_sum(nums, target):
    """
    四数之和 - 双指针法
    
    Args:
        nums: 整数数组
        target: 目标值
        
    Returns:
        所有满足条件的四元组列表
    """
    if len(nums) < 4:
        return []
    
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 3):
        # 跳过重复元素
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        for j in range(i + 1, n - 2):
            # 跳过重复元素
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            
            left, right = j + 1, n - 1
            
            while left < right:
                current_sum = nums[i] + nums[j] + nums[left] + nums[right]
                
                if current_sum == target:
                    result.append([nums[i], nums[j], nums[left], nums[right]])
                    
                    # 跳过重复元素
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
    
    return result


def test_four_sum():
    """测试函数"""
    # 测试用例1
    nums1 = [1, 0, -1, 0, -2, 2]
    target1 = 0
    result1 = four_sum(nums1, target1)
    print(f"测试1: {result1}")
    # 期望: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
    
    # 测试用例2
    nums2 = [2, 2, 2, 2, 2]
    target2 = 8
    result2 = four_sum(nums2, target2)
    print(f"测试2: {result2}")
    # 期望: [[2,2,2,2]]
    
    # 测试用例3
    nums3 = [1, -2, -5, -4, -3, 3, 3, 5]
    target3 = -11
    result3 = four_sum(nums3, target3)
    print(f"测试3: {result3}")
    # 期望: [[-5,-4,-3,1]]


if __name__ == "__main__":
    test_four_sum()
