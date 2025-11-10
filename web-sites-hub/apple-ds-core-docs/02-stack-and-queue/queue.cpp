/**
 * 队列的实现：循环队列和链式队列
 */

#include <iostream>
#include <stdexcept>

// ========== 循环队列 ==========
template<typename T>
class CircularQueue {
private:
    T* data;
    int front_index;
    int rear_index;
    int capacity;

public:
    CircularQueue(int cap = 5) : capacity(cap + 1), front_index(0), rear_index(0) {
        data = new T[capacity];
    }
    
    ~CircularQueue() {
        delete[] data;
    }
    
    void enqueue(const T& val) {
        if (isFull()) {
            throw std::runtime_error("Queue is full");
        }
        data[rear_index] = val;
        rear_index = (rear_index + 1) % capacity;
    }
    
    T dequeue() {
        if (isEmpty()) {
            throw std::runtime_error("Dequeue from empty queue");
        }
        T val = data[front_index];
        front_index = (front_index + 1) % capacity;
        return val;
    }
    
    T front() const {
        if (isEmpty()) {
            throw std::runtime_error("Front from empty queue");
        }
        return data[front_index];
    }
    
    bool isEmpty() const {
        return front_index == rear_index;
    }
    
    bool isFull() const {
        return (rear_index + 1) % capacity == front_index;
    }
    
    int size() const {
        return (rear_index - front_index + capacity) % capacity;
    }
    
    void print() const {
        std::cout << "Queue[";
        if (!isEmpty()) {
            int i = front_index;
            while (i != rear_index) {
                std::cout << data[i];
                i = (i + 1) % capacity;
                if (i != rear_index) std::cout << ", ";
            }
        }
        std::cout << "]" << std::endl;
    }
};


// ========== 链式队列 ==========
template<typename T>
class LinkedQueue {
private:
    struct Node {
        T val;
        Node* next;
        Node(T v) : val(v), next(nullptr) {}
    };
    
    Node* head;
    Node* tail;
    int queue_size;

public:
    LinkedQueue() : head(nullptr), tail(nullptr), queue_size(0) {}
    
    ~LinkedQueue() {
        while (!isEmpty()) {
            dequeue();
        }
    }
    
    void enqueue(const T& val) {
        Node* newNode = new Node(val);
        if (tail == nullptr) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
        queue_size++;
    }
    
    T dequeue() {
        if (isEmpty()) {
            throw std::runtime_error("Dequeue from empty queue");
        }
        Node* temp = head;
        T val = temp->val;
        head = head->next;
        if (head == nullptr) {
            tail = nullptr;
        }
        delete temp;
        queue_size--;
        return val;
    }
    
    T front() const {
        if (isEmpty()) {
            throw std::runtime_error("Front from empty queue");
        }
        return head->val;
    }
    
    bool isEmpty() const {
        return queue_size == 0;
    }
    
    int size() const {
        return queue_size;
    }
};


int main() {
    std::cout << "=== 循环队列演示 ===" << std::endl << std::endl;
    
    CircularQueue<int> queue(5);
    
    std::cout << "入队: 1, 2, 3" << std::endl;
    for (int i = 1; i <= 3; i++) {
        queue.enqueue(i);
        std::cout << "enqueue(" << i << "): ";
        queue.print();
    }
    
    std::cout << "\nfront(): " << queue.front() << std::endl;
    std::cout << "size(): " << queue.size() << std::endl;
    
    std::cout << "\ndequeue(): " << queue.dequeue() << std::endl;
    std::cout << "队列: ";
    queue.print();
    
    std::cout << "\n入队: 4, 5" << std::endl;
    queue.enqueue(4);
    queue.enqueue(5);
    std::cout << "队列: ";
    queue.print();
    
    return 0;
}

