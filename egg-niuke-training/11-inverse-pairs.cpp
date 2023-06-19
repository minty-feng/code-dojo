/**
 * NC117 数组中的逆序对
 * https://www.nowcoder.com/practice/96bd6684e04a44eb80e6a68efc0ec6c5
 * 
 * 在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个逆序对。
 * 
 * 时间复杂度：O(nlogn)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    /**
     * 归并排序统计逆序对
     */
    int InversePairs(vector<int> nums) {
        if (nums.empty()) return 0;
        
        vector<int> temp(nums.size());
        return mergeSort(nums, temp, 0, nums.size() - 1);
    }

private:
    const int MOD = 1000000007;
    
    int mergeSort(vector<int>& nums, vector<int>& temp, int left, int right) {
        if (left >= right) {
            return 0;
        }
        
        int mid = left + (right - left) / 2;
        long long count = 0;
        
        count += mergeSort(nums, temp, left, mid);
        count += mergeSort(nums, temp, mid + 1, right);
        count += merge(nums, temp, left, mid, right);
        
        return count % MOD;
    }
    
    int merge(vector<int>& nums, vector<int>& temp, int left, int mid, int right) {
        int i = left, j = mid + 1, k = 0;
        long long count = 0;
        
        while (i <= mid && j <= right) {
            if (nums[i] <= nums[j]) {
                temp[k++] = nums[i++];
            } else {
                temp[k++] = nums[j++];
                count += mid - i + 1;  // 统计逆序对
            }
        }
        
        while (i <= mid) temp[k++] = nums[i++];
        while (j <= right) temp[k++] = nums[j++];
        
        // 复制回原数组
        for (int p = 0; p < k; p++) {
            nums[left + p] = temp[p];
        }
        
        return count % MOD;
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {1, 2, 3, 4, 5, 6, 7, 0},
        {7, 5, 6, 4},
        {1, 2, 3}
    };
    
    for (auto& nums : testCases) {
        int count = solution.InversePairs(nums);
        cout << "逆序对数: " << count << endl;
    }
    
    return 0;
}

