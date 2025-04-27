from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, List
import random
from datetime import datetime, timedelta
from ..schemas.dashboard import *
import pandas as pd
from io import BytesIO

router = APIRouter()

# 模拟部门数据
DEPARTMENTS = ["技术部", "市场部", "销售部", "人力资源部", "财务部"]
DEPT_COLORS = {
    "技术部": "#5470C6",
    "市场部": "#91CC75",
    "销售部": "#FAC858",
    "人力资源部": "#EE6666",
    "财务部": "#73C0DE"
}

def generate_mock_data() -> DashboardDataVO:
    """生成模拟数据"""
    # 生成汇总数据
    summary = [
        SummaryBarVO(name="总点击量", value=random.randint(10000, 50000), unit="次"),
        SummaryBarVO(name="总访问量", value=random.randint(5000, 20000), unit="次"),
        SummaryBarVO(name="总用户数", value=random.randint(1000, 5000), unit="人")
    ]

    # 生成时间轴数据
    now = datetime.now()
    dates = [(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    dates.reverse()

    # 生成折线图数据
    line_charts = [
        LineChartVO(
            legend=DEPARTMENTS,
            xAxis=dates,
            series=[
                SeriesDataVO(
                    name=dept,
                    data=[random.randint(100, 1000) for _ in range(7)]
                )
                for dept in DEPARTMENTS
            ]
        ),
        LineChartVO(
            legend=DEPARTMENTS,
            xAxis=dates,
            series=[
                SeriesDataVO(
                    name=dept,
                    data=[random.randint(50, 500) for _ in range(7)]
                )
                for dept in DEPARTMENTS
            ]
        )
    ]

    # 生成饼图数据
    pie_data = [
        PieChartDataVO(name=dept, value=random.randint(1000, 5000))
        for dept in DEPARTMENTS
    ]

    # 生成排名数据
    user_ranks = [
        RankItemVO(name=f"用户{i}", value=random.randint(100, 1000), rank=i)
        for i in range(1, 11)
    ]
    dept_ranks = [
        RankItemVO(name=dept, value=random.randint(1000, 5000), rank=i+1)
        for i, dept in enumerate(DEPARTMENTS)
    ]

    return DashboardDataVO(
        summary_bars=summary,
        line_charts=line_charts,
        pie_chart=pie_data,
        user_ranks=sorted(user_ranks, key=lambda x: x.value, reverse=True),
        dept_ranks=sorted(dept_ranks, key=lambda x: x.value, reverse=True),
        dept_colors=DEPT_COLORS
    )

@router.get("/dashboard", response_model=DashboardDataVO)
async def get_dashboard_data():
    """获取仪表盘数据"""
    return generate_mock_data()

@router.post("/upload-excel", response_model=ExcelUploadResponseVO)
async def upload_excel(file: UploadFile = File(...)):
    """处理Excel上传"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="只支持Excel格式的文件(.xlsx或.xls)")
    
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))
        
        # 验证必要的列是否存在
        required_columns = ['部门', '访问量', '点击量', '用户数']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"Excel文件必须包含以下列：{', '.join(required_columns)}")
        
        # 处理Excel数据
        dept_stats: Dict[str, DepartmentStatsVO] = {}
        
        for _, row in df.iterrows():
            dept = row['部门']
            if pd.notna(dept):
                dept_stats[dept] = DepartmentStatsVO(
                    visits=int(row['访问量'] if pd.notna(row['访问量']) else 0),
                    clicks=int(row['点击量'] if pd.notna(row['点击量']) else 0),
                    users=int(row['用户数'] if pd.notna(row['用户数']) else 0)
                )
        
        return ExcelUploadResponseVO(
            success=True,
            message=f"成功处理{len(dept_stats)}个部门的数据",
            data=dept_stats
        )
        
    except Exception as e:
        return ExcelUploadResponseVO(
            success=False,
            message=f"处理Excel文件时出错: {str(e)}",
            data=None
        ) 