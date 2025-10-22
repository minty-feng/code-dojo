/*
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
*/

#include <iostream>
#include <vector>
#include <string>
using namespace std;

void basicInputOutput() {
    int n;
    cin >> n;
    
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    // 读取字符串（跳过换行符）
    cin.ignore();
    string s;
    getline(cin, s);
    
    // 输出
    cout << n << endl;
    for (int i = 0; i < n; i++) {
        cout << arr[i];
        if (i < n - 1) cout << " ";
    }
    cout << endl;
    cout << s << endl;
}

void testCases() {
    cout << "=== 基础输入输出测试 ===" << endl;
    
    // 模拟输入数据
    int n = 5;
    vector<int> arr = {1, 2, 3, 4, 5};
    string s = "hello world";
    
    cout << "整数: " << n << endl;
    cout << "数组: ";
    for (int i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << " ";
    }
    cout << endl;
    cout << "字符串: " << s << endl;
    
    cout << "\n格式化输出:" << endl;
    cout << n << endl;
    for (int i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << " ";
    }
    cout << endl;
    cout << s << endl;
}

int main() {
    // 运行测试
    testCases();
    
    // 交互式输入（取消注释以启用）
    // basicInputOutput();
    
    return 0;
}
