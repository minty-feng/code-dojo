"""
LeetCode 438. 找到字符串中所有字母异位词
https://leetcode.cn/problems/find-all-anagrams-in-a-string/

给定两个字符串s和p，找到s中所有p的字母异位词的子串，返回这些子串的起始索引。

滑动窗口

时间复杂度：O(|s| + |p|)
空间复杂度：O(|s| + |p|)
"""

def find_anagrams(s, p):
    """
    找到字符串中所有字母异位词 - 滑动窗口
    """
    if len(s) < len(p):
        return []
    
    # 统计p中每个字符的频次
    need = {}
    for char in p:
        need[char] = need.get(char, 0) + 1
    
    # 滑动窗口
    left = 0
    valid = 0
    window = {}
    result = []
    
    for right in range(len(s)):
        c = s[right]
        window[c] = window.get(c, 0) + 1
        
        if c in need and window[c] == need[c]:
            valid += 1
        
        # 收缩窗口
        while right - left + 1 >= len(p):
            if valid == len(need):
                result.append(left)
            
            d = s[left]
            left += 1
            
            if d in need:
                if window[d] == need[d]:
                    valid -= 1
                window[d] -= 1
    
    return result

# 测试
if __name__ == "__main__":
    test_cases = [
        ("cbaebabacd", "abc"),
        ("abab", "ab"),
        ("baa", "aa")
    ]
    
    for s, p in test_cases:
        result = find_anagrams(s, p)
        print(f"s: '{s}', p: '{p}'")
        print(f"字母异位词起始索引: {result}\n")

