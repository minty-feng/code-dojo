/**
 * NC7 二分查找
 * https://www.nowcoder.com/practice/d3df40bd23594118b57554129cadf47b
 * 
 * 请实现无重复数字的升序数组的二分查找。
 * 
 * 时间复杂度：O(logn)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    /**
     * 二分查找 - 迭代
     */
    int search(vector<int>& nums, int target) {
        int left = 0, right = nums.size() - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * 二分查找 - 递归
     */
    int searchRecursive(vector<int>& nums, int target) {
        return binarySearch(nums, target, 0, nums.size() - 1);
    }

private:
    int binarySearch(vector<int>& nums, int target, int left, int right) {
        if (left > right) return -1;
        
        int mid = left + (right - left) / 2;
        
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            return binarySearch(nums, target, mid + 1, right);
        } else {
            return binarySearch(nums, target, left, mid - 1);
        }
    }
};

int main() {
    Solution solution;
    
    vector<int> nums = {1, 3, 5, 7, 9, 11, 13, 15};
    vector<int> targets = {7, 10, 1, 15};
    
    for (int target : targets) {
        int result = solution.search(nums, target);
        cout << "查找 " << target << ": 索引 " << result << endl;
    }
    
    return 0;
}

