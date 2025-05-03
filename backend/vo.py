from typing import List
from pydantic import BaseModel

class SummaryVO(BaseModel):
    total_visits: int
    total_users: int
    total_code_lines: int

class DailyStatsVO(BaseModel):
    dates: List[str]
    daily_active_users: List[int]
    daily_visits: List[int]

class DepartmentPieVO(BaseModel):
    department_names: List[str]
    visit_counts: List[int]
    colors: List[str]

class TopUserVO(BaseModel):
    rank: int
    department: str
    user: str
    user_count: int

class TopVisitVO(BaseModel):
    rank: int
    department: str
    visit_count: int

class DepartmentDetailVO(BaseModel):
    daily_users: List[int]
    daily_visits: List[int]
    pie: DepartmentPieVO
    top_users: List[TopUserVO] 