"""
LeetCode 567. 字符串的排列
https://leetcode.cn/problems/permutation-in-string/

给你两个字符串s1和s2，写一个函数来判断s2是否包含s1的排列。
换句话说，第一个字符串的排列之一是第二个字符串的子串。

滑动窗口 + 哈希表

时间复杂度：O(n)
空间复杂度：O(1)
"""

def check_inclusion(s1, s2):
    """
    字符串的排列 - 滑动窗口法
    
    Args:
        s1: 模式串
        s2: 目标串
        
    Returns:
        是否包含排列
    """
    if len(s1) > len(s2):
        return False
    
    # 统计s1中每个字符的频次
    need = {}
    for c in s1:
        need[c] = need.get(c, 0) + 1
    
    # 滑动窗口
    window = {}
    left = 0
    valid = 0
    
    for right in range(len(s2)):
        c = s2[right]
        
        # 扩展窗口
        if c in need:
            window[c] = window.get(c, 0) + 1
            if window[c] == need[c]:
                valid += 1
        
        # 收缩窗口
        while right - left + 1 >= len(s1):
            if valid == len(need):
                return True
            
            d = s2[left]
            left += 1
            
            if d in need:
                if window[d] == need[d]:
                    valid -= 1
                window[d] -= 1
    
    return False


def test_check_inclusion():
    """测试函数"""
    # 测试用例1
    s1_1, s2_1 = "ab", "eidbaooo"
    result1 = check_inclusion(s1_1, s2_1)
    print(f"测试1: {result1}")
    # 期望: True
    
    # 测试用例2
    s1_2, s2_2 = "ab", "eidboaoo"
    result2 = check_inclusion(s1_2, s2_2)
    print(f"测试2: {result2}")
    # 期望: False
    
    # 测试用例3
    s1_3, s2_3 = "adc", "dcda"
    result3 = check_inclusion(s1_3, s2_3)
    print(f"测试3: {result3}")
    # 期望: True


if __name__ == "__main__":
    test_check_inclusion()
