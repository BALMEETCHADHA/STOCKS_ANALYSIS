# StockAI Portal

A real-time, AI-assisted stock / crypto / forex study portal. Built on top
of the original LSTM/BiLSTM/ARIMA notebooks in this repo, wrapped in a
working web portal (Flask) with a real UI, personalization, multi-language
reports, and multi-format downloads.

**No API key is required anywhere.** Live prices come from `yfinance`,
which is free.

---

## What it does

1. **Onboarding** — collects your name, preferred language (**~80 world
   languages**, not just English/Hindi), risk tolerance, investing style,
   asset type, **how much you plan to invest (any amount + currency)**,
   and **years of investing experience**. All of this personalizes the
   final report — including two worked money examples and an
   experience-tailored paragraph (see below).
2. **Dashboard** —
   - Enter any symbol (stock, crypto, or forex).
   - Pick a **preset time period or a fully custom duration** — any
     number of days / weeks / months / years you want.
   - Upload price history as **CSV, PDF, or Word (.docx)** — not just
     CSV. The app extracts the Date/Close table from whichever format
     you give it.
   - Optionally upload a photo of a chart (best-effort visual trace —
     see limitation note below), or **paste a screenshot directly**
     with Ctrl+V/Cmd+V into the paste box, as another way in.
   - **Search Official Sites panel** — now sits **side-by-side with the
     form** (left: your inputs, right: search) so both fit on one
     screen. Type a company/coin/currency name and click through to
     Yahoo Finance, Google Finance, NSE/BSE India, CoinMarketCap,
     CoinGecko, XE, or Investing.com. Sites known to block a guessed
     direct query (NSE, BSE, CoinMarketCap, CoinGecko, Google Finance)
     are routed through a Google site-restricted search instead, so
     every button reliably opens something useful.
3. **Live time-series study** —
   - Fetches real OHLCV history via `yfinance` (no key needed).
   - Finds the **last 10 swing highs and 10 swing lows** (local maxima/
     minima) and turns them into support/resistance levels.
   - Computes RSI and MACD momentum indicators.
   - Produces a short-horizon forecast (ARIMA, falling back to a linear
     trend projection if ARIMA can't fit).
   - Combines all of the above into a transparent, rule-based
     **BUY / SELL / HOLD** call, plus the **next suggested entry
     ("call") zone** — buy near support, watch the resistance zone.
   - **Worked BUY and SELL examples** — both directions, always shown,
     using the exact amount and currency you gave at sign-up (e.g. "with
     ₹1000 near the support zone, you'd get ~X units; at the resistance
     zone that's worth ~₹Y, a gain of ~Z%").
4. **10 chart types**, viewable on screen (pick from a dropdown) and
   **all embedded as images in the PDF/DOCX downloads**: line with
   entry/exit points highlighted, moving averages, support/resistance
   zones, candlestick/OHLC, volume bar, up/down-days pie, daily-return
   scatter (dot), price area, cumulative-return area, and a return
   histogram.
5. **Detailed report** — a point-by-point (no word limit) summary:
   trend, support/resistance, momentum, forecast, next entry zone, the
   worked buy/sell examples, an **experience-level-specific
   highlight** (beginner / intermediate / experienced get different
   guidance built from the same call and zones), recommendation with
   reasons, concrete next steps, and a list of the official research
   links. Shown in your chosen language.
6. **Downloads** — the exact same report, with charts, as **PDF, Word
   (DOCX)**, plus **CSV and TXT** (text-only, since those formats can't
   hold images).
7. **Daily Market Scenario** — a live snapshot of major indices (NIFTY
   50, SENSEX, S&P 500, NASDAQ, Bitcoin, USD/INR), each **tile clickable
   through to a live Google Finance search** for that index, plus a
   "for further live study" section linking out to the same official
   sites, with a disclaimer to treat this as a starting point, not the
   full picture.
8. **Live link on the report** — right under the report title, a "View
   SYMBOL LIVE on Yahoo Finance" link opens that exact symbol's live
   quote page.
9. **Dark/light theme toggle** — 🌙/☀️ icon top-right of every page,
   defaults to dark, remembers your choice.

---

## Project structure

```
StockAI_Portal/
├── app.py                  # Flask routes / the "portal"
├── requirements.txt
├── modules/
│   ├── data_fetch.py        # live yfinance fetch (preset + custom duration) + daily snapshot
│   ├── file_loaders.py      # CSV / PDF / Word (.docx) price-history upload parsing
│   ├── analysis.py          # swing highs/lows, support/resistance, RSI, MACD, trend
│   ├── forecast.py          # ARIMA/linear forecast, BUY/SELL/HOLD engine, worked buy/sell examples, experience highlight
│   ├── charts.py            # generates all 10 chart types (matplotlib, PNG bytes)
│   ├── chart_image.py       # optional best-effort chart-photo tracing
│   ├── search_links.py      # official site links + first-time-user search steps
│   ├── translations.py      # English / Hindi phrase dictionary + dynamic-text translation
│   └── lang_support.py      # ~80-language list + free machine translation fallback
├── templates/                # onboarding, dashboard, report, daily pages
└── static/                   # css + js (custom-duration toggle, chart selector, site search buttons)
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

- **Language coverage is honest, not overclaimed.** The onboarding
  dropdown offers ~80 major world languages/scripts. English and Hindi
  report text is hand-written for accuracy. Every other language is
  machine-translated at request time via the free `deep-translator`
  (Google Translate) library — this needs internet, and if a
  translation call fails (offline, rate-limited), the app quietly
  falls back to English rather than breaking the report.
- **PDF/Word price-history upload is best-effort.** It looks for a
  table (or, in PDFs without a real table, date/price-shaped lines of
  text) containing "Date" and "Close" columns. Clean, simple tables
  work well; complex multi-column financial statements may not parse —
  CSV upload remains the most reliable fallback.
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
Colab (File -> Upload notebook), then:
1. Run the install cell.
2. Run the upload cell — a file picker pops up. Choose your project zip
   directly (no GitHub needed at all for this).
3. Run the ngrok cell — it will prompt you to paste your free authtoken
   (get one at https://dashboard.ngrok.com/get-started/your-authtoken).
4. Run the last cell — it prints a clickable public URL running the
   real app.

(An alternate GitHub-clone cell is included as a markdown snippet if
you'd rather clone an already-pushed, already-extracted repo instead.)

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
