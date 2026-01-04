from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ===== User Schemas =====

class UserBase(BaseModel):
    """用户基础模式"""
    email: EmailStr
    nickname: str


class UserCreate(UserBase):
    """用户创建模式"""
    password: str


class UserUpdate(BaseModel):
    """用户更新模式"""
    nickname: str | None = None


class UserInDB(UserBase):
    """数据库中的用户模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    """用户响应模式"""
    pass


# ===== Auth Schemas =====

class Token(BaseModel):
    """Token 响应模式"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 数据模式"""
    user_id: int | None = None


class LoginRequest(BaseModel):
    """登录请求模式"""
    email: EmailStr
    password: str

