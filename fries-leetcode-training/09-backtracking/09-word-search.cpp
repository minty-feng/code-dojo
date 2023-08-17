/**
 * LeetCode 79. 单词搜索
 * https://leetcode.cn/problems/word-search/
 * 
 * 给定一个m x n二维字符网格board和一个字符串单词word。
 * 如果word存在于网格中，返回true；否则，返回false。
 * 
 * DFS回溯
 * 
 * 时间复杂度：O(m*n*4^L) L为单词长度
 * 空间复杂度：O(L)
 */

class Solution {
public:
    bool exist(vector<vector<char>>& board, string word) {
        if (board.empty() || board[0].empty() || word.empty()) {
            return false;
        }
        
        int rows = board.size();
        int cols = board[0].size();
        
        // 从每个位置开始搜索
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (dfs(board, word, i, j, 0)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
private:
    bool dfs(vector<vector<char>>& board, const string& word, int row, int col, int index) {
        if (index == word.length()) {
            return true;
        }
        
        if (row < 0 || row >= board.size() || col < 0 || col >= board[0].size() ||
            board[row][col] != word[index]) {
            return false;
        }
        
        // 标记当前位置为已访问
        char temp = board[row][col];
        board[row][col] = '#';
        
        // 四个方向搜索
        bool found = dfs(board, word, row + 1, col, index + 1) ||
                     dfs(board, word, row - 1, col, index + 1) ||
                     dfs(board, word, row, col + 1, index + 1) ||
                     dfs(board, word, row, col - 1, index + 1);
        
        // 恢复当前位置
        board[row][col] = temp;
        
        return found;
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testExist() {
    Solution solution;
    
    vector<vector<char>> board = {
        {'A','B','C','E'},
        {'S','F','C','S'},
        {'A','D','E','E'}
    };
    
    string word1 = "ABCCED";
    bool result1 = solution.exist(board, word1);
    cout << "搜索 'ABCCED': " << (result1 ? "True" : "False") << endl;  // 期望: True
    
    string word2 = "SEE";
    bool result2 = solution.exist(board, word2);
    cout << "搜索 'SEE': " << (result2 ? "True" : "False") << endl;  // 期望: True
    
    string word3 = "ABCB";
    bool result3 = solution.exist(board, word3);
    cout << "搜索 'ABCB': " << (result3 ? "True" : "False") << endl;  // 期望: False
}

int main() {
    testExist();
    return 0;
}
