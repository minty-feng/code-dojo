"""
NC143 最小覆盖子串
https://www.nowcoder.com/practice/c466d480d20c4c7c9d322d12ca7955ac

给出两个字符串S和T，要求在O(n)的时间复杂度内在S中找出最短的包含T中所有字符的子串。

滑动窗口 + 双指针

时间复杂度：O(n)
空间复杂度：O(1)
"""

def min_window(s, t):
    """
    最小覆盖子串
    """
    if not s or not t or len(s) < len(t):
        return ""
    
    # 统计t中每个字符的频次
    need = {}
    for char in t:
        need[char] = need.get(char, 0) + 1
    
    # 滑动窗口
    left = 0
    valid = 0  # 窗口中满足条件的字符个数
    window = {}
    
    start = 0
    min_len = float('inf')
    
    for right in range(len(s)):
        c = s[right]
        
        # 右移窗口
        if c in need:
            window[c] = window.get(c, 0) + 1
            if window[c] == need[c]:
                valid += 1
        
        # 收缩窗口
        while valid == len(need):
            # 更新最小覆盖子串
            if right - left + 1 < min_len:
                start = left
                min_len = right - left + 1
            
            d = s[left]
            left += 1
            
            if d in need:
                if window[d] == need[d]:
                    valid -= 1
                window[d] -= 1
    
    return s[start:start + min_len] if min_len != float('inf') else ""

# 测试
if __name__ == "__main__":
    test_cases = [
        ("ADOBECODEBANC", "ABC"),
        ("a", "a"),
        ("a", "aa")
    ]
    
    for s, t in test_cases:
        result = min_window(s, t)
        print(f"s='{s}', t='{t}'")
        print(f"最小覆盖子串: '{result}'\n")

