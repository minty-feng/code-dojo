/**
 * LeetCode 21. 合并两个有序链表
 * https://leetcode.cn/problems/merge-two-sorted-lists/
 * 
 * 将两个升序链表合并为一个新的升序链表并返回。
 * 
 * 归并排序思想
 * 
 * 时间复杂度：O(n+m)
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
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        ListNode dummy(0);
        ListNode* current = &dummy;
        
        while (l1 && l2) {
            if (l1->val <= l2->val) {
                current->next = l1;
                l1 = l1->next;
            } else {
                current->next = l2;
                l2 = l2->next;
            }
            current = current->next;
        }
        
        current->next = l1 ? l1 : l2;
        return dummy.next;
    }
};

// 测试函数
#include <iostream>
void testMergeTwoLists() {
    Solution solution;
    
    // 创建测试链表1: 1->2->4
    ListNode* l1 = new ListNode(1);
    l1->next = new ListNode(2);
    l1->next->next = new ListNode(4);
    
    // 创建测试链表2: 1->3->4
    ListNode* l2 = new ListNode(1);
    l2->next = new ListNode(3);
    l2->next->next = new ListNode(4);
    
    ListNode* merged = solution.mergeTwoLists(l1, l2);
    
    cout << "合并结果: ";
    ListNode* current = merged;
    while (current) {
        cout << current->val;
        if (current->next) cout << "->";
        current = current->next;
    }
    cout << endl;
}

int main() {
    testMergeTwoLists();
    return 0;
}
