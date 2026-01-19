import argparse
import sys
from src.core.app import ChronoSyncScheduler, TaskType

"""
Entry point for the ChronoSync Task Manager application.
"""

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ChronoSync: Schedule tasks based on energy levels."
    )
    parser.add_argument(
        "--energy", 
        type=int, 
        choices=range(1, 11), 
        default=7,
        help="Current energy level (1-10). Defaults to 7."
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    print(f"[*] Initializing ChronoSync (Energy Level: {args.energy}/10)...")

    scheduler = ChronoSyncScheduler()

    # Seed with some example data for the MVP
    print("[*] Loading pending tasks...")
    scheduler.add_task("Write Q3 Report", TaskType.DEEP_WORK, 90)
    scheduler.add_task("Email Catch-up", TaskType.SHALLOW_WORK, 30)
    scheduler.add_task("Code Review", TaskType.DEEP_WORK, 45)
    scheduler.add_task("Team Standup", TaskType.SHALLOW_WORK, 15)
    scheduler.add_task("Update Jira", TaskType.SHALLOW_WORK, 10)

    # Get optimization
    optimized_schedule = scheduler.suggest_tasks(args.energy)
    
    print("\n=== Optimized Schedule ===")
    if args.energy >= 7:
        print("Detected Biological Peak: Prioritizing Deep Work.")
    else:
        print("Detected Energy Dip: Prioritizing Administrative/Shallow Tasks.")
    print("==========================")

    for idx, task in enumerate(optimized_schedule, 1):
        print(f"{idx}. [{task.task_type.name}] {task.name} ({task.duration_minutes} min)")

if __name__ == "__main__":
    main()