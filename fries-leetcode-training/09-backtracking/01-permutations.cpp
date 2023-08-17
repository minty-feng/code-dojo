/**
 * LeetCode 46. 全排列
 * https://leetcode.cn/problems/permutations/
 * 
 * 给定一个不含重复数字的数组nums，返回其所有可能的全排列。
 * 
 * 回溯
 * 
 * 时间复杂度：O(n! * n)
 * 空间复杂度：O(n)
 */

class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> path;
        vector<bool> used(nums.size(), false);
        
        backtrack(nums, path, used, result);
        return result;
    }
    
private:
    void backtrack(vector<int>& nums, vector<int>& path, vector<bool>& used, vector<vector<int>>& result) {
        if (path.size() == nums.size()) {
            result.push_back(path);
            return;
        }
        
        for (int i = 0; i < nums.size(); i++) {
            if (!used[i]) {
                path.push_back(nums[i]);
                used[i] = true;
                backtrack(nums, path, used, result);
                path.pop_back();
                used[i] = false;
            }
        }
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testPermute() {
    Solution solution;
    
    vector<int> nums1 = {1, 2, 3};
    vector<vector<int>> result1 = solution.permute(nums1);
    
    cout << "全排列结果: [";
    for (int i = 0; i < result1.size(); i++) {
        cout << "[";
        for (int j = 0; j < result1[i].size(); j++) {
            cout << result1[i][j];
            if (j < result1[i].size() - 1) cout << ",";
        }
        cout << "]";
        if (i < result1.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

int main() {
    testPermute();
    return 0;
}
