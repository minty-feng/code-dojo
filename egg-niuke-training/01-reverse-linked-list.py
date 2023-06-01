"""
NC78 反转链表
https://www.nowcoder.com/practice/75e878df47f24fdc9dc3e400ec6058ca

给定一个单链表的头节点head，请反转链表，并返回反转后链表的头节点。

时间复杂度：O(n)
空间复杂度：O(1)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    """
    反转链表 - 迭代法
    """
    prev = None
    curr = head
    
    while curr:
        next_node = curr.next  # 保存下一个节点
        curr.next = prev       # 反转指针
        prev = curr            # prev前进
        curr = next_node       # curr前进
    
    return prev

def reverse_linked_list_recursive(head):
    """
    反转链表 - 递归法
    """
    if not head or not head.next:
        return head
    
    # 递归反转后面的链表
    new_head = reverse_linked_list_recursive(head.next)
    
    # 当前节点的下一个节点指向当前节点
    head.next.next = head
    head.next = None
    
    return new_head

# 辅助函数
def create_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def print_list(head):
    values = []
    while head:
        values.append(str(head.val))
        head = head.next
    print(' -> '.join(values))

if __name__ == "__main__":
    # 测试
    head = create_list([1, 2, 3, 4, 5])
    print("原链表:")
    print_list(head)
    
    reversed_head = reverse_linked_list(head)
    print("反转后:")
    print_list(reversed_head)

