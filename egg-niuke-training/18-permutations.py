"""
NC42 全排列
https://www.nowcoder.com/practice/4bcf3081067a4d028f95acee3ddcd2b1

给定一个不含重复数字的数组nums，返回其所有可能的全排列。

回溯算法
时间复杂度：O(n*n!)
空间复杂度：O(n)
"""

def permute(nums):
    """
    全排列 - 回溯法
    """
    result = []
    
    def backtrack(path, remaining):
        # 终止条件
        if not remaining:
            result.append(path[:])
            return
        
        # 选择列表
        for i in range(len(remaining)):
            # 做选择
            path.append(remaining[i])
            # 递归
            backtrack(path, remaining[:i] + remaining[i+1:])
            # 撤销选择
            path.pop()
    
    backtrack([], nums)
    return result

def permute_swap(nums):
    """
    全排列 - 交换法
    """
    result = []
    
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        
        for i in range(start, len(nums)):
            # 交换
            nums[start], nums[i] = nums[i], nums[start]
            # 递归
            backtrack(start + 1)
            # 回溯
            nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return result

# 测试
if __name__ == "__main__":
    nums = [1, 2, 3]
    
    result = permute(nums)
    print(f"数组 {nums} 的全排列:")
    for perm in result:
        print(perm)
    
    print(f"\n共 {len(result)} 种排列")

