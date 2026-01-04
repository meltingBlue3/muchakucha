from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.models.group import Group, GroupMember
from app.models.user import User
from app.schemas.group import GroupCreate, GroupUpdate


class GroupService:
    """群组服务"""
    
    @staticmethod
    def create_group(db: Session, group_data: GroupCreate, creator_id: int) -> Group:
        """创建群组"""
        # 创建群组
        db_group = Group(
            name=group_data.name,
            description=group_data.description,
            created_by=creator_id
        )
        db.add(db_group)
        db.flush()  # 获取 group id
        
        # 将创建者添加为群组 owner
        db_member = GroupMember(
            group_id=db_group.id,
            user_id=creator_id,
            role="owner"
        )
        db.add(db_member)
        db.commit()
        db.refresh(db_group)
        return db_group
    
    @staticmethod
    def get_group_by_id(db: Session, group_id: int) -> Group:
        """根据 ID 获取群组"""
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            raise NotFoundException(detail="Group not found")
        return group
    
    @staticmethod
    def get_user_groups(db: Session, user_id: int) -> list[Group]:
        """获取用户所属的所有群组"""
        groups = (
            db.query(Group)
            .join(GroupMember, Group.id == GroupMember.group_id)
            .filter(GroupMember.user_id == user_id)
            .all()
        )
        return groups
    
    @staticmethod
    def update_group(db: Session, group_id: int, group_data: GroupUpdate, user_id: int) -> Group:
        """更新群组信息"""
        group = GroupService.get_group_by_id(db, group_id)
        
        # 检查权限（只有 owner 和 admin 可以更新）
        if not GroupService.is_group_admin(db, group_id, user_id):
            raise ForbiddenException(detail="Only group owner or admin can update group")
        
        if group_data.name is not None:
            group.name = group_data.name
        if group_data.description is not None:
            group.description = group_data.description
        
        db.commit()
        db.refresh(group)
        return group
    
    @staticmethod
    def delete_group(db: Session, group_id: int, user_id: int):
        """删除群组"""
        group = GroupService.get_group_by_id(db, group_id)
        
        # 只有 owner 可以删除群组
        if not GroupService.is_group_owner(db, group_id, user_id):
            raise ForbiddenException(detail="Only group owner can delete group")
        
        # 删除所有成员
        db.query(GroupMember).filter(GroupMember.group_id == group_id).delete()
        
        # 删除群组
        db.delete(group)
        db.commit()
    
    @staticmethod
    def add_member(db: Session, group_id: int, email: str, role: str, requester_id: int) -> GroupMember:
        """添加群组成员"""
        # 检查请求者权限
        if not GroupService.is_group_admin(db, group_id, requester_id):
            raise ForbiddenException(detail="Only group owner or admin can add members")
        
        # 查找要添加的用户
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise NotFoundException(detail=f"User with email {email} not found")
        
        # 检查是否已经是成员
        existing = db.query(GroupMember).filter(
            and_(GroupMember.group_id == group_id, GroupMember.user_id == user.id)
        ).first()
        if existing:
            raise BadRequestException(detail="User is already a member of this group")
        
        # 添加成员
        db_member = GroupMember(
            group_id=group_id,
            user_id=user.id,
            role=role
        )
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return db_member
    
    @staticmethod
    def get_group_members(db: Session, group_id: int, user_id: int) -> list[dict]:
        """获取群组成员列表"""
        # 检查用户是否是群组成员
        if not GroupService.is_group_member(db, group_id, user_id):
            raise ForbiddenException(detail="You are not a member of this group")
        
        # 获取成员列表，包含用户信息
        members = (
            db.query(GroupMember, User)
            .join(User, GroupMember.user_id == User.id)
            .filter(GroupMember.group_id == group_id)
            .all()
        )
        
        result = []
        for member, user in members:
            result.append({
                "id": member.id,
                "group_id": member.group_id,
                "user_id": member.user_id,
                "role": member.role,
                "joined_at": member.joined_at,
                "user_email": user.email,
                "user_nickname": user.nickname,
            })
        return result
    
    @staticmethod
    def update_member_role(db: Session, group_id: int, target_user_id: int, new_role: str, requester_id: int) -> GroupMember:
        """更新成员角色"""
        # 检查请求者权限（只有 owner 可以修改角色）
        if not GroupService.is_group_owner(db, group_id, requester_id):
            raise ForbiddenException(detail="Only group owner can update member roles")
        
        # 不能修改自己的角色
        if target_user_id == requester_id:
            raise BadRequestException(detail="Cannot change your own role")
        
        # 查找成员
        member = db.query(GroupMember).filter(
            and_(GroupMember.group_id == group_id, GroupMember.user_id == target_user_id)
        ).first()
        if not member:
            raise NotFoundException(detail="Member not found in this group")
        
        member.role = new_role
        db.commit()
        db.refresh(member)
        return member
    
    @staticmethod
    def remove_member(db: Session, group_id: int, target_user_id: int, requester_id: int):
        """移除群组成员"""
        # 检查请求者权限
        if not GroupService.is_group_admin(db, group_id, requester_id):
            raise ForbiddenException(detail="Only group owner or admin can remove members")
        
        # 不能移除 owner
        member = db.query(GroupMember).filter(
            and_(GroupMember.group_id == group_id, GroupMember.user_id == target_user_id)
        ).first()
        if not member:
            raise NotFoundException(detail="Member not found in this group")
        
        if member.role == "owner":
            raise BadRequestException(detail="Cannot remove group owner")
        
        db.delete(member)
        db.commit()
    
    # ===== 权限检查辅助方法 =====
    
    @staticmethod
    def is_group_member(db: Session, group_id: int, user_id: int) -> bool:
        """检查用户是否是群组成员"""
        member = db.query(GroupMember).filter(
            and_(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        ).first()
        return member is not None
    
    @staticmethod
    def is_group_admin(db: Session, group_id: int, user_id: int) -> bool:
        """检查用户是否是群组管理员（owner 或 admin）"""
        member = db.query(GroupMember).filter(
            and_(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        ).first()
        return member is not None and member.role in ["owner", "admin"]
    
    @staticmethod
    def is_group_owner(db: Session, group_id: int, user_id: int) -> bool:
        """检查用户是否是群组所有者"""
        member = db.query(GroupMember).filter(
            and_(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        ).first()
        return member is not None and member.role == "owner"
    
    @staticmethod
    def check_group_access(db: Session, group_id: int, user_id: int):
        """检查用户对群组的访问权限（抛出异常）"""
        if not GroupService.is_group_member(db, group_id, user_id):
            raise ForbiddenException(detail="You are not a member of this group")

