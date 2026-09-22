# STOCKS_ANALYSIS — StockAI Portal

An end-to-end, real-time AI-assisted financial market study portal for stocks, cryptocurrencies, and forex — combining live market data, deep learning (LSTM/BiLSTM) and statistical (ARIMA) forecasting, swing-point technical analysis, and a personalized, multi-language reporting engine, all wrapped in a working Flask web app.

---

## Live Demo

**[Stock AI Portal — Live Dashboard](https://stocks-analysis-ib28.onrender.com)**

No sign-up, no API key needed — just open the link and use it.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technologies Used](#technologies-used)
4. [Data Source](#data-source)
5. [Model Architecture](#model-architecture)
6. [Repository Structure](#repository-structure)
7. [How to Run the Project](#how-to-run-the-project)
8. [Run & Test on Google Colab](#run--test-on-google-colab)
9. [Symbol Formats](#symbol-formats)
10. [Limitations & Honest Notes](#limitations--honest-notes)
11. [Results](#results)
12. [Disclaimer](#disclaimer)
13. [License](#license)

---

## Project Overview

**STOCKS_ANALYSIS** started as a set of LSTM/BiLSTM/ARIMA notebooks for forecasting stock prices (Tata Motors, Google) and has grown into **StockAI Portal** — a full web application that lets anyone:

- pick a stock, cryptocurrency, or currency pair,
- study its recent swing highs/lows, momentum, and trend,
- get a transparent, rule-based BUY/SELL/HOLD call with a concrete "next entry zone,"
- see it personalized to their own investment amount, risk tolerance, and experience level,
- and download the full report — charts included — as PDF, Word, CSV, or TXT.

It connects live market feeds from Yahoo Finance (`yfinance`, free, no key) with the project's trained time-series models and packages everything into a clean, responsive Flask web application.

---

## Key Features

- **Live Market Data Integration** — real-time OHLCV data via `yfinance` for stocks, crypto, and forex, with **no API key required anywhere**.
- **Flexible Time Periods** — preset ranges (1 month to Max) or a **fully custom duration** in any number of days/weeks/months/years.
- **Multi-Format Data Upload** — bring your own price history as **CSV, PDF, or Word (.docx)**, or **paste a chart screenshot directly** (Ctrl+V) as an alternative to a file picker.
- **Swing-Point Technical Analysis** — automatically finds the last 10 swing highs and 10 swing lows, derives support/resistance zones, and computes RSI and MACD.
- **Deep Learning & Statistical Forecasting** — LSTM/BiLSTM neural networks (see the research notebooks) and ARIMA time-series forecasting, with an automatic linear-trend fallback when ARIMA can't converge.
- **Explainable BUY/SELL/HOLD Engine** — a transparent, rule-based recommendation (not a black box) with a stated reason for every point, plus a concrete **next entry ("call") zone**.
- **Worked Buy & Sell Examples** — using the investment amount and currency you provide at sign-up, the report shows real worked numbers for both a buy and a sell scenario.
- **Experience-Tailored Guidance** — beginner / intermediate / experienced users each get differently-worded guidance built from the same underlying call and zones.
- **10 Chart Types** — line with entry/exit highlighted, candlestick/OHLC, moving averages, support/resistance, volume bar, pie, scatter, area, cumulative return, and return histogram — viewable on screen and embedded directly into the PDF/DOCX downloads.
- **~80-Language Support** — hand-written English/Hindi report phrasing, with automatic machine translation (via `deep-translator`) for every other language, falling back to English if a translation call fails.
- **Search Official Sites Panel** — look up the exact ticker for any company, coin, or currency via one-click links to Yahoo Finance, Google Finance, NSE/BSE India, CoinMarketCap, CoinGecko, XE, and Investing.com.
- **Live Reference Links** — a direct "View live on Yahoo Finance" link for the analyzed symbol, and clickable Daily Market tiles linking to live Google Finance data.
- **Daily Market Scenario** — a live snapshot of major indices (NIFTY 50, SENSEX, S&P 500, NASDAQ, Bitcoin, USD/INR).
- **Dark/Light Theme Toggle** — defaults to dark, remembered across visits.
- **Multi-Format Report Export** — the full personalized report, with charts, as **PDF, Word (DOCX), CSV, or TXT**.

---

## Technologies Used

- **Python**, **Flask**, **Gunicorn** (production server)
- **NumPy**, **Pandas**, **SciPy**, **Statsmodels** (ARIMA)
- **TensorFlow / Keras**, **Scikit-Learn** (LSTM / BiLSTM notebooks)
- **yfinance** (live market data, no API key)
- **Matplotlib**, **mplfinance** (chart generation)
- **OpenCV** (best-effort chart-photo tracing)
- **ReportLab**, **python-docx**, **pdfplumber** (multi-format report export & upload parsing)
- **deep-translator** (multi-language report translation)
- **pyngrok** (Colab live-link testing)

---

## Data Source

Historical and live data for stocks, crypto, and forex all come from **Yahoo Finance** via `yfinance` — free, and no API key needed. The original LSTM research notebooks were trained on Tata Motors data spanning **January 1, 2010 to November 28, 2024**; the live portal fetches fresh data on demand for whatever symbol and period you choose.

---

## Model Architecture

The LSTM research model (see `BiLSTM_Stock_Model.ipynb`) consists of:

- 4 LSTM layers with varying units (50, 60, 80, 120)
- Dropout layers for regularization (0.2, 0.3, 0.4, 0.5)
- 1 Dense layer for output

### Model Summary

```
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
lstm (LSTM)                  (None, 100, 50)           10400     
_________________________________________________________________
dropout (Dropout)            (None, 100, 50)           0         
_________________________________________________________________
lstm_1 (LSTM)                (None, 100, 60)           26640     
_________________________________________________________________
dropout_1 (Dropout)          (None, 100, 60)           0         
_________________________________________________________________
lstm_2 (LSTM)                (None, 100, 80)           45120     
_________________________________________________________________
dropout_2 (Dropout)          (None, 100, 80)           0         
_________________________________________________________________
lstm_3 (LSTM)                (None, 120)               96480     
_________________________________________________________________
dropout_3 (Dropout)          (None, 120)               0         
_________________________________________________________________
dense (Dense)                (None, 1)                 121       
=================================================================
Total params: 178,761
Trainable params: 178,761
Non-trainable params: 0
_________________________________________________________________
```

The live portal's forecast step currently uses ARIMA (falling back to a linear trend projection) so it works instantly for *any* symbol without a pre-trained model per stock — `forecast.py` can be extended to load a saved LSTM/BiLSTM model from these notebooks in place of, or alongside, ARIMA.

---

## Repository Structure

```text
STOCKS_ANALYSIS/
├── StockAI_Portal/                        # Main Flask web application
│   ├── app.py                             # Application entry point & web routes
│   ├── requirements.txt                   # Production dependency list
│   ├── Procfile                           # Render/Railway/Heroku-style deploy config
│   ├── Run_StockAI_Portal_On_Colab.ipynb  # One-click Colab runner (upload zip, get a live link)
│   ├── modules/
│   │   ├── data_fetch.py                  # live yfinance fetch (preset + custom duration) + daily snapshot
│   │   ├── file_loaders.py                # CSV / PDF / Word (.docx) price-history upload parsing
│   │   ├── analysis.py                    # swing highs/lows, support/resistance, RSI, MACD, trend
│   │   ├── forecast.py                    # ARIMA/linear forecast, BUY/SELL/HOLD engine, worked buy/sell examples
│   │   ├── charts.py                      # generates all 10 chart types (matplotlib)
│   │   ├── chart_image.py                 # best-effort chart-photo tracing
│   │   ├── search_links.py                # official site links + first-time-user search steps
│   │   ├── translations.py                # English/Hindi phrasing + dynamic-text translation
│   │   ├── lang_support.py                # ~80-language list + machine translation fallback
│   │   └── report_gen.py                  # builds the point-wise report + PDF/DOCX/CSV/TXT export
│   ├── templates/                         # onboarding, dashboard, report, daily pages
│   └── static/                            # CSS + JS (theme toggle, chart selector, paste-screenshot, search buttons)
├── ARIMA.ipynb                            # ARIMA model notebook
├── BiLSTM_Stock_Model.ipynb               # BiLSTM architecture experiment
├── TATAMOTORS_Model_Comparison.ipynb      # Tata Motors model benchmark
├── GOOG_Model_Comparison.ipynb            # Google stock model benchmark
├── Time Series - Stock Price Forecast using ARIMA.ipynb
└── STOCK_MARKET.ipynb                     # Exploratory data analysis notebook
```

---

## How to Run the Project

### Prerequisites

```bash
cd StockAI_Portal
pip install -r requirements.txt
```

### Steps to Run Locally

```bash
git clone https://github.com/BALMEETCHADHA/STOCKS_ANALYSIS.git
cd STOCKS_ANALYSIS/StockAI_Portal
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

### Deploy Your Own Live Link (Render)

1. Push this repo to GitHub as real files (not a zipped folder — GitHub can browse folders/files, not the inside of a `.zip`).
2. Go to [render.com](https://render.com) → New → Web Service → connect this repo.
3. Root Directory: `StockAI_Portal`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app` (auto-detected from the included `Procfile`)
6. Deploy — Render gives you a permanent `https://your-app.onrender.com` link.

(Railway, PythonAnywhere, and Fly.io work the same way if you prefer one of those instead of Render.)

---

## Run & Test on Google Colab

This repo includes **`Run_StockAI_Portal_On_Colab.ipynb`** for quick, no-setup testing:

1. Open it in Colab.
2. Run the install cell.
3. Run the upload cell — pick your project zip when the file picker appears (no GitHub step needed for this).
4. Run the ngrok cell — paste your free authtoken when prompted ([get one here](https://dashboard.ngrok.com/get-started/your-authtoken)).
5. Run the last cell — it prints a clickable public URL running the real app.

This link is temporary (only while the Colab cell is running) — use the Render deployment above for a permanent link.

---

## Symbol Formats

All free via `yfinance` — no API key needed for any of these:

| Asset | Format | Example |
|---|---|---|
| Indian stocks (NSE) | `SYMBOL.NS` | `TATAMOTORS.NS` |
| US stocks | `SYMBOL` | `AAPL` |
| Cryptocurrency | `TICKER-USD` | `BTC-USD` |
| Forex / currency pairs | `BASEQUOTE=X` | `EURINR=X`, `EURUSD=X` |

Use the **Search Official Sites** panel on the dashboard if you're unsure of the exact ticker for a company, coin, or currency — it links straight to Yahoo Finance, Google Finance, NSE/BSE India, CoinMarketCap, CoinGecko, XE, and Investing.com to help you confirm it.

---

## Limitations & Honest Notes

- **Language coverage** — the ~80-language dropdown covers major world languages, not literally every language on Earth. English/Hindi report text is hand-written; every other language is machine-translated at request time (needs internet) and falls back to English if translation fails.
- **PDF/Word upload parsing is best-effort** — it looks for a table (or date/price-shaped text) with Date and Close columns. Clean, simple tables work well; complex financial statements may not parse. CSV remains the most reliable upload format.
- **Chart-photo tracing is approximate** — it traces the plotted line's pixel path and rescales it to the actual fetched price range. It cannot recover exact OHLC values from a picture, so it's a supporting preview, not the primary numbers in the report.
- **All BUY/SELL/HOLD calls are rule-based and explainable, not financial advice.** Every point traces back to a specific indicator (trend, RSI, MACD, forecast) — see the Disclaimer below.

---

## Results

The model predicts future `Close` prices based on historical data. Below is a sample output visualization:

![Stock Price Prediction](assets/stock_price_prediction.png)

- **Blue Line**: Original Prices
- **Red Line**: Predicted Prices

The live portal additionally generates this as an interactive, annotated entry/exit chart plus 9 other chart views, on demand, for whatever symbol and period you choose — all embedded in the downloadable PDF/DOCX reports.

---

## Disclaimer

This project is for educational and research purposes only. All forecasts, technical calls, and recommendations are AI-generated and rule-based — they are **not financial advice**. Markets carry risk; always do your own research or consult a licensed financial advisor before investing.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
