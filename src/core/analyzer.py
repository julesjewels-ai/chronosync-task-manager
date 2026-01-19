from typing import List, Tuple
from collections import defaultdict
from datetime import time
from .models import SleepData, EnergyLog, CircadianProfile

class SimpleCircadianAnalyzer:
    def analyze(self, sleep_data: List[SleepData], energy_logs: List[EnergyLog]) -> CircadianProfile:
        """
        Analyzes sleep data and energy logs to determine circadian peaks and dips.

        Heuristic:
        - Calculates average energy level per hour from logs.
        - > 7 is PEAK, <= 4 is DIP.
        - Returns time ranges.
        """
        # Group energy logs by hour
        energy_by_hour = defaultdict(list)
        for log in energy_logs:
            energy_by_hour[log.timestamp.hour].append(log.level)

        hourly_states = {}
        # Default assumption if no data: Peak 9-11 and 14-16?
        # For now, let's stick to data driven. If no data, Neutral.

        for h in range(24):
            levels = energy_by_hour.get(h, [])
            if not levels:
                hourly_states[h] = "NEUTRAL"
                continue

            avg_level = sum(levels) / len(levels)

            # Simple adjustment based on sleep quality
            # If recent sleep was bad, maybe we don't hit true peak?
            # For MVP, ignoring sleep data complexity, just focusing on energy logs
            # as direct ground truth of "how user feels".

            if avg_level >= 7:
                hourly_states[h] = "PEAK"
            elif avg_level <= 4:
                hourly_states[h] = "DIP"
            else:
                hourly_states[h] = "NEUTRAL"

        peaks = self._extract_ranges(hourly_states, "PEAK")
        dips = self._extract_ranges(hourly_states, "DIP")

        return CircadianProfile(peaks=peaks, dips=dips)

    def _extract_ranges(self, hourly_states: dict, target_state: str) -> List[Tuple[time, time]]:
        ranges = []
        start_hour = None

        # Iterate 0 to 23. Note: this doesn't handle wrapping around midnight for simplicity.
        for h in range(24):
            state = hourly_states.get(h, "NEUTRAL")
            if state == target_state:
                if start_hour is None:
                    start_hour = h
            else:
                if start_hour is not None:
                    # Range ended at h-1
                    ranges.append((time(start_hour, 0), time(h, 0))) # h, 0 is the start of the next hour, so it covers up to h:00
                    start_hour = None

        # Handle case where range goes until end of day (23:59:59 essentially, or just mark end as next day start if we were using datetimes, but here just max time)
        if start_hour is not None:
             ranges.append((time(start_hour, 0), time(23, 59))) # Close enough for MVP

        return ranges
