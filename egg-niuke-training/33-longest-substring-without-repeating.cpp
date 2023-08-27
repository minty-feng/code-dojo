/**
 * NC41 最长无重复子数组
 * https://www.nowcoder.com/practice/b56799ebfd684fb394bd315e89324fb4
 * 
 * 给定一个数组arr，返回arr的最长无重复元素子数组的长度。
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxLength(vector<int>& arr) {
        if (arr.empty()) return 0;
        
        unordered_map<int, int> charMap;
        int left = 0;
        int maxLen = 0;
        
        for (int right = 0; right < arr.size(); right++) {
            if (charMap.count(arr[right]) && charMap[arr[right]] >= left) {
                // 更新左边界
                left = charMap[arr[right]] + 1;
            }
            
            charMap[arr[right]] = right;
            maxLen = max(maxLen, right - left + 1);
        }
        
        return maxLen;
    }
};

int main() {
    Solution solution;
    
    vector<vector<int>> testCases = {
        {2, 3, 4, 5},
        {2, 2, 3, 4, 3},
        {1, 2, 3, 1, 2, 3, 2, 2},
        {1, 1, 1, 1}
    };
    
    for (auto& arr : testCases) {
        cout << "数组: ";
        for (int num : arr) cout << num << " ";
        cout << endl;
        
        int result = solution.maxLength(arr);
        cout << "最长无重复子数组长度: " << result << "\n" << endl;
    }
    
    return 0;
}

