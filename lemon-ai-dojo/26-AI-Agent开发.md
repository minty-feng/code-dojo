# AI Agent开发

## 💡 核心结论

1. **AI Agent是能够自主感知、决策、行动的智能体**
2. **ReAct框架结合推理和行动，提高Agent可靠性**
3. **工具调用让Agent可以访问外部API和数据库**
4. **记忆系统让Agent具有长期记忆能力**
5. **AutoGPT、BabyAGI展示了完全自主的Agent**

---

## 1. Agent架构

### 1.1 核心组件

```
感知（Perception）
  ↓
推理（Reasoning）
  ↓
规划（Planning）
  ↓
行动（Action）
  ↓
反思（Reflection）
```

### 1.2 ReAct模式

```
Thought: 思考下一步做什么
Action: 执行动作
Observation: 观察结果
... (重复直到完成任务)
```

---

## 2. 使用LangChain构建Agent

### 2.1 基础Agent

```python
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

# 定义工具
search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="搜索互联网信息，输入应该是搜索查询"
    ),
    Tool(
        name="Calculator",
        func=lambda x: str(eval(x)),
        description="执行数学计算，输入应该是数学表达式"
    )
]

# 创建Agent
llm = ChatOpenAI(temperature=0, model="gpt-4")
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5
)

# 运行
result = agent.run("2024年诺贝尔物理学奖得主是谁？他们的年龄总和是多少？")
print(result)
```

### 2.2 自定义工具

```python
from langchain.tools import BaseTool
from typing import Optional
import requests

class WeatherTool(BaseTool):
    name = "get_weather"
    description = "获取指定城市的实时天气信息"
    
    def _run(self, city: str) -> str:
        # 调用天气API
        api_key = "your-api-key"
        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url)
        data = response.json()
        
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text']
        
        return f"{city}当前天气：{condition}，温度{temp}°C"
    
    async def _arun(self, city: str) -> str:
        raise NotImplementedError("不支持异步")

class DatabaseTool(BaseTool):
    name = "query_database"
    description = "查询用户数据库，输入应该是SQL查询语句"
    
    def _run(self, query: str) -> str:
        import sqlite3
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return str(results)
    
    async def _arun(self, query: str) -> str:
        raise NotImplementedError()

# 使用自定义工具
tools = [WeatherTool(), DatabaseTool()]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

result = agent.run("北京今天天气怎么样？数据库中有多少个用户？")
```

---

## 3. Agent记忆系统

### 3.1 对话记忆

```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor

# 缓冲记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 多轮对话
agent.run("我叫张三")
agent.run("我的爱好是编程")
agent.run("我叫什么名字？我的爱好是什么？")  # Agent会记得
```

### 3.2 向量记忆

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# 向量存储记忆（长期记忆）
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts([], embeddings)

memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs=dict(k=5))
)

# 保存和检索记忆
memory.save_context(
    {"input": "我最喜欢的编程语言是Python"},
    {"output": "好的，我记住了"}
)

relevant_memories = memory.load_memory_variables(
    {"input": "我喜欢什么编程语言？"}
)
```

---

## 4. 实战案例

### 4.1 自动化研究Agent

```python
from langchain.agents import load_tools

# 加载预定义工具
tools = load_tools([
    "serpapi",          # Google搜索
    "llm-math",         # 数学计算
    "wikipedia",        # 维基百科
    "arxiv"             # 论文搜索
], llm=llm)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 复杂任务
task = """
研究"Attention is All You Need"这篇论文：
1. 找到论文的发表时间和作者
2. 总结论文的核心创新
3. 计算从发表到现在多少年了
4. 列出3篇引用这篇论文的重要后续工作
"""

result = agent.run(task)
```

---

## 参考资源

- Anthropic Claude文档
- Google Gemini文档  
- LangChain Agent指南

