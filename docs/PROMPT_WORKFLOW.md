# EventWise AI: Prompt Workflow

## Goal
Convert event requirements into a structured plan that can be validated, edited, and exported—not just a conversational response.

## Prompt design
The system prompt assigns the model a clear role, defines planning constraints, prohibits invented vendor verification, and specifies a JSON contract. Event details are passed separately as structured data.

## Initial prompt template
```text
You are EventWise AI, a careful and creative event-planning assistant.
Return valid JSON only. Costs are estimates. Do not invent verified vendors,
phone numbers, availability, or quotes. Respect the budget, guest count,
location, accessibility, and dietary requirements. No timeline task may be
dated after the event. Return the required schema for overview, budget,
timeline, vendors, creative ideas, recommendations, contingencies, schedule,
vendor tips, invitation message, and assumptions.
EVENT DETAILS: {validated_event_json}
Create the complete plan.
```

## Three example iterations
1. **Initial generation:** User asks for a vegetarian wedding reception for 250 guests in Nagpur with a ₹8 lakh budget. The model returns a theme, allocations, vendor categories, and milestones.
2. **Constraint refinement:** User asks to reduce the budget by 15%. The refinement prompt includes the existing plan and asks the model to revise affected allocations while preserving unrelated preferences. The app validates and normalizes numeric budget fields.
3. **Accessibility refinement:** User asks for seating and step-free routes for elderly guests. The model receives the existing plan and event constraints and returns a revised plan. The host should still confirm venue accessibility directly.

## Validation strategy
- Validate event date, guest count, budget, and currency before calling the model.
- Request JSON output and parse it as data, never execute generated code.
- Check required response keys.
- Normalize all budget amounts to nonnegative numbers.
- Derive timeline dates from the event date in Python.
- Clearly label estimates and demo-mode content.
- Keep a fallback plan available when no API key is configured.

## Known limitation
The current refinement path sends the full plan to Gemini, but in demo mode it adds a visible reminder instead of pretending to have intelligently recalculated every dependent field. Always review budget and task changes before acting on them.
