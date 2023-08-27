/**
 * LeetCode 73. 矩阵置零
 * https://leetcode.cn/problems/set-matrix-zeroes/
 * 
 * 给定一个m x n的矩阵，如果一个元素为0，则将其所在行和列的所有元素都设为0。请使用原地算法。
 * 
 * 原地算法
 * 
 * 时间复杂度：O(m*n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) {
            return;
        }
        
        int m = matrix.size();
        int n = matrix[0].size();
        
        // 使用第一行和第一列作为标记
        bool firstRowZero = false;
        bool firstColZero = false;
        
        // 检查第一行是否有0
        for (int j = 0; j < n; j++) {
            if (matrix[0][j] == 0) {
                firstRowZero = true;
                break;
            }
        }
        
        // 检查第一列是否有0
        for (int i = 0; i < m; i++) {
            if (matrix[i][0] == 0) {
                firstColZero = true;
                break;
            }
        }
        
        // 标记需要置零的行和列
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][j] == 0) {
                    matrix[i][0] = 0;  // 标记第i行
                    matrix[0][j] = 0;  // 标记第j列
                }
            }
        }
        
        // 根据标记置零
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) {
                    matrix[i][j] = 0;
                }
            }
        }
        
        // 处理第一行和第一列
        if (firstRowZero) {
            for (int j = 0; j < n; j++) {
                matrix[0][j] = 0;
            }
        }
        
        if (firstColZero) {
            for (int i = 0; i < m; i++) {
                matrix[i][0] = 0;
            }
        }
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void printMatrix(const vector<vector<int>>& matrix) {
    cout << "[";
    for (int i = 0; i < matrix.size(); i++) {
        cout << "[";
        for (int j = 0; j < matrix[i].size(); j++) {
            cout << matrix[i][j];
            if (j < matrix[i].size() - 1) cout << ",";
        }
        cout << "]";
        if (i < matrix.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

void testSetZeroes() {
    Solution solution;
    
    vector<vector<int>> matrix1 = {{1, 1, 1}, {1, 0, 1}, {1, 1, 1}};
    cout << "测试1 原矩阵: ";
    printMatrix(matrix1);
    
    solution.setZeroes(matrix1);
    cout << "置零后: ";
    printMatrix(matrix1);
    cout << "期望: [[1,0,1],[0,0,0],[1,0,1]]" << endl << endl;
    
    vector<vector<int>> matrix2 = {{0, 1, 2, 0}, {3, 4, 5, 2}, {1, 3, 1, 5}};
    cout << "测试2 原矩阵: ";
    printMatrix(matrix2);
    
    solution.setZeroes(matrix2);
    cout << "置零后: ";
    printMatrix(matrix2);
    cout << "期望: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]" << endl;
}

int main() {
    testSetZeroes();
    return 0;
}
