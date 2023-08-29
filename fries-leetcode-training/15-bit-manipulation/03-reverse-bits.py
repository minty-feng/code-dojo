"""
LeetCode 190. 颠倒二进制位
https://leetcode.cn/problems/reverse-bits/

颠倒给定的32位无符号整数的二进制位。

位运算

时间复杂度：O(1)
空间复杂度：O(1)
"""

def reverse_bits(n):
    """
    颠倒二进制位 - 逐位法
    
    Args:
        n: 32位无符号整数
        
    Returns:
        颠倒后的32位无符号整数
    """
    result = 0
    
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    
    return result


def reverse_bits_optimized(n):
    """
    颠倒二进制位 - 优化法
    
    Args:
        n: 32位无符号整数
        
    Returns:
        颠倒后的32位无符号整数
    """
    # 分治思想：先交换16位，再交换8位，4位，2位，1位
    n = ((n & 0xffff0000) >> 16) | ((n & 0x0000ffff) << 16)
    n = ((n & 0xff00ff00) >> 8) | ((n & 0x00ff00ff) << 8)
    n = ((n & 0xf0f0f0f0) >> 4) | ((n & 0x0f0f0f0f) << 4)
    n = ((n & 0xcccccccc) >> 2) | ((n & 0x33333333) << 2)
    n = ((n & 0xaaaaaaaa) >> 1) | ((n & 0x55555555) << 1)
    
    return n


def reverse_bits_string(n):
    """
    颠倒二进制位 - 字符串法
    
    Args:
        n: 32位无符号整数
        
    Returns:
        颠倒后的32位无符号整数
    """
    # 转换为32位二进制字符串
    binary = format(n, '032b')
    # 颠倒字符串
    reversed_binary = binary[::-1]
    # 转换回整数
    return int(reversed_binary, 2)


def test_reverse_bits():
    """测试函数"""
    # 测试用例1
    n1 = 0b00000010100101000001111010011100
    result1 = reverse_bits(n1)
    result1_opt = reverse_bits_optimized(n1)
    result1_str = reverse_bits_string(n1)
    print(f"测试1 n={bin(n1)}: Bit={bin(result1)}, Opt={bin(result1_opt)}, Str={bin(result1_str)}")
    print(f"期望: 0b00111001011110000010100101000000")
    
    # 测试用例2
    n2 = 0b11111111111111111111111111111101
    result2 = reverse_bits(n2)
    result2_opt = reverse_bits_optimized(n2)
    result2_str = reverse_bits_string(n2)
    print(f"测试2 n={bin(n2)}: Bit={bin(result2)}, Opt={bin(result2_opt)}, Str={bin(result2_str)}")
    print(f"期望: 0b10111111111111111111111111111111")
    
    # 测试用例3
    n3 = 0b00000000000000000000000000000001
    result3 = reverse_bits(n3)
    result3_opt = reverse_bits_optimized(n3)
    result3_str = reverse_bits_string(n3)
    print(f"测试3 n={bin(n3)}: Bit={bin(result3)}, Opt={bin(result3_opt)}, Str={bin(result3_str)}")
    print(f"期望: 0b10000000000000000000000000000000")


if __name__ == "__main__":
    test_reverse_bits()
