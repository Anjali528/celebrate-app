from datetime import date

def validate_event(event):
    errors = []
    if not event.get("event_type"):
        errors.append("Choose an event type.")
    if not event.get("event_name", "").strip():
        errors.append("Enter an event name.")
    try:
        event_date = date.fromisoformat(str(event.get("event_date", "")))
        if event_date < date.today():
            errors.append("Choose today or a future date for the event.")
    except (ValueError, TypeError):
        errors.append("Enter a valid event date.")
    try:
        guests = int(event.get("guest_count", 0))
        if guests < 1:
            errors.append("Guest count must be at least 1.")
    except (ValueError, TypeError):
        errors.append("Guest count must be a whole number.")
    try:
        budget = float(event.get("budget", -1))
        if budget < 0:
            errors.append("Budget cannot be negative.")
    except (ValueError, TypeError):
        errors.append("Budget must be a valid number.")
    if not event.get("currency"):
        errors.append("Choose a currency.")
    return errors
