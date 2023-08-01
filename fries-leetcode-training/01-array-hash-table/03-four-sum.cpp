/**
 * LeetCode 18. 四数之和
 * https://leetcode.cn/problems/4sum/
 * 
 * 给你一个由n个整数组成的数组nums，和一个目标值target。
 * 请你找出并返回满足下述全部条件且不重复的四元组[nums[a], nums[b], nums[c], nums[d]]：
 * - 0 <= a, b, c, d < n
 * - a、b、c和d互不相同
 * - nums[a] + nums[b] + nums[c] + nums[d] == target
 * 
 * 双指针 + 排序
 * 
 * 时间复杂度：O(n³)
 * 空间复杂度：O(1)
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        vector<vector<int>> result;
        int n = nums.size();
        
        if (n < 4) {
            return result;
        }
        
        // 排序
        sort(nums.begin(), nums.end());
        
        for (int i = 0; i < n - 3; i++) {
            // 跳过重复元素
            if (i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }
            
            for (int j = i + 1; j < n - 2; j++) {
                // 跳过重复元素
                if (j > i + 1 && nums[j] == nums[j - 1]) {
                    continue;
                }
                
                int left = j + 1;
                int right = n - 1;
                
                while (left < right) {
                    long long sum = (long long)nums[i] + nums[j] + nums[left] + nums[right];
                    
                    if (sum == target) {
                        result.push_back({nums[i], nums[j], nums[left], nums[right]});
                        
                        // 跳过重复元素
                        while (left < right && nums[left] == nums[left + 1]) {
                            left++;
                        }
                        while (left < right && nums[right] == nums[right - 1]) {
                            right--;
                        }
                        
                        left++;
                        right--;
                    } else if (sum < target) {
                        left++;
                    } else {
                        right--;
                    }
                }
            }
        }
        
        return result;
    }
};

// 测试函数
#include <iostream>
void testFourSum() {
    Solution solution;
    
    // 测试用例1
    vector<int> nums1 = {1, 0, -1, 0, -2, 2};
    int target1 = 0;
    auto result1 = solution.fourSum(nums1, target1);
    cout << "测试1: ";
    for (const auto& quad : result1) {
        cout << "[";
        for (int i = 0; i < quad.size(); i++) {
            cout << quad[i];
            if (i < quad.size() - 1) cout << ",";
        }
        cout << "] ";
    }
    cout << endl;
    
    // 测试用例2
    vector<int> nums2 = {2, 2, 2, 2, 2};
    int target2 = 8;
    auto result2 = solution.fourSum(nums2, target2);
    cout << "测试2: ";
    for (const auto& quad : result2) {
        cout << "[";
        for (int i = 0; i < quad.size(); i++) {
            cout << quad[i];
            if (i < quad.size() - 1) cout << ",";
        }
        cout << "] ";
    }
    cout << endl;
}

int main() {
    testFourSum();
    return 0;
}
