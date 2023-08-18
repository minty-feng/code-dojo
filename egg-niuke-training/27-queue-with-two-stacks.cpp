/**
 * NC76 用两个栈实现队列
 * https://www.nowcoder.com/practice/54275ddae22f475981afa2244dd448c6
 * 
 * 用两个栈来实现一个队列，完成队列的Push和Pop操作。
 * 
 * 时间复杂度：Push O(1), Pop 摊还O(1)
 * 空间复杂度：O(n)
 */

#include <iostream>
#include <stack>
using namespace std;

class Solution {
public:
    void push(int node) {
        stack1.push(node);
    }

    int pop() {
        if (stack2.empty()) {
            // 将stack1的所有元素转移到stack2
            while (!stack1.empty()) {
                stack2.push(stack1.top());
                stack1.pop();
            }
        }
        
        if (stack2.empty()) {
            return -1;  // 队列为空
        }
        
        int result = stack2.top();
        stack2.pop();
        return result;
    }

private:
    stack<int> stack1;  // 用于入队
    stack<int> stack2;  // 用于出队
};

int main() {
    Solution queue;
    
    // 测试
    queue.push(1);
    queue.push(2);
    queue.push(3);
    
    cout << "出队: " << queue.pop() << endl;  // 1
    cout << "出队: " << queue.pop() << endl;  // 2
    
    queue.push(4);
    cout << "出队: " << queue.pop() << endl;  // 3
    cout << "出队: " << queue.pop() << endl;  // 4
    
    return 0;
}

