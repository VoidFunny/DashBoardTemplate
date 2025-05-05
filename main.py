from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import random

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/line_data")
def get_line_data(chart_id: int = Query(...), data_type: str = Query(...)):
    # 模拟不同类型的数据
    x = [f"第{i}天" for i in range(1, 8)]
    if data_type == "A":
        y = [random.randint(10, 30) for _ in range(7)]
    elif data_type == "B":
        y = [random.randint(20, 50) for _ in range(7)]
    else:
        y = [random.randint(5, 15) for _ in range(7)]
    return JSONResponse(content={"x": x, "y": y, "data_type": data_type, "chart_id": chart_id}) 