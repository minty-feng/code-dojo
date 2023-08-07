/**
 * LeetCode 155. 最小栈
 * https://leetcode.cn/problems/min-stack/
 * 
 * 设计一个支持push，pop，top操作，并能在常数时间内检索到最小元素的栈。
 * 
 * 辅助栈
 * 
 * 时间复杂度：O(1) 所有操作
 * 空间复杂度：O(n)
 */

#include <stack>
using namespace std;

class MinStack {
private:
    stack<int> data_stack;
    stack<int> min_stack;
    
public:
    MinStack() {}
    
    void push(int val) {
        data_stack.push(val);
        if (min_stack.empty() || val <= min_stack.top()) {
            min_stack.push(val);
        }
    }
    
    void pop() {
        if (data_stack.empty()) {
            return;
        }
        
        int val = data_stack.top();
        data_stack.pop();
        
        if (!min_stack.empty() && val == min_stack.top()) {
            min_stack.pop();
        }
    }
    
    int top() {
        return data_stack.top();
    }
    
    int getMin() {
        return min_stack.top();
    }
};

// 测试函数
#include <iostream>
void testMinStack() {
    MinStack minStack;
    
    minStack.push(-2);
    minStack.push(0);
    minStack.push(-3);
    
    cout << "最小元素: " << minStack.getMin() << endl;  // 期望: -3
    
    minStack.pop();
    cout << "栈顶元素: " << minStack.top() << endl;      // 期望: 0
    cout << "最小元素: " << minStack.getMin() << endl;  // 期望: -2
}

int main() {
    testMinStack();
    return 0;
}
