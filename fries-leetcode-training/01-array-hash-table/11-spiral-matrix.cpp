/**
 * LeetCode 54. 螺旋矩阵
 * https://leetcode.cn/problems/spiral-matrix/
 * 
 * 给你一个m行n列的矩阵matrix，请按照顺时针螺旋顺序，返回矩阵中的所有元素。
 * 
 * 时间复杂度：O(m*n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) return {};
        
        int m = matrix.size(), n = matrix[0].size();
        vector<int> result;
        int top = 0, bottom = m - 1;
        int left = 0, right = n - 1;
        
        while (top <= bottom && left <= right) {
            // 从左到右
            for (int j = left; j <= right; j++) {
                result.push_back(matrix[top][j]);
            }
            top++;
            
            // 从上到下
            for (int i = top; i <= bottom; i++) {
                result.push_back(matrix[i][right]);
            }
            right--;
            
            // 从右到左
            if (top <= bottom) {
                for (int j = right; j >= left; j--) {
                    result.push_back(matrix[bottom][j]);
                }
                bottom--;
            }
            
            // 从下到上
            if (left <= right) {
                for (int i = bottom; i >= top; i--) {
                    result.push_back(matrix[i][left]);
                }
                left++;
            }
        }
        
        return result;
    }
};

int main() {
    Solution solution;
    vector<vector<vector<int>>> testCases = {
        {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}},
        {{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}},
        {{1, 2, 3}}
    };
    
    for (auto& matrix : testCases) {
        cout << "矩阵:" << endl;
        for (const auto& row : matrix) {
            for (int val : row) cout << val << " ";
            cout << endl;
        }
        
        vector<int> result = solution.spiralOrder(matrix);
        cout << "螺旋顺序: ";
        for (int val : result) cout << val << " ";
        cout << "\n" << endl;
    }
    
    return 0;
}

