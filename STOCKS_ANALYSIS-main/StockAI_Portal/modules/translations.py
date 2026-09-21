"""
translations.py
----------------
Simple dictionary-based translation layer.
No external API / API key needed. Add more languages by adding a new
key to TRANSLATIONS with the same set of phrase-keys as "en".
"""

TRANSLATIONS = {
    "en": {
        "app_name": "StockAI Portal",
        "welcome": "Welcome",
        "onboarding_title": "Tell us about yourself",
        "name_label": "Your Name",
        "language_label": "Preferred Language",
        "risk_label": "Risk Tolerance",
        "risk_low": "Low (Conservative)",
        "risk_med": "Medium (Balanced)",
        "risk_high": "High (Aggressive)",
        "style_label": "Investing Style",
        "style_long": "Long-term / Growth",
        "style_short": "Short-term / Trading",
        "style_dividend": "Dividend / Income",
        "asset_label": "Asset Type",
        "asset_stock": "Stock",
        "asset_crypto": "Cryptocurrency",
        "asset_forex": "Currency / Forex",
        "symbol_label": "Symbol / Ticker (e.g. TATAMOTORS.NS, BTC-USD, EURUSD=X)",
        "period_label": "Time Period to Study",
        "upload_csv_label": "Optional: Upload price history (CSV)",
        "upload_img_label": "Optional: Upload a chart photo (best-effort analysis)",
        "continue_btn": "Continue to Dashboard",
        "analyze_btn": "Analyze Now",
        "dashboard_title": "Live Analysis Dashboard",
        "report_title": "Detailed Stock Study & Summary Report",
        "current_price": "Current Price",
        "trend": "Overall Trend",
        "support_levels": "Support Levels (from recent minima)",
        "resistance_levels": "Resistance Levels (from recent maxima)",
        "rsi": "RSI (Momentum)",
        "macd": "MACD Signal",
        "forecast": "AI Forecast (Next Period)",
        "next_entry": "Suggested Next Entry / Call Zone",
        "recommendation": "Recommendation",
        "action_steps": "Suggested Next Steps",
        "disclaimer": "This is an AI-generated educational analysis, not financial advice. Markets carry risk; please do your own research or consult a licensed advisor before investing.",
        "download_pdf": "Download PDF",
        "download_docx": "Download Word (DOCX)",
        "download_csv": "Download CSV",
        "download_txt": "Download TXT",
        "daily_scenario": "Today's Market Scenario",
        "nav_home": "Home",
        "nav_dashboard": "Dashboard",
        "nav_daily": "Daily Market",
        "nav_report": "Report",
        "buy": "BUY",
        "sell": "SELL",
        "hold": "HOLD",
        "investment_amount_label": "How much are you planning to invest? (numeral)",
        "currency_label": "Currency",
        "experience_label": "Years of investing/trading experience",
        "experience_beginner": "Beginner (0-1 years)",
        "experience_intermediate": "Intermediate (1-5 years)",
        "experience_experienced": "Experienced (5+ years)",
        "duration_preset_label": "Choose a preset period",
        "duration_custom_label": "Or set a custom duration",
        "duration_custom_value": "Number",
        "duration_custom_unit": "Unit",
        "unit_days": "Days",
        "unit_weeks": "Weeks",
        "unit_months": "Months",
        "unit_years": "Years",
        "upload_any_label": "Optional: Upload price history — CSV, PDF, or Word (.docx)",
        "buy_example_heading": "Worked BUY Example",
        "sell_example_heading": "Worked SELL Example",
        "experience_highlight_heading": "Personalized For Your Experience Level",
        "search_section_title": "Search Official Sites for a Symbol",
        "search_placeholder": "Type a stock/crypto/currency name and pick a site",
        "search_helper": "New here? Type a name (e.g. \"Tata Motors\", \"Bitcoin\", \"Euro Dollar\") above, then click a site below to search it there and find the exact ticker/symbol to paste into the box above.",
        "chart_section_title": "Chart View",
        "chart_select_label": "Choose a chart type",
        "daily_visit_heading": "For Further Live Study",
        "daily_visit_text": "This snapshot updates on each page load. For deeper live charts, order books, and news, please visit the official sites below.",
    },
    "hi": {
        "app_name": "स्टॉकएआई पोर्टल",
        "welcome": "स्वागत है",
        "onboarding_title": "अपने बारे में बताएं",
        "name_label": "आपका नाम",
        "language_label": "पसंदीदा भाषा",
        "risk_label": "जोखिम सहनशीलता",
        "risk_low": "कम (सतर्क)",
        "risk_med": "मध्यम (संतुलित)",
        "risk_high": "उच्च (आक्रामक)",
        "style_label": "निवेश शैली",
        "style_long": "दीर्घकालिक / वृद्धि",
        "style_short": "अल्पकालिक / ट्रेडिंग",
        "style_dividend": "लाभांश / आय",
        "asset_label": "एसेट प्रकार",
        "asset_stock": "स्टॉक",
        "asset_crypto": "क्रिप्टोकरेंसी",
        "asset_forex": "मुद्रा / फॉरेक्स",
        "symbol_label": "सिंबल / टिकर (जैसे TATAMOTORS.NS, BTC-USD, EURUSD=X)",
        "period_label": "अध्ययन के लिए समयावधि",
        "upload_csv_label": "वैकल्पिक: प्राइस हिस्ट्री अपलोड करें (CSV)",
        "upload_img_label": "वैकल्पिक: चार्ट की फोटो अपलोड करें (अनुमानित विश्लेषण)",
        "continue_btn": "डैशबोर्ड पर जाएं",
        "analyze_btn": "अभी विश्लेषण करें",
        "dashboard_title": "लाइव विश्लेषण डैशबोर्ड",
        "report_title": "विस्तृत स्टॉक अध्ययन और सारांश रिपोर्ट",
        "current_price": "वर्तमान मूल्य",
        "trend": "समग्र रुझान",
        "support_levels": "सपोर्ट स्तर (हाल के न्यूनतम से)",
        "resistance_levels": "रेजिस्टेंस स्तर (हाल के अधिकतम से)",
        "rsi": "आरएसआई (मोमेंटम)",
        "macd": "एमएसीडी संकेत",
        "forecast": "एआई पूर्वानुमान (अगली अवधि)",
        "next_entry": "अगला सुझाया गया एंट्री / कॉल ज़ोन",
        "recommendation": "सिफारिश",
        "action_steps": "अगले सुझाए गए कदम",
        "disclaimer": "यह एक एआई-जनित शैक्षिक विश्लेषण है, वित्तीय सलाह नहीं। बाजार में जोखिम है; निवेश से पहले अपना शोध करें या लाइसेंस प्राप्त सलाहकार से सलाह लें।",
        "download_pdf": "पीडीएफ डाउनलोड करें",
        "download_docx": "वर्ड (DOCX) डाउनलोड करें",
        "download_csv": "सीएसवी डाउनलोड करें",
        "download_txt": "टीएक्सटी डाउनलोड करें",
        "daily_scenario": "आज का बाज़ार परिदृश्य",
        "nav_home": "होम",
        "nav_dashboard": "डैशबोर्ड",
        "nav_daily": "दैनिक बाज़ार",
        "nav_report": "रिपोर्ट",
        "buy": "खरीदें",
        "sell": "बेचें",
        "hold": "रोकें",
        "investment_amount_label": "आप कितना निवेश करने की योजना बना रहे हैं? (अंकों में)",
        "currency_label": "मुद्रा",
        "experience_label": "निवेश/ट्रेडिंग अनुभव (वर्षों में)",
        "experience_beginner": "शुरुआती (0-1 वर्ष)",
        "experience_intermediate": "मध्यम (1-5 वर्ष)",
        "experience_experienced": "अनुभवी (5+ वर्ष)",
        "duration_preset_label": "एक निर्धारित अवधि चुनें",
        "duration_custom_label": "या कस्टम अवधि सेट करें",
        "duration_custom_value": "संख्या",
        "duration_custom_unit": "इकाई",
        "unit_days": "दिन",
        "unit_weeks": "सप्ताह",
        "unit_months": "महीने",
        "unit_years": "वर्ष",
        "upload_any_label": "वैकल्पिक: प्राइस हिस्ट्री अपलोड करें — CSV, PDF, या Word (.docx)",
        "buy_example_heading": "उदाहरण सहित BUY (खरीद) योजना",
        "sell_example_heading": "उदाहरण सहित SELL (बिक्री) योजना",
        "experience_highlight_heading": "आपके अनुभव स्तर के अनुसार व्यक्तिगत सुझाव",
        "search_section_title": "सिंबल खोजने के लिए आधिकारिक साइटें",
        "search_placeholder": "स्टॉक/क्रिप्टो/मुद्रा का नाम लिखें और एक साइट चुनें",
        "search_helper": "पहली बार आए हैं? ऊपर एक नाम लिखें (जैसे \"Tata Motors\", \"Bitcoin\", \"Euro Dollar\"), फिर नीचे किसी साइट पर क्लिक करके वहां खोजें और सही टिकर/सिंबल पता करें, फिर उसे ऊपर के बॉक्स में डालें।",
        "chart_section_title": "चार्ट व्यू",
        "chart_select_label": "चार्ट का प्रकार चुनें",
        "daily_visit_heading": "आगे के लाइव अध्ययन के लिए",
        "daily_visit_text": "यह स्नैपशॉट हर पेज लोड पर अपडेट होता है। गहरे लाइव चार्ट, ऑर्डर बुक और समाचार के लिए कृपया नीचे दी गई आधिकारिक साइटों पर जाएं।",
    },
}


def t(lang, key):
    """
    Looks up `key` in the hand-written English/Hindi dictionary first
    (fast, no network). For any other world language, falls back to
    free machine translation of the English phrase (see lang_support.py),
    so the whole UI works in any language, not just the two built in.
    """
    english_text = TRANSLATIONS["en"].get(key, key)

    if lang in TRANSLATIONS:
        return TRANSLATIONS[lang].get(key, english_text)

    from .lang_support import translate
    return translate(english_text, lang)


def translate_text(text, lang):
    """
    Translates an arbitrary dynamic sentence (e.g. a report bullet that
    already contains real numbers/symbol names) into `lang`. English
    and Hindi text built by report_gen is already in the right language
    at build time, so this is only used for every other world language.
    """
    if lang in ("en", "hi") or not text:
        return text
    from .lang_support import translate
    return translate(text, lang)
