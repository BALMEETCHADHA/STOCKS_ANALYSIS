"""
analysis.py
-----------
Time-series study of the price history:
  - last 10 swing maxima and 10 swing minima (local turning points)
  - support / resistance zones derived from them
  - RSI (momentum) and MACD (trend momentum) indicators
  - a plain-English trend read

No look-ahead: everything here is computed only from data up to "today".
"""

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema


def find_swing_points(df: pd.DataFrame, order: int = 5, n_points: int = 10):
    """
    Finds local maxima and minima in the Close price using a rolling
    comparison window (`order` candles on each side).
    Returns the most recent `n_points` of each, oldest -> newest.
    """
    close = df["Close"].values
    max_idx = argrelextrema(close, np.greater_equal, order=order)[0]
    min_idx = argrelextrema(close, np.less_equal, order=order)[0]

    # de-duplicate consecutive flat runs that argrelextrema can double-count
    max_idx = _dedupe_adjacent(max_idx)
    min_idx = _dedupe_adjacent(min_idx)

    max_points = [
        {"date": df.index[i].strftime("%Y-%m-%d"), "price": round(float(close[i]), 2)}
        for i in max_idx[-n_points:]
    ]
    min_points = [
        {"date": df.index[i].strftime("%Y-%m-%d"), "price": round(float(close[i]), 2)}
        for i in min_idx[-n_points:]
    ]
    return max_points, min_points


def _dedupe_adjacent(idx_array, min_gap=2):
    if len(idx_array) == 0:
        return idx_array
    out = [idx_array[0]]
    for i in idx_array[1:]:
        if i - out[-1] >= min_gap:
            out.append(i)
    return np.array(out)


def support_resistance(max_points, min_points):
    """
    Turns the swing points into clean support/resistance levels
    (rounded clusters), nearest levels first.
    """
    resistance = sorted({p["price"] for p in max_points}, reverse=True)
    support = sorted({p["price"] for p in min_points}, reverse=True)
    return support, resistance


def compute_rsi(close: pd.Series, period: int = 14) -> float:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1]) if not rsi.empty and not np.isnan(rsi.iloc[-1]) else 50.0


def compute_macd(close: pd.Series):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    return {
        "macd": round(float(macd_line.iloc[-1]), 4),
        "signal": round(float(signal_line.iloc[-1]), 4),
        "histogram": round(float(histogram.iloc[-1]), 4),
        "bullish_cross": bool(histogram.iloc[-1] > 0 and histogram.iloc[-2] <= 0) if len(histogram) > 1 else False,
        "bearish_cross": bool(histogram.iloc[-1] < 0 and histogram.iloc[-2] >= 0) if len(histogram) > 1 else False,
    }


def trend_read(df: pd.DataFrame) -> str:
    close = df["Close"]
    sma20 = close.rolling(20).mean().iloc[-1]
    sma50 = close.rolling(min(50, len(close))).mean().iloc[-1]
    last = close.iloc[-1]
    if last > sma20 > sma50:
        return "Uptrend"
    if last < sma20 < sma50:
        return "Downtrend"
    return "Sideways / Consolidating"


def full_analysis(df: pd.DataFrame) -> dict:
    max_points, min_points = find_swing_points(df)
    support, resistance = support_resistance(max_points, min_points)
    rsi = compute_rsi(df["Close"])
    macd = compute_macd(df["Close"])
    trend = trend_read(df)

    return {
        "current_price": round(float(df["Close"].iloc[-1]), 2),
        "as_of": df.index[-1].strftime("%Y-%m-%d"),
        "trend": trend,
        "swing_maxima": max_points,
        "swing_minima": min_points,
        "support_levels": support,
        "resistance_levels": resistance,
        "rsi": round(rsi, 2),
        "macd": macd,
    }
