# BERT与预训练模型

## 💡 核心结论

1. **BERT通过双向Transformer学习上下文表示**
2. **预训练+微调是NLP的新范式**
3. **Masked Language Model和Next Sentence Prediction是BERT的预训练任务**
4. **BERT可以用于分类、NER、问答等多种任务**
5. **RoBERTa、ALBERT、ELECTRA是BERT的改进版本**

---

## 1. BERT架构

### 1.1 原理

```
预训练任务：
1. Masked Language Model (MLM)
   随机遮盖15%的词，预测被遮盖的词
   
2. Next Sentence Prediction (NSP)
   预测两个句子是否连续

输入：[CLS] Sentence A [SEP] Sentence B [SEP]
```

### 1.2 使用Hugging Face

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 加载预训练模型
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(
    model_name, 
    num_labels=2
)

# 文本分类
text = "这部电影很精彩"
inputs = tokenizer(
    text, 
    return_tensors='pt',
    padding=True,
    truncation=True,
    max_length=128
)

# 预测
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)
    pred = torch.argmax(probs, dim=1)
    
print(f"预测: {pred.item()}")
print(f"概率: {probs}")
```

---

## 2. 微调BERT

```python
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# 加载数据集
dataset = load_dataset('imdb')

# 分词
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=512
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 加载模型
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2
)

# 训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=100,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True
)

# 训练
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test']
)

trainer.train()
```

---

## 3. 命名实体识别（NER）

```python
from transformers import BertForTokenClassification, BertTokenizerFast

# 加载模型
model = BertForTokenClassification.from_pretrained(
    'bert-base-chinese',
    num_labels=7  # O, B-PER, I-PER, B-LOC, I-LOC, B-ORG, I-ORG
)
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')

# 预测
text = "苹果公司的CEO是蒂姆·库克"
inputs = tokenizer(text, return_tensors='pt')

with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)

# 解码
label_map = {0: 'O', 1: 'B-PER', 2: 'I-PER', 3: 'B-LOC', 4: 'I-LOC', 5: 'B-ORG', 6: 'I-ORG'}
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
labels = [label_map[p.item()] for p in predictions[0]]

for token, label in zip(tokens, labels):
    print(f"{token}\t{label}")
```

---

## 参考资源

- Hugging Face Transformers文档
- BERT论文

