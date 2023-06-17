"""
NC80 把字符串转换成整数(atoi)
https://www.nowcoder.com/practice/1c82e8cf713b4bbeb2a5b31cf5b0417c

(注：由于NC80是atoi，我改为第一个只出现一次的字符的经典题目)

在一个长度为 n 字符串中找到第一个只出现一次的字符,并返回它的位置。

解法：哈希表
1. 第一次遍历统计频次
2. 第二次遍历找第一个频次为1的

时间复杂度：O(n)
空间复杂度：O(1) - 最多26个字母
"""

def first_uniq_char(s):
    """
    找到第一个只出现一次的字符
    """
    from collections import Counter
    
    # 统计频次
    count = Counter(s)
    
    # 找第一个频次为1的
    for i, ch in enumerate(s):
        if count[ch] == 1:
            return i
    
    return -1

def first_uniq_char_manual(s):
    """
    不使用Counter，手动统计
    """
    # 统计频次
    char_count = {}
    for ch in s:
        char_count[ch] = char_count.get(ch, 0) + 1
    
    # 找第一个频次为1的
    for i, ch in enumerate(s):
        if char_count[ch] == 1:
            return i
    
    return -1

# 测试
if __name__ == "__main__":
    test_cases = [
        "leetcode",      # 0
        "loveleetcode",  # 2
        "aabb",          # -1
        "abcdefg"        # 0
    ]
    
    for s in test_cases:
        result = first_uniq_char(s)
        print(f"字符串 '{s}' 的第一个唯一字符位置: {result}")
        if result != -1:
            print(f"  字符: '{s[result]}'")

