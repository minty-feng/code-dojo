"""
LeetCode 135. 分发糖果
https://leetcode.cn/problems/candy/

n个孩子站成一排。给你一个整数数组ratings表示每个孩子的评分。
你需要按照以下要求，给这些孩子分发糖果：
- 每个孩子至少分得1个糖果
- 相邻的孩子中，评分高的孩子必须获得更多的糖果

贪心

时间复杂度：O(n)
空间复杂度：O(n)
"""

def candy(ratings):
    """
    分发糖果 - 贪心法
    
    Args:
        ratings: 每个孩子的评分数组
        
    Returns:
        最少需要的糖果数量
    """
    n = len(ratings)
    candies = [1] * n
    
    # 从左到右遍历，确保右边评分高的孩子糖果更多
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            candies[i] = candies[i-1] + 1
    
    # 从右到左遍历，确保左边评分高的孩子糖果更多
    for i in range(n-2, -1, -1):
        if ratings[i] > ratings[i+1]:
            candies[i] = max(candies[i], candies[i+1] + 1)
    
    return sum(candies)


def candy_optimized(ratings):
    """
    分发糖果 - 空间优化版本
    
    Args:
        ratings: 每个孩子的评分数组
        
    Returns:
        最少需要的糖果数量
    """
    n = len(ratings)
    
    # 计算每个位置左边递增序列的长度
    left = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            left[i] = left[i-1] + 1
    
    # 计算每个位置右边递增序列的长度
    right = [1] * n
    for i in range(n-2, -1, -1):
        if ratings[i] > ratings[i+1]:
            right[i] = right[i+1] + 1
    
    # 取最大值
    return sum(max(left[i], right[i]) for i in range(n))


def test_candy():
    """测试函数"""
    # 测试用例1
    ratings1 = [1, 0, 2]
    result1 = candy(ratings1)
    result1_opt = candy_optimized(ratings1)
    print(f"测试1 [1,0,2]: DP={result1}, Opt={result1_opt}")  # 期望: 5
    
    # 测试用例2
    ratings2 = [1, 2, 2]
    result2 = candy(ratings2)
    result2_opt = candy_optimized(ratings2)
    print(f"测试2 [1,2,2]: DP={result2}, Opt={result2_opt}")  # 期望: 4
    
    # 测试用例3
    ratings3 = [1, 3, 2, 2, 1]
    result3 = candy(ratings3)
    result3_opt = candy_optimized(ratings3)
    print(f"测试3 [1,3,2,2,1]: DP={result3}, Opt={result3_opt}")  # 期望: 7


if __name__ == "__main__":
    test_candy()
