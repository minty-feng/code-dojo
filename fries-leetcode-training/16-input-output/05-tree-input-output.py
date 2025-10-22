"""
05-树结构输入输出处理

题目描述：
演示二叉树的输入输出处理，包括层序遍历构建和输出。

输入格式：
第一行：整数n（节点数量）
第二行：n个整数，按层序遍历顺序，null用-1表示

输出格式：
输出二叉树的层序遍历结果

示例：
输入：
7
1 2 3 4 5 6 7

输出：
1 2 3 4 5 6 7
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree_from_level_order(values):
    """根据层序遍历数组构建二叉树"""
    if not values or values[0] == -1:
        return None
    
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    
    while queue and i < len(values):
        node = queue.pop(0)
        
        # 左子节点
        if i < len(values) and values[i] != -1:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        # 右子节点
        if i < len(values) and values[i] != -1:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root

def level_order_traversal(root):
    """层序遍历二叉树"""
    if not root:
        return []
    
    result = []
    queue = [root]
    
    while queue:
        node = queue.pop(0)
        result.append(node.val)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return result

def print_tree_level_order(root):
    """打印二叉树的层序遍历"""
    values = level_order_traversal(root)
    print(*values)
    return values

def test_cases():
    """测试用例"""
    print("=== 树结构输入输出测试 ===")
    
    # 模拟输入
    values = [1, 2, 3, 4, 5, 6, 7]
    print(f"输入数组: {values}")
    
    # 构建二叉树
    root = build_tree_from_level_order(values)
    
    # 输出层序遍历
    print("层序遍历输出:")
    print_tree_level_order(root)
    
    # 测试包含null的情况
    print("\n包含null的测试:")
    null_values = [1, 2, 3, -1, -1, 4, 5]
    print(f"输入数组: {null_values}")
    null_root = build_tree_from_level_order(null_values)
    print_tree_level_order(null_root)

if __name__ == "__main__":
    # 运行测试
    test_cases()
    
    # 交互式输入（取消注释以启用）
    # n = int(input())
    # values = list(map(int, input().split()))
    # root = build_tree_from_level_order(values)
    # print_tree_level_order(root)
