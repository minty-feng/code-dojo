/**
 * LeetCode 212. 单词搜索II
 * https://leetcode.cn/problems/word-search-ii/
 * 
 * 给定一个m x n二维字符网格board和一个单词（字符串）列表words，返回所有二维网格上的单词。
 * 
 * Trie + DFS回溯
 * 
 * 时间复杂度：O(m*n*4^L) L为单词最大长度
 * 空间复杂度：O(N) N为所有单词的字符总数
 */

struct TrieNode {
    unordered_map<char, TrieNode*> children;
    string word;
    
    TrieNode() {}
};

class Solution {
private:
    TrieNode* root;
    vector<string> result;
    
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        if (board.empty() || board[0].empty() || words.empty()) {
            return {};
        }
        
        // 构建Trie
        root = new TrieNode();
        for (const string& word : words) {
            TrieNode* node = root;
            for (char c : word) {
                if (node->children.find(c) == node->children.end()) {
                    node->children[c] = new TrieNode();
                }
                node = node->children[c];
            }
            node->word = word;
        }
        
        int rows = board.size();
        int cols = board[0].size();
        
        // 从每个位置开始搜索
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                dfs(board, i, j, root);
            }
        }
        
        return result;
    }
    
private:
    void dfs(vector<vector<char>>& board, int row, int col, TrieNode* node) {
        char c = board[row][col];
        
        // 检查当前字符是否在Trie中
        if (node->children.find(c) == node->children.end()) {
            return;
        }
        
        node = node->children[c];
        
        // 如果找到完整单词
        if (!node->word.empty()) {
            result.push_back(node->word);
            node->word = "";  // 避免重复
        }
        
        // 标记当前位置为已访问
        board[row][col] = '#';
        
        // 四个方向DFS
        vector<pair<int, int>> directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        for (auto& dir : directions) {
            int new_row = row + dir.first;
            int new_col = col + dir.second;
            
            if (new_row >= 0 && new_row < board.size() && 
                new_col >= 0 && new_col < board[0].size() && 
                board[new_row][new_col] != '#') {
                dfs(board, new_row, new_col, node);
            }
        }
        
        // 恢复当前位置
        board[row][col] = c;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

void testFindWords() {
    Solution solution;
    
    vector<vector<char>> board = {
        {'o','a','a','n'},
        {'e','t','a','e'},
        {'i','h','k','r'},
        {'i','f','l','v'}
    };
    vector<string> words = {"oath","pea","eat","rain"};
    
    vector<string> result = solution.findWords(board, words);
    
    cout << "找到的单词: [";
    for (int i = 0; i < result.size(); i++) {
        cout << "\"" << result[i] << "\"";
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;  // 期望: ["eat","oath"]
}

int main() {
    testFindWords();
    return 0;
}
