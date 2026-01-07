from datetime import datetime
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.event import Event
from app.models.label import EventLabel
from app.schemas.event import EventCreate, EventUpdate
from app.services.group import GroupService
from app.services.label import LabelService


class EventService:
    """事件服务"""
    
    @staticmethod
    def create_event(db: Session, group_id: int, event_data: EventCreate, creator_id: int) -> Event:
        """创建事件"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, creator_id)
        
        db_event = Event(
            group_id=group_id,
            title=event_data.title,
            description=event_data.description,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            all_day=event_data.all_day,
            location=event_data.location,
            created_by=creator_id
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        
        # 添加标签关联
        if event_data.label_ids:
            for label_id in event_data.label_ids:
                LabelService.add_label_to_event(db, db_event.id, label_id)
            db.commit()
        
        # 加载标签
        db_event.labels = LabelService.get_event_labels(db, db_event.id)
        return db_event
    
    @staticmethod
    def get_event_by_id(db: Session, event_id: int, group_id: int, user_id: int) -> Event:
        """根据 ID 获取事件"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        event = db.query(Event).filter(Event.id == event_id, Event.group_id == group_id).first()
        if not event:
            raise NotFoundException(detail="Event not found")
        
        # 加载标签
        event.labels = LabelService.get_event_labels(db, event.id)
        return event
    
    @staticmethod
    def get_group_events(
        db: Session, 
        group_id: int, 
        user_id: int,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        label_ids: list[int] | None = None
    ) -> list[Event]:
        """获取群组的事件列表"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        query = db.query(Event).filter(Event.group_id == group_id)
        
        # 日期范围过滤
        if start_date:
            query = query.filter(Event.start_time >= start_date)
        if end_date:
            query = query.filter(Event.start_time <= end_date)
        
        # 标签过滤
        if label_ids:
            query = query.join(EventLabel).filter(EventLabel.label_id.in_(label_ids)).distinct()
        
        events = query.order_by(Event.start_time).all()
        
        # 为每个事件加载标签
        for event in events:
            event.labels = LabelService.get_event_labels(db, event.id)
        
        return events
    
    @staticmethod
    def update_event(db: Session, event_id: int, group_id: int, event_data: EventUpdate, user_id: int) -> Event:
        """更新事件"""
        event = EventService.get_event_by_id(db, event_id, group_id, user_id)
        
        if event_data.title is not None:
            event.title = event_data.title
        if event_data.description is not None:
            event.description = event_data.description
        if event_data.start_time is not None:
            event.start_time = event_data.start_time
        if event_data.end_time is not None:
            event.end_time = event_data.end_time
        if event_data.all_day is not None:
            event.all_day = event_data.all_day
        if event_data.location is not None:
            event.location = event_data.location
        
        # 更新标签关联
        if event_data.label_ids is not None:
            # 删除现有标签关联
            db.query(EventLabel).filter(EventLabel.event_id == event_id).delete()
            # 添加新的标签关联
            for label_id in event_data.label_ids:
                LabelService.add_label_to_event(db, event_id, label_id)
        
        db.commit()
        db.refresh(event)
        
        # 加载标签
        event.labels = LabelService.get_event_labels(db, event.id)
        return event
    
    @staticmethod
    def delete_event(db: Session, event_id: int, group_id: int, user_id: int):
        """删除事件"""
        event = EventService.get_event_by_id(db, event_id, group_id, user_id)
        db.delete(event)
        db.commit()

