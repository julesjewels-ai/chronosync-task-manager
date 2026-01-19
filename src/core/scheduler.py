from typing import List
from datetime import datetime, timedelta, time
from .models import Task, TaskType, CircadianProfile, Schedule, ScheduleItem, EnergyState

class ChronoSyncScheduler:
    """
    Schedules tasks by matching task cognitive load to user's energy state.
    """

    def schedule(self, tasks: List[Task], profile: CircadianProfile, start_time: datetime) -> Schedule:
        """
        Generates a schedule starting from start_time.
        """
        # Sort tasks: Deep Work first? Or maybe sort by priority?
        # Strategy:
        # 1. Identify all available slots in the day and their energy state.
        # 2. Fill slots.

        # Simplification: We iterate through time in chunks (e.g. 15 mins) and assign tasks.

        current_time = start_time
        # Round up to next 15 min? Let's keep it simple.

        schedule_items = []
        remaining_tasks = sorted(tasks, key=lambda t: (t.priority, t.duration_minutes), reverse=True)
        # High priority first. If same priority, longer tasks first? Or maybe shorter?
        # Deep work usually is high cognitive load.

        # Separate Deep and Shallow tasks
        deep_tasks = [t for t in remaining_tasks if t.task_type == TaskType.DEEP_WORK]
        shallow_tasks = [t for t in remaining_tasks if t.task_type == TaskType.SHALLOW_WORK]

        # We process deep tasks first because they are harder to schedule (need Peak time).
        # Actually, a better greedy approach:
        # Iterate through the day, check energy state.
        # If Peak: try to schedule a Deep Task. If no Deep Task, schedule Shallow.
        # If Dip: try to schedule Shallow Task. If no Shallow, maybe rest? or schedule Deep if desperate?
        # (For now: Dip -> Shallow only. If only Deep left, maybe force it or leave empty?)
        # Let's say: Peak -> Deep > Shallow. Dip -> Shallow > Deep (suboptimal). Neutral -> Deep > Shallow.

        # But we need to fit the *whole* task.

        # Let's try to place tasks one by one into the earliest suitable slot.

        # But this is a bin packing problem essentially.

        # Let's do a time-simulation approach.
        # Queue of tasks.

        work_day_end = start_time.replace(hour=18, minute=0, second=0, microsecond=0) # Assume 6 PM end
        if current_time >= work_day_end:
             # Next day? For MVP, just schedule for today.
             pass

        while (deep_tasks or shallow_tasks) and current_time < work_day_end:
            state = self._get_energy_state(current_time.time(), profile)

            selected_task = None

            if state == EnergyState.PEAK:
                if deep_tasks:
                    selected_task = deep_tasks[0]
                    # Check if it fits? For MVP assume we can overflow peak slightly or just start it.
                    deep_tasks.pop(0)
                elif shallow_tasks:
                    selected_task = shallow_tasks[0]
                    shallow_tasks.pop(0)
            elif state == EnergyState.DIP:
                if shallow_tasks:
                    selected_task = shallow_tasks[0]
                    shallow_tasks.pop(0)
                else:
                    # Only deep tasks left.
                    # Option 1: Skip dip (take a break).
                    # Option 2: Do deep work anyway.
                    # Let's skip 30 mins for a break/recharge if only deep tasks are left in a dip?
                    # Or just schedule it. User requirements: "allocating... shallow work during energy dips".
                    # Doesn't explicitly say forbid deep work in dips, but implies it.
                    # Let's advance time if we can't schedule suitable work.
                    current_time += timedelta(minutes=30)
                    continue
            else: # NEUTRAL
                # Prefer Deep work?
                if deep_tasks:
                    selected_task = deep_tasks[0]
                    deep_tasks.pop(0)
                elif shallow_tasks:
                    selected_task = shallow_tasks[0]
                    shallow_tasks.pop(0)

            if selected_task:
                end_time = current_time + timedelta(minutes=selected_task.duration_minutes)
                if end_time > work_day_end:
                    # Truncate or don't schedule?
                    # Let's schedule it but warn? Or just stop.
                    # For MVP, let's stop scheduling if it doesn't fit.
                    # Or better, just fit it and end the loop.
                    schedule_items.append(ScheduleItem(selected_task, current_time, end_time))
                    current_time = end_time
                    break

                schedule_items.append(ScheduleItem(selected_task, current_time, end_time))
                current_time = end_time

        return Schedule(items=schedule_items)

    def _get_energy_state(self, t: time, profile: CircadianProfile) -> EnergyState:
        # Check peaks
        for start, end in profile.peaks:
            if self._is_between(t, start, end):
                return EnergyState.PEAK

        # Check dips
        for start, end in profile.dips:
             if self._is_between(t, start, end):
                return EnergyState.DIP

        return EnergyState.NEUTRAL

    def _is_between(self, t: time, start: time, end: time) -> bool:
        if start <= end:
            return start <= t < end
        else: # Crosses midnight
            return start <= t or t < end
