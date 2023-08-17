"""
LeetCode 39. 组合总和
https://leetcode.cn/problems/combination-sum/

给你一个无重复元素的整数数组candidates和一个目标整数target，
找出candidates中可以使数字和为target的所有不同组合。

回溯

时间复杂度：O(2^t) t为target值
空间复杂度：O(target)
"""

def combination_sum(candidates, target):
    """
    组合总和 - 回溯法
    
    Args:
        candidates: 无重复元素的整数数组
        target: 目标整数
        
    Returns:
        所有不同组合
    """
    result = []
    candidates.sort()  # 排序以便剪枝
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # 剪枝：当前数字已经大于剩余值
            
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # 可以重复使用
            path.pop()  # 回溯
    
    backtrack(0, [], target)
    return result


def test_combination_sum():
    """测试函数"""
    # 测试用例1
    candidates1 = [2, 3, 6, 7]
    target1 = 7
    result1 = combination_sum(candidates1, target1)
    print(f"测试1 candidates=[2,3,6,7], target=7: {result1}")
    # 期望: [[2,2,3],[7]]
    
    # 测试用例2
    candidates2 = [2, 3, 5]
    target2 = 8
    result2 = combination_sum(candidates2, target2)
    print(f"测试2 candidates=[2,3,5], target=8: {result2}")
    # 期望: [[2,2,2,2],[2,3,3],[3,5]]


if __name__ == "__main__":
    test_combination_sum()
