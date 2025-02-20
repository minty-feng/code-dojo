# ArkUI组件开发

## 💡 核心结论

1. **ArkUI采用声明式开发，类似React/Flutter**
2. **组件分为基础组件和自定义组件**
3. **@Builder装饰器用于构建可复用的UI结构**
4. **@Styles和@Extend用于样式复用**
5. **状态管理通过@State、@Prop、@Link实现**

---

## 1. 基础组件

### 1.1 容器组件

```typescript
@Entry
@Component
struct ContainerDemo {
  build() {
    Column({ space: 10 }) {  // 垂直布局，间距10
      Row({ space: 5 }) {    // 水平布局
        Text('左')
        Text('中')
        Text('右')
      }
      
      Stack() {              // 堆叠布局
        Image($r('app.media.bg'))
        Text('叠加文字').fontColor(Color.White)
      }
      
      Flex({ direction: FlexDirection.Row, wrap: FlexWrap.Wrap }) {
        Text('Item1').width('30%')
        Text('Item2').width('30%')
        Text('Item3').width('30%')
      }
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}
```

### 1.2 基本组件

```typescript
@Entry
@Component
struct BasicComponents {
  @State text: string = ''
  @State checked: boolean = false
  @State sliderValue: number = 50

  build() {
    Column({ space: 20 }) {
      // 文本
      Text('标题文字')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor('#FF0000')
      
      // 图片
      Image($r('app.media.icon'))
        .width(100)
        .height(100)
        .objectFit(ImageFit.Contain)
      
      // 按钮
      Button('普通按钮')
        .type(ButtonType.Normal)
        .onClick(() => {
          console.log('按钮点击')
        })
      
      // 输入框
      TextInput({ placeholder: '请输入内容' })
        .onChange((value: string) => {
          this.text = value
        })
      
      // 复选框
      Checkbox()
        .select(this.checked)
        .onChange((value: boolean) => {
          this.checked = value
        })
      
      // 滑块
      Slider({
        value: this.sliderValue,
        min: 0,
        max: 100,
        step: 1
      })
        .onChange((value: number) => {
          this.sliderValue = value
        })
      
      // 进度条
      Progress({ value: this.sliderValue, total: 100, type: ProgressType.Linear })
        .width('80%')
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}
```

### 1.3 列表

```typescript
@Entry
@Component
struct ListDemo {
  private items: string[] = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']

  build() {
    Column() {
      List({ space: 10 }) {
        ForEach(this.items, (item: string, index: number) => {
          ListItem() {
            Row() {
              Text(item)
                .fontSize(16)
              Blank()
              Text(`#${index}`)
                .fontSize(12)
                .fontColor('#999')
            }
            .width('100%')
            .padding(15)
            .backgroundColor(Color.White)
            .borderRadius(8)
          }
          .onClick(() => {
            console.log('点击了:', item)
          })
        }, item => item)
      }
      .width('100%')
      .layoutWeight(1)
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
    .padding(10)
  }
}
```

---

## 2. 自定义组件

### 2.1 定义组件

```typescript
// components/UserCard.ets
@Component
export struct UserCard {
  @Prop name: string
  @Prop avatar: string
  @Link likeCount: number

  build() {
    Row({ space: 10 }) {
      Image(this.avatar)
        .width(50)
        .height(50)
        .borderRadius(25)
      
      Column({ space: 5 }) {
        Text(this.name)
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
        
        Row({ space: 5 }) {
          Text(`👍 ${this.likeCount}`)
          
          Button('点赞')
            .fontSize(12)
            .onClick(() => {
              this.likeCount++
            })
        }
      }
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .padding(10)
    .backgroundColor(Color.White)
    .borderRadius(8)
  }
}
```

### 2.2 使用组件

```typescript
// pages/Index.ets
import { UserCard } from '../components/UserCard'

@Entry
@Component
struct Index {
  @State likes: number = 10

  build() {
    Column() {
      UserCard({
        name: '张三',
        avatar: $r('app.media.avatar'),
        likeCount: $likes
      })
    }
    .padding(20)
  }
}
```

---

## 3. @Builder和@Styles

### 3.1 @Builder构建函数

```typescript
@Entry
@Component
struct BuilderDemo {
  @Builder
  CardBuilder(title: string, content: string) {
    Column({ space: 5 }) {
      Text(title)
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
      Text(content)
        .fontSize(14)
        .fontColor('#666')
    }
    .width('100%')
    .padding(15)
    .backgroundColor(Color.White)
    .borderRadius(8)
  }

  build() {
    Column({ space: 10 }) {
      this.CardBuilder('标题1', '内容1')
      this.CardBuilder('标题2', '内容2')
      this.CardBuilder('标题3', '内容3')
    }
    .padding(20)
  }
}
```

### 3.2 @Styles样式复用

```typescript
@Styles function cardStyle() {
  .width('100%')
  .padding(15)
  .backgroundColor(Color.White)
  .borderRadius(8)
  .shadow({ radius: 10, color: '#00000020' })
}

@Entry
@Component
struct StylesDemo {
  build() {
    Column({ space: 10 }) {
      Text('卡片1')
        .cardStyle()
      
      Text('卡片2')
        .cardStyle()
    }
  }
}
```

### 3.3 @Extend扩展组件

```typescript
@Extend(Text) function fancyText(fontSize: number, color: string) {
  .fontSize(fontSize)
  .fontColor(color)
  .fontWeight(FontWeight.Bold)
  .textShadow({ radius: 2, color: '#00000040' })
}

@Entry
@Component
struct ExtendDemo {
  build() {
    Column() {
      Text('标题')
        .fancyText(24, '#FF0000')
      
      Text('副标题')
        .fancyText(18, '#0000FF')
    }
  }
}
```

---

## 4. 路由导航

### 4.1 页面跳转

```typescript
import router from '@ohos.router'

@Entry
@Component
struct HomePage {
  build() {
    Column() {
      Button('跳转到详情页')
        .onClick(() => {
          router.pushUrl({
            url: 'pages/Detail',
            params: {
              id: 123,
              title: '商品详情'
            }
          })
        })
      
      Button('替换当前页')
        .onClick(() => {
          router.replaceUrl({
            url: 'pages/Other'
          })
        })
      
      Button('返回')
        .onClick(() => {
          router.back()
        })
    }
  }
}
```

### 4.2 接收参数

```typescript
// pages/Detail.ets
import router from '@ohos.router'

@Entry
@Component
struct Detail {
  @State id: number = 0
  @State title: string = ''

  aboutToAppear() {
    const params = router.getParams() as Record<string, Object>
    this.id = params.id as number
    this.title = params.title as string
  }

  build() {
    Column() {
      Text(`ID: ${this.id}`)
      Text(`标题: ${this.title}`)
    }
  }
}
```

---

## 5. 常见问题

### Q1: 如何在真机上调试？
**A**:
1. 设置 → 系统 → 开发人员选项 → USB调试
2. 连接电脑
3. DevEco Studio会自动识别

### Q2: 如何查看日志？
**A**:
```typescript
import hilog from '@ohos.hilog'

hilog.info(0x0000, 'MyTag', 'This is a log')
```

### Q3: 如何适配不同设备？
**A**: 使用响应式布局和资源限定符

---

## 参考资源

- HarmonyOS应用开发官方文档
- ArkTS语言规范
- DevEco Studio用户指南

