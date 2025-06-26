from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

app = FastAPI(title="Simple Task Manager")

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: int = Field(..., ge=1, le=5, description="Priority from 1 (lowest) to 5 (highest)")

class Task(TaskBase):
    id: UUID = Field(default_factory=uuid4)
    status: constr(pattern="^(pending|done)$") = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# In-memory store
tasks: List[Task] = []

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    """Get all tasks."""
    return tasks

@app.get("/tasks/pending", response_model=List[Task])
def get_pending_tasks():
    """Get only pending tasks."""
    return [t for t in tasks if t.status == "pending"]

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID):
    """Get a specific task by ID."""
    for t in tasks:
        if t.id == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_data: TaskBase):
    """Create a new task with generated ID, default status 'pending' and timestamp."""
    new_task = Task(**task_data.dict())
    tasks.append(new_task)
    return new_task

@app.post("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: UUID):
    """Mark a specific task as done."""
    for t in tasks:
        if t.id == task_id:
            t.status = "done"
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks/{task_id}/uncomplete", response_model=Task)
def uncomplete_task(task_id: UUID):
    """Revert a specific task back to pending."""
    for t in tasks:
        if t.id == task_id:
            t.status = "pending"
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: UUID):
    """Delete a task by ID."""
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")

# To run: uvicorn main:app --reload
