"""
NC127 最长公共子序列(二)
https://www.nowcoder.com/practice/6d29638c85bb4ffd80c020fe244baf11

给定两个字符串str1和str2，输出两个字符串的最长公共子序列。如果最长公共子序列为空，则返回"-1"。

动态规划：
dp[i][j] = str1[0:i]和str2[0:j]的LCS长度

时间复杂度：O(n*m)
空间复杂度：O(n*m)
"""

def longest_common_subsequence(s1, s2):
    """
    返回LCS的长度和具体序列
    """
    m, n = len(s1), len(s2)
    
    # dp[i][j]表示s1[0:i]和s2[0:j]的LCS长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 填充dp表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # 回溯构造LCS
    if dp[m][n] == 0:
        return "-1"
    
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))

# 测试
if __name__ == "__main__":
    test_cases = [
        ("1A2C3D4B56", "B1D23A456A"),
        ("abc", "def"),
        ("abc", "abc")
    ]
    
    for s1, s2 in test_cases:
        result = longest_common_subsequence(s1, s2)
        print(f"s1={s1}, s2={s2}")
        print(f"LCS={result}\n")

