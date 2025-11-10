/**
 * 分治算法实现
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

// 归并排序
void merge(vector<int>& arr, int left, int mid, int right) {
    vector<int> L(arr.begin() + left, arr.begin() + mid + 1);
    vector<int> R(arr.begin() + mid + 1, arr.begin() + right + 1);
    
    int i = 0, j = 0, k = left;
    
    while (i < L.size() && j < R.size()) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }
    
    while (i < L.size()) arr[k++] = L[i++];
    while (j < R.size()) arr[k++] = R[j++];
}

void mergeSortHelper(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSortHelper(arr, left, mid);
        mergeSortHelper(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

vector<int> mergeSort(vector<int> arr) {
    mergeSortHelper(arr, 0, arr.size() - 1);
    return arr;
}

// 快速选择（第K大元素）
int partition(vector<int>& nums, int left, int right) {
    int pivot = nums[right];
    int i = left;
    
    for (int j = left; j < right; j++) {
        if (nums[j] >= pivot) {  // 降序，找第k大
            swap(nums[i], nums[j]);
            i++;
        }
    }
    swap(nums[i], nums[right]);
    return i;
}

int quickSelect(vector<int>& nums, int left, int right, int k) {
    if (left == right) return nums[left];
    
    int pivotIndex = partition(nums, left, right);
    
    if (pivotIndex == k) {
        return nums[k];
    } else if (pivotIndex < k) {
        return quickSelect(nums, pivotIndex + 1, right, k);
    } else {
        return quickSelect(nums, left, pivotIndex - 1, k);
    }
}

int findKthLargest(vector<int> nums, int k) {
    return quickSelect(nums, 0, nums.size() - 1, k - 1);
}

// 最大子数组和（分治）
int maxCrossingSum(const vector<int>& nums, int left, int mid, int right) {
    int leftSum = INT_MIN;
    int sum = 0;
    for (int i = mid; i >= left; i--) {
        sum += nums[i];
        leftSum = max(leftSum, sum);
    }
    
    int rightSum = INT_MIN;
    sum = 0;
    for (int i = mid + 1; i <= right; i++) {
        sum += nums[i];
        rightSum = max(rightSum, sum);
    }
    
    return leftSum + rightSum;
}

int maxSubArrayDC(const vector<int>& nums, int left, int right) {
    if (left == right) {
        return nums[left];
    }
    
    int mid = (left + right) / 2;
    
    int leftMax = maxSubArrayDC(nums, left, mid);
    int rightMax = maxSubArrayDC(nums, mid + 1, right);
    int crossMax = maxCrossingSum(nums, left, mid, right);
    
    return max({leftMax, rightMax, crossMax});
}

int maxSubArray(const vector<int>& nums) {
    return maxSubArrayDC(nums, 0, nums.size() - 1);
}

// 计算逆序对
long long mergeAndCount(vector<int>& arr, int left, int mid, int right) {
    vector<int> L(arr.begin() + left, arr.begin() + mid + 1);
    vector<int> R(arr.begin() + mid + 1, arr.begin() + right + 1);
    
    int i = 0, j = 0, k = left;
    long long invCount = 0;
    
    while (i < L.size() && j < R.size()) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
            invCount += L.size() - i;  // 逆序对数
        }
    }
    
    while (i < L.size()) arr[k++] = L[i++];
    while (j < R.size()) arr[k++] = R[j++];
    
    return invCount;
}

long long mergeSortCount(vector<int>& arr, int left, int right) {
    long long invCount = 0;
    
    if (left < right) {
        int mid = left + (right - left) / 2;
        invCount += mergeSortCount(arr, left, mid);
        invCount += mergeSortCount(arr, mid + 1, right);
        invCount += mergeAndCount(arr, left, mid, right);
    }
    
    return invCount;
}

long long countInversions(vector<int> arr) {
    return mergeSortCount(arr, 0, arr.size() - 1);
}

int main() {
    cout << "=== 分治算法演示 ===" << endl << endl;
    
    // 快速选择
    vector<int> nums = {3, 2, 1, 5, 6, 4};
    int k = 2;
    cout << "第" << k << "大元素 [3,2,1,5,6,4]:" << endl;
    cout << "  结果: " << findKthLargest(nums, k) << endl << endl;
    
    // 归并排序
    vector<int> arr = {5, 2, 8, 1, 9, 3};
    cout << "归并排序 [5,2,8,1,9,3]:" << endl;
    vector<int> sorted = mergeSort(arr);
    cout << "  结果: [";
    for (size_t i = 0; i < sorted.size(); i++) {
        cout << sorted[i];
        if (i < sorted.size() - 1) cout << ", ";
    }
    cout << "]" << endl << endl;
    
    // 逆序对
    vector<int> arr2 = {8, 4, 2, 1};
    cout << "逆序对 [8,4,2,1]:" << endl;
    cout << "  数量: " << countInversions(arr2) << endl << endl;
    
    // 最大子数组和
    vector<int> nums2 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    cout << "最大子数组和 [-2,1,-3,4,-1,2,1,-5,4]:" << endl;
    cout << "  结果: " << maxSubArray(nums2) << endl;
    
    return 0;
}

