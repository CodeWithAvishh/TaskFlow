from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import time
from datetime import datetime
from . import database
from . import models
from . import schemas
from . import crud
from . import algorithms
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Initialize FastAPI app
app = FastAPI(
    title="TaskFlow API",
    description="Full-stack task and project management system",
    version="1.0.0"
)

# ==================== Database Setup ====================

# Create all tables on startup
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    models.Base.metadata.create_all(bind=database.engine)
    print("Database tables created successfully")


# ==================== CORS Configuration ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Request Timing Middleware ====================

class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Middleware to measure and log request processing time."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        print(f"{request.method} {request.url.path} - {process_time:.4f}s")
        return response


app.add_middleware(RequestTimingMiddleware)


# ==================== Health Check ====================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return {
        "message": "TaskFlow API is running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== User Endpoints ====================

@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Create a new user with unique email."""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    """Get all users with pagination."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    """Get a specific user by ID."""
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    """Update user details."""
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    """Delete a user."""
    db_user = crud.delete_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ==================== Project Endpoints ====================

@app.post("/projects/", response_model=schemas.Project, tags=["Projects"])
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    """Create a new project."""
    # Verify owner exists
    owner = crud.get_user(db, project.owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner (user) not found")
    
    return crud.create_project(db=db, project=project)


@app.get("/projects/", response_model=list[schemas.Project], tags=["Projects"])
def read_projects(
    skip: int = 0,
    limit: int = 10,
    owner_id: int = Query(None),
    db: Session = Depends(database.get_db)
):
    """Get all projects, optionally filtered by owner."""
    projects = crud.get_projects(db, skip=skip, limit=limit, owner_id=owner_id)
    return projects


@app.get("/projects/{project_id}", response_model=schemas.Project, tags=["Projects"])
def read_project(project_id: int, db: Session = Depends(database.get_db)):
    """Get a specific project by ID."""
    db_project = crud.get_project(db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.put("/projects/{project_id}", response_model=schemas.Project, tags=["Projects"])
def update_project(project_id: int, project_update: schemas.ProjectUpdate, db: Session = Depends(database.get_db)):
    """Update project details."""
    db_project = crud.update_project(db, project_id=project_id, project_update=project_update)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.delete("/projects/{project_id}", tags=["Projects"])
def delete_project(project_id: int, db: Session = Depends(database.get_db)):
    """Delete a project."""
    success = crud.delete_project(db, project_id=project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


# ==================== Task Endpoints ====================

@app.post("/tasks/", response_model=schemas.Task, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    """Create a new task."""
    # Verify project exists
    project = crud.get_project(db, task.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Verify creator exists
    creator = crud.get_user(db, task.creator_id)
    if not creator:
        raise HTTPException(status_code=404, detail="Creator (user) not found")
    
    return crud.create_task(db=db, task=task)


@app.get("/tasks/", response_model=list[schemas.Task], tags=["Tasks"])
def read_tasks(
    skip: int = 0,
    limit: int = 20,
    project_id: int = Query(None),
    sort: str = Query(None, description="Sort by: priority, title, due_date"),
    db: Session = Depends(database.get_db)
):
    """
    Get all tasks, optionally filtered by project and sorted.
    
    Query parameters:
    - skip: Number of items to skip (default: 0)
    - limit: Maximum items to return (default: 20)
    - project_id: Filter by project ID
    - sort: Sort by 'priority', 'title', or 'due_date'
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit, project_id=project_id)
    
    # Apply sorting if requested
    if sort == "priority":
        sorted_tasks, stats = algorithms.sort_tasks_by_priority(tasks)
        return sorted_tasks
    
    return tasks


@app.get("/tasks/search", response_model=dict, tags=["Tasks"])
def search_tasks(
    title: str = Query(..., description="Search term"),
    algo: str = Query("linear", description="Search algorithm: binary or linear"),
    project_id: int = Query(None, description="Filter by project ID"),
    db: Session = Depends(database.get_db)
):
    """
    Search tasks by title using specified algorithm.
    
    Query parameters:
    - title: Search term (required)
    - algo: Algorithm to use - 'binary' or 'linear' (default: linear)
    - project_id: Optional project ID filter
    """
    tasks = crud.get_tasks(db, skip=0, limit=1000, project_id=project_id)
    
    if algo.lower() == "binary":
        results, stats = algorithms.search_tasks_binary(tasks, title)
    else:
        results, stats = algorithms.search_tasks_linear(tasks, title)
    
    return {
        "algorithm": algo,
        "search_term": title,
        "results": [schemas.Task.model_validate(task) for task in results],
        "total_results": len(results),
        "statistics": stats
    }


@app.get("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def read_task(task_id: int, db: Session = Depends(database.get_db)):
    """Get a specific task by ID."""
    db_task = crud.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["Tasks"])
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    """Update task details."""
    db_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    """Delete a task."""
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


# ==================== Statistics Endpoints ====================

@app.get("/stats/aggregate", response_model=schemas.AggregateStats, tags=["Statistics"])
def get_aggregate_stats(db: Session = Depends(database.get_db)):
    """Get aggregate statistics across the system."""
    return crud.get_aggregate_stats(db)


# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
