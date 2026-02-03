/**
 * 递归与回溯算法实现
 */

#include <iostream>
#include <vector>
#include <string>

using namespace std;

// ========== 全排列 ==========

void permuteHelper(vector<int>& nums, vector<bool>& used, 
                   vector<int>& path, vector<vector<int>>& result) {
    if (path.size() == nums.size()) {
        result.push_back(path);
        return;
    }
    
    for (int i = 0; i < nums.size(); i++) {
        if (used[i]) continue;
        
        used[i] = true;
        path.push_back(nums[i]);
        permuteHelper(nums, used, path, result);
        path.pop_back();
        used[i] = false;
    }
}

vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> path;
    vector<bool> used(nums.size(), false);
    permuteHelper(nums, used, path, result);
    return result;
}

// ========== 组合 ==========

void combineHelper(int n, int k, int start, vector<int>& path, 
                   vector<vector<int>>& result) {
    if (path.size() == k) {
        result.push_back(path);
        return;
    }
    
    for (int i = start; i <= n; i++) {
        path.push_back(i);
        combineHelper(n, k, i + 1, path, result);
        path.pop_back();
    }
}

vector<vector<int>> combine(int n, int k) {
    vector<vector<int>> result;
    vector<int> path;
    combineHelper(n, k, 1, path, result);
    return result;
}

// ========== 子集 ==========

void subsetsHelper(vector<int>& nums, int start, vector<int>& path,
                   vector<vector<int>>& result) {
    result.push_back(path);
    
    for (int i = start; i < nums.size(); i++) {
        path.push_back(nums[i]);
        subsetsHelper(nums, i + 1, path, result);
        path.pop_back();
    }
}

vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> path;
    subsetsHelper(nums, 0, path, result);
    return result;
}

// ========== N皇后 ==========

bool isValid(const vector<string>& board, int row, int col, int n) {
    // 检查列
    for (int i = 0; i < row; i++) {
        if (board[i][col] == 'Q') return false;
    }
    
    // 检查左上对角线
    for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
        if (board[i][j] == 'Q') return false;
    }
    
    // 检查右上对角线
    for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
        if (board[i][j] == 'Q') return false;
    }
    
    return true;
}

void solveNQueensHelper(int n, int row, vector<string>& board,
                        vector<vector<string>>& result) {
    if (row == n) {
        result.push_back(board);
        return;
    }
    
    for (int col = 0; col < n; col++) {
        if (isValid(board, row, col, n)) {
            board[row][col] = 'Q';
            solveNQueensHelper(n, row + 1, board, result);
            board[row][col] = '.';
        }
    }
}

vector<vector<string>> solveNQueens(int n) {
    vector<vector<string>> result;
    vector<string> board(n, string(n, '.'));
    solveNQueensHelper(n, 0, board, result);
    return result;
}

// ========== 括号生成 ==========

void generateParenthesisHelper(int n, int left, int right,
                               string& path, vector<string>& result) {
    if (path.length() == 2 * n) {
        result.push_back(path);
        return;
    }
    
    if (left < n) {
        path.push_back('(');
        generateParenthesisHelper(n, left + 1, right, path, result);
        path.pop_back();
    }
    
    if (right < left) {
        path.push_back(')');
        generateParenthesisHelper(n, left, right + 1, path, result);
        path.pop_back();
    }
}

vector<string> generateParenthesis(int n) {
    vector<string> result;
    string path;
    generateParenthesisHelper(n, 0, 0, path, result);
    return result;
}

// 打印结果
template<typename T>
void printVector(const vector<T>& vec) {
    cout << "[";
    for (size_t i = 0; i < vec.size(); i++) {
        cout << vec[i];
        if (i < vec.size() - 1) cout << ", ";
    }
    cout << "]";
}

int main() {
    cout << "=== 回溯算法演示 ===" << endl << endl;
    
    // 全排列
    vector<int> nums = {1, 2, 3};
    cout << "全排列 [1,2,3]:" << endl;
    vector<vector<int>> perms = permute(nums);
    for (const auto& perm : perms) {
        cout << "  ";
        printVector(perm);
        cout << endl;
    }
    cout << endl;
    
    // 组合
    cout << "C(4,2) 组合:" << endl;
    vector<vector<int>> combs = combine(4, 2);
    for (const auto& comb : combs) {
        cout << "  ";
        printVector(comb);
        cout << endl;
    }
    cout << endl;
    
    // 子集
    vector<int> nums2 = {1, 2, 3};
    cout << "子集 [1,2,3]:" << endl;
    vector<vector<int>> subs = subsets(nums2);
    cout << "  共" << subs.size() << "个子集" << endl << endl;
    
    // N皇后
    cout << "4皇后问题:" << endl;
    vector<vector<string>> queens = solveNQueens(4);
    cout << "  共" << queens.size() << "种解法" << endl << endl;
    
    // 括号生成
    cout << "3对括号:" << endl;
    vector<string> parens = generateParenthesis(3);
    for (const auto& p : parens) {
        cout << "  " << p << endl;
    }
    
    return 0;
}

