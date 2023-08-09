/**
 * LeetCode 234. 回文链表
 * https://leetcode.cn/problems/palindrome-linked-list/
 * 
 * 给你一个单链表的头节点head，请你判断该链表是否为回文链表。
 * 
 * 快慢指针 + 反转
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
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
    bool isPalindrome(ListNode* head) {
        if (!head || !head->next) {
            return true;
        }
        
        // 找到链表中点
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        
        // 反转后半部分
        ListNode* second_half = reverseList(slow);
        
        // 比较前半部分和反转后的后半部分
        ListNode* first_half = head;
        while (second_half) {
            if (first_half->val != second_half->val) {
                return false;
            }
            first_half = first_half->next;
            second_half = second_half->next;
        }
        
        return true;
    }
    
private:
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
};

// 测试函数
#include <iostream>
void testIsPalindrome() {
    Solution solution;
    
    // 测试用例1: 1->2->2->1 (回文)
    ListNode* head1 = new ListNode(1);
    head1->next = new ListNode(2);
    head1->next->next = new ListNode(2);
    head1->next->next->next = new ListNode(1);
    
    bool result1 = solution.isPalindrome(head1);
    cout << "测试1 (1->2->2->1): " << (result1 ? "True" : "False") << endl;  // 期望: True
    
    // 测试用例2: 1->2 (非回文)
    ListNode* head2 = new ListNode(1);
    head2->next = new ListNode(2);
    
    bool result2 = solution.isPalindrome(head2);
    cout << "测试2 (1->2): " << (result2 ? "True" : "False") << endl;  // 期望: False
}

int main() {
    testIsPalindrome();
    return 0;
}
