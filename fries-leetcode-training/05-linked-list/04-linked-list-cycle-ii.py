"""
LeetCode 142. 环形链表II
https://leetcode.cn/problems/linked-list-cycle-ii/

给定一个链表的头节点head，返回链表开始入环的第一个节点。如果链表无环，则返回null。

快慢指针（Floyd判圈算法）

时间复杂度：O(n)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def detect_cycle(head):
    """
    环形链表II - 快慢指针法
    
    Args:
        head: 链表头节点
        
    Returns:
        环的起始节点，无环则返回None
    """
    if not head or not head.next:
        return None
    
    # 第一阶段：找到相遇点
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # 无环
    
    # 第二阶段：找到环的起点
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow


def test_detect_cycle():
    """测试函数"""
    # 创建有环的链表: 1->2->3->4->2
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = head.next  # 形成环
    
    cycle_start = detect_cycle(head)
    if cycle_start:
        print(f"环的起始节点值: {cycle_start.val}")  # 期望: 2
    else:
        print("无环")


if __name__ == "__main__":
    test_detect_cycle()
