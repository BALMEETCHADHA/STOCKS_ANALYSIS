"""
search_links.py
----------------
Real, official financial sites the user can search directly to find a
name/company's exact ticker before pasting it into the Symbol box, and
to do deeper live research than this portal's own snapshot provides.

Several sites (NSE, BSE, CoinGecko, Google Finance) block or reject a
freshly-guessed query URL hit from another domain (bot/WAF checks, or
a query-param format that isn't actually their real search endpoint),
which is exactly the "link doesn't open" problem. To make every single
button reliably open something useful, those go through a Google
site-restricted search instead (`site:domain query`) — Google's own
search always loads, and the very first result is that site's page for
the query. Yahoo Finance's and Investing.com's own search endpoints are
well-documented and stable, so those go direct.

Everything here is a plain outbound https link — no scraping, no API
key, no login. The search sites take a `%s` query placeholder that the
frontend fills in with JavaScript from whatever the user typed.
"""


def _google_site_search(domain: str) -> str:
    return f"https://www.google.com/search?q=site:{domain}+%s"


SEARCH_SITES = [
    {
        "name": "Yahoo Finance",
        "for": "Stocks, crypto, forex, indices (global)",
        "search_url": "https://finance.yahoo.com/lookup?s=%s",
        "steps": [
            "Type the company/asset name (e.g. \"Tata Motors\") in the search box.",
            "Yahoo shows a list of matches with their exact ticker symbol (e.g. TATAMOTORS.NS).",
            "Copy that exact ticker and paste it into this portal's Symbol box.",
        ],
    },
    {
        "name": "Google Finance",
        "for": "Stocks & indices (global) — live market view",
        "search_url": "https://www.google.com/search?q=%s+google+finance+live+price",
        "steps": [
            "Type the company/asset name.",
            "Google usually shows a live price card right at the top of results.",
            "Click through to the full Google Finance page for charts and news.",
        ],
    },
    {
        "name": "NSE India",
        "for": "Indian stocks (official exchange)",
        "search_url": _google_site_search("nseindia.com"),
        "steps": [
            "Type the company name or NSE symbol.",
            "Open the official nseindia.com result to confirm the exact NSE symbol.",
            "In this portal, add \".NS\" after that symbol, e.g. TATAMOTORS.NS.",
        ],
    },
    {
        "name": "BSE India",
        "for": "Indian stocks (official exchange, alternate)",
        "search_url": _google_site_search("bseindia.com"),
        "steps": [
            "Type the company name.",
            "Open the official bseindia.com result to see its BSE code.",
            "Yahoo/NSE tickers are usually easier to paste directly into this portal.",
        ],
    },
    {
        "name": "CoinMarketCap",
        "for": "Cryptocurrencies",
        "search_url": _google_site_search("coinmarketcap.com"),
        "steps": [
            "Type the coin's name (e.g. \"Bitcoin\", \"Ethereum\").",
            "Note its ticker (e.g. BTC, ETH) on the official coinmarketcap.com page.",
            "In this portal, use the format TICKER-USD, e.g. BTC-USD.",
        ],
    },
    {
        "name": "CoinGecko",
        "for": "Cryptocurrencies (alternate)",
        "search_url": _google_site_search("coingecko.com"),
        "steps": [
            "Type the coin name or ticker.",
            "Confirm the exact ticker symbol on its official coingecko.com page.",
            "Use TICKER-USD in this portal's Symbol box.",
        ],
    },
    {
        "name": "XE Currency Converter",
        "for": "Currency / forex pairs",
        "search_url": "https://www.xe.com/currencyconverter/convert/?Amount=1&From=%s&To=USD",
        "steps": [
            "Type the 3-letter currency code (e.g. EUR, GBP, INR, JPY) — not the full name.",
            "XE shows the live conversion rate against USD.",
            "In this portal, combine the two codes as BASEQUOTE=X, e.g. EURUSD=X.",
        ],
    },
    {
        "name": "Investing.com",
        "for": "Stocks, crypto, forex, commodities (global)",
        "search_url": "https://www.investing.com/search/?q=%s",
        "steps": [
            "Type any asset name — stock, crypto, or currency pair.",
            "Investing.com shows category-matched results with more details.",
            "Cross-check the exact ticker format on Yahoo Finance before pasting here.",
        ],
    },
]


def google_finance_search_url(name: str) -> str:
    """Used for the Daily Market tiles -- a guaranteed-to-open Google
    search that surfaces that index/asset's live Google Finance price
    card, without depending on guessing Google Finance's internal
    ticker:exchange code format."""
    from urllib.parse import quote_plus
    return f"https://www.google.com/search?q={quote_plus(name)}+google+finance+live+price"


def yahoo_quote_url(symbol: str) -> str:
    """Direct, stable Yahoo Finance quote page for a specific symbol —
    used as the 'view live' link once a symbol has actually been
    analyzed (e.g. in the report's Welcome section)."""
    from urllib.parse import quote_plus
    return f"https://finance.yahoo.com/quote/{quote_plus(symbol)}"
