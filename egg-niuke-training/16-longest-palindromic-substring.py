"""
NC17 最长回文子串
https://www.nowcoder.com/practice/b4525d1d84934cf280439aeecc36f4af

对于长度为n的一个字符串A，找到一个最长的回文子串。

解法1：中心扩展法 O(n^2)
解法2：动态规划 O(n^2)
解法3：Manacher算法 O(n)

时间复杂度：O(n^2) - 中心扩展
空间复杂度：O(1)
"""

def longest_palindrome_center(s):
    """
    方法1：中心扩展法
    """
    if not s:
        return ""
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1
    
    start = end = 0
    
    for i in range(len(s)):
        # 奇数长度回文
        left1, right1 = expand_around_center(i, i)
        # 偶数长度回文
        left2, right2 = expand_around_center(i, i + 1)
        
        # 选择更长的
        if right1 - left1 > end - start:
            start, end = left1, right1
        if right2 - left2 > end - start:
            start, end = left2, right2
    
    return s[start:end+1]

def longest_palindrome_dp(s):
    """
    方法2：动态规划
    dp[i][j]表示s[i:j+1]是否为回文
    """
    if not s:
        return ""
    
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    
    # 单个字符都是回文
    for i in range(n):
        dp[i][i] = True
    
    # 枚举子串长度
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                if length == 2:
                    dp[i][j] = True
                else:
                    dp[i][j] = dp[i+1][j-1]
            
            if dp[i][j] and length > max_len:
                start = i
                max_len = length
    
    return s[start:start+max_len]

# 测试
if __name__ == "__main__":
    test_cases = [
        "babad",
        "cbbd",
        "a",
        "ac"
    ]
    
    for s in test_cases:
        print(f"字符串: {s}")
        print(f"中心扩展: {longest_palindrome_center(s)}")
        print(f"动态规划: {longest_palindrome_dp(s)}\n")

