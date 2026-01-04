from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, User, Token, LoginRequest
from app.services.auth import AuthService
from app.api.deps import get_current_user
from app.models.user import User as UserModel

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=User, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    user = AuthService.register(db, user_data)
    return user


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    user = AuthService.authenticate(db, login_data.email, login_data.password)
    access_token = AuthService.create_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def get_me(current_user: UserModel = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

