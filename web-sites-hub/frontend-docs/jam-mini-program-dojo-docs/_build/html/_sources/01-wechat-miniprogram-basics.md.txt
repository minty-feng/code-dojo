# 基础

## 💡 核心结论

1. **小程序采用双线程架构：逻辑层(JSCore)和视图层(WebView)分离**
2. **WXML是类HTML语法，WXSS是类CSS语法，支持rpx响应式单位**
3. **生命周期分为应用生命周期和页面生命周期**
4. **小程序不支持DOM操作，数据驱动视图更新**
5. **小程序包体积限制2MB，分包后主包不超过2MB**

---

## 1. 快速开始

### 1.1 注册与配置

```bash
# 1. 注册小程序账号
https://mp.weixin.qq.com/

# 2. 获取AppID
开发 → 开发管理 → 开发设置 → AppID

# 3. 下载开发者工具
https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
```

### 1.2 项目结构

```
my-miniprogram/
├── pages/                  # 页面目录
│   ├── index/
│   │   ├── index.js       # 页面逻辑
│   │   ├── index.json     # 页面配置
│   │   ├── index.wxml     # 页面结构
│   │   └── index.wxss     # 页面样式
│   └── logs/
│       ├── logs.js
│       ├── logs.json
│       ├── logs.wxml
│       └── logs.wxss
├── utils/                  # 工具函数
│   └── util.js
├── app.js                  # 应用逻辑
├── app.json                # 全局配置
├── app.wxss                # 全局样式
├── project.config.json     # 项目配置
└── sitemap.json            # 索引配置
```

### 1.3 全局配置 (app.json)

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"
  ],
  "window": {
    "backgroundTextStyle": "light",
    "navigationBarBackgroundColor": "#fff",
    "navigationBarTitleText": "我的小程序",
    "navigationBarTextStyle": "black",
    "enablePullDownRefresh": true,
    "backgroundColor": "#f8f8f8"
  },
  "tabBar": {
    "color": "#999",
    "selectedColor": "#07c160",
    "backgroundColor": "#fff",
    "borderStyle": "black",
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "images/home.png",
        "selectedIconPath": "images/home-active.png"
      },
      {
        "pagePath": "pages/profile/profile",
        "text": "我的",
        "iconPath": "images/profile.png",
        "selectedIconPath": "images/profile-active.png"
      }
    ]
  },
  "networkTimeout": {
    "request": 10000,
    "downloadFile": 10000
  },
  "debug": false
}
```

---

## 2. 页面开发

### 2.1 WXML 语法

**数据绑定**：
```html
<!-- pages/index/index.wxml -->
<view class="container">
  <!-- 文本绑定 -->
  <text>{{message}}</text>
  
  <!-- 属性绑定 -->
  <image src="{{imgUrl}}" mode="aspectFit"></image>
  
  <!-- 运算 -->
  <text>{{a + b}}</text>
  <text>{{flag ? '真' : '假'}}</text>
  
  <!-- 组合 -->
  <view class="item-{{index}}">Item {{index + 1}}</view>
</view>
```

**列表渲染**：
```html
<!-- wx:for -->
<view wx:for="{{items}}" wx:key="id">
  {{index}}: {{item.name}}
</view>

<!-- 自定义变量名 -->
<view wx:for="{{items}}" wx:for-item="product" wx:for-index="idx" wx:key="id">
  {{idx}}: {{product.name}}
</view>

<!-- 嵌套循环 -->
<view wx:for="{{categories}}" wx:key="id">
  <text>{{item.name}}</text>
  <view wx:for="{{item.products}}" wx:for-item="product" wx:key="id">
    {{product.name}}
  </view>
</view>
```

**条件渲染**：
```html
<!-- wx:if -->
<view wx:if="{{condition}}">显示内容</view>
<view wx:elif="{{condition2}}">其他内容</view>
<view wx:else>默认内容</view>

<!-- hidden -->
<view hidden="{{!show}}">隐藏内容</view>

<!-- block -->
<block wx:if="{{true}}">
  <view>内容1</view>
  <view>内容2</view>
</block>
```

**模板**：
```html
<!-- 定义模板 -->
<template name="msgItem">
  <view>
    <text>{{index}}: {{msg}}</text>
    <text>Time: {{time}}</text>
  </view>
</template>

<!-- 使用模板 -->
<template is="msgItem" data="{{...item}}" />
```

### 2.2 WXSS 样式

```css
/* pages/index/index.wxss */

/* rpx：响应式单位（750rpx = 屏幕宽度） */
.container {
  width: 750rpx;
  padding: 20rpx;
}

/* 全局选择器 */
page {
  background-color: #f8f8f8;
  font-size: 28rpx;
}

/* 类选择器 */
.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

/* ID选择器 */
#header {
  height: 100rpx;
}

/* 伪类 */
.button:active {
  opacity: 0.7;
}

/* Flex布局 */
.flex-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

/* 导入样式 */
@import "../../styles/common.wxss";
```

### 2.3 页面逻辑 (JS)

```javascript
// pages/index/index.js
Page({
  // 页面数据
  data: {
    message: 'Hello World',
    count: 0,
    items: [],
    userInfo: {}
  },
  
  // 生命周期函数
  onLoad(options) {
    console.log('页面加载', options)
    this.loadData()
  },
  
  onShow() {
    console.log('页面显示')
  },
  
  onReady() {
    console.log('页面初次渲染完成')
  },
  
  onHide() {
    console.log('页面隐藏')
  },
  
  onUnload() {
    console.log('页面卸载')
  },
  
  // 下拉刷新
  onPullDownRefresh() {
    this.loadData()
    wx.stopPullDownRefresh()
  },
  
  // 上拉加载
  onReachBottom() {
    this.loadMore()
  },
  
  // 分享
  onShareAppMessage() {
    return {
      title: '分享标题',
      path: '/pages/index/index',
      imageUrl: '/images/share.jpg'
    }
  },
  
  // 自定义方法
  loadData() {
    wx.showLoading({ title: '加载中' })
    
    wx.request({
      url: 'https://api.example.com/data',
      success: (res) => {
        this.setData({
          items: res.data
        })
      },
      complete: () => {
        wx.hideLoading()
      }
    })
  },
  
  // 事件处理
  handleTap(e) {
    console.log('点击事件', e)
    this.setData({
      count: this.data.count + 1
    })
  },
  
  handleInput(e) {
    this.setData({
      message: e.detail.value
    })
  }
})
```

---

## 3. 生命周期

### 3.1 应用生命周期

```javascript
// app.js
App({
  // 全局数据
  globalData: {
    userInfo: null,
    token: ''
  },
  
  // 小程序初始化
  onLaunch(options) {
    console.log('小程序启动', options)
    // 场景值：options.scene
    // 启动参数：options.query
    
    // 检查更新
    this.checkUpdate()
    
    // 获取系统信息
    const systemInfo = wx.getSystemInfoSync()
    console.log(systemInfo)
  },
  
  // 小程序显示
  onShow(options) {
    console.log('小程序切前台', options)
  },
  
  // 小程序隐藏
  onHide() {
    console.log('小程序切后台')
  },
  
  // 错误监听
  onError(msg) {
    console.error('小程序错误', msg)
  },
  
  // 页面不存在
  onPageNotFound(res) {
    console.log('页面不存在', res)
    wx.redirectTo({
      url: '/pages/index/index'
    })
  },
  
  // 检查更新
  checkUpdate() {
    const updateManager = wx.getUpdateManager()
    
    updateManager.onCheckForUpdate((res) => {
      console.log('检查更新', res.hasUpdate)
    })
    
    updateManager.onUpdateReady(() => {
      wx.showModal({
        title: '更新提示',
        content: '新版本已准备好，是否重启应用？',
        success(res) {
          if (res.confirm) {
            updateManager.applyUpdate()
          }
        }
      })
    })
  }
})
```

### 3.2 页面生命周期流程

```
小程序启动
    ↓
App.onLaunch
    ↓
App.onShow
    ↓
Page.onLoad ────→ 页面加载，只调用一次
    ↓
Page.onShow ────→ 页面显示，每次切换都调用
    ↓
Page.onReady ───→ 初次渲染完成，只调用一次
    ↓
[用户操作]
    ↓
Page.onHide ────→ 页面隐藏
    ↓
Page.onUnload ──→ 页面卸载
```

---

## 4. 组件

### 4.1 视图容器

```html
<!-- view：块级容器 -->
<view class="container">
  <view class="item">Item 1</view>
  <view class="item">Item 2</view>
</view>

<!-- scroll-view：可滚动容器 -->
<scroll-view 
  scroll-y 
  style="height: 400rpx"
  bindscrolltolower="onReachBottom"
  enable-back-to-top
>
  <view wx:for="{{items}}" wx:key="id">{{item.name}}</view>
</scroll-view>

<!-- swiper：轮播图 -->
<swiper 
  indicator-dots 
  autoplay 
  interval="3000" 
  duration="500"
  circular
>
  <swiper-item wx:for="{{banners}}" wx:key="id">
    <image src="{{item.image}}" mode="aspectFill"></image>
  </swiper-item>
</swiper>
```

### 4.2 基础组件

```html
<!-- text：文本 -->
<text selectable user-select>可选择的文本</text>

<!-- image：图片 -->
<image 
  src="{{imgUrl}}" 
  mode="aspectFit"
  lazy-load
  bindload="onImageLoad"
  binderror="onImageError"
></image>

<!-- icon：图标 -->
<icon type="success" size="40" color="#07c160"></icon>

<!-- progress：进度条 -->
<progress percent="60" show-info stroke-width="4" activeColor="#07c160"></progress>

<!-- rich-text：富文本 -->
<rich-text nodes="{{htmlContent}}"></rich-text>
```

### 4.3 表单组件

```html
<form bindsubmit="onSubmit" bindreset="onReset">
  <!-- input：输入框 -->
  <input 
    type="text" 
    placeholder="请输入用户名"
    value="{{username}}"
    bindinput="onUsernameInput"
    maxlength="20"
  />
  
  <!-- textarea：多行输入 -->
  <textarea 
    placeholder="请输入内容"
    auto-height
    maxlength="200"
  ></textarea>
  
  <!-- button：按钮 -->
  <button type="primary" form-type="submit">提交</button>
  <button type="default" form-type="reset">重置</button>
  
  <!-- checkbox：复选框 -->
  <checkbox-group bindchange="onCheckboxChange">
    <label wx:for="{{items}}" wx:key="id">
      <checkbox value="{{item.value}}"/>{{item.name}}
    </label>
  </checkbox-group>
  
  <!-- radio：单选框 -->
  <radio-group bindchange="onRadioChange">
    <label wx:for="{{items}}" wx:key="id">
      <radio value="{{item.value}}"/>{{item.name}}
    </label>
  </radio-group>
  
  <!-- switch：开关 -->
  <switch checked="{{isChecked}}" bindchange="onSwitchChange"/>
  
  <!-- slider：滑块 -->
  <slider min="0" max="100" value="{{value}}" bindchange="onSliderChange"/>
  
  <!-- picker：选择器 -->
  <picker mode="selector" range="{{items}}" bindchange="onPickerChange">
    <view>{{items[index]}}</view>
  </picker>
</form>
```

### 4.4 导航组件

```html
<!-- navigator：页面跳转 -->
<navigator url="/pages/detail/detail?id=1">跳转到详情</navigator>
<navigator url="/pages/list/list" open-type="redirect">重定向</navigator>
<navigator url="/pages/other/other" open-type="switchTab">切换Tab</navigator>
```

### 4.5 自定义组件

**创建组件**：
```javascript
// components/product-item/product-item.js
Component({
  // 组件属性
  properties: {
    product: {
      type: Object,
      value: {}
    },
    showPrice: {
      type: Boolean,
      value: true
    }
  },
  
  // 组件数据
  data: {
    count: 0
  },
  
  // 组件生命周期
  lifetimes: {
    attached() {
      console.log('组件被添加到页面')
    },
    detached() {
      console.log('组件从页面移除')
    }
  },
  
  // 页面生命周期（组件所在页面）
  pageLifetimes: {
    show() {
      console.log('页面显示')
    },
    hide() {
      console.log('页面隐藏')
    }
  },
  
  // 组件方法
  methods: {
    onTap() {
      // 触发自定义事件
      this.triggerEvent('tap', {
        id: this.data.product.id
      })
    },
    
    onAdd() {
      this.setData({
        count: this.data.count + 1
      })
    }
  }
})
```

```html
<!-- components/product-item/product-item.wxml -->
<view class="product-item" bindtap="onTap">
  <image src="{{product.image}}" class="product-image"></image>
  <view class="product-info">
    <text class="product-name">{{product.name}}</text>
    <text class="product-desc">{{product.description}}</text>
    <view class="product-footer" wx:if="{{showPrice}}">
      <text class="product-price">¥{{product.price}}</text>
      <button size="mini" bindtap="onAdd">加购</button>
    </view>
  </view>
</view>
```

```css
/* components/product-item/product-item.wxss */
.product-item {
  display: flex;
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
}

.product-image {
  width: 200rpx;
  height: 200rpx;
  border-radius: 8rpx;
}

.product-info {
  flex: 1;
  margin-left: 20rpx;
}

.product-name {
  font-size: 32rpx;
  font-weight: bold;
}

.product-price {
  color: #ff5722;
  font-size: 36rpx;
}
```

```json
// components/product-item/product-item.json
{
  "component": true,
  "usingComponents": {}
}
```

**使用组件**：
```json
// pages/index/index.json
{
  "usingComponents": {
    "product-item": "/components/product-item/product-item"
  }
}
```

```html
<!-- pages/index/index.wxml -->
<view class="container">
  <product-item 
    wx:for="{{products}}" 
    wx:key="id"
    product="{{item}}"
    show-price="{{true}}"
    bind:tap="onProductTap"
  ></product-item>
</view>
```

```javascript
// pages/index/index.js
Page({
  data: {
    products: []
  },
  
  onProductTap(e) {
    const { id } = e.detail
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    })
  }
})
```

**组件通信**：
```javascript
// 父组件向子组件传值（通过properties）
// 子组件向父组件传值（通过triggerEvent）

// 获取父组件实例
const parent = this.getRelationNodes('../parent/parent')[0]
parent.someMethod()

// 组件间关系
// components/child/child.json
{
  "component": true,
  "relations": {
    "../parent/parent": {
      "type": "ancestor"
    }
  }
}
```

---

## 5. API

### 5.1 路由跳转

```javascript
// 保留当前页面，跳转
wx.navigateTo({
  url: '/pages/detail/detail?id=1'
})

// 关闭当前页面，跳转
wx.redirectTo({
  url: '/pages/result/result'
})

// 跳转到tabBar页面
wx.switchTab({
  url: '/pages/index/index'
})

// 关闭所有页面，跳转
wx.reLaunch({
  url: '/pages/home/home'
})

// 返回上一页
wx.navigateBack({
  delta: 1  // 返回的页面数
})
```

### 5.2 交互反馈

```javascript
// 显示提示
wx.showToast({
  title: '操作成功',
  icon: 'success',
  duration: 2000
})

// 显示模态对话框
wx.showModal({
  title: '提示',
  content: '确定要删除吗？',
  success(res) {
    if (res.confirm) {
      console.log('用户点击确定')
    } else if (res.cancel) {
      console.log('用户点击取消')
    }
  }
})

// 显示加载提示
wx.showLoading({
  title: '加载中',
  mask: true
})
wx.hideLoading()

// 显示操作菜单
wx.showActionSheet({
  itemList: ['选项1', '选项2', '选项3'],
  success(res) {
    console.log('用户点击了', res.tapIndex)
  }
})
```

### 5.3 数据缓存

```javascript
// 同步存储
wx.setStorageSync('key', 'value')
const value = wx.getStorageSync('key')
wx.removeStorageSync('key')
wx.clearStorageSync()

// 异步存储
wx.setStorage({
  key: 'userInfo',
  data: {name: '张三', age: 25},
  success() {
    console.log('存储成功')
  }
})

wx.getStorage({
  key: 'userInfo',
  success(res) {
    console.log(res.data)
  }
})

// 获取存储信息
wx.getStorageInfo({
  success(res) {
    console.log(res.keys)        // 所有key
    console.log(res.currentSize) // 当前大小（KB）
    console.log(res.limitSize)   // 限制大小（KB）
  }
})
```

---

## 6. 常见问题

### Q1: rpx和px的区别？
**A**: 
- `rpx`：响应式像素，750rpx = 屏幕宽度
- `px`：固定像素，不同屏幕显示大小不同
- iPhone6：375px = 750rpx

### Q2: setData的注意事项？
**A**:
1. 单次setData数据不超过1MB
2. 不要频繁调用（会阻塞渲染）
3. 只更新需要改变的数据
4. 避免在后台态调用

### Q3: 小程序包体积限制？
**A**:
- 整个小程序：不超过20MB
- 主包：不超过2MB
- 单个分包：不超过2MB

---

## 参考资源

- 微信小程序官方文档
- 微信开放社区
- 小程序示例代码

