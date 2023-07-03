/**
 * NC42 全排列
 * https://www.nowcoder.com/practice/4bcf3081067a4d028f95acee3ddcd2b1
 * 
 * 给定一个不含重复数字的数组nums，返回其所有可能的全排列。
 * 
 * 时间复杂度：O(n*n!)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * 全排列 - 回溯法
     */
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> path;
        vector<bool> used(nums.size(), false);
        
        backtrack(nums, path, used, result);
        return result;
    }
    
    /**
     * 全排列 - 交换法
     */
    vector<vector<int>> permuteSwap(vector<int>& nums) {
        vector<vector<int>> result;
        backtrackSwap(nums, 0, result);
        return result;
    }

private:
    void backtrack(vector<int>& nums, vector<int>& path, 
                  vector<bool>& used, vector<vector<int>>& result) {
        // 终止条件
        if (path.size() == nums.size()) {
            result.push_back(path);
            return;
        }
        
        // 选择列表
        for (int i = 0; i < nums.size(); i++) {
            if (used[i]) continue;
            
            // 做选择
            path.push_back(nums[i]);
            used[i] = true;
            
            // 递归
            backtrack(nums, path, used, result);
            
            // 撤销选择
            path.pop_back();
            used[i] = false;
        }
    }
    
    void backtrackSwap(vector<int>& nums, int start, vector<vector<int>>& result) {
        if (start == nums.size()) {
            result.push_back(nums);
            return;
        }
        
        for (int i = start; i < nums.size(); i++) {
            swap(nums[start], nums[i]);
            backtrackSwap(nums, start + 1, result);
            swap(nums[start], nums[i]);
        }
    }
};

int main() {
    Solution solution;
    
    vector<int> nums = {1, 2, 3};
    vector<vector<int>> result = solution.permute(nums);
    
    cout << "数组 [1, 2, 3] 的全排列:" << endl;
    for (const auto& perm : result) {
        cout << "[";
        for (size_t i = 0; i < perm.size(); i++) {
            cout << perm[i];
            if (i < perm.size() - 1) cout << ", ";
        }
        cout << "]" << endl;
    }
    
    cout << "\n共 " << result.size() << " 种排列" << endl;
    
    return 0;
}

