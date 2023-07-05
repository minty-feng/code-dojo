"""
NC61 字符串的排列
https://www.nowcoder.com/practice/fe6b651b66ae47d7acce78ffdd9a96c7

输入一个长度为 n 字符串，打印出该字符串中字符的所有排列，你可以以任意顺序返回这个字符串数组。
注意：字符串可能有重复字符。

回溯 + 去重

时间复杂度：O(n*n!)
空间复杂度：O(n)
"""

def permutation(s):
    """
    字符串的所有排列（去重）
    """
    result = []
    chars = sorted(list(s))  # 排序便于去重
    used = [False] * len(chars)
    
    def backtrack(path):
        if len(path) == len(chars):
            result.append(''.join(path))
            return
        
        for i in range(len(chars)):
            # 已使用过
            if used[i]:
                continue
            
            # 去重：相同元素，前面的没用过就跳过
            if i > 0 and chars[i] == chars[i-1] and not used[i-1]:
                continue
            
            # 做选择
            path.append(chars[i])
            used[i] = True
            
            # 递归
            backtrack(path)
            
            # 撤销选择
            path.pop()
            used[i] = False
    
    backtrack([])
    return result

# 测试
if __name__ == "__main__":
    test_cases = [
        "abc",
        "abb",
        "aab"
    ]
    
    for s in test_cases:
        result = permutation(s)
        print(f"'{s}' 的排列:")
        for perm in result:
            print(f"  {perm}")
        print(f"共 {len(result)} 种\n")

