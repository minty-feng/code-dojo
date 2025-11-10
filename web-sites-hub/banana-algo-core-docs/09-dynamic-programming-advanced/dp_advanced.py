"""
DP进阶问题实现
"""

# ========== 最长公共子序列 ==========

def longest_common_subsequence(text1, text2):
    """LCS"""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]


# ========== 编辑距离 ==========

def min_distance(word1, word2):
    """编辑距离"""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # 删除
                    dp[i][j-1],    # 插入
                    dp[i-1][j-1]   # 替换
                )
    
    return dp[m][n]


# ========== 最长回文子串 ==========

def longest_palindrome(s):
    """最长回文子串"""
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    
    # 初始化
    for i in range(n):
        dp[i][i] = True
    
    # 长度为2
    for i in range(n - 1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            start = i
            max_len = 2
    
    # 长度>=3
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i+1][j-1]:
                dp[i][j] = True
                start = i
                max_len = length
    
    return s[start:start + max_len]


# ========== 股票问题 ==========

def max_profit_one(prices):
    """买卖一次"""
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    
    return max_profit


def max_profit_unlimited(prices):
    """买卖多次"""
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    return profit


def max_profit_k(k, prices):
    """最多k次交易"""
    if not prices:
        return 0
    
    n = len(prices)
    if k >= n // 2:
        return max_profit_unlimited(prices)
    
    # dp[i][j][0/1] = 第i天，最多j次交易，不持有/持有
    dp = [[[0, 0] for _ in range(k + 1)] for _ in range(n)]
    
    for i in range(n):
        for j in range(k, 0, -1):
            if i == 0:
                dp[i][j][0] = 0
                dp[i][j][1] = -prices[i]
            else:
                dp[i][j][0] = max(dp[i-1][j][0], dp[i-1][j][1] + prices[i])
                dp[i][j][1] = max(dp[i-1][j][1], dp[i-1][j-1][0] - prices[i])
    
    return dp[n-1][k][0]


# ========== 打家劫舍II（环形） ==========

def rob_circular(nums):
    """环形房屋"""
    if len(nums) == 1:
        return nums[0]
    
    def rob_range(start, end):
        prev, curr = 0, 0
        for i in range(start, end):
            prev, curr = curr, max(curr, prev + nums[i])
        return curr
    
    return max(
        rob_range(0, len(nums) - 1),
        rob_range(1, len(nums))
    )


# ========== 最长递增子序列（二分优化） ==========

def length_of_lis_binary(nums):
    """LIS O(n log n)"""
    if not nums:
        return 0
    
    tails = []
    
    for num in nums:
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num
    
    return len(tails)


def demo():
    """演示DP进阶"""
    print("=== DP进阶演示 ===\n")
    
    # LCS
    text1, text2 = "abcde", "ace"
    print(f"最长公共子序列 '{text1}' 和 '{text2}':")
    print(f"  长度: {longest_common_subsequence(text1, text2)}\n")
    
    # 编辑距离
    word1, word2 = "horse", "ros"
    print(f"编辑距离 '{word1}' -> '{word2}':")
    print(f"  最少操作: {min_distance(word1, word2)}\n")
    
    # 最长回文
    s = "babad"
    print(f"最长回文子串 '{s}':")
    print(f"  结果: {longest_palindrome(s)}\n")
    
    # 股票
    prices = [7,1,5,3,6,4]
    print(f"股票问题 {prices}:")
    print(f"  买卖一次: {max_profit_one(prices)}")
    print(f"  买卖多次: {max_profit_unlimited(prices)}")
    print(f"  最多2次: {max_profit_k(2, prices)}\n")
    
    # 打家劫舍II
    nums = [2,3,2]
    print(f"打家劫舍II（环形）{nums}:")
    print(f"  最大金额: {rob_circular(nums)}\n")
    
    # LIS
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"最长递增子序列 {nums}:")
    print(f"  长度: {length_of_lis_binary(nums)}")


if __name__ == '__main__':
    demo()

