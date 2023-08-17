/**
 * LeetCode 90. 子集II
 * https://leetcode.cn/problems/subsets-ii/
 * 
 * 给你一个整数数组nums，其中可能包含重复元素，请你返回该数组所有可能的子集。
 * 
 * 回溯 + 去重
 * 
 * 时间复杂度：O(2^n * n)
 * 空间复杂度：O(n)
 */

class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> path;
        
        sort(nums.begin(), nums.end());  // 排序以便去重
        
        backtrack(nums, 0, path, result);
        return result;
    }
    
private:
    void backtrack(vector<int>& nums, int start, vector<int>& path, vector<vector<int>>& result) {
        result.push_back(path);  // 添加当前路径到结果
        
        for (int i = start; i < nums.size(); i++) {
            // 去重：如果当前数字与前一个数字相同，且不是第一次选择，则跳过
            if (i > start && nums[i] == nums[i-1]) {
                continue;
            }
            
            path.push_back(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.pop_back();  // 回溯
        }
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testSubsetsWithDup() {
    Solution solution;
    
    vector<int> nums = {1, 2, 2};
    vector<vector<int>> result = solution.subsetsWithDup(nums);
    
    cout << "子集结果: [";
    for (int i = 0; i < result.size(); i++) {
        cout << "[";
        for (int j = 0; j < result[i].size(); j++) {
            cout << result[i][j];
            if (j < result[i].size() - 1) cout << ",";
        }
        cout << "]";
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;  // 期望: [[],[1],[1,2],[1,2,2],[2],[2,2]]
}

int main() {
    testSubsetsWithDup();
    return 0;
}
