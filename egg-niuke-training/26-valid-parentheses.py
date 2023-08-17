"""
NC52 有效括号序列
https://www.nowcoder.com/practice/37548e94a270412c8b9fb85643c8ccc2

给出一个仅包含字符'(',')','{','}','['和']',的字符串，判断给出的字符串是否是合法的括号序列。

栈的应用

时间复杂度：O(n)
空间复杂度：O(n)
"""

def is_valid_parentheses(s):
    """
    有效括号序列
    """
    if not s:
        return True
    
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # 右括号
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            # 左括号
            stack.append(char)
    
    return len(stack) == 0

# 测试
if __name__ == "__main__":
    test_cases = [
        "()",
        "()[]{}",
        "(]",
        "([)]",
        "{[]}",
        ""
    ]
    
    for s in test_cases:
        result = is_valid_parentheses(s)
        print(f"'{s}' 是否有效: {result}")

