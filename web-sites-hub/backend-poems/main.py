from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI(title="Poem Service", description="API for fetching classic Chinese poems")

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_methods=["*"],
    allow_headers=["*"],
)

class Poem(BaseModel):
    id: int
    title: str
    author: str
    dynesty: str
    content: str
    tags: Optional[List[str]] = []

# Mock Database
# In a real app, this would be SQLite or PostgreSQL
poems_db = [
    Poem(id=1, title="定风波", author="苏轼", dynesty="宋", 
         content="莫听穿林打叶声，何妨吟啸且徐行。\n竹杖芒鞋轻胜马，谁怕？\n一蓑烟雨任平生。\n\n料峭春风吹酒醒，微冷，山头斜照却相迎。\n回首向来萧瑟处，归去，\n也无风雨也无晴。",
         tags=["豁达", "人生"]),
    Poem(id=2, title="将进酒", author="李白", dynesty="唐", 
         content="君不见，黄河之水天上来，奔流到海不复回。\n君不见，高堂明镜悲白发，朝如青丝暮成雪。\n人生得意须尽欢，莫使金樽空对月。\n天生我材必有用，千金散尽还复来。",
         tags=["豪迈", "饮酒"]),
    Poem(id=3, title="春江花月夜", author="张若虚", dynesty="唐", 
         content="春江潮水连海平，海上明月共潮生。\n滟滟随波千万里，何处春江无月明！\n江流宛转绕芳甸，月照花林皆似霰。\n空里流霜不觉飞，汀上白沙看不见。",
         tags=["唯美", "月夜"]),
    Poem(id=4, title="临江仙", author="杨慎", dynesty="明",
         content="滚滚长江东逝水，浪花淘尽英雄。\n是非成败转头空。\n青山依旧在，几度夕阳红。",
         tags=["历史", "感慨"]),
     Poem(id=5, title="望岳", author="杜甫", dynesty="唐",
         content="岱宗夫如何？齐鲁青未了。\n造化钟神秀，阴阳割昏晓。\n荡胸生曾云，决眦入归鸟。\n会当凌绝顶，一览众山小。",
         tags=["壮志", "登山"])
]

@app.get("/")
async def root():
    return {"message": "Welcome to Poem Service. Visit /docs for API documentation."}

@app.get("/api/poems", response_model=List[Poem])
async def get_poems():
    """Get all poems"""
    return poems_db

@app.get("/api/poems/random", response_model=Poem)
async def get_random_poem():
    """Get a single random poem"""
    return random.choice(poems_db)

@app.get("/api/poems/{poem_id}", response_model=Poem)
async def get_poem(poem_id: int):
    """Get a specific poem by ID"""
    for poem in poems_db:
        if poem.id == poem_id:
            return poem
    raise HTTPException(status_code=404, detail="Poem not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
