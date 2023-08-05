"""
LeetCode 3. 无重复字符的最长子串
https://leetcode.cn/problems/longest-substring-without-repeating-characters/

给定一个字符串s，请你找出其中不含有重复字符的最长子串的长度。

滑动窗口 + 哈希表

时间复杂度：O(n)
空间复杂度：O(min(m,n)) m为字符集大小
"""

def length_of_longest_substring(s):
    """
    无重复字符的最长子串 - 滑动窗口
    """
    if not s:
        return 0
    
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # 如果右指针字符已存在，移动左指针
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # 添加右指针字符
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

# 测试
if __name__ == "__main__":
    test_cases = [
        "abcabcbb",
        "bbbbb",
        "pwwkew",
        ""
    ]
    
    for s in test_cases:
        result = length_of_longest_substring(s)
        print(f"字符串: '{s}'")
        print(f"最长无重复子串长度: {result}\n")

