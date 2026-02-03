from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import random
import io
import csv

app = FastAPI(title="Fund Valuation Service", description="API for fund valuation data")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Fund(BaseModel):
    code: str
    name: str
    nav: float  # Net Asset Value
    estimated_nav: float
    growth_rate: float
    last_update: str
    type: str

# Mock Data Generator
def generate_mock_data():
    types = ["股票型", "混合型", "债券型", "指数型"]
    names_prefix = ["华夏", "易方达", "汇添富", "广发", "南方", "嘉实", "富国", "博时"]
    names_suffix = ["成长", "价值", "创新", "医疗", "科技", "消费", "新能源", "军工", "蓝筹", "精选"]
    
    data = []
    for i in range(50):
        code = f"{random.randint(0, 999999):06d}"
        name = f"{random.choice(names_prefix)}{random.choice(names_suffix)}{random.choice(types)}"
        nav = round(random.uniform(0.5, 5.0), 4)
        growth = round(random.uniform(-5.0, 5.0), 2)
        est = round(nav * (1 + growth/100), 4)
        
        data.append(Fund(
            code=code,
            name=name,
            nav=nav,
            estimated_nav=est,
            growth_rate=growth,
            last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            type=random.choice(types)
        ))
    return data

FUNDS_DB = generate_mock_data()

@app.get("/")
async def root():
    return {"message": "Fund Valuation Service API"}

@app.get("/api/funds", response_model=List[Fund])
async def get_funds(search: Optional[str] = None, type: Optional[str] = None):
    """Search funds with optional filtering"""
    results = FUNDS_DB
    
    if search:
        search = search.lower()
        results = [f for f in results if search in f.code or search in f.name.lower()]
        
    if type:
        results = [f for f in results if f.type == type]
        
    return results

@app.get("/api/funds/download")
async def download_funds(type: Optional[str] = None):
    """Download fund data as CSV"""
    results = FUNDS_DB
    if type and type != "all":
        results = [f for f in results if f.type == type]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["基金代码", "基金名称", "单位净值", "估算净值", "估算涨跌幅", "更新时间", "类型"])
    
    for fund in results:
        writer.writerow([
            fund.code, 
            fund.name, 
            fund.nav, 
            fund.estimated_nav, 
            f"{fund.growth_rate}%", 
            fund.last_update, 
            fund.type
        ])
    
    output.seek(0)
    
    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=funds_valuation.csv"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
