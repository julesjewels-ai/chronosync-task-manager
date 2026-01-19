from typing import Protocol, List
from datetime import datetime
from .models import SleepData, EnergyLog, CircadianProfile, Task, Schedule

class DataIngestion(Protocol):
    def ingest_sleep_data(self) -> List[SleepData]:
        ...

    def ingest_energy_logs(self) -> List[EnergyLog]:
        ...

class Analyzer(Protocol):
    def analyze(self, sleep_data: List[SleepData], energy_logs: List[EnergyLog]) -> CircadianProfile:
        ...

class Scheduler(Protocol):
    def schedule(self, tasks: List[Task], profile: CircadianProfile, start_time: datetime) -> Schedule:
        ...
