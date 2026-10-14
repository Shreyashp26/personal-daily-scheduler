
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.task import Task


def create_task(
    db: Session,
    name: str,
    start_time,
    end_time
):
    task = Task(
        name=name,
        start_time=start_time,
        end_time=end_time
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_all_tasks(db: Session):
    return db.query(Task).order_by(Task.start_time).all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()




def start_task(db: Session, task: Task):
    task.status = "in_progress"
    task.actual_started_at = datetime.now()

    db.commit()
    db.refresh(task)

    return task


def finish_task(db: Session, task: Task):
    task.status = "completed"
    task.actual_finished_at = datetime.now()

    db.commit()
    db.refresh(task)

    return task