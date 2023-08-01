"""
LeetCode 49. 字母异位词分组
https://leetcode.cn/problems/group-anagrams/

给你一个字符串数组，请你将字母异位词组合在一起。可以按任意顺序返回结果列表。

哈希表 + 字符串排序

时间复杂度：O(nklogk) k为字符串平均长度
空间复杂度：O(nk)
"""

from collections import defaultdict

def group_anagrams(strs):
    """
    字母异位词分组 - 排序法
    """
    groups = defaultdict(list)
    
    for s in strs:
        # 排序后的字符串作为key
        key = ''.join(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())

def group_anagrams_count(strs):
    """
    字母异位词分组 - 计数法
    """
    groups = defaultdict(list)
    
    for s in strs:
        # 字符计数作为key
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)
        groups[key].append(s)
    
    return list(groups.values())

# 测试
if __name__ == "__main__":
    test_cases = [
        ["eat", "tea", "tan", "ate", "nat", "bat"],
        [""],
        ["a"]
    ]
    
    for strs in test_cases:
        result = group_anagrams(strs)
        print(f"输入: {strs}")
        print(f"分组结果: {result}\n")

