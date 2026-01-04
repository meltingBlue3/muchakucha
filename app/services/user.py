from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.user import User
from app.schemas.user import UserUpdate


class UserService:
    """用户服务"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """根据 ID 获取用户"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException(detail="User not found")
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """更新用户信息"""
        user = UserService.get_user_by_id(db, user_id)
        
        if user_data.nickname is not None:
            user.nickname = user_data.nickname
        
        db.commit()
        db.refresh(user)
        return user

