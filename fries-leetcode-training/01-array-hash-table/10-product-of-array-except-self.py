"""
LeetCode 238. 除自身以外数组的乘积
https://leetcode.cn/problems/product-of-array-except-self/

给你一个整数数组nums，返回数组answer，其中answer[i]等于nums中除nums[i]之外其余各元素的乘积。

左右乘积列表

时间复杂度：O(n)
空间复杂度：O(1)
"""

def product_except_self(nums):
    """
    除自身以外数组的乘积 - 左右乘积列表
    """
    n = len(nums)
    result = [1] * n
    
    # 计算左乘积
    for i in range(1, n):
        result[i] = result[i-1] * nums[i-1]
    
    # 计算右乘积并更新结果
    right_product = 1
    for i in range(n-1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result

# 测试
if __name__ == "__main__":
    test_cases = [
        [1, 2, 3, 4],
        [-1, 1, 0, -3, 3],
        [2, 3, 4, 5]
    ]
    
    for nums in test_cases:
        result = product_except_self(nums)
        print(f"数组: {nums}")
        print(f"除自身以外乘积: {result}\n")

