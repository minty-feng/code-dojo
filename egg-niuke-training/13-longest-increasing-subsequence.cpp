/**
 * NC91 最长递增子序列
 * https://www.nowcoder.com/practice/9cf027bf54714ad889d4f30ff0ae5481
 * 
 * 给定一个长度为n的数组，找出其中最长严格递增子序列的长度。
 * 
 * 时间复杂度：O(nlogn)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * 方法1：动态规划 O(n^2)
     */
    int lengthOfLIS_DP(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        int n = nums.size();
        vector<int> dp(n, 1);
        
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[i] > nums[j]) {
                    dp[i] = max(dp[i], dp[j] + 1);
                }
            }
        }
        
        return *max_element(dp.begin(), dp.end());
    }
    
    /**
     * 方法2：动态规划+二分查找 O(nlogn)
     */
    int lengthOfLIS_Binary(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        vector<int> tails;
        
        for (int num : nums) {
            auto it = lower_bound(tails.begin(), tails.end(), num);
            
            if (it == tails.end()) {
                tails.push_back(num);
            } else {
                *it = num;
            }
        }
        
        return tails.size();
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {10, 9, 2, 5, 3, 7, 101, 18},
        {0, 1, 0, 3, 2, 3},
        {7, 7, 7, 7, 7}
    };
    
    for (auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        cout << "DP法: " << solution.lengthOfLIS_DP(nums) << endl;
        cout << "二分法: " << solution.lengthOfLIS_Binary(nums) << endl << endl;
    }
    
    return 0;
}

