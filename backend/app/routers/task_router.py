
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.task import Task
from app.database import get_db
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskResponse

from app.services.task_service import (
    get_actual_duration,
    get_planned_duration,
    get_time_difference,
)


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    return task_repository.create_task(
        db=db,
        name=task_data.name,
        start_time=task_data.start_time,
        end_time=task_data.end_time
    )


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return task_repository.get_all_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    
    response: TaskResponse = TaskResponse.model_validate(task)
    response.planned_duration_minutes = get_planned_duration(task)
    response.actual_duration_minutes = get_actual_duration(task)
    response.time_difference_minutes = get_time_difference(task)

    return response



@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_repository.delete_task(db, task)

    return {"message": f"Task {task_id} deleted successfully"}




@router.patch("/{task_id}/start", response_model=TaskResponse)
def start_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending tasks can be started"
        )

    return task_repository.start_task(db, task)


@router.patch("/{task_id}/finish", response_model=TaskResponse)
def finish_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repository.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail="Only in-progress tasks can be finished"
        )

    return task_repository.finish_task(db, task)
