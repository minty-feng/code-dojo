/**
 * NC51 合并K个升序链表
 * https://www.nowcoder.com/practice/65cfde9e5b9b4cf2b6bafa5f3ef33fa6
 * 
 * 合并k个已排序的链表并将其作为一个已排序的链表返回。
 * 
 * 时间复杂度：O(nlogk)
 * 空间复杂度：O(logk)
 */

#include <iostream>
#include <vector>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        if (lists.empty()) return nullptr;
        
        return mergeLists(lists, 0, lists.size() - 1);
    }

private:
    ListNode* mergeLists(vector<ListNode*>& lists, int left, int right) {
        if (left == right) {
            return lists[left];
        }
        
        int mid = left + (right - left) / 2;
        ListNode* l1 = mergeLists(lists, left, mid);
        ListNode* l2 = mergeLists(lists, mid + 1, right);
        
        return mergeTwoLists(l1, l2);
    }
    
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        ListNode dummy(0);
        ListNode* curr = &dummy;
        
        while (l1 && l2) {
            if (l1->val < l2->val) {
                curr->next = l1;
                l1 = l1->next;
            } else {
                curr->next = l2;
                l2 = l2->next;
            }
            curr = curr->next;
        }
        
        curr->next = l1 ? l1 : l2;
        return dummy.next;
    }
};

int main() {
    // 创建测试链表
    ListNode* list1 = new ListNode(1);
    list1->next = new ListNode(4);
    list1->next->next = new ListNode(5);
    
    ListNode* list2 = new ListNode(1);
    list2->next = new ListNode(3);
    list2->next->next = new ListNode(4);
    
    ListNode* list3 = new ListNode(2);
    list3->next = new ListNode(6);
    
    vector<ListNode*> lists = {list1, list2, list3};
    
    Solution solution;
    ListNode* merged = solution.mergeKLists(lists);
    
    cout << "合并结果: ";
    while (merged) {
        cout << merged->val;
        if (merged->next) cout << " -> ";
        merged = merged->next;
    }
    cout << endl;
    
    return 0;
}

