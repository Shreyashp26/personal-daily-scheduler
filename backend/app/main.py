
from fastapi import FastAPI
from app.database import Base, engine
from app.models.task import Task
from app.routers.task_router import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Daily Scheduler")

app.include_router(task_router)


@app.get("/")
def home():
    return {"message": "Personal Daily Scheduler API is running!"}
