"""
StockAI Portal — app.py
========================
A single Flask app that is the "live portal" the user asked for:

  /                -> onboarding (name, language, risk, style, asset, symbol, period, uploads)
  /dashboard        -> quick re-entry point once a profile exists
  /analyze (POST)  -> runs the full pipeline and stores the result in session
  /report           -> shows the detailed point-wise report + download buttons
  /report/download/<fmt> -> pdf / docx / csv / txt export of the last report
  /daily            -> today's market scenario (major indices, live)

No API key is required anywhere — all live data comes from yfinance,
which is free and key-less.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import os
import uuid
import traceback

from flask import Flask, render_template, request, session, send_file, redirect, url_for, flash

from modules import data_fetch, analysis as analysis_mod, forecast as forecast_mod, report_gen
from modules.translations import t, TRANSLATIONS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "user_data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("STOCKAI_SECRET", "dev-secret-change-me")

# in-memory store of the last generated report per session id
# (kept simple on purpose - swap for a DB/Redis for multi-user production use)
REPORT_STORE = {}


def get_lang():
    profile = session.get("profile", {})
    return profile.get("language", "en")


@app.context_processor
def inject_globals():
    return {"t": t, "lang": get_lang(), "profile": session.get("profile", {})}


@app.route("/", methods=["GET", "POST"])
def onboarding():
    if request.method == "POST":
        profile = {
            "name": request.form.get("name", "Investor").strip() or "Investor",
            "language": request.form.get("language", "en"),
            "risk": request.form.get("risk", "medium"),
            "style": request.form.get("style", "long"),
            "asset_type": request.form.get("asset_type", "stock"),
        }
        session["profile"] = profile
        return redirect(url_for("dashboard"))

    return render_template("onboarding.html", languages=TRANSLATIONS.keys())


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "profile" not in session:
        return redirect(url_for("onboarding"))
    return render_template("dashboard.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "profile" not in session:
        return redirect(url_for("onboarding"))
    profile = session["profile"]

    symbol = request.form.get("symbol", "").strip()
    period = request.form.get("period", "1y")
    csv_file = request.files.get("csv_file")
    img_file = request.files.get("img_file")

    try:
        df = None

        # 1) Prefer live real-time data (no API key needed)
        if symbol:
            try:
                df = data_fetch.fetch_live_data(symbol, period=period)
            except Exception as live_err:
                flash(f"Live fetch failed ({live_err}). Trying uploaded file instead.")

        # 2) Fallback / override: user-uploaded CSV
        if df is None and csv_file and csv_file.filename:
            path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{csv_file.filename}")
            csv_file.save(path)
            df = data_fetch.load_uploaded_csv(path)
            symbol = symbol or csv_file.filename

        if df is None or df.empty:
            flash("No usable data: enter a valid symbol or upload a CSV of price history.")
            return redirect(url_for("dashboard"))

        # Optional: best-effort chart-photo trace (supporting signal only)
        chart_trace = None
        if img_file and img_file.filename:
            try:
                from modules import chart_image
                img_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{img_file.filename}")
                img_file.save(img_path)
                price_min = float(df["Close"].min())
                price_max = float(df["Close"].max())
                chart_trace = chart_image.trace_chart_line(img_path, price_min, price_max)
            except Exception:
                chart_trace = None  # best-effort only, never block the main report

        analysis = analysis_mod.full_analysis(df)
        forecast = forecast_mod.forecast_next_period(df)
        call_zone = forecast_mod.next_call_zone(
            analysis["current_price"], analysis["support_levels"], analysis["resistance_levels"]
        )
        rec = forecast_mod.recommendation(analysis, forecast, risk_tolerance=profile.get("risk", "medium"))

        points = report_gen.build_report_points(profile, symbol, period, analysis, forecast, call_zone, rec)
        title = report_gen.report_title(symbol, period)

        report_id = uuid.uuid4().hex
        REPORT_STORE[report_id] = {"points": points, "title": title}
        session["report_id"] = report_id
        session["last_symbol"] = symbol
        session["chart_trace_preview"] = chart_trace[:20] if chart_trace else None

        return redirect(url_for("report_view"))

    except Exception as e:
        traceback.print_exc()
        flash(f"Analysis failed: {e}")
        return redirect(url_for("dashboard"))


@app.route("/report")
def report_view():
    report_id = session.get("report_id")
    report = REPORT_STORE.get(report_id)
    if not report:
        flash("No report yet — run an analysis first.")
        return redirect(url_for("dashboard"))
    return render_template("report.html", points=report["points"], title=report["title"],
                            chart_trace=session.get("chart_trace_preview"))


@app.route("/report/download/<fmt>")
def download_report(fmt):
    report_id = session.get("report_id")
    report = REPORT_STORE.get(report_id)
    if not report:
        return redirect(url_for("dashboard"))

    points, title = report["points"], report["title"]
    filename = f"stockai_report_{session.get('last_symbol','asset')}.{fmt}"

    if fmt == "pdf":
        data = report_gen.to_pdf(points, title)
        mimetype = "application/pdf"
    elif fmt == "docx":
        data = report_gen.to_docx(points, title)
        mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif fmt == "csv":
        data = report_gen.to_csv(points)
        mimetype = "text/csv"
    elif fmt == "txt":
        data = report_gen.to_txt(points, title)
        mimetype = "text/plain"
    else:
        return "Unsupported format", 400

    import io
    return send_file(io.BytesIO(data), mimetype=mimetype, as_attachment=True, download_name=filename)


@app.route("/daily")
def daily():
    try:
        snapshot = data_fetch.fetch_daily_snapshot()
    except Exception:
        snapshot = {}
    return render_template("daily.html", snapshot=snapshot)


if __name__ == "__main__":
    app.run(debug=True)
