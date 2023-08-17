/**
 * LeetCode 37. 解数独
 * https://leetcode.cn/problems/sudoku-solver/
 * 
 * 编写一个程序，通过填充空格来解决数独问题。
 * 
 * 回溯
 * 
 * 时间复杂度：O(9^(空格数))
 * 空间复杂度：O(1)
 */

class Solution {
public:
    void solveSudoku(vector<vector<char>>& board) {
        backtrack(board);
    }
    
private:
    bool backtrack(vector<vector<char>>& board) {
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (board[i][j] == '.') {
                    for (char c = '1'; c <= '9'; c++) {
                        if (isValid(board, i, j, c)) {
                            board[i][j] = c;
                            if (backtrack(board)) {
                                return true;
                            }
                            board[i][j] = '.';  // 回溯
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }
    
    bool isValid(vector<vector<char>>& board, int row, int col, char c) {
        // 检查行
        for (int j = 0; j < 9; j++) {
            if (board[row][j] == c) {
                return false;
            }
        }
        
        // 检查列
        for (int i = 0; i < 9; i++) {
            if (board[i][col] == c) {
                return false;
            }
        }
        
        // 检查3x3宫格
        int startRow = (row / 3) * 3;
        int startCol = (col / 3) * 3;
        for (int i = startRow; i < startRow + 3; i++) {
            for (int j = startCol; j < startCol + 3; j++) {
                if (board[i][j] == c) {
                    return false;
                }
            }
        }
        
        return true;
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testSolveSudoku() {
    Solution solution;
    
    vector<vector<char>> board = {
        {'5','3','.','.','7','.','.','.','.'},
        {'6','.','.','1','9','5','.','.','.'},
        {'.','9','8','.','.','.','.','6','.'},
        {'8','.','.','.','6','.','.','.','3'},
        {'4','.','.','8','.','3','.','.','1'},
        {'7','.','.','.','2','.','.','.','6'},
        {'.','6','.','.','.','.','2','8','.'},
        {'.','.','.','4','1','9','.','.','5'},
        {'.','.','.','.','8','.','.','7','9'}
    };
    
    cout << "原始数独:" << endl;
    for (const auto& row : board) {
        for (char c : row) {
            cout << c << " ";
        }
        cout << endl;
    }
    
    solution.solveSudoku(board);
    
    cout << "\n解数独后:" << endl;
    for (const auto& row : board) {
        for (char c : row) {
            cout << c << " ";
        }
        cout << endl;
    }
}

int main() {
    testSolveSudoku();
    return 0;
}
