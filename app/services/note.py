from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.group import GroupService


class NoteService:
    """笔记服务"""
    
    @staticmethod
    def create_note(db: Session, group_id: int, note_data: NoteCreate, creator_id: int) -> Note:
        """创建笔记"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, creator_id)
        
        db_note = Note(
            group_id=group_id,
            title=note_data.title,
            content=note_data.content,
            created_by=creator_id
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    
    @staticmethod
    def get_note_by_id(db: Session, note_id: int, group_id: int, user_id: int) -> Note:
        """根据 ID 获取笔记"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        note = db.query(Note).filter(Note.id == note_id, Note.group_id == group_id).first()
        if not note:
            raise NotFoundException(detail="Note not found")
        return note
    
    @staticmethod
    def get_group_notes(db: Session, group_id: int, user_id: int) -> list[Note]:
        """获取群组的笔记列表"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        notes = db.query(Note).filter(Note.group_id == group_id).order_by(Note.created_at.desc()).all()
        return notes
    
    @staticmethod
    def update_note(db: Session, note_id: int, group_id: int, note_data: NoteUpdate, user_id: int) -> Note:
        """更新笔记"""
        note = NoteService.get_note_by_id(db, note_id, group_id, user_id)
        
        if note_data.title is not None:
            note.title = note_data.title
        if note_data.content is not None:
            note.content = note_data.content
        
        db.commit()
        db.refresh(note)
        return note
    
    @staticmethod
    def delete_note(db: Session, note_id: int, group_id: int, user_id: int):
        """删除笔记"""
        note = NoteService.get_note_by_id(db, note_id, group_id, user_id)
        db.delete(note)
        db.commit()

