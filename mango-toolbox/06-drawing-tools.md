# 绘图工具集合

## 数据可视化工具

### Matplotlib
```python
import matplotlib.pyplot as plt
import numpy as np

# 基础绘图
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='sin(x)')
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.title('正弦函数')
plt.legend()
plt.grid(True)
plt.show()

# 子图
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0,0].plot(x, np.sin(x))
axes[0,1].plot(x, np.cos(x))
axes[1,0].plot(x, np.tan(x))
axes[1,1].plot(x, np.exp(x))
plt.tight_layout()
plt.show()

# 散点图
plt.scatter(x, y, c=y, cmap='viridis', alpha=0.7)
plt.colorbar()
plt.show()

# 直方图
plt.hist(np.random.normal(0, 1, 1000), bins=30, alpha=0.7)
plt.show()
```

### Seaborn
```python
import seaborn as sns
import pandas as pd

# 设置样式
sns.set_style("whitegrid")
sns.set_palette("husl")

# 数据准备
tips = sns.load_dataset("tips")

# 散点图
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="smoker")
plt.show()

# 箱线图
sns.boxplot(data=tips, x="day", y="total_bill", hue="smoker")
plt.show()

# 热力图
correlation_matrix = tips.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()

# 分布图
sns.displot(data=tips, x="total_bill", hue="smoker", kind="kde")
plt.show()

# 回归图
sns.regplot(data=tips, x="total_bill", y="tip")
plt.show()
```

### Plotly
```python
import plotly.express as px
import plotly.graph_objects as go

# 交互式散点图
fig = px.scatter(tips, x="total_bill", y="tip", color="smoker", 
                 title="账单与小费关系")
fig.show()

# 3D散点图
fig = go.Figure(data=[go.Scatter3d(
    x=tips['total_bill'],
    y=tips['tip'],
    z=tips['size'],
    mode='markers',
    marker=dict(size=5, color=tips['tip'], colorscale='Viridis')
)])
fig.show()

# 动态图表
fig = px.line(x=range(10), y=np.random.randn(10).cumsum())
fig.show()

# 地图
fig = px.scatter_mapbox(tips, lat="lat", lon="lon", 
                        color="total_bill", size="tip")
fig.update_layout(mapbox_style="open-street-map")
fig.show()
```

## Web前端图表库

### Chart.js
```javascript
// 基础柱状图
const ctx = document.getElementById('myChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['一月', '二月', '三月', '四月'],
        datasets: [{
            label: '销售额',
            data: [12, 19, 3, 5],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// 折线图
const lineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1月', '2月', '3月', '4月', '5月'],
        datasets: [{
            label: '用户增长',
            data: [65, 59, 80, 81, 56],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    }
});

// 饼图
const pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Chrome', 'Firefox', 'Safari', 'Edge'],
        datasets: [{
            data: [65, 20, 10, 5],
            backgroundColor: [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0'
            ]
        }]
    }
});
```

### D3.js
```javascript
// SVG容器
const svg = d3.select("body")
    .append("svg")
    .attr("width", 400)
    .attr("height", 300);

// 数据
const data = [10, 20, 30, 40, 50];

// 比例尺
const xScale = d3.scaleBand()
    .domain(d3.range(data.length))
    .range([0, 400])
    .padding(0.1);

const yScale = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([300, 0]);

// 绘制柱状图
svg.selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", (d, i) => xScale(i))
    .attr("y", d => yScale(d))
    .attr("width", xScale.bandwidth())
    .attr("height", d => 300 - yScale(d))
    .attr("fill", "steelblue");

// 添加标签
svg.selectAll("text")
    .data(data)
    .enter()
    .append("text")
    .text(d => d)
    .attr("x", (d, i) => xScale(i) + xScale.bandwidth() / 2)
    .attr("y", d => yScale(d) - 5)
    .attr("text-anchor", "middle");

// 力导向图
const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));
```

## 专业绘图工具

### Gnuplot
```gnuplot
# 基础绘图
set terminal png
set output 'plot.png'
set title '函数图像'
set xlabel 'X'
set ylabel 'Y'
set grid

plot sin(x) with lines title 'sin(x)', \
     cos(x) with lines title 'cos(x)'

# 3D绘图
set terminal png
set output '3d.png'
set title '3D Surface'
set xlabel 'X'
set ylabel 'Y'
set zlabel 'Z'

splot sin(x)*cos(y)

# 数据文件绘图
set terminal png
set output 'data.png'
plot 'data.txt' using 1:2 with points title 'Data Points'

# 多面板图
set multiplot layout 2,2
plot sin(x)
plot cos(x)
plot tan(x)
plot exp(x)
unset multiplot
```

### Graphviz
```dot
# 有向图
digraph G {
    A -> B
    B -> C
    C -> D
    D -> A
    
    A [label="开始"]
    B [label="处理"]
    C [label="验证"]
    D [label="结束"]
}

# 无向图
graph G {
    A -- B
    B -- C
    C -- D
    D -- A
    
    A [shape=box]
    B [shape=circle]
    C [shape=diamond]
    D [shape=triangle]
}

# 流程图
digraph flowchart {
    start [shape=ellipse, label="开始"]
    input [shape=box, label="输入数据"]
    process [shape=box, label="处理数据"]
    decision [shape=diamond, label="是否有效?"]
    output [shape=box, label="输出结果"]
    end [shape=ellipse, label="结束"]
    
    start -> input
    input -> process
    process -> decision
    decision ->|是| output
    decision ->|否| input
    output -> end
}
```

## 在线绘图工具

### Draw.io (diagrams.net)
```xml
<!-- 流程图示例 -->
<mxfile host="app.diagrams.net">
  <diagram name="流程图">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="开始" style="ellipse;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="364" y="40" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="处理" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="364" y="140" width="100" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="结束" style="ellipse;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="364" y="240" width="100" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Mermaid
```mermaid
graph TD
    A[开始] --> B{条件判断}
    B -->|是| C[处理A]
    B -->|否| D[处理B]
    C --> E[输出结果]
    D --> E
    E --> F[结束]

sequenceDiagram
    participant A as 用户
    participant B as 服务器
    participant C as 数据库
    
    A->>B: 发送请求
    B->>C: 查询数据
    C-->>B: 返回数据
    B-->>A: 返回响应

gantt
    title 项目时间表
    dateFormat  YYYY-MM-DD
    section 设计
    需求分析    :done, des1, 2024-01-01, 2024-01-07
    原型设计    :done, des2, 2024-01-08, 2024-01-14
    section 开发
    前端开发    :active, dev1, 2024-01-15, 2024-02-15
    后端开发    :dev2, 2024-01-20, 2024-02-20
    section 测试
    单元测试    :test1, 2024-02-21, 2024-02-28
    集成测试    :test2, 2024-03-01, 2024-03-07
```

## 科学计算绘图

### MATLAB
```matlab
% 基础绘图
x = 0:0.1:2*pi;
y1 = sin(x);
y2 = cos(x);

figure;
plot(x, y1, 'r-', 'LineWidth', 2);
hold on;
plot(x, y2, 'b--', 'LineWidth', 2);
xlabel('X');
ylabel('Y');
title('三角函数');
legend('sin(x)', 'cos(x)');
grid on;

% 3D绘图
[X, Y] = meshgrid(-2:0.1:2, -2:0.1:2);
Z = X.^2 + Y.^2;
figure;
surf(X, Y, Z);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('抛物面');

% 子图
figure;
subplot(2, 2, 1);
plot(x, y1);
title('sin(x)');

subplot(2, 2, 2);
plot(x, y2);
title('cos(x)');

subplot(2, 2, 3);
plot(x, tan(x));
title('tan(x)');

subplot(2, 2, 4);
plot(x, exp(x));
title('exp(x)');
```

### R语言
```r
# 基础绘图
x <- seq(0, 2*pi, length.out=100)
y1 <- sin(x)
y2 <- cos(x)

plot(x, y1, type="l", col="red", lwd=2, 
     xlab="X", ylab="Y", main="三角函数")
lines(x, y2, col="blue", lwd=2)
legend("topright", legend=c("sin(x)", "cos(x)"), 
       col=c("red", "blue"), lwd=2)

# ggplot2
library(ggplot2)
library(dplyr)

data <- data.frame(x=x, sin=y1, cos=y2) %>%
  tidyr::pivot_longer(cols=c(sin, cos), names_to="func", values_to="y")

ggplot(data, aes(x=x, y=y, color=func)) +
  geom_line(size=1) +
  labs(title="三角函数", x="X", y="Y") +
  theme_minimal()

# 散点图
ggplot(mtcars, aes(x=wt, y=mpg, color=factor(cyl))) +
  geom_point(size=3) +
  geom_smooth(method="lm", se=FALSE) +
  labs(title="汽车重量与油耗关系", x="重量", y="油耗")
```

## 设计工具

### Figma
```javascript
// Figma API示例
const figma = require('figma-api');

const api = new figma.Api({
    personalAccessToken: 'your-token'
});

// 获取文件
api.getFile('file-id').then(data => {
    console.log(data);
});

// 获取节点
api.getNode('file-id', 'node-id').then(data => {
    console.log(data);
});
```

### Adobe Illustrator脚本
```javascript
// AI脚本示例
var doc = app.activeDocument;
var artboard = doc.artboards[0];

// 创建矩形
var rect = doc.pathItems.rectangle(0, 0, 100, 100);

// 设置颜色
rect.fillColor = doc.swatches[0].color;

// 创建文本
var textFrame = doc.textFrames.add();
textFrame.contents = "Hello World";
textFrame.position = [50, 50];
```

## 命令行绘图

### ASCII艺术
```bash
# 使用figlet创建ASCII艺术
figlet "Hello World"

# 使用cowsay
cowsay "Hello World"

# 使用boxes
echo "Hello World" | boxes -d diamond

# 使用toilet
toilet -f big "Hello World"
```

### 终端图表
```bash
# 使用spark创建迷你图表
spark 1 2 3 4 5 4 3 2 1

# 使用grapheasy创建ASCII图表
echo "A -> B -> C" | grapheasy

# 使用termgraph
termgraph data.txt
```

## 实用技巧

### 颜色搭配
```python
# 颜色调色板
import matplotlib.pyplot as plt
import seaborn as sns

# 设置调色板
sns.set_palette("husl")  # 彩虹色
sns.set_palette("Set2")  # 柔和色
sns.set_palette("viridis")  # 科学色

# 自定义颜色
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
plt.bar(range(5), [1,2,3,4,5], color=colors)
```

### 图表优化
```python
# 图表美化
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
```

### 导出设置
```python
# 高质量导出
plt.savefig('chart.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')

# 矢量格式
plt.savefig('chart.svg', format='svg', bbox_inches='tight')

# PDF格式
plt.savefig('chart.pdf', format='pdf', bbox_inches='tight')
```

