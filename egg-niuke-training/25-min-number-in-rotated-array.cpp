/**
 * NC88 旋转数组的最小数字
 * https://www.nowcoder.com/practice/9f3231a991af4f55b95579b44b7a01ba
 * 
 * 把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。
 * 
 * 时间复杂度：O(logn)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int minNumberInRotateArray(vector<int> nums) {
        if (nums.empty()) return -1;
        
        int left = 0, right = nums.size() - 1;
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] > nums[right]) {
                // 最小值在右半部分
                left = mid + 1;
            } else if (nums[mid] < nums[right]) {
                // 最小值在左半部分（包括mid）
                right = mid;
            } else {
                // nums[mid] == nums[right]，无法确定，right--
                right--;
            }
        }
        
        return nums[left];
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {3, 4, 5, 1, 2},
        {2, 2, 2, 0, 1},
        {1, 0, 1, 1, 1},
        {1, 2, 3, 4, 5}
    };
    
    for (const auto& nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        int result = solution.minNumberInRotateArray(nums);
        cout << "最小值: " << result << "\n" << endl;
    }
    
    return 0;
}

