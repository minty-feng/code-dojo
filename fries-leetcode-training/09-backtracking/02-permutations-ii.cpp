/**
 * LeetCode 47. 全排列II
 * https://leetcode.cn/problems/permutations-ii/
 * 
 * 给定一个可包含重复数字的序列nums，按任意顺序返回所有不重复的全排列。
 * 
 * 回溯 + 去重
 * 
 * 时间复杂度：O(n! * n)
 * 空间复杂度：O(n)
 */

class Solution {
public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> path;
        vector<bool> used(nums.size(), false);
        
        sort(nums.begin(), nums.end());  // 排序以便去重
        
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
            if (used[i]) {
                continue;
            }
            
            // 去重：如果当前数字与前一个数字相同，且前一个数字未被使用，则跳过
            if (i > 0 && nums[i] == nums[i-1] && !used[i-1]) {
                continue;
            }
            
            path.push_back(nums[i]);
            used[i] = true;
            backtrack(nums, path, used, result);
            path.pop_back();
            used[i] = false;
        }
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testPermuteUnique() {
    Solution solution;
    
    vector<int> nums = {1, 1, 2};
    vector<vector<int>> result = solution.permuteUnique(nums);
    
    cout << "全排列结果: [";
    for (int i = 0; i < result.size(); i++) {
        cout << "[";
        for (int j = 0; j < result[i].size(); j++) {
            cout << result[i][j];
            if (j < result[i].size() - 1) cout << ",";
        }
        cout << "]";
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;  // 期望: [[1,1,2],[1,2,1],[2,1,1]]
}

int main() {
    testPermuteUnique();
    return 0;
}
