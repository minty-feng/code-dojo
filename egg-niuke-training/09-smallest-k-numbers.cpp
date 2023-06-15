/**
 * NC119 最小的K个数
 * https://www.nowcoder.com/practice/6a296eb82cf844ca8539b57c23e6e9bf
 * 
 * 给定一个长度为 n 的可能有重复值的数组，找出其中不去重的最小的 k 个数。
 * 
 * 时间复杂度：O(nlogk)
 * 空间复杂度：O(k)
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * 方法1：大顶堆
     */
    vector<int> GetLeastNumbers_Heap(vector<int> arr, int k) {
        if (k == 0 || arr.empty()) {
            return {};
        }
        
        // 维护大小为k的大顶堆
        priority_queue<int> heap;
        
        for (int num : arr) {
            if (heap.size() < k) {
                heap.push(num);
            } else if (heap.top() > num) {
                heap.pop();
                heap.push(num);
            }
        }
        
        // 提取结果
        vector<int> result;
        while (!heap.empty()) {
            result.push_back(heap.top());
            heap.pop();
        }
        
        sort(result.begin(), result.end());
        return result;
    }
    
    /**
     * 方法2：快速选择
     */
    vector<int> GetLeastNumbers_QuickSelect(vector<int> arr, int k) {
        if (k == 0 || arr.empty()) {
            return {};
        }
        
        quickselect(arr, 0, arr.size() - 1, k);
        
        vector<int> result(arr.begin(), arr.begin() + k);
        sort(result.begin(), result.end());
        return result;
    }

private:
    int partition(vector<int>& arr, int left, int right) {
        int pivot = arr[right];
        int i = left;
        
        for (int j = left; j < right; j++) {
            if (arr[j] <= pivot) {
                swap(arr[i], arr[j]);
                i++;
            }
        }
        swap(arr[i], arr[right]);
        return i;
    }
    
    void quickselect(vector<int>& arr, int left, int right, int k) {
        if (left >= right) return;
        
        int pos = partition(arr, left, right);
        
        if (pos == k) {
            return;
        } else if (pos < k) {
            quickselect(arr, pos + 1, right, k);
        } else {
            quickselect(arr, left, pos - 1, k);
        }
    }
};

int main() {
    Solution solution;
    
    vector<int> arr = {4, 5, 1, 6, 2, 7, 3, 8};
    int k = 4;
    
    cout << "数组: ";
    for (int num : arr) cout << num << " ";
    cout << endl;
    
    vector<int> result = solution.GetLeastNumbers_Heap(arr, k);
    
    cout << "最小的" << k << "个数: ";
    for (int num : result) cout << num << " ";
    cout << endl;
    
    return 0;
}

