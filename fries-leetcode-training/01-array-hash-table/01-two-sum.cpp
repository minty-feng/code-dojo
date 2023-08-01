/**
 * LeetCode 1. 两数之和
 * https://leetcode.cn/problems/two-sum/
 * 
 * 给定一个整数数组nums和一个整数目标值target，请你在该数组中找出和为目标值target的那两个整数。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> hashMap;
        
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            
            if (hashMap.count(complement)) {
                return {hashMap[complement], i};
            }
            
            hashMap[nums[i]] = i;
        }
        
        return {};
    }
};

int main() {
    Solution solution;
    
    vector<pair<vector<int>, int>> testCases = {
        {{2, 7, 11, 15}, 9},
        {{3, 2, 4}, 6},
        {{3, 3}, 6}
    };
    
    for (const auto& [nums, target] : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << ", 目标: " << target << endl;
        
        vector<int> result = solution.twoSum(const_cast<vector<int>&>(nums), target);
        
        cout << "结果: [";
        for (size_t i = 0; i < result.size(); i++) {
            cout << result[i];
            if (i < result.size() - 1) cout << ", ";
        }
        cout << "]" << endl;
        
        if (result.size() == 2) {
            cout << "验证: " << nums[result[0]] << " + " << nums[result[1]] 
                 << " = " << nums[result[0]] + nums[result[1]] << endl;
        }
        cout << endl;
    }
    
    return 0;
}

