# বাংলা শব্দ বিশ্লেষণ

ওয়েব-সূত্রভিত্তিক বাংলা শব্দ বিশ্লেষণের একটি responsive single-page app ও installable PWA। শব্দের বর্ণ, প্রকৃতি/মূল, উপসর্গ, প্রত্যয়, অনুসর্গ, উৎপত্তি, অর্থ, সন্ধি, পদ-প্রকরণ এবং ক্রিয়া-ভিত্তিক ও বর্ণ-ভিত্তিক ব্যাখ্যা দেখায়। কোনো বিশ্লেষণ প্রযোজ্য না হলে বা সূত্রে নিশ্চিত না হলে সেটি স্পষ্ট করে।

## ব্যবহার

1. HTTPS-এ প্রকাশিত অ্যাপ খুলুন অথবা স্থানীয় preview-এর জন্য এই ফোল্ডার থেকে `python -m http.server 8000` চালিয়ে `http://localhost:8000` খুলুন।
2. Gemini API key লিখুন ও সংরক্ষণ করুন। key শুধু ওই browser-এর local storage-এ থাকে; অনুরোধে সরাসরি Google-এ পাঠানো হয়। অন্য ব্যবহারকারীর key আপনার সঙ্গে ভাগ হয় না।
3. একটি বাংলা শব্দ লিখে অনুসন্ধান করুন। অ্যাপ Gemini Search grounding দিয়ে ওয়েবের সূত্র খোঁজে এবং পাওয়া citation-গুলো দেখায়।

অ্যাপটি Google Interactions API-তে `gemini-3.8-flash` ও Google Search grounding ব্যবহার করে। এটি নির্ভরযোগ্য সূত্র দেখানোর চেষ্টা করে, কিন্তু ব্যুৎপত্তি বা ভাষাতাত্ত্বিক বিশ্লেষণ প্রকাশের আগে উৎসে যাচাই করা উচিত। API key কখনও public GitHub repository-তে যোগ করবেন না।

GitHub Pages-এ প্রকাশ করতে `index.html`, `manifest.json`, `sw.js`, এবং icon ফাইলগুলো repository root-এ রাখুন; Settings → Pages-এ `main` branch ও `/(root)` বেছে নিন। Service worker/PWA HTTPS বা localhost-এ কাজ করে, `file://` থেকে নয়।

Created & Maintained by NilanjanC

