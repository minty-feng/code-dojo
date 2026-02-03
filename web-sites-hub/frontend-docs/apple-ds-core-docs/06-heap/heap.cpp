/**
 * 最大堆实现
 */

#include <iostream>
#include <vector>
#include <stdexcept>

class MaxHeap {
private:
    std::vector<int> heap;
    
    int parent(int i) {
        return (i - 1) / 2;
    }
    
    int leftChild(int i) {
        return 2 * i + 1;
    }
    
    int rightChild(int i) {
        return 2 * i + 2;
    }
    
    void swim(int i) {
        while (i > 0 && heap[i] > heap[parent(i)]) {
            std::swap(heap[i], heap[parent(i)]);
            i = parent(i);
        }
    }
    
    void sink(int i) {
        int maxIndex = i;
        int left = leftChild(i);
        int right = rightChild(i);
        
        if (left < heap.size() && heap[left] > heap[maxIndex]) {
            maxIndex = left;
        }
        if (right < heap.size() && heap[right] > heap[maxIndex]) {
            maxIndex = right;
        }
        
        if (maxIndex != i) {
            std::swap(heap[i], heap[maxIndex]);
            sink(maxIndex);
        }
    }

public:
    void insert(int val) {
        heap.push_back(val);
        swim(heap.size() - 1);
    }
    
    int extractMax() {
        if (heap.empty()) {
            throw std::runtime_error("Extract from empty heap");
        }
        
        if (heap.size() == 1) {
            int val = heap.back();
            heap.pop_back();
            return val;
        }
        
        int maxVal = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        sink(0);
        return maxVal;
    }
    
    int peek() const {
        if (heap.empty()) {
            throw std::runtime_error("Peek from empty heap");
        }
        return heap[0];
    }
    
    int size() const {
        return heap.size();
    }
    
    bool isEmpty() const {
        return heap.empty();
    }
    
    static MaxHeap heapify(const std::vector<int>& arr) {
        MaxHeap h;
        h.heap = arr;
        
        for (int i = (arr.size() - 2) / 2; i >= 0; i--) {
            h.sink(i);
        }
        
        return h;
    }
    
    void print() const {
        std::cout << "[";
        for (size_t i = 0; i < heap.size(); i++) {
            std::cout << heap[i];
            if (i < heap.size() - 1) std::cout << ", ";
        }
        std::cout << "]" << std::endl;
    }
};


// 堆排序
std::vector<int> heapSort(std::vector<int> arr) {
    MaxHeap heap = MaxHeap::heapify(arr);
    std::vector<int> result;
    
    while (!heap.isEmpty()) {
        result.push_back(heap.extractMax());
    }
    
    std::reverse(result.begin(), result.end());
    return result;
}


int main() {
    std::cout << "=== 最大堆演示 ===" << std::endl << std::endl;
    
    MaxHeap heap;
    
    std::vector<int> values = {3, 1, 6, 5, 2, 4};
    std::cout << "插入: ";
    for (int val : values) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
    
    for (int val : values) {
        heap.insert(val);
        std::cout << "插入 " << val << ": ";
        heap.print();
    }
    
    std::cout << "\n堆顶（最大值）: " << heap.peek() << std::endl;
    
    std::cout << "\n依次删除最大值:" << std::endl;
    while (!heap.isEmpty()) {
        std::cout << "删除: " << heap.extractMax() << ", 堆: ";
        heap.print();
    }
    
    std::cout << "\n=== 建堆演示 ===" << std::endl << std::endl;
    std::vector<int> arr = {3, 1, 6, 5, 2, 4};
    std::cout << "原数组: ";
    for (int val : arr) std::cout << val << " ";
    std::cout << std::endl;
    
    MaxHeap heap2 = MaxHeap::heapify(arr);
    std::cout << "建堆后: ";
    heap2.print();
    
    std::cout << "\n=== 堆排序演示 ===" << std::endl << std::endl;
    std::vector<int> sorted = heapSort(arr);
    std::cout << "排序后: ";
    for (int val : sorted) std::cout << val << " ";
    std::cout << std::endl;
    
    return 0;
}

