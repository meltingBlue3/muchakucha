from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    """笔记基础模式"""
    title: str
    content: str | None = None


class NoteCreate(NoteBase):
    """笔记创建模式"""
    pass


class NoteUpdate(BaseModel):
    """笔记更新模式"""
    title: str | None = None
    content: str | None = None


class NoteInDB(NoteBase):
    """数据库中的笔记模式"""
    id: int
    group_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Note(NoteInDB):
    """笔记响应模式"""
    pass

