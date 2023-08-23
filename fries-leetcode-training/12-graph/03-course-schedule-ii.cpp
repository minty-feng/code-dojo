/**
 * LeetCode 210. 课程表II
 * https://leetcode.cn/problems/course-schedule-ii/
 * 
 * 现在你总共有numCourses门课需要选，记为0到numCourses-1。
 * 给你一个数组prerequisites，其中prerequisites[i] = [ai, bi]，
 * 表示在选修课程ai前必须先选修bi。
 * 
 * 拓扑排序
 * 
 * 时间复杂度：O(V + E)
 * 空间复杂度：O(V + E)
 */

class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        // 构建邻接表和入度数组
        vector<vector<int>> graph(numCourses);
        vector<int> indegree(numCourses, 0);
        
        for (const auto& prereq : prerequisites) {
            int course = prereq[0];
            int prereq_course = prereq[1];
            graph[prereq_course].push_back(course);
            indegree[course]++;
        }
        
        // 找到所有入度为0的课程
        queue<int> q;
        for (int i = 0; i < numCourses; i++) {
            if (indegree[i] == 0) {
                q.push(i);
            }
        }
        
        vector<int> result;
        
        while (!q.empty()) {
            int course = q.front();
            q.pop();
            result.push_back(course);
            
            // 处理该课程的所有后续课程
            for (int next_course : graph[course]) {
                indegree[next_course]--;
                if (indegree[next_course] == 0) {
                    q.push(next_course);
                }
            }
        }
        
        return result.size() == numCourses ? result : vector<int>();
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

void testFindOrder() {
    Solution solution;
    
    int numCourses1 = 2;
    vector<vector<int>> prerequisites1 = {{1, 0}};
    vector<int> result1 = solution.findOrder(numCourses1, prerequisites1);
    cout << "测试1 numCourses=2, prerequisites={{1,0}}: ";
    for (int course : result1) {
        cout << course << " ";
    }
    cout << endl;  // 期望: 0 1
    
    int numCourses2 = 4;
    vector<vector<int>> prerequisites2 = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
    vector<int> result2 = solution.findOrder(numCourses2, prerequisites2);
    cout << "测试2 numCourses=4, prerequisites={{1,0},{2,0},{3,1},{3,2}}: ";
    for (int course : result2) {
        cout << course << " ";
    }
    cout << endl;  // 期望: 0 1 2 3 或 0 2 1 3
}

int main() {
    testFindOrder();
    return 0;
}
