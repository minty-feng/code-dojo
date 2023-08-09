/**
 * LeetCode 160. 相交链表
 * https://leetcode.cn/problems/intersection-of-two-linked-lists/
 * 
 * 给你两个单链表的头节点headA和headB，请你找出并返回两个单链表相交的起始节点。
 * 
 * 双指针
 * 
 * 时间复杂度：O(m+n)
 * 空间复杂度：O(1)
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        if (!headA || !headB) {
            return nullptr;
        }
        
        ListNode* ptrA = headA;
        ListNode* ptrB = headB;
        
        // 当两个指针都走完两个链表时，会在相交点相遇
        while (ptrA != ptrB) {
            ptrA = ptrA ? ptrA->next : headB;
            ptrB = ptrB ? ptrB->next : headA;
        }
        
        return ptrA;
    }
};

// 测试函数
#include <iostream>
void testGetIntersectionNode() {
    Solution solution;
    
    // 创建相交的链表
    // 链表A: 4->1->8->4->5
    // 链表B: 5->6->1->8->4->5
    // 相交点: 8
    
    ListNode* common = new ListNode(8);
    common->next = new ListNode(4);
    common->next->next = new ListNode(5);
    
    ListNode* headA = new ListNode(4);
    headA->next = new ListNode(1);
    headA->next->next = common;
    
    ListNode* headB = new ListNode(5);
    headB->next = new ListNode(6);
    headB->next->next = new ListNode(1);
    headB->next->next->next = common;
    
    ListNode* intersection = solution.getIntersectionNode(headA, headB);
    if (intersection) {
        cout << "相交节点值: " << intersection->val << endl;  // 期望: 8
    } else {
        cout << "无相交" << endl;
    }
}

int main() {
    testGetIntersectionNode();
    return 0;
}
