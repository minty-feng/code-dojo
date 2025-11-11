# Git 版本控制工具

## 核心概念
- **仓库(Repository)**：代码存储的地方，包含所有版本历史
- **提交(Commit)**：代码变更的快照，包含作者、时间、变更内容
- **分支(Branch)**：独立的开发线，可以并行开发不同功能
- **合并(Merge)**：将不同分支的代码整合到一起
- **远程(Remote)**：网络上的仓库，用于团队协作

## 基础操作
```bash
# 初始化仓库
git init                    # 在当前目录创建新仓库
git clone <url>             # 克隆远程仓库到本地
git clone -b <branch> <url> # 克隆指定分支

# 查看状态和历史
git status                  # 查看工作区状态
git log                     # 查看提交历史
git log --oneline           # 简洁的单行显示
git log --graph --oneline   # 图形化显示分支
git log -p <file>           # 查看文件的修改历史

# 添加和提交
git add <file>              # 添加文件到暂存区
git add .                   # 添加所有文件
git add -A                  # 添加所有文件(包括删除的)
git commit -m "message"     # 提交暂存区的文件
git commit -am "message"    # 添加并提交已跟踪的文件
```

## 分支管理
```bash
# 分支操作
git branch                  # 查看本地分支
git branch -r               # 查看远程分支
git branch -a               # 查看所有分支
git branch <name>           # 创建新分支
git checkout <branch>       # 切换分支
git checkout -b <branch>    # 创建并切换到新分支
git switch <branch>         # 新语法：切换分支
git switch -c <branch>      # 新语法：创建并切换

# 分支合并
git merge <branch>           # 合并指定分支到当前分支
git merge --no-ff <branch>  # 禁用快进合并
git merge --squash <branch> # 压缩合并为一个提交

# 分支删除
git branch -d <branch>      # 删除已合并的分支
git branch -D <branch>       # 强制删除分支
git push origin --delete <branch> # 删除远程分支
```

## 远程操作
```bash
# 远程仓库管理
git remote -v               # 查看远程仓库
git remote add <name> <url> # 添加远程仓库
git remote remove <name>    # 删除远程仓库
git remote rename <old> <new> # 重命名远程仓库

# 推送和拉取
git push origin <branch>    # 推送分支到远程
git push -u origin <branch> # 推送并设置上游分支
git push --all origin       # 推送所有分支
git push --tags origin      # 推送所有标签

git pull origin <branch>    # 拉取并合并远程分支
git fetch origin            # 获取远程更新但不合并
git fetch --all             # 获取所有远程仓库的更新
```

## 撤销和回退
```bash
# 撤销工作区修改
git checkout -- <file>      # 撤销文件修改
git restore <file>          # 新语法：撤销文件修改

# 撤销暂存区修改
git reset HEAD <file>       # 取消暂存文件
git restore --staged <file> # 新语法：取消暂存

# 撤销提交
git reset --soft HEAD~1     # 撤销提交，保留修改在暂存区
git reset --mixed HEAD~1    # 撤销提交，修改回到工作区
git reset --hard HEAD~1     # 撤销提交，丢弃所有修改
git revert <commit>         # 创建新提交来撤销指定提交

# 修改最后一次提交
git commit --amend -m "new message" # 修改提交信息
git commit --amend --no-edit        # 修改提交内容，不修改信息
```

## 查看差异
```bash
# 查看各种差异
git diff                    # 工作区 vs 暂存区
git diff --cached           # 暂存区 vs 最后一次提交
git diff HEAD               # 工作区 vs 最后一次提交
git diff <commit1> <commit2> # 两个提交间的差异
git diff <branch1> <branch2> # 两个分支间的差异
git diff --name-only        # 只显示文件名
git diff --stat             # 显示统计信息
```

## 暂存工作
```bash
# 暂存当前工作
git stash                   # 暂存当前工作
git stash push -m "message" # 暂存并添加说明
git stash list              # 查看暂存列表
git stash show              # 查看最新暂存的内容
git stash show -p            # 查看最新暂存的详细内容

# 恢复暂存的工作
git stash pop               # 恢复并删除最新暂存
git stash apply             # 恢复但不删除
git stash apply stash@{2}   # 恢复指定的暂存
git stash drop              # 删除最新暂存
git stash clear             # 删除所有暂存
```

## 标签管理
```bash
# 标签操作
git tag                     # 查看所有标签
git tag <name>              # 创建轻量标签
git tag -a <name> -m "msg"  # 创建带注释的标签
git tag -a <name> <commit>   # 为指定提交创建标签
git show <tag>              # 查看标签信息

# 推送标签
git push origin <tag>       # 推送指定标签
git push origin --tags     # 推送所有标签
git push origin :refs/tags/<tag> # 删除远程标签

# 删除标签
git tag -d <tag>           # 删除本地标签
```

## 高级操作
```bash
# 交互式rebase
git rebase -i HEAD~3        # 交互式rebase最近3个提交
git rebase -i <commit>      # 从指定提交开始rebase

# 挑选提交
git cherry-pick <commit>    # 挑选指定提交到当前分支
git cherry-pick <commit1> <commit2> # 挑选多个提交

# 二分查找
git bisect start            # 开始二分查找
git bisect bad <commit>     # 标记坏的提交
git bisect good <commit>    # 标记好的提交
git bisect reset            # 结束二分查找

# 查找内容
git log -S "function_name"  # 查找包含特定内容的提交
git log -G "pattern"       # 查找匹配正则表达式的提交
git log --follow <file>     # 跟踪文件的重命名历史
```

## 配置和别名
```bash
# 全局配置
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "code --wait"
git config --global init.defaultBranch main
git config --global core.autocrlf true  # Windows
git config --global core.autocrlf input # macOS/Linux

# 常用别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'"
```

## .gitignore 配置
```gitignore
# 依赖文件
node_modules/
vendor/
__pycache__/

# 构建输出
dist/
build/
target/
*.o
*.so
*.dylib

# 环境配置
.env
.env.local
.env.production
config/database.yml

# 日志文件
*.log
logs/
npm-debug.log*

# 系统文件
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE文件
.vscode/
.idea/
*.swp
*.swo
*~

# 临时文件
*.tmp
*.temp
.cache/
```

## 工作流模式

### 功能分支工作流
```bash
# 1. 创建功能分支
git checkout -b feature/new-feature
git push -u origin feature/new-feature

# 2. 开发功能
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature

# 3. 合并到主分支
git checkout main
git pull origin main
git merge feature/new-feature
git push origin main
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### Git Flow工作流
```bash
# 主分支
main/master    # 生产环境代码
develop        # 开发环境代码

# 功能分支
feature/user-login
feature/payment-system

# 发布分支
release/v1.2.0

# 热修复分支
hotfix/critical-bug-fix
```

## 解决冲突
```bash
# 1. 查看冲突状态
git status

# 2. 手动解决冲突
# 编辑冲突文件，删除 <<<<<<< ======= >>>>>>> 标记
# 选择保留的代码

# 3. 标记冲突已解决
git add <resolved-file>

# 4. 完成合并
git commit
```

## 实用技巧

### 提交信息规范
```bash
# 提交类型
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动

# 示例
git commit -m "feat: add user authentication"
git commit -m "fix: resolve login validation issue"
git commit -m "docs: update API documentation"
```

### 查找和恢复
```bash
# 恢复被删除的文件
git checkout HEAD -- <file>

# 查看删除的文件历史
git log --diff-filter=D --summary

# 查找文件的修改历史
git log --follow <file>

# 查看文件的每一行修改历史
git blame <file>
```

### 性能优化
```bash
# 清理仓库
git gc                      # 垃圾回收
git prune                   # 清理不可达对象
git repack -a -d            # 重新打包

# 大文件处理
git lfs track "*.psd"       # 使用Git LFS跟踪大文件
git lfs migrate import --include="*.psd" # 迁移现有大文件
```

## 故障排查
```bash
# 查看操作历史
git reflog                  # 查看所有操作历史
git reflog show <branch>    # 查看分支操作历史

# 恢复丢失的提交
git reflog                  # 找到丢失的提交哈希
git checkout <commit-hash>  # 切换到丢失的提交
git checkout -b <new-branch> # 创建新分支保存

# 强制推送(谨慎使用)
git push --force-with-lease origin <branch> # 更安全的强制推送
```

## 团队协作
```bash
# 代码审查
git request-pull <start> <url> [<end>] # 生成拉取请求

# 同步远程分支
git fetch origin
git checkout -b <branch> origin/<branch> # 创建本地分支跟踪远程分支

# 更新上游分支
git checkout main
git pull origin main
git checkout <feature-branch>
git rebase main             # 将功能分支rebase到最新的main
```