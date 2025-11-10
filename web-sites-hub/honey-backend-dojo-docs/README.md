# Backend Tutorial - Sphinx 文档站点

Backend Tutorial 的 Sphinx 静态文档站点。

## 📁 项目结构

```
sphinx-docs/honey-backend-dojo-docs/
├── conf.py              # Sphinx 配置文件
├── index.rst            # 主索引文件
├── introduction.md      # 介绍页面
├── requirements.txt     # Python 依赖
├── Makefile             # 构建脚本
├── build.sh             # 首次构建脚本
├── convert-md-to-rst.sh # Markdown 转 RST 脚本
├── package-nginx.sh     # Nginx 部署包脚本
├── deploy.sh            # 服务器部署脚本
├── cpp/                 # C++ 文档（RST 格式）
│   ├── index.rst
│   └── *.rst
├── python/              # Python 文档
│   ├── index.rst
│   └── *.rst
├── java/                # Java 文档
├── nodejs/              # Node.js 文档
├── go/                  # Go 文档
├── rust/                # Rust 文档
└── shell/               # Shell 文档
```

## ✨ 新结构优势

1. **使用 RST 格式**：原生 Sphinx 格式，性能更好
2. **自动转换**：从源目录的 Markdown 文件自动转换为 RST
3. **独立管理**：转换后的 RST 文件独立管理
4. **无需符号链接**：使用实际文件，不依赖符号链接

## 🚀 快速开始

### 首次构建

```bash
cd sphinx-docs/honey-backend-dojo-docs
./build.sh
```

### 后续构建

```bash
# 使用 make（会自动转换 RST）
make html

# 或手动转换后构建
bash convert-md-to-rst.sh
sphinx-build -b html . _build/html
```

### 查看文档

构建完成后，在浏览器中打开 `_build/html/index.html` 查看文档。

## 📦 部署

### 创建 Nginx 部署包

```bash
./package-nginx.sh
```

### 服务器部署

```bash
sudo bash deploy.sh backend-docs-nginx-*.tar.gz
```

## 📝 更新文档

文档文件通过转换脚本从源目录的 Markdown 文件生成：

1. **修改源文件**：在 `honey-backend-dojo/go/` 等目录下修改 Markdown 文件
2. **重新转换**：
   ```bash
   bash convert-md-to-rst.sh
   ```
3. **重新构建**：
   ```bash
   make html
   ```

## 🔄 Markdown 转 RST

使用 `convert-md-to-rst.sh` 脚本可以自动从源目录转换所有 Markdown 文件：

```bash
./convert-md-to-rst.sh
```

这个脚本会：
- 从 `../../honey-backend-dojo/` 目录读取所有语言的 Markdown 文件
- 使用 m2r2/pandoc 转换为 RST 格式
- 保存到对应的语言目录下（如 `go/01-environment-setup.rst`）

### 转换工具要求

- **m2r2**（推荐）：`pip install m2r2`
- **pandoc**（备选）：`brew install pandoc` 或 `pip install pypandoc`

## 💡 工作原理

1. `convert-md-to-rst.sh` 脚本从源目录读取 Markdown 文件
2. 使用转换工具（m2r2/pandoc）将 Markdown 转换为 RST
3. 转换后的 RST 文件保存在当前目录的语言目录下
4. Sphinx 构建时直接使用 RST 文件

## 📋 文件格式

- **源文件**：`honey-backend-dojo/go/01-environment-setup.md`（Markdown）
- **转换后**：`sphinx-docs/honey-backend-dojo-docs/go/01-environment-setup.rst`（RST）
- **配置文件**：`conf.py` 只支持 `.rst` 格式
