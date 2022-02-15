# GPT系列演进

## 💡 核心结论

1. **GPT是生成式预训练模型，采用单向Transformer**
2. **GPT-2展示了大规模语言模型的zero-shot能力**
3. **GPT-3通过1750亿参数实现少样本学习**
4. **InstructGPT通过人类反馈强化学习对齐人类意图**
5. **ChatGPT通过对话优化，成为现象级应用**

---

## 1. GPT发展历程

### 1.1 时间线

```
2018.06  GPT-1     117M参数   预训练+微调
2019.02  GPT-2     1.5B参数   zero-shot
2020.05  GPT-3     175B参数   few-shot
2022.01  InstructGPT         RLHF对齐
2022.11  ChatGPT             对话优化
2023.03  GPT-4               多模态
```

### 1.2 架构演进

**GPT-1**：
```
12层Transformer Decoder
768维隐藏层
12个注意力头
117M参数
```

**GPT-3**：
```
96层Transformer Decoder
12288维隐藏层
96个注意力头
175B参数
```

---

## 2. GPT使用

### 2.1 OpenAI API

```python
import openai

openai.api_key = 'your-api-key'

# GPT-3.5 Turbo
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "什么是机器学习？"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)

# 流式输出
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "讲个笑话"}],
    stream=True
)

for chunk in response:
    if 'content' in chunk.choices[0].delta:
        print(chunk.choices[0].delta.content, end='')
```

### 2.2 Prompt Engineering

```python
# Few-shot提示
prompt = """
将以下评论分类为正面或负面：

评论：这个产品很好用
分类：正面

评论：质量太差了
分类：负面

评论：还不错，值得购买
分类：正面

评论：不推荐，浪费钱
分类：负面

评论：物超所值，非常满意
分类：
"""

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=10
)
```

---

## 3. GPT微调

```python
# 准备训练数据
training_data = [
    {"prompt": "将这句话翻译成英文：我爱学习", "completion": "I love learning"},
    {"prompt": "将这句话翻译成英文：今天天气很好", "completion": "The weather is nice today"},
    # ... 更多数据
]

# 微调（需要OpenAI API）
import openai

# 上传训练文件
with open('training_data.jsonl', 'w') as f:
    for item in training_data:
        f.write(json.dumps(item) + '\n')

# 创建微调任务
openai.File.create(file=open('training_data.jsonl'), purpose='fine-tune')
openai.FineTune.create(training_file='file-xxx', model='davinci')
```

---

## 参考资源

- OpenAI API文档
- GPT-3论文
- Prompt Engineering Guide

