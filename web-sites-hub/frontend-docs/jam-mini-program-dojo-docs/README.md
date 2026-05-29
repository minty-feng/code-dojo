# WeChat Mini Program Tutorial Documentation Site

微信小程序开发完整指南的静态文档站点。

## 📚 文档内容

本站点包含以下6个章节：

1. **基础** - 快速开始、WXML/WXSS语法、生命周期、组件与API
2. **网络请求与云开发** - 网络请求封装、用户登录、云开发、WebSocket
3. **性能优化与最佳实践** - setData优化、长列表优化、图片优化、分包加载
4. **部署与发布** - 开发环境配置、版本管理、代码上传与审核、发布上线
5. **测试与调试** - 开发者工具调试、真机调试、单元测试、集成测试、E2E测试
6. **后端开发与集成** - 后端架构设计、用户登录与认证、RESTful API、数据库设计

## 🚀 构建文档

### 首次构建

```bash
# 运行构建脚本（会自动创建虚拟环境并安装依赖）
./build.sh
```

### 后续构建

```bash
# 激活虚拟环境
source venv/bin/activate

# 构建文档
sphinx-build -b html . _build/html
```

## 📦 打包部署

### 创建部署包

```bash
./package-nginx.sh
```

### 部署到服务器

```bash
# 上传打包文件到服务器后
sudo ./deploy-miniprogram.sh miniprogram-docs-nginx-*.tar.gz
```

### 配置 Nginx

使用统一部署脚本：

```bash
# HTTP 部署
sudo ./deploy-joketop-nginx.sh

# HTTPS 部署（Let's Encrypt）
sudo ./deploy-joketop-nginx.sh --letsencrypt --email your@email.com
```

## 📁 目录结构

```
jam-mini-program-dojo-docs/
├── conf.py                    # Sphinx 配置文件
├── index.rst                  # 主索引文件
├── introduction.md            # 介绍文档
├── 01-wechat-miniprogram-basics.md       # 第一章
├── 02-network-request-and-cloud.md       # 第二章
├── 03-performance-optimization.md        # 第三章
├── 04-deployment-and-release.md         # 第四章
├── 05-testing-and-debugging.md          # 第五章
├── 06-backend-development.md            # 第六章
├── requirements.txt           # Python 依赖
├── build.sh                   # 构建脚本
├── deploy-miniprogram.sh      # 部署脚本
├── package-nginx.sh           # 打包脚本
├── _static/                   # 静态资源
│   ├── custom.css
│   ├── favicon.ico
│   └── favicon.svg
└── _templates/                # 模板文件
```

## 🔧 技术栈

- **Sphinx** - 文档生成工具
- **MyST Parser** - Markdown 解析器
- **sphinx-rtd-theme** - Read the Docs 主题

## 📝 更新文档

当源文档更新时，需要重新拷贝文件：

```bash
# 从源目录拷贝最新文档
cp ../../jam-mini-program-dojo/README.md introduction.md
cp ../../jam-mini-program-dojo/01-微信小程序基础.md 01-wechat-miniprogram-basics.md
cp ../../jam-mini-program-dojo/02-网络请求与云开发.md 02-network-request-and-cloud.md
cp ../../jam-mini-program-dojo/03-性能优化与最佳实践.md 03-performance-optimization.md
cp ../../jam-mini-program-dojo/04-部署与发布.md 04-deployment-and-release.md
cp ../../jam-mini-program-dojo/05-测试与调试.md 05-testing-and-debugging.md
cp ../../jam-mini-program-dojo/06-后端开发与集成.md 06-backend-development.md

# 重新构建
./build.sh
```

## 🌐 访问地址

部署后的访问地址：
- HTTP: `http://blog.joketop.com/miniprogram`
- HTTPS: `https://blog.joketop.com/miniprogram`

