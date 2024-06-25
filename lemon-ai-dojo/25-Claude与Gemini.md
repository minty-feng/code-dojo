# Claude与Gemini

## 💡 核心结论

1. **Claude以安全性和长上下文著称，支持200K tokens**
2. **Claude 3系列包括Haiku、Sonnet、Opus三个版本**
3. **Gemini是Google的多模态大模型**
4. **Gemini 1.5 Pro支持100万tokens超长上下文**
5. **Claude和Gemini在某些任务上超越GPT-4**

---

## 1. Claude系列

### 1.1 版本演进

```
2023.03  Claude 1        100K上下文
2023.07  Claude 2        100K上下文，更安全
2024.03  Claude 3        200K上下文
  - Haiku:  快速轻量
  - Sonnet: 平衡性能
  - Opus:   最强性能
2024.06  Claude 3.5 Sonnet  性能提升
```

### 1.2 使用Claude API

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# 基础对话
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "解释一下Transformer架构"}
    ]
)

print(message.content[0].text)

# 长文档分析
with open('long_document.txt', 'r') as f:
    document = f.read()

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=2000,
    messages=[
        {
            "role": "user",
            "content": f"请总结以下文档的关键要点：\n\n{document}"
        }
    ]
)

print(message.content[0].text)
```

### 1.3 Claude特色功能

```python
# 系统提示
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="你是一个Python编程专家，代码要简洁高效",
    messages=[
        {"role": "user", "content": "写一个快速排序"}
    ]
)

# 思维链
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=2000,
    messages=[
        {
            "role": "user",
            "content": "一个水池有两个水龙头，一个每小时注水10升，另一个每小时注水15升。同时有一个排水口每小时排水8升。现在水池是空的，问多久能装满50升水？请逐步思考。"
        }
    ]
)
```

---

## 2. Gemini系列

### 2.1 版本演进

```
2023.12  Gemini 1.0
  - Nano:  设备端
  - Pro:   平衡
  - Ultra: 旗舰
2024.02  Gemini 1.5 Pro    100万tokens上下文
2024.12  Gemini 2.0        多模态增强
```

### 2.2 使用Gemini API

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")

# 文本生成
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("解释量子计算")
print(response.text)

# 多轮对话
chat = model.start_chat(history=[])
response = chat.send_message("什么是深度学习？")
print(response.text)

response = chat.send_message("它和机器学习有什么区别？")
print(response.text)
```

### 2.3 多模态功能

```python
# Gemini Pro Vision
import PIL.Image

model = genai.GenerativeModel('gemini-pro-vision')

# 图像理解
img = PIL.Image.open('image.jpg')
response = model.generate_content([
    "这张图片里有什么？请详细描述",
    img
])
print(response.text)

# 视频分析（Gemini 1.5 Pro）
import google.generativeai as genai

video_file = genai.upload_file(path="video.mp4")

model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content([
    "总结这个视频的主要内容",
    video_file
])
print(response.text)
```

---

## 3. 超长上下文应用

### 3.1 长文档问答

```python
# Claude 200K上下文
with open('long_book.txt', 'r') as f:
    book_content = f.read()  # 可以是整本书！

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=2000,
    messages=[
        {
            "role": "user",
            "content": f"基于以下内容回答问题：\n\n{book_content}\n\n问题：主人公的性格特点是什么？"
        }
    ]
)
```

### 3.2 代码库分析

```python
# Gemini 1.5 Pro 100万tokens
import os

def read_codebase(directory):
    code = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file)) as f:
                    code += f"# {file}\n{f.read()}\n\n"
    return code

codebase = read_codebase('./my_project')  # 整个代码库！

model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content([
    f"分析这个代码库的架构和主要功能：\n\n{codebase}"
])
print(response.text)
```

---

## 4. 模型对比

| 特性 | GPT-4 | Claude 3 Opus | Gemini 1.5 Pro |
|------|-------|---------------|----------------|
| 上下文 | 128K | 200K | 1000K |
| 多模态 | ✅ | ✅ | ✅ |
| 代码能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 推理能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 价格 | 高 | 中 | 低 |

---

## 参考资源

- Anthropic Claude文档
- Google AI Studio
- Gemini API文档

