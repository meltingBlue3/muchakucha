from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ===== Group Schemas =====

class GroupBase(BaseModel):
    """群组基础模式"""
    name: str
    description: str | None = None


class GroupCreate(GroupBase):
    """群组创建模式"""
    pass


class GroupUpdate(BaseModel):
    """群组更新模式"""
    name: str | None = None
    description: str | None = None


class GroupInDB(GroupBase):
    """数据库中的群组模式"""
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Group(GroupInDB):
    """群组响应模式"""
    pass


# ===== Group Member Schemas =====

class GroupMemberBase(BaseModel):
    """群组成员基础模式"""
    role: str = "member"  # owner, admin, member


class GroupMemberAdd(BaseModel):
    """添加群组成员模式"""
    email: EmailStr
    role: str = "member"


class GroupMemberUpdate(BaseModel):
    """更新群组成员模式"""
    role: str


class GroupMemberInDB(BaseModel):
    """数据库中的群组成员模式"""
    id: int
    group_id: int
    user_id: int
    role: str
    joined_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class GroupMember(GroupMemberInDB):
    """群组成员响应模式"""
    pass


class GroupMemberDetail(BaseModel):
    """群组成员详情模式（包含用户信息）"""
    id: int
    group_id: int
    user_id: int
    role: str
    joined_at: datetime
    user_email: str
    user_nickname: str
    
    model_config = ConfigDict(from_attributes=True)

