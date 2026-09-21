"""
charts.py
---------
Generates the visual side of the report: 10 different chart "views"
the user can pick from on screen, all of which are also embedded into
the downloaded PDF/DOCX report so the file matches what was on screen.

Every chart is returned as PNG bytes (matplotlib, headless Agg backend
-- no display server needed) so it can be shown inline in the browser
(<img src="data:image/png;base64,...">) and embedded in exported files.
"""

import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# a dark theme that matches the portal's UI
plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor": "#131a24",
    "axes.edgecolor": "#24303d",
    "axes.labelcolor": "#e7ecf2",
    "text.color": "#e7ecf2",
    "xtick.color": "#93a3b3",
    "ytick.color": "#93a3b3",
    "grid.color": "#24303d",
    "font.size": 9,
})

UP_COLOR = "#3fb97f"
DOWN_COLOR = "#d9695f"
GOLD = "#c9a24b"


def _fig_to_png(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()


def _entry_exit_points(df, analysis):
    entries = [(pd.to_datetime(p["date"]), p["price"]) for p in analysis["swing_minima"]]
    exits = [(pd.to_datetime(p["date"]), p["price"]) for p in analysis["swing_maxima"]]
    return entries, exits


def chart_line_entry_exit(df, analysis, symbol):
    entries, exits = _entry_exit_points(df, analysis)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(df.index, df["Close"], color=GOLD, linewidth=1.4, label="Close")
    if entries:
        ax.scatter(*zip(*entries), color=UP_COLOR, marker="^", s=70, zorder=5, label="Entry (support)")
    if exits:
        ax.scatter(*zip(*exits), color=DOWN_COLOR, marker="v", s=70, zorder=5, label="Exit (resistance)")
    ax.set_title(f"{symbol} — Price with Entry/Exit Points")
    ax.legend(facecolor="#131a24", labelcolor="#e7ecf2")
    ax.grid(alpha=0.3)
    return _fig_to_png(fig)


def chart_bar_volume(df, analysis, symbol):
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = [UP_COLOR if c >= o else DOWN_COLOR for o, c in zip(df["Open"], df["Close"])]
    ax.bar(df.index, df["Volume"], color=colors, width=1.0)
    ax.set_title(f"{symbol} — Daily Volume")
    ax.grid(alpha=0.3)
    return _fig_to_png(fig)


def chart_pie_updown(df, analysis, symbol):
    up_days = int((df["Close"].diff() > 0).sum())
    down_days = int((df["Close"].diff() < 0).sum())
    flat_days = max(len(df) - up_days - down_days - 1, 0)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        [up_days, down_days, flat_days],
        labels=["Up days", "Down days", "Flat days"],
        colors=[UP_COLOR, DOWN_COLOR, "#93a3b3"],
        autopct="%1.0f%%",
        textprops={"color": "#0d1117"},
    )
    ax.set_title(f"{symbol} — Up vs Down Days")
    return _fig_to_png(fig)


def chart_scatter_returns(df, analysis, symbol):
    returns = df["Close"].pct_change().dropna() * 100
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = [UP_COLOR if r >= 0 else DOWN_COLOR for r in returns]
    ax.scatter(returns.index, returns.values, color=colors, s=14)
    ax.axhline(0, color="#93a3b3", linewidth=0.8)
    ax.set_title(f"{symbol} — Daily % Returns (dot view)")
    ax.grid(alpha=0.3)
    return _fig_to_png(fig)


def chart_area(df, analysis, symbol):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(df.index, df["Close"], color=GOLD, alpha=0.25)
    ax.plot(df.index, df["Close"], color=GOLD, linewidth=1.2)
    ax.set_title(f"{symbol} — Price (Area View)")
    ax.grid(alpha=0.3)
    return _fig_to_png(fig)


def chart_histogram_returns(df, analysis, symbol):
    returns = df["Close"].pct_change().dropna() * 100
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(returns, bins=30, color=GOLD, edgecolor="#0d1117")
    ax.set_title(f"{symbol} — Distribution of Daily Returns")
    ax.grid(alpha=0.3)
    return _fig_to_png(fig)


def chart_candlestick(df, analysis, symbol):
    try:
        import mplfinance as mpf
        style = mpf.make_mpf_style(
            base_mpf_style="nightclouds",
            marketcolors=mpf.make_marketcolors(up=UP_COLOR, down=DOWN_COLOR),
        )
        fig, _ = mpf.plot(
            df.tail(90), type="candle", style=style, returnfig=True,
            figsize=(8, 4.2), title=f"{symbol} — Candlestick (last 90 candles)",
        )
        return _fig_to_png(fig)
    except Exception:
        # fallback: simple manual OHLC bars if mplfinance isn't installed
        recent = df.tail(60)
        fig, ax = plt.subplots(figsize=(8, 4.2))
        for i, (_, row) in enumerate(recent.iterrows()):
            color = UP_COLOR if row["Close"] >= row["Open"] else DOWN_COLOR
            ax.plot([i, i], [row["Low"], row["High"]], color=color, linewidth=1)
            ax.plot([i, i], [row["Open"], row["Close"]], color=color, linewidth=4)
        ax.set_title(f"{symbol} — OHLC (fallback view)")
        ax.grid(alpha=0.3)
        return _fig_to_png(fig)


def chart_moving_averages(df, analysis, symbol):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(df.index, df["Close"], color="#e7ecf2", linewidth=1, label="Close")
    ax.plot(df.index, df["Close"].rolling(20).mean(), color=GOLD, linewidth=1.4, label="SMA 20")
    ax.plot(df.index, df["Close"].rolling(50).mean(), color=UP_COLOR, linewidth=1.4, label="SMA 50")
    ax.set_title(f"{symbol} — Moving Averages")
    ax.legend(facecolor="#131a24", labelcolor="#e7ecf2")
    ax.grid(alpha=0.3)
    return _fig_to_png(fig)


def chart_support_resistance(df, analysis, symbol):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(df.index, df["Close"], color=GOLD, linewidth=1.3, label="Close")
    for lvl in analysis["support_levels"][:3]:
        ax.axhline(lvl, color=UP_COLOR, linestyle="--", linewidth=1)
    for lvl in analysis["resistance_levels"][:3]:
        ax.axhline(lvl, color=DOWN_COLOR, linestyle="--", linewidth=1)
    ax.set_title(f"{symbol} — Support (green) / Resistance (red) Zones")
    ax.grid(alpha=0.3)
    return _fig_to_png(fig)


def chart_cumulative_return(df, analysis, symbol):
    cum = (df["Close"] / df["Close"].iloc[0] - 1) * 100
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df.index, cum, color=GOLD, linewidth=1.4)
    ax.axhline(0, color="#93a3b3", linewidth=0.8)
    ax.fill_between(df.index, cum, 0, where=(cum >= 0), color=UP_COLOR, alpha=0.2)
    ax.fill_between(df.index, cum, 0, where=(cum < 0), color=DOWN_COLOR, alpha=0.2)
    ax.set_title(f"{symbol} — Cumulative Return Since Start of Period (%)")
    ax.grid(alpha=0.3)
    return _fig_to_png(fig)


# Registry — 10 selectable chart types. Keys are used in the UI dropdown
# and the ?type= query param / download bundling.
CHART_REGISTRY = {
    "line_entry_exit": ("Line — Entry/Exit Highlighted", chart_line_entry_exit),
    "bar_volume": ("Bar — Daily Volume", chart_bar_volume),
    "pie_updown": ("Pie — Up vs Down Days", chart_pie_updown),
    "scatter_returns": ("Dot/Scatter — Daily Returns", chart_scatter_returns),
    "area": ("Area — Price", chart_area),
    "histogram_returns": ("Histogram — Return Distribution", chart_histogram_returns),
    "candlestick": ("Candlestick — OHLC", chart_candlestick),
    "moving_averages": ("Line — Moving Averages (SMA20/50)", chart_moving_averages),
    "support_resistance": ("Line — Support/Resistance Zones", chart_support_resistance),
    "cumulative_return": ("Area — Cumulative Return %", chart_cumulative_return),
}


def generate_chart(chart_key, df, analysis, symbol) -> bytes:
    if chart_key not in CHART_REGISTRY:
        chart_key = "line_entry_exit"
    _, func = CHART_REGISTRY[chart_key]
    return func(df, analysis, symbol)


def generate_all_charts(df, analysis, symbol) -> dict:
    """Used when building the downloadable report — every chart type, embedded."""
    out = {}
    for key, (label, func) in CHART_REGISTRY.items():
        try:
            out[label] = func(df, analysis, symbol)
        except Exception:
            continue
    return out
