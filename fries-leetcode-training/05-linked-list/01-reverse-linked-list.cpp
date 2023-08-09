/**
 * LeetCode 206. 反转链表
 * https://leetcode.cn/problems/reverse-linked-list/
 * 
 * 给你单链表的头节点head，请你反转链表，并返回反转后的链表。
 * 
 * 迭代/递归
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1) 迭代 / O(n) 递归
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    // 迭代法
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* current = head;
        
        while (current) {
            ListNode* next_temp = current->next;
            current->next = prev;
            prev = current;
            current = next_temp;
        }
        
        return prev;
    }
    
    // 递归法
    ListNode* reverseListRecursive(ListNode* head) {
        if (!head || !head->next) {
            return head;
        }
        
        ListNode* new_head = reverseListRecursive(head->next);
        head->next->next = head;
        head->next = nullptr;
        
        return new_head;
    }
};

// 测试函数
#include <iostream>
void testReverseList() {
    Solution solution;
    
    // 创建测试链表: 1->2->3->4->5
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = new ListNode(5);
    
    ListNode* reversed_head = solution.reverseList(head);
    
    cout << "反转结果: ";
    ListNode* current = reversed_head;
    while (current) {
        cout << current->val;
        if (current->next) cout << "->";
        current = current->next;
    }
    cout << endl;
}

int main() {
    testReverseList();
    return 0;
}
