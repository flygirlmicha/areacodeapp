# Network Lookup Tools

A Flask web app with three side-by-side lookup tools and a companion Chrome extension. Built for use during investigations where you need quick lookups without switching between multiple websites.

---

## What Was Built

### Phase 1 — Area Code Lookup (Local Flask App)
Started as a simple Flask web app running locally on a Mac. The user enters a 3-digit area code and gets back the city or region it serves. The app includes an embedded dictionary of 330+ US and Canada area codes — no external API needed.

**Files created:**
- `app.py` — Flask app with the area code dictionary and route
- `templates/index.html` — Simple HTML form with result display
- `requirements.txt` — Dependency list

### Phase 2 — WHOIS and IP Geolocation Added
Two additional lookup tools were added to the same page:
- **Domain WHOIS** — enter a domain like `google.com` and get back the registrar and the date it was registered. Uses the `python-whois` library.
- **IP Geolocation** — enter an IP address like `8.8.8.8` and get back the city, region, country, ISP, organization, and coordinates. Uses the free `ip-api.com` API (no API key required).

### Phase 3 — Side-by-Side Layout
The three tools were redesigned into a single page with three panels displayed side by side. Each panel has its own independent search form. On narrow screens (mobile) the panels stack vertically.

### Phase 4 — Persistent Results Across Searches
Flask sessions were added so that searching in one panel does not clear the results in the other two. This allows all three panels to show results simultaneously during an investigation. A **Clear All Results** button was added to reset everything between investigations.

### Phase 5 — Deployed Publicly to cPanel
The app was deployed to `http://tools.spamuraiwarrior.com` via cPanel's Python App (Passenger/WSGI). Key steps involved:
- Creating a `passenger_wsgi.py` file to connect Apache to Flask
- Creating a `.htaccess` file with Passenger configuration
- Installing dependencies into the cPanel virtual environment
- Creating a `static/favicon.ico` to fix 500 errors on favicon requests
- Using `touch tmp/restart.txt` to restart the app after changes

To update the live server after any code change:
```
cd /home/aixtou0mky78/areacodeapp && git pull && touch tmp/restart.txt
```

### Phase 6 — Chrome Extension
A Chrome extension was built that calls the live Flask app as a backend API. The extension popup mirrors the three-panel layout of the web app.

**Extension files:**
- `extension/manifest.json` — Chrome extension configuration (Manifest V3)
- `extension/popup.html` — The popup UI with three search panels
- `extension/popup.js` — Handles lookups by calling `POST /` on the Flask app with an `X-Requested-With: XMLHttpRequest` header, which triggers a JSON response instead of HTML
- `extension/background.js` — Registers right-click context menu items
- `extension/icon.png` — Extension icon (blue circle)

**Key technical detail:** The `/api` route was unreachable through Apache/Passenger on cPanel shared hosting. The fix was to detect `X-Requested-With: XMLHttpRequest` in the existing `POST /` route and return JSON when that header is present, bypassing the need for a separate `/api` route entirely.

### Phase 7 — Right-Click Context Menu
The Chrome extension was extended with a right-click context menu. Highlighting any text on a webpage and right-clicking shows three options:
- Lookup Area Code
- Lookup Domain WHOIS
- Lookup IP Geolocation

Clicking a menu item opens the extension popup with the selected text pre-filled and the lookup already run.

---

## Project Structure

```
areacodeapp/
├── app.py                  # Flask app — all routes and area code data
├── requirements.txt        # Python dependencies
├── Procfile                # Gunicorn startup command (for deployment)
├── passenger_wsgi.py       # cPanel/Passenger WSGI entry point
├── templates/
│   └── index.html          # Main page with three lookup panels
├── static/
│   └── favicon.ico         # Site favicon
└── extension/
    ├── manifest.json        # Chrome extension manifest (V3)
    ├── popup.html           # Extension popup UI
    ├── popup.js             # Extension lookup logic
    ├── background.js        # Context menu registration and handling
    └── icon.png             # Extension icon
```

---

## Dependencies

| Package | Purpose |
|---|---|
| flask | Web framework |
| python-whois | Domain WHOIS lookups |
| requests | IP geolocation API calls (ip-api.com) |
| gunicorn | Production web server |

---

## Installation (Local Mac)

### 1. Clone the repository
```
git clone https://github.com/flygirlmicha/areacodeapp.git
cd areacodeapp
```

### 2. Create a virtual environment (recommended)
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip3 install -r requirements.txt
```

### 4. Run the app
```
python3 app.py
```

Open your browser and go to `http://localhost:5000`. To stop, press `Control + C`.

### Optional: Terminal shortcut
```
echo 'alias areacode="python3 ~/areacodeapp/app.py"' >> ~/.zshrc && source ~/.zshrc
```

After this you can start the app by just typing `areacode` in any Terminal window.

---

## Installing the Chrome Extension

1. Go to `chrome://extensions` in Chrome
2. Enable **Developer mode** (toggle top right)
3. Click **Load unpacked**
4. Select the `extension/` folder from this repo
5. The Network Lookup Tools icon will appear in your Chrome toolbar

---

## Deploying Updates to cPanel

After making changes locally, push to GitHub and then on the server run:
```
cd /home/aixtou0mky78/areacodeapp && git pull && touch tmp/restart.txt
```

---

## Live URL

`http://tools.spamuraiwarrior.com`
