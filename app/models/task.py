from datetime import date
from sqlalchemy import String, Text, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class Task(Base, TimestampMixin):
    """任务模型"""
    
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)  # pending, in_progress, completed
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")  # low, medium, high
    assigned_to: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    created_by: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"

