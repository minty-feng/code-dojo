/**
 * NC66 两个链表的第一个公共节点
 * https://www.nowcoder.com/practice/6ab1d9a29e88450685099d45c9e31e46
 * 
 * 输入两个无环的单向链表，找出它们的第一个公共节点。
 * 
 * 时间复杂度：O(m+n)
 * 空间复杂度：O(1)
 */

#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    /**
     * 找到第一个公共节点 - 双指针法
     */
    ListNode* FindFirstCommonNode(ListNode* head1, ListNode* head2) {
        if (!head1 || !head2) {
            return nullptr;
        }
        
        ListNode* p1 = head1;
        ListNode* p2 = head2;
        
        // 两个指针分别走完两个链表
        while (p1 != p2) {
            p1 = p1 ? p1->next : head2;
            p2 = p2 ? p2->next : head1;
        }
        
        return p1;
    }
};

int main() {
    // 创建两个相交的链表
    ListNode* common = new ListNode(6);
    common->next = new ListNode(7);
    
    ListNode* head1 = new ListNode(1);
    head1->next = new ListNode(2);
    head1->next->next = new ListNode(3);
    head1->next->next->next = common;
    
    ListNode* head2 = new ListNode(4);
    head2->next = new ListNode(5);
    head2->next->next = common;
    
    Solution solution;
    ListNode* result = solution.FindFirstCommonNode(head1, head2);
    
    if (result) {
        cout << "第一个公共节点值: " << result->val << endl;
    } else {
        cout << "无公共节点" << endl;
    }
    
    return 0;
}

