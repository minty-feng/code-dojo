/**
 * LeetCode 48. 旋转图像
 * https://leetcode.cn/problems/rotate-image/
 * 
 * 给定一个n×n的二维矩阵matrix表示一个图像。请你将图像顺时针旋转90度。
 * 你必须在原地旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要使用另一个矩阵来旋转图像。
 * 
 * 数学变换
 * 
 * 时间复杂度：O(n^2)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();
        
        // 转置矩阵
        for (int i = 0; i < n; i++) {
            for (int j = i; j < n; j++) {
                swap(matrix[i][j], matrix[j][i]);
            }
        }
        
        // 翻转每一行
        for (int i = 0; i < n; i++) {
            reverse(matrix[i].begin(), matrix[i].end());
        }
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void printMatrix(const vector<vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int val : row) {
            cout << val << " ";
        }
        cout << endl;
    }
}

void testRotate() {
    Solution solution;
    
    vector<vector<int>> matrix1 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    cout << "测试1 原矩阵:" << endl;
    printMatrix(matrix1);
    
    solution.rotate(matrix1);
    cout << "旋转后:" << endl;
    printMatrix(matrix1);
    cout << "期望: [[7,4,1],[8,5,2],[9,6,3]]" << endl << endl;
    
    vector<vector<int>> matrix2 = {{5, 1, 9, 11}, {2, 4, 8, 10}, {13, 3, 6, 7}, {15, 14, 12, 16}};
    cout << "测试2 原矩阵:" << endl;
    printMatrix(matrix2);
    
    solution.rotate(matrix2);
    cout << "旋转后:" << endl;
    printMatrix(matrix2);
    cout << "期望: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]" << endl;
}

int main() {
    testRotate();
    return 0;
}
