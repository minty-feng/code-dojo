# ChatGPT原理解析

## 💡 核心结论

1. **ChatGPT = GPT-3.5 + RLHF（人类反馈强化学习）**
2. **RLHF包括：监督微调、奖励模型训练、PPO优化**
3. **ChatGPT通过对话数据训练，更适合交互场景**
4. **Temperature控制输出随机性，越高越有创造性**
5. **System Message定义AI角色，User/Assistant构建对话**

---

## 1. RLHF流程

### 1.1 三个阶段

```
阶段1：监督微调（SFT）
  人工标注对话数据
  微调GPT-3.5
  
阶段2：训练奖励模型（RM）
  人工对输出排序
  训练奖励模型预测人类偏好
  
阶段3：强化学习（PPO）
  用奖励模型指导
  优化策略模型
```

### 1.2 对话格式

```python
messages = [
    {
        "role": "system",
        "content": "你是一个专业的Python编程助手"
    },
    {
        "role": "user",
        "content": "如何读取CSV文件？"
    },
    {
        "role": "assistant",
        "content": "可以使用pandas库：import pandas as pd\ndf = pd.read_csv('file.csv')"
    },
    {
        "role": "user",
        "content": "如何筛选数据？"
    }
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)
```

---

## 2. 高级技巧

### 2.1 Temperature和Top_p

```python
# Temperature: 0-2
# 0: 确定性输出（贪婪）
# 1: 平衡
# 2: 更随机、更有创造性

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "写一首诗"}],
    temperature=1.5,    # 创造性
    top_p=0.9,          # 核采样
    max_tokens=200,
    n=3                 # 生成3个回复
)
```

### 2.2 函数调用（Function Calling）

```python
functions = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["city"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "北京天气怎么样？"}],
    functions=functions,
    function_call="auto"
)

if response.choices[0].finish_reason == "function_call":
    function_call = response.choices[0].message.function_call
    function_name = function_call.name
    arguments = json.loads(function_call.arguments)
    
    # 调用实际函数
    result = get_weather(arguments['city'])
    
    # 将结果返回给模型
    messages.append({
        "role": "function",
        "name": function_name,
        "content": json.dumps(result)
    })
    
    final_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
```

---

## 3. Prompt工程

### 3.1 提示词技巧

```python
# 1. 明确角色
system_message = "你是一个资深的机器学习工程师，擅长用简单的语言解释复杂概念"

# 2. 提供示例（Few-shot）
prompt = """
请将以下句子改写为更正式的表达：

非正式：这个东西挺好的
正式：该产品质量上乘

非正式：搞不懂这个问题
正式：该问题尚不明确

非正式：赶紧去做吧
正式：
"""

# 3. 指定输出格式
prompt = """
分析以下文本的情感，并以JSON格式输出：
{
  "sentiment": "正面/负面/中性",
  "confidence": 0.0-1.0,
  "keywords": ["关键词1", "关键词2"]
}

文本：这部电影非常精彩，演员演技很好
"""

# 4. 思维链（Chain of Thought）
prompt = """
问题：一个班级有30个学生，其中60%是女生，女生中有75%戴眼镜，请问有多少个女生戴眼镜？

让我们一步步思考：
1. 首先计算女生人数
2. 然后计算戴眼镜的女生人数
"""
```

---

## 4. 实战应用

### 4.1 智能客服

```python
class ChatBot:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.messages = [
            {"role": "system", "content": "你是一个专业的客服助手"}
        ]
    
    def chat(self, user_message):
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message

# 使用
bot = ChatBot('your-api-key')
print(bot.chat("我的订单什么时候发货？"))
print(bot.chat("订单号是123456"))
```

---

## 参考资源

- OpenAI官方文档
- ChatGPT Prompt Engineering

