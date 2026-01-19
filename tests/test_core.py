import pytest
from src.core.app import ChronoSyncScheduler, TaskType, Task

"""
Unit tests for the ChronoSync core logic.
"""

def test_add_task():
    scheduler = ChronoSyncScheduler()
    scheduler.add_task("Test Task", TaskType.DEEP_WORK, 60)
    assert len(scheduler.tasks) == 1
    assert scheduler.tasks[0].name == "Test Task"

def test_high_energy_prioritization():
    scheduler = ChronoSyncScheduler()
    scheduler.add_task("Shallow Task", TaskType.SHALLOW_WORK, 10)
    scheduler.add_task("Deep Task", TaskType.DEEP_WORK, 60)
    
    # Energy 9/10 (Peak) -> Expect Deep Work first
    sorted_tasks = scheduler.suggest_tasks(9)
    
    assert sorted_tasks[0].task_type == TaskType.DEEP_WORK
    assert sorted_tasks[1].task_type == TaskType.SHALLOW_WORK

def test_low_energy_prioritization():
    scheduler = ChronoSyncScheduler()
    scheduler.add_task("Deep Task", TaskType.DEEP_WORK, 60)
    scheduler.add_task("Shallow Task", TaskType.SHALLOW_WORK, 10)
    
    # Energy 3/10 (Dip) -> Expect Shallow Work first
    sorted_tasks = scheduler.suggest_tasks(3)
    
    assert sorted_tasks[0].task_type == TaskType.SHALLOW_WORK
    assert sorted_tasks[1].task_type == TaskType.DEEP_WORK