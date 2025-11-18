# 部署与发布

## 💡 核心结论

1. **小程序发布需要经过开发版本→体验版本→审核版本→正式版本的流程**
2. **版本号遵循语义化版本规范，主版本号.次版本号.修订号**
3. **审核前需配置合法域名、完善隐私政策、通过真机调试**
4. **支持灰度发布和分阶段发布，降低风险**
5. **监控和日志收集对线上问题排查至关重要**

---

## 1. 开发环境配置

### 1.1 项目配置

```json
// project.config.json
{
  "description": "项目配置文件",
  "packOptions": {
    "ignore": [
      {
        "type": "file",
        "value": ".eslintrc.js"
      },
      {
        "type": "folder",
        "value": "node_modules"
      }
    ]
  },
  "setting": {
    "urlCheck": false,  // 开发环境关闭域名校验
    "es6": true,
    "enhance": true,
    "postcss": true,
    "minified": true,
    "newFeature": true,
    "coverView": true,
    "nodeModules": true,
    "autoAudits": false,
    "showShadowRootInWxmlPanel": true,
    "scopeDataCheck": false,
    "uglifyFileName": false,
    "checkInvalidKey": true,
    "checkSiteMap": true,
    "uploadWithSourceMap": true,
    "compileHotReLoad": false,
    "useMultiFrameRuntime": true,
    "useApiHook": true,
    "babelSetting": {
      "ignore": [],
      "disablePlugins": [],
      "outputPath": ""
    }
  },
  "compileType": "miniprogram",
  "libVersion": "2.19.4",
  "appid": "your_appid",
  "projectname": "my-miniprogram",
  "condition": {},
  "editorSetting": {
    "tabIndent": "insertSpaces",
    "tabSize": 2
  }
}
```

### 1.2 环境变量管理

```javascript
// config/env.js
const env = {
  // 开发环境
  development: {
    baseURL: 'https://dev-api.example.com',
    envId: 'dev-env-id',
    debug: true
  },
  // 测试环境
  testing: {
    baseURL: 'https://test-api.example.com',
    envId: 'test-env-id',
    debug: true
  },
  // 生产环境
  production: {
    baseURL: 'https://api.example.com',
    envId: 'prod-env-id',
    debug: false
  }
}

// 根据编译模式选择环境
const currentEnv = env[process.env.NODE_ENV] || env.development

export default currentEnv
```

```javascript
// utils/request.js
import config from '../config/env.js'

const baseURL = config.baseURL

export function request(options) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: baseURL + options.url,
      // ...
    })
  })
}
```

### 1.3 构建脚本

```json
// package.json
{
  "scripts": {
    "dev": "cross-env NODE_ENV=development",
    "test": "cross-env NODE_ENV=testing",
    "build": "cross-env NODE_ENV=production",
    "lint": "eslint .",
    "format": "prettier --write \"**/*.{js,json,wxml,wxss}\""
  }
}
```

---

## 2. 版本管理

### 2.1 版本号规范

```javascript
// 语义化版本：主版本号.次版本号.修订号
// 1.0.0 → 1.0.1 (修复bug)
// 1.0.1 → 1.1.0 (新功能)
// 1.1.0 → 2.0.0 (重大变更)

// app.json
{
  "version": "1.2.3",
  "versionName": "v1.2.3 - 新增商品搜索功能"
}
```

### 2.2 版本发布流程

```
开发版本 (开发工具上传)
    ↓
体验版本 (后台设置为体验版)
    ↓
提交审核 (填写版本信息、上传代码)
    ↓
审核中 (1-7个工作日)
    ↓
审核通过 → 发布上线
审核拒绝 → 修改后重新提交
```

### 2.3 开发版本管理

```bash
# 1. 在开发者工具中上传代码
# 工具 → 上传 → 填写版本号和项目备注

# 2. 查看版本列表
# 小程序后台 → 版本管理 → 开发版本

# 3. 设置体验版
# 选择开发版本 → 选为体验版
```

### 2.4 版本回退

```javascript
// 小程序后台 → 版本管理 → 版本回退
// 可以回退到之前的任意版本
// 注意：回退后需要重新提交审核
```

---

## 3. 域名配置

### 3.1 服务器域名配置

```bash
# 小程序后台 → 开发 → 开发管理 → 开发设置 → 服务器域名

# request合法域名
https://api.example.com
https://api2.example.com

# uploadFile合法域名
https://upload.example.com

# downloadFile合法域名
https://cdn.example.com

# socket合法域名
wss://ws.example.com
```

### 3.2 业务域名配置

```bash
# 小程序后台 → 开发 → 开发管理 → 开发设置 → 业务域名

# web-view组件使用的域名
https://h5.example.com
```

### 3.3 域名校验

```javascript
// 开发环境关闭域名校验
// project.config.json
{
  "setting": {
    "urlCheck": false
  }
}

// 生产环境必须配置合法域名
// 否则会报错：不在以下 request 合法域名列表中
```

---

## 4. 代码上传与审核

### 4.1 上传代码

```bash
# 方式1：开发者工具上传
# 工具 → 上传 → 填写版本号和备注

# 方式2：CI/CD自动上传
# 使用微信开发者工具命令行
```

```javascript
// scripts/upload.js
const { execSync } = require('child_process')

const version = process.env.VERSION || '1.0.0'
const desc = process.env.DESC || '自动上传'

execSync(
  `cli upload --project ./miniprogram --version ${version} --desc ${desc}`,
  { stdio: 'inherit' }
)
```

### 4.2 提交审核

**审核前检查清单**：

```markdown
- [ ] 功能完整性测试
- [ ] 真机调试通过
- [ ] 隐私政策配置
- [ ] 用户协议配置
- [ ] 合法域名配置
- [ ] 代码无报错
- [ ] 包体积符合要求（主包≤2MB）
- [ ] 测试账号准备
- [ ] 审核说明文档
```

**提交审核**：

```bash
# 小程序后台 → 版本管理 → 提交审核

# 填写信息：
# 1. 版本号
# 2. 版本描述
# 3. 测试账号（如需要）
# 4. 审核说明
# 5. 类目选择
```

### 4.3 审核要点

**常见拒绝原因**：

1. **功能不完整**
   - 页面空白或无法正常使用
   - 功能与描述不符

2. **隐私问题**
   - 未配置隐私政策
   - 未获取用户授权就收集信息

3. **内容违规**
   - 涉及敏感内容
   - 诱导分享

4. **技术问题**
   - 页面崩溃
   - 网络请求失败
   - 性能问题

**审核说明模板**：

```markdown
## 版本更新说明
本次更新主要功能：
1. 新增商品搜索功能
2. 优化订单列表加载速度
3. 修复已知bug

## 测试账号
测试账号：test@example.com
密码：123456

## 测试路径
首页 → 搜索 → 输入"手机" → 查看结果

## 注意事项
- 需要登录后才能使用完整功能
- 部分功能需要网络连接
```

---

## 5. 发布上线

### 5.1 全量发布

```bash
# 小程序后台 → 版本管理 → 审核版本
# 点击"发布" → 确认发布

# 发布后：
# - 所有用户可立即使用新版本
# - 旧版本用户需要重启小程序才能看到新版本
```

### 5.2 灰度发布

```javascript
// 小程序后台 → 版本管理 → 审核版本 → 灰度发布

// 灰度比例设置：
// - 10%：10%用户使用新版本
// - 25%：25%用户使用新版本
// - 50%：50%用户使用新版本
// - 100%：全量发布

// 灰度期间监控：
// - 错误率
// - 性能指标
// - 用户反馈
```

### 5.3 分阶段发布

```javascript
// 阶段1：灰度10%用户，观察1-2天
// 阶段2：灰度50%用户，观察1天
// 阶段3：全量发布

// 如果发现问题，可以：
// 1. 停止灰度
// 2. 回退版本
// 3. 修复后重新发布
```

---

## 6. 监控与日志

### 6.1 错误监控

```javascript
// utils/monitor.js
export const monitor = {
  // 上报错误
  reportError(error, context = {}) {
    const errorInfo = {
      message: error.message || error,
      stack: error.stack,
      timestamp: Date.now(),
      userInfo: wx.getStorageSync('userInfo'),
      systemInfo: wx.getSystemInfoSync(),
      ...context
    }
    
    // 上报到后端
    wx.request({
      url: 'https://api.example.com/monitor/error',
      method: 'POST',
      data: errorInfo,
      fail: () => {
        // 上报失败，存储到本地
        const errors = wx.getStorageSync('errorLogs') || []
        errors.push(errorInfo)
        wx.setStorageSync('errorLogs', errors.slice(-10)) // 只保留最近10条
      }
    })
  },
  
  // 上报性能数据
  reportPerformance(metrics) {
    wx.request({
      url: 'https://api.example.com/monitor/performance',
      method: 'POST',
      data: {
        ...metrics,
        timestamp: Date.now()
      }
    })
  }
}
```

```javascript
// app.js
App({
  onLaunch() {
    // 全局错误监听
    wx.onError((error) => {
      monitor.reportError(error, {
        type: 'global',
        page: getCurrentPages().pop()?.route
      })
    })
    
    // Promise未捕获错误
    wx.onUnhandledRejection((res) => {
      monitor.reportError(res.reason, {
        type: 'unhandledRejection',
        promise: res.promise
      })
    })
  }
})
```

### 6.2 日志收集

```javascript
// utils/logger.js
const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
}

class Logger {
  constructor() {
    this.logs = []
    this.maxLogs = 100
    this.level = LOG_LEVELS.INFO
  }
  
  log(level, message, data = {}) {
    if (level < this.level) return
    
    const logEntry = {
      level,
      message,
      data,
      timestamp: Date.now(),
      page: getCurrentPages().pop()?.route
    }
    
    this.logs.push(logEntry)
    
    // 限制日志数量
    if (this.logs.length > this.maxLogs) {
      this.logs.shift()
    }
    
    // 开发环境打印到控制台
    if (wx.getSystemInfoSync().platform === 'devtools') {
      console.log(`[${this.getLevelName(level)}]`, message, data)
    }
  }
  
  debug(message, data) {
    this.log(LOG_LEVELS.DEBUG, message, data)
  }
  
  info(message, data) {
    this.log(LOG_LEVELS.INFO, message, data)
  }
  
  warn(message, data) {
    this.log(LOG_LEVELS.WARN, message, data)
  }
  
  error(message, data) {
    this.log(LOG_LEVELS.ERROR, message, data)
  }
  
  // 上报日志
  upload() {
    if (this.logs.length === 0) return
    
    wx.request({
      url: 'https://api.example.com/logs',
      method: 'POST',
      data: {
        logs: this.logs,
        userInfo: wx.getStorageSync('userInfo')
      },
      success: () => {
        this.logs = []
      }
    })
  }
  
  getLevelName(level) {
    return Object.keys(LOG_LEVELS).find(key => LOG_LEVELS[key] === level)
  }
}

export default new Logger()
```

```javascript
// 使用
import logger from '../../utils/logger.js'

Page({
  onLoad() {
    logger.info('页面加载', { page: 'index' })
  },
  
  async loadData() {
    try {
      logger.debug('开始加载数据')
      const res = await wx.request({ url: '...' })
      logger.info('数据加载成功', { count: res.data.length })
    } catch (error) {
      logger.error('数据加载失败', { error: error.message })
    }
  },
  
  onUnload() {
    // 页面卸载时上报日志
    logger.upload()
  }
})
```

### 6.3 性能监控

```javascript
// utils/performance.js
export const performance = {
  // 页面加载时间
  measurePageLoad(pageName) {
    const startTime = Date.now()
    
    return {
      end() {
        const loadTime = Date.now() - startTime
        monitor.reportPerformance({
          type: 'pageLoad',
          page: pageName,
          duration: loadTime
        })
        return loadTime
      }
    }
  },
  
  // API请求时间
  measureRequest(url) {
    const startTime = Date.now()
    
    return {
      end(statusCode) {
        const duration = Date.now() - startTime
        monitor.reportPerformance({
          type: 'request',
          url,
          duration,
          statusCode
        })
        return duration
      }
    }
  }
}
```

```javascript
// 使用
Page({
  onLoad() {
    const pageLoad = performance.measurePageLoad('index')
    
    this.loadData().then(() => {
      pageLoad.end()
    })
  },
  
  async loadData() {
    const request = performance.measureRequest('/api/products')
    
    try {
      const res = await wx.request({ url: '...' })
      request.end(res.statusCode)
    } catch (error) {
      request.end(0)
    }
  }
})
```

---

## 7. 热更新与版本控制

### 7.1 检查更新

```javascript
// app.js
App({
  onLaunch() {
    this.checkUpdate()
  },
  
  checkUpdate() {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager()
      
      // 检查更新
      updateManager.onCheckForUpdate((res) => {
        if (res.hasUpdate) {
          console.log('发现新版本')
        }
      })
      
      // 下载完成
      updateManager.onUpdateReady(() => {
        wx.showModal({
          title: '更新提示',
          content: '新版本已准备好，是否重启应用？',
          success: (res) => {
            if (res.confirm) {
              updateManager.applyUpdate()
            }
          }
        })
      })
      
      // 更新失败
      updateManager.onUpdateFailed(() => {
        wx.showModal({
          title: '更新失败',
          content: '新版本下载失败，请删除小程序后重新搜索打开',
          showCancel: false
        })
      })
    } else {
      // 低版本兼容
      wx.showModal({
        title: '提示',
        content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
      })
    }
  }
})
```

### 7.2 版本对比

```javascript
// utils/version.js
export function compareVersion(v1, v2) {
  v1 = v1.split('.')
  v2 = v2.split('.')
  const len = Math.max(v1.length, v2.length)
  
  while (v1.length < len) {
    v1.push('0')
  }
  while (v2.length < len) {
    v2.push('0')
  }
  
  for (let i = 0; i < len; i++) {
    const num1 = parseInt(v1[i])
    const num2 = parseInt(v2[i])
    
    if (num1 > num2) {
      return 1
    } else if (num1 < num2) {
      return -1
    }
  }
  
  return 0
}

// 使用
const currentVersion = '1.2.3'
const minVersion = '1.2.0'

if (compareVersion(currentVersion, minVersion) >= 0) {
  console.log('版本满足要求')
}
```

---

## 8. CI/CD自动化

### 8.1 GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy MiniProgram

on:
  push:
    branches:
      - main
      - develop

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      
      - name: Install dependencies
        run: npm install
      
      - name: Build
        run: npm run build
      
      - name: Upload to WeChat
        uses: wechat-miniprogram/action-upload@v1
        with:
          project-path: ./miniprogram
          version: ${{ github.ref_name }}
          desc: ${{ github.event.head_commit.message }}
          appid: ${{ secrets.WECHAT_APPID }}
          secret: ${{ secrets.WECHAT_SECRET }}
```

### 8.2 Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Upload') {
            steps {
                sh '''
                    cli upload \
                    --project ./miniprogram \
                    --version ${BUILD_NUMBER} \
                    --desc "CI/CD自动上传"
                '''
            }
        }
    }
}
```

---

## 9. 常见问题

### Q1: 如何快速定位线上问题？
**A**:
1. 查看小程序后台错误日志
2. 使用监控系统查看错误上报
3. 查看用户反馈和评价
4. 使用真机调试复现问题

### Q2: 审核被拒怎么办？
**A**:
1. 查看拒绝原因
2. 根据原因修改代码
3. 重新提交审核
4. 如不理解，联系微信客服

### Q3: 如何实现灰度发布？
**A**:
1. 小程序后台 → 版本管理 → 审核版本
2. 点击"灰度发布"
3. 设置灰度比例
4. 监控数据，逐步扩大范围

### Q4: 如何回退版本？
**A**:
1. 小程序后台 → 版本管理 → 版本回退
2. 选择要回退的版本
3. 确认回退
4. 注意：回退后需要重新提交审核

---

## 参考资源

- 微信小程序发布流程文档
- 小程序审核规范
- 小程序版本管理指南
- CI/CD最佳实践

