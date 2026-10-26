import json
from datetime import date
from pathlib import Path
import os
import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_service import generate_plan, refine_plan
from src.budget import normalize_budget, budget_summary
from src.exports import plan_to_csv, plan_to_pdf
from src.timeline import build_timeline
from src.validators import validate_event

APP_DIR = Path(__file__).parent
SAVED_DIR = APP_DIR / "data" / "saved_plans"
SAVED_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="EventWise AI", page_icon="✨", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.hero {padding:2rem 2.2rem;border-radius:24px;background:linear-gradient(120deg,#211b3d,#584a86 62%,#a27c9c);color:white;margin-bottom:1.2rem}
.hero h1 {font-family:'Playfair Display',serif;font-size:2.65rem;line-height:1.1;margin:0 0 .55rem 0}
.hero p {font-size:1.05rem;opacity:.92;max-width:760px}
.eyebrow {text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;font-weight:700;opacity:.8}
.metric-card {padding:1rem 1.1rem;border:1px solid #e7e3ef;border-radius:16px;background:#fff}
.small-muted {color:#777187;font-size:.88rem}
div[data-testid="stMetric"] {background:#fff;border:1px solid #e7e3ef;padding:14px 16px;border-radius:14px}
.stButton button {border-radius:12px;font-weight:600}
</style>
""", unsafe_allow_html=True)

if "plan" not in st.session_state:
    st.session_state.plan = None
if "event" not in st.session_state:
    st.session_state.event = None

def demo_event():
    return {
        "event_type": "Wedding", "event_name": "Meera & Aarav's Reception",
        "event_date": (date.today().replace(day=1)).isoformat(),
        "location": "Nagpur, Maharashtra", "guest_count": 250, "budget": 800000,
        "currency": "INR", "theme": "Warm traditional Indian elegance",
        "colors": "ivory, marigold, sage green", "venue_type": "Indoor / covered",
        "food_preferences": "Vegetarian", "accessibility": "Seating for elderly guests; step-free access",
        "special_requirements": "Floral stage, photography, family-friendly schedule"
    }

def format_money(value, currency):
    if currency == "INR":
        return f"₹{value:,.0f}"
    return f"{currency} {value:,.2f}"

st.markdown("""
<div class="hero">
  <div class="eyebrow">Your personal AI event co-planner</div>
  <h1>Make room for the moments<br>that matter.</h1>
  <p>Turn an idea, a guest list, and a budget into a thoughtful event plan—with practical costs, a preparation timeline, vendor tasks, and creative ideas.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ✨ EventWise AI")
    page = st.radio("Workspace", ["Create a plan", "Plan dashboard", "Creative studio", "Save / open"])
    st.divider()
    st.caption("AI mode")
    if os.getenv("GEMINI_API_KEY"):
        st.success("Gemini API key detected")
    else:
        st.info("Demo mode is available. Add GEMINI_API_KEY for live generation.")
    st.caption("Estimates are planning guidance, not vendor quotes.")

if page == "Create a plan":
    st.subheader("Tell us what you're planning")
    st.write("Start with a few details. You can refine the generated plan afterwards.")
    if st.button("Load sample wedding", type="secondary"):
        st.session_state.event = demo_event()
        st.rerun()
    current = st.session_state.event or {}
    with st.form("event_form"):
        natural = st.text_area("Describe your event in your own words", placeholder="Plan a cozy 40th birthday for 60 guests, with a garden theme and a budget of ₹1.5 lakh…", height=90)
        c1, c2, c3 = st.columns(3)
        event_type = c1.selectbox("Event type", ["Wedding", "Birthday", "Community Event"], index=["Wedding","Birthday","Community Event"].index(current.get("event_type","Wedding")))
        event_name = c2.text_input("Event name", value=current.get("event_name","My special event"))
        location = c3.text_input("Location", value=current.get("location",""))
        c4, c5, c6 = st.columns(3)
        event_date = c4.date_input("Event date", value=date.fromisoformat(current["event_date"]) if current.get("event_date") else date.today())
        guest_count = c5.number_input("Expected guests", min_value=1, max_value=100000, value=int(current.get("guest_count",50)), step=5)
        budget = c6.number_input("Total budget", min_value=0, value=int(current.get("budget",50000)), step=5000)
        c7, c8, c9 = st.columns(3)
        currency = c7.selectbox("Currency", ["INR", "USD", "GBP", "EUR"])
        theme = c8.text_input("Theme / atmosphere", value=current.get("theme",""))
        colors = c9.text_input("Preferred colors", value=current.get("colors",""))
        c10, c11 = st.columns(2)
        venue_type = c10.selectbox("Venue preference", ["Indoor / covered", "Outdoor", "Flexible"])
        food_preferences = c11.text_input("Food / dietary preferences", value=current.get("food_preferences",""))
        accessibility = st.text_input("Accessibility needs", value=current.get("accessibility",""))
        special_requirements = st.text_area("Special requirements", value=current.get("special_requirements",""), height=70)
        submitted = st.form_submit_button("✨ Generate my event plan", type="primary", use_container_width=True)

    if submitted:
        event = {
            "event_type": event_type, "event_name": event_name.strip() or "My event",
            "event_date": event_date.isoformat(), "location": location.strip(),
            "guest_count": int(guest_count), "budget": float(budget), "currency": currency,
            "theme": theme.strip(), "colors": colors.strip(), "venue_type": venue_type,
            "food_preferences": food_preferences.strip(), "accessibility": accessibility.strip(),
            "special_requirements": special_requirements.strip(), "natural_language": natural.strip()
        }
        errors = validate_event(event)
        if errors:
            for error in errors:
                st.error(error)
        else:
            with st.spinner("Putting your plan together…"):
                try:
                    plan, mode = generate_plan(event)
                    plan["budget"] = normalize_budget(plan.get("budget", []), event["budget"])
                    plan["timeline"] = build_timeline(event["event_date"], plan.get("timeline", []))
                    plan["_mode"] = mode
                    st.session_state.event = event
                    st.session_state.plan = plan
                    st.success(f"Plan created using {mode}.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not generate a plan: {exc}")

elif page == "Plan dashboard":
    plan = st.session_state.plan
    event = st.session_state.event
    if not plan or not event:
        st.info("Create a plan first, or load the sample wedding from the Create a plan page.")
    else:
        st.subheader(event["event_name"])
        st.caption(f'{event["event_type"]} · {event["event_date"]} · {event.get("location") or "Location not set"} · {event["guest_count"]} guests')
        if plan.get("_mode") == "Demo mode":
            st.info("Demo mode: this plan uses transparent rule-based sample content, not a live AI response.")
        summary = budget_summary(plan["budget"], event["budget"])
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Planned budget", format_money(event["budget"],event["currency"]))
        m2.metric("Allocated", format_money(summary["allocated"],event["currency"]))
        m3.metric("Remaining", format_money(summary["remaining"],event["currency"]))
        m4.metric("Vendor tasks", f'{sum(1 for x in plan.get("vendors",[]) if x.get("status")=="Booked")}/{len(plan.get("vendors",[]))} booked')
        tab1, tab2, tab3, tab4 = st.tabs(["Overview & budget", "Timeline", "Vendor checklist", "Export"])
        with tab1:
            st.markdown("### The concept")
            st.write(plan.get("overview",""))
            st.markdown("### Why this fits")
            st.write(plan.get("fit_rationale",""))
            st.markdown("### Budget planner")
            budget_df = pd.DataFrame(plan["budget"])
            if not budget_df.empty:
                budget_df["amount"] = pd.to_numeric(budget_df["amount"], errors="coerce").fillna(0)
                edited = st.data_editor(budget_df, use_container_width=True, hide_index=True,
                    column_config={"amount": st.column_config.NumberColumn("Estimated amount", min_value=0, step=500, format="%.0f")},
                    disabled=["category","reason"], key="budget_editor")
                plan["budget"] = normalize_budget(edited.to_dict("records"), event["budget"])
                summary = budget_summary(plan["budget"], event["budget"])
                chart_df = pd.DataFrame(plan["budget"])
                left,right = st.columns([1,1])
                with left:
                    st.plotly_chart(px.pie(chart_df, values="amount", names="category", hole=.48, title="Budget allocation"), use_container_width=True)
                with right:
                    st.plotly_chart(px.bar(chart_df, x="category", y="amount", title="Estimated cost by category"), use_container_width=True)
                if summary["allocated"] > event["budget"]:
                    st.warning(f'Allocation exceeds budget by {format_money(summary["allocated"]-event["budget"],event["currency"])}. Adjust the amounts.')
                else:
                    st.success(f'Remaining unallocated: {format_money(summary["remaining"],event["currency"])}')
            st.markdown("### Practical recommendations")
            for item in plan.get("recommendations", []):
                st.markdown(f"- {item}")
            st.markdown("### Contingency plan")
            for item in plan.get("contingencies", []):
                st.markdown(f"- {item}")
        with tab2:
            st.markdown("### Preparation timeline")
            tl = pd.DataFrame(plan.get("timeline",[]))
            if not tl.empty:
                edited_tl = st.data_editor(tl, use_container_width=True, hide_index=True,
                    column_config={"status": st.column_config.SelectboxColumn("Status", options=["To do","In progress","Done"])},
                    key="timeline_editor")
                plan["timeline"] = edited_tl.to_dict("records")
                st.markdown("### Event-day schedule")
                for item in plan.get("event_day_schedule",[]):
                    st.markdown(f'**{item.get("time","")} — {item.get("activity","")}**  \n{item.get("notes","")}')
            else:
                st.caption("No timeline tasks generated.")
        with tab3:
            st.markdown("### Vendor command center")
            vendors = pd.DataFrame(plan.get("vendors",[]))
            if not vendors.empty:
                edited_vendors = st.data_editor(vendors, use_container_width=True, hide_index=True,
                    column_config={"status": st.column_config.SelectboxColumn("Status", options=["Not contacted","Shortlisted","Contacted","Booked","Done"])},
                    key="vendor_editor")
                plan["vendors"] = edited_vendors.to_dict("records")
                st.caption("Vendor suggestions are categories and selection criteria—not verified business listings or quotes.")
            st.markdown("### Booking checklist")
            for item in plan.get("vendor_tips",[]):
                st.markdown(f"- {item}")
        with tab4:
            st.markdown("### Take your plan with you")
            col1,col2 = st.columns(2)
            with col1:
                st.download_button("Download budget CSV", data=plan_to_csv(plan["budget"]), file_name="eventwise-budget.csv", mime="text/csv", use_container_width=True)
            with col2:
                try:
                    pdf_data = plan_to_pdf(event, plan)
                    st.download_button("Download full plan PDF", data=pdf_data, file_name="eventwise-plan.pdf", mime="application/pdf", use_container_width=True)
                except Exception as exc:
                    st.error(f"PDF export unavailable: {exc}")
            st.download_button("Download plan JSON", data=json.dumps({"event":event,"plan":plan}, indent=2, ensure_ascii=False), file_name="eventwise-plan.json", mime="application/json", use_container_width=True)

elif page == "Creative studio":
    st.subheader("Creative studio")
    if not st.session_state.event or not st.session_state.plan:
        st.info("Generate a plan first to personalize creative suggestions.")
    else:
        event, plan = st.session_state.event, st.session_state.plan
        st.write("Ask for a change. EventWise will try to preserve the plan while adapting the relevant parts.")
        request = st.text_area("Refinement request", placeholder="Reduce the budget by 15%, keep the floral theme, and add activities for children.")
        if st.button("Refine my plan", type="primary", disabled=not request.strip()):
            with st.spinner("Refining your plan…"):
                try:
                    updated, mode = refine_plan(event, plan, request)
                    updated["budget"] = normalize_budget(updated.get("budget", plan["budget"]), event["budget"])
                    updated["timeline"] = build_timeline(event["event_date"], updated.get("timeline", plan.get("timeline",[])))
                    updated["_mode"] = mode
                    st.session_state.plan = updated
                    st.success(f"Updated using {mode}. Review the dashboard to check all changes.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Refinement failed: {exc}")
        st.markdown("### Current creative ideas")
        for idea in plan.get("creative_ideas", []):
            st.markdown(f"**{idea.get('title','Idea')}**  \n{idea.get('description','')}  \n*Why it fits:* {idea.get('why_it_fits','')}")
        st.markdown("### Invitation message")
        st.write(plan.get("invitation_message",""))

elif page == "Save / open":
    st.subheader("Save or reopen a plan")
    plan, event = st.session_state.plan, st.session_state.event
    if plan and event:
        save_name = st.text_input("Save name", value=event.get("event_name","my-event"))
        safe_name = "".join(c.lower() if c.isalnum() else "-" for c in save_name).strip("-") or "event-plan"
        if st.button("Save current plan", type="primary"):
            path = SAVED_DIR / f"{safe_name}.json"
            path.write_text(json.dumps({"event":event,"plan":plan},ensure_ascii=False,indent=2), encoding="utf-8")
            st.success(f"Saved locally as {path.name}")
    saved = sorted(SAVED_DIR.glob("*.json"))
    if saved:
        selected = st.selectbox("Saved plans", saved, format_func=lambda p:p.name)
        if st.button("Open selected plan"):
            try:
                payload = json.loads(selected.read_text(encoding="utf-8"))
                st.session_state.event = payload["event"]
                st.session_state.plan = payload["plan"]
                st.success("Plan loaded.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not open plan: {exc}")
    else:
        st.caption("No saved plans yet. Saved plans are local to this installation.")
