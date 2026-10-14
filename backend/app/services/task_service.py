
from datetime import datetime


def calculate_duration(start: datetime, finish: datetime):
    duration = finish - start
    return round(duration.total_seconds() / 60, 2)


def get_actual_duration(task):
    if task.actual_started_at is None:
        return None

    if task.actual_finished_at is None:
        return None

    return calculate_duration(
        task.actual_started_at,
        task.actual_finished_at
    )

def get_planned_duration(task):
    planned_duration = (
        task.end_time.hour * 60
        + task.end_time.minute
        - task.start_time.hour * 60
        - task.start_time.minute
    )

    return planned_duration



def get_time_difference(task):
    planned = get_planned_duration(task)
    actual = get_actual_duration(task)

    if actual is None:
        return None

    return round(planned - actual, 2)
