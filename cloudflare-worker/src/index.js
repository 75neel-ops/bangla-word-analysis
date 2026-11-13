const MODEL = "gemini-3.8-flash";
const MAX_WORD_LENGTH = 80;

const schema = {
  type: "object",
  properties: {
    word: { type: "string" }, pronunciation: { type: "string" },
    letter_analysis: { type: "string" }, prakriti: { type: "string" },
    prefix: { type: "string" }, suffix: { type: "string" }, anusarga: { type: "string" },
    formation_analysis: { type: "string" }, origin_analysis: { type: "string" },
    semantic_analysis: { type: "string" }, synonyms: { type: "string" },
    antonyms: { type: "string" }, sandhi_analysis: { type: "string" },
    part_of_speech: { type: "string" }, syntax_analysis: { type: "string" },
    action_based_meaning: { type: "string" }, letter_based_meaning: { type: "string" },
    reliability_note: { type: "string" }
  },
  required: [
    "word", "pronunciation", "letter_analysis", "prakriti", "prefix", "suffix",
    "anusarga", "formation_analysis", "origin_analysis", "semantic_analysis",
    "synonyms", "antonyms", "sandhi_analysis", "part_of_speech", "syntax_analysis",
    "action_based_meaning", "letter_based_meaning", "reliability_note"
  ]
};

function jsonResponse(data, status, origin, allowed) {
  const headers = { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" };
  if (origin && allowed) {
    headers["Access-Control-Allow-Origin"] = origin;
    headers["Vary"] = "Origin";
    headers["Access-Control-Allow-Methods"] = "POST, OPTIONS";
    headers["Access-Control-Allow-Headers"] = "Content-Type";
    headers["Access-Control-Max-Age"] = "86400";
  }
  return new Response(JSON.stringify(data), { status, headers });
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowedOrigins = (env.ALLOWED_ORIGINS || "").split(",").map((value) => value.trim()).filter(Boolean);
    const allowed = allowedOrigins.includes(origin);

    if (request.method === "OPTIONS") {
      if (!allowed) return jsonResponse({ error: "Origin not allowed." }, 403, origin, false);
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": origin,
          "Vary": "Origin",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
          "Access-Control-Max-Age": "86400"
        }
      });
    }
    if (new URL(request.url).pathname !== "/analyze") return jsonResponse({ error: "Not found." }, 404, origin, allowed);
    if (request.method !== "POST") return jsonResponse({ error: "Method not allowed." }, 405, origin, allowed);
    if (!allowed) return jsonResponse({ error: "This app origin is not configured for the API." }, 403, origin, false);
    if (!env.GEMINI_API_KEY) return jsonResponse({ error: "The publisher has not configured the Gemini API key." }, 503, origin, allowed);

    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const { success } = await env.ANALYZE_LIMITER.limit({ key: ip });
    if (!success) return jsonResponse({ error: "অনেকগুলো অনুসন্ধান হয়েছে। এক মিনিট পরে আবার চেষ্টা করুন।" }, 429, origin, allowed);

    const length = Number(request.headers.get("Content-Length") || 0);
    if (length > 2048) return jsonResponse({ error: "Request is too large." }, 413, origin, allowed);

    let word;
    try {
      const body = await request.json();
      word = typeof body.word === "string" ? body.word.trim() : "";
    } catch {
      return jsonResponse({ error: "Invalid JSON request." }, 400, origin, allowed);
    }
    if (!word || word.length > MAX_WORD_LENGTH) {
      return jsonResponse({ error: "একটি শব্দ লিখুন (সর্বোচ্চ ৮০ অক্ষর)।" }, 400, origin, allowed);
    }

    const prompt = `বাংলা শব্দ “${word}”-এর একটি স্বতন্ত্র, সূত্র-সমর্থিত ভাষাতাত্ত্বিক বিশ্লেষণ তৈরি করুন। Google Search ব্যবহার করে একাধিক নির্ভরযোগ্য বাংলা অভিধান, বাংলা একাডেমি/বিশ্ববিদ্যালয়/ভাষাবিজ্ঞান সূত্র যেখানে পাওয়া যায় যাচাই করুন। সব ব্যাখ্যা সহজ বাংলায় লিখুন এবং JSON schema-র প্রতিটি ঘর পূরণ করুন।
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
- শুধু JSON ফেরত দিন। প্রতিটি ঘরে তথ্য না থাকলে সংক্ষেপে কী জানা যায়নি বলুন।`;
    const body = {
      model: MODEL,
      input: prompt,
      tools: [{ type: "google_search" }],
      generation_config: { thinking_level: "low" },
      response_format: { type: "text", mime_type: "application/json", schema }
    };

    let upstream;
    try {
      upstream = await fetch("https://generativelanguage.googleapis.com/v1beta/interactions", {
        method: "POST",
        headers: { "Content-Type": "application/json", "x-goog-api-key": env.GEMINI_API_KEY },
        body: JSON.stringify(body)
      });
    } catch {
      return jsonResponse({ error: "Google API-তে সংযোগ করা যায়নি।" }, 502, origin, allowed);
    }
    const responseText = await upstream.text();
    return new Response(responseText, {
      status: upstream.status,
      headers: {
        "Content-Type": upstream.headers.get("Content-Type") || "application/json; charset=utf-8",
        "Cache-Control": "no-store",
        "Access-Control-Allow-Origin": origin,
        "Vary": "Origin"
      }
    });
  }
};
