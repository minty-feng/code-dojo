"""
LeetCode 1143. 最长公共子序列
https://leetcode.cn/problems/longest-common-subsequence/

给定两个字符串text1和text2，返回这两个字符串的最长公共子序列的长度。
如果不存在公共子序列，返回0。

动态规划

时间复杂度：O(m * n)
空间复杂度：O(m * n)
"""

def longest_common_subsequence(text1, text2):
    """
    最长公共子序列 - 动态规划法
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        
    Returns:
        最长公共子序列的长度
    """
    m, n = len(text1), len(text2)
    
    # 创建dp表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 填充dp表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]


def longest_common_subsequence_optimized(text1, text2):
    """
    最长公共子序列 - 空间优化版本
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        
    Returns:
        最长公共子序列的长度
    """
    m, n = len(text1), len(text2)
    
    # 确保text1是较短的字符串
    if m > n:
        text1, text2 = text2, text1
        m, n = n, m
    
    # 使用两个一维数组
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if text1[i-1] == text2[j-1]:
                curr[i] = prev[i-1] + 1
            else:
                curr[i] = max(prev[i], curr[i-1])
        prev, curr = curr, prev
    
    return prev[m]


def longest_common_subsequence_with_path(text1, text2):
    """
    最长公共子序列 - 带路径记录版本
    
    Args:
        text1: 第一个字符串
        text2: 第二个字符串
        
    Returns:
        (最长公共子序列的长度, 最长公共子序列)
    """
    m, n = len(text1), len(text2)
    
    # 创建dp表和路径表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    path = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 填充dp表和路径表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                path[i][j] = 1  # 来自左上角
            else:
                if dp[i-1][j] > dp[i][j-1]:
                    dp[i][j] = dp[i-1][j]
                    path[i][j] = 2  # 来自上方
                else:
                    dp[i][j] = dp[i][j-1]
                    path[i][j] = 3  # 来自左方
    
    # 重构路径
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if path[i][j] == 1:
            lcs.append(text1[i-1])
            i -= 1
            j -= 1
        elif path[i][j] == 2:
            i -= 1
        else:
            j -= 1
    
    lcs.reverse()
    return dp[m][n], ''.join(lcs)


def test_longest_common_subsequence():
    """测试函数"""
    # 测试用例1
    text1_1, text2_1 = "abcde", "ace"
    result1 = longest_common_subsequence(text1_1, text2_1)
    result1_opt = longest_common_subsequence_optimized(text1_1, text2_1)
    length1, lcs1 = longest_common_subsequence_with_path(text1_1, text2_1)
    print(f"测试1 '{text1_1}' & '{text2_1}': DP={result1}, Opt={result1_opt}, LCS='{lcs1}'")  # 期望: 3
    
    # 测试用例2
    text1_2, text2_2 = "abc", "abc"
    result2 = longest_common_subsequence(text1_2, text2_2)
    result2_opt = longest_common_subsequence_optimized(text1_2, text2_2)
    length2, lcs2 = longest_common_subsequence_with_path(text1_2, text2_2)
    print(f"测试2 '{text1_2}' & '{text2_2}': DP={result2}, Opt={result2_opt}, LCS='{lcs2}'")  # 期望: 3
    
    # 测试用例3
    text1_3, text2_3 = "abc", "def"
    result3 = longest_common_subsequence(text1_3, text2_3)
    result3_opt = longest_common_subsequence_optimized(text1_3, text2_3)
    length3, lcs3 = longest_common_subsequence_with_path(text1_3, text2_3)
    print(f"测试3 '{text1_3}' & '{text2_3}': DP={result3}, Opt={result3_opt}, LCS='{lcs3}'")  # 期望: 0


if __name__ == "__main__":
    test_longest_common_subsequence()
