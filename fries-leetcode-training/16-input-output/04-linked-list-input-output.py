"""
04-链表输入输出处理

题目描述：
演示链表的输入输出处理，包括链表构建和遍历。

输入格式：
第一行：整数n（链表长度）
第二行：n个整数，表示链表节点的值

输出格式：
输出链表的所有节点值，空格分隔

示例：
输入：
5
1 2 3 4 5

输出：
1 2 3 4 5
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_linked_list(values):
    """根据数组构建链表"""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    
    for i in range(1, len(values)):
        current.next = ListNode(values[i])
        current = current.next
    
    return head

def print_linked_list(head):
    """打印链表"""
    values = []
    current = head
    
    while current:
        values.append(current.val)
        current = current.next
    
    print(*values)
    return values

def linked_list_to_array(head):
    """链表转数组"""
    result = []
    current = head
    
    while current:
        result.append(current.val)
        current = current.next
    
    return result

def test_cases():
    """测试用例"""
    print("=== 链表输入输出测试 ===")
    
    # 模拟输入
    values = [1, 2, 3, 4, 5]
    print(f"输入数组: {values}")
    
    # 构建链表
    head = build_linked_list(values)
    
    # 输出链表
    print("输出链表:")
    print_linked_list(head)
    
    # 验证转换
    converted = linked_list_to_array(head)
    print(f"转换回数组: {converted}")
    
    # 测试空链表
    print("\n空链表测试:")
    empty_head = build_linked_list([])
    print_linked_list(empty_head)

if __name__ == "__main__":
    # 运行测试
    test_cases()
    
    # 交互式输入（取消注释以启用）
    # n = int(input())
    # values = list(map(int, input().split()))
    # head = build_linked_list(values)
    # print_linked_list(head)
