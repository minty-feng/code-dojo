/**
 * 动态数组实现
 * 支持自动扩容和缩容
 */

#include <iostream>
#include <stdexcept>

template<typename T>
class DynamicArray {
private:
    T* data;
    int size;
    int capacity;
    
    void resize(int newCapacity) {
        T* newData = new T[newCapacity];
        for (int i = 0; i < size; i++) {
            newData[i] = data[i];
        }
        delete[] data;
        data = newData;
        capacity = newCapacity;
    }

public:
    // 构造函数
    DynamicArray(int initialCapacity = 4) 
        : size(0), capacity(initialCapacity) {
        data = new T[capacity];
    }
    
    // 析构函数
    ~DynamicArray() {
        delete[] data;
    }
    
    // 拷贝构造函数
    DynamicArray(const DynamicArray& other) 
        : size(other.size), capacity(other.capacity) {
        data = new T[capacity];
        for (int i = 0; i < size; i++) {
            data[i] = other.data[i];
        }
    }
    
    // 赋值运算符
    DynamicArray& operator=(const DynamicArray& other) {
        if (this != &other) {
            delete[] data;
            size = other.size;
            capacity = other.capacity;
            data = new T[capacity];
            for (int i = 0; i < size; i++) {
                data[i] = other.data[i];
            }
        }
        return *this;
    }
    
    // 获取大小
    int getSize() const {
        return size;
    }
    
    // 获取容量
    int getCapacity() const {
        return capacity;
    }
    
    // 是否为空
    bool isEmpty() const {
        return size == 0;
    }
    
    // 访问元素
    T& operator[](int index) {
        if (index < 0 || index >= size) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }
    
    const T& operator[](int index) const {
        if (index < 0 || index >= size) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }
    
    // 尾部添加
    void append(const T& val) {
        if (size == capacity) {
            resize(2 * capacity);
        }
        data[size++] = val;
    }
    
    // 指定位置插入
    void insert(int index, const T& val) {
        if (index < 0 || index > size) {
            throw std::out_of_range("Index out of range");
        }
        
        if (size == capacity) {
            resize(2 * capacity);
        }
        
        for (int i = size; i > index; i--) {
            data[i] = data[i - 1];
        }
        data[index] = val;
        size++;
    }
    
    // 删除元素
    void remove(const T& val) {
        for (int i = 0; i < size; i++) {
            if (data[i] == val) {
                pop(i);
                return;
            }
        }
        throw std::runtime_error("Value not found");
    }
    
    // 删除指定位置
    T pop(int index = -1) {
        if (isEmpty()) {
            throw std::runtime_error("Pop from empty array");
        }
        
        if (index == -1) {
            index = size - 1;
        }
        
        if (index < 0 || index >= size) {
            throw std::out_of_range("Index out of range");
        }
        
        T val = data[index];
        
        for (int i = index; i < size - 1; i++) {
            data[i] = data[i + 1];
        }
        size--;
        
        // 缩容
        if (size > 0 && size == capacity / 4) {
            resize(capacity / 2);
        }
        
        return val;
    }
    
    // 查找索引
    int find(const T& val) const {
        for (int i = 0; i < size; i++) {
            if (data[i] == val) {
                return i;
            }
        }
        return -1;
    }
    
    // 清空
    void clear() {
        size = 0;
        capacity = 4;
        delete[] data;
        data = new T[capacity];
    }
    
    // 打印
    void print() const {
        std::cout << "[";
        for (int i = 0; i < size; i++) {
            std::cout << data[i];
            if (i < size - 1) std::cout << ", ";
        }
        std::cout << "]" << std::endl;
    }
};


// 演示
int main() {
    std::cout << "=== 动态数组演示 ===" << std::endl << std::endl;
    
    DynamicArray<int> arr;
    std::cout << "创建空数组" << std::endl;
    std::cout << "容量: " << arr.getCapacity() 
              << ", 大小: " << arr.getSize() << std::endl << std::endl;
    
    // 添加元素
    std::cout << "添加元素: 1, 2, 3, 4, 5" << std::endl;
    for (int i = 1; i <= 5; i++) {
        arr.append(i);
    }
    std::cout << "数组: ";
    arr.print();
    std::cout << "容量: " << arr.getCapacity() 
              << ", 大小: " << arr.getSize() << std::endl << std::endl;
    
    // 继续添加触发扩容
    std::cout << "继续添加: 6, 7, 8" << std::endl;
    for (int i = 6; i <= 8; i++) {
        arr.append(i);
    }
    std::cout << "数组: ";
    arr.print();
    std::cout << "容量: " << arr.getCapacity() 
              << ", 大小: " << arr.getSize() << std::endl << std::endl;
    
    // 访问和修改
    std::cout << "访问索引2: " << arr[2] << std::endl;
    arr[2] = 99;
    std::cout << "修改索引2为99" << std::endl;
    std::cout << "数组: ";
    arr.print();
    std::cout << std::endl;
    
    // 插入
    std::cout << "在索引0插入100" << std::endl;
    arr.insert(0, 100);
    std::cout << "数组: ";
    arr.print();
    std::cout << std::endl;
    
    // 删除
    std::cout << "删除末尾元素: " << arr.pop() << std::endl;
    std::cout << "数组: ";
    arr.print();
    std::cout << std::endl;
    
    // 查找
    int index = arr.find(99);
    std::cout << "查找元素99的索引: " << index << std::endl << std::endl;
    
    // 删除多个元素
    std::cout << "删除多个元素..." << std::endl;
    for (int i = 0; i < 5; i++) {
        arr.pop();
    }
    std::cout << "数组: ";
    arr.print();
    std::cout << "容量: " << arr.getCapacity() 
              << ", 大小: " << arr.getSize() << std::endl;
    
    return 0;
}

