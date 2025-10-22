"""
02-多行输入处理

题目描述：
演示如何处理多行输入数据，包括未知行数的输入和EOF处理。

输入格式：
多行数据，每行包含一个整数，直到EOF

输出格式：
所有整数的和

示例：
输入：
1
2
3
4
5
(EOF)

输出：
15
"""

def multi_line_input():
    """多行输入处理"""
    total = 0
    
    try:
        while True:
            line = input()
            if not line:  # 空行表示结束
                break
            num = int(line.strip())
            total += num
    except EOFError:
        pass  # 到达文件末尾
    
    return total

def multi_line_input_alternative():
    """多行输入处理（替代方法）"""
    total = 0
    
    # 方法1：使用sys.stdin
    import sys
    for line in sys.stdin:
        if line.strip():  # 非空行
            num = int(line.strip())
            total += num
        else:
            break
    
    return total

def test_cases():
    """测试用例"""
    print("=== 多行输入测试 ===")
    
    # 模拟多行输入
    test_data = [1, 2, 3, 4, 5]
    total = sum(test_data)
    
    print(f"输入数据: {test_data}")
    print(f"计算结果: {total}")
    
    # 演示处理过程
    print("\n处理过程:")
    running_sum = 0
    for i, num in enumerate(test_data):
        running_sum += num
        print(f"第{i+1}行: {num}, 累计和: {running_sum}")
    
    print(f"\n最终结果: {total}")

if __name__ == "__main__":
    # 运行测试
    test_cases()
    
    # 交互式输入（取消注释以启用）
    # result = multi_line_input()
    # print(result)
