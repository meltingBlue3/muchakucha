from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class LabelBase(BaseModel):
    """标签基础模式"""
    name: str = Field(..., min_length=1, max_length=50, description="标签名称")
    color: str = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$", description="标签颜色（十六进制）")


class LabelCreate(LabelBase):
    """标签创建模式"""
    pass


class LabelUpdate(BaseModel):
    """标签更新模式"""
    name: str | None = Field(None, min_length=1, max_length=50, description="标签名称")
    color: str | None = Field(None, pattern="^#[0-9A-Fa-f]{6}$", description="标签颜色（十六进制）")


class LabelInDB(LabelBase):
    """数据库中的标签模式"""
    id: int
    group_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Label(LabelInDB):
    """标签响应模式"""
    pass


class LabelWithStats(Label):
    """带统计信息的标签响应模式"""
    event_count: int = Field(default=0, description="关联的事件数量")
    task_count: int = Field(default=0, description="关联的任务数量")

