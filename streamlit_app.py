import json
from urllib.parse import urlparse

import requests
import streamlit as st

MODEL = "gemini-3.8-flash"
API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"

FIELDS = [
    ("letter_analysis", "বর্ণ বিশ্লেষণ"),
    ("prakriti", "প্রকৃতি / মূল শব্দ"),
    ("prefix", "উপসর্গ"),
    ("suffix", "প্রত্যয়"),
    ("anusarga", "অনুসর্গ"),
    ("formation_analysis", "শব্দগঠন বিশ্লেষণ"),
    ("origin_analysis", "উৎপত্তিগত বিশ্লেষণ"),
    ("semantic_analysis", "অর্থগত বিশ্লেষণ"),
    ("synonyms", "সমার্থক শব্দ"),
    ("antonyms", "বিপরীতার্থক শব্দ"),
    ("sandhi_analysis", "সন্ধি বিশ্লেষণ"),
    ("part_of_speech", "পদ প্রকরণ"),
    ("syntax_analysis", "পদ / বাক্যে ব্যবহার"),
    ("action_based_meaning", "ক্রিয়া-ভিত্তিক শব্দার্থ"),
    ("letter_based_meaning", "বর্ণ-ভিত্তিক শব্দার্থ"),
    ("reliability_note", "বিশ্লেষণের সীমা ও নির্ভরযোগ্যতা"),
]

PROPERTIES = {
    "word": {"type": "string"},
    "pronunciation": {"type": "string"},
    **{key: {"type": "string"} for key, _ in FIELDS},
}
SCHEMA = {
    "type": "object",
    "properties": PROPERTIES,
    "required": list(PROPERTIES),
}

st.set_page_config(page_title="বাংলা শব্দ বিশ্লেষণ", page_icon="📚", layout="wide")
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Noto+Serif+Bengali:wght@400;500;600;700&display=swap');
      html, body, [class*="st-"] { font-family: 'Hind Siliguri', sans-serif; }
      .stApp { background: #f7f4ee; color: #1d2e42; }
      h1, h2, h3 { color: #182c44; }
      .hero { text-align:center; padding: 1.2rem 0 .5rem; }
      .eyebrow { color:#8c3949; font-weight:700; letter-spacing:1px; }
      .hero h1 { font-family:'Noto Serif Bengali',serif; }
      .muted { color:#777c80; }
      div[data-testid="stForm"] { background:#fffefa; border:1px solid #e8e2d7; border-radius:16px; padding:1rem; }
      div[data-testid="stVerticalBlockBorderWrapper"] { background:#fffefa; border-color:#eee8de; }
      a { color:#355c7e !important; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero"><div class="eyebrow">ওয়েব সূত্রসহ ভাষা বিশ্লেষণ</div>'
    '<h1>শব্দের গঠন ও অর্থ বুঝুন</h1>'
    '<p class="muted">বাংলা শব্দ লিখুন। গঠন, ব্যুৎপত্তি, অর্থ, পদ, সমার্থক ও বিপরীতার্থক শব্দ একসঙ্গে দেখুন।</p>'
    '<p class="muted">Created &amp; Maintained by NilanjanC</p></div>',
    unsafe_allow_html=True,
)

def build_prompt(word: str) -> str:
    return f"""বাংলা শব্দ “{word}”-এর একটি স্বতন্ত্র, সূত্র-সমর্থিত ভাষাতাত্ত্বিক বিশ্লেষণ তৈরি করুন। Google Search ব্যবহার করে একাধিক নির্ভরযোগ্য বাংলা অভিধান, বাংলা একাডেমি/বিশ্ববিদ্যালয়/ভাষাবিজ্ঞান সূত্র যেখানে পাওয়া যায় যাচাই করুন। সব ব্যাখ্যা সহজ বাংলায় লিখুন এবং JSON schema-র প্রতিটি ঘর পূরণ করুন।
বিশ্লেষণের নিয়ম:
- বর্ণ বিশ্লেষণে বানানের অক্ষর, কারচিহ্ন ও যুক্তবর্ণ আলাদা করে দেখান; বানানভুল ধরে নিলে জানান।
- প্রকৃতি/মূল শব্দ, উপসর্গ, প্রত্যয়, অনুসর্গ, শব্দগঠন এবং সন্ধি—প্রতিটি আলাদা করে বিচার করুন। কোনোটি প্রযোজ্য না হলে “প্রযোজ্য নয়” বলুন; কল্পিত উপাদান বানাবেন না।
- উৎপত্তিগত বিশ্লেষণে উৎসভাষা বা ঐতিহাসিক পরিবর্তনের দাবির পাশে নির্ভরযোগ্য সূত্রের ভিত্তি দিন; নিশ্চিত না হলে অনিশ্চয়তা স্পষ্ট করুন।
- অর্থগত বিশ্লেষণে প্রচলিত অর্থ, প্রসঙ্গভেদ, রূপক অর্থ আলাদা করুন।
- সমার্থক শব্দে শব্দটির প্রসঙ্গ-উপযোগী কাছাকাছি অর্থের বাংলা শব্দ দিন; প্রতিটির সূক্ষ্ম অর্থপার্থক্য বা ব্যবহার-প্রসঙ্গ সংক্ষেপে উল্লেখ করুন। এগুলোকে সব ক্ষেত্রে বিনিময়যোগ্য বলবেন না।
- বিপরীতার্থক শব্দে কেবল প্রকৃত অর্থবৈপরীত্য থাকলে প্রচলিত বাংলা বিপরীত শব্দ দিন এবং কোন অর্থের বিপরীত তা জানান। নির্ভরযোগ্য বিপরীত না থাকলে “প্রচলিত বিপরীতার্থক শব্দ নেই” বলুন; জোর করে জোড়া বানাবেন না।
- পদ প্রকরণে পদ/শব্দশ্রেণি ও বাক্যে ভূমিকা লিখুন।
- শেষে ক্রিয়া-ভিত্তিক ও বর্ণ-ভিত্তিক ব্যাখ্যা দিন, তবে এগুলিকে প্রতিষ্ঠিত ব্যুৎপত্তির বিকল্প বলে দাবি করবেন না। সূত্রে সমর্থন না থাকলে তা ব্যাখ্যামূলক অনুমান হিসেবে চিহ্নিত করুন।
- কোনো নির্দিষ্ট লেখক, অভিধান বা ব্যক্তির নাম/পদ্ধতির নামে উত্তর দেবেন না; ব্যাখ্যাটি নিজস্ব ও সূত্রনির্ভর রাখুন।
- শুধু JSON ফেরত দিন। প্রতিটি ঘরে তথ্য না থাকলে সংক্ষেপে কী জানা যায়নি বলুন।"""

def analyze(word: str):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception as exc:
        raise RuntimeError(
            "অ্যাপের মালিককে Streamlit settings → Secrets-এ GEMINI_API_KEY যোগ করতে হবে।"
        ) from exc

    payload = {
        "model": MODEL,
        "input": build_prompt(word),
        "tools": [{"type": "google_search"}],
        "generation_config": {"thinking_level": "low"},
        "response_format": {"type": "text", "mime_type": "application/json", "schema": SCHEMA},
    }
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
            json=payload,
            timeout=120,
        )
    except requests.RequestException as exc:
        raise RuntimeError("Google API-তে সংযোগ করা যায়নি। ইন্টারনেট সংযোগ পরীক্ষা করে আবার চেষ্টা করুন।") from exc

    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("Google API থেকে সঠিক উত্তর পাওয়া যায়নি।") from exc
    if not response.ok:
        error = result.get("error", {})
        message = error.get("message") if isinstance(error, dict) else str(error)
        raise RuntimeError(message or f"Gemini request failed ({response.status_code})")

    output_text = ""
    sources = []
    for step in result.get("steps", []):
        if step.get("type") != "model_output":
            continue
        for block in step.get("content", []):
            if block.get("type") != "text":
                continue
            output_text += block.get("text", "")
            for annotation in block.get("annotations", []):
                url = annotation.get("url")
                if annotation.get("type") == "url_citation" and isinstance(url, str):
                    title = annotation.get("title")
                    sources.append({
                        "url": url,
                        "title": title if isinstance(title, str) and title else urlparse(url).netloc,
                    })

    if not output_text:
        output_text = "".join(
            item.get("text", "") for item in result.get("outputs", [])
            if item.get("type") == "text"
        ) or result.get("output_text", "")
    output_text = output_text.strip()
    if output_text.startswith("```"):
        output_text = output_text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        data = json.loads(output_text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("বিশ্লেষণের JSON পড়া যায়নি। আবার চেষ্টা করুন।") from exc

    unique_sources = {source["url"]: source for source in sources}
    return data, list(unique_sources.values())

with st.form("word-search", clear_on_submit=False):
    word = st.text_input("বাংলা শব্দ", placeholder="একটি বাংলা শব্দ লিখুন…", max_chars=80)
    submitted = st.form_submit_button("বিশ্লেষণ  →", type="primary", use_container_width=True)

if submitted:
    if not word.strip():
        st.warning("একটি বাংলা শব্দ লিখুন।")
    else:
        with st.spinner("ওয়েব সূত্র খোঁজা ও বিশ্লেষণ চলছে…"):
            try:
                st.session_state["word_analysis"] = analyze(word.strip())
                st.session_state.pop("analysis_error", None)
            except RuntimeError as exc:
                st.session_state.pop("word_analysis", None)
                st.session_state["analysis_error"] = str(exc)

if st.session_state.get("analysis_error"):
    st.error(st.session_state["analysis_error"])

if st.session_state.get("word_analysis"):
    data, sources = st.session_state["word_analysis"]
    st.divider()
    st.title(data.get("word") or word)
    st.caption("ওয়েব-সূত্রভিত্তিক বিশ্লেষণ  ·  " + (data.get("pronunciation") or "উচ্চারণ অনির্দিষ্ট"))

    for start in range(0, len(FIELDS), 2):
        columns = st.columns(2)
        for column, (key, label) in zip(columns, FIELDS[start:start + 2]):
            with column:
                with st.container(border=True):
                    st.markdown(f"**{label}**")
                    st.write(data.get(key) or "প্রযোজ্য নয় / নির্ভরযোগ্য তথ্য পাওয়া যায়নি।")

    st.subheader("ওয়েবে ব্যবহৃত সূত্র")
    if sources:
        for source in sources:
            url = source["url"]
            if urlparse(url).scheme in ("https", "http"):
                st.caption(source["title"])
                st.link_button("সূত্র খুলুন", url)
        st.caption("সূত্রগুলো অনুসন্ধান-উত্তরের ভিত্তি। ব্যুৎপত্তি ও ব্যাকরণগত বিশ্লেষণ প্রয়োজনে মূল সূত্রে মিলিয়ে নিন।")
    else:
        st.caption("এই অনুরোধে Google Search citation দেয়নি। ব্যুৎপত্তি-সংক্রান্ত দাবিগুলো যাচাই করে নিন।")
