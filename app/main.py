
from pathlib import Path
from datetime import date

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import or_

from .database import Base, engine, get_db
from .models import Task


# -----------------------------
# Application Configuration
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow — Task Manager")

# Static files configuration
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Jinja2 templates configuration
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# -----------------------------
# Dashboard - Read Tasks
# -----------------------------

@app.get("/")
def dashboard(
    request: Request,
    status: str = "all",
    q: str = "",
    db: Session = Depends(get_db)
):

    query = db.query(Task)

    if status == "pending":
        query = query.filter(Task.completed.is_(False))

    elif status == "completed":
        query = query.filter(Task.completed.is_(True))

    if q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Task.title.ilike(term),
                Task.description.ilike(term)
            )
        )

    tasks = query.order_by(
        Task.completed.asc(),
        Task.created_at.desc()
    ).all()

    all_tasks = db.query(Task).all()

    total = len(all_tasks)

    completed_count = sum(
        1 for task in all_tasks if task.completed
    )

    pending_count = total - completed_count

    completion_rate = (
        round((completed_count / total) * 100)
        if total else 0
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": tasks,
            "status": status,
            "q": q,
            "total": total,
            "completed_count": completed_count,
            "pending_count": pending_count,
            "completion_rate": completion_rate,
            "today": date.today().isoformat()
        }
    )


# -----------------------------
# Display Create Task Form
# -----------------------------

@app.get("/tasks/new")
def new_task_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="task_form.html",
        context={
            "task": None,
            "page_title": "Create a task"
        }
    )


# -----------------------------
# Create Task
# -----------------------------

@app.post("/tasks")
def create_task(
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    due_date: str = Form(""),
    db: Session = Depends(get_db)
):

    title = title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Task title is required"
        )

    if priority not in {"Low", "Medium", "High"}:
        priority = "Medium"

    task = Task(
        title=title,
        description=description.strip(),
        priority=priority,
        due_date=due_date or None
    )

    db.add(task)
    db.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )


# -----------------------------
# Display Edit Task Form
# -----------------------------

@app.get("/tasks/{task_id}/edit")
def edit_task_page(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="task_form.html",
        context={
            "task": task,
            "page_title": "Edit task"
        }
    )


# -----------------------------
# Update Task
# -----------------------------

@app.post("/tasks/{task_id}/edit")
def update_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    due_date: str = Form(""),
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    title = title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Task title is required"
        )

    task.title = title
    task.description = description.strip()

    task.priority = (
        priority
        if priority in {"Low", "Medium", "High"}
        else "Medium"
    )

    task.due_date = due_date or None

    db.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )


# -----------------------------
# Toggle Task Completion
# -----------------------------

@app.post("/tasks/{task_id}/toggle")
def toggle_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.completed = not task.completed

    db.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )


# -----------------------------
# Delete Task
# -----------------------------

@app.post("/tasks/{task_id}/delete")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )
