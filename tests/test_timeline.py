from datetime import date, timedelta
from src.timeline import build_timeline

def test_timeline_dates_not_before_today():
    target = (date.today() + timedelta(days=30)).isoformat()
    tasks = build_timeline(target)
    assert all(date.fromisoformat(row["date"]) >= date.today() for row in tasks)

def test_timeline_has_event_day_task():
    target = (date.today() + timedelta(days=20)).isoformat()
    tasks = build_timeline(target)
    assert any(row["date"] == target for row in tasks)
