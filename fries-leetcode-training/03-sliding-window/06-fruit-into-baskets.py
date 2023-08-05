"""
LeetCode 904. 水果成篮
https://leetcode.cn/problems/fruit-into-baskets/

你正在探访一家农场，农场从左到右种植了一排果树。这些树用一个整数数组fruits表示，其中fruits[i]是第i棵树上的水果种类。

你想要尽可能多地收集水果。然而，农场的主人设定了一些严格的规则，你必须按照要求采摘水果：

你只有两个篮子，并且每个篮子只能装单一类型的水果。每个篮子能够装的水果总量没有限制。
你可以选择任意一棵树开始采摘，你必须从每棵树（包括开始采摘的树）上恰好摘一个水果。采摘的水果应当符合篮子中的水果类型。每采摘一次，你将会向右移动到下一棵树，并继续采摘。
一旦你走到某棵树前，但水果不符合篮子的水果类型，那么就必须停止采摘。

滑动窗口

时间复杂度：O(n)
空间复杂度：O(1)
"""

def total_fruit(fruits):
    """
    水果成篮 - 滑动窗口法
    
    Args:
        fruits: 水果数组
        
    Returns:
        最多能收集的水果数量
    """
    left = 0
    max_fruits = 0
    fruit_count = {}
    
    for right in range(len(fruits)):
        # 扩展窗口
        fruit = fruits[right]
        fruit_count[fruit] = fruit_count.get(fruit, 0) + 1
        
        # 收缩窗口
        while len(fruit_count) > 2:
            left_fruit = fruits[left]
            fruit_count[left_fruit] -= 1
            if fruit_count[left_fruit] == 0:
                del fruit_count[left_fruit]
            left += 1
        
        # 更新结果
        max_fruits = max(max_fruits, right - left + 1)
    
    return max_fruits


def test_total_fruit():
    """测试函数"""
    # 测试用例1
    fruits1 = [1, 2, 1, 2, 3]
    result1 = total_fruit(fruits1)
    print(f"测试1: {result1}")
    # 期望: 4
    
    # 测试用例2
    fruits2 = [0, 1, 2, 2]
    result2 = total_fruit(fruits2)
    print(f"测试2: {result2}")
    # 期望: 3
    
    # 测试用例3
    fruits3 = [1, 2, 3, 2, 2]
    result3 = total_fruit(fruits3)
    print(f"测试3: {result3}")
    # 期望: 4


if __name__ == "__main__":
    test_total_fruit()
