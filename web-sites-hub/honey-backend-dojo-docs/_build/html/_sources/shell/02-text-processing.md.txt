# 02-文本处理三剑客：grep、sed、awk

Linux文本处理三剑客：grep查找、sed编辑、awk分析。掌握这三个工具可解决90%的文本处理需求。

## grep - 文本搜索

grep（Global Regular Expression Print）用于搜索文本，支持正则表达式。

### 基本用法

```bash
# 基本搜索
grep "pattern" file.txt

# 忽略大小写
grep -i "pattern" file.txt

# 显示行号
grep -n "pattern" file.txt

# 反向匹配（不包含）
grep -v "pattern" file.txt

# 递归搜索目录
grep -r "pattern" /path/to/dir

# 只显示文件名
grep -l "pattern" *.txt

# 显示匹配行的上下文
grep -C 3 "pattern" file.txt   # 前后各3行
grep -A 2 "pattern" file.txt   # 后2行
grep -B 2 "pattern" file.txt   # 前2行

# 统计匹配行数
grep -c "pattern" file.txt

# 精确匹配整行
grep -x "exact line" file.txt

# 匹配整个单词
grep -w "word" file.txt
```

### 正则表达式

```bash
# 基本正则表达式（BRE）
grep "^start" file.txt     # 行首
grep "end$" file.txt       # 行尾
grep "^$" file.txt         # 空行
grep "." file.txt          # 任意字符
grep "a*" file.txt         # 0个或多个a
grep "[abc]" file.txt      # a、b或c
grep "[^abc]" file.txt     # 非a、b、c
grep "[0-9]" file.txt      # 数字
grep "[a-z]" file.txt      # 小写字母

# 扩展正则表达式（ERE，-E）
grep -E "a+" file.txt      # 1个或多个a
grep -E "a?" file.txt      # 0个或1个a
grep -E "a{3}" file.txt    # 恰好3个a
grep -E "a{2,5}" file.txt  # 2-5个a
grep -E "a{2,}" file.txt   # 至少2个a
grep -E "ab|cd" file.txt   # ab或cd
grep -E "(ab)+" file.txt   # 1个或多个ab

# Perl正则（-P，功能最强）
grep -P "\d+" file.txt     # 数字
grep -P "\w+" file.txt     # 字母数字下划线
grep -P "\s+" file.txt     # 空白字符
grep -P "(?<=@)\w+" file.txt  # 正向后查找
```

### 实战案例

```bash
# 查找IP地址
grep -E "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" file.txt

# 查找邮箱
grep -E "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" file.txt

# 查找URL
grep -E "https?://[^\s]+" file.txt

# 查找ERROR日志
grep -i "error" /var/log/syslog

# 排除注释行和空行
grep -v "^#" file.txt | grep -v "^$"

# 多模式搜索
grep -e "pattern1" -e "pattern2" file.txt
grep -E "pattern1|pattern2" file.txt

# 从文件读取模式
grep -f patterns.txt file.txt

# 统计代码行（排除空行和注释）
grep -v "^$" file.c | grep -v "^\s*//" | wc -l

# 查找进程
ps aux | grep nginx | grep -v grep

# 彩色高亮（默认）
grep --color=auto "pattern" file.txt
```

### grep变体

```bash
# egrep = grep -E（扩展正则）
egrep "a+" file.txt

# fgrep = grep -F（固定字符串，不解析正则）
fgrep "a*b" file.txt  # 搜索字面量 "a*b"

# zgrep（搜索压缩文件）
zgrep "pattern" file.gz
```

## sed - 流编辑器

sed（Stream Editor）逐行处理文本，支持查找、替换、删除、插入。

### 基本语法

```bash
sed [options] 'command' file

# -n：静默模式（只打印处理的行）
# -e：多个编辑命令
# -i：原地编辑（修改文件）
# -r/-E：扩展正则
```

### 替换（s命令）

```bash
# 基本替换（只替换每行第一个）
sed 's/old/new/' file.txt

# 全局替换（每行所有匹配）
sed 's/old/new/g' file.txt

# 替换第N个匹配
sed 's/old/new/2' file.txt  # 第2个

# 忽略大小写
sed 's/old/new/gi' file.txt

# 替换特定行
sed '3s/old/new/' file.txt       # 第3行
sed '2,5s/old/new/' file.txt     # 2-5行
sed '2,$s/old/new/' file.txt     # 2到末尾
sed '/pattern/s/old/new/' file.txt  # 匹配pattern的行

# 原地修改文件
sed -i 's/old/new/g' file.txt

# 备份后修改
sed -i.bak 's/old/new/g' file.txt

# 分隔符替换（避免转义/）
sed 's|/usr/bin|/usr/local/bin|g' file.txt
sed 's#old#new#g' file.txt

# 使用正则
sed -E 's/[0-9]+/NUMBER/g' file.txt

# 引用匹配内容（&）
sed 's/[0-9]\+/"&"/g' file.txt  # 123 → "123"

# 引用分组（\1, \2...）
sed -E 's/([a-z]+)@([a-z]+)/\2@\1/' file.txt  # user@host → host@user
```

### 删除（d命令）

```bash
# 删除特定行
sed '3d' file.txt           # 第3行
sed '2,5d' file.txt         # 2-5行
sed '2,$d' file.txt         # 2到末尾
sed '$d' file.txt           # 最后一行

# 删除匹配行
sed '/pattern/d' file.txt

# 删除空行
sed '/^$/d' file.txt

# 删除注释行
sed '/^#/d' file.txt

# 删除空行和注释
sed '/^$/d; /^#/d' file.txt
```

### 插入和追加

```bash
# a：在后面追加
sed '2a\new line' file.txt        # 第2行后
sed '/pattern/a\new line' file.txt  # 匹配行后

# i：在前面插入
sed '2i\new line' file.txt        # 第2行前
sed '/pattern/i\new line' file.txt  # 匹配行前

# c：替换整行
sed '2c\new line' file.txt
sed '/pattern/c\new line' file.txt
```

### 打印（p命令）

```bash
# 打印特定行（-n静默模式）
sed -n '3p' file.txt          # 第3行
sed -n '2,5p' file.txt        # 2-5行
sed -n '/pattern/p' file.txt  # 匹配行
sed -n '$p' file.txt          # 最后一行

# 打印并删除
sed -n '/pattern/p; /pattern/d' file.txt
```

### 多命令和分支

```bash
# -e 多命令
sed -e 's/old/new/g' -e '/pattern/d' file.txt

# ; 分隔
sed 's/old/new/g; /pattern/d' file.txt

# 脚本文件
sed -f script.sed file.txt

# script.sed 内容：
# s/old/new/g
# /pattern/d
```

### 实战案例

```bash
# 配置文件修改
sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config

# 添加配置
sed -i '/\[mysqld\]/a\max_connections=1000' /etc/my.cnf

# 替换变量
sed "s/@@VERSION@@/$VERSION/g" template.txt > output.txt

# 删除行尾空格
sed -i 's/[[:space:]]*$//' file.txt

# 删除Windows换行符
sed -i 's/\r$//' file.txt

# 在每行前加行号
sed = file.txt | sed 'N;s/\n/\t/'

# 大小写转换
echo "Hello" | sed 'y/a-z/A-Z/'  # HELLO

# 提取IP地址
ifconfig | sed -n '/inet /p' | sed 's/.*inet \([0-9.]*\).*/\1/'

# 批量重命名
for f in *.txt; do
    mv "$f" "$(echo $f | sed 's/\.txt$/.bak/')"
done

# HTML转义
sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g' file.html
```

### sed高级技巧

```bash
# 保持空间（h、H、g、G、x）
# h：复制模式空间到保持空间
# g：复制保持空间到模式空间
# x：交换

# 倒序输出（tac的实现）
sed '1!G;h;$!d' file.txt

# 删除重复行（uniq的实现）
sed '$!N; /^\(.*\)\n\1$/!P; D'

# 每两行合并
sed 'N;s/\n/ /' file.txt
```

## awk - 文本分析

awk是强大的文本分析工具，支持变量、数组、函数，类似小型编程语言。

### 基本语法

```bash
awk 'pattern {action}' file

# 内置变量
$0      # 整行
$1-$NF  # 第1到最后一列
NF      # 列数（字段数）
NR      # 行号（总）
FNR     # 行号（当前文件）
FS      # 输入分隔符（默认空格）
OFS     # 输出分隔符（默认空格）
RS      # 行分隔符（默认换行）
ORS     # 输出行分隔符
FILENAME # 当前文件名
```

### 基本用法

```bash
# 打印整行
awk '{print}' file.txt
awk '{print $0}' file.txt

# 打印特定列
awk '{print $1}' file.txt        # 第1列
awk '{print $1, $3}' file.txt    # 第1和第3列
awk '{print $1 "\t" $3}' file.txt  # 制表符分隔
awk '{print $NF}' file.txt       # 最后一列
awk '{print $(NF-1)}' file.txt   # 倒数第2列

# 打印行号
awk '{print NR, $0}' file.txt

# 自定义分隔符
awk -F: '{print $1}' /etc/passwd  # 冒号分隔
awk -F'[,:]' '{print $1}' file.txt  # 多个分隔符

# 输出分隔符
awk 'BEGIN{OFS=","} {print $1, $2}' file.txt

# 条件打印
awk '$3 > 100' file.txt          # 第3列>100
awk '/pattern/' file.txt         # 包含pattern
awk '!/pattern/' file.txt        # 不包含
awk 'NR==5' file.txt             # 第5行
awk 'NR>=2 && NR<=5' file.txt    # 2-5行
```

### 模式匹配

```bash
# 正则匹配
awk '/^[0-9]/' file.txt          # 数字开头
awk '/error/i' file.txt          # 忽略大小写
awk '$1 ~ /^a/' file.txt         # 第1列以a开头
awk '$1 !~ /^a/' file.txt        # 第1列不以a开头

# 范围匹配
awk '/start/,/end/' file.txt     # start到end之间

# 逻辑运算
awk '$1 == "root"' /etc/passwd
awk '$3 > 100 && $4 < 200' file.txt
awk '$1 == "Alice" || $1 == "Bob"' file.txt
```

### BEGIN和END

```bash
# BEGIN：处理前执行
awk 'BEGIN {print "Name\tAge"} {print}' file.txt

# END：处理后执行
awk '{sum += $1} END {print "Total:", sum}' file.txt

# 组合使用
awk 'BEGIN {print "Start"} {print} END {print "End"}' file.txt
```

### 运算和变量

```bash
# 算术运算
awk '{print $1 + $2}' file.txt
awk '{print $1 * 2}' file.txt
awk '{sum += $1} END {print sum}' file.txt

# 变量
awk '{count++} END {print count}' file.txt
awk 'BEGIN {total=0} {total += $1} END {print total/NR}' file.txt

# 数组
awk '{arr[$1]++} END {for (i in arr) print i, arr[i]}' file.txt

# 统计
awk '{sum += $1; sumsq += $1*$1}
     END {print "Avg:", sum/NR, "StdDev:", sqrt(sumsq/NR - (sum/NR)^2)}' file.txt
```

### 格式化输出

```bash
# printf
awk '{printf "%s\t%d\n", $1, $2}' file.txt
awk '{printf "%-10s %5d\n", $1, $2}' file.txt  # 左对齐、右对齐
awk '{printf "%.2f\n", $1}' file.txt  # 保留2位小数
```

### 条件和循环

```bash
# if语句
awk '{if ($3 > 100) print $1}' file.txt
awk '{if ($1 == "Alice") print $0; else print "Not Alice"}' file.txt

# for循环
awk '{for (i=1; i<=NF; i++) print $i}' file.txt

# while循环
awk '{i=1; while (i<=NF) {print $i; i++}}' file.txt
```

### 函数

```bash
# 字符串函数
length($1)           # 长度
substr($1, 1, 3)     # 截取（从1开始，长度3）
index($1, "a")       # 查找位置
split($0, arr, ",")  # 分割
sub(/old/, "new")    # 替换第一个
gsub(/old/, "new")   # 替换所有
tolower($1)          # 转小写
toupper($1)          # 转大写

# 数学函数
int($1)              # 取整
sqrt($1)             # 平方根
rand()               # 随机数[0,1)
srand()              # 设置随机种子

# 示例
awk '{print tolower($1)}' file.txt
awk '{print length($1)}' file.txt
```

### 实战案例

```bash
# 统计文件大小
ls -l | awk '{sum += $5} END {print "Total:", sum/1024/1024, "MB"}'

# 统计日志
awk '{status[$9]++} END {for (s in status) print s, status[s]}' access.log

# 提取第N列
awk -F: '{print $1}' /etc/passwd

# 去重统计
awk '{arr[$1]++} END {for (i in arr) print i, arr[i]}' file.txt

# 计算平均值
awk '{sum += $1} END {print sum/NR}' file.txt

# Top N
awk '{print $1}' file.txt | sort -rn | head -10

# 合并列
awk '{print $1 $2 $3}' file.txt

# 条件求和
awk '$2 == "error" {count++; sum += $3} END {print count, sum}' log.txt

# 多文件处理
awk '{print FILENAME, $0}' file1.txt file2.txt

# 处理CSV
awk -F, '{print $1, $3}' data.csv

# JSON提取（简单）
echo '{"name":"Alice","age":25}' | awk -F'"' '{print $4}'

# 生成SQL
awk '{printf "INSERT INTO users VALUES (\"%s\", %d);\n", $1, $2}' data.txt

# 日志分析：统计状态码
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# 计算第95百分位
awk '{arr[NR]=$1} END {
    asort(arr);
    idx = int(NR * 0.95);
    print "P95:", arr[idx]
}' data.txt

# 过滤时间范围
awk '$1 >= "2023-01-01" && $1 <= "2023-12-31"' log.txt

# 格式化表格
awk 'BEGIN {printf "%-10s %-10s %10s\n", "Name", "Age", "Score"}
     {printf "%-10s %-10d %10.2f\n", $1, $2, $3}' data.txt
```

### awk脚本文件

```bash
# script.awk
BEGIN {
    FS = ","
    OFS = "\t"
    print "Name\tScore"
}

{
    if ($2 >= 60) {
        pass++
        total += $2
    }
}

END {
    print "Pass:", pass
    print "Average:", total/pass
}

# 执行
awk -f script.awk data.csv
```

## 三剑客组合使用

### 管道组合

```bash
# 统计错误日志
grep "ERROR" app.log | awk '{print $1}' | sort | uniq -c

# 提取IP并统计
grep "Failed password" /var/log/auth.log | \
    awk '{print $11}' | \
    sort | uniq -c | sort -rn

# 日志分析
cat access.log | \
    grep "404" | \
    awk '{print $7}' | \
    sort | uniq -c | \
    sort -rn | \
    head -10

# 替换后过滤
sed 's/old/new/g' file.txt | grep "new" | awk '{print $1}'

# 多步处理
cat data.txt | \
    grep -v "^#" | \           # 删除注释
    grep -v "^$" | \           # 删除空行
    sed 's/  */ /g' | \        # 多空格转单空格
    awk '{print $1, $3}' | \   # 提取列
    sort -k2 -n                # 按第2列排序
```

### 实战脚本

```bash
#!/bin/bash
# 分析Nginx访问日志

LOG_FILE="/var/log/nginx/access.log"

echo "=== Top 10 IP ==="
awk '{print $1}' $LOG_FILE | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== Top 10 URL ==="
awk '{print $7}' $LOG_FILE | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== Status Code Statistics ==="
awk '{print $9}' $LOG_FILE | sort | uniq -c | sort -rn

echo ""
echo "=== 4xx and 5xx Errors ==="
awk '$9 ~ /^[45]/ {print $0}' $LOG_FILE | wc -l

echo ""
echo "=== Traffic by Hour ==="
awk '{print substr($4, 14, 2)}' $LOG_FILE | sort | uniq -c
```

## 性能对比

| 任务 | grep | sed | awk | 说明 |
|------|------|-----|-----|------|
| 简单搜索 | ⭐⭐⭐ | ⭐ | ⭐ | grep最快 |
| 替换 | ✗ | ⭐⭐⭐ | ⭐⭐ | sed专用 |
| 列提取 | ✗ | ⭐ | ⭐⭐⭐ | awk最强 |
| 统计计算 | ✗ | ✗ | ⭐⭐⭐ | awk专用 |
| 复杂逻辑 | ✗ | ⭐ | ⭐⭐⭐ | awk最灵活 |

## 最佳实践

### 选择工具

```bash
# 仅搜索：grep
grep "error" app.log

# 简单替换：sed
sed 's/old/new/g' file.txt

# 列处理/统计：awk
awk '{sum += $3} END {print sum}' data.txt

# 复杂处理：awk脚本
awk -f complex.awk data.txt
```

### 性能优化

```bash
# grep: 使用固定字符串（-F）
grep -F "literal string" file.txt  # 比正则快

# sed: 减少正则复杂度
sed 's/[0-9]\+/NUM/g'  # 比 's/[0-9][0-9]*/NUM/g' 快

# awk: 提前退出
awk '{if (NR > 1000) exit} {print}' huge.txt

# 避免不必要的管道
awk '/pattern/ {print $1}' file.txt  # 优于 grep pattern | awk '{print $1}'
```

### 可读性

```bash
# 复杂命令分行
grep "ERROR" app.log | \
    awk '{print $1, $5}' | \
    sort | \
    uniq -c

# 注释
awk '
    # 统计每个状态码的出现次数
    {status[$9]++}
    
    # 输出统计结果
    END {for (s in status) print s, status[s]}
' access.log
```

**核心：** grep查、sed改、awk析，熟练掌握三剑客是Linux运维的必备技能。

