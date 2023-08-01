"""
LeetCode 287. 寻找重复数
https://leetcode.cn/problems/find-the-duplicate-number/

给定一个包含n+1个整数的数组nums，其数字都在1到n之间（包括1和n），可知至少存在一个重复的整数。

快慢指针（Floyd判圈算法）

时间复杂度：O(n)
空间复杂度：O(1)
"""

def find_duplicate(nums):
    """
    寻找重复数 - 快慢指针
    """
    # 第一阶段：找到相遇点
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    # 第二阶段：找到环的入口
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    
    return slow

# 测试
if __name__ == "__main__":
    test_cases = [
        [1, 3, 4, 2, 2],
        [3, 1, 3, 4, 2],
        [1, 1]
    ]
    
    for nums in test_cases:
        result = find_duplicate(nums)
        print(f"数组: {nums}")
        print(f"重复数: {result}\n")

