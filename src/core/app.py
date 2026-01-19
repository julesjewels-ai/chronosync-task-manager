from dataclasses import dataclass
from enum import Enum, auto
from typing import List

"""
Core application logic for the ChronoSync Scheduler.
Handles task definitions and circadian-based sorting algorithms.
"""

class TaskType(Enum):
    """Enum categorizing the cognitive load of a task."""
    DEEP_WORK = auto()
    SHALLOW_WORK = auto()

@dataclass
class Task:
    """Represents a single work unit."""
    name: str
    task_type: TaskType
    duration_minutes: int

class ChronoSyncScheduler:
    """Manager for scheduling tasks based on biological energy levels."""

    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add_task(self, name: str, task_type: TaskType, duration: int) -> None:
        """
        Add a task to the queue.
        
        Args:
            name: Description of the task.
            task_type: DEEP_WORK or SHALLOW_WORK.
            duration: Estimated time in minutes.
        """
        self.tasks.append(Task(name, task_type, duration))

    def suggest_tasks(self, current_energy_level: int) -> List[Task]:
        """
        Reorders tasks based on current energy.

        Args:
            current_energy_level: Integer 1-10. 
                                  Levels >= 7 are considered 'Peak'.
        
        Returns:
            List[Task]: Sorted list of tasks.
        """
        # Threshold for peak performance
        PEAK_THRESHOLD = 7
        is_peak = current_energy_level >= PEAK_THRESHOLD

        if is_peak:
            # Sort Deep Work to top, preserve original secondary order
            return sorted(self.tasks, key=lambda t: t.task_type != TaskType.DEEP_WORK)
        else:
            # Sort Shallow Work to top
            return sorted(self.tasks, key=lambda t: t.task_type != TaskType.SHALLOW_WORK)