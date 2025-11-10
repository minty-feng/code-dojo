/**
 * 二分查找及变种实现
 */

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 基本二分查找
int binarySearch(const vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}

// 左边界查找
int leftBound(const vector<int>& arr, int target) {
    int left = 0, right = arr.size();
    
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    return left;
}

// 右边界查找
int rightBound(const vector<int>& arr, int target) {
    int left = 0, right = arr.size();
    
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] <= target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    return left - 1;
}

// 平方根
int mySqrt(int x) {
    if (x < 2) return x;
    
    int left = 1, right = x / 2;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        long long square = (long long)mid * mid;
        
        if (square == x) {
            return mid;
        } else if (square < x) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return right;
}

// 旋转数组查找
int searchRotated(const vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (nums[mid] == target) {
            return mid;
        }
        
        if (nums[left] <= nums[mid]) {
            if (nums[left] <= target && target < nums[mid]) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            if (nums[mid] < target && target <= nums[right]) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }
    
    return -1;
}

int main() {
    cout << "=== 二分查找演示 ===" << endl << endl;
    
    vector<int> arr = {1, 2, 2, 2, 3, 4, 5, 5, 6};
    int target = 2;
    
    cout << "数组: [";
    for (size_t i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << ", ";
    }
    cout << "]" << endl;
    cout << "目标: " << target << endl << endl;
    
    cout << "基本查找: " << binarySearch(arr, target) << endl;
    cout << "左边界: " << leftBound(arr, target) << endl;
    cout << "右边界: " << rightBound(arr, target) << endl << endl;
    
    int x = 8;
    cout << "sqrt(" << x << ") = " << mySqrt(x) << endl << endl;
    
    vector<int> rotated = {4, 5, 6, 7, 0, 1, 2};
    int search_target = 0;
    cout << "旋转数组: [";
    for (size_t i = 0; i < rotated.size(); i++) {
        cout << rotated[i];
        if (i < rotated.size() - 1) cout << ", ";
    }
    cout << "]" << endl;
    cout << "查找 " << search_target << ": " << searchRotated(rotated, search_target) << endl;
    
    return 0;
}

