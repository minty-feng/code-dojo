/**
 * 哈希表实现（链地址法）
 */

#include <iostream>
#include <vector>
#include <list>
#include <string>
#include <stdexcept>

template<typename K, typename V>
class HashTable {
private:
    struct Entry {
        K key;
        V value;
        Entry(K k, V v) : key(k), value(v) {}
    };
    
    std::vector<std::list<Entry>> table;
    int size;
    int capacity;
    double load_factor_threshold;
    
    int hash(const K& key) const {
        return std::hash<K>{}(key) % capacity;
    }
    
    void resize() {
        int old_capacity = capacity;
        capacity *= 2;
        
        std::vector<std::list<Entry>> old_table = table;
        table = std::vector<std::list<Entry>>(capacity);
        size = 0;
        
        for (const auto& bucket : old_table) {
            for (const auto& entry : bucket) {
                insert(entry.key, entry.value);
            }
        }
    }

public:
    HashTable(int cap = 16) 
        : capacity(cap), size(0), load_factor_threshold(0.75) {
        table.resize(capacity);
    }
    
    void insert(const K& key, const V& value) {
        if ((double)size / capacity > load_factor_threshold) {
            resize();
        }
        
        int index = hash(key);
        auto& bucket = table[index];
        
        // 更新已存在的key
        for (auto& entry : bucket) {
            if (entry.key == key) {
                entry.value = value;
                return;
            }
        }
        
        // 插入新key
        bucket.push_back(Entry(key, value));
        size++;
    }
    
    V get(const K& key) const {
        int index = hash(key);
        const auto& bucket = table[index];
        
        for (const auto& entry : bucket) {
            if (entry.key == key) {
                return entry.value;
            }
        }
        
        throw std::runtime_error("Key not found");
    }
    
    void remove(const K& key) {
        int index = hash(key);
        auto& bucket = table[index];
        
        for (auto it = bucket.begin(); it != bucket.end(); ++it) {
            if (it->key == key) {
                bucket.erase(it);
                size--;
                return;
            }
        }
        
        throw std::runtime_error("Key not found");
    }
    
    bool contains(const K& key) const {
        try {
            get(key);
            return true;
        } catch (...) {
            return false;
        }
    }
    
    int getSize() const {
        return size;
    }
    
    void print() const {
        std::cout << "{";
        bool first = true;
        for (const auto& bucket : table) {
            for (const auto& entry : bucket) {
                if (!first) std::cout << ", ";
                std::cout << entry.key << ": " << entry.value;
                first = false;
            }
        }
        std::cout << "}" << std::endl;
    }
};


int main() {
    std::cout << "=== 哈希表演示 ===" << std::endl << std::endl;
    
    HashTable<std::string, int> ht(4);
    
    std::cout << "插入键值对:" << std::endl;
    ht.insert("apple", 5);
    std::cout << "  apple: 5" << std::endl;
    ht.insert("banana", 3);
    std::cout << "  banana: 3" << std::endl;
    ht.insert("orange", 7);
    std::cout << "  orange: 7" << std::endl;
    
    std::cout << "\n哈希表: ";
    ht.print();
    std::cout << "大小: " << ht.getSize() << std::endl << std::endl;
    
    std::cout << "查找 'apple': " << ht.get("apple") << std::endl;
    std::cout << "包含 'grape': " << (ht.contains("grape") ? "是" : "否") << std::endl << std::endl;
    
    std::cout << "更新 'apple' 为 10" << std::endl;
    ht.insert("apple", 10);
    std::cout << "哈希表: ";
    ht.print();
    std::cout << std::endl;
    
    std::cout << "删除 'banana'" << std::endl;
    ht.remove("banana");
    std::cout << "哈希表: ";
    ht.print();
    
    return 0;
}

