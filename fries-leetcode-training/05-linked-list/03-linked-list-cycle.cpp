/**
 * LeetCode 141. 环形链表
 * https://leetcode.cn/problems/linked-list-cycle/
 * 
 * 给你一个链表的头节点head，判断链表中是否有环。
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
    bool hasCycle(ListNode *head) {
        if (!head || !head->next) {
            return false;
        }
        
        ListNode* slow = head;
        ListNode* fast = head->next;
        
        while (fast && fast->next) {
            if (slow == fast) {
                return true;
            }
            slow = slow->next;
            fast = fast->next->next;
        }
        
        return false;
    }
};

// 测试函数
#include <iostream>
void testHasCycle() {
    Solution solution;
    
    // 创建有环的链表: 1->2->3->4->2
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = head->next;  // 形成环
    
    bool result = solution.hasCycle(head);
    cout << "是否有环: " << (result ? "True" : "False") << endl;
}

int main() {
    testHasCycle();
    return 0;
}
