/*
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
*/

#include <iostream>
using namespace std;

int multiLineInput() {
    int total = 0;
    int num;
    
    // 方法1：使用while(cin >> num)
    while (cin >> num) {
        total += num;
    }
    
    return total;
}

int multiLineInputAlternative() {
    int total = 0;
    int num;
    
    // 方法2：使用getline处理
    string line;
    while (getline(cin, line)) {
        if (line.empty()) break;
        num = stoi(line);
        total += num;
    }
    
    return total;
}

void testCases() {
    cout << "=== 多行输入测试 ===" << endl;
    
    // 模拟多行输入
    vector<int> test_data = {1, 2, 3, 4, 5};
    int total = 0;
    
    cout << "输入数据: ";
    for (int i = 0; i < test_data.size(); i++) {
        cout << test_data[i];
        if (i < test_data.size() - 1) cout << " ";
        total += test_data[i];
    }
    cout << endl;
    
    cout << "计算结果: " << total << endl;
    
    // 演示处理过程
    cout << "\n处理过程:" << endl;
    int running_sum = 0;
    for (int i = 0; i < test_data.size(); i++) {
        running_sum += test_data[i];
        cout << "第" << (i+1) << "行: " << test_data[i] 
             << ", 累计和: " << running_sum << endl;
    }
    
    cout << "\n最终结果: " << total << endl;
}

int main() {
    // 运行测试
    testCases();
    
    // 交互式输入（取消注释以启用）
    // int result = multiLineInput();
    // cout << result << endl;
    
    return 0;
}
