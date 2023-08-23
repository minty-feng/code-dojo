/**
 * LeetCode 207. 课程表
 * https://leetcode.cn/problems/course-schedule/
 * 
 * 你这个学期必须选修numCourses门课程，记为0到numCourses-1。
 * 在选修某些课程之前需要一些先修课程。先修课程按数组prerequisites给出。
 * 
 * 拓扑排序
 * 
 * 时间复杂度：O(V + E)
 * 空间复杂度：O(V + E)
 */

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
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
        
        int completed = 0;
        
        while (!q.empty()) {
            int course = q.front();
            q.pop();
            completed++;
            
            // 处理该课程的所有后续课程
            for (int next_course : graph[course]) {
                indegree[next_course]--;
                if (indegree[next_course] == 0) {
                    q.push(next_course);
                }
            }
        }
        
        return completed == numCourses;
    }
};

// 测试函数
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

void testCanFinish() {
    Solution solution;
    
    int numCourses1 = 2;
    vector<vector<int>> prerequisites1 = {{1, 0}};
    bool result1 = solution.canFinish(numCourses1, prerequisites1);
    cout << "测试1 numCourses=2, prerequisites={{1,0}}: " << (result1 ? "True" : "False") << endl;  // 期望: True
    
    int numCourses2 = 2;
    vector<vector<int>> prerequisites2 = {{1, 0}, {0, 1}};
    bool result2 = solution.canFinish(numCourses2, prerequisites2);
    cout << "测试2 numCourses=2, prerequisites={{1,0},{0,1}}: " << (result2 ? "True" : "False") << endl;  // 期望: False
}

int main() {
    testCanFinish();
    return 0;
}
