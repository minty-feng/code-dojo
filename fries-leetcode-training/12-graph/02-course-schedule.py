"""
LeetCode 207. 课程表
https://leetcode.cn/problems/course-schedule/

你这个学期必须选修numCourses门课程，记为0到numCourses-1。
在选修某些课程之前需要一些先修课程。先修课程按数组prerequisites给出。

拓扑排序

时间复杂度：O(V + E)
空间复杂度：O(V + E)
"""

def can_finish(num_courses, prerequisites):
    """
    课程表 - 拓扑排序法
    
    Args:
        num_courses: 课程总数
        prerequisites: 先修课程关系
        
    Returns:
        是否能够完成所有课程
    """
    # 构建邻接表和入度数组
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    # 找到所有入度为0的课程
    queue = []
    for i in range(num_courses):
        if indegree[i] == 0:
            queue.append(i)
    
    completed = 0
    
    while queue:
        course = queue.pop(0)
        completed += 1
        
        # 处理该课程的所有后续课程
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)
    
    return completed == num_courses


def test_can_finish():
    """测试函数"""
    # 测试用例1
    num_courses1 = 2
    prerequisites1 = [[1, 0]]
    result1 = can_finish(num_courses1, prerequisites1)
    print(f"测试1 numCourses=2, prerequisites=[[1,0]]: {result1}")  # 期望: True
    
    # 测试用例2
    num_courses2 = 2
    prerequisites2 = [[1, 0], [0, 1]]
    result2 = can_finish(num_courses2, prerequisites2)
    print(f"测试2 numCourses=2, prerequisites=[[1,0],[0,1]]: {result2}")  # 期望: False
    
    # 测试用例3
    num_courses3 = 4
    prerequisites3 = [[1, 0], [2, 0], [3, 1], [3, 2]]
    result3 = can_finish(num_courses3, prerequisites3)
    print(f"测试3 numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]: {result3}")  # 期望: True


if __name__ == "__main__":
    test_can_finish()
