"""
lang_support.py
----------------
1. WORLD_LANGUAGES — a large list of (code, native name) pairs so the
   onboarding page can offer "all languages of the world", not just a
   couple of hardcoded ones.
2. translate(text, lang) — translates any report string into the
   chosen language on the fly using `deep-translator`'s free Google
   Translate wrapper (no API key). English and Hindi are always served
   from the static, hand-written dictionary in translations.py (fast,
   no network dependency); every other language is machine-translated
   at request time.
3. Fails safe: if there's no internet or the translation call errors,
   the original English text is returned rather than breaking the
   report.
"""

# (code, native display name) — a broad set covering every major
# world region/script. Extend this list any time.
WORLD_LANGUAGES = [
    ("en", "English"), ("hi", "हिन्दी (Hindi)"), ("es", "Español (Spanish)"),
    ("fr", "Français (French)"), ("de", "Deutsch (German)"), ("it", "Italiano (Italian)"),
    ("pt", "Português (Portuguese)"), ("ru", "Русский (Russian)"), ("zh-CN", "中文 (Chinese, Simplified)"),
    ("zh-TW", "中文 (Chinese, Traditional)"), ("ja", "日本語 (Japanese)"), ("ko", "한국어 (Korean)"),
    ("ar", "العربية (Arabic)"), ("bn", "বাংলা (Bengali)"), ("ur", "اردو (Urdu)"),
    ("pa", "ਪੰਜਾਬੀ (Punjabi)"), ("gu", "ગુજરાતી (Gujarati)"), ("mr", "मराठी (Marathi)"),
    ("ta", "தமிழ் (Tamil)"), ("te", "తెలుగు (Telugu)"), ("kn", "ಕನ್ನಡ (Kannada)"),
    ("ml", "മലയാളം (Malayalam)"), ("or", "ଓଡ଼ିଆ (Odia)"), ("as", "অসমীয়া (Assamese)"),
    ("ne", "नेपाली (Nepali)"), ("si", "සිංහල (Sinhala)"), ("th", "ไทย (Thai)"),
    ("vi", "Tiếng Việt (Vietnamese)"), ("id", "Bahasa Indonesia"), ("ms", "Bahasa Melayu (Malay)"),
    ("tl", "Filipino (Tagalog)"), ("my", "မြန်မာ (Burmese)"), ("km", "ខ្មែរ (Khmer)"),
    ("lo", "ລາວ (Lao)"), ("tr", "Türkçe (Turkish)"), ("fa", "فارسی (Persian)"),
    ("he", "עברית (Hebrew)"), ("pl", "Polski (Polish)"), ("nl", "Nederlands (Dutch)"),
    ("sv", "Svenska (Swedish)"), ("no", "Norsk (Norwegian)"), ("da", "Dansk (Danish)"),
    ("fi", "Suomi (Finnish)"), ("el", "Ελληνικά (Greek)"), ("cs", "Čeština (Czech)"),
    ("sk", "Slovenčina (Slovak)"), ("ro", "Română (Romanian)"), ("hu", "Magyar (Hungarian)"),
    ("bg", "Български (Bulgarian)"), ("uk", "Українська (Ukrainian)"), ("hr", "Hrvatski (Croatian)"),
    ("sr", "Српски (Serbian)"), ("sl", "Slovenščina (Slovenian)"), ("lt", "Lietuvių (Lithuanian)"),
    ("lv", "Latviešu (Latvian)"), ("et", "Eesti (Estonian)"), ("sq", "Shqip (Albanian)"),
    ("mk", "Македонски (Macedonian)"), ("ka", "ქართული (Georgian)"), ("hy", "Հայերեն (Armenian)"),
    ("az", "Azərbaycan (Azerbaijani)"), ("kk", "Қазақ (Kazakh)"), ("uz", "Oʻzbek (Uzbek)"),
    ("mn", "Монгол (Mongolian)"), ("sw", "Kiswahili (Swahili)"), ("am", "አማርኛ (Amharic)"),
    ("ha", "Hausa"), ("yo", "Yorùbá"), ("ig", "Igbo"), ("zu", "isiZulu (Zulu)"),
    ("xh", "isiXhosa (Xhosa)"), ("af", "Afrikaans"), ("so", "Soomaali (Somali)"),
    ("is", "Íslenska (Icelandic)"), ("ga", "Gaeilge (Irish)"), ("cy", "Cymraeg (Welsh)"),
    ("eu", "Euskara (Basque)"), ("ca", "Català (Catalan)"), ("gl", "Galego (Galician)"),
]


def translate(text: str, lang: str, static_lookup=None) -> str:
    """
    Returns `text` translated into `lang`.
    - If `lang` is 'en', returns text unchanged.
    - If a static_lookup(text) is supplied and returns a value (used
      for the hand-written English/Hindi phrase dictionary), that is
      preferred over machine translation for accuracy/speed.
    - Otherwise, attempts a free machine translation. On any failure
      (no internet, library missing, rate limit) it silently falls
      back to the original English text so the app never breaks.
    """
    if lang == "en" or not text:
        return text

    if static_lookup is not None:
        looked_up = static_lookup(text)
        if looked_up is not None:
            return looked_up

    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="en", target=lang).translate(text)
    except Exception:
        return text


def translate_many(texts, lang: str, static_lookup=None):
    """Batch helper — translates a list of strings, same fallback rules."""
    return [translate(t_, lang, static_lookup) for t_ in texts]
