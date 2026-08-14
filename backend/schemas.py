from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PriorityEnum(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    pass


class UserUpdate(BaseModel):
    """User update schema."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    """User response schema."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Project Schemas
class ProjectBase(BaseModel):
    """Base project schema."""
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Project creation schema."""
    owner_id: int


class ProjectUpdate(BaseModel):
    """Project update schema."""
    name: Optional[str] = None
    description: Optional[str] = None


class Project(ProjectBase):
    """Project response schema."""
    id: int
    owner_id: int
    created_at: datetime
    owner: Optional[User] = None

    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    """Base task schema."""
    title: str
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.MEDIUM
    due_date: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    """Task creation schema."""
    project_id: int
    creator_id: int


class TaskUpdate(BaseModel):
    """Task update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    """Task response schema."""
    id: int
    project_id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    project: Optional[Project] = None
    creator: Optional[User] = None

    class Config:
        from_attributes = True


# Statistics Schema
class AggregateStats(BaseModel):
    """Aggregate statistics schema."""
    total_users: int
    total_projects: int
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    high_priority_tasks: int
    medium_priority_tasks: int
    low_priority_tasks: int
