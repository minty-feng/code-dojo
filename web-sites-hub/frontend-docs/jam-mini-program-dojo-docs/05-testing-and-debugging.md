# 测试与调试

## 💡 核心结论

1. **小程序测试包括单元测试、集成测试、端到端测试**
2. **开发者工具提供调试器、性能分析、网络监控等功能**
3. **真机调试是发现问题的关键，不同机型表现可能不同**
4. **Mock数据和测试工具可以提升开发效率**
5. **自动化测试可以保证代码质量和稳定性**

---

## 1. 开发者工具调试

### 1.1 调试器使用

**Console面板**：
```javascript
// 基础日志
console.log('普通日志', data)
console.info('信息日志', data)
console.warn('警告日志', data)
console.error('错误日志', data)

// 分组日志
console.group('分组1')
console.log('内容1')
console.log('内容2')
console.groupEnd()

// 表格显示
console.table([
  { name: '张三', age: 25 },
  { name: '李四', age: 30 }
])

// 计时
console.time('timer')
// ... 代码执行
console.timeEnd('timer')  // 输出: timer: 123.456ms
```

**Sources面板**：
```javascript
// 断点调试
// 1. 在代码行号左侧点击设置断点
// 2. 触发代码执行
// 3. 查看变量值、调用栈
// 4. 单步执行（F10）、进入函数（F11）、跳出函数（Shift+F11）

// 条件断点
// 右键断点 → 编辑断点 → 设置条件
// 例如：index > 10
```

**Network面板**：
```javascript
// 查看所有网络请求
// - 请求URL、方法、状态码
// - 请求头、响应头
// - 请求参数、响应数据
// - 请求耗时

// 过滤请求
// - 按类型：XHR、Image、WebSocket
// - 按关键词搜索
```

### 1.2 性能分析

```javascript
// Performance面板
// 1. 点击"开始录制"
// 2. 执行操作
// 3. 点击"停止录制"
// 4. 查看性能数据：
//    - FPS（帧率）
//    - CPU使用率
//    - 内存占用
//    - setData调用次数
//    - 渲染时间
```

### 1.3 存储面板

```javascript
// Storage面板
// 查看：
// - Local Storage
// - Session Storage
// - 小程序Storage（wx.setStorage存储的数据）

// 可以：
// - 查看所有key-value
// - 编辑、删除数据
// - 清空所有数据
```

---

## 2. 真机调试

### 2.1 预览功能

```bash
# 开发者工具 → 预览
# 生成二维码 → 微信扫码 → 真机预览

# 注意事项：
# 1. 手机和电脑需在同一网络
# 2. 需要登录开发者账号
# 3. 可以查看控制台日志
```

### 2.2 真机调试

```bash
# 开发者工具 → 真机调试
# 生成二维码 → 微信扫码 → 开启调试

# 功能：
# 1. 实时查看控制台日志
# 2. 查看网络请求
# 3. 查看Storage数据
# 4. 查看页面结构
# 5. 查看元素样式
```

### 2.3 远程调试

```javascript
// 小程序后台 → 开发 → 开发管理 → 开发设置 → 远程调试

// 使用场景：
// 1. 真机预览无法复现问题
// 2. 需要查看详细日志
// 3. 需要调试特定功能
```

### 2.4 常见真机问题

**1. 样式问题**：
```css
/* 不同机型可能表现不同 */
/* 使用rpx单位，避免使用px */
.container {
  width: 750rpx;  /* ✅ 正确 */
  width: 375px;   /* ❌ 可能在不同机型显示异常 */
}

/* 测试不同机型 */
/* iPhone、Android、iPad */
```

**2. 兼容性问题**：
```javascript
// 检查API支持
if (wx.canIUse('getUpdateManager')) {
  // 使用新API
} else {
  // 降级方案
}

// 检查基础库版本
const systemInfo = wx.getSystemInfoSync()
console.log('基础库版本', systemInfo.SDKVersion)

// 最低基础库版本要求
// app.json
{
  "libVersion": "2.19.4"
}
```

**3. 网络问题**：
```javascript
// 真机网络环境可能不同
// 测试：
// - WiFi环境
// - 4G/5G环境
// - 弱网环境

// 模拟弱网
// 开发者工具 → 设置 → 项目设置 → 不校验合法域名
```

---

## 3. 单元测试

### 3.1 测试框架配置

```bash
# 安装依赖
npm install --save-dev jest @miniprogram/jest

# 或使用miniprogram-simulate
npm install --save-dev miniprogram-simulate
```

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "preset": "@miniprogram/jest",
    "testEnvironment": "jsdom",
    "testMatch": ["**/__tests__/**/*.test.js"],
    "collectCoverageFrom": [
      "**/*.js",
      "!**/node_modules/**",
      "!**/dist/**"
    ]
  }
}
```

### 3.2 工具函数测试

```javascript
// utils/format.test.js
import { formatPrice, formatDate } from './format.js'

describe('format工具函数', () => {
  test('formatPrice应该正确格式化价格', () => {
    expect(formatPrice(100)).toBe('¥1.00')
    expect(formatPrice(1234)).toBe('¥12.34')
    expect(formatPrice(0)).toBe('¥0.00')
  })
  
  test('formatDate应该正确格式化日期', () => {
    const date = new Date('2024-01-01')
    expect(formatDate(date)).toBe('2024-01-01')
  })
})
```

```javascript
// utils/format.js
export function formatPrice(price) {
  return '¥' + (price / 100).toFixed(2)
}

export function formatDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
```

### 3.3 API测试

```javascript
// utils/request.test.js
import { http } from './request.js'

// Mock wx.request
jest.mock('wx', () => ({
  request: jest.fn()
}))

describe('request工具', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })
  
  test('get请求应该正确调用wx.request', async () => {
    const mockData = { list: [1, 2, 3] }
    wx.request.mockImplementation((options) => {
      options.success({ data: mockData })
    })
    
    const result = await http.get('/api/products')
    
    expect(wx.request).toHaveBeenCalledWith(
      expect.objectContaining({
        url: expect.stringContaining('/api/products'),
        method: 'GET'
      })
    )
    expect(result).toEqual(mockData)
  })
  
  test('请求失败应该抛出错误', async () => {
    wx.request.mockImplementation((options) => {
      options.fail({ errMsg: 'request:fail' })
    })
    
    await expect(http.get('/api/products')).rejects.toThrow()
  })
})
```

### 3.4 组件测试

```javascript
// components/product-item/product-item.test.js
const simulate = require('miniprogram-simulate')

describe('ProductItem组件', () => {
  let comp
  
  beforeEach(() => {
    comp = simulate.load('/components/product-item/product-item')
  })
  
  test('应该正确显示商品信息', () => {
    const product = {
      id: 1,
      name: '测试商品',
      price: 10000
    }
    
    comp.setData({ product })
    comp.attach(document.body)
    
    expect(comp.querySelector('.product-name').textContent).toBe('测试商品')
    expect(comp.querySelector('.product-price').textContent).toBe('¥100.00')
  })
  
  test('点击应该触发tap事件', () => {
    const product = { id: 1, name: '测试商品', price: 10000 }
    comp.setData({ product })
    comp.attach(document.body)
    
    const tapHandler = jest.fn()
    comp.addEventListener('tap', tapHandler)
    
    comp.querySelector('.product-item').dispatchEvent('tap')
    
    expect(tapHandler).toHaveBeenCalledWith(
      expect.objectContaining({
        detail: { id: 1 }
      })
    )
  })
})
```

---

## 4. 集成测试

### 4.1 页面流程测试

```javascript
// tests/pages/index.test.js
const simulate = require('miniprogram-simulate')

describe('首页流程测试', () => {
  let page
  
  beforeEach(() => {
    page = simulate.load('/pages/index/index')
  })
  
  test('页面加载应该请求数据', async () => {
    const mockRequest = jest.fn()
    wx.request = mockRequest
    
    page.triggerLifeTime('onLoad')
    
    await simulate.sleep(100)
    
    expect(mockRequest).toHaveBeenCalled()
  })
  
  test('下拉刷新应该重新加载数据', async () => {
    const mockRequest = jest.fn()
    wx.request = mockRequest
    
    page.triggerLifeTime('onPullDownRefresh')
    
    await simulate.sleep(100)
    
    expect(mockRequest).toHaveBeenCalled()
    expect(wx.stopPullDownRefresh).toHaveBeenCalled()
  })
  
  test('上拉加载应该加载更多', async () => {
    page.setData({
      list: Array(10).fill(0).map((_, i) => ({ id: i }))
    })
    
    const mockRequest = jest.fn()
    wx.request = mockRequest
    
    page.triggerLifeTime('onReachBottom')
    
    await simulate.sleep(100)
    
    expect(mockRequest).toHaveBeenCalled()
  })
})
```

### 4.2 用户交互测试

```javascript
// tests/user-interaction.test.js
describe('用户交互测试', () => {
  test('点击按钮应该触发相应操作', () => {
    const page = simulate.load('/pages/index/index')
    page.attach(document.body)
    
    const button = page.querySelector('.submit-button')
    const submitHandler = jest.fn()
    
    page.instance.onSubmit = submitHandler
    button.dispatchEvent('tap')
    
    expect(submitHandler).toHaveBeenCalled()
  })
  
  test('输入框输入应该更新数据', () => {
    const page = simulate.load('/pages/index/index')
    page.attach(document.body)
    
    const input = page.querySelector('.search-input')
    input.dispatchEvent('input', {
      detail: { value: '测试' }
    })
    
    expect(page.data.keyword).toBe('测试')
  })
})
```

---

## 5. E2E测试

### 5.1 自动化测试工具

```bash
# 安装miniprogram-automator
npm install --save-dev miniprogram-automator
```

```javascript
// tests/e2e/index.test.js
const automator = require('miniprogram-automator')

describe('E2E测试', () => {
  let miniProgram
  let page
  
  beforeAll(async () => {
    miniProgram = await automator.launch({
      projectPath: './miniprogram',
      cliPath: '/Applications/wechatwebdevtools.app/Contents/MacOS/cli'
    })
    
    page = await miniProgram.reLaunch('/pages/index/index')
    await page.waitFor(1000)
  })
  
  afterAll(async () => {
    await miniProgram.close()
  })
  
  test('应该正确显示首页内容', async () => {
    const title = await page.$('.page-title')
    const text = await title.text()
    
    expect(text).toBe('首页')
  })
  
  test('应该能够搜索商品', async () => {
    const searchInput = await page.$('.search-input')
    await searchInput.input('手机')
    
    const searchButton = await page.$('.search-button')
    await searchButton.tap()
    
    await page.waitFor(2000)
    
    const products = await page.$$('.product-item')
    expect(products.length).toBeGreaterThan(0)
  })
  
  test('应该能够添加商品到购物车', async () => {
    const addButton = await page.$('.add-to-cart')
    await addButton.tap()
    
    await page.waitFor(500)
    
    const toast = await page.$('.weui-toast')
    const toastText = await toast.text()
    
    expect(toastText).toContain('添加成功')
  })
})
```

---

## 6. Mock数据

### 6.1 本地Mock

```javascript
// mock/api.js
export const mockData = {
  products: [
    { id: 1, name: '商品1', price: 10000 },
    { id: 2, name: '商品2', price: 20000 }
  ],
  
  user: {
    id: 1,
    name: '测试用户',
    avatar: 'https://example.com/avatar.png'
  }
}

// utils/request.js
import { mockData } from '../mock/api.js'

const isDev = process.env.NODE_ENV === 'development'
const useMock = isDev && wx.getStorageSync('useMock')

export function request(options) {
  if (useMock) {
    return Promise.resolve(mockData[options.url])
  }
  
  return new Promise((resolve, reject) => {
    wx.request({
      url: options.url,
      success: resolve,
      fail: reject
    })
  })
}
```

### 6.2 Mock服务

```javascript
// 使用mockjs
// npm install mockjs

// mock/index.js
import Mock from 'mockjs'

Mock.mock('/api/products', 'get', {
  code: 0,
  data: {
    list: Mock.mock({
      'list|10': [{
        'id|+1': 1,
        'name': '@ctitle(5, 10)',
        'price|1000-10000': 1,
        'image': '@image("200x200")'
      }]
    })
  }
})

// 在开发环境启用
if (process.env.NODE_ENV === 'development') {
  require('./mock')
}
```

---

## 7. 调试技巧

### 7.1 条件断点

```javascript
// 只在特定条件下暂停
// 例如：只在index > 10时暂停
for (let i = 0; i < 100; i++) {
  // 设置条件断点：i > 10
  console.log(i)
}
```

### 7.2 日志分级

```javascript
// utils/logger.js
const DEBUG = wx.getStorageSync('debug') === 'true'

export const logger = {
  debug(...args) {
    if (DEBUG) {
      console.log('[DEBUG]', ...args)
    }
  },
  
  info(...args) {
    console.log('[INFO]', ...args)
  },
  
  error(...args) {
    console.error('[ERROR]', ...args)
  }
}
```

### 7.3 性能分析

```javascript
// utils/performance.js
export function measure(name, fn) {
  const start = Date.now()
  const result = fn()
  const end = Date.now()
  
  console.log(`[Performance] ${name}: ${end - start}ms`)
  
  return result
}

// 使用
measure('loadData', () => {
  this.loadData()
})
```

### 7.4 数据快照

```javascript
// 保存数据快照用于调试
export function snapshot(data, name = 'snapshot') {
  const snapshotData = {
    timestamp: Date.now(),
    data: JSON.parse(JSON.stringify(data))
  }
  
  wx.setStorageSync(`snapshot_${name}`, snapshotData)
  console.log(`[Snapshot] ${name} saved`, snapshotData)
}

// 使用
snapshot(this.data, 'pageData')
```

---

## 8. 测试最佳实践

### 8.1 测试覆盖率

```bash
# 运行测试并生成覆盖率报告
npm run test:coverage

# 目标覆盖率：
# - 语句覆盖率 > 80%
# - 分支覆盖率 > 75%
# - 函数覆盖率 > 80%
```

### 8.2 测试金字塔

```
        /\
       /E2E\        ← 少量端到端测试
      /------\
     /集成测试\      ← 适量集成测试
    /----------\
   /  单元测试  \    ← 大量单元测试
  /--------------\
```

### 8.3 测试命名规范

```javascript
// ✅ 好的测试命名
describe('ProductItem组件', () => {
  test('应该正确显示商品名称和价格', () => {})
  test('点击商品应该跳转到详情页', () => {})
  test('价格应该格式化为两位小数', () => {})
})

// ❌ 不好的测试命名
describe('test', () => {
  test('test1', () => {})
  test('test2', () => {})
})
```

### 8.4 测试隔离

```javascript
// 每个测试应该独立，不依赖其他测试
describe('用户登录', () => {
  beforeEach(() => {
    // 每个测试前重置状态
    wx.clearStorageSync()
  })
  
  test('应该能够登录', () => {
    // 测试代码
  })
  
  test('登录失败应该显示错误', () => {
    // 测试代码
  })
})
```

---

## 9. 常见问题

### Q1: 真机调试看不到日志？
**A**:
1. 确认开启了真机调试模式
2. 检查手机和电脑是否在同一网络
3. 尝试重启开发者工具
4. 检查防火墙设置

### Q2: 如何测试不同机型？
**A**:
1. 使用真机预览功能
2. 准备多台测试设备
3. 使用云测试平台（如Testin、WeTest）

### Q3: 单元测试如何Mock wx API？
**A**:
```javascript
// 使用jest.mock
jest.mock('wx', () => ({
  request: jest.fn(),
  showToast: jest.fn()
}))
```

### Q4: 如何测试异步操作？
**A**:
```javascript
test('应该异步加载数据', async () => {
  const promise = loadData()
  await expect(promise).resolves.toEqual(expectedData)
})
```

---

## 参考资源

- 微信开发者工具文档
- Jest测试框架文档
- miniprogram-simulate文档
- 小程序测试最佳实践

