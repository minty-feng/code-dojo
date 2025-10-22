"""
06-复杂数据结构输入输出处理

题目描述：
演示复杂嵌套数据结构的输入输出处理，包括字典、列表嵌套等。

输入格式：
第一行：整数n（数据组数）
接下来n行：每行包含一个字符串和一个整数列表

输出格式：
输出处理后的数据结构

示例：
输入：
3
apple 1 2 3
banana 4 5
cherry 6 7 8 9

输出：
{'apple': [1, 2, 3], 'banana': [4, 5], 'cherry': [6, 7, 8, 9]}
"""

def complex_data_input_output():
    """复杂数据结构输入输出处理"""
    n = int(input())
    data_dict = {}
    
    for _ in range(n):
        line = input().split()
        key = line[0]
        values = list(map(int, line[1:]))
        data_dict[key] = values
    
    return data_dict

def process_complex_data(data_dict):
    """处理复杂数据结构"""
    result = {}
    
    for key, values in data_dict.items():
        # 计算统计信息
        stats = {
            'count': len(values),
            'sum': sum(values),
            'avg': sum(values) / len(values) if values else 0,
            'max': max(values) if values else 0,
            'min': min(values) if values else 0
        }
        result[key] = {
            'values': values,
            'stats': stats
        }
    
    return result

def print_complex_data(data_dict):
    """打印复杂数据结构"""
    print("原始数据:")
    print(data_dict)
    
    print("\n处理后的数据:")
    processed = process_complex_data(data_dict)
    for key, info in processed.items():
        print(f"{key}: {info['values']}")
        print(f"  统计: 数量={info['stats']['count']}, "
              f"和={info['stats']['sum']}, "
              f"平均={info['stats']['avg']:.2f}, "
              f"最大={info['stats']['max']}, "
              f"最小={info['stats']['min']}")

def test_cases():
    """测试用例"""
    print("=== 复杂数据结构输入输出测试 ===")
    
    # 模拟输入数据
    test_data = {
        'apple': [1, 2, 3],
        'banana': [4, 5],
        'cherry': [6, 7, 8, 9]
    }
    
    print("输入数据:")
    for key, values in test_data.items():
        print(f"{key}: {values}")
    
    # 处理数据
    print_complex_data(test_data)
    
    # 测试JSON格式输出
    import json
    print("\nJSON格式输出:")
    print(json.dumps(test_data, indent=2))

if __name__ == "__main__":
    # 运行测试
    test_cases()
    
    # 交互式输入（取消注释以启用）
    # data = complex_data_input_output()
    # print_complex_data(data)
