/**
 * NC4 链表中环的入口节点
 * https://www.nowcoder.com/practice/253d2c59ec3e4bc68da16833f79a38e4
 * 
 * 给一个长度为n链表，若其中包含环，请找出该链表的环的入口结点，否则，返回null。
 * 
 * 时间复杂度：O(n)
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
     * 找到环的入口节点
     */
    ListNode* EntryNodeOfLoop(ListNode* head) {
        if (!head || !head->next) {
            return nullptr;
        }
        
        // 1. 快慢指针找相遇点
        ListNode* slow = head;
        ListNode* fast = head;
        
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            
            if (slow == fast) {
                // 2. 找到入口点
                ListNode* ptr = head;
                while (ptr != slow) {
                    ptr = ptr->next;
                    slow = slow->next;
                }
                return ptr;
            }
        }
        
        return nullptr;  // 无环
    }
};

int main() {
    // 创建带环的链表: 1 -> 2 -> 3 -> 4 -> 5 -> 3 (环)
    ListNode* head = new ListNode(1);
    ListNode* node2 = new ListNode(2);
    ListNode* node3 = new ListNode(3);
    ListNode* node4 = new ListNode(4);
    ListNode* node5 = new ListNode(5);
    
    head->next = node2;
    node2->next = node3;
    node3->next = node4;
    node4->next = node5;
    node5->next = node3;  // 形成环
    
    Solution solution;
    ListNode* entry = solution.EntryNodeOfLoop(head);
    
    if (entry) {
        cout << "环的入口节点值: " << entry->val << endl;
    } else {
        cout << "无环" << endl;
    }
    
    return 0;
}

