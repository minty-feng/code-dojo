# 国产大模型DeepSeek

## 💡 核心结论

1. **DeepSeek是国产开源大模型，性能媲美GPT-4**
2. **DeepSeek-Coder专注代码生成，超越Codex**
3. **DeepSeek-V2采用MoE架构，推理效率高**
4. **国产大模型包括通义千问、文心一言、智谱AI等**
5. **开源生态让中国AI快速发展**

---

## 1. DeepSeek系列

### 1.1 模型版本

```
2023.11  DeepSeek-LLM-7B/67B     通用对话
2024.01  DeepSeek-Coder-6.7B/33B 代码生成
2024.05  DeepSeek-V2              MoE架构
2024.12  DeepSeek-R1              推理增强
```

### 1.2 特点

- ✅ 完全开源
- ✅ 商用友好
- ✅ 中英双语
- ✅ 支持32K上下文
- ✅ API价格低

---

## 2. 使用DeepSeek

### 2.1 API调用

```python
import openai

# DeepSeek兼容OpenAI API
openai.api_base = "https://api.deepseek.com/v1"
openai.api_key = "your-deepseek-api-key"

response = openai.ChatCompletion.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个编程助手"},
        {"role": "user", "content": "用Python实现快速排序"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### 2.2 DeepSeek-Coder

```python
# 代码补全
prompt = """
def binary_search(arr, target):
    \"\"\"二分查找算法\"\"\"
    left, right = 0, len(arr) - 1
"""

response = openai.Completion.create(
    model="deepseek-coder",
    prompt=prompt,
    max_tokens=200,
    temperature=0.2  # 代码生成用低温度
)

code = response.choices[0].text
print(code)
```

---

## 3. 其他国产大模型

### 3.1 通义千问（Qwen）

```python
# 阿里云通义千问
from dashscope import Generation

response = Generation.call(
    model='qwen-turbo',
    messages=[
        {'role': 'user', 'content': '介绍一下机器学习'}
    ]
)

print(response.output.text)
```

### 3.2 智谱AI（ChatGLM）

```python
# 智谱AI
import zhipuai

zhipuai.api_key = "your-api-key"

response = zhipuai.model_api.invoke(
    model="chatglm_turbo",
    prompt=[{"role": "user", "content": "什么是Transformer？"}]
)

print(response['data']['choices'][0]['content'])
```

### 3.3 百度文心一言

```python
# 文心一言
import requests

url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"

payload = {
    "messages": [
        {"role": "user", "content": "介绍深度学习"}
    ]
}

response = requests.post(url, json=payload, headers={
    "Content-Type": "application/json"
})

print(response.json()['result'])
```

---

## 4. 模型对比

| 模型 | 公司 | 参数量 | 开源 | 特点 |
|------|------|--------|------|------|
| DeepSeek | DeepSeek | 7B-236B | ✅ | 代码能力强 |
| 通义千问 | 阿里 | 7B-72B | ✅ | 中文能力强 |
| ChatGLM | 智谱AI | 6B-130B | ✅ | 对话流畅 |
| 文心一言 | 百度 | 未公开 | ❌ | 搜索集成 |
| 讯飞星火 | 科大讯飞 | 未公开 | ❌ | 多模态 |

---

## 参考资源

- DeepSeek官网
- 通义千问文档
- ChatGLM GitHub

