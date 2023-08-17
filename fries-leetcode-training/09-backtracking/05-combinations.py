"""
LeetCode 77. 组合
https://leetcode.cn/problems/combinations/

给定两个整数n和k，返回范围[1, n]中所有可能的k个数的组合。

回溯

时间复杂度：O(C(n,k) * k)
空间复杂度：O(k)
"""

def combine(n, k):
    """
    组合 - 回溯法
    
    Args:
        n: 范围[1, n]
        k: 组合中数字的个数
        
    Returns:
        所有可能的k个数的组合
    """
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        
        # 剪枝：剩余数字不够组成k个数的组合
        for i in range(start, n + 1):
            if len(path) + (n - i + 1) < k:
                break
            
            path.append(i)
            backtrack(i + 1, path)
            path.pop()  # 回溯
    
    backtrack(1, [])
    return result


def test_combine():
    """测试函数"""
    # 测试用例1
    n1, k1 = 4, 2
    result1 = combine(n1, k1)
    print(f"测试1 n=4,k=2: {result1}")
    # 期望: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
    
    # 测试用例2
    n2, k2 = 1, 1
    result2 = combine(n2, k2)
    print(f"测试2 n=1,k=1: {result2}")
    # 期望: [[1]]


if __name__ == "__main__":
    test_combine()
