# 向量数据库与RAG

## 💡 核心结论

1. **向量数据库存储高维向量，支持高效相似度搜索**
2. **RAG通过检索外部知识增强LLM生成能力**
3. **Embedding模型将文本转换为向量表示**
4. **分块策略影响检索质量，需要平衡粒度和语义**
5. **混合检索结合关键词和语义搜索，效果更好**

---

## 1. 向量数据库

### 1.1 主流向量数据库

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| Chroma | 轻量、易用 | 原型开发 |
| Pinecone | 云服务、高性能 | 生产环境 |
| Milvus | 开源、分布式 | 大规模应用 |
| Weaviate | 混合搜索 | 企业应用 |
| Qdrant | 高性能、Rust | 实时搜索 |

### 1.2 使用Chroma

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# 文档
documents = [
    "机器学习是人工智能的一个分支",
    "深度学习使用多层神经网络",
    "Transformer是NLP的突破性架构"
]

# 分割文本
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
docs = text_splitter.create_documents(documents)

# 创建向量数据库
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 相似度搜索
query = "什么是神经网络？"
results = vectorstore.similarity_search(query, k=2)

for doc in results:
    print(doc.page_content)
    print('---')

# 带分数的搜索
results_with_scores = vectorstore.similarity_search_with_score(query, k=2)

for doc, score in results_with_scores:
    print(f"分数: {score}")
    print(doc.page_content)
    print('---')
```

---

## 2. RAG实现

### 2.1 基础RAG

```python
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# 创建问答链
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# 提问
query = "Transformer的核心创新是什么？"
result = qa_chain({"query": query})

print("回答:", result['result'])
print("\n来源文档:")
for doc in result['source_documents']:
    print(doc.page_content)
```

### 2.2 高级RAG

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# 压缩检索器（过滤无关内容）
llm = ChatOpenAI(temperature=0)
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)

# 混合检索（关键词 + 语义）
from langchain.retrievers import BM25Retriever, EnsembleRetriever

bm25_retriever = BM25Retriever.from_documents(docs)
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vectorstore.as_retriever()],
    weights=[0.5, 0.5]
)

# 使用
results = ensemble_retriever.get_relevant_documents("Transformer")
```

---

## 3. 文档处理

### 3.1 文档加载

```python
from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    TextLoader,
    WebBaseLoader
)

# PDF
loader = PyPDFLoader("document.pdf")
pages = loader.load_and_split()

# Markdown
loader = UnstructuredMarkdownLoader("README.md")
docs = loader.load()

# 网页
loader = WebBaseLoader("https://example.com/article")
docs = loader.load()
```

### 3.2 文本分块策略

```python
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter
)

# 按字符分割
splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separator="\n\n"
)

# 递归分割（推荐）
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

# 按token分割
splitter = TokenTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)
```

---

## 4. 生产级RAG

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# 记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key='answer'
)

# 问答链
qa = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(temperature=0.7),
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    memory=memory,
    return_source_documents=True
)

# 多轮对话
response1 = qa({"question": "文档主要讲什么？"})
print(response1['answer'])

response2 = qa({"question": "能详细解释一下第一部分吗？"})
print(response2['answer'])
```

---

## 参考资源

- LangChain文档
- Chroma文档
- RAG Survey论文

