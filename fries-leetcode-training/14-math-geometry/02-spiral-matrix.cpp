/**
 * LeetCode 54. 螺旋矩阵
 * https://leetcode.cn/problems/spiral-matrix/
 * 
 * 给你一个m行n列的矩阵matrix，请按照顺时针螺旋顺序，返回矩阵中的所有元素。
 * 
 * 模拟
 * 
 * 时间复杂度：O(m*n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) {
            return {};
        }
        
        vector<int> result;
        int top = 0, bottom = matrix.size() - 1;
        int left = 0, right = matrix[0].size() - 1;
        
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

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void printVector(const vector<int>& vec) {
    cout << "[";
    for (int i = 0; i < vec.size(); i++) {
        cout << vec[i];
        if (i < vec.size() - 1) cout << ",";
    }
    cout << "]";
}

void testSpiralOrder() {
    Solution solution;
    
    vector<vector<int>> matrix1 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    vector<int> result1 = solution.spiralOrder(matrix1);
    cout << "测试1 {{1,2,3},{4,5,6},{7,8,9}}: ";
    printVector(result1);
    cout << endl;  // 期望: [1,2,3,6,9,8,7,4,5]
    
    vector<vector<int>> matrix2 = {{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}};
    vector<int> result2 = solution.spiralOrder(matrix2);
    cout << "测试2 {{1,2,3,4},{5,6,7,8},{9,10,11,12}}: ";
    printVector(result2);
    cout << endl;  // 期望: [1,2,3,4,8,12,11,10,9,5,6,7]
    
    vector<vector<int>> matrix3 = {{1}};
    vector<int> result3 = solution.spiralOrder(matrix3);
    cout << "测试3 {{1}}: ";
    printVector(result3);
    cout << endl;  // 期望: [1]
}

int main() {
    testSpiralOrder();
    return 0;
}
