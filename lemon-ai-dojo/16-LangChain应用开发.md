# LangChain应用开发

## 💡 核心结论

1. **LangChain是构建LLM应用的框架**
2. **Chain组合多个组件实现复杂工作流**
3. **Agent可以使用工具，自主决策行动**
4. **向量数据库存储文本嵌入，实现语义搜索**
5. **RAG（检索增强生成）让LLM访问外部知识**

---

## 1. LangChain核心概念

### 1.1 Models

```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# LLM
llm = OpenAI(temperature=0.7, model_name="text-davinci-003")
response = llm("什么是机器学习？")

# Chat Model
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo")
from langchain.schema import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="你是一个Python专家"),
    HumanMessage(content="如何读取JSON文件？")
]
response = chat_model(messages)
```

### 1.2 Prompts

```python
from langchain import PromptTemplate

# 单变量模板
template = "请用{language}写一个{task}的示例代码"
prompt = PromptTemplate(
    input_variables=["language", "task"],
    template=template
)

formatted_prompt = prompt.format(language="Python", task="快速排序")

# 聊天提示模板
from langchain.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}"),
    ("human", "{input}")
])

messages = chat_template.format_messages(
    role="专业的翻译",
    input="将'Hello'翻译成中文"
)
```

---

## 2. Chains

### 2.1 Simple Chain

```python
from langchain import LLMChain

llm = OpenAI(temperature=0.7)
template = "请为{product}写一句广告语"
prompt = PromptTemplate(template=template, input_variables=["product"])

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("智能手表")
print(result)
```

### 2.2 Sequential Chain

```python
from langchain.chains import SimpleSequentialChain

# Chain 1: 生成故事
chain1 = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        template="为{topic}写一个简短的故事",
        input_variables=["topic"]
    )
)

# Chain 2: 总结故事
chain2 = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        template="用一句话总结以下故事：\n{story}",
        input_variables=["story"]
    )
)

# 组合
overall_chain = SimpleSequentialChain(chains=[chain1, chain2])
result = overall_chain.run("人工智能")
```

---

## 3. RAG（检索增强生成）

### 3.1 向量数据库

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# 加载文档
loader = TextLoader('document.txt')
documents = loader.load()

# 分割文档
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# 创建向量数据库
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)

# 相似度搜索
query = "什么是机器学习？"
similar_docs = vectorstore.similarity_search(query, k=3)

for doc in similar_docs:
    print(doc.page_content)
    print('---')
```

### 3.2 问答系统

```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

question = "文档中提到了哪些机器学习算法？"
answer = qa_chain.run(question)
print(answer)
```

---

## 4. Agents

### 4.1 工具

```python
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import DuckDuckGoSearchRun

# 定义工具
search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="搜索互联网信息"
    ),
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="计算数学表达式"
    )
]

# 创建Agent
agent = initialize_agent(
    tools,
    ChatOpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 运行
result = agent.run("2023年诺贝尔物理学奖获得者是谁？他们的主要贡献是什么？")
```

### 4.2 自定义工具

```python
from langchain.tools import BaseTool

class WeatherTool(BaseTool):
    name = "Weather"
    description = "获取指定城市的天气信息"
    
    def _run(self, city: str) -> str:
        # 实际调用天气API
        return f"{city}的天气：晴天，25°C"
    
    async def _arun(self, city: str) -> str:
        raise NotImplementedError()

tools = [WeatherTool()]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

result = agent.run("北京今天天气怎么样？")
```

---

## 5. 实战项目

### 5.1 文档问答系统

```python
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# 加载PDF
loader = PyPDFLoader("document.pdf")
pages = loader.load_and_split()

# 创建向量数据库
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(pages, embeddings)

# 创建问答链（带记忆）
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

qa_chain = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(temperature=0),
    vectorstore.as_retriever(),
    memory=memory
)

# 多轮对话
print(qa_chain({"question": "文档主要讲什么？"}))
print(qa_chain({"question": "能详细解释第一部分吗？"}))
```

---

## 参考资源

- LangChain官方文档
- LangChain Cookbook

