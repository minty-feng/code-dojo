# 卷积神经网络（CNN）

## 💡 核心结论

1. **卷积层通过局部连接和权值共享大幅减少参数**
2. **池化层降低空间维度，增强平移不变性**
3. **经典架构：LeNet → AlexNet → VGG → ResNet**
4. **残差连接解决深层网络退化问题**
5. **迁移学习可以用预训练模型快速解决新任务**

---

## 1. CNN基础

### 1.1 卷积操作

```
输入：5×5图像
卷积核：3×3
步长：1
输出：3×3特征图

卷积核滑动，逐个位置计算内积
```

```python
import torch
import torch.nn as nn

# 卷积层
conv = nn.Conv2d(
    in_channels=1,      # 输入通道数
    out_channels=32,    # 输出通道数（卷积核数量）
    kernel_size=3,      # 卷积核大小
    stride=1,           # 步长
    padding=1           # 填充
)

# 输入：[batch_size, channels, height, width]
x = torch.randn(1, 1, 28, 28)
output = conv(x)
print(output.shape)  # [1, 32, 28, 28]
```

### 1.2 池化层

```python
# 最大池化
pool = nn.MaxPool2d(kernel_size=2, stride=2)

# 平均池化
pool = nn.AvgPool2d(kernel_size=2, stride=2)

x = torch.randn(1, 32, 28, 28)
output = pool(x)
print(output.shape)  # [1, 32, 14, 14]
```

---

## 2. 经典CNN架构

### 2.1 LeNet-5（1998）

```python
class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
    
    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 16 * 4 * 4)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
```

### 2.2 AlexNet（2012）

```python
class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
```

### 2.3 ResNet（2015）

```python
class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)
    
    def forward(self, x):
        residual = x
        x = torch.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual  # 残差连接
        x = torch.relu(x)
        return x
```

---

## 3. 图像分类实战

```python
import torchvision
import torchvision.transforms as transforms

# 数据增强
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 加载CIFAR-10
trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform
)
trainloader = torch.utils.data.DataLoader(
    trainset, batch_size=128, shuffle=True, num_workers=2
)

# 训练
model = ResNet()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(trainloader):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    
    print(f'Epoch {epoch+1}, Loss: {running_loss/len(trainloader):.4f}')
```

---

## 参考资源

- 《深度学习》- Goodfellow
- PyTorch官方教程
- CS231n课程

