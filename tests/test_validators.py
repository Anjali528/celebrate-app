from datetime import date, timedelta
from src.validators import validate_event

def valid_event():
    return {"event_type":"Birthday","event_name":"Test","event_date":(date.today()+timedelta(days=1)).isoformat(),
            "guest_count":20,"budget":1000,"currency":"INR"}

def test_valid_event_passes():
    assert validate_event(valid_event()) == []

def test_negative_budget_rejected():
    event = valid_event()
    event["budget"] = -1
    assert any("negative" in error.lower() for error in validate_event(event))
