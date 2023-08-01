/**
 * LeetCode 41. 缺失的第一个正数
 * https://leetcode.cn/problems/first-missing-positive/
 * 
 * 给你一个未排序的整数数组nums，请你找出其中没有出现的最小的正整数。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        
        // 将数组中的数映射到1-n的位置
        for (int i = 0; i < n; i++) {
            while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                swap(nums[nums[i] - 1], nums[i]);
            }
        }
        
        // 找到第一个位置不正确的数
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) {
                return i + 1;
            }
        }
        
        return n + 1;
    }
};

int main() {
    Solution solution;
    vector<vector<int>> testCases = {{1, 2, 0}, {3, 4, -1, 1}, {7, 8, 9, 11, 12}};
    
    for (auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        int result = solution.firstMissingPositive(nums);
        cout << "缺失的第一个正数: " << result << "\n" << endl;
    }
    
    return 0;
}

