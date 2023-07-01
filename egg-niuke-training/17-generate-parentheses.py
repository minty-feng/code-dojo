"""
NC137 括号生成
https://www.nowcoder.com/practice/c9addb265cdf4cdd92c092c655d164ca

给出n对括号，请编写一个函数来生成所有的由n对括号组成的合法组合。

回溯算法：
- left: 左括号数量
- right: 右括号数量
- 剪枝条件：left <= n, right <= left

时间复杂度：O(4^n / sqrt(n)) - 第n个卡特兰数
空间复杂度：O(n)
"""

def generate_parenthesis(n):
    """
    生成所有合法括号组合 - 回溯法
    """
    result = []
    
    def backtrack(path, left, right):
        # 终止条件
        if len(path) == 2 * n:
            result.append(path)
            return
        
        # 添加左括号
        if left < n:
            backtrack(path + '(', left + 1, right)
        
        # 添加右括号
        if right < left:
            backtrack(path + ')', left, right + 1)
    
    backtrack('', 0, 0)
    return result

def generate_parenthesis_dp(n):
    """
    动态规划方法
    dp[i] = "(" + dp[j] + ")" + dp[i-1-j], 其中 j in [0, i-1]
    """
    if n == 0:
        return ['']
    
    dp = [[] for _ in range(n + 1)]
    dp[0] = ['']
    
    for i in range(1, n + 1):
        for j in range(i):
            for left in dp[j]:
                for right in dp[i-1-j]:
                    dp[i].append(f'({left}){right}')
    
    return dp[n]

# 测试
if __name__ == "__main__":
    for n in range(1, 5):
        result = generate_parenthesis(n)
        print(f"n={n}:")
        for s in result:
            print(f"  {s}")
        print(f"共 {len(result)} 种组合\n")

