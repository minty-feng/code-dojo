/**
 * LeetCode 15. 三数之和
 * https://leetcode.cn/problems/3sum/
 * 
 * 给你一个包含n个整数的数组nums，判断nums中是否存在三个元素a，b，c，使得a+b+c=0？
 * 
 * 时间复杂度：O(n^2)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> result;
        int n = nums.size();
        
        for (int i = 0; i < n - 2; i++) {
            // 跳过重复元素
            if (i > 0 && nums[i] == nums[i-1]) continue;
            
            int left = i + 1, right = n - 1;
            
            while (left < right) {
                int currentSum = nums[i] + nums[left] + nums[right];
                
                if (currentSum == 0) {
                    result.push_back({nums[i], nums[left], nums[right]});
                    
                    // 跳过重复元素
                    while (left < right && nums[left] == nums[left+1]) left++;
                    while (left < right && nums[right] == nums[right-1]) right--;
                    
                    left++;
                    right--;
                } else if (currentSum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        
        return result;
    }
};

int main() {
    Solution solution;
    vector<vector<int>> testCases = {{-1, 0, 1, 2, -1, -4}, {0, 1, 1}, {0, 0, 0}};
    
    for (auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        vector<vector<int>> result = solution.threeSum(nums);
        cout << "三数之和为0的组合:" << endl;
        for (const auto& triplet : result) {
            cout << "  [";
            for (size_t i = 0; i < triplet.size(); i++) {
                cout << triplet[i];
                if (i < triplet.size() - 1) cout << ", ";
            }
            cout << "]" << endl;
        }
        cout << endl;
    }
    
    return 0;
}

