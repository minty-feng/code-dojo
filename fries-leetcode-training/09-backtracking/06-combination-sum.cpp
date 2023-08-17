/**
 * LeetCode 39. 组合总和
 * https://leetcode.cn/problems/combination-sum/
 * 
 * 给你一个无重复元素的整数数组candidates和一个目标整数target，
 * 找出candidates中可以使数字和为target的所有不同组合。
 * 
 * 回溯
 * 
 * 时间复杂度：O(2^t) t为target值
 * 空间复杂度：O(target)
 */

class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<vector<int>> result;
        vector<int> path;
        
        sort(candidates.begin(), candidates.end());  // 排序以便剪枝
        
        backtrack(candidates, target, 0, path, result);
        return result;
    }
    
private:
    void backtrack(vector<int>& candidates, int target, int start, vector<int>& path, vector<vector<int>>& result) {
        if (target == 0) {
            result.push_back(path);
            return;
        }
        
        for (int i = start; i < candidates.size(); i++) {
            if (candidates[i] > target) {
                break;  // 剪枝：当前数字已经大于剩余值
            }
            
            path.push_back(candidates[i]);
            backtrack(candidates, target - candidates[i], i, path, result);  // 可以重复使用
            path.pop_back();  // 回溯
        }
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void testCombinationSum() {
    Solution solution;
    
    vector<int> candidates = {2, 3, 6, 7};
    int target = 7;
    vector<vector<int>> result = solution.combinationSum(candidates, target);
    
    cout << "组合总和结果: [";
    for (int i = 0; i < result.size(); i++) {
        cout << "[";
        for (int j = 0; j < result[i].size(); j++) {
            cout << result[i][j];
            if (j < result[i].size() - 1) cout << ",";
        }
        cout << "]";
        if (i < result.size() - 1) cout << ",";
    }
    cout << "]" << endl;  // 期望: [[2,2,3],[7]]
}

int main() {
    testCombinationSum();
    return 0;
}
