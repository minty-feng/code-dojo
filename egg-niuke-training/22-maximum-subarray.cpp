/**
 * NC19 最大子数组和
 * https://www.nowcoder.com/practice/459bd355da1549fa8a49e350bf3df484
 * 
 * 输入一个长度为n的整型数组，求所有子数组的和的最大值。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int FindGreatestSumOfSubArray(vector<int> nums) {
        if (nums.empty()) return 0;
        
        int maxSum = nums[0];
        int currentSum = nums[0];
        
        for (int i = 1; i < nums.size(); i++) {
            currentSum = max(currentSum + nums[i], nums[i]);
            maxSum = max(maxSum, currentSum);
        }
        
        return maxSum;
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {1, -2, 3, 10, -4, 7, 2, -5},
        {-2, -1},
        {1, 2, 3, 4, 5}
    };
    
    for (const auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        int result = solution.FindGreatestSumOfSubArray(nums);
        cout << "最大子数组和: " << result << "\n" << endl;
    }
    
    return 0;
}

