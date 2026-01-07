from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    """事件基础模式"""
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    all_day: bool = False
    location: str | None = None


class EventCreate(EventBase):
    """事件创建模式"""
    label_ids: list[int] = []


class EventUpdate(BaseModel):
    """事件更新模式"""
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    all_day: bool | None = None
    location: str | None = None
    label_ids: list[int] | None = None


class EventInDB(EventBase):
    """数据库中的事件模式"""
    id: int
    group_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Event(EventInDB):
    """事件响应模式"""
    labels: list["LabelBasic"] = []


# 避免循环导入，定义简化的标签模式
class LabelBasic(BaseModel):
    """标签基础信息"""
    id: int
    name: str
    color: str
    
    model_config = ConfigDict(from_attributes=True)

