# Network Lookup Tools

A locally-hosted Flask web app with three side-by-side lookup tools:
- **Area Code Lookup** — US & Canada area codes
- **Domain WHOIS** — registrar and registration date
- **IP Geolocation** — city, region, country, ISP, and coordinates

---

## Requirements

- Python 3 (comes pre-installed on Mac)
- pip3

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/flygirlmicha/areacodeapp.git
cd areacodeapp
```

### 2. (Recommended) Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip3 install -r requirements.txt
```

---

## Running the App

```
python3 app.py
```

Then open your browser and go to:

```
http://localhost:5000
```

To stop the server, press `Control + C` in Terminal.

---

## Optional: Create a shortcut to start the app

Add an alias to your shell so you can start the app by typing `areacode` in any Terminal window:

```
echo 'alias areacode="python3 ~/areacodeapp/app.py"' >> ~/.zshrc && source ~/.zshrc
```

Adjust the path if you cloned the repo to a different location.

---

## Dependencies

| Package | Purpose |
|---|---|
| flask | Web framework |
| python-whois | Domain WHOIS lookups |
| requests | IP geolocation API calls |
| gunicorn | Production web server (for deployment) |
