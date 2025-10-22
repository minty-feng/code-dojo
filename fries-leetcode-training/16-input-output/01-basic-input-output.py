"""
01-基础输入输出处理

题目描述：
演示基本的输入输出处理，包括整数、字符串、数组的读取和输出。

输入格式：
第一行：整数n
第二行：n个整数，空格分隔
第三行：字符串

输出格式：
第一行：整数n
第二行：n个整数，空格分隔
第三行：字符串

示例：
输入：
5
1 2 3 4 5
hello world

输出：
5
1 2 3 4 5
hello world
"""

def basic_input_output():
    """基础输入输出处理"""
    # 读取整数
    n = int(input())
    
    # 读取整数数组
    arr = list(map(int, input().split()))
    
    # 读取字符串
    s = input().strip()
    
    # 输出
    print(n)
    print(*arr)  # 输出数组，空格分隔
    print(s)

def test_cases():
    """测试用例"""
    print("=== 基础输入输出测试 ===")
    
    # 模拟输入
    test_input = """5
1 2 3 4 5
hello world"""
    
    # 分割输入行
    lines = test_input.strip().split('\n')
    
    # 处理输入
    n = int(lines[0])
    arr = list(map(int, lines[1].split()))
    s = lines[2]
    
    # 输出结果
    print(f"整数: {n}")
    print(f"数组: {arr}")
    print(f"字符串: {s}")
    
    print("\n格式化输出:")
    print(n)
    print(*arr)
    print(s)

if __name__ == "__main__":
    # 运行测试
    test_cases()
    
    # 交互式输入（取消注释以启用）
    # basic_input_output()
