from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import User, UserUpdate
from app.services.user import UserService
from app.api.deps import get_current_user
from app.models.user import User as UserModel

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.put("/me", response_model=User)
def update_me(
    user_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    user = UserService.update_user(db, current_user.id, user_data)
    return user

