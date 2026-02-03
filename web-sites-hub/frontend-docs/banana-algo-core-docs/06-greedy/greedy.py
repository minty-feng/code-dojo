"""
贪心算法实现
"""

import heapq

# ========== 区间调度 ==========

def interval_scheduling(intervals):
    """最多不重叠区间数"""
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])  # 按结束时间排序
    
    count = 1
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] >= end:
            count += 1
            end = intervals[i][1]
    
    return count


# ========== 跳跃游戏 ==========

def can_jump(nums):
    """能否跳到最后"""
    max_reach = 0
    
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    
    return True


def jump(nums):
    """最少跳跃次数"""
    jumps = 0
    curr_end = 0
    max_reach = 0
    
    for i in range(len(nums) - 1):
        max_reach = max(max_reach, i + nums[i])
        
        if i == curr_end:
            jumps += 1
            curr_end = max_reach
    
    return jumps


# ========== 分配饼干 ==========

def find_content_children(g, s):
    """g:孩子胃口 s:饼干大小"""
    g.sort()
    s.sort()
    
    child = cookie = 0
    
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    
    return child


# ========== 买卖股票II ==========

def max_profit(prices):
    """可多次买卖"""
    profit = 0
    
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    
    return profit


# ========== 加油站 ==========

def can_complete_circuit(gas, cost):
    """能否环绕一圈"""
    total_tank = 0
    curr_tank = 0
    start = 0
    
    for i in range(len(gas)):
        total_tank += gas[i] - cost[i]
        curr_tank += gas[i] - cost[i]
        
        if curr_tank < 0:
            start = i + 1
            curr_tank = 0
    
    return start if total_tank >= 0 else -1


# ========== 分发糖果 ==========

def candy(ratings):
    """每个孩子至少一个糖，评分高的比邻居多"""
    n = len(ratings)
    candies = [1] * n
    
    # 从左到右
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            candies[i] = candies[i-1] + 1
    
    # 从右到左
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i+1]:
            candies[i] = max(candies[i], candies[i+1] + 1)
    
    return sum(candies)


# ========== 任务调度器 ==========

def least_interval(tasks, n):
    """任务调度最短时间"""
    from collections import Counter
    
    task_counts = Counter(tasks)
    max_count = max(task_counts.values())
    max_count_tasks = sum(1 for count in task_counts.values() if count == max_count)
    
    # 计算最短时间
    intervals = (max_count - 1) * (n + 1) + max_count_tasks
    
    return max(intervals, len(tasks))


def demo():
    """演示贪心算法"""
    print("=== 贪心算法演示 ===\n")
    
    # 区间调度
    intervals = [[1,3], [2,4], [3,5], [1,2]]
    print(f"区间调度 {intervals}:")
    print(f"  最多不重叠区间: {interval_scheduling(intervals)}\n")
    
    # 跳跃游戏
    nums = [2,3,1,1,4]
    print(f"跳跃游戏 {nums}:")
    print(f"  能否跳到最后: {can_jump(nums)}")
    print(f"  最少跳跃次数: {jump(nums)}\n")
    
    # 分配饼干
    g, s = [1,2,3], [1,1]
    print(f"分配饼干 g={g}, s={s}:")
    print(f"  满足孩子数: {find_content_children(g, s)}\n")
    
    # 买卖股票
    prices = [7,1,5,3,6,4]
    print(f"买卖股票II {prices}:")
    print(f"  最大利润: {max_profit(prices)}\n")
    
    # 加油站
    gas = [1,2,3,4,5]
    cost = [3,4,5,1,2]
    print(f"加油站 gas={gas}, cost={cost}:")
    print(f"  起始站: {can_complete_circuit(gas, cost)}\n")
    
    # 分发糖果
    ratings = [1,0,2]
    print(f"分发糖果 {ratings}:")
    print(f"  最少糖果数: {candy(ratings)}")


if __name__ == '__main__':
    demo()

