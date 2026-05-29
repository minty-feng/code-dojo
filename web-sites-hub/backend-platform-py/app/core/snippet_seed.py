"""Default snippet records seeded on first database init."""

DEFAULT_SNIPPETS: list[dict] = [
    {
        "slug": "lowest-common-ancestor",
        "title": "二叉树的最近公共祖先",
        "file_name": "lowest_common_ancestor.cpp",
        "lang": "cpp",
        "category": "tree",
        "tags": "binary-tree,lca",
        "sort_order": 10,
        "description": "给定二叉树与两个节点，求最近公共祖先。",
        "code": """\
//
// 示例：
//        3
//       / \\
//      5   1
//     / \\ / \\
//    6  2 0  8
//      / \\
//     7   4
// p = 5, q = 1  →  LCA = 3
// p = 5, q = 4  →  LCA = 5

#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    explicit TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* lowest_common_ancestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) {
        return root;
    }
    TreeNode* left = lowest_common_ancestor(root->left, p, q);
    TreeNode* right = lowest_common_ancestor(root->right, p, q);
    if (left && right) {
        return root;
    }
    return left ? left : right;
}

TreeNode* build_sample_tree(
    TreeNode*& n5, TreeNode*& n1, TreeNode*& n4) {
    auto* n3 = new TreeNode(3);
    n5 = new TreeNode(5);
    n1 = new TreeNode(1);
    auto* n6 = new TreeNode(6);
    auto* n2 = new TreeNode(2);
    auto* n0 = new TreeNode(0);
    auto* n8 = new TreeNode(8);
    auto* n7 = new TreeNode(7);
    n4 = new TreeNode(4);

    n3->left = n5;
    n3->right = n1;
    n5->left = n6;
    n5->right = n2;
    n1->left = n0;
    n1->right = n8;
    n2->left = n7;
    n2->right = n4;
    return n3;
}

int main() {
    TreeNode *p = nullptr, *q = nullptr, *node4 = nullptr;
    TreeNode* root = build_sample_tree(p, q, node4);
    q = root->right;  // 节点 1

    TreeNode* lca1 = lowest_common_ancestor(root, p, q);
    std::cout << "LCA(5, 1) = " << (lca1 ? lca1->val : -1) << std::endl;

    TreeNode* lca2 = lowest_common_ancestor(root, p, node4);
    std::cout << "LCA(5, 4) = " << (lca2 ? lca2->val : -1) << std::endl;
    return 0;
}""",
    },
    {
        "slug": "find-seq-arr",
        "title": "最长连续序列",
        "file_name": "find_seq_arr.cpp",
        "lang": "cpp",
        "category": "array-hash",
        "tags": "array,hash",
        "sort_order": 20,
        "description": "给定整数数组，找出数字连续的最长序列。",
        "code": """\
/* 
  你必须定义一个 `main()` 函数入口。
  you must define a `main()` function entry.
*/

// 算法：给定一个整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）
// input: {9, 3, 1, 4, 2, 3, 7, 6}
// {1, 2, 3, 4}
// {6, 7}
// {9}
// output: {1, 2, 3, 4}




#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_set>


// 1 3 5 7 9

std::vector<int> find_seq_arr(const std::vector<int>& vec){
  if(vec.empty()) return std::vector<int>();
  if(vec.size() == 1) return vec;

  auto arr_set = std::unordered_set<int>(vec.begin(),vec.end());
  auto arr = std::vector<int>(arr_set.begin(), arr_set.end());
  std::sort(arr.begin(), arr.end());
  int length = static_cast<int>(arr.size());
    
    int pre = arr[0]; // check 
    int pose = 0;  // start
    int count = 1; // count

    int pose_sign = pose; //max pose
    int count_sign = count; // max
    
    for(int i = 1; i < length; i++){
        if(arr[i] != pre + 1){
          pre = arr[i];
          if(count > count_sign) {
            pose_sign = pose;
            count_sign = count;
          }
          pose = i;
          count = 1;  
        }else{
          count++;
          pre = arr[i];
        }
    }
    if (count > count_sign) {
      pose_sign = pose;
      count_sign = count;
    }

    std::vector<int> ret;
    ret.reserve(count_sign);
    for(int i = 0; i < count_sign; i++){
      ret.emplace_back(arr[i+pose_sign]);
    }
    return ret;
}

int main()
{
  std::cout << "Talk is cheap. Show me the code." << std::endl;
  std::vector<int> arr{9, 3, 1, 4, 2, 3, 7, 6};
  auto ret = find_seq_arr(arr);
  for(auto elem:ret){
    std::cout << elem <<" ";
  }
  std::cout <<"\\n";
  return 0;
}""",
    },
]
