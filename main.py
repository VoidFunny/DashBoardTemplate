from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import random
from datetime import datetime, timedelta

app = FastAPI()

# 配置静态文件和模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 生成模拟数据
def generate_mock_data():
    # 生成时间序列数据
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(7)]
    dates.reverse()
    
    # 生成折线图数据
    line_data1 = {
        'category1': [random.randint(100, 200) for _ in range(7)],
        'category2': [random.randint(150, 250) for _ in range(7)],
        'category3': [random.randint(80, 180) for _ in range(7)]
    }
    
    line_data2 = {
        'category1': [random.randint(300, 400) for _ in range(7)],
        'category2': [random.randint(250, 350) for _ in range(7)]
    }
    
    # 生成饼图数据
    pie_data = [
        {'name': '类别A', 'value': random.randint(200, 300)},
        {'name': '类别B', 'value': random.randint(150, 250)},
        {'name': '类别C', 'value': random.randint(100, 200)},
        {'name': '类别D', 'value': random.randint(50, 150)}
    ]
    
    # 生成排名数据
    ranking_data1 = [
        {'name': f'项目{i}', 'value': random.randint(1000, 5000)} 
        for i in range(1, 6)
    ]
    
    ranking_data2 = [
        {'name': f'产品{i}', 'value': random.randint(2000, 8000)} 
        for i in range(1, 6)
    ]
    
    # 生成顶部统计数据
    summary_data = {
        'total_users': random.randint(10000, 20000),
        'total_orders': random.randint(5000, 10000),
        'total_revenue': random.randint(100000, 200000)
    }
    
    return {
        'dates': dates,
        'line_data1': line_data1,
        'line_data2': line_data2,
        'pie_data': pie_data,
        'ranking_data1': ranking_data1,
        'ranking_data2': ranking_data2,
        'summary_data': summary_data
    }

def generate_detail_data():
    # 生成条形图数据
    bar_data1 = {
        'category1': random.randint(100, 200),
        'category2': random.randint(150, 250),
        'category3': random.randint(80, 180),
        'category4': random.randint(120, 220)
    }
    
    bar_data2 = {
        'product1': random.randint(300, 400),
        'product2': random.randint(250, 350),
        'product3': random.randint(200, 300),
        'product4': random.randint(150, 250)
    }
    
    # 生成排名数据
    ranking_data1 = [
        {'name': f'项目{i}', 'value': random.randint(1000, 5000)} 
        for i in range(1, 8)
    ]
    
    ranking_data2 = [
        {'name': f'产品{i}', 'value': random.randint(2000, 8000)} 
        for i in range(1, 8)
    ]
    
    return {
        'bar_data1': bar_data1,
        'bar_data2': bar_data2,
        'ranking_data1': ranking_data1,
        'ranking_data2': ranking_data2
    }

@app.get("/")
async def home(request: Request):
    data = generate_mock_data()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "data": data}
    )

@app.get("/detail")
async def detail(request: Request):
    data = generate_detail_data()
    return templates.TemplateResponse(
        "detail.html",
        {"request": request, "data": data}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 