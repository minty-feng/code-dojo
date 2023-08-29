"""
LeetCode 461. 汉明距离
https://leetcode.cn/problems/hamming-distance/

两个整数之间的汉明距离指的是这两个数字对应二进制位不同的位置的数目。
给你两个整数x和y，计算并返回它们之间的汉明距离。

位运算

时间复杂度：O(1)
空间复杂度：O(1)
"""

def hamming_distance(x, y):
    """
    汉明距离 - 异或法
    
    Args:
        x: 第一个整数
        y: 第二个整数
        
    Returns:
        汉明距离
    """
    xor = x ^ y
    count = 0
    
    while xor:
        count += xor & 1
        xor >>= 1
    
    return count


def hamming_distance_builtin(x, y):
    """
    汉明距离 - 内置函数法
    
    Args:
        x: 第一个整数
        y: 第二个整数
        
    Returns:
        汉明距离
    """
    return bin(x ^ y).count('1')


def hamming_distance_brian_kernighan(x, y):
    """
    汉明距离 - Brian Kernighan算法
    
    Args:
        x: 第一个整数
        y: 第二个整数
        
    Returns:
        汉明距离
    """
    xor = x ^ y
    count = 0
    
    while xor:
        count += 1
        xor &= xor - 1  # 移除最右边的1
    
    return count


def test_hamming_distance():
    """测试函数"""
    # 测试用例1
    x1, y1 = 1, 4
    result1 = hamming_distance(x1, y1)
    result1_builtin = hamming_distance_builtin(x1, y1)
    result1_bk = hamming_distance_brian_kernighan(x1, y1)
    print(f"测试1 x={x1}, y={y1}: XOR={result1}, Builtin={result1_builtin}, BK={result1_bk}")  # 期望: 2
    
    # 测试用例2
    x2, y2 = 3, 1
    result2 = hamming_distance(x2, y2)
    result2_builtin = hamming_distance_builtin(x2, y2)
    result2_bk = hamming_distance_brian_kernighan(x2, y2)
    print(f"测试2 x={x2}, y={y2}: XOR={result2}, Builtin={result2_builtin}, BK={result2_bk}")  # 期望: 1
    
    # 测试用例3
    x3, y3 = 0, 0
    result3 = hamming_distance(x3, y3)
    result3_builtin = hamming_distance_builtin(x3, y3)
    result3_bk = hamming_distance_brian_kernighan(x3, y3)
    print(f"测试3 x={x3}, y={y3}: XOR={result3}, Builtin={result3_builtin}, BK={result3_bk}")  # 期望: 0


if __name__ == "__main__":
    test_hamming_distance()
