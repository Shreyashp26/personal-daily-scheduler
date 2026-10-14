
from datetime import time, datetime

from pydantic import BaseModel, ConfigDict, model_validator


class TaskCreate(BaseModel):
    name: str
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def check_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be later than start time.")
        return self


class TaskResponse(BaseModel):
    id: int
    name: str
    start_time: time
    end_time: time
    status: str
    actual_started_at: datetime | None
    actual_finished_at: datetime | None
    actual_duration_minutes: float | None = None
    planned_duration_minutes: int | None = None
    time_difference_minutes: float | None = None

    model_config = ConfigDict(from_attributes=True)
