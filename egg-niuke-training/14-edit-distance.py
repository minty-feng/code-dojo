"""
NC35 编辑距离
https://www.nowcoder.com/practice/05fed41805ae4394ab6607d0d745c8e4

给定两个字符串word1和word2，计算出将word1转换成word2所使用的最少操作数。
你可以对一个字符串进行如下三种操作：
1. 插入一个字符
2. 删除一个字符
3. 替换一个字符

动态规划：
dp[i][j] = word1[0:i]转换为word2[0:j]的最小操作数

时间复杂度：O(m*n)
空间复杂度：O(m*n)
"""

def min_distance(word1, word2):
    """
    编辑距离 - 动态规划
    """
    m, n = len(word1), len(word2)
    
    # dp[i][j]表示word1[0:i]转换为word2[0:j]的最小操作数
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 初始化：空串转换
    for i in range(m + 1):
        dp[i][0] = i  # 删除i个字符
    for j in range(n + 1):
        dp[0][j] = j  # 插入j个字符
    
    # 状态转移
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(
                    dp[i-1][j] + 1,    # 删除
                    dp[i][j-1] + 1,    # 插入
                    dp[i-1][j-1] + 1   # 替换
                )
    
    return dp[m][n]

def min_distance_optimized(word1, word2):
    """
    空间优化版本 O(n)
    """
    m, n = len(word1), len(word2)
    
    # 只需要保存前一行
    prev = list(range(n + 1))
    
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = min(prev[j], curr[j-1], prev[j-1]) + 1
        prev = curr
    
    return prev[n]

# 测试
if __name__ == "__main__":
    test_cases = [
        ("horse", "ros"),
        ("intention", "execution"),
        ("", "a"),
        ("a", "")
    ]
    
    for word1, word2 in test_cases:
        dist = min_distance(word1, word2)
        print(f"'{word1}' -> '{word2}': 编辑距离 = {dist}")

