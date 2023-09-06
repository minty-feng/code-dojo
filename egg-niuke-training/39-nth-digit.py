"""
NC132 数字序列中某一位的数字
https://www.nowcoder.com/practice/29311ff7404d44e0b07077f4201418f5

数字以0123456789101112131415...的格式序列化到一个字符序列中。
在这个序列中，第5位（从下标0开始计数）是5，第13位是1，第19位是4，等等。

数学计算

时间复杂度：O(logn)
空间复杂度：O(1)
"""

def find_nth_digit(n):
    """
    数字序列中某一位的数字
    """
    if n < 0:
        return -1
    
    digit = 1  # 位数
    start = 1  # 该位数的起始数字
    count = 9  # 该位数的数字个数
    
    # 确定n所在的位数
    while n > count:
        n -= count
        digit += 1
        start *= 10
        count = 9 * start * digit
    
    # 确定具体的数字
    num = start + (n - 1) // digit
    
    # 确定数字中的第几位
    digit_index = (n - 1) % digit
    
    return int(str(num)[digit_index])

# 测试
if __name__ == "__main__":
    test_cases = [5, 13, 19, 1000]
    
    for n in test_cases:
        result = find_nth_digit(n)
        print(f"第{n}位数字: {result}")

