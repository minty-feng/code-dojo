"""
LeetCode 15. 三数之和
https://leetcode.cn/problems/3sum/

给你一个包含n个整数的数组nums，判断nums中是否存在三个元素a，b，c，使得a+b+c=0？

双指针

时间复杂度：O(n^2)
空间复杂度：O(1)
"""

def three_sum(nums):
    """
    三数之和 - 双指针
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # 跳过重复元素
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        left, right = i + 1, n - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # 跳过重复元素
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return result

# 测试
if __name__ == "__main__":
    test_cases = [
        [-1, 0, 1, 2, -1, -4],
        [0, 1, 1],
        [0, 0, 0]
    ]
    
    for nums in test_cases:
        result = three_sum(nums[:])
        print(f"数组: {nums}")
        print(f"三数之和为0的组合: {result}\n")

