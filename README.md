# Kalim Khan Digital Dictionary

A static, responsive single page app and installable PWA. Serve this folder from localhost or HTTPS (service workers do not work from `file://`). For a quick local preview, run `python -m http.server 8000` from this folder and open `http://localhost:8000`.

## Getting started

1. Open the app and add the two PDF volumes with **PDF যোগ করুন**. The PDFs are read in your browser and are not copied to a server.
2. Add a Gemini API key. It is stored in this browser's local storage and sent directly to Google's Gemini API when you search.
3. Review **পৃষ্ঠা সূচি দেখুন / সম্পাদনা করুন**. The included `index.json` contains broad starter ranges, not an exact word index. Set each Bengali initial to the part and page range in your edition, then apply it. You can also download the updated JSON.
4. Search a word. The app renders the routed PDF page, sends its image and the word to `gemini-2.5-flash`, and displays the extracted entry. The scan can be expanded under the result.
5. Switch to **Web Dictionary Search** to ask Gemini for a standard dictionary style definition.

The initial PDF page numbers and part assignments are only starter values because a verified per-letter index was not supplied. Confirm them against the printed contents/index in your copies. Sample offline entries demonstrate the interface before PDFs or a key are added.

## Publish it with GitHub Pages

1. On GitHub, create a repository such as `kalim-khan-digital-dictionary`. Choose **Public** if you want the free GitHub Pages site to be publicly accessible.
2. In the new repository, choose **Add file → Upload files**. Drag in the *contents* of this `outputs` folder (including `index.html`, `manifest.json`, `sw.js`, `index.json`, and the icons), then commit to `main`. Do not upload your PDFs or API key.
3. Open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select `main` and `/(root)`, then save.
4. Wait for the Pages deployment, then open the URL shown on the Pages settings screen. It is typically `https://ACCOUNT.github.io/REPOSITORY/`.

The app uses relative paths and works from the repository subpath.

## Install it as an app

The deployed site is an installable PWA (web app) for desktop and mobile; it is not a separately packaged Windows `.exe` or Play Store / App Store binary.

- **Windows / macOS / Linux:** open the HTTPS site in Chrome or Edge. Use the install icon in the address bar, or the browser menu's **Install page as app** option.
- **Android:** open the HTTPS site in Chrome, tap the menu, then **Install app** (or **Add to Home screen**).
- **iPhone / iPad:** open the HTTPS site in Safari, tap **Share → Add to Home Screen**, then enable **Open as Web App** if shown.

The service worker caches the app shell, manifest and index; Gemini requests need a network connection. The PDF.js viewer is loaded from a CDN, so scan viewing also needs that library to be available. User PDFs and the API key are not part of the app cache.

This is a static client-side demo, not a secure multi-user API service. A key entered in the browser is visible to that browser and used in direct API requests. For a public deployment, put Gemini calls behind a server you control and protect the key there.

## Files

- `index.html` - UI, PDF.js integration, Gemini calls, and local settings.
- `index.json` - editable Bengali-letter to PDF-page routing map.
- `manifest.json`, `sw.js`, `icon.svg` - install and offline shell support.
