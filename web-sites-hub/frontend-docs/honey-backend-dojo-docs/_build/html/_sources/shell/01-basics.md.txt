# 01-Shell基础

Shell是Linux/Unix的命令解释器，既是用户界面也是编程语言。Shell脚本是运维自动化的核心工具。

## Shell简介

### 常见Shell类型

```bash
# 查看可用Shell
cat /etc/shells

# 常见Shell
/bin/sh        # Bourne Shell（POSIX标准）
/bin/bash      # Bourne Again Shell（最流行）
/bin/zsh       # Z Shell（macOS默认）
/bin/fish      # Friendly Interactive Shell
/bin/dash      # Debian Almquist Shell（轻量）

# 查看当前Shell
echo $SHELL

# 查看脚本使用的Shell
ps -p $$
```

### Bash vs Zsh

| 特性 | Bash | Zsh |
|------|------|-----|
| 兼容性 | POSIX兼容，广泛支持 | Bash兼容+增强 |
| 补全 | 基础补全 | 智能补全，路径展开 |
| 主题 | 无内置 | Oh My Zsh丰富主题 |
| 性能 | 启动快 | 稍慢但功能强 |
| 默认系统 | 大部分Linux | macOS 10.15+ |

## 第一个Shell脚本

### 基本结构

```bash
#!/bin/bash
# 这是注释
# Shebang指定解释器

echo "Hello, Shell!"

# 执行权限
chmod +x script.sh
./script.sh

# 或直接用bash执行
bash script.sh
```

### Shebang详解

```bash
#!/bin/bash              # 使用bash
#!/bin/sh                # 使用sh（可能是bash或dash）
#!/usr/bin/env bash      # 推荐：自动查找bash路径
#!/usr/bin/env python3   # Python脚本
```

## 变量

### 变量定义和使用

```bash
# 定义变量（=两边无空格）
name="Alice"
age=25
readonly PI=3.14159  # 只读变量

# 使用变量
echo $name
echo ${name}         # 推荐：明确边界
echo "Hello, $name"
echo 'Hello, $name'  # 单引号不解析变量

# 变量拼接
fullname="${name} Smith"

# 删除变量
unset name
```

### 特殊变量

```bash
$0      # 脚本名
$1-$9   # 第1-9个参数
${10}   # 第10个及以上参数
$#      # 参数个数
$@      # 所有参数（分开）
$*      # 所有参数（合并）
$?      # 上一命令退出状态（0=成功）
$$      # 当前Shell的PID
$!      # 最后一个后台进程的PID

# 示例
#!/bin/bash
echo "脚本名: $0"
echo "第一个参数: $1"
echo "参数个数: $#"
echo "所有参数: $@"
echo "退出状态: $?"

# 执行：./script.sh arg1 arg2
```

### 变量作用域

```bash
# 局部变量（当前Shell）
name="local"

# 环境变量（子进程可见）
export PATH=$PATH:/usr/local/bin

# 函数内局部变量
function test() {
    local var="local"  # 仅函数内可见
    global="global"    # 全局
}
```

### 命令替换

```bash
# 反引号（旧）
result=`date`

# $() 推荐
result=$(date)
count=$(ls | wc -l)

# 示例
today=$(date +%Y-%m-%d)
echo "Today is $today"
```

## 数据类型

### 字符串

```bash
# 单引号：原样输出
str='Hello $USER'  # 输出：Hello $USER

# 双引号：解析变量
str="Hello $USER"  # 输出：Hello alice

# 字符串长度
echo ${#str}

# 字符串截取
str="Hello World"
echo ${str:0:5}    # Hello（从0开始，长度5）
echo ${str:6}      # World（从6到末尾）

# 字符串替换
echo ${str/World/Shell}  # 替换第一个
echo ${str//o/O}         # 替换所有

# 字符串删除
file="script.sh.bak"
echo ${file%.bak}        # script.sh（删除最短后缀）
echo ${file%.*}          # script.sh（删除最短.后缀）
echo ${file%%.*}         # script（删除最长.后缀）
echo ${file#script.}     # sh.bak（删除最短前缀）

# 字符串拼接
str1="Hello"
str2="World"
result="$str1 $str2"
result="${str1}${str2}"
```

### 数组

```bash
# 定义数组
arr=(1 2 3 4 5)
arr[0]=10

# 访问元素
echo ${arr[0]}     # 第一个元素
echo ${arr[@]}     # 所有元素
echo ${arr[*]}     # 所有元素（合并）
echo ${#arr[@]}    # 数组长度

# 切片
echo ${arr[@]:1:3} # 从索引1开始，3个元素

# 添加元素
arr+=(6 7 8)

# 遍历数组
for item in "${arr[@]}"; do
    echo $item
done

# 关联数组（Bash 4+）
declare -A map
map["name"]="Alice"
map["age"]=25

echo ${map["name"]}
echo ${!map[@]}    # 所有键
echo ${map[@]}     # 所有值
```

## 运算符

### 算术运算

```bash
# let命令
let a=5+3
let "a = 5 + 3"

# (()) 推荐
a=$((5 + 3))
((a++))
((a += 5))

# expr（旧）
a=`expr 5 + 3`

# 运算符
$((a + b))   # 加
$((a - b))   # 减
$((a * b))   # 乘
$((a / b))   # 除
$((a % b))   # 取模
$((a ** b))  # 幂

# 自增自减
((i++))
((i--))
((++i))
((--i))

# 示例
num=10
result=$((num * 2 + 5))
echo $result  # 25
```

### 比较运算

```bash
# 整数比较
-eq   # 等于
-ne   # 不等于
-gt   # 大于
-ge   # 大于等于
-lt   # 小于
-le   # 小于等于

# 示例
if [ $a -eq $b ]; then
    echo "equal"
fi

# (()) 支持 C 风格
if ((a == b)); then
    echo "equal"
fi

# 字符串比较
=     # 等于（或 ==）
!=    # 不等于
-z    # 字符串为空
-n    # 字符串非空
<     # 小于（需转义）
>     # 大于（需转义）

# 示例
if [ "$str1" = "$str2" ]; then
    echo "equal"
fi

if [ -z "$str" ]; then
    echo "empty"
fi

# 文件测试
-e file   # 文件存在
-f file   # 常规文件
-d file   # 目录
-r file   # 可读
-w file   # 可写
-x file   # 可执行
-s file   # 文件非空
-L file   # 符号链接

# 示例
if [ -f "file.txt" ]; then
    echo "file exists"
fi
```

### 逻辑运算

```bash
# [ ] 中
-a    # AND
-o    # OR
!     # NOT

if [ $a -gt 0 -a $b -gt 0 ]; then
    echo "both positive"
fi

# [[ ]] 中（推荐）
&&    # AND
||    # OR
!     # NOT

if [[ $a > 0 && $b > 0 ]]; then
    echo "both positive"
fi

# 命令级
cmd1 && cmd2  # cmd1成功才执行cmd2
cmd1 || cmd2  # cmd1失败才执行cmd2

# 示例
[ -f file.txt ] && cat file.txt
[ -f file.txt ] || touch file.txt
```

## 输入输出

### echo vs printf

```bash
# echo：简单输出
echo "Hello World"
echo -n "no newline"    # 不换行
echo -e "tab:\t newline:\n"  # 解析转义

# printf：格式化输出（推荐）
printf "Name: %s, Age: %d\n" "Alice" 25
printf "%10s %5d\n" "Alice" 25  # 右对齐
printf "%-10s %-5d\n" "Alice" 25  # 左对齐
printf "%.2f\n" 3.14159  # 保留2位小数
```

### 读取输入

```bash
# read命令
read name
read -p "Enter name: " name       # 提示符
read -s password                  # 隐藏输入
read -t 5 name                    # 5秒超时
read -n 1 key                     # 读1个字符
read -a arr                       # 读入数组

# 读取文件
while IFS= read -r line; do
    echo "$line"
done < file.txt

# 读取多个变量
read -p "Enter name and age: " name age
```

### 重定向

```bash
# 输出重定向
cmd > file      # 覆盖写入
cmd >> file     # 追加写入
cmd 2> error.log     # 错误输出
cmd > output.log 2>&1  # 合并标准输出和错误
cmd &> all.log       # 合并（简写）

# 输入重定向
cmd < file      # 从文件读取
cmd << EOF      # Here Document
line1
line2
EOF

cmd <<< "string"  # Here String

# 管道
cmd1 | cmd2     # cmd1的输出作为cmd2的输入
ls -l | grep ".sh" | wc -l

# /dev/null（黑洞）
cmd > /dev/null      # 丢弃输出
cmd 2> /dev/null     # 丢弃错误
cmd &> /dev/null     # 全丢弃
```

## 流程控制

### if语句

```bash
# 基本语法
if [ condition ]; then
    commands
elif [ condition ]; then
    commands
else
    commands
fi

# 示例
if [ $1 -gt 100 ]; then
    echo "greater than 100"
elif [ $1 -gt 50 ]; then
    echo "greater than 50"
else
    echo "less than or equal 50"
fi

# [[ ]] 增强（支持正则、通配符）
if [[ $str =~ ^[0-9]+$ ]]; then
    echo "number"
fi

if [[ $file == *.sh ]]; then
    echo "shell script"
fi

# 多条件
if [ -f file.txt ] && [ -r file.txt ]; then
    cat file.txt
fi
```

### case语句

```bash
case $var in
    pattern1)
        commands
        ;;
    pattern2|pattern3)
        commands
        ;;
    *)
        default commands
        ;;
esac

# 示例
case $1 in
    start)
        echo "Starting..."
        ;;
    stop)
        echo "Stopping..."
        ;;
    restart)
        echo "Restarting..."
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

# 通配符
case $file in
    *.sh)
        echo "Shell script"
        ;;
    *.py)
        echo "Python script"
        ;;
    *)
        echo "Unknown type"
        ;;
esac
```

### for循环

```bash
# 遍历列表
for item in 1 2 3 4 5; do
    echo $item
done

# 遍历数组
for item in "${arr[@]}"; do
    echo $item
done

# 遍历文件
for file in *.sh; do
    echo $file
done

# C风格
for ((i=0; i<10; i++)); do
    echo $i
done

# 遍历命令输出
for user in $(cat users.txt); do
    echo $user
done

# seq命令
for i in $(seq 1 10); do
    echo $i
done

# Brace扩展
for i in {1..10}; do
    echo $i
done

for i in {1..10..2}; do  # 步长2
    echo $i
done
```

### while循环

```bash
# 基本语法
while [ condition ]; do
    commands
done

# 示例：计数器
count=1
while [ $count -le 5 ]; do
    echo $count
    ((count++))
done

# 无限循环
while true; do
    echo "infinite loop"
    sleep 1
done

# 读取文件
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

### until循环

```bash
# 直到条件为真
until [ condition ]; do
    commands
done

# 示例
count=1
until [ $count -gt 5 ]; do
    echo $count
    ((count++))
done
```

### break和continue

```bash
# break：跳出循环
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        break
    fi
    echo $i
done

# continue：跳过当前迭代
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        continue
    fi
    echo $i
done
```

## 函数

### 函数定义

```bash
# 方式1
function_name() {
    commands
}

# 方式2
function function_name {
    commands
}

# 示例
greet() {
    echo "Hello, $1"
}

greet "Alice"  # 调用
```

### 参数和返回值

```bash
# 函数参数
add() {
    local a=$1
    local b=$2
    echo $((a + b))
}

result=$(add 3 5)
echo $result  # 8

# return（0-255）
is_even() {
    local num=$1
    if [ $((num % 2)) -eq 0 ]; then
        return 0  # 成功
    else
        return 1  # 失败
    fi
}

if is_even 4; then
    echo "even"
fi

# echo返回字符串
get_date() {
    echo $(date +%Y-%m-%d)
}

today=$(get_date)
```

### 局部变量

```bash
global_var="global"

test_func() {
    local local_var="local"    # 局部变量
    global_var="modified"      # 修改全局
    echo "$local_var"
}

test_func
echo "$global_var"   # modified
# echo "$local_var"  # 错误：未定义
```

## 调试

### 调试选项

```bash
# -x：打印执行的命令
bash -x script.sh

# 脚本内启用
#!/bin/bash
set -x        # 开启
commands
set +x        # 关闭

# -e：遇到错误立即退出
set -e

# -u：使用未定义变量时报错
set -u

# 组合使用
set -eux
set -euo pipefail  # 管道中任一命令失败都退出
```

### 常用调试技巧

```bash
# 检查语法
bash -n script.sh

# 打印调试信息
echo "DEBUG: var=$var" >&2

# 条件调试
DEBUG=1
[ "$DEBUG" = 1 ] && echo "Debug info"

# trap捕获错误
trap 'echo "Error at line $LINENO"' ERR
```

## 最佳实践

### Shebang和选项

```bash
#!/usr/bin/env bash

# 严格模式
set -euo pipefail
# -e: 命令失败立即退出
# -u: 使用未定义变量报错
# -o pipefail: 管道中任一失败都失败
```

### 变量命名

```bash
# 小写：局部变量
local_var="value"

# 大写：环境变量/常量
export PATH=$PATH:/usr/local/bin
readonly MAX_COUNT=100

# 引号保护
echo "$var"        # 推荐
echo "${var}"      # 明确边界
echo "${var:-default}"  # 默认值
```

### 错误处理

```bash
# 检查命令是否存在
if ! command -v git &> /dev/null; then
    echo "git not found"
    exit 1
fi

# 检查上一命令状态
if [ $? -ne 0 ]; then
    echo "Command failed"
    exit 1
fi

# 更优雅
if ! some_command; then
    echo "Failed"
    exit 1
fi
```

### 代码组织

```bash
#!/usr/bin/env bash
set -euo pipefail

# 常量
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/var/log/script.log"

# 函数
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

cleanup() {
    log "Cleaning up..."
    # 清理操作
}

main() {
    trap cleanup EXIT  # 退出时清理
    
    log "Starting..."
    # 主逻辑
}

# 入口
main "$@"
```

**核心：** Shell脚本重在实用，掌握基础语法和文本处理工具是关键。

