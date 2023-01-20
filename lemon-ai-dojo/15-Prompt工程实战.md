# Prompt工程实战

## 💡 核心结论

1. **好的Prompt需要清晰的指令、相关的上下文、明确的输出格式**
2. **Few-shot示例可以大幅提升输出质量**
3. **思维链提示让模型逐步推理，提高准确性**
4. **角色扮演让模型更好地理解任务**
5. **迭代优化Prompt是关键技能**

---

## 1. Prompt基本原则

### 1.1 清晰具体

```
❌ 差：告诉我关于Python的事
✅ 好：列出Python中5种常用的数据结构，并解释它们的特点和使用场景
```

### 1.2 提供上下文

```
❌ 差：解释这个错误
✅ 好：我在运行Python代码时遇到了"IndexError: list index out of range"错误。
代码是：
```python
lst = [1, 2, 3]
print(lst[5])
```
请解释错误原因并提供解决方案。
```

### 1.3 指定格式

```python
prompt = """
分析以下产品评论，以JSON格式输出：
{
  "sentiment": "正面/负面/中性",
  "score": 1-5,
  "aspects": {
    "质量": "评价",
    "价格": "评价",
    "服务": "评价"
  }
}

评论：产品质量很好，价格有点贵，客服态度不错
"""
```

---

## 2. 高级技巧

### 2.1 思维链（Chain of Thought）

```python
# 复杂推理问题
prompt = """
问题：一辆汽车以60公里/小时的速度行驶了2小时，然后以80公里/小时的速度又行驶了1.5小时，总共行驶了多少公里？

让我们一步步思考：
第一步：计算第一段距离
第二步：计算第二段距离
第三步：计算总距离

请按照这个思路解答。
"""
```

### 2.2 角色扮演

```python
system_prompts = {
    "编程助手": "你是一个经验丰富的Python开发工程师，擅长代码优化和调试",
    "老师": "你是一个有10年教学经验的数学老师，擅长用简单的例子解释复杂概念",
    "翻译": "你是一个专业的英中翻译，追求准确性和流畅性",
    "文案": "你是一个创意文案策划，擅长撰写吸引人的广告文案"
}
```

### 2.3 Few-shot示例

```python
prompt = """
将产品描述改写为营销文案：

产品：保温杯
描述：这是一个保温杯，能保温12小时
文案：告别冷水！这款革命性保温杯让您随时随地享受热饮，12小时持久保温，温暖相伴每一刻！

产品：耳机
描述：无线蓝牙耳机，降噪功能
文案：沉浸音乐世界！主动降噪技术隔绝喧嚣，无线自由畅听，让每个音符直达心灵！

产品：背包
描述：防水背包，容量大
文案：
"""
```

---

## 3. 实战场景

### 3.1 代码生成

```python
prompt = """
用Python实现一个函数，功能如下：
- 函数名：find_duplicates
- 输入：一个整数列表
- 输出：列表中所有重复的元素
- 要求：使用字典统计，时间复杂度O(n)
- 包含docstring和类型注解
- 包含测试用例
"""
```

### 3.2 文本摘要

```python
prompt = """
将以下文章总结为3个要点：

[长文本内容...]

要求：
1. 每个要点不超过30字
2. 按重要性排序
3. 使用项目符号
"""
```

### 3.3 数据提取

```python
prompt = """
从以下文本中提取关键信息，以JSON格式输出：

文本：张三于2023年10月15日在北京购买了一台iPhone 15 Pro，价格为8999元。

输出格式：
{
  "姓名": "",
  "日期": "",
  "地点": "",
  "商品": "",
  "价格": 0
}
"""
```

---

## 4. LangChain框架

### 4.1 基础使用

```python
from langchain import OpenAI, PromptTemplate, LLMChain

# 创建提示模板
template = """
你是一个{role}。

任务：{task}

输出格式：{format}
"""

prompt = PromptTemplate(
    input_variables=["role", "task", "format"],
    template=template
)

# 创建链
llm = OpenAI(temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# 运行
result = chain.run(
    role="专业的文案策划",
    task="为一款新手机写广告语",
    format="3条简短有力的广告语"
)
```

### 4.2 记忆功能

```python
from langchain.memory import ConversationBufferMemory
from langchain import ConversationChain

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=OpenAI(),
    memory=memory,
    verbose=True
)

# 多轮对话
conversation.predict(input="我叫张三")
conversation.predict(input="我喜欢Python编程")
conversation.predict(input="我叫什么名字？")  # 模型会记得
```

---

## 参考资源

- OpenAI Prompt Engineering Guide
- LangChain文档
- Awesome ChatGPT Prompts

