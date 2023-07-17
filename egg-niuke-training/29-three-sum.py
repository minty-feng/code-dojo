"""
NC54 三数之和
https://www.nowcoder.com/practice/345e2ed5f81d4017bbb8cc6055b0b711

给出一个有n个元素的数组S，S中是否有元素a,b,c满足a+b+c=0？
找出数组S中所有满足条件的三元组。

双指针 + 排序

时间复杂度：O(n^2)
空间复杂度：O(1)
"""

def three_sum(nums):
    """
    三数之和为0
    """
    if len(nums) < 3:
        return []
    
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # 去重
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        # 优化：如果最小值都大于0，后面不可能为0
        if nums[i] > 0:
            break
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # 去重
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result

# 测试
if __name__ == "__main__":
    test_cases = [
        [-1, 0, 1, 2, -1, -4],
        [0, 0, 0, 0],
        [-2, 0, 1, 1, 2]
    ]
    
    for nums in test_cases:
        result = three_sum(nums)
        print(f"数组: {nums}")
        print(f"三数之和为0: {result}\n")

