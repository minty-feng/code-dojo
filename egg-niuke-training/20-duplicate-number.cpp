/**
 * NC60 数组中重复的数字
 * https://www.nowcoder.com/practice/6fe361ede7e54db1b84adc81d09d8524
 * 
 * 在一个长度为n的数组里的所有数字都在0到n-1的范围内。
 * 找出数组中任意一个重复的数字。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * 方法1：哈希表
     */
    int duplicate_Hash(vector<int> nums) {
        unordered_set<int> seen;
        for (int num : nums) {
            if (seen.count(num)) {
                return num;
            }
            seen.insert(num);
        }
        return -1;
    }
    
    /**
     * 方法2：原地哈希（最优）
     */
    int duplicate_InPlace(vector<int> nums) {
        for (int i = 0; i < nums.size(); i++) {
            while (nums[i] != i) {
                // nums[i]应该放在索引nums[i]的位置
                if (nums[i] == nums[nums[i]]) {
                    return nums[i];  // 找到重复
                }
                
                // 交换到正确位置
                swap(nums[i], nums[nums[i]]);
            }
        }
        return -1;
    }
    
    /**
     * 方法3：排序
     */
    int duplicate_Sort(vector<int> nums) {
        sort(nums.begin(), nums.end());
        for (int i = 1; i < nums.size(); i++) {
            if (nums[i] == nums[i-1]) {
                return nums[i];
            }
        }
        return -1;
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {2, 3, 1, 0, 2, 5, 3},
        {0, 1, 2, 3, 4, 5, 1},
        {1, 1, 1, 1, 1}
    };
    
    for (auto nums : testCases) {
        cout << "数组: ";
        for (int num : nums) cout << num << " ";
        cout << endl;
        
        cout << "哈希表: " << solution.duplicate_Hash(nums) << endl;
        cout << "原地哈希: " << solution.duplicate_InPlace(nums) << endl;
        cout << "排序: " << solution.duplicate_Sort(nums) << endl << endl;
    }
    
    return 0;
}

