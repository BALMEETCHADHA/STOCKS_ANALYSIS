"""
data_fetch.py
-------------
Fetches real-time / historical price data.
Uses yfinance, which is FREE and needs NO API key.
Works for stocks (e.g. "TATAMOTORS.NS", "AAPL"), crypto (e.g. "BTC-USD"),
and forex (e.g. "EURUSD=X").

If live fetch fails (no internet, bad symbol, etc.) the caller can fall
back to a user-uploaded CSV via load_uploaded_csv().
"""

from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


PERIOD_MAP = {
    "1mo": "1mo",
    "3mo": "3mo",
    "6mo": "6mo",
    "1y": "1y",
    "2y": "2y",
    "5y": "5y",
    "max": "max",
}


def fetch_live_data(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Pulls OHLCV history for `symbol` over `period` at `interval`.
    Returns a DataFrame indexed by Date with columns:
    Open, High, Low, Close, Volume
    Raises ValueError if no data is returned (bad symbol / no internet).
    """
    symbol = symbol.strip().upper()
    period = PERIOD_MAP.get(period, "1y")

    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)

    if df is None or df.empty:
        raise ValueError(
            f"No live data found for '{symbol}'. Check the ticker format "
            f"(NSE stocks need '.NS', e.g. TATAMOTORS.NS; crypto like BTC-USD; "
            f"forex like EURUSD=X) or upload a CSV instead."
        )

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    df.index.name = "Date"
    return df


def custom_range_to_start_date(amount: int, unit: str) -> str:
    """
    Converts a user's custom duration ("5", "weeks") into a start date
    string for yfinance's start= parameter.
    """
    amount = max(int(amount), 1)
    unit = unit.lower()
    if unit.startswith("day"):
        delta = timedelta(days=amount)
    elif unit.startswith("week"):
        delta = timedelta(weeks=amount)
    elif unit.startswith("month"):
        delta = timedelta(days=amount * 30)
    elif unit.startswith("year"):
        delta = timedelta(days=amount * 365)
    else:
        delta = timedelta(days=amount)
    start = datetime.now() - delta
    return start.strftime("%Y-%m-%d")


def fetch_live_data_custom(symbol: str, amount: int, unit: str, interval: str = "1d") -> pd.DataFrame:
    """
    Same as fetch_live_data, but for a user-defined custom duration
    (e.g. "45 days", "6 weeks", "18 months", "3 years") instead of one
    of the preset periods.
    """
    symbol = symbol.strip().upper()
    start_date = custom_range_to_start_date(amount, unit)

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, interval=interval)

    if df is None or df.empty:
        raise ValueError(
            f"No live data found for '{symbol}' over the last {amount} {unit}. "
            f"Check the ticker format or try a preset period instead."
        )

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    df.index.name = "Date"
    return df


def fetch_daily_snapshot() -> dict:
    """
    Pulls a quick daily snapshot of major indices/assets for the
    'Daily Market Scenario' page. No API key needed.
    """
    watch = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Bitcoin": "BTC-USD",
        "USD/INR": "INR=X",
    }
    snapshot = {}
    for name, sym in watch.items():
        try:
            hist = yf.Ticker(sym).history(period="5d", interval="1d")
            if hist.empty or len(hist) < 2:
                continue
            last = hist["Close"].iloc[-1]
            prev = hist["Close"].iloc[-2]
            change_pct = ((last - prev) / prev) * 100
            snapshot[name] = {
                "price": round(float(last), 2),
                "change_pct": round(float(change_pct), 2),
            }
        except Exception:
            continue
    return snapshot


def load_uploaded_csv(filepath: str) -> pd.DataFrame:
    """
    Loads a user-uploaded CSV of historical prices.
    Expects at minimum a Date column and a Close column
    (Open/High/Low/Volume optional -> filled with Close/0 if missing).
    """
    df = pd.read_csv(filepath)
    df.columns = [c.strip().capitalize() for c in df.columns]

    if "Date" not in df.columns:
        raise ValueError("CSV must contain a 'Date' column.")
    if "Close" not in df.columns:
        raise ValueError("CSV must contain a 'Close' column.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).set_index("Date").sort_index()

    for col in ["Open", "High", "Low"]:
        if col not in df.columns:
            df[col] = df["Close"]
    if "Volume" not in df.columns:
        df["Volume"] = 0

    return df[["Open", "High", "Low", "Close", "Volume"]]
