# Transformer架构

## 💡 核心结论

1. **Transformer完全基于注意力机制，抛弃了RNN**
2. **自注意力机制可以并行处理序列，训练速度快**
3. **多头注意力从多个子空间学习表示**
4. **位置编码让模型感知序列顺序**
5. **Transformer是GPT、BERT等模型的基础**

---

## 1. 自注意力机制

### 1.1 原理

```
Query, Key, Value矩阵

Attention(Q, K, V) = softmax(QKᵀ / √d_k) * V

步骤：
1. 计算相似度：QKᵀ
2. 缩放：除以√d_k（防止梯度消失）
3. softmax：得到注意力权重
4. 加权求和：乘以V
```

### 1.2 实现

```python
import torch
import torch.nn as nn
import math

class SelfAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(SelfAttention, self).__init__()
        self.embed_size = embed_size
        self.heads = heads
        self.head_dim = embed_size // heads
        
        assert self.head_dim * heads == embed_size
        
        self.values = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.keys = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.queries = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.fc_out = nn.Linear(heads * self.head_dim, embed_size)
    
    def forward(self, values, keys, query, mask=None):
        N = query.shape[0]
        value_len, key_len, query_len = values.shape[1], keys.shape[1], query.shape[1]
        
        # 分成多个头
        values = values.reshape(N, value_len, self.heads, self.head_dim)
        keys = keys.reshape(N, key_len, self.heads, self.head_dim)
        queries = query.reshape(N, query_len, self.heads, self.head_dim)
        
        # Q, K, V变换
        values = self.values(values)
        keys = self.keys(keys)
        queries = self.queries(queries)
        
        # 计算注意力分数
        energy = torch.einsum("nqhd,nkhd->nhqk", [queries, keys])
        # energy shape: (N, heads, query_len, key_len)
        
        if mask is not None:
            energy = energy.masked_fill(mask == 0, float("-1e20"))
        
        attention = torch.softmax(energy / (self.embed_size ** (1/2)), dim=3)
        
        out = torch.einsum("nhql,nlhd->nqhd", [attention, values])
        out = out.reshape(N, query_len, self.heads * self.head_dim)
        out = self.fc_out(out)
        return out
```

---

## 2. Transformer架构

### 2.1 编码器

```python
class TransformerBlock(nn.Module):
    def __init__(self, embed_size, heads, dropout, forward_expansion):
        super(TransformerBlock, self).__init__()
        self.attention = SelfAttention(embed_size, heads)
        self.norm1 = nn.LayerNorm(embed_size)
        self.norm2 = nn.LayerNorm(embed_size)
        
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_size, forward_expansion * embed_size),
            nn.ReLU(),
            nn.Linear(forward_expansion * embed_size, embed_size)
        )
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, value, key, query, mask):
        attention = self.attention(value, key, query, mask)
        x = self.dropout(self.norm1(attention + query))
        forward = self.feed_forward(x)
        out = self.dropout(self.norm2(forward + x))
        return out
```

### 2.2 位置编码

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           -(math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return x
```

---

## 3. 使用Hugging Face

```python
from transformers import BertTokenizer, BertModel

# 加载预训练模型
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# 编码文本
text = "Hello, how are you?"
encoded = tokenizer(text, return_tensors='pt')

# 前向传播
with torch.no_grad():
    output = model(**encoded)
    last_hidden_states = output.last_hidden_state
```

---

## 参考资源

- 《Attention is All You Need》论文
- The Illustrated Transformer
- Hugging Face Transformers

