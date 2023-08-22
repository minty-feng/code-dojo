"""
NC51 合并K个升序链表
https://www.nowcoder.com/practice/65cfde9e5b9b4cf2b6bafa5f3ef33fa6

合并k个已排序的链表并将其作为一个已排序的链表返回。

分治法 + 归并

时间复杂度：O(nlogk)
空间复杂度：O(logk)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists):
    """
    合并K个升序链表 - 分治法
    """
    if not lists:
        return None
    
    def merge_two_lists(l1, l2):
        dummy = ListNode(0)
        curr = dummy
        
        while l1 and l2:
            if l1.val < l2.val:
                curr.next = l1
                l1 = l1.next
            else:
                curr.next = l2
                l2 = l2.next
            curr = curr.next
        
        curr.next = l1 if l1 else l2
        return dummy.next
    
    def merge_lists(lists, left, right):
        if left == right:
            return lists[left]
        
        mid = (left + right) // 2
        l1 = merge_lists(lists, left, mid)
        l2 = merge_lists(lists, mid + 1, right)
        
        return merge_two_lists(l1, l2)
    
    return merge_lists(lists, 0, len(lists) - 1)

# 测试
if __name__ == "__main__":
    # 创建测试链表
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
    
    lists = [
        create_list([1, 4, 5]),
        create_list([1, 3, 4]),
        create_list([2, 6])
    ]
    
    merged = merge_k_lists(lists)
    print_list(merged)

