# EventWise AI ✨
**Your personal AI event co-planner** — plan weddings, birthdays, and community events with a budget, timeline, vendor checklist, and personalized ideas.

## Problem
Event planning often scatters costs, deadlines, vendor tasks, and creative decisions across messages and spreadsheets. EventWise AI brings those pieces into one editable plan.

## Features
- Natural-language event context and structured event form
- Gemini-powered generation with transparent demo fallback
- Editable budget allocations and Plotly charts
- Timeline milestones based on event date
- Vendor-category checklist and status tracking
- Creative ideas and plan refinement
- CSV, PDF, and JSON export
- Save and reopen plans locally
- Unit tests for budget, timeline, and validation

> Cost outputs are estimates, not vendor quotes. Vendor categories are planning suggestions, not verified businesses.

## Technology
Python, Streamlit, Google Gemini SDK (`google-genai`), Pandas, Plotly, ReportLab, Pytest.

## Quick start

### 1. Requirements
- Python 3.10 or newer
- Optional: a Gemini API key for live generation

### 2. Install
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Gemini (optional)
Copy `.env.example` to `.env`, then set `GEMINI_API_KEY`. The app reads environment variables; for local use you can export the variable in your terminal or use Streamlit secrets. Never commit `.env`.

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="your-key-here"
```

macOS/Linux:
```bash
export GEMINI_API_KEY="your-key-here"
```

If no key is configured, the application uses a clearly labeled demo mode.

### 4. Run
```bash
streamlit run app.py
```
Streamlit prints the local URL, usually `http://localhost:8501`.

## Example workflow
1. Open **Create a plan**.
2. Select **Load sample wedding**.
3. Generate a plan using the form.
4. Visit **Plan dashboard** to edit budget values, timeline tasks, and vendor status.
5. Use **Creative studio** to request a refinement.
6. Export the budget CSV, full PDF, or plan JSON.
7. Save the plan in **Save / open**.

## Tests
```bash
pytest -q
```

## Architecture
See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). Prompt strategy and example iterations are documented in [`docs/PROMPT_WORKFLOW.md`](docs/PROMPT_WORKFLOW.md).

## Screenshots
Add screenshots from your actual running app here before submission:
- `docs/screenshots/home.png`
- `docs/screenshots/dashboard.png`
- `docs/screenshots/budget.png`

Do not use mock screenshots as evidence of working functionality.

## Deployment
A simple deployment option is Streamlit Community Cloud:
1. Push this repository to GitHub.
2. Create a new app in Streamlit Community Cloud and select `app.py`.
3. Add `GEMINI_API_KEY` to the deployment's Secrets settings if live AI is desired.
4. Deploy and test the public URL.

Local JSON persistence may not be durable across hosted restarts and is not multi-user storage. Use a managed database and authentication for a production deployment.

## Limitations
- Vendor suggestions are categories and criteria, not live marketplace listings.
- Prices depend on location, date, taxes, and vendor packages; verify independently.
- Demo-mode refinements are reminders rather than full automatic replanning.
- Local plan files are intended for a local demo, not shared multi-user use.

## Future improvements
- Verified vendor search and availability integrations
- User accounts and cloud plan storage
- Calendar integrations and reminders
- Multi-language generation
- Automated budget change detection across dependent tasks

## License
MIT. See [`LICENSE`](LICENSE).

## Author
Anjali Desai
Email:anjalidesai9822@gmail.com
