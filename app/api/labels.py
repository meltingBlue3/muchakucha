from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.label import Label, LabelCreate, LabelUpdate, LabelWithStats
from app.services.label import LabelService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/groups/{group_id}/labels", tags=["Labels"])


@router.post("", response_model=Label, status_code=201)
def create_label(
    group_id: int,
    label_data: LabelCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建标签"""
    label = LabelService.create_label(db, group_id, label_data, current_user.id)
    return label


@router.get("", response_model=list[Label])
def get_labels(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取群组所有标签"""
    labels = LabelService.get_group_labels(db, group_id, current_user.id)
    return labels


@router.get("/stats", response_model=list[LabelWithStats])
def get_labels_stats(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取带统计信息的标签列表"""
    labels = LabelService.get_labels_with_stats(db, group_id, current_user.id)
    return labels


@router.get("/{label_id}", response_model=Label)
def get_label(
    group_id: int,
    label_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取标签详情"""
    label = LabelService.get_label_by_id(db, label_id, group_id, current_user.id)
    return label


@router.put("/{label_id}", response_model=Label)
def update_label(
    group_id: int,
    label_id: int,
    label_data: LabelUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新标签"""
    label = LabelService.update_label(db, label_id, group_id, label_data, current_user.id)
    return label


@router.delete("/{label_id}", status_code=204)
def delete_label(
    group_id: int,
    label_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除标签"""
    LabelService.delete_label(db, label_id, group_id, current_user.id)
    return None

