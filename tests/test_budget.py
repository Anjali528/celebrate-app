from src.budget import normalize_budget, budget_summary

def test_budget_summary_calculates_remaining():
    rows = [{"category":"Venue","amount":200,"reason":""},{"category":"Food","amount":300,"reason":""}]
    summary = budget_summary(rows, 1000)
    assert summary["allocated"] == 500
    assert summary["remaining"] == 500
    assert summary["over_budget"] is False

def test_budget_summary_flags_overrun():
    assert budget_summary([{"amount":120}], 100)["over_budget"] is True

def test_normalize_budget_clamps_negative_amount():
    rows = normalize_budget([{"category":"Test","amount":-4,"reason":"x"}], 100)
    assert rows[0]["amount"] == 0
