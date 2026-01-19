from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime, time
from typing import List, Tuple

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
    priority: int = 1 # 1 (Low) to 5 (High)
    deadline: datetime = None

@dataclass
class SleepData:
    """Represents a sleep session."""
    start_time: datetime
    end_time: datetime
    quality_score: int # 1-100

@dataclass
class EnergyLog:
    """Represents a manual energy log."""
    timestamp: datetime
    level: int # 1-10

class EnergyState(Enum):
    PEAK = auto()
    DIP = auto()
    NEUTRAL = auto()

@dataclass
class CircadianProfile:
    """Defines the user's energy patterns."""
    peaks: List[Tuple[time, time]] = field(default_factory=list)
    dips: List[Tuple[time, time]] = field(default_factory=list)

@dataclass
class ScheduleItem:
    """A task assigned to a time slot."""
    task: Task
    start_time: datetime
    end_time: datetime

@dataclass
class Schedule:
    """A generated schedule."""
    items: List[ScheduleItem] = field(default_factory=list)
