from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.group import (
    Group, GroupCreate, GroupUpdate, 
    GroupMemberAdd, GroupMemberUpdate, GroupMemberDetail
)
from app.services.group import GroupService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/groups", tags=["Groups"])


@router.post("", response_model=Group, status_code=201)
def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建群组"""
    group = GroupService.create_group(db, group_data, current_user.id)
    return group


@router.get("", response_model=list[Group])
def get_my_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的所有群组"""
    groups = GroupService.get_user_groups(db, current_user.id)
    return groups


@router.get("/{group_id}", response_model=Group)
def get_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取群组详情"""
    # 检查访问权限
    GroupService.check_group_access(db, group_id, current_user.id)
    group = GroupService.get_group_by_id(db, group_id)
    return group


@router.put("/{group_id}", response_model=Group)
def update_group(
    group_id: int,
    group_data: GroupUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新群组信息"""
    group = GroupService.update_group(db, group_id, group_data, current_user.id)
    return group


@router.delete("/{group_id}", status_code=204)
def delete_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除群组"""
    GroupService.delete_group(db, group_id, current_user.id)
    return None


@router.post("/{group_id}/members", response_model=dict, status_code=201)
def add_member(
    group_id: int,
    member_data: GroupMemberAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加群组成员"""
    member = GroupService.add_member(db, group_id, member_data.email, member_data.role, current_user.id)
    return {
        "id": member.id,
        "group_id": member.group_id,
        "user_id": member.user_id,
        "role": member.role,
        "joined_at": member.joined_at
    }


@router.get("/{group_id}/members", response_model=list[GroupMemberDetail])
def get_group_members(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取群组成员列表"""
    members = GroupService.get_group_members(db, group_id, current_user.id)
    return members


@router.put("/{group_id}/members/{user_id}", response_model=dict)
def update_member_role(
    group_id: int,
    user_id: int,
    member_data: GroupMemberUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新成员角色"""
    member = GroupService.update_member_role(db, group_id, user_id, member_data.role, current_user.id)
    return {
        "id": member.id,
        "group_id": member.group_id,
        "user_id": member.user_id,
        "role": member.role,
        "joined_at": member.joined_at
    }


@router.delete("/{group_id}/members/{user_id}", status_code=204)
def remove_member(
    group_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """移除群组成员"""
    GroupService.remove_member(db, group_id, user_id, current_user.id)
    return None

