/**
 * LeetCode 743. 网络延迟时间
 * https://leetcode.cn/problems/network-delay-time/
 * 
 * 有n个网络节点，标记为1到n。
 * 给你一个列表times，表示信号经过有向边的传递时间。times[i] = (ui, vi, wi)，
 * 其中ui是源节点，vi是目标节点，wi是一个信号从源节点传递到目标节点的时间。
 * 
 * 最短路径（Dijkstra算法）
 * 
 * 时间复杂度：O(E log V)
 * 空间复杂度：O(V)
 */

class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        // 构建邻接表
        vector<vector<pair<int, int>>> graph(n + 1);
        for (const auto& time : times) {
            int source = time[0];
            int target = time[1];
            int weight = time[2];
            graph[source].push_back({target, weight});
        }
        
        // Dijkstra算法
        vector<int> dist(n + 1, INT_MAX);
        dist[k] = 0;
        
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, k});
        
        while (!pq.empty()) {
            int d = pq.top().first;
            int u = pq.top().second;
            pq.pop();
            
            if (d > dist[u]) {
                continue;
            }
            
            for (const auto& edge : graph[u]) {
                int v = edge.first;
                int w = edge.second;
                
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.push({dist[v], v});
                }
            }
        }
        
        // 检查是否所有节点都可达
        int maxTime = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == INT_MAX) {
                return -1;
            }
            maxTime = max(maxTime, dist[i]);
        }
        
        return maxTime;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <algorithm>
using namespace std;

void testNetworkDelayTime() {
    Solution solution;
    
    vector<vector<int>> times1 = {{2, 1, 1}, {2, 3, 1}, {3, 4, 1}};
    int n1 = 4, k1 = 2;
    int result1 = solution.networkDelayTime(times1, n1, k1);
    cout << "测试1 times={{2,1,1},{2,3,1},{3,4,1}}, n=" << n1 << ", k=" << k1 << ": " << result1 << endl;  // 期望: 2
    
    vector<vector<int>> times2 = {{1, 2, 1}};
    int n2 = 2, k2 = 1;
    int result2 = solution.networkDelayTime(times2, n2, k2);
    cout << "测试2 times={{1,2,1}}, n=" << n2 << ", k=" << k2 << ": " << result2 << endl;  // 期望: 1
    
    vector<vector<int>> times3 = {{1, 2, 1}};
    int n3 = 2, k3 = 2;
    int result3 = solution.networkDelayTime(times3, n3, k3);
    cout << "测试3 times={{1,2,1}}, n=" << n3 << ", k=" << k3 << ": " << result3 << endl;  // 期望: -1
}

int main() {
    testNetworkDelayTime();
    return 0;
}
