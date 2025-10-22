/*
06-复杂数据结构输入输出处理

题目描述：
演示复杂嵌套数据结构的输入输出处理，包括map、vector嵌套等。

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
apple: 1 2 3
banana: 4 5
cherry: 6 7 8 9
*/

#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
using namespace std;

map<string, vector<int>> complexDataInputOutput() {
    int n;
    cin >> n;
    
    map<string, vector<int>> dataMap;
    
    for (int i = 0; i < n; i++) {
        string key;
        cin >> key;
        
        vector<int> values;
        int val;
        while (cin >> val) {
            values.push_back(val);
            if (cin.peek() == '\n') break;
        }
        
        dataMap[key] = values;
    }
    
    return dataMap;
}

struct DataStats {
    int count;
    int sum;
    double avg;
    int max_val;
    int min_val;
};

map<string, DataStats> processComplexData(const map<string, vector<int>>& dataMap) {
    map<string, DataStats> result;
    
    for (const auto& pair : dataMap) {
        const string& key = pair.first;
        const vector<int>& values = pair.second;
        
        DataStats stats;
        stats.count = values.size();
        stats.sum = 0;
        stats.max_val = INT_MIN;
        stats.min_val = INT_MAX;
        
        for (int val : values) {
            stats.sum += val;
            stats.max_val = max(stats.max_val, val);
            stats.min_val = min(stats.min_val, val);
        }
        
        stats.avg = stats.count > 0 ? (double)stats.sum / stats.count : 0.0;
        
        result[key] = stats;
    }
    
    return result;
}

void printComplexData(const map<string, vector<int>>& dataMap) {
    cout << "原始数据:" << endl;
    for (const auto& pair : dataMap) {
        cout << pair.first << ": ";
        for (int i = 0; i < pair.second.size(); i++) {
            cout << pair.second[i];
            if (i < pair.second.size() - 1) cout << " ";
        }
        cout << endl;
    }
    
    cout << "\n处理后的数据:" << endl;
    map<string, DataStats> processed = processComplexData(dataMap);
    
    for (const auto& pair : dataMap) {
        const string& key = pair.first;
        const vector<int>& values = pair.second;
        const DataStats& stats = processed[key];
        
        cout << key << ": ";
        for (int i = 0; i < values.size(); i++) {
            cout << values[i];
            if (i < values.size() - 1) cout << " ";
        }
        cout << endl;
        
        cout << "  统计: 数量=" << stats.count 
             << ", 和=" << stats.sum 
             << ", 平均=" << fixed << setprecision(2) << stats.avg
             << ", 最大=" << stats.max_val 
             << ", 最小=" << stats.min_val << endl;
    }
}

void testCases() {
    cout << "=== 复杂数据结构输入输出测试 ===" << endl;
    
    // 模拟输入数据
    map<string, vector<int>> testData = {
        {"apple", {1, 2, 3}},
        {"banana", {4, 5}},
        {"cherry", {6, 7, 8, 9}}
    };
    
    cout << "输入数据:" << endl;
    for (const auto& pair : testData) {
        cout << pair.first << ": ";
        for (int i = 0; i < pair.second.size(); i++) {
            cout << pair.second[i];
            if (i < pair.second.size() - 1) cout << " ";
        }
        cout << endl;
    }
    
    // 处理数据
    printComplexData(testData);
}

int main() {
    // 运行测试
    testCases();
    
    // 交互式输入（取消注释以启用）
    // map<string, vector<int>> data = complexDataInputOutput();
    // printComplexData(data);
    
    return 0;
}
