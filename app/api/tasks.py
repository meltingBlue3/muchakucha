from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task import TaskService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/groups/{group_id}/tasks", tags=["Tasks"])


@router.post("", response_model=Task, status_code=201)
def create_task(
    group_id: int,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建任务"""
    task = TaskService.create_task(db, group_id, task_data, current_user.id)
    return task


@router.get("", response_model=list[Task])
def get_tasks(
    group_id: int,
    status: str | None = Query(None),
    priority: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取任务列表（支持状态/优先级过滤）"""
    tasks = TaskService.get_group_tasks(db, group_id, current_user.id, status, priority)
    return tasks


@router.get("/{task_id}", response_model=Task)
def get_task(
    group_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取任务详情"""
    task = TaskService.get_task_by_id(db, task_id, group_id, current_user.id)
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    group_id: int,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新任务"""
    task = TaskService.update_task(db, task_id, group_id, task_data, current_user.id)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    group_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除任务"""
    TaskService.delete_task(db, task_id, group_id, current_user.id)
    return None

