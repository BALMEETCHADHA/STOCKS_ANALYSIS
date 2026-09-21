"""
forecast.py
-----------
Two things:
1. A short-horizon price forecast using ARIMA (statsmodels) -- falls back
   to a simple linear-regression trend projection if ARIMA fails to
   converge (e.g. too little data).
2. A rule-based BUY / SELL / HOLD call that combines:
     - trend (from analysis.py)
     - RSI / MACD momentum
     - distance to nearest support / resistance (from swing points)
   and produces the "next suggested entry / call zone" the user asked for.

This is a transparent, explainable model (not a black box) so every
number in the report can be traced back to a rule.
"""

import numpy as np
import pandas as pd


def forecast_next_period(df: pd.DataFrame, steps: int = 5) -> dict:
    close = df["Close"]
    try:
        from statsmodels.tsa.arima.model import ARIMA
        model = ARIMA(close, order=(5, 1, 0))
        fit = model.fit()
        forecast = fit.forecast(steps=steps)
        method = "ARIMA(5,1,0)"
        values = [round(float(v), 2) for v in forecast]
    except Exception:
        # fallback: linear regression on the last 30 candles
        window = close.tail(30).values
        x = np.arange(len(window))
        coeffs = np.polyfit(x, window, 1)
        slope, intercept = coeffs[0], coeffs[1]
        future_x = np.arange(len(window), len(window) + steps)
        values = [round(float(slope * fx + intercept), 2) for fx in future_x]
        method = "Linear trend projection"

    return {
        "method": method,
        "horizon_steps": steps,
        "projected_prices": values,
        "projected_change_pct": round(((values[-1] - float(close.iloc[-1])) / float(close.iloc[-1])) * 100, 2),
    }


def next_call_zone(current_price: float, support_levels: list, resistance_levels: list) -> dict:
    """
    Finds the nearest support below and resistance above current price --
    this is the "next call" zone: buy near support, book profit / sell
    near resistance.
    """
    supports_below = sorted([s for s in support_levels if s < current_price], reverse=True)
    resistances_above = sorted([r for r in resistance_levels if r > current_price])

    nearest_support = supports_below[0] if supports_below else min(support_levels, default=current_price * 0.95)
    nearest_resistance = resistances_above[0] if resistances_above else max(resistance_levels, default=current_price * 1.05)

    return {
        "buy_zone_near": round(nearest_support, 2),
        "sell_zone_near": round(nearest_resistance, 2),
        "risk_reward_ratio": round(
            (nearest_resistance - current_price) / max(current_price - nearest_support, 0.01), 2
        ),
    }


def worked_examples(investment_amount: float, currency: str, current_price: float, call_zone: dict) -> dict:
    """
    Turns the abstract buy/sell zone into a concrete worked example using
    the amount the user told us they plan to invest (asked at sign-up),
    so "next entry" isn't just a price -- it's "with ₹1000 you could..."
    Always returns BOTH a buy-side and a sell-side example, as requested.
    """
    investment_amount = max(float(investment_amount or 1000), 1.0)
    buy_price = call_zone["buy_zone_near"]
    sell_price = call_zone["sell_zone_near"]

    units_at_buy = round(investment_amount / buy_price, 4) if buy_price > 0 else 0
    units_at_current = round(investment_amount / current_price, 4) if current_price > 0 else 0
    potential_value_at_sell = round(units_at_buy * sell_price, 2)
    potential_gain = round(potential_value_at_sell - investment_amount, 2)
    potential_gain_pct = round((potential_gain / investment_amount) * 100, 2) if investment_amount else 0

    proceeds_if_sold_now = round(units_at_current * current_price, 2)

    return {
        "investment_amount": round(investment_amount, 2),
        "currency": currency,
        "buy_example": {
            "narrative": (
                f"If you had {currency} {investment_amount:,.0f} ready to deploy and bought near the "
                f"support/BUY zone of {buy_price}, that would get you approximately {units_at_buy:,.4f} "
                f"units. If price then reaches the resistance/SELL zone of {sell_price}, that position "
                f"would be worth approximately {currency} {potential_value_at_sell:,.2f} "
                f"— a potential gain of {currency} {potential_gain:,.2f} ({potential_gain_pct}%)."
            ),
            "units": units_at_buy,
            "entry_price": buy_price,
            "target_price": sell_price,
            "potential_gain": potential_gain,
            "potential_gain_pct": potential_gain_pct,
        },
        "sell_example": {
            "narrative": (
                f"If you already hold this asset and bought it earlier, selling near the current "
                f"resistance zone of {sell_price} locks in the upside before a possible pullback. "
                f"For reference, {currency} {investment_amount:,.0f} worth at today's price of "
                f"{current_price} equals about {units_at_current:,.4f} units, worth approximately "
                f"{currency} {proceeds_if_sold_now:,.2f} if sold right now at market price."
            ),
            "units": units_at_current,
            "sell_price": sell_price,
            "current_value": proceeds_if_sold_now,
        },
    }


def experience_highlight(rec: dict, call_zone: dict, years_experience: str) -> str:
    """
    A one-paragraph, experience-tailored highlight built from the same
    call/zone data as the rest of the report -- ties the recommendation
    and the buy/sell zone together differently depending on how
    experienced the user told us they are at sign-up.
    """
    call = rec["call"]
    buy = call_zone["buy_zone_near"]
    sell = call_zone["sell_zone_near"]

    if years_experience == "beginner":
        return (
            f"Since you're new to investing (0-1 years), keep this simple: the model's current call is "
            f"{call}. Treat {buy} as a 'good value' zone to consider buying in small amounts, and {sell} "
            f"as a 'take some profit' zone if you already hold it. Avoid putting in a large lump sum at "
            f"once — start small, watch how it behaves, and only increase your position as you get "
            f"more comfortable reading these reports."
        )
    if years_experience == "experienced":
        return (
            f"Given your 5+ years of experience, you'll likely want to combine this rule-based "
            f"{call} call with your own read on volume profile, sector trends, and news catalysts "
            f"around the {buy}-{sell} range, and size positions using your own risk framework rather "
            f"than relying on this alone — this report is best used as one more confirming (or "
            f"contradicting) data point."
        )
    return (
        f"With 1-5 years of experience, you're likely comfortable acting on the {call} call directly: "
        f"use {buy} as your planned entry zone and {sell} as your planned exit/profit-booking zone, "
        f"and consider scaling in/out across 2-3 tranches rather than a single order."
    )


def recommendation(analysis: dict, forecast: dict, risk_tolerance: str = "medium") -> dict:
    score = 0
    reasons = []

    if analysis["trend"] == "Uptrend":
        score += 1
        reasons.append("Price is trading above its 20 & 50-day averages (uptrend).")
    elif analysis["trend"] == "Downtrend":
        score -= 1
        reasons.append("Price is trading below its 20 & 50-day averages (downtrend).")
    else:
        reasons.append("Price is moving sideways with no clear trend.")

    rsi = analysis["rsi"]
    if rsi < 30:
        score += 1
        reasons.append(f"RSI is {rsi} — asset looks oversold, often a bounce zone.")
    elif rsi > 70:
        score -= 1
        reasons.append(f"RSI is {rsi} — asset looks overbought, pullback risk.")
    else:
        reasons.append(f"RSI is {rsi} — neutral momentum.")

    macd = analysis["macd"]
    if macd["bullish_cross"]:
        score += 1
        reasons.append("MACD just crossed bullish (upward momentum trigger).")
    elif macd["bearish_cross"]:
        score -= 1
        reasons.append("MACD just crossed bearish (downward momentum trigger).")

    if forecast["projected_change_pct"] > 1:
        score += 1
        reasons.append(f"Short-term model projects a further +{forecast['projected_change_pct']}% move.")
    elif forecast["projected_change_pct"] < -1:
        score -= 1
        reasons.append(f"Short-term model projects a {forecast['projected_change_pct']}% pullback.")

    # risk tolerance shifts the threshold for calling BUY vs HOLD
    thresholds = {"low": 2, "medium": 1, "high": 0}
    buy_threshold = thresholds.get(risk_tolerance, 1)

    if score > buy_threshold:
        call = "BUY"
    elif score < -buy_threshold:
        call = "SELL"
    else:
        call = "HOLD"

    return {"call": call, "score": score, "reasons": reasons}
