import sys
from datetime import datetime, timedelta, time
from src.core.models import Task, TaskType, SleepData, EnergyLog
from src.core.analyzer import SimpleCircadianAnalyzer
from src.core.scheduler import ChronoSyncScheduler

def main():
    print("Welcome to ChronoSync Productivity Scheduler")

    # 1. Simulate Data Ingestion
    print("Ingesting (Simulated) Data...")

    # Simulate recent sleep
    today = datetime.now().date()
    sleep_data = [
        SleepData(
            start_time=datetime.combine(today - timedelta(days=1), time(23, 0)),
            end_time=datetime.combine(today, time(7, 0)),
            quality_score=85
        )
    ]

    # Simulate energy logs (past few days average pattern)
    # Let's say user is a morning lark: Peak 9-11AM, Dip 2-4PM.
    energy_logs = []
    # Morning Peak
    for h in [9, 10]:
        energy_logs.append(EnergyLog(datetime.combine(today, time(h, 30)), level=9))
    # Afternoon Dip
    for h in [14, 15]:
        energy_logs.append(EnergyLog(datetime.combine(today, time(h, 30)), level=3))
    # Evening Neutral
    for h in [18, 19]:
        energy_logs.append(EnergyLog(datetime.combine(today, time(h, 30)), level=6))

    # 2. Analyze
    analyzer = SimpleCircadianAnalyzer()
    profile = analyzer.analyze(sleep_data, energy_logs)

    print("\nCalculated Circadian Profile:")
    print("Peaks:", profile.peaks)
    print("Dips:", profile.dips)

    # 3. Input Tasks
    print("\nDefining Tasks...")
    tasks = [
        Task("Write Report", TaskType.DEEP_WORK, 90, priority=5),
        Task("Email Correspondence", TaskType.SHALLOW_WORK, 30, priority=3),
        Task("Code Review", TaskType.DEEP_WORK, 60, priority=4),
        Task("Team Meeting", TaskType.SHALLOW_WORK, 45, priority=2),
    ]

    # 4. Schedule
    print("\nGenerating Schedule...")
    scheduler = ChronoSyncScheduler()
    # Start scheduling from 8 AM today
    start_time = datetime.combine(today, time(8, 0))
    schedule = scheduler.schedule(tasks, profile, start_time)
    
    print(f"\nSchedule for {today}:")
    for item in schedule.items:
        start_str = item.start_time.strftime("%H:%M")
        end_str = item.end_time.strftime("%H:%M")
        print(f"{start_str} - {end_str}: [{item.task.task_type.name}] {item.task.name}")

if __name__ == "__main__":
    main()
