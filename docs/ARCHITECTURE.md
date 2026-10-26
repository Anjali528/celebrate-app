# Architecture

EventWise AI is a Streamlit application with a small Python service layer.

- `app.py`: UI, session state, editing, charts, and downloads.
- `src/ai_service.py`: Gemini integration, prompt contract, demo fallback, and refinement.
- `src/validators.py`: input validation.
- `src/budget.py`: budget normalization and calculations.
- `src/timeline.py`: date-aware milestone generation.
- `src/exports.py`: CSV and PDF generation.
- `tests/`: unit tests for core logic.

## Data flow
1. User enters event details.
2. `validators.py` checks inputs.
3. `ai_service.py` requests structured JSON from Gemini or supplies a clearly labeled demo plan.
4. Python normalizes the budget and derives timeline dates.
5. Streamlit renders editable tables and charts.
6. User can export a CSV, PDF, or JSON snapshot.

## Security and privacy
API keys are loaded from environment variables. Saved plans are stored locally under `data/saved_plans`; do not use this local persistence pattern for multi-user production hosting without adding authentication, access controls, and data-retention rules.
