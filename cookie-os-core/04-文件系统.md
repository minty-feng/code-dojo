# 文件系统

## 💡 核心结论

1. **inode存储文件元数据，数据块存储文件内容**
2. **目录是特殊的文件，存储文件名到inode的映射**
3. **硬链接共享inode，软链接是独立文件存储路径**
4. **日志文件系统通过预写日志保证一致性**
5. **缓存和预读是文件系统性能的关键**

---

## 1. 文件系统结构

### 1.1 磁盘布局

```
典型文件系统布局（如ext2/3/4）:

┌──────────────┬──────────┬──────────┬──────────┬──────────┐
│  Boot Block  │  Super   │  inode   │  Data    │  Data    │
│   (1 block)  │  Block   │  Bitmap  │  Bitmap  │  Blocks  │
└──────────────┴──────────┴──────────┴──────────┴──────────┘

Boot Block:  启动信息
Super Block: 文件系统元信息
inode Bitmap: inode使用情况
Data Bitmap:  数据块使用情况
Data Blocks:  实际数据
```

### 1.2 超级块（Super Block）

```c
struct ext2_super_block {
    __u32 s_inodes_count;      // inode总数
    __u32 s_blocks_count;      // 块总数
    __u32 s_free_blocks_count; // 空闲块数
    __u32 s_free_inodes_count; // 空闲inode数
    __u32 s_first_data_block;  // 第一个数据块
    __u32 s_log_block_size;    // 块大小（1024 << s_log_block_size）
    __u32 s_blocks_per_group;  // 每组块数
    __u32 s_inodes_per_group;  // 每组inode数
    __u32 s_mtime;             // 挂载时间
    __u32 s_wtime;             // 写入时间
    __u16 s_magic;             // 魔数（0xEF53）
    __u16 s_state;             // 文件系统状态
    // ... 更多字段
};
```

---

## 2. inode结构

### 2.1 inode定义

**inode（索引节点）**：存储文件元数据

```c
struct ext2_inode {
    __u16 i_mode;        // 文件类型和权限
    __u16 i_uid;         // 所有者用户ID
    __u32 i_size;        // 文件大小（字节）
    __u32 i_atime;       // 访问时间
    __u32 i_ctime;       // 创建时间
    __u32 i_mtime;       // 修改时间
    __u32 i_dtime;       // 删除时间
    __u16 i_gid;         // 组ID
    __u16 i_links_count; // 硬链接计数
    __u32 i_blocks;      // 块数
    __u32 i_flags;       // 标志
    
    // 数据块指针（关键！）
    __u32 i_block[15];   // 块指针数组
    // [0-11]: 直接指针
    // [12]:   一级间接指针
    // [13]:   二级间接指针
    // [14]:   三级间接指针
};
```

### 2.2 数据块索引

```
i_block[15]数组：

[0-11]: 直接指针 → 数据块
        12个块 × 4KB = 48KB

[12]: 一级间接指针 → 指针块 → 数据块
      1024个指针 × 4KB = 4MB

[13]: 二级间接指针 → 指针块 → 指针块 → 数据块
      1024 × 1024 × 4KB = 4GB

[14]: 三级间接指针
      1024 × 1024 × 1024 × 4KB = 4TB

最大文件大小 ≈ 4TB
```

**查找数据块示例**：
```c
// 读取文件偏移offset处的数据
int get_block_num(struct inode *inode, int offset) {
    int block_size = 4096;
    int block_index = offset / block_size;
    int ptrs_per_block = block_size / 4;  // 每块1024个指针
    
    if (block_index < 12) {
        // 直接块
        return inode->i_block[block_index];
    }
    
    block_index -= 12;
    if (block_index < ptrs_per_block) {
        // 一级间接块
        int *indirect = read_block(inode->i_block[12]);
        return indirect[block_index];
    }
    
    block_index -= ptrs_per_block;
    if (block_index < ptrs_per_block * ptrs_per_block) {
        // 二级间接块
        int level1_index = block_index / ptrs_per_block;
        int level2_index = block_index % ptrs_per_block;
        
        int *indirect1 = read_block(inode->i_block[13]);
        int *indirect2 = read_block(indirect1[level1_index]);
        return indirect2[level2_index];
    }
    
    // 三级间接块...
}
```

---

## 3. 目录结构

### 3.1 目录项

**目录也是文件**，内容是目录项列表

```c
struct ext2_dir_entry {
    __u32 inode;          // inode号
    __u16 rec_len;        // 记录长度
    __u8  name_len;       // 文件名长度
    __u8  file_type;      // 文件类型
    char  name[255];      // 文件名
};
```

**目录示例**：
```
目录inode: 10
数据块内容:
  [inode=12, name="file1.txt"]
  [inode=13, name="file2.txt"]
  [inode=14, name="subdir"]
```

### 3.2 路径解析

```c
int path_lookup(const char *path) {
    int current_inode = root_inode;  // 从根目录开始
    
    char *token = strtok(path, "/");
    while (token != NULL) {
        // 1. 读取当前目录的数据块
        struct ext2_inode *dir = read_inode(current_inode);
        char *dir_data = read_block(dir->i_block[0]);
        
        // 2. 查找目录项
        struct ext2_dir_entry *entry = find_entry(dir_data, token);
        if (!entry) {
            return -ENOENT;  // 文件不存在
        }
        
        // 3. 进入下一级
        current_inode = entry->inode;
        token = strtok(NULL, "/");
    }
    
    return current_inode;
}
```

**路径查找示例**：
```
查找路径: /home/user/file.txt

1. 从根inode (2) 开始
2. 读取根目录，查找"home" → inode 100
3. 读取inode 100，查找"user" → inode 200
4. 读取inode 200，查找"file.txt" → inode 300
5. 返回inode 300
```

---

## 4. 硬链接 vs 软链接

### 4.1 硬链接

**原理**：多个目录项指向同一个inode

```bash
# 创建硬链接
$ ln file.txt hardlink.txt

# inode相同
$ ls -i
12345 file.txt
12345 hardlink.txt
```

```c
int create_hard_link(const char *oldpath, const char *newpath) {
    // 1. 获取原文件inode
    int inode_num = path_lookup(oldpath);
    
    // 2. 在新目录中创建目录项
    int dir_inode = path_lookup(dirname(newpath));
    add_dir_entry(dir_inode, basename(newpath), inode_num);
    
    // 3. 增加硬链接计数
    struct inode *inode = read_inode(inode_num);
    inode->i_links_count++;
    write_inode(inode);
    
    return 0;
}
```

**特点**：
- 共享inode和数据
- 删除一个链接，文件仍存在
- 不能跨文件系统
- 不能链接目录

### 4.2 软链接（符号链接）

**原理**：独立的文件，内容是目标路径

```bash
# 创建软链接
$ ln -s file.txt symlink.txt

# inode不同
$ ls -i
12345 file.txt
67890 symlink.txt
```

```c
int create_symlink(const char *target, const char *linkpath) {
    // 1. 创建新inode
    int inode_num = alloc_inode();
    struct inode *inode = read_inode(inode_num);
    
    // 2. 设置类型为符号链接
    inode->i_mode = S_IFLNK | 0777;
    
    // 3. 存储目标路径
    strcpy(inode->i_block, target);  // 路径存在i_block中
    inode->i_size = strlen(target);
    
    // 4. 在目录中添加目录项
    int dir_inode = path_lookup(dirname(linkpath));
    add_dir_entry(dir_inode, basename(linkpath), inode_num);
    
    return 0;
}
```

**特点**：
- 独立文件
- 可以跨文件系统
- 可以链接目录
- 目标删除后变成悬空链接

### 4.3 对比

| 特性 | 硬链接 | 软链接 |
|------|--------|--------|
| inode | 相同 | 不同 |
| 跨文件系统 | 否 | 是 |
| 链接目录 | 否 | 是 |
| 原文件删除 | 仍可访问 | 悬空 |
| 磁盘空间 | 共享 | 独立（路径） |

---

## 5. 文件操作

### 5.1 文件创建

```c
int create_file(const char *path, mode_t mode) {
    // 1. 分配inode
    int inode_num = alloc_inode();
    struct inode *inode = get_inode(inode_num);
    
    // 2. 初始化inode
    inode->i_mode = mode;
    inode->i_uid = current_uid();
    inode->i_gid = current_gid();
    inode->i_size = 0;
    inode->i_atime = inode->i_mtime = inode->i_ctime = time(NULL);
    inode->i_links_count = 1;
    inode->i_blocks = 0;
    
    // 3. 在父目录添加目录项
    int dir_inode = path_lookup(dirname(path));
    add_dir_entry(dir_inode, basename(path), inode_num);
    
    return inode_num;
}
```

### 5.2 文件读取

```c
ssize_t file_read(int fd, void *buf, size_t count, off_t offset) {
    struct file *file = get_file(fd);
    struct inode *inode = file->f_inode;
    
    // 1. 计算读取范围
    if (offset >= inode->i_size) {
        return 0;  // EOF
    }
    
    size_t to_read = min(count, inode->i_size - offset);
    size_t bytes_read = 0;
    
    // 2. 逐块读取
    while (bytes_read < to_read) {
        int block_num = get_block_num(inode, offset + bytes_read);
        char *block_data = read_block(block_num);
        
        int block_offset = (offset + bytes_read) % BLOCK_SIZE;
        int copy_len = min(BLOCK_SIZE - block_offset, to_read - bytes_read);
        
        memcpy(buf + bytes_read, block_data + block_offset, copy_len);
        bytes_read += copy_len;
    }
    
    // 3. 更新访问时间
    inode->i_atime = time(NULL);
    
    return bytes_read;
}
```

### 5.3 文件写入

```c
ssize_t file_write(int fd, const void *buf, size_t count, off_t offset) {
    struct file *file = get_file(fd);
    struct inode *inode = file->f_inode;
    
    size_t bytes_written = 0;
    
    while (bytes_written < count) {
        // 1. 获取或分配数据块
        int block_num = get_block_num(inode, offset + bytes_written);
        if (block_num == 0) {
            block_num = alloc_block();
            set_block_num(inode, offset + bytes_written, block_num);
        }
        
        // 2. 写入数据
        char *block_data = read_block(block_num);
        int block_offset = (offset + bytes_written) % BLOCK_SIZE;
        int copy_len = min(BLOCK_SIZE - block_offset, count - bytes_written);
        
        memcpy(block_data + block_offset, buf + bytes_written, copy_len);
        write_block(block_num, block_data);
        
        bytes_written += copy_len;
    }
    
    // 3. 更新inode
    if (offset + bytes_written > inode->i_size) {
        inode->i_size = offset + bytes_written;
    }
    inode->i_mtime = inode->i_ctime = time(NULL);
    
    return bytes_written;
}
```

### 5.4 文件删除

```c
int delete_file(const char *path) {
    // 1. 获取inode
    int inode_num = path_lookup(path);
    struct inode *inode = read_inode(inode_num);
    
    // 2. 从父目录删除目录项
    int dir_inode = path_lookup(dirname(path));
    remove_dir_entry(dir_inode, basename(path));
    
    // 3. 减少硬链接计数
    inode->i_links_count--;
    
    // 4. 如果没有链接了，释放资源
    if (inode->i_links_count == 0) {
        // 释放数据块
        for (int i = 0; i < inode->i_blocks / 8; i++) {
            int block_num = get_block_num(inode, i * BLOCK_SIZE);
            free_block(block_num);
        }
        
        // 释放inode
        free_inode(inode_num);
    }
    
    return 0;
}
```

---

## 6. 缓存机制

### 6.1 页缓存（Page Cache）

**原理**：将磁盘数据缓存在内存中

```c
struct page_cache {
    struct rb_root pages;      // 红黑树索引
    spinlock_t lock;
};

struct cached_page {
    unsigned long index;       // 页索引
    struct page *page;         // 物理页
    int dirty;                 // 是否修改
    struct rb_node rb_node;
};

void *read_with_cache(struct inode *inode, off_t offset) {
    unsigned long page_index = offset / PAGE_SIZE;
    
    // 1. 查找缓存
    struct cached_page *cp = find_cached_page(inode, page_index);
    if (cp) {
        // 缓存命中
        return cp->page->data + (offset % PAGE_SIZE);
    }
    
    // 2. 缓存未命中，从磁盘读取
    struct page *page = alloc_page();
    read_from_disk(inode, page_index, page->data);
    
    // 3. 加入缓存
    add_to_cache(inode, page_index, page);
    
    return page->data + (offset % PAGE_SIZE);
}
```

### 6.2 预读（Read-ahead）

```c
void readahead(struct file *file, off_t offset, size_t count) {
    // 预读后续N个页面
    int ra_pages = 16;  // 预读16个页面
    
    for (int i = 1; i <= ra_pages; i++) {
        off_t ra_offset = offset + i * PAGE_SIZE;
        if (ra_offset >= file->f_inode->i_size) {
            break;
        }
        
        // 异步读取到缓存
        async_read_to_cache(file->f_inode, ra_offset);
    }
}
```

### 6.3 脏页回写

```c
void flush_dirty_pages() {
    struct list_head *dirty_list = get_dirty_pages();
    
    list_for_each_entry(page, dirty_list, list) {
        // 写回磁盘
        write_to_disk(page->inode, page->index, page->data);
        
        // 标记为干净
        page->dirty = 0;
    }
}

// 定期刷新（每30秒）
void pdflush_thread() {
    while (1) {
        sleep(30);
        flush_dirty_pages();
    }
}
```

---

## 7. 日志文件系统

### 7.1 一致性问题

**问题**：系统崩溃可能导致文件系统不一致

```
场景：创建文件
1. 在目录中添加目录项
2. 分配inode
3. 写入数据

如果在步骤2后崩溃：
- 目录项存在，但inode未分配
- 文件系统不一致！
```

### 7.2 日志机制

**原理**：先写日志，再写数据

```c
struct journal_entry {
    int transaction_id;
    int type;  // BEGIN, COMMIT, ABORT
    // 操作内容
};

void journaled_create(const char *path) {
    int tid = begin_transaction();
    
    // 1. 写日志
    write_journal(tid, BEGIN);
    write_journal(tid, "allocate inode");
    write_journal(tid, "add dir entry");
    write_journal(tid, "write data");
    write_journal(tid, COMMIT);
    
    // 2. 执行实际操作
    int inode = alloc_inode();
    add_dir_entry(path, inode);
    write_data(inode, data);
    
    // 3. 标记日志完成
    write_journal(tid, DONE);
}
```

**恢复过程**：
```c
void recover() {
    for (transaction in journal) {
        if (transaction.state == COMMIT && 
            transaction.state != DONE) {
            // 重做未完成的事务
            redo_transaction(transaction);
        } else if (transaction.state == BEGIN &&
                   transaction.state != COMMIT) {
            // 回滚未提交的事务
            undo_transaction(transaction);
        }
    }
}
```

---

## 8. 磁盘调度

### 8.1 FCFS（先来先服务）

```c
void fcfs_schedule(request_queue *queue) {
    while (!queue_empty(queue)) {
        request *req = dequeue(queue);
        seek_to(req->sector);
        read_or_write(req);
    }
}
```

### 8.2 SSTF（最短寻道时间优先）

```c
void sstf_schedule(request_queue *queue, int current_pos) {
    while (!queue_empty(queue)) {
        // 选择距离当前位置最近的请求
        request *closest = find_closest(queue, current_pos);
        seek_to(closest->sector);
        read_or_write(closest);
        current_pos = closest->sector;
    }
}
```

### 8.3 SCAN（电梯算法）

```c
void scan_schedule(request_queue *queue) {
    int direction = UP;  // 向上扫描
    int current = 0;
    
    while (!queue_empty(queue)) {
        if (direction == UP) {
            request *req = get_next_higher(queue, current);
            if (req) {
                seek_to(req->sector);
                current = req->sector;
            } else {
                direction = DOWN;  // 到达顶端，反向
            }
        } else {
            request *req = get_next_lower(queue, current);
            if (req) {
                seek_to(req->sector);
                current = req->sector;
            } else {
                direction = UP;  // 到达底端，反向
            }
        }
    }
}
```

---

## 9. 常见问题

### Q1: 为什么需要inode？
**A**: 
- 分离文件名和元数据
- 支持硬链接
- 快速查找文件属性
- 灵活的权限管理

### Q2: 目录可以有硬链接吗？
**A**: 
- 不可以（会导致循环）
- 只有`.`和`..`是特殊的硬链接
- 可以创建目录的软链接

### Q3: 如何提高文件系统性能？
**A**:
1. 页缓存
2. 预读
3. 延迟写入
4. inode缓存
5. 目录缓存

### Q4: ext4比ext3好在哪里？
**A**:
- 更大文件和文件系统支持
- Extent代替间接块（连续分配）
- 延迟分配
- 日志校验和
- 在线碎片整理

---

## 参考资源

- 《Operating Systems: Three Easy Pieces》- File Systems章节
- Linux源码：`fs/ext4/`, `fs/inode.c`
- ext4文档：Documentation/filesystems/ext4.txt
- 《Unix文件系统剖析》

