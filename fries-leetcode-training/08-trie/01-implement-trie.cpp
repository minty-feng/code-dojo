/**
 * LeetCode 208. 实现Trie
 * https://leetcode.cn/problems/implement-trie-prefix-tree/
 * 
 * Trie（发音类似"try"）或者说前缀树是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。
 * 
 * Trie
 * 
 * 时间复杂度：O(m) m为字符串长度
 * 空间复杂度：O(ALPHABET_SIZE * N * M) N为键的数量，M为键的长度
 */

class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    bool is_end;
    
    TrieNode() : is_end(false) {}
};

class Trie {
private:
    TrieNode* root;
    
public:
    Trie() {
        root = new TrieNode();
    }
    
    void insert(string word) {
        TrieNode* node = root;
        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
        }
        node->is_end = true;
    }
    
    bool search(string word) {
        TrieNode* node = root;
        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                return false;
            }
            node = node->children[c];
        }
        return node->is_end;
    }
    
    bool startsWith(string prefix) {
        TrieNode* node = root;
        for (char c : prefix) {
            if (node->children.find(c) == node->children.end()) {
                return false;
            }
            node = node->children[c];
        }
        return true;
    }
};

// 测试函数
#include <iostream>
#include <unordered_map>
using namespace std;

void testTrie() {
    Trie trie;
    
    // 插入单词
    trie.insert("apple");
    trie.insert("app");
    trie.insert("application");
    
    // 测试搜索
    cout << "搜索 'app': " << (trie.search("app") ? "True" : "False") << endl;        // 期望: True
    cout << "搜索 'apple': " << (trie.search("apple") ? "True" : "False") << endl;    // 期望: True
    cout << "搜索 'appl': " << (trie.search("appl") ? "True" : "False") << endl;      // 期望: False
    
    // 测试前缀
    cout << "前缀 'app': " << (trie.startsWith("app") ? "True" : "False") << endl;     // 期望: True
    cout << "前缀 'appl': " << (trie.startsWith("appl") ? "True" : "False") << endl;  // 期望: True
    cout << "前缀 'xyz': " << (trie.startsWith("xyz") ? "True" : "False") << endl;    // 期望: False
}

int main() {
    testTrie();
    return 0;
}
