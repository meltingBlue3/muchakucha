from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    """任务基础模式"""
    title: str
    description: str | None = None
    due_date: date | None = None
    status: str = "pending"  # pending, in_progress, completed
    priority: str = "medium"  # low, medium, high
    assigned_to: int | None = None


class TaskCreate(TaskBase):
    """任务创建模式"""
    pass


class TaskUpdate(BaseModel):
    """任务更新模式"""
    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    status: str | None = None
    priority: str | None = None
    assigned_to: int | None = None


class TaskInDB(TaskBase):
    """数据库中的任务模式"""
    id: int
    group_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Task(TaskInDB):
    """任务响应模式"""
    pass

