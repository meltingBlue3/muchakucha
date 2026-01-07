from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.exceptions import NotFoundException
from app.models.label import Label, EventLabel, TaskLabel
from app.schemas.label import LabelCreate, LabelUpdate, LabelWithStats
from app.services.group import GroupService


class LabelService:
    """标签服务"""
    
    @staticmethod
    def create_label(db: Session, group_id: int, label_data: LabelCreate, creator_id: int) -> Label:
        """创建标签"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, creator_id)
        
        db_label = Label(
            group_id=group_id,
            name=label_data.name,
            color=label_data.color
        )
        db.add(db_label)
        db.commit()
        db.refresh(db_label)
        return db_label
    
    @staticmethod
    def get_label_by_id(db: Session, label_id: int, group_id: int, user_id: int) -> Label:
        """根据 ID 获取标签"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        label = db.query(Label).filter(Label.id == label_id, Label.group_id == group_id).first()
        if not label:
            raise NotFoundException(detail="Label not found")
        return label
    
    @staticmethod
    def get_group_labels(db: Session, group_id: int, user_id: int) -> list[Label]:
        """获取群组的所有标签"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        labels = db.query(Label).filter(Label.group_id == group_id).order_by(Label.name).all()
        return labels
    
    @staticmethod
    def update_label(db: Session, label_id: int, group_id: int, label_data: LabelUpdate, user_id: int) -> Label:
        """更新标签"""
        label = LabelService.get_label_by_id(db, label_id, group_id, user_id)
        
        if label_data.name is not None:
            label.name = label_data.name
        if label_data.color is not None:
            label.color = label_data.color
        
        db.commit()
        db.refresh(label)
        return label
    
    @staticmethod
    def delete_label(db: Session, label_id: int, group_id: int, user_id: int):
        """删除标签"""
        label = LabelService.get_label_by_id(db, label_id, group_id, user_id)
        
        # 删除关联关系
        db.query(EventLabel).filter(EventLabel.label_id == label_id).delete()
        db.query(TaskLabel).filter(TaskLabel.label_id == label_id).delete()
        
        # 删除标签
        db.delete(label)
        db.commit()
    
    @staticmethod
    def get_labels_with_stats(db: Session, group_id: int, user_id: int) -> list[LabelWithStats]:
        """获取带统计信息的标签列表"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        # 查询标签及其关联的事件和任务数量
        labels = db.query(Label).filter(Label.group_id == group_id).all()
        
        result = []
        for label in labels:
            event_count = db.query(func.count(EventLabel.id)).filter(EventLabel.label_id == label.id).scalar()
            task_count = db.query(func.count(TaskLabel.id)).filter(TaskLabel.label_id == label.id).scalar()
            
            label_with_stats = LabelWithStats(
                id=label.id,
                group_id=label.group_id,
                name=label.name,
                color=label.color,
                created_at=label.created_at,
                updated_at=label.updated_at,
                event_count=event_count or 0,
                task_count=task_count or 0
            )
            result.append(label_with_stats)
        
        return result
    
    @staticmethod
    def add_label_to_event(db: Session, event_id: int, label_id: int):
        """为事件添加标签"""
        # 检查是否已存在关联
        existing = db.query(EventLabel).filter(
            EventLabel.event_id == event_id,
            EventLabel.label_id == label_id
        ).first()
        
        if not existing:
            event_label = EventLabel(event_id=event_id, label_id=label_id)
            db.add(event_label)
    
    @staticmethod
    def add_label_to_task(db: Session, task_id: int, label_id: int):
        """为任务添加标签"""
        # 检查是否已存在关联
        existing = db.query(TaskLabel).filter(
            TaskLabel.task_id == task_id,
            TaskLabel.label_id == label_id
        ).first()
        
        if not existing:
            task_label = TaskLabel(task_id=task_id, label_id=label_id)
            db.add(task_label)
    
    @staticmethod
    def remove_label_from_event(db: Session, event_id: int, label_id: int):
        """从事件移除标签"""
        db.query(EventLabel).filter(
            EventLabel.event_id == event_id,
            EventLabel.label_id == label_id
        ).delete()
    
    @staticmethod
    def remove_label_from_task(db: Session, task_id: int, label_id: int):
        """从任务移除标签"""
        db.query(TaskLabel).filter(
            TaskLabel.task_id == task_id,
            TaskLabel.label_id == label_id
        ).delete()
    
    @staticmethod
    def get_event_labels(db: Session, event_id: int) -> list[Label]:
        """获取事件的所有标签"""
        labels = db.query(Label).join(EventLabel).filter(EventLabel.event_id == event_id).all()
        return labels
    
    @staticmethod
    def get_task_labels(db: Session, task_id: int) -> list[Label]:
        """获取任务的所有标签"""
        labels = db.query(Label).join(TaskLabel).filter(TaskLabel.task_id == task_id).all()
        return labels

