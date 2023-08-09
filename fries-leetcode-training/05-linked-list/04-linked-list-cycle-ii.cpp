/**
 * LeetCode 142. 环形链表II
 * https://leetcode.cn/problems/linked-list-cycle-ii/
 * 
 * 给定一个链表的头节点head，返回链表开始入环的第一个节点。如果链表无环，则返回null。
 * 
 * 快慢指针（Floyd判圈算法）
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        if (!head || !head->next) {
            return nullptr;
        }
        
        // 第一阶段：找到相遇点
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) {
                break;
            }
        }
        
        if (!fast || !fast->next) {
            return nullptr;  // 无环
        }
        
        // 第二阶段：找到环的起点
        slow = head;
        while (slow != fast) {
            slow = slow->next;
            fast = fast->next;
        }
        
        return slow;
    }
};

// 测试函数
#include <iostream>
void testDetectCycle() {
    Solution solution;
    
    // 创建有环的链表: 1->2->3->4->2
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = head->next;  // 形成环
    
    ListNode* cycle_start = solution.detectCycle(head);
    if (cycle_start) {
        cout << "环的起始节点值: " << cycle_start->val << endl;  // 期望: 2
    } else {
        cout << "无环" << endl;
    }
}

int main() {
    testDetectCycle();
    return 0;
}
