/**
 * LeetCode 16. 最接近的三数之和
 * https://leetcode.cn/problems/3sum-closest/
 * 
 * 给你一个长度为n的整数数组nums和一个目标值target。请你从nums中选出三个整数，使它们的和与target最接近。
 * 
 * 时间复杂度：O(n^2)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    int threeSumClosest(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int closestSum = INT_MAX;
        
        for (int i = 0; i < n - 2; i++) {
            int left = i + 1, right = n - 1;
            
            while (left < right) {
                int currentSum = nums[i] + nums[left] + nums[right];
                
                // 更新最接近的和
                if (abs(currentSum - target) < abs(closestSum - target)) {
                    closestSum = currentSum;
                }
                
                if (currentSum < target) {
                    left++;
                } else if (currentSum > target) {
                    right--;
                } else {
                    return target;  // 找到完全匹配
                }
            }
        }
        
        return closestSum;
    }
};

int main() {
    Solution solution;
    vector<pair<vector<int>, int>> testCases = {
        {{-1, 2, 1, -4}, 1},
        {{0, 0, 0}, 1},
        {{1, 1, 1, 0}, -100}
    };
    
    for (auto& testCase : testCases) {
        vector<int> nums = testCase.first;
        int target = testCase.second;
        
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << ", 目标: " << target << endl;
        
        int result = solution.threeSumClosest(nums, target);
        cout << "最接近的三数之和: " << result << "\n" << endl;
    }
    
    return 0;
}

