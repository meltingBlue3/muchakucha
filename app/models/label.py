from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class Label(Base, TimestampMixin):
    """标签模型"""
    
    __tablename__ = "labels"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False, default="#3B82F6")
    
    def __repr__(self):
        return f"<Label(id={self.id}, name='{self.name}', group_id={self.group_id})>"


class EventLabel(Base):
    """事件-标签关联模型"""
    
    __tablename__ = "event_labels"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    label_id: Mapped[int] = mapped_column(Integer, ForeignKey("labels.id"), nullable=False, index=True)
    
    def __repr__(self):
        return f"<EventLabel(event_id={self.event_id}, label_id={self.label_id})>"


class TaskLabel(Base):
    """任务-标签关联模型"""
    
    __tablename__ = "task_labels"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=False, index=True)
    label_id: Mapped[int] = mapped_column(Integer, ForeignKey("labels.id"), nullable=False, index=True)
    
    def __repr__(self):
        return f"<TaskLabel(task_id={self.task_id}, label_id={self.label_id})>"

