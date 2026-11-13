# বাংলা শব্দ বিশ্লেষণ

ওয়েব-সূত্রভিত্তিক বাংলা শব্দ বিশ্লেষণের একটি responsive single-page app ও installable PWA। শব্দের বর্ণ, প্রকৃতি/মূল, উপসর্গ, প্রত্যয়, অনুসর্গ, উৎপত্তি, অর্থ, প্রসঙ্গভিত্তিক সমার্থক ও বিপরীতার্থক শব্দ, সন্ধি, পদ-প্রকরণ এবং ক্রিয়া-ভিত্তিক ও বর্ণ-ভিত্তিক ব্যাখ্যা দেখায়। কোনো বিশ্লেষণ প্রযোজ্য না হলে বা সূত্রে নিশ্চিত না হলে সেটি স্পষ্ট করে।

## ব্যবহার

1. HTTPS-এ প্রকাশিত অ্যাপ খুলুন অথবা স্থানীয় preview-এর জন্য এই ফোল্ডার থেকে `python -m http.server 8000` চালিয়ে `http://localhost:8000` খুলুন।
2. Gemini API key লিখুন ও সংরক্ষণ করুন। key শুধু ওই browser-এর local storage-এ থাকে; অনুরোধে সরাসরি Google-এ পাঠানো হয়। অন্য ব্যবহারকারীর key আপনার সঙ্গে ভাগ হয় না।
3. একটি বাংলা শব্দ লিখে অনুসন্ধান করুন। অ্যাপ Gemini Search grounding দিয়ে ওয়েবের সূত্র খোঁজে এবং পাওয়া citation-গুলো দেখায়।

অ্যাপটি Google Interactions API-তে `gemini-3.8-flash` ও Google Search grounding ব্যবহার করে। এটি নির্ভরযোগ্য সূত্র দেখানোর চেষ্টা করে, কিন্তু ব্যুৎপত্তি বা ভাষাতাত্ত্বিক বিশ্লেষণ প্রকাশের আগে উৎসে যাচাই করা উচিত। API key কখনও public GitHub repository-তে যোগ করবেন না।

GitHub Pages-এ প্রকাশ করতে `index.html`, `manifest.json`, `sw.js`, এবং icon ফাইলগুলো repository root-এ রাখুন; Settings → Pages-এ `main` branch ও `/(root)` বেছে নিন। Service worker/PWA HTTPS বা localhost-এ কাজ করে, `file://` থেকে নয়।


## itch.io-তে API key গোপন রাখা

itch.io build-এ সরাসরি Gemini API key রাখবেন না। HTML/JavaScript থেকে খেলোয়াড়রা সেটি বের করতে পারে। এই repository-তে থাকা Cloudflare Worker-টি server-side proxy হিসেবে ব্যবহার করুন; key Cloudflare-এর encrypted Worker Secret-এ থাকবে। Worker-এ প্রতি IP-তে ৮টি বিশ্লেষণ/মিনিটের আনুমানিক rate limit আছে। এটি abuse কমায়, তবে global spend cap নয়; Google AI project-এর quota/billing limit-ও নির্ধারণ করুন।

একবার publisher হিসেবে সেটআপ করুন:

1. Cloudflare account-এ Worker deploy করুন: cloudflare-worker ফোল্ডারে গিয়ে npx wrangler login চালান, তারপর npx wrangler secret put GEMINI_API_KEY দিয়ে Gemini key দিন এবং npx wrangler deploy চালান।
2. cloudflare-worker/wrangler.toml-এর ALLOWED_ORIGINS-এ আপনার itch.io game-এর origin যোগ করুন। itch.io iframe-এর জন্য https://html-classic.itch.zone এবং আপনার game page-এর origin, যেমন https://75neel-ops.itch.io, রাখুন। নিজের game URL অনুযায়ী মানটি বদলান।
3. Deploy শেষে Wrangler যে workers.dev URL দেখায়, সেটি api-config.js-এর BWA_API_ENDPOINT-এ বসান।
4. index.html এবং api-config.js-সহ game files itch.io-তে upload করুন। Endpoint সেট থাকলে API key field লুকানো থাকবে; খেলোয়াড়দের কোনো key লিখতে হবে না।

নিজের GitHub Pages preview-তে endpoint ফাঁকা রাখলে আগের ব্যক্তিগত API key mode চালু থাকবে। Worker source বা api-config.js-এ কখনও Gemini key লিখবেন না। Cloudflare Secrets key-টিকে server-side রাখে: https://developers.cloudflare.com/workers/configuration/secrets/ . Rate limit-এর সীমাবদ্ধতা: https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/ .

Created & Maintained by NilanjanC

