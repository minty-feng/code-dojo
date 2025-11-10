"""
二叉树实现和遍历
"""

class TreeNode:
    """二叉树节点"""
    
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BinaryTree:
    """二叉树"""
    
    def __init__(self):
        self.root = None
    
    # ========== 递归遍历 ==========
    
    def preorder(self, root):
        """前序遍历：根→左→右"""
        if not root:
            return []
        return [root.val] + self.preorder(root.left) + self.preorder(root.right)
    
    def inorder(self, root):
        """中序遍历：左→根→右"""
        if not root:
            return []
        return self.inorder(root.left) + [root.val] + self.inorder(root.right)
    
    def postorder(self, root):
        """后序遍历：左→右→根"""
        if not root:
            return []
        return self.postorder(root.left) + self.postorder(root.right) + [root.val]
    
    # ========== 迭代遍历 ==========
    
    def preorder_iterative(self, root):
        """前序遍历（迭代）"""
        if not root:
            return []
        
        stack, result = [root], []
        while stack:
            node = stack.pop()
            result.append(node.val)
            # 先压右子树，再压左子树（栈是后进先出）
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result
    
    def inorder_iterative(self, root):
        """中序遍历（迭代）"""
        stack, result = [], []
        curr = root
        
        while curr or stack:
            # 一直往左走
            while curr:
                stack.append(curr)
                curr = curr.left
            # 处理节点
            curr = stack.pop()
            result.append(curr.val)
            # 转向右子树
            curr = curr.right
        
        return result
    
    def levelorder(self, root):
        """层序遍历（BFS）"""
        if not root:
            return []
        
        queue, result = [root], []
        while queue:
            node = queue.pop(0)
            result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result
    
    def levelorder_levels(self, root):
        """层序遍历（分层）"""
        if not root:
            return []
        
        queue, result = [root], []
        while queue:
            level_size = len(queue)
            level_vals = []
            
            for _ in range(level_size):
                node = queue.pop(0)
                level_vals.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level_vals)
        return result
    
    # ========== 树的性质 ==========
    
    def height(self, root):
        """树的高度"""
        if not root:
            return 0
        return 1 + max(self.height(root.left), self.height(root.right))
    
    def count_nodes(self, root):
        """节点数"""
        if not root:
            return 0
        return 1 + self.count_nodes(root.left) + self.count_nodes(root.right)
    
    def is_balanced(self, root):
        """判断是否平衡"""
        def check(node):
            if not node:
                return 0, True
            
            left_height, left_balanced = check(node.left)
            right_height, right_balanced = check(node.right)
            
            balanced = (left_balanced and right_balanced and 
                       abs(left_height - right_height) <= 1)
            height = 1 + max(left_height, right_height)
            
            return height, balanced
        
        return check(root)[1]
    
    def mirror(self, root):
        """镜像翻转"""
        if not root:
            return
        root.left, root.right = root.right, root.left
        self.mirror(root.left)
        self.mirror(root.right)
    
    def max_path_sum(self, root):
        """最大路径和"""
        self.max_sum = float('-inf')
        
        def helper(node):
            if not node:
                return 0
            
            left = max(0, helper(node.left))
            right = max(0, helper(node.right))
            
            # 更新最大路径和
            self.max_sum = max(self.max_sum, node.val + left + right)
            
            # 返回经过当前节点的最大单边路径
            return node.val + max(left, right)
        
        helper(root)
        return self.max_sum


def demo():
    """演示二叉树操作"""
    print("=== 二叉树演示 ===\n")
    
    # 构建树
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    tree = BinaryTree()
    tree.root = root
    
    # 遍历
    print("前序遍历（递归）:", tree.preorder(root))
    print("前序遍历（迭代）:", tree.preorder_iterative(root))
    print()
    
    print("中序遍历（递归）:", tree.inorder(root))
    print("中序遍历（迭代）:", tree.inorder_iterative(root))
    print()
    
    print("后序遍历（递归）:", tree.postorder(root))
    print()
    
    print("层序遍历:", tree.levelorder(root))
    print("层序遍历（分层）:", tree.levelorder_levels(root))
    print()
    
    # 性质
    print(f"树的高度: {tree.height(root)}")
    print(f"节点数: {tree.count_nodes(root)}")
    print(f"是否平衡: {tree.is_balanced(root)}")


if __name__ == '__main__':
    demo()

