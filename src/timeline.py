from datetime import date, timedelta

DEFAULT_TASKS = [
    (90, "Confirm event goals, guest estimate, and budget", "High"),
    (75, "Research venues and shortlist options", "High"),
    (60, "Book venue and priority vendors", "High"),
    (45, "Confirm theme, menu, and decoration direction", "Medium"),
    (30, "Send invitations and track responses", "High"),
    (21, "Confirm entertainment, rentals, and transport", "Medium"),
    (14, "Review guest count and dietary requirements", "High"),
    (7, "Confirm vendor arrival times and final details", "High"),
    (3, "Prepare signage, supplies, and emergency kit", "Medium"),
    (1, "Complete final walkthrough and contact check", "High"),
    (0, "Event day: coordinate setup and guest experience", "High"),
]

def build_timeline(event_date, supplied=None):
    target = date.fromisoformat(str(event_date))
    tasks = supplied or []
    if not tasks:
        tasks = [{"task": name, "days_before": days, "priority": priority, "status": "To do"}
                 for days, name, priority in DEFAULT_TASKS]
    result = []
    for item in tasks:
        try:
            days_before = int(item.get("days_before", 0))
        except (TypeError, ValueError):
            days_before = 0
        days_before = max(0, days_before)
        due = target - timedelta(days=days_before)
        if due < date.today():
            due = date.today()
        result.append({
            "date": due.isoformat(),
            "task": str(item.get("task", "Review event plan")),
            "priority": item.get("priority", "Medium") if item.get("priority") in ["High","Medium","Low"] else "Medium",
            "status": item.get("status", "To do") if item.get("status") in ["To do","In progress","Done"] else "To do",
        })
    result.sort(key=lambda x: x["date"])
    return result
