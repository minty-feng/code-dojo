/**
 * LeetCode 51. N皇后
 * https://leetcode.cn/problems/n-queens/
 * 
 * 按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。
 * n皇后问题研究的是如何将n个皇后放置在n×n的棋盘上，并且使皇后彼此之间不能相互攻击。
 * 
 * 回溯
 * 
 * 时间复杂度：O(N!)
 * 空间复杂度：O(N)
 */

class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> result;
        vector<string> board(n, string(n, '.'));
        
        backtrack(board, 0, result);
        return result;
    }
    
private:
    void backtrack(vector<string>& board, int row, vector<vector<string>>& result) {
        if (row == board.size()) {
            result.push_back(board);
            return;
        }
        
        for (int col = 0; col < board.size(); col++) {
            if (isValid(board, row, col)) {
                board[row][col] = 'Q';
                backtrack(board, row + 1, result);
                board[row][col] = '.';  // 回溯
            }
        }
    }
    
    bool isValid(vector<string>& board, int row, int col) {
        // 检查列
        for (int i = 0; i < row; i++) {
            if (board[i][col] == 'Q') {
                return false;
            }
        }
        
        // 检查左上对角线
        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 'Q') {
                return false;
            }
        }
        
        // 检查右上对角线
        for (int i = row - 1, j = col + 1; i >= 0 && j < board.size(); i--, j++) {
            if (board[i][j] == 'Q') {
                return false;
            }
        }
        
        return true;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <string>
using namespace std;

void testSolveNQueens() {
    Solution solution;
    
    int n = 4;
    vector<vector<string>> result = solution.solveNQueens(n);
    
    cout << "N皇后解决方案数量: " << result.size() << endl;
    for (int i = 0; i < result.size(); i++) {
        cout << "解决方案 " << (i + 1) << ":" << endl;
        for (const string& row : result[i]) {
            cout << row << endl;
        }
        cout << endl;
    }
}

int main() {
    testSolveNQueens();
    return 0;
}
