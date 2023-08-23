"""
LeetCode 743. 网络延迟时间
https://leetcode.cn/problems/network-delay-time/

有n个网络节点，标记为1到n。
给你一个列表times，表示信号经过有向边的传递时间。times[i] = (ui, vi, wi)，
其中ui是源节点，vi是目标节点，wi是一个信号从源节点传递到目标节点的时间。

最短路径（Dijkstra算法）

时间复杂度：O(E log V)
空间复杂度：O(V)
"""

def network_delay_time(times, n, k):
    """
    网络延迟时间 - Dijkstra算法
    
    Args:
        times: 边列表，每个边为(source, target, weight)
        n: 节点数量
        k: 起始节点
        
    Returns:
        所有节点收到信号的最短时间，如果无法到达所有节点则返回-1
    """
    import heapq
    
    # 构建邻接表
    graph = [[] for _ in range(n + 1)]
    for source, target, weight in times:
        graph[source].append((target, weight))
    
    # Dijkstra算法
    dist = [float('inf')] * (n + 1)
    dist[k] = 0
    
    heap = [(0, k)]
    
    while heap:
        d, u = heapq.heappop(heap)
        
        if d > dist[u]:
            continue
        
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    
    # 检查是否所有节点都可达
    max_time = max(dist[1:n+1])
    return max_time if max_time != float('inf') else -1


def network_delay_time_bellman_ford(times, n, k):
    """
    网络延迟时间 - Bellman-Ford算法
    
    Args:
        times: 边列表
        n: 节点数量
        k: 起始节点
        
    Returns:
        最短时间
    """
    dist = [float('inf')] * (n + 1)
    dist[k] = 0
    
    # 松弛操作
    for _ in range(n - 1):
        for source, target, weight in times:
            if dist[source] != float('inf') and dist[source] + weight < dist[target]:
                dist[target] = dist[source] + weight
    
    max_time = max(dist[1:n+1])
    return max_time if max_time != float('inf') else -1


def test_network_delay_time():
    """测试函数"""
    # 测试用例1
    times1 = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    n1, k1 = 4, 2
    result1 = network_delay_time(times1, n1, k1)
    result1_bf = network_delay_time_bellman_ford(times1, n1, k1)
    print(f"测试1 times={times1}, n={n1}, k={k1}: Dijkstra={result1}, BF={result1_bf}")  # 期望: 2
    
    # 测试用例2
    times2 = [[1, 2, 1]]
    n2, k2 = 2, 1
    result2 = network_delay_time(times2, n2, k2)
    result2_bf = network_delay_time_bellman_ford(times2, n2, k2)
    print(f"测试2 times={times2}, n={n2}, k={k2}: Dijkstra={result2}, BF={result2_bf}")  # 期望: 1
    
    # 测试用例3
    times3 = [[1, 2, 1]]
    n3, k3 = 2, 2
    result3 = network_delay_time(times3, n3, k3)
    result3_bf = network_delay_time_bellman_ford(times3, n3, k3)
    print(f"测试3 times={times3}, n={n3}, k={k3}: Dijkstra={result3}, BF={result3_bf}")  # 期望: -1


if __name__ == "__main__":
    test_network_delay_time()
