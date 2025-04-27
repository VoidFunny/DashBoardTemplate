from pydantic import BaseModel
from typing import List, Dict, Optional

class SummaryBarVO(BaseModel):
    """汇总数据Bar的VO类"""
    name: str
    value: int
    unit: Optional[str] = None

class SeriesDataVO(BaseModel):
    """折线图系列数据VO类"""
    name: str
    data: List[int]

class LineChartVO(BaseModel):
    """折线图VO类"""
    legend: List[str]
    xAxis: List[str]
    series: List[SeriesDataVO]

class PieChartDataVO(BaseModel):
    """饼图数据项VO类"""
    name: str
    value: int

class RankItemVO(BaseModel):
    """排名项VO类"""
    name: str
    value: int
    rank: int

class DepartmentStatsVO(BaseModel):
    """部门统计数据VO类"""
    visits: int
    clicks: int
    users: int

class DashboardDataVO(BaseModel):
    """仪表盘完整数据VO类"""
    summary_bars: List[SummaryBarVO]
    line_charts: List[LineChartVO]
    pie_chart: List[PieChartDataVO]
    user_ranks: List[RankItemVO]
    dept_ranks: List[RankItemVO]
    dept_colors: Dict[str, str]

class ExcelUploadResponseVO(BaseModel):
    """Excel上传响应VO类"""
    success: bool
    message: str
    data: Optional[Dict[str, DepartmentStatsVO]] = None 