# StockAI Portal

A real-time, AI-assisted stock / crypto / forex study portal. Built on top
of the original LSTM/BiLSTM/ARIMA notebooks in this repo, wrapped in a
working web portal (Flask) with a real UI, personalization, multi-language
reports, and multi-format downloads.

**No API key is required anywhere.** Live prices come from `yfinance`,
which is free.

---

## What it does

1. **Onboarding** — collects your name, preferred language (English /
   Hindi), risk tolerance, investing style (long-term / short-term /
   dividend), and asset type. This context is used to personalize the
   final report's tone and recommendations.
2. **Dashboard** — enter any symbol (stock, crypto, or forex) and a time
   period. Optionally upload a CSV of price history (fallback/override
   for when live data isn't available) and/or a photo of a chart
   (best-effort visual trace — see limitation note below).
3. **Live time-series study** —
   - Fetches real OHLCV history via `yfinance` (no key needed).
   - Finds the **last 10 swing highs and 10 swing lows** (local maxima/
     minima) and turns them into support/resistance levels.
   - Computes RSI and MACD momentum indicators.
   - Produces a short-horizon forecast (ARIMA, falling back to a linear
     trend projection if ARIMA can't fit).
   - Combines all of the above into a transparent, rule-based
     **BUY / SELL / HOLD** call, plus the **next suggested entry
     ("call") zone** — i.e., "buy near ₹X support, watch ₹Y resistance."
4. **Detailed report** — a point-by-point (no word limit) summary:
   trend, support/resistance, momentum, forecast, next entry zone,
   recommendation with reasons, and concrete next steps tailored to your
   risk profile and investing style. Shown in your chosen language.
5. **Downloads** — the exact same report as **PDF, Word (DOCX), CSV, and
   TXT**.
6. **Daily Market Scenario** — a live snapshot of major indices (NIFTY
   50, SENSEX, S&P 500, NASDAQ, Bitcoin, USD/INR) refreshed each visit.

---

## Project structure

```
StockAI_Portal/
├── app.py                  # Flask routes / the "portal"
├── requirements.txt
├── modules/
│   ├── data_fetch.py        # live yfinance fetch + CSV fallback + daily snapshot
│   ├── analysis.py          # swing highs/lows, support/resistance, RSI, MACD, trend
│   ├── forecast.py          # ARIMA/linear forecast + rule-based BUY/SELL/HOLD engine
│   ├── report_gen.py        # builds the point-wise report + PDF/DOCX/CSV/TXT export
│   ├── chart_image.py       # optional best-effort chart-photo tracing
│   └── translations.py      # English / Hindi phrase dictionary
├── templates/                # onboarding, dashboard, report, daily pages
└── static/css/style.css      # UI styling
```

---

## How to run

```bash
cd StockAI_Portal
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

### Symbol formats (all free via yfinance, no key)
- **Indian stocks (NSE):** `TATAMOTORS.NS`, `RELIANCE.NS`
- **US stocks:** `AAPL`, `TSLA`
- **Crypto:** `BTC-USD`, `ETH-USD`
- **Forex:** `EURUSD=X`, `INR=X`

---

## Notes & limitations

- **Chart-photo tracing is approximate.** It traces the plotted line's
  pixel path and rescales it using the price range of the *actual* data
  already fetched (or that you provide) — it cannot recover exact OHLC
  values from a picture, so it's shown only as a supporting preview, not
  the primary numbers in the report.
- **The forecast and BUY/SELL/HOLD call are educational**, rule-based,
  and explainable (every point in the report traces back to a specific
  indicator) — they are **not financial advice**. This is stated in the
  report itself.
- **ARIMA needs `statsmodels`.** If it isn't installed or fails to
  converge on a given symbol, the app automatically falls back to a
  linear trend projection so the report is never blocked.
- The report store is in-memory per Flask session for simplicity. For a
  multi-user production deployment, swap `REPORT_STORE` in `app.py` for
  a real database.

---

## Push this to GitHub

```bash
cd StockAI_Portal
git init
git add .
git commit -m "StockAI Portal - initial version"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```
(Create the empty repo first at github.com -> New repository, then copy its URL for the `git remote add` line above.)

## Test it live from Google Colab

This repo includes **`Run_StockAI_Portal_On_Colab.ipynb`**. Open it in
Colab (File -> Upload notebook, or push it to GitHub and use
`colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/StockAI_Portal/Run_StockAI_Portal_On_Colab.ipynb`),
then:
1. Update the `REPO_URL` variable to your GitHub repo URL.
2. Get a free ngrok authtoken at https://dashboard.ngrok.com/get-started/your-authtoken and paste it in the notebook.
3. Run all cells — the last cell prints a clickable public URL running the real app.

This link is temporary (only while the Colab cell keeps running) — it's for quick testing/demos, not 24/7 hosting.

## Get a permanent live link (no Colab needed)

GitHub itself can only host **static** sites (GitHub Pages) — it can't run a Flask backend that fetches live prices. Use a free web-service host connected to your GitHub repo instead, e.g. **Render**:
1. Push the project to GitHub (steps above).
2. Go to https://render.com -> New -> Web Service -> connect your GitHub repo.
3. Set **Root Directory** to `StockAI_Portal`.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app` (already included as `Procfile`, Render auto-detects it).
6. Deploy — Render gives you a permanent `https://your-app.onrender.com` link anyone can open and use.

(Railway, PythonAnywhere, and Fly.io work the same way if you prefer one of those instead of Render.)

## Original research (kept in this repo)

The original notebooks (`STOCK_MARKET.ipynb`, `BiLSTM_Stock_Model.ipynb`,
`ARIMA.ipynb`, `TATAMOTORS_Model_Comparison.ipynb`,
`GOOG_Model_Comparison.ipynb`) and research write-ups are untouched and
still here — the portal's `forecast.py` can be extended to load a saved
Keras LSTM/BiLSTM model from those notebooks instead of (or alongside)
the ARIMA/linear forecast, if you want to swap in your trained deep
model for the numeric forecast step.
