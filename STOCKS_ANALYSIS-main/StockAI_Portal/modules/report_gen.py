"""
report_gen.py
-------------
Builds the detailed, point-by-point (no word-limit) summary report the
user asked for, personalized with their name / risk style / language,
and exports it to PDF, DOCX, CSV, and TXT.
"""

import csv
import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Image
from docx import Document
from docx.shared import Inches

from .translations import t, translate_text
from . import forecast as forecast_mod
from .search_links import SEARCH_SITES


def build_report_points(profile: dict, symbol: str, period: str, analysis: dict,
                         forecast: dict, call_zone: dict, rec: dict) -> list:
    """
    Returns an ordered list of (heading, [bullet strings]) tuples —
    this is the single source of truth used by the UI, PDF, DOCX and TXT
    exports, so every format shows exactly the same content.
    """
    lang = profile.get("language", "en")
    name = profile.get("name", "Investor")
    risk = profile.get("risk", "medium")
    style = profile.get("style", "long")

    points = []

    points.append((f"{t(lang,'welcome')}, {name}", [
        f"Asset studied: {symbol}",
        f"Time period analyzed: {period}",
        f"Data as of: {analysis['as_of']}",
        f"Your profile: risk tolerance = {risk}, investing style = {style}",
    ]))

    points.append((t(lang, "trend"), [
        f"{analysis['trend']}",
        f"{t(lang,'current_price')}: {analysis['current_price']}",
    ]))

    points.append((t(lang, "support_levels"), [
        f"Support: {p['price']} on {p['date']}" for p in analysis["swing_minima"]
    ] or ["Not enough data to identify swing lows yet."]))

    points.append((t(lang, "resistance_levels"), [
        f"Resistance: {p['price']} on {p['date']}" for p in analysis["swing_maxima"]
    ] or ["Not enough data to identify swing highs yet."]))

    macd = analysis["macd"]
    points.append(("Momentum Indicators", [
        f"{t(lang,'rsi')}: {analysis['rsi']} "
        f"({'Oversold' if analysis['rsi']<30 else 'Overbought' if analysis['rsi']>70 else 'Neutral'})",
        f"{t(lang,'macd')}: MACD={macd['macd']}, Signal={macd['signal']}, Histogram={macd['histogram']}",
        f"Bullish crossover just occurred: {'Yes' if macd['bullish_cross'] else 'No'}",
        f"Bearish crossover just occurred: {'Yes' if macd['bearish_cross'] else 'No'}",
    ]))

    points.append((t(lang, "forecast"), [
        f"Model used: {forecast['method']}",
        f"Projected prices over next {forecast['horizon_steps']} periods: {forecast['projected_prices']}",
        f"Projected change: {forecast['projected_change_pct']}%",
    ]))

    points.append((t(lang, "next_entry"), [
        f"Nearest support / potential BUY zone: {call_zone['buy_zone_near']}",
        f"Nearest resistance / potential SELL zone: {call_zone['sell_zone_near']}",
        f"Approx. risk-reward ratio at current price: {call_zone['risk_reward_ratio']}",
    ]))

    # Worked BUY and SELL examples, using the amount the user told us
    # at sign-up they plan to invest (defaults to 1000 if not given).
    investment_amount = profile.get("investment_amount", 1000)
    currency = profile.get("currency", "INR")
    worked = forecast_mod.worked_examples(investment_amount, currency, analysis["current_price"], call_zone)

    points.append((t(lang, "buy_example_heading"), [worked["buy_example"]["narrative"]]))
    points.append((t(lang, "sell_example_heading"), [worked["sell_example"]["narrative"]]))

    points.append((t(lang, "recommendation"), [
        f"AI Call: {t(lang, rec['call'].lower()) if rec['call'].lower() in ('buy','sell','hold') else rec['call']}",
        f"Confidence score: {rec['score']} (rule-based, range roughly -4 to +4)",
        *[f"Reason: {r}" for r in rec["reasons"]],
    ]))

    # Personalized narrative based on the years-of-experience the user
    # gave us at sign-up, tying together the same call + buy/sell zone.
    years_experience = profile.get("years_experience", "intermediate")
    highlight = forecast_mod.experience_highlight(rec, call_zone, years_experience)
    points.append((t(lang, "experience_highlight_heading"), [highlight]))

    action_steps = _action_steps(rec["call"], style, risk)
    points.append((t(lang, "action_steps"), action_steps))

    links_bullets = [f"{s['name']} ({s['for']}): {s['search_url'].replace('%s', '')}" for s in SEARCH_SITES]
    points.append(("Useful Official Links for Further Research", links_bullets))

    points.append(("Disclaimer", [t(lang, "disclaimer")]))

    # English & Hindi bullets above are already written in the right
    # language. For every other world language, machine-translate each
    # bullet on the fly (headings are already localized via t()).
    if lang not in ("en", "hi"):
        points = [(heading, [translate_text(b, lang) for b in bullets]) for heading, bullets in points]

    return points


def _action_steps(call: str, style: str, risk: str) -> list:
    steps = []
    if call == "BUY":
        steps.append("Consider scaling in near the identified support zone rather than all at once.")
        steps.append("Set a stop-loss just below the nearest support to manage downside risk.")
        if style == "short":
            steps.append("As a short-term trader, plan to book partial profit near the resistance zone.")
        else:
            steps.append("As a long-term investor, review fundamentals (earnings, sector news) before committing full position size.")
    elif call == "SELL":
        steps.append("Consider trimming or exiting the position near the current resistance zone.")
        steps.append("Watch for a confirmed breakdown below the nearest support before adding new shorts.")
    else:
        steps.append("No strong edge either way right now — consider waiting for price to reach the buy or sell zone.")
        steps.append("Keep this symbol on your watchlist and re-run the analysis after the next few sessions.")

    if risk == "low":
        steps.append("Given your conservative profile, keep position size small and prioritize capital protection.")
    elif risk == "high":
        steps.append("Given your aggressive profile, you may size up but keep a strict stop-loss discipline.")

    steps.append("This report should be combined with your own research — it is educational, not financial advice.")
    return steps


# ---------------- Exporters ----------------

def to_txt(points: list, title: str) -> bytes:
    lines = [title, "=" * len(title), ""]
    for heading, bullets in points:
        lines.append(heading)
        lines.append("-" * len(heading))
        for b in bullets:
            lines.append(f"  • {b}")
        lines.append("")
    return "\n".join(lines).encode("utf-8")


def to_csv(points: list) -> bytes:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Section", "Point"])
    for heading, bullets in points:
        for b in bullets:
            writer.writerow([heading, b])
    return buf.getvalue().encode("utf-8")


def to_pdf(points: list, title: str, charts: dict = None) -> bytes:
    """charts: optional {label: png_bytes} — every chart type gets embedded,
    right after the text sections, so the PDF matches what's on screen."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    for heading, bullets in points:
        story.append(Paragraph(heading, styles["Heading2"]))
        items = [ListItem(Paragraph(b, styles["Normal"])) for b in bullets]
        story.append(ListFlowable(items, bulletType="bullet"))
        story.append(Spacer(1, 10))

    if charts:
        story.append(Paragraph("Charts", styles["Heading1"]))
        for label, png_bytes in charts.items():
            story.append(Paragraph(label, styles["Heading2"]))
            try:
                story.append(Image(io.BytesIO(png_bytes), width=430, height=240))
            except Exception:
                pass
            story.append(Spacer(1, 14))

    doc.build(story)
    return buf.getvalue()


def to_docx(points: list, title: str, charts: dict = None) -> bytes:
    """charts: optional {label: png_bytes} — every chart type gets embedded
    as an image at the end of the document, matching the on-screen report."""
    doc = Document()
    doc.add_heading(title, level=0)
    for heading, bullets in points:
        doc.add_heading(heading, level=2)
        for b in bullets:
            doc.add_paragraph(b, style="List Bullet")

    if charts:
        doc.add_heading("Charts", level=1)
        for label, png_bytes in charts.items():
            doc.add_heading(label, level=2)
            try:
                doc.add_picture(io.BytesIO(png_bytes), width=Inches(6))
            except Exception:
                pass

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def report_title(symbol: str, period: str) -> str:
    return f"AI Stock Study Report — {symbol} ({period}) — generated {datetime.now().strftime('%Y-%m-%d %H:%M')}"
