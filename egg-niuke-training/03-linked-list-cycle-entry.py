"""
NC4 链表中环的入口节点
https://www.nowcoder.com/practice/253d2c59ec3e4bc68da16833f79a38e4

给一个长度为n链表，若其中包含环，请找出该链表的环的入口结点，否则，返回null。

算法：快慢指针
1. 快指针每次走2步，慢指针每次走1步
2. 相遇后，一个指针回到head，两个指针每次都走1步
3. 再次相遇的节点就是环的入口

时间复杂度：O(n)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def detect_cycle(head):
    """
    找到环的入口节点
    """
    if not head or not head.next:
        return None
    
    # 1. 快慢指针找相遇点
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            # 2. 找到入口点
            ptr = head
            while ptr != slow:
                ptr = ptr.next
                slow = slow.next
            return ptr
    
    return None  # 无环

# 测试
if __name__ == "__main__":
    # 创建带环的链表: 1 -> 2 -> 3 -> 4 -> 5 -> 3 (环)
    head = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node5 = ListNode(5)
    
    head.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node3  # 形成环
    
    entry = detect_cycle(head)
    if entry:
        print(f"环的入口节点值: {entry.val}")
    else:
        print("无环")

