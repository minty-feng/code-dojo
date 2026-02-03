"""
递归与回溯算法实现
"""

# ========== 1. 全排列 ==========

def permute(nums):
    """全排列"""
    result = []
    
    def backtrack(path, choices):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(choices)):
            path.append(choices[i])
            backtrack(path, choices[:i] + choices[i+1:])
            path.pop()
    
    backtrack([], nums)
    return result


# ========== 2. 组合 ==========

def combine(n, k):
    """从1到n选k个数的所有组合"""
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result


# ========== 3. 子集 ==========

def subsets(nums):
    """所有子集"""
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result


# ========== 4. N皇后 ==========

def solve_n_queens(n):
    """N皇后问题"""
    result = []
    board = [['.'] * n for _ in range(n)]
    
    def is_valid(row, col):
        # 检查列
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # 检查左上对角线
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # 检查右上对角线
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(row):
        if row == n:
            result.append([''.join(row) for row in board])
            return
        
        for col in range(n):
            if is_valid(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
    
    backtrack(0)
    return result


# ========== 5. 括号生成 ==========

def generate_parenthesis(n):
    """生成n对有效括号"""
    result = []
    
    def backtrack(path, left, right):
        if len(path) == 2 * n:
            result.append(path)
            return
        
        if left < n:
            backtrack(path + '(', left + 1, right)
        if right < left:
            backtrack(path + ')', left, right + 1)
    
    backtrack('', 0, 0)
    return result


# ========== 6. 组合总和 ==========

def combination_sum(candidates, target):
    """数字可重复使用"""
    result = []
    
    def backtrack(start, path, total):
        if total == target:
            result.append(path[:])
            return
        if total > target:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, total + candidates[i])  # i不是i+1，可重复
            path.pop()
    
    backtrack(0, [], 0)
    return result


# ========== 7. 单词搜索 ==========

def exist(board, word):
    """在网格中查找单词"""
    m, n = len(board), len(board[0])
    
    def backtrack(i, j, k):
        if k == len(word):
            return True
        
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
            return False
        
        temp = board[i][j]
        board[i][j] = '#'  # 标记已访问
        
        found = (backtrack(i+1, j, k+1) or
                backtrack(i-1, j, k+1) or
                backtrack(i, j+1, k+1) or
                backtrack(i, j-1, k+1))
        
        board[i][j] = temp  # 恢复
        return found
    
    for i in range(m):
        for j in range(n):
            if backtrack(i, j, 0):
                return True
    return False


def demo():
    """演示回溯算法"""
    print("=== 回溯算法演示 ===\n")
    
    # 全排列
    print("全排列 [1,2,3]:")
    print(permute([1, 2, 3]))
    print()
    
    # 组合
    print("C(4,2) 组合:")
    print(combine(4, 2))
    print()
    
    # 子集
    print("子集 [1,2,3]:")
    print(subsets([1, 2, 3]))
    print()
    
    # N皇后
    print("4皇后问题:")
    solutions = solve_n_queens(4)
    print(f"共{len(solutions)}种解法")
    for i, solution in enumerate(solutions):
        print(f"\n解法{i+1}:")
        for row in solution:
            print(row)
    print()
    
    # 括号生成
    print("3对括号:")
    print(generate_parenthesis(3))
    print()
    
    # 组合总和
    print("组合总和 candidates=[2,3,6,7], target=7:")
    print(combination_sum([2, 3, 6, 7], 7))


if __name__ == '__main__':
    demo()

