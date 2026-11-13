# বাংলা শব্দ বিশ্লেষণ

ওয়েব-সূত্রভিত্তিক বাংলা শব্দ বিশ্লেষণের Streamlit app। বর্ণ, প্রকৃতি/মূল, উপসর্গ, প্রত্যয়, উৎপত্তি, অর্থ, প্রসঙ্গভিত্তিক সমার্থক ও বিপরীতার্থক শব্দ, সন্ধি, পদ-প্রকরণ এবং ব্যাখ্যার নির্ভরযোগ্যতার সীমা দেখায়।

## Streamlit-এ প্রকাশ (shared API key)

এই সংস্করণে Gemini অনুরোধ Python/Streamlit server থেকে যায়। খেলোয়াড়ের browser-এ API key পাঠানো হয় না।

1. Streamlit Community Cloud-এ Create app বেছে এই repository, main branch, এবং streamlit_app.py entrypoint নির্বাচন করুন.
2. Deploy করার সময় Advanced settings → Secrets-এ নিজের key দিয়ে এই TOML যোগ করুন:

   GEMINI_API_KEY = "your-gemini-api-key"

3. Deploy করুন। পরে key পরিবর্তন করতে app-এর Settings → Secrets-এ যান.

Streamlit Secrets স্থানীয়ভাবে .streamlit/secrets.toml থেকে পড়া যায়; প্রকৃত secrets ফাইলটি .gitignore-এ আছে। Repository-তে শুধু .streamlit/secrets.toml.example নমুনা রাখা হয়েছে. [Streamlit Secrets guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

## itch.io

Streamlit app-এর public URL-টি itch.io project description-এ দিন. Streamlit public apps support iframe embedding with ?embed=true; itch.io game page-এ সেটি কাজ করে কি না upload-এর পরে যাচাই করুন. itch.io HTML game embed নিজেই iframe ব্যবহার করে, তাই সবচেয়ে নির্ভরযোগ্য fallback হলো Streamlit app-টি নতুন tab-এ খোলার link দেওয়া.

Streamlit Community Cloud app-টি public হলে URL-টি যে কেউ খুলতে পারে; itch.io purchase নিজে Streamlit app-এ access control যোগ করে না. Shared Gemini key-র ব্যবহারের Google AI project quota/billing limit সেট করুন.

## Local development

1. Python environment-এ pip install -r requirements.txt চালান.
2. .streamlit/secrets.toml.example-এর অনুরূপ .streamlit/secrets.toml তৈরি করে key দিন.
3. streamlit run streamlit_app.py চালান.

## Static preview

Root-এর index.html পুরোনো static preview হিসেবে রাখা আছে। সেটি browser থেকে সরাসরি Google-এ request করে এবং প্রত্যেক user-এর নিজস্ব API key চায়. Shared publisher key ও itch.io release-এর জন্য Streamlit app deploy করুন.

অ্যাপটি Google Interactions API-তে gemini-3.8-flash ও Google Search grounding ব্যবহার করে। ব্যুৎপত্তি বা ভাষাতাত্ত্বিক বিশ্লেষণ প্রকাশের আগে সূত্রে যাচাই করুন.

Created & Maintained by NilanjanC