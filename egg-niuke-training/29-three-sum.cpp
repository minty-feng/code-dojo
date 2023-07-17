/**
 * NC54 三数之和
 * https://www.nowcoder.com/practice/345e2ed5f81d4017bbb8cc6055b0b711
 * 
 * 给出一个有n个元素的数组S，找出所有满足a+b+c=0的三元组。
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
        vector<vector<int>> result;
        if (nums.size() < 3) return result;
        
        sort(nums.begin(), nums.end());
        
        for (int i = 0; i < nums.size() - 2; i++) {
            // 去重
            if (i > 0 && nums[i] == nums[i-1]) continue;
            
            // 优化
            if (nums[i] > 0) break;
            
            int left = i + 1, right = nums.size() - 1;
            
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                
                if (sum == 0) {
                    result.push_back({nums[i], nums[left], nums[right]});
                    
                    // 去重
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    
                    left++;
                    right--;
                } else if (sum < 0) {
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
    
    vector<vector<int>> testCases = {
        {-1, 0, 1, 2, -1, -4},
        {0, 0, 0, 0},
        {-2, 0, 1, 1, 2}
    };
    
    for (auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        vector<vector<int>> result = solution.threeSum(nums);
        cout << "三数之和为0:" << endl;
        for (const auto& triplet : result) {
            cout << "  [" << triplet[0] << ", " << triplet[1] << ", " << triplet[2] << "]" << endl;
        }
        cout << endl;
    }
    
    return 0;
}

