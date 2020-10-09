# Shell脚本学习路径

Shell是Linux/Unix系统的命令解释器和脚本语言，运维自动化的核心工具。

## 学习时间线

**2020年6月 - 2020年10月（5个月）**

### 阶段一：Shell基础（2020-06）
- Shell类型（Bash、Zsh）
- 变量、数据类型、运算符
- 流程控制、函数
- 输入输出、重定向

### 阶段二：文本处理（2020-07）
- grep：文本搜索
- sed：流编辑器
- awk：文本分析
- 三剑客组合使用

### 阶段三：实战应用（2020-09）
- 系统监控脚本
- 日志分析脚本
- 备份脚本
- 批量处理脚本
- 部署自动化

## 学习文档

1. **01-Shell基础.md** - Shell语法、变量、流程控制、函数
2. **02-文本处理三剑客.md** - grep、sed、awk详解
3. **03-实用脚本.md** - 系统管理、日志分析、备份部署

## Shell核心特性

### 语言特性
- **简单语法**：易学易用，快速编写脚本
- **命令集成**：直接调用系统命令
- **管道机制**：命令组合，功能强大
- **正则表达式**：文本处理能力强
- **进程控制**：后台任务、信号处理

### 文本处理三剑客
- **grep**：搜索过滤，正则匹配
- **sed**：流编辑，替换删除
- **awk**：分析统计，列处理

### 应用场景
- **系统运维**：监控、巡检、告警
- **日志分析**：统计、过滤、报表
- **自动化部署**：CI/CD流程
- **批量处理**：文件操作、格式转换
- **定时任务**：备份、清理、同步

## 常用命令速查

### 文件操作
```bash
ls, cd, pwd, mkdir, rm, cp, mv
cat, head, tail, less, more
find, locate, which, whereis
chmod, chown, chgrp
tar, gzip, zip, unzip
```

### 文本处理
```bash
grep, egrep, fgrep
sed
awk
cut, sort, uniq, wc
tr, diff, patch
```

### 系统管理
```bash
ps, top, htop, kill
systemctl, service
df, du, free
netstat, ss, lsof
crontab, at
```

### 网络工具
```bash
ping, traceroute, nslookup
curl, wget
ssh, scp, rsync
nc, telnet
```

## 项目实践

### 常用脚本类型
1. **监控脚本** - CPU、内存、磁盘、服务监控
2. **日志分析** - 访问日志、错误日志统计
3. **备份脚本** - 数据库备份、文件同步
4. **部署脚本** - 应用部署、容器管理
5. **批处理** - 文件重命名、格式转换

### 脚本模板
```bash
#!/usr/bin/env bash

set -euo pipefail  # 严格模式

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/var/log/script.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

cleanup() {
    log "清理资源..."
}

trap cleanup EXIT

main() {
    log "开始执行..."
    # 主逻辑
}

main "$@"
```

## 最佳实践

### 脚本规范
1. **Shebang**：`#!/usr/bin/env bash`
2. **严格模式**：`set -euo pipefail`
3. **变量引用**：`"$var"` 而不是 `$var`
4. **函数分解**：逻辑清晰，单一职责
5. **错误处理**：检查命令返回值
6. **日志记录**：关键操作留痕
7. **参数校验**：检查输入有效性

### 变量命名
```bash
# 小写：局部变量
local_var="value"

# 大写：环境变量/常量
readonly MAX_COUNT=100
export PATH=$PATH:/usr/local/bin

# 明确引用
"${var}"                # 推荐
"${var:-default}"       # 默认值
"${var:?error}"         # 未定义报错
"${var/old/new}"        # 替换
```

### 错误处理
```bash
# 检查命令存在
if ! command -v git &> /dev/null; then
    echo "git 未安装"
    exit 1
fi

# 检查文件
if [ ! -f "$file" ]; then
    echo "文件不存在: $file"
    exit 1
fi

# 检查命令状态
if ! some_command; then
    echo "命令失败"
    exit 1
fi

# 捕获错误行号
trap 'echo "错误在第 $LINENO 行"' ERR
```

### 性能优化
```bash
# 避免不必要的管道
# ❌ 慢
cat file | grep pattern

# ✅ 快
grep pattern file

# 使用内建命令
# ❌ 慢（外部命令）
result=$(basename "$path")

# ✅ 快（参数扩展）
result="${path##*/}"

# 批量处理用while
# ❌ 慢（每次fork）
for line in $(cat file); do
    process "$line"
done

# ✅ 快（管道）
while IFS= read -r line; do
    process "$line"
done < file
```

## 调试技巧

### 调试选项
```bash
bash -x script.sh      # 打印执行命令
bash -n script.sh      # 检查语法
bash -v script.sh      # 打印原始命令

# 脚本内控制
set -x  # 开启
set +x  # 关闭
```

### 调试函数
```bash
debug() {
    [ "$DEBUG" = "1" ] && echo "DEBUG: $*" >&2
}

# 使用
DEBUG=1 ./script.sh
```

### ShellCheck
```bash
# 安装静态分析工具
apt install shellcheck

# 检查脚本
shellcheck script.sh

# 忽略特定规则
# shellcheck disable=SC2086
```

## grep、sed、awk选择

### 使用场景
| 任务 | 工具 | 理由 |
|------|------|------|
| 搜索过滤 | grep | 专用，最快 |
| 简单替换 | sed | 流编辑专用 |
| 列处理 | awk | 列处理最强 |
| 统计计算 | awk | 支持变量数组 |
| 复杂逻辑 | awk | 接近编程语言 |

### 组合使用
```bash
# 典型流程
grep "pattern" file.log |    # 过滤
    sed 's/old/new/g' |       # 替换
    awk '{print $1, $3}' |    # 提取列
    sort | uniq -c             # 统计

# 避免不必要的管道
# ❌
grep "pattern" file | awk '{print $1}'

# ✅
awk '/pattern/ {print $1}' file
```

## 常见陷阱

### 1. 变量不加引号
```bash
# ❌ 变量包含空格会出错
rm $file

# ✅
rm "$file"
```

### 2. 比较运算符混淆
```bash
# ❌ 字符串比较用数值运算符
[ "$str" -eq "value" ]

# ✅
[ "$str" = "value" ]
```

### 3. 管道中变量作用域
```bash
# ❌ 管道创建子shell，count不生效
count=0
cat file | while read line; do
    ((count++))
done
echo $count  # 0

# ✅
count=0
while read line; do
    ((count++))
done < file
echo $count  # 正确
```

### 4. 文件名中的空格
```bash
# ❌
for file in $(ls *.txt); do
    process $file
done

# ✅
while IFS= read -r -d '' file; do
    process "$file"
done < <(find . -name "*.txt" -print0)
```

## 学习资源

### 在线资源
- Bash官方手册：https://www.gnu.org/software/bash/manual/
- Advanced Bash-Scripting Guide
- ShellCheck：https://www.shellcheck.net/
- Explain Shell：https://explainshell.com/

### 推荐书籍
- 《Linux命令行与shell脚本编程大全》
- 《sed与awk》
- 《精通正则表达式》

### 练习平台
- HackerRank Shell
- LeetCode Shell题目
- 实际生产环境问题

## 应用领域

### DevOps
- CI/CD脚本
- 自动化部署
- 配置管理
- 容器管理

### 运维
- 系统监控
- 日志分析
- 备份恢复
- 告警通知

### 数据处理
- 日志清洗
- 格式转换
- 统计分析
- 报表生成

## 学习心得

1. **实用主义**：Shell重在解决实际问题
2. **简洁为美**：复杂逻辑用Python等其他语言
3. **三剑客必会**：grep/sed/awk是核心技能
4. **管道思维**：组合简单命令实现复杂功能
5. **错误处理**：生产环境必须严谨
6. **日志记录**：关键操作可追溯
7. **模板复用**：建立常用脚本库
8. **持续学习**：新工具新特性不断涌现
9. **实践为主**：看千遍不如手写一遍
10. **代码审查**：用ShellCheck检查规范

**核心：** Shell是Linux运维的基本功，掌握基础语法和三剑客可解决大部分实际问题。复杂逻辑建议用Python/Go等语言。

