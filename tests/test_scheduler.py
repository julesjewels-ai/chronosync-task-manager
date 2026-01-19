import pytest
from datetime import datetime, time, timedelta
from src.core.models import Task, TaskType, CircadianProfile, Schedule
from src.core.scheduler import ChronoSyncScheduler

def test_schedule_deep_work_in_peak():
    scheduler = ChronoSyncScheduler()
    profile = CircadianProfile(
        peaks=[(time(9, 0), time(11, 0))], # 9-11 AM Peak
        dips=[]
    )

    tasks = [
        Task("Deep Task", TaskType.DEEP_WORK, 60, priority=5),
        Task("Shallow Task", TaskType.SHALLOW_WORK, 60, priority=1)
    ]

    start_time = datetime(2023, 1, 1, 9, 0) # Start exactly at peak
    schedule = scheduler.schedule(tasks, profile, start_time)

    # Expect Deep Task first
    assert len(schedule.items) == 2
    assert schedule.items[0].task.name == "Deep Task"
    assert schedule.items[1].task.name == "Shallow Task"

def test_schedule_shallow_work_in_dip():
    scheduler = ChronoSyncScheduler()
    profile = CircadianProfile(
        peaks=[],
        dips=[(time(14, 0), time(16, 0))] # 2-4 PM Dip
    )

    tasks = [
        Task("Deep Task", TaskType.DEEP_WORK, 60, priority=5),
        Task("Shallow Task", TaskType.SHALLOW_WORK, 60, priority=1)
    ]

    start_time = datetime(2023, 1, 1, 14, 0) # Start at dip
    schedule = scheduler.schedule(tasks, profile, start_time)

    # Expect Shallow Task first, despite lower priority, because of Dip
    assert len(schedule.items) == 2
    assert schedule.items[0].task.name == "Shallow Task"
    assert schedule.items[1].task.name == "Deep Task"

def test_schedule_respects_time():
    scheduler = ChronoSyncScheduler()
    profile = CircadianProfile() # All Neutral

    tasks = [
        Task("Task 1", TaskType.SHALLOW_WORK, 30),
        Task("Task 2", TaskType.SHALLOW_WORK, 30)
    ]

    start_time = datetime(2023, 1, 1, 9, 0)
    schedule = scheduler.schedule(tasks, profile, start_time)

    assert schedule.items[0].start_time == start_time
    assert schedule.items[0].end_time == start_time + timedelta(minutes=30)

    assert schedule.items[1].start_time == start_time + timedelta(minutes=30)
    assert schedule.items[1].end_time == start_time + timedelta(minutes=60)
