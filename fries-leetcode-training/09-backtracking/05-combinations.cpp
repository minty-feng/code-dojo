/**
 * LeetCode 77. 组合
 * https://leetcode.cn/problems/combinations/
 * 
 * 给定两个整数n和k，返回范围[1, n]中所有可能的k个数的组合。
 * 
 * 回溯
 * 
 * 时间复杂度：O(C(n,k) * k)
 * 空间复杂度：O(k)
 */

class Solution {
public:
    vector<vector<int>> combine(int n, int k) {
        vector<vector<int>> result;
        vector<int> path;
        
        backtrack(n, k, 1, path, result);
        return result;
    }
    
private:
    void backtrack(int n, int k, int start, vector<int>& path, vector<vector<int>>& result) {
        if (path.size() == k) {
            result.push_back(path);
            return;
        }
        
        // 剪枝：剩余数字不够组成k个数的组合
        for (int i = start; i <= n; i++) {
            if (path.size() + (n - i + 1) < k) {
                break;
            }
            
            path.push_back(i);
            backtrack(n, k, i + 1, path, result);
            path.pop_back();  // 回溯
        }
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testCombine() {
    Solution solution;
    
    vector<vector<int>> result = solution.combine(4, 2);
    
    cout << "组合结果: [";
    for (int i = 0; i < result.size(); i++) {
        cout << "[";
        for (int j = 0; j < result[i].size(); j++) {
            cout << result[i][j];
            if (j < result[i].size() - 1) cout << ",";
        }
        cout << "]";
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;  // 期望: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
}

int main() {
    testCombine();
    return 0;
}
