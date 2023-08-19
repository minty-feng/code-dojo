"""
LeetCode 72. 编辑距离
https://leetcode.cn/problems/edit-distance/

给你两个单词word1和word2，请返回将word1转换成word2所使用的最少操作数。
你可以对一个单词进行如下三种操作：
- 插入一个字符
- 删除一个字符
- 替换一个字符

动态规划

时间复杂度：O(m * n)
空间复杂度：O(m * n)
"""

def min_distance(word1, word2):
    """
    编辑距离 - 动态规划法
    
    Args:
        word1: 第一个单词
        word2: 第二个单词
        
    Returns:
        最少操作数
    """
    m, n = len(word1), len(word2)
    
    # 创建dp表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 初始化边界条件
    for i in range(m + 1):
        dp[i][0] = i  # word1的前i个字符变成空字符串需要i次删除操作
    
    for j in range(n + 1):
        dp[0][j] = j  # 空字符串变成word2的前j个字符需要j次插入操作
    
    # 填充dp表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # 字符相同，不需要操作
            else:
                dp[i][j] = min(
                    dp[i-1][j] + 1,      # 删除word1[i-1]
                    dp[i][j-1] + 1,      # 插入word2[j-1]
                    dp[i-1][j-1] + 1     # 替换word1[i-1]为word2[j-1]
                )
    
    return dp[m][n]


def min_distance_optimized(word1, word2):
    """
    编辑距离 - 空间优化版本
    
    Args:
        word1: 第一个单词
        word2: 第二个单词
        
    Returns:
        最少操作数
    """
    m, n = len(word1), len(word2)
    
    # 确保word1是较短的字符串
    if m > n:
        word1, word2 = word2, word1
        m, n = n, m
    
    # 使用两个一维数组
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        curr[0] = j
        for i in range(1, m + 1):
            if word1[i-1] == word2[j-1]:
                curr[i] = prev[i-1]
            else:
                curr[i] = min(
                    prev[i] + 1,      # 删除
                    curr[i-1] + 1,    # 插入
                    prev[i-1] + 1     # 替换
                )
        prev, curr = curr, prev
    
    return prev[m]


def test_min_distance():
    """测试函数"""
    # 测试用例1
    word1_1, word2_1 = "horse", "ros"
    result1 = min_distance(word1_1, word2_1)
    result1_opt = min_distance_optimized(word1_1, word2_1)
    print(f"测试1 '{word1_1}' -> '{word2_1}': DP={result1}, Opt={result1_opt}")  # 期望: 3
    
    # 测试用例2
    word1_2, word2_2 = "intention", "execution"
    result2 = min_distance(word1_2, word2_2)
    result2_opt = min_distance_optimized(word1_2, word2_2)
    print(f"测试2 '{word1_2}' -> '{word2_2}': DP={result2}, Opt={result2_opt}")  # 期望: 5
    
    # 测试用例3
    word1_3, word2_3 = "", "a"
    result3 = min_distance(word1_3, word2_3)
    result3_opt = min_distance_optimized(word1_3, word2_3)
    print(f"测试3 '{word1_3}' -> '{word2_3}': DP={result3}, Opt={result3_opt}")  # 期望: 1


if __name__ == "__main__":
    test_min_distance()
