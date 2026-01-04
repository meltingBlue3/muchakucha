from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.event import Event, EventCreate, EventUpdate
from app.services.event import EventService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/groups/{group_id}/events", tags=["Events"])


@router.post("", response_model=Event, status_code=201)
def create_event(
    group_id: int,
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建事件"""
    event = EventService.create_event(db, group_id, event_data, current_user.id)
    return event


@router.get("", response_model=list[Event])
def get_events(
    group_id: int,
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取事件列表（支持日期范围过滤）"""
    events = EventService.get_group_events(db, group_id, current_user.id, start_date, end_date)
    return events


@router.get("/{event_id}", response_model=Event)
def get_event(
    group_id: int,
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取事件详情"""
    event = EventService.get_event_by_id(db, event_id, group_id, current_user.id)
    return event


@router.put("/{event_id}", response_model=Event)
def update_event(
    group_id: int,
    event_id: int,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新事件"""
    event = EventService.update_event(db, event_id, group_id, event_data, current_user.id)
    return event


@router.delete("/{event_id}", status_code=204)
def delete_event(
    group_id: int,
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除事件"""
    EventService.delete_event(db, event_id, group_id, current_user.id)
    return None

