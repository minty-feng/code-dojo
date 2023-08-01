/**
 * LeetCode 48. 旋转图像
 * https://leetcode.cn/problems/rotate-image/
 * 
 * 给定一个n×n的二维矩阵matrix表示一个图像。请你将图像顺时针旋转90度。
 * 
 * 时间复杂度：O(n^2)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

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

int main() {
    Solution solution;
    vector<vector<int>> matrix = {{1,2,3},{4,5,6},{7,8,9}};
    
    cout << "原矩阵:" << endl;
    for (const auto& row : matrix) {
        for (int val : row) cout << val << " ";
        cout << endl;
    }
    
    solution.rotate(matrix);
    
    cout << "旋转后:" << endl;
    for (const auto& row : matrix) {
        for (int val : row) cout << val << " ";
        cout << endl;
    }
    
    return 0;
}

