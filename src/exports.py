import csv
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def plan_to_csv(items):
    buffer = io.StringIO()
    fields = ["category","amount","reason"]
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(items)
    return buffer.getvalue().encode("utf-8-sig")

def plan_to_pdf(event, plan):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("EventWise AI — Event Plan", styles["Title"]),
        Spacer(1, 8),
        Paragraph(f"<b>{event.get('event_name','Event')}</b>", styles["Heading2"]),
        Paragraph(f"{event.get('event_type','')} · {event.get('event_date','')} · {event.get('location','')}", styles["BodyText"]),
        Paragraph(f"Guests: {event.get('guest_count','')} · Budget: {event.get('currency','')} {event.get('budget',0):,.0f}", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Event concept", styles["Heading2"]),
        Paragraph(str(plan.get("overview","")).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("Budget breakdown (estimates)", styles["Heading2"]),
    ]
    data = [["Category","Estimated amount","Reason"]]
    for row in plan.get("budget",[]):
        data.append([str(row.get("category","")), f'{float(row.get("amount",0)):,.2f}', str(row.get("reason",""))[:100]])
    table = Table(data, colWidths=[115,100,260], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#514477")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#ddd7e8")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("FONTSIZE",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),6),
    ]))
    story.extend([table, Spacer(1,12), Paragraph("Timeline", styles["Heading2"])])
    for task in plan.get("timeline",[]):
        story.append(Paragraph(f"• {task.get('date','')} — {task.get('task','')} ({task.get('priority','')}; {task.get('status','')})", styles["BodyText"]))
    story.extend([Spacer(1,8), Paragraph("Vendor checklist", styles["Heading2"])])
    for vendor in plan.get("vendors",[]):
        story.append(Paragraph(f"• {vendor.get('category','')}: {vendor.get('selection_criteria','')} — status: {vendor.get('status','Not contacted')}", styles["BodyText"]))
    story.extend([Spacer(1,8), Paragraph("Recommendations", styles["Heading2"])])
    for item in plan.get("recommendations",[]):
        story.append(Paragraph("• " + str(item).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), styles["BodyText"]))
    story.extend([Spacer(1,8), Paragraph("Planning note: costs are estimates, not verified vendor quotes. Verify local prices, taxes, availability, and contract terms.", styles["Italic"])])
    doc.build(story)
    return buffer.getvalue()
