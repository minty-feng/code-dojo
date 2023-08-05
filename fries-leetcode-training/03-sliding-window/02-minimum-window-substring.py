"""
LeetCode 76. 最小覆盖子串
https://leetcode.cn/problems/minimum-window-substring/

给你一个字符串s、一个字符串t。返回s中涵盖t所有字符的最小子串。

滑动窗口

时间复杂度：O(|s| + |t|)
空间复杂度：O(|s| + |t|)
"""

def min_window(s, t):
    """
    最小覆盖子串 - 滑动窗口
    """
    if not s or not t or len(s) < len(t):
        return ""
    
    # 统计t中每个字符的频次
    need = {}
    for char in t:
        need[char] = need.get(char, 0) + 1
    
    # 滑动窗口
    left = 0
    valid = 0  # 窗口中满足条件的字符种类数
    window = {}
    
    start = 0
    min_len = float('inf')
    
    for right in range(len(s)):
        c = s[right]
        window[c] = window.get(c, 0) + 1
        
        # 如果当前字符满足条件
        if c in need and window[c] == need[c]:
            valid += 1
        
        # 收缩窗口
        while valid == len(need):
            # 更新最小窗口
            if right - left + 1 < min_len:
                start = left
                min_len = right - left + 1
            
            d = s[left]
            left += 1
            
            if d in need:
                if window[d] == need[d]:
                    valid -= 1
                window[d] -= 1
    
    return "" if min_len == float('inf') else s[start:start + min_len]

# 测试
if __name__ == "__main__":
    test_cases = [
        ("ADOBECODEBANC", "ABC"),
        ("a", "a"),
        ("a", "aa")
    ]
    
    for s, t in test_cases:
        result = min_window(s, t)
        print(f"s: '{s}', t: '{t}'")
        print(f"最小覆盖子串: '{result}'\n")

