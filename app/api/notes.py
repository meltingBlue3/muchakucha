from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.note import Note, NoteCreate, NoteUpdate
from app.services.note import NoteService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/groups/{group_id}/notes", tags=["Notes"])


@router.post("", response_model=Note, status_code=201)
def create_note(
    group_id: int,
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建笔记"""
    note = NoteService.create_note(db, group_id, note_data, current_user.id)
    return note


@router.get("", response_model=list[Note])
def get_notes(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取笔记列表"""
    notes = NoteService.get_group_notes(db, group_id, current_user.id)
    return notes


@router.get("/{note_id}", response_model=Note)
def get_note(
    group_id: int,
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取笔记详情"""
    note = NoteService.get_note_by_id(db, note_id, group_id, current_user.id)
    return note


@router.put("/{note_id}", response_model=Note)
def update_note(
    group_id: int,
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新笔记"""
    note = NoteService.update_note(db, note_id, group_id, note_data, current_user.id)
    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(
    group_id: int,
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除笔记"""
    NoteService.delete_note(db, note_id, group_id, current_user.id)
    return None

