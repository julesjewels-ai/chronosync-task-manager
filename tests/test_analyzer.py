import pytest
from datetime import datetime, time, timedelta
from src.core.models import SleepData, EnergyLog, Task, TaskType
from src.core.analyzer import SimpleCircadianAnalyzer

def test_analyzer_identifies_peak():
    analyzer = SimpleCircadianAnalyzer()
    logs = [
        EnergyLog(datetime(2023, 1, 1, 9, 30), 8),
        EnergyLog(datetime(2023, 1, 1, 10, 30), 9),
    ]
    profile = analyzer.analyze([], logs)

    # Expect 9-11 Peak (since 9:XX and 10:XX are high)
    # The analyzer logic groups by hour.
    # 9:30 -> hour 9 -> avg 8 -> Peak
    # 10:30 -> hour 10 -> avg 9 -> Peak
    # Range should be 9:00 to 11:00 (because 10:00-11:00 is hour 10)

    assert len(profile.peaks) == 1
    start, end = profile.peaks[0]
    assert start == time(9, 0)
    assert end == time(11, 0)

def test_analyzer_identifies_dip():
    analyzer = SimpleCircadianAnalyzer()
    logs = [
        EnergyLog(datetime(2023, 1, 1, 14, 15), 3),
        EnergyLog(datetime(2023, 1, 1, 15, 45), 2),
    ]
    profile = analyzer.analyze([], logs)

    assert len(profile.dips) == 1
    start, end = profile.dips[0]
    assert start == time(14, 0)
    assert end == time(16, 0)

def test_analyzer_mixed_data():
    analyzer = SimpleCircadianAnalyzer()
    logs = [
        EnergyLog(datetime(2023, 1, 1, 9, 0), 8),  # Peak
        EnergyLog(datetime(2023, 1, 1, 10, 0), 8), # Peak
        EnergyLog(datetime(2023, 1, 1, 12, 0), 5), # Neutral
        EnergyLog(datetime(2023, 1, 1, 14, 0), 3), # Dip
    ]
    profile = analyzer.analyze([], logs)

    assert len(profile.peaks) == 1
    assert profile.peaks[0] == (time(9, 0), time(11, 0))

    assert len(profile.dips) == 1
    assert profile.dips[0] == (time(14, 0), time(15, 0))
