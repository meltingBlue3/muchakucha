from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.group import GroupService


class TaskService:
    """任务服务"""
    
    @staticmethod
    def create_task(db: Session, group_id: int, task_data: TaskCreate, creator_id: int) -> Task:
        """创建任务"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, creator_id)
        
        db_task = Task(
            group_id=group_id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            status=task_data.status,
            priority=task_data.priority,
            assigned_to=task_data.assigned_to,
            created_by=creator_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def get_task_by_id(db: Session, task_id: int, group_id: int, user_id: int) -> Task:
        """根据 ID 获取任务"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        task = db.query(Task).filter(Task.id == task_id, Task.group_id == group_id).first()
        if not task:
            raise NotFoundException(detail="Task not found")
        return task
    
    @staticmethod
    def get_group_tasks(
        db: Session, 
        group_id: int, 
        user_id: int,
        status: str | None = None,
        priority: str | None = None
    ) -> list[Task]:
        """获取群组的任务列表"""
        # 检查群组访问权限
        GroupService.check_group_access(db, group_id, user_id)
        
        query = db.query(Task).filter(Task.group_id == group_id)
        
        # 状态过滤
        if status:
            query = query.filter(Task.status == status)
        
        # 优先级过滤
        if priority:
            query = query.filter(Task.priority == priority)
        
        tasks = query.order_by(Task.created_at.desc()).all()
        return tasks
    
    @staticmethod
    def update_task(db: Session, task_id: int, group_id: int, task_data: TaskUpdate, user_id: int) -> Task:
        """更新任务"""
        task = TaskService.get_task_by_id(db, task_id, group_id, user_id)
        
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.due_date is not None:
            task.due_date = task_data.due_date
        if task_data.status is not None:
            task.status = task_data.status
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.assigned_to is not None:
            task.assigned_to = task_data.assigned_to
        
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def delete_task(db: Session, task_id: int, group_id: int, user_id: int):
        """删除任务"""
        task = TaskService.get_task_by_id(db, task_id, group_id, user_id)
        db.delete(task)
        db.commit()

