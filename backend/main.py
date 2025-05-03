from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from vo import *
import pandas as pd
import random
import threading
import http.server
import socketserver
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟部门颜色
DEPT_COLORS = {
    "研发部": "#5470C6",
    "市场部": "#91CC75",
    "销售部": "#FAC858",
    "人事部": "#EE6666",
    "财务部": "#73C0DE",
    "运维部": "#3BA272",
    "产品部": "#FC8452",
    "设计部": "#9A60B4",
    "测试部": "#EA7CCC",
    "客服部": "#FFC300"
}

# 模拟数据接口
@app.get("/api/summary", response_model=SummaryVO)
def get_summary():
    return SummaryVO(
        total_visits=12345,
        total_users=234,
        total_code_lines=567890
    )

@app.get("/api/daily_stats", response_model=DailyStatsVO)
def get_daily_stats():
    dates = [f"2024-06-{i:02d}" for i in range(1, 11)]
    return DailyStatsVO(
        dates=dates,
        daily_active_users=[random.randint(20, 50) for _ in dates],
        daily_visits=[random.randint(100, 300) for _ in dates]
    )

@app.get("/api/department_pie", response_model=DepartmentPieVO)
def get_department_pie():
    depts = list(DEPT_COLORS.keys())
    visits = [random.randint(100, 1000) for _ in depts]
    colors = [DEPT_COLORS[d] for d in depts]
    return DepartmentPieVO(
        department_names=depts,
        visit_counts=visits,
        colors=colors
    )

@app.get("/api/top_users", response_model=List[TopUserVO])
def get_top_users():
    return [
        TopUserVO(rank=i+1, department="研发部", user=f"用户{i+1}", user_count=random.randint(1, 10))
        for i in range(10)
    ]

@app.get("/api/top_visits", response_model=List[TopVisitVO])
def get_top_visits():
    depts = list(DEPT_COLORS.keys())
    return [
        TopVisitVO(rank=i+1, department=depts[i], visit_count=random.randint(100, 1000))
        for i in range(10)
    ]

# Excel上传与解析API
@app.post("/api/upload_excel")
async def upload_excel(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)
    # 假设Excel有：部门名称，用户名，工具名称，代码生成量
    dept_group = df.groupby('部门名称')
    visits = dept_group.size().to_dict()
    users = dept_group['用户名'].nunique().to_dict()
    code_lines = dept_group['代码生成量'].sum().to_dict()
    return {
        "visits": visits,
        "users": users,
        "code_lines": code_lines
    }

def start_frontend_server():
    # 切换到前端目录
    os.chdir(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    
    # 设置服务器端口
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"前端服务运行在: http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    import uvicorn
    
    # 启动前端服务（在新线程中）
    frontend_thread = threading.Thread(target=start_frontend_server)
    frontend_thread.daemon = True  # 设置为守护线程，这样主线程退出时会自动结束
    frontend_thread.start()
    
    # 启动后端服务
    print("后端服务运行在: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

