/*
03-矩阵输入输出处理

题目描述：
演示二维数组（矩阵）的输入输出处理。

输入格式：
第一行：两个整数m, n（矩阵的行数和列数）
接下来m行：每行n个整数

输出格式：
输出矩阵，每行n个整数，空格分隔

示例：
输入：
3 4
1 2 3 4
5 6 7 8
9 10 11 12

输出：
1 2 3 4
5 6 7 8
9 10 11 12
*/

#include <iostream>
#include <vector>
using namespace std;

vector<vector<int>> matrixInputOutput() {
    int m, n;
    cin >> m >> n;
    
    vector<vector<int>> matrix(m, vector<int>(n));
    
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            cin >> matrix[i][j];
        }
    }
    
    // 输出矩阵
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            cout << matrix[i][j];
            if (j < n - 1) cout << " ";
        }
        cout << endl;
    }
    
    return matrix;
}

void matrixOperations(const vector<vector<int>>& matrix) {
    int m = matrix.size();
    int n = matrix[0].size();
    
    cout << "矩阵维度: " << m << " x " << n << endl;
    
    // 计算每行和
    cout << "每行和: ";
    for (int i = 0; i < m; i++) {
        int row_sum = 0;
        for (int j = 0; j < n; j++) {
            row_sum += matrix[i][j];
        }
        cout << row_sum;
        if (i < m - 1) cout << " ";
    }
    cout << endl;
    
    // 计算每列和
    cout << "每列和: ";
    for (int j = 0; j < n; j++) {
        int col_sum = 0;
        for (int i = 0; i < m; i++) {
            col_sum += matrix[i][j];
        }
        cout << col_sum;
        if (j < n - 1) cout << " ";
    }
    cout << endl;
    
    // 计算总和
    int total_sum = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            total_sum += matrix[i][j];
        }
    }
    cout << "总和: " << total_sum << endl;
}

void testCases() {
    cout << "=== 矩阵输入输出测试 ===" << endl;
    
    // 模拟矩阵数据
    vector<vector<int>> matrix = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    
    cout << "输入矩阵:" << endl;
    for (int i = 0; i < matrix.size(); i++) {
        for (int j = 0; j < matrix[i].size(); j++) {
            cout << matrix[i][j];
            if (j < matrix[i].size() - 1) cout << " ";
        }
        cout << endl;
    }
    
    cout << "\n矩阵操作:" << endl;
    matrixOperations(matrix);
}

int main() {
    // 运行测试
    testCases();
    
    // 交互式输入（取消注释以启用）
    // vector<vector<int>> matrix = matrixInputOutput();
    // matrixOperations(matrix);
    
    return 0;
}
