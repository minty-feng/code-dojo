"""
LeetCode 134. 加油站
https://leetcode.cn/problems/gas-station/

在一条环路上有n个加油站，其中第i个加油站有汽油gas[i]升。
你有一辆油箱容量无限的的汽车，从第i个加油站开往第i+1个加油站需要消耗汽油cost[i]升。

贪心

时间复杂度：O(n)
空间复杂度：O(1)
"""

def can_complete_circuit(gas, cost):
    """
    加油站 - 贪心法
    
    Args:
        gas: 每个加油站的汽油量
        cost: 每个加油站到下一个加油站的消耗
        
    Returns:
        可以完成环路的起始加油站索引，否则返回-1
    """
    if not gas or not cost or len(gas) != len(cost):
        return -1
    
    total_tank = 0
    current_tank = 0
    start_station = 0
    
    for i in range(len(gas)):
        total_tank += gas[i] - cost[i]
        current_tank += gas[i] - cost[i]
        
        # 如果当前油箱为负，说明从start_station到i都不能作为起点
        if current_tank < 0:
            start_station = i + 1
            current_tank = 0
    
    return start_station if total_tank >= 0 else -1


def test_can_complete_circuit():
    """测试函数"""
    # 测试用例1
    gas1 = [1, 2, 3, 4, 5]
    cost1 = [3, 4, 5, 1, 2]
    result1 = can_complete_circuit(gas1, cost1)
    print(f"测试1 gas={gas1}, cost={cost1}: {result1}")  # 期望: 3
    
    # 测试用例2
    gas2 = [2, 3, 4]
    cost2 = [3, 4, 3]
    result2 = can_complete_circuit(gas2, cost2)
    print(f"测试2 gas={gas2}, cost={cost2}: {result2}")  # 期望: -1
    
    # 测试用例3
    gas3 = [5, 1, 2, 3, 4]
    cost3 = [4, 4, 1, 5, 1]
    result3 = can_complete_circuit(gas3, cost3)
    print(f"测试3 gas={gas3}, cost={cost3}: {result3}")  # 期望: 4


if __name__ == "__main__":
    test_can_complete_circuit()
