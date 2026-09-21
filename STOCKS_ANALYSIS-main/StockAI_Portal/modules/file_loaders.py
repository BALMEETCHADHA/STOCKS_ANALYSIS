"""
file_loaders.py
----------------
Lets the user upload their price history in PDF, Word (.docx), or CSV —
not just CSV. All three end up normalized to the same
Open/High/Low/Close/Volume DataFrame that data_fetch.py produces from
live data, so the rest of the pipeline (analysis/forecast/report)
doesn't need to care which format the user uploaded.

Expected table layout in the PDF/Word file: a Date column plus a Close
column (Open/High/Low/Volume are optional and filled in if missing) —
the same convention as the CSV loader.
"""

import re
import pandas as pd


def _normalize_table(rows_with_header):
    """rows_with_header: list of lists, first row = header."""
    header = [str(h).strip().capitalize() for h in rows_with_header[0]]
    data_rows = rows_with_header[1:]
    df = pd.DataFrame(data_rows, columns=header)

    if "Date" not in df.columns or "Close" not in df.columns:
        raise ValueError("Could not find 'Date' and 'Close' columns in the uploaded file's table.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).set_index("Date").sort_index()

    for col in ["Open", "High", "Low", "Close"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "").str.replace("₹", "").str.replace("$", ""),
                errors="coerce",
            )
    df = df.dropna(subset=["Close"])

    for col in ["Open", "High", "Low"]:
        if col not in df.columns:
            df[col] = df["Close"]
    if "Volume" not in df.columns:
        df["Volume"] = 0
    else:
        df["Volume"] = pd.to_numeric(df["Volume"].astype(str).str.replace(",", ""), errors="coerce").fillna(0)

    return df[["Open", "High", "Low", "Close", "Volume"]]


def load_pdf(filepath: str) -> pd.DataFrame:
    """Extracts the first table it finds in the PDF that has Date/Close-like columns."""
    import pdfplumber

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                if not table or len(table) < 2:
                    continue
                header = [str(h).strip().lower() for h in table[0]]
                if any("date" in h for h in header) and any("close" in h for h in header):
                    return _normalize_table(table)

    # fallback: try to regex "date  price" style lines out of raw text
    rows = [["Date", "Close"]]
    date_price_re = re.compile(r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})\s+[\₹\$]?([\d,]+\.?\d*)")
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for match in date_price_re.finditer(text):
                rows.append([match.group(1), match.group(2)])

    if len(rows) < 2:
        raise ValueError("No recognizable Date/Close table or Date-Price lines found in this PDF.")
    return _normalize_table(rows)


def load_docx(filepath: str) -> pd.DataFrame:
    """Extracts the first table in the Word document with Date/Close-like columns."""
    from docx import Document

    doc = Document(filepath)
    for table in doc.tables:
        rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
        if not rows or len(rows) < 2:
            continue
        header = [h.lower() for h in rows[0]]
        if any("date" in h for h in header) and any("close" in h for h in header):
            return _normalize_table(rows)

    raise ValueError("No table with 'Date' and 'Close' columns found in this Word document.")


def load_any(filepath: str, filename: str) -> pd.DataFrame:
    """Dispatches to the right loader based on file extension."""
    from . import data_fetch

    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if ext == "csv":
        return data_fetch.load_uploaded_csv(filepath)
    if ext == "pdf":
        return load_pdf(filepath)
    if ext in ("docx", "doc"):
        return load_docx(filepath)
    raise ValueError(f"Unsupported file type '.{ext}'. Please upload CSV, PDF, or Word (.docx).")
