"""
LeetCode 141. 环形链表
https://leetcode.cn/problems/linked-list-cycle/

给你一个链表的头节点head，判断链表中是否有环。

快慢指针（Floyd判圈算法）

时间复杂度：O(n)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head):
    """
    环形链表 - 快慢指针法
    
    Args:
        head: 链表头节点
        
    Returns:
        是否有环
    """
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    
    return False


def test_has_cycle():
    """测试函数"""
    # 创建有环的链表: 1->2->3->4->2
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = head.next  # 形成环
    
    result = has_cycle(head)
    print(f"是否有环: {result}")  # 期望: True


if __name__ == "__main__":
    test_has_cycle()
