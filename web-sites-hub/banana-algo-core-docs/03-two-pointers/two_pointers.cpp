/**
 * 双指针技巧实现
 */

#include <iostream>
#include <vector>
#include <unordered_set>
#include <algorithm>

using namespace std;

// 两数之和（有序数组）
vector<int> twoSum(const vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    
    while (left < right) {
        int sum = nums[left] + nums[right];
        if (sum == target) {
            return {left, right};
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    
    return {};
}

// 三数之和
vector<vector<int>> threeSum(vector<int>& nums) {
    vector<vector<int>> result;
    sort(nums.begin(), nums.end());
    
    for (int i = 0; i < (int)nums.size() - 2; i++) {
        if (i > 0 && nums[i] == nums[i-1]) continue;
        
        int left = i + 1, right = nums.size() - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.push_back({nums[i], nums[left], nums[right]});
                while (left < right && nums[left] == nums[left+1]) left++;
                while (left < right && nums[right] == nums[right-1]) right--;
                left++;
                right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    
    return result;
}

// 盛最多水的容器
int maxArea(const vector<int>& height) {
    int left = 0, right = height.size() - 1;
    int maxWater = 0;
    
    while (left < right) {
        int width = right - left;
        int h = min(height[left], height[right]);
        maxWater = max(maxWater, width * h);
        
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    
    return maxWater;
}

// 最长无重复字符子串
int lengthOfLongestSubstring(const string& s) {
    unordered_set<char> charSet;
    int left = 0;
    int maxLen = 0;
    
    for (int right = 0; right < s.length(); right++) {
        while (charSet.count(s[right])) {
            charSet.erase(s[left]);
            left++;
        }
        charSet.insert(s[right]);
        maxLen = max(maxLen, right - left + 1);
    }
    
    return maxLen;
}

int main() {
    cout << "=== 双指针技巧演示 ===" << endl << endl;
    
    // 两数之和
    vector<int> nums = {2, 7, 11, 15};
    int target = 9;
    cout << "两数之和 [2,7,11,15], target=9:" << endl;
    vector<int> indices = twoSum(nums, target);
    cout << "  结果: [" << indices[0] << ", " << indices[1] << "]" << endl << endl;
    
    // 三数之和
    vector<int> nums2 = {-1, 0, 1, 2, -1, -4};
    cout << "三数之和 [-1,0,1,2,-1,-4]:" << endl;
    vector<vector<int>> triplets = threeSum(nums2);
    cout << "  结果: [";
    for (size_t i = 0; i < triplets.size(); i++) {
        cout << "[" << triplets[i][0] << "," << triplets[i][1] << "," << triplets[i][2] << "]";
        if (i < triplets.size() - 1) cout << ", ";
    }
    cout << "]" << endl << endl;
    
    // 盛水
    vector<int> height = {1, 8, 6, 2, 5, 4, 8, 3, 7};
    cout << "盛最多水 [1,8,6,2,5,4,8,3,7]:" << endl;
    cout << "  最大面积: " << maxArea(height) << endl << endl;
    
    // 最长无重复子串
    string s = "abcabcbb";
    cout << "最长无重复子串 '" << s << "':" << endl;
    cout << "  长度: " << lengthOfLongestSubstring(s) << endl;
    
    return 0;
}

