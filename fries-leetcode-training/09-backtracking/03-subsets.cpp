/**
 * LeetCode 78. 子集
 * https://leetcode.cn/problems/subsets/
 * 
 * 给你一个整数数组nums，数组中的元素互不相同。返回该数组所有可能的子集。
 * 
 * 回溯
 * 
 * 时间复杂度：O(2^n * n)
 * 空间复杂度：O(n)
 */

class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> path;
        
        backtrack(nums, 0, path, result);
        return result;
    }
    
private:
    void backtrack(vector<int>& nums, int start, vector<int>& path, vector<vector<int>>& result) {
        result.push_back(path);  // 添加当前路径到结果
        
        for (int i = start; i < nums.size(); i++) {
            path.push_back(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.pop_back();  // 回溯
        }
    }
};

// 测试函数
#include <iostream>
#include <vector>
using namespace std;

void testSubsets() {
    Solution solution;
    
    vector<int> nums = {1, 2, 3};
    vector<vector<int>> result = solution.subsets(nums);
    
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
    cout << "]" << endl;  // 期望: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
}

int main() {
    testSubsets();
    return 0;
}
