/**
 * 栈的实现：数组栈和链式栈
 */

#include <iostream>
#include <stdexcept>

// ========== 数组栈 ==========
template<typename T>
class ArrayStack {
private:
    T* data;
    int capacity;
    int top_index;

public:
    ArrayStack(int cap = 10) : capacity(cap), top_index(-1) {
        data = new T[capacity];
    }
    
    ~ArrayStack() {
        delete[] data;
    }
    
    void push(const T& val) {
        if (top_index == capacity - 1) {
            // 扩容
            capacity *= 2;
            T* newData = new T[capacity];
            for (int i = 0; i <= top_index; i++) {
                newData[i] = data[i];
            }
            delete[] data;
            data = newData;
        }
        data[++top_index] = val;
    }
    
    T pop() {
        if (isEmpty()) {
            throw std::runtime_error("Pop from empty stack");
        }
        return data[top_index--];
    }
    
    T peek() const {
        if (isEmpty()) {
            throw std::runtime_error("Peek from empty stack");
        }
        return data[top_index];
    }
    
    bool isEmpty() const {
        return top_index == -1;
    }
    
    int size() const {
        return top_index + 1;
    }
    
    void print() const {
        std::cout << "Stack[";
        for (int i = 0; i <= top_index; i++) {
            std::cout << data[i];
            if (i < top_index) std::cout << ", ";
        }
        std::cout << "]" << std::endl;
    }
};


// ========== 链式栈 ==========
template<typename T>
class LinkedStack {
private:
    struct Node {
        T val;
        Node* next;
        Node(T v) : val(v), next(nullptr) {}
    };
    
    Node* top_node;
    int stack_size;

public:
    LinkedStack() : top_node(nullptr), stack_size(0) {}
    
    ~LinkedStack() {
        while (!isEmpty()) {
            pop();
        }
    }
    
    void push(const T& val) {
        Node* newNode = new Node(val);
        newNode->next = top_node;
        top_node = newNode;
        stack_size++;
    }
    
    T pop() {
        if (isEmpty()) {
            throw std::runtime_error("Pop from empty stack");
        }
        Node* temp = top_node;
        T val = temp->val;
        top_node = top_node->next;
        delete temp;
        stack_size--;
        return val;
    }
    
    T peek() const {
        if (isEmpty()) {
            throw std::runtime_error("Peek from empty stack");
        }
        return top_node->val;
    }
    
    bool isEmpty() const {
        return stack_size == 0;
    }
    
    int size() const {
        return stack_size;
    }
};


int main() {
    std::cout << "=== 数组栈演示 ===" << std::endl << std::endl;
    
    ArrayStack<int> stack;
    
    std::cout << "入栈: 1, 2, 3" << std::endl;
    for (int i = 1; i <= 3; i++) {
        stack.push(i);
        std::cout << "push(" << i << "): ";
        stack.print();
    }
    
    std::cout << "\npeek(): " << stack.peek() << std::endl;
    std::cout << "size(): " << stack.size() << std::endl << std::endl;
    
    std::cout << "出栈:" << std::endl;
    while (!stack.isEmpty()) {
        std::cout << "pop(): " << stack.pop() << std::endl;
    }
    
    std::cout << "\n栈是否为空: " << (stack.isEmpty() ? "是" : "否") << std::endl;
    
    return 0;
}

