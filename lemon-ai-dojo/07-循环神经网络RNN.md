# 循环神经网络（RNN）

## 💡 核心结论

1. **RNN通过隐藏状态处理序列数据**
2. **LSTM通过门控机制解决梯度消失问题**
3. **GRU是LSTM的简化版本，参数更少**
4. **双向RNN可以同时利用前后文信息**
5. **Seq2Seq架构是机器翻译的基础**

---

## 1. RNN基础

### 1.1 原理

```
h_t = tanh(W_hh * h_{t-1} + W_xh * x_t + b_h)
y_t = W_hy * h_t + b_y

h_t: 隐藏状态
x_t: 当前输入
y_t: 当前输出
```

### 1.2 PyTorch实现

```python
import torch
import torch.nn as nn

class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleRNN, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        # x: [batch_size, seq_len, input_size]
        h0 = torch.zeros(1, x.size(0), self.hidden_size)
        out, hn = self.rnn(x, h0)
        # out: [batch_size, seq_len, hidden_size]
        out = self.fc(out[:, -1, :])  # 只取最后一个时间步
        return out
```

---

## 2. LSTM

### 2.1 结构

```
遗忘门：f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
输入门：i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
输出门：o_t = σ(W_o · [h_{t-1}, x_t] + b_o)

候选值：C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)
细胞状态：C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t
隐藏状态：h_t = o_t ⊙ tanh(C_t)
```

### 2.2 实现

```python
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(
            input_size, 
            hidden_size, 
            num_layers, 
            batch_first=True,
            dropout=0.2
        )
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out, (hn, cn) = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

# 文本分类示例
model = LSTMModel(input_size=100, hidden_size=128, num_layers=2, output_size=2)
```

---

## 3. 序列预测

```python
# 股票价格预测
import numpy as np

# 准备序列数据
def create_sequences(data, seq_length=10):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# 训练
X_train, y_train = create_sequences(train_data, seq_length=10)
X_train = torch.FloatTensor(X_train).unsqueeze(-1)
y_train = torch.FloatTensor(y_train)

model = LSTMModel(input_size=1, hidden_size=64, num_layers=2, output_size=1)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    output = model(X_train)
    loss = criterion(output.squeeze(), y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

---

## 参考资源

- 《Deep Learning》- Goodfellow
- PyTorch RNN Tutorial

