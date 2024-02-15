# 开源大模型Llama

## 💡 核心结论

1. **Llama是Meta开源的大语言模型，推动了开源AI发展**
2. **Llama 2支持商用，有7B、13B、70B不同规模**
3. **本地部署Llama可以保护数据隐私**
4. **量化技术（GPTQ、GGML）让普通电脑也能运行大模型**
5. **Alpaca、Vicuna等是基于Llama的微调模型**

---

## 1. Llama系列

### 1.1 发展历程

```
2023.02  Llama 1    7B-65B    研究用途
2023.07  Llama 2    7B-70B    商用许可
2024.04  Llama 3    8B-70B    性能大幅提升
```

### 1.2 模型规模

| 模型 | 参数量 | 内存需求 | 适用场景 |
|------|--------|----------|----------|
| Llama-7B | 7B | 14GB | 个人电脑 |
| Llama-13B | 13B | 26GB | 工作站 |
| Llama-70B | 70B | 140GB | 服务器 |

---

## 2. 本地部署

### 2.1 使用llama.cpp

```bash
# 安装llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# 下载模型（量化版本）
wget https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf

# 运行
./main -m llama-2-7b.Q4_K_M.gguf -p "What is machine learning?" -n 128
```

### 2.2 使用Ollama

```bash
# 安装Ollama
curl https://ollama.ai/install.sh | sh

# 下载并运行Llama 2
ollama run llama2

# Python调用
pip install ollama

import ollama

response = ollama.chat(model='llama2', messages=[
  {
    'role': 'user',
    'content': '什么是机器学习？',
  },
])
print(response['message']['content'])
```

---

## 3. 微调Llama

### 3.1 使用LoRA

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 加载模型
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    load_in_8bit=True,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# LoRA配置
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 准备模型
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

# 训练
# ...
```

---

## 4. 应用案例

### 4.1 本地聊天机器人

```python
from transformers import pipeline

# 加载本地模型
chatbot = pipeline(
    "text-generation",
    model="meta-llama/Llama-2-7b-chat-hf",
    device_map="auto"
)

# 对话
prompt = """[INST] <<SYS>>
你是一个有帮助的助手
<</SYS>>

什么是深度学习？[/INST]"""

response = chatbot(prompt, max_new_tokens=200)
print(response[0]['generated_text'])
```

---

## 参考资源

- Llama官方仓库
- llama.cpp项目
- Ollama文档

