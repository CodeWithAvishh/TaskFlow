from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
from . import schemas
from datetime import datetime


# ==================== User Operations ====================

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user."""
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    """Get user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """Get all users with pagination."""
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """Update user details."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Delete a user."""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# ==================== Project Operations ====================

def create_project(db: Session, project: schemas.ProjectCreate):
    """Create a new project."""
    db_project = models.Project(
        name=project.name,
        description=project.description,
        owner_id=project.owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project(db: Session, project_id: int):
    """Get project by ID."""
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 10, owner_id: int = None):
    """Get projects with optional filtering by owner."""
    query = db.query(models.Project)
    if owner_id:
        query = query.filter(models.Project.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()


def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    """Update project details."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    """Delete a project."""
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False


# ==================== Task Operations ====================

def create_task(db: Session, task: schemas.TaskCreate):
    """Create a new task."""
    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        project_id=task.project_id,
        creator_id=task.creator_id,
        due_date=task.due_date,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    """Get task by ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 20, project_id: int = None):
    """Get tasks with optional filtering by project."""
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    return query.offset(skip).limit(limit).all()


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    """Update task details."""
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    """Delete a task."""
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False


# ==================== Statistics Operations ====================

def get_aggregate_stats(db: Session) -> schemas.AggregateStats:
    """Get aggregate statistics across the system."""
    total_users = db.query(func.count(models.User.id)).scalar() or 0
    total_projects = db.query(func.count(models.Project.id)).scalar() or 0
    total_tasks = db.query(func.count(models.Task.id)).scalar() or 0
    
    completed_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.completed == True
    ).scalar() or 0
    
    pending_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.completed == False
    ).scalar() or 0
    
    high_priority_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.priority == models.PriorityEnum.HIGH
    ).scalar() or 0
    
    medium_priority_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.priority == models.PriorityEnum.MEDIUM
    ).scalar() or 0
    
    low_priority_tasks = db.query(func.count(models.Task.id)).filter(
        models.Task.priority == models.PriorityEnum.LOW
    ).scalar() or 0
    
    return schemas.AggregateStats(
        total_users=total_users,
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        high_priority_tasks=high_priority_tasks,
        medium_priority_tasks=medium_priority_tasks,
        low_priority_tasks=low_priority_tasks
    )
