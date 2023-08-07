"""
LeetCode 20. 有效的括号
https://leetcode.cn/problems/valid-parentheses/

给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串s，判断字符串是否有效。

栈

时间复杂度：O(n)
空间复杂度：O(n)
"""

def is_valid(s):
    """
    有效的括号 - 栈法
    
    Args:
        s: 字符串
        
    Returns:
        是否有效
    """
    if len(s) % 2 == 1:
        return False
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack


def test_is_valid():
    """测试函数"""
    # 测试用例1
    s1 = "()"
    result1 = is_valid(s1)
    print(f"测试1: {result1}")
    # 期望: True
    
    # 测试用例2
    s2 = "()[]{}"
    result2 = is_valid(s2)
    print(f"测试2: {result2}")
    # 期望: True
    
    # 测试用例3
    s3 = "(]"
    result3 = is_valid(s3)
    print(f"测试3: {result3}")
    # 期望: False
    
    # 测试用例4
    s4 = "([)]"
    result4 = is_valid(s4)
    print(f"测试4: {result4}")
    # 期望: False


if __name__ == "__main__":
    test_is_valid()
