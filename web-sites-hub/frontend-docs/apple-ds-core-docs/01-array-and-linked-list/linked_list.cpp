/**
 * 单链表和双链表实现
 */

#include <iostream>
#include <stdexcept>

// 单链表节点
template<typename T>
struct ListNode {
    T val;
    ListNode* next;
    
    ListNode(T v) : val(v), next(nullptr) {}
};

// 单链表
template<typename T>
class LinkedList {
private:
    ListNode<T>* head;
    int size;

public:
    LinkedList() : head(nullptr), size(0) {}
    
    ~LinkedList() {
        clear();
    }
    
    int getSize() const {
        return size;
    }
    
    bool isEmpty() const {
        return size == 0;
    }
    
    // 头部添加
    void prepend(const T& val) {
        ListNode<T>* newNode = new ListNode<T>(val);
        newNode->next = head;
        head = newNode;
        size++;
    }
    
    // 尾部添加
    void append(const T& val) {
        if (head == nullptr) {
            head = new ListNode<T>(val);
        } else {
            ListNode<T>* curr = head;
            while (curr->next) {
                curr = curr->next;
            }
            curr->next = new ListNode<T>(val);
        }
        size++;
    }
    
    // 插入
    void insert(int index, const T& val) {
        if (index < 0 || index > size) {
            throw std::out_of_range("Index out of range");
        }
        
        if (index == 0) {
            prepend(val);
            return;
        }
        
        ListNode<T>* curr = head;
        for (int i = 0; i < index - 1; i++) {
            curr = curr->next;
        }
        
        ListNode<T>* newNode = new ListNode<T>(val);
        newNode->next = curr->next;
        curr->next = newNode;
        size++;
    }
    
    // 删除
    void remove(const T& val) {
        if (head == nullptr) {
            throw std::runtime_error("Remove from empty list");
        }
        
        // 删除头节点
        if (head->val == val) {
            ListNode<T>* temp = head;
            head = head->next;
            delete temp;
            size--;
            return;
        }
        
        // 删除其他节点
        ListNode<T>* curr = head;
        while (curr->next) {
            if (curr->next->val == val) {
                ListNode<T>* temp = curr->next;
                curr->next = curr->next->next;
                delete temp;
                size--;
                return;
            }
            curr = curr->next;
        }
        
        throw std::runtime_error("Value not found");
    }
    
    // 反转
    void reverse() {
        ListNode<T>* prev = nullptr;
        ListNode<T>* curr = head;
        while (curr) {
            ListNode<T>* next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        head = prev;
    }
    
    // 查找
    int find(const T& val) const {
        ListNode<T>* curr = head;
        int index = 0;
        while (curr) {
            if (curr->val == val) {
                return index;
            }
            curr = curr->next;
            index++;
        }
        return -1;
    }
    
    // 清空
    void clear() {
        while (head) {
            ListNode<T>* temp = head;
            head = head->next;
            delete temp;
        }
        size = 0;
    }
    
    // 打印
    void print() const {
        ListNode<T>* curr = head;
        while (curr) {
            std::cout << curr->val;
            if (curr->next) std::cout << " -> ";
            curr = curr->next;
        }
        std::cout << " -> NULL" << std::endl;
    }
};


// 双链表节点
template<typename T>
struct DListNode {
    T val;
    DListNode* prev;
    DListNode* next;
    
    DListNode(T v) : val(v), prev(nullptr), next(nullptr) {}
};

// 双链表
template<typename T>
class DoublyLinkedList {
private:
    DListNode<T>* head;
    DListNode<T>* tail;
    int size;

public:
    DoublyLinkedList() : head(nullptr), tail(nullptr), size(0) {}
    
    ~DoublyLinkedList() {
        clear();
    }
    
    int getSize() const {
        return size;
    }
    
    bool isEmpty() const {
        return size == 0;
    }
    
    // 头部添加
    void prepend(const T& val) {
        DListNode<T>* newNode = new DListNode<T>(val);
        if (head == nullptr) {
            head = tail = newNode;
        } else {
            newNode->next = head;
            head->prev = newNode;
            head = newNode;
        }
        size++;
    }
    
    // 尾部添加
    void append(const T& val) {
        DListNode<T>* newNode = new DListNode<T>(val);
        if (tail == nullptr) {
            head = tail = newNode;
        } else {
            newNode->prev = tail;
            tail->next = newNode;
            tail = newNode;
        }
        size++;
    }
    
    // 头部删除
    T popFront() {
        if (head == nullptr) {
            throw std::runtime_error("Pop from empty list");
        }
        
        T val = head->val;
        DListNode<T>* temp = head;
        head = head->next;
        if (head) {
            head->prev = nullptr;
        } else {
            tail = nullptr;
        }
        delete temp;
        size--;
        return val;
    }
    
    // 尾部删除
    T popBack() {
        if (tail == nullptr) {
            throw std::runtime_error("Pop from empty list");
        }
        
        T val = tail->val;
        DListNode<T>* temp = tail;
        tail = tail->prev;
        if (tail) {
            tail->next = nullptr;
        } else {
            head = nullptr;
        }
        delete temp;
        size--;
        return val;
    }
    
    // 清空
    void clear() {
        while (head) {
            DListNode<T>* temp = head;
            head = head->next;
            delete temp;
        }
        tail = nullptr;
        size = 0;
    }
    
    // 打印
    void print() const {
        DListNode<T>* curr = head;
        while (curr) {
            std::cout << curr->val;
            if (curr->next) std::cout << " <-> ";
            curr = curr->next;
        }
        std::cout << std::endl;
    }
};


// 演示
int main() {
    std::cout << "=== 单链表演示 ===" << std::endl << std::endl;
    
    LinkedList<int> ll;
    
    std::cout << "尾部添加: 1, 2, 3" << std::endl;
    for (int i = 1; i <= 3; i++) {
        ll.append(i);
    }
    std::cout << "链表: ";
    ll.print();
    std::cout << std::endl;
    
    std::cout << "头部添加: 0" << std::endl;
    ll.prepend(0);
    std::cout << "链表: ";
    ll.print();
    std::cout << std::endl;
    
    std::cout << "在索引2插入99" << std::endl;
    ll.insert(2, 99);
    std::cout << "链表: ";
    ll.print();
    std::cout << std::endl;
    
    std::cout << "反转链表" << std::endl;
    ll.reverse();
    std::cout << "链表: ";
    ll.print();
    std::cout << std::endl;
    
    std::cout << "=== 双链表演示 ===" << std::endl << std::endl;
    
    DoublyLinkedList<int> dll;
    
    std::cout << "尾部添加: 1, 2, 3" << std::endl;
    for (int i = 1; i <= 3; i++) {
        dll.append(i);
    }
    std::cout << "双链表: ";
    dll.print();
    std::cout << std::endl;
    
    std::cout << "头部添加: 0" << std::endl;
    dll.prepend(0);
    std::cout << "双链表: ";
    dll.print();
    std::cout << std::endl;
    
    std::cout << "头部删除: " << dll.popFront() << std::endl;
    std::cout << "双链表: ";
    dll.print();
    std::cout << std::endl;
    
    std::cout << "尾部删除: " << dll.popBack() << std::endl;
    std::cout << "双链表: ";
    dll.print();
    
    return 0;
}

