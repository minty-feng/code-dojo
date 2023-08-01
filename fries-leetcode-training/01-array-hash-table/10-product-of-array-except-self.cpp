/**
 * LeetCode 238. 除自身以外数组的乘积
 * https://leetcode.cn/problems/product-of-array-except-self/
 * 
 * 给你一个整数数组nums，返回数组answer，其中answer[i]等于nums中除nums[i]之外其余各元素的乘积。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, 1);
        
        // 计算左乘积
        for (int i = 1; i < n; i++) {
            result[i] = result[i-1] * nums[i-1];
        }
        
        // 计算右乘积并更新结果
        int rightProduct = 1;
        for (int i = n-1; i >= 0; i--) {
            result[i] *= rightProduct;
            rightProduct *= nums[i];
        }
        
        return result;
    }
};

int main() {
    Solution solution;
    vector<vector<int>> testCases = {{1, 2, 3, 4}, {-1, 1, 0, -3, 3}, {2, 3, 4, 5}};
    
    for (auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        vector<int> result = solution.productExceptSelf(nums);
        cout << "除自身以外乘积: ";
        for (int val : result) cout << val << " ";
        cout << "\n" << endl;
    }
    
    return 0;
}

