from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.exceptions import UnauthorizedException, ConflictException
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    """认证服务"""
    
    @staticmethod
    def register(db: Session, user_data: UserCreate) -> User:
        """用户注册"""
        # 检查邮箱是否已存在
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ConflictException(detail="Email already registered")
        
        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            nickname=user_data.nickname,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User:
        """用户认证"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise UnauthorizedException(detail="Incorrect email or password")
        
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException(detail="Incorrect email or password")
        
        return user
    
    @staticmethod
    def create_token(user_id: int) -> str:
        """创建 JWT Token"""
        return create_access_token(data={"sub": str(user_id)})

