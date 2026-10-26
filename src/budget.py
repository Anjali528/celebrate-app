DEFAULT_CATEGORIES = [
    ("Venue", 0.20, "Venue hire, utilities, and basic setup"),
    ("Food & catering", 0.30, "Meals, beverages, and service"),
    ("Decoration", 0.12, "Backdrop, flowers, lighting, and table styling"),
    ("Photography", 0.10, "Photography or video coverage"),
    ("Entertainment", 0.07, "Music, activities, or performers"),
    ("Invitations", 0.03, "Digital or printed invitations"),
    ("Transport & logistics", 0.05, "Guest movement and deliveries"),
    ("Miscellaneous", 0.05, "Small essentials and supplies"),
    ("Contingency reserve", 0.08, "Buffer for unexpected costs"),
]

def normalize_budget(items, total_budget):
    """Return budget rows with nonnegative numeric amounts and a consistent schema."""
    if not items:
        items = [{"category": n, "amount": total_budget * share, "reason": reason}
                 for n, share, reason in DEFAULT_CATEGORIES]
    clean = []
    for item in items:
        try:
            amount = max(0.0, float(item.get("amount", 0)))
        except (ValueError, TypeError):
            amount = 0.0
        clean.append({
            "category": str(item.get("category", "Other")),
            "amount": round(amount, 2),
            "reason": str(item.get("reason", "")),
        })
    if not clean:
        clean = [{"category": n, "amount": round(total_budget*share,2), "reason": reason}
                 for n, share, reason in DEFAULT_CATEGORIES]
    return clean

def budget_summary(items, total_budget):
    allocated = round(sum(float(item.get("amount", 0) or 0) for item in items), 2)
    total_budget = float(total_budget)
    return {
        "allocated": allocated,
        "remaining": round(total_budget - allocated, 2),
        "over_budget": allocated > total_budget,
        "percent_used": round((allocated / total_budget) * 100, 1) if total_budget else 0,
    }
