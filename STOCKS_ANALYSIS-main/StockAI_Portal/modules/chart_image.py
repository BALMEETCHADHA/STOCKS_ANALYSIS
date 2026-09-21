"""
chart_image.py
--------------
Optional, best-effort feature: if a user uploads a PHOTO of a chart
(screenshot, graph image) instead of/alongside real data, we trace the
dominant plotted line's pixel path and rescale it to a price series
using the price-axis min/max the user provides.

IMPORTANT (shown to the user in the UI too): this is an approximation
of the visual shape only. It cannot recover exact OHLC values, so it
is used for a *supporting* trend read, not the primary numeric
analysis. Live/CSV data always takes priority when available.
"""

import numpy as np
import cv2


def trace_chart_line(image_path: str, price_min: float, price_max: float, n_points: int = 100):
    """
    Reads an image, isolates the most prominent non-background line
    color, and returns an approximate normalized price series scaled
    between price_min and price_max.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read the uploaded image.")

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge map to find the plotted line irrespective of its color
    edges = cv2.Canny(gray, 50, 150)

    # Sample columns left -> right, take the topmost edge pixel per column
    # (works reasonably for a single line-chart trace on a plain background)
    xs = np.linspace(0, w - 1, n_points).astype(int)
    ys = []
    for x in xs:
        col = edges[:, x]
        nonzero = np.nonzero(col)[0]
        if len(nonzero) > 0:
            ys.append(np.mean(nonzero))
        else:
            ys.append(np.nan)

    ys = np.array(ys, dtype=float)
    # fill any gaps by interpolation
    nans = np.isnan(ys)
    if nans.all():
        raise ValueError("Could not detect a chart line in this image.")
    ys[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), ys[~nans])

    # invert because image y=0 is the top of the picture (higher price = smaller y)
    y_min, y_max = ys.min(), ys.max()
    if y_max == y_min:
        normalized = np.full_like(ys, 0.5)
    else:
        normalized = 1 - (ys - y_min) / (y_max - y_min)

    prices = price_min + normalized * (price_max - price_min)
    return [round(float(p), 2) for p in prices]
