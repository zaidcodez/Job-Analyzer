# 🚀 Job Intelligence Scraper – Setup Guide

This guide explains how to run the system locally.

---

## 🧩 1. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

## ⚙️ 2. Start Backend Server

Run the FastAPI backend:

```bash
uvicorn backend.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

## 📊 3. Start Dashboard (Streamlit UI)

In a new terminal:

```bash
streamlit run dashboard/app.py
```

## 🌐 4. Load Chrome Extension

1. Open Chrome and go to `chrome://extensions`
2. Enable **Developer Mode** (top right)
3. Click **Load unpacked**
4. Select the `extension/` folder from this project

## 🔎 5. Collect Job Listings

1. Go to a job listing website (Rozee / Indeed / Mustakbil)
2. Open any job listings page (not login/home page)
3. Click the extension icon
4. Click **"Collect Visible Listings"**

## 📡 6. Send Data to Backend

After collecting jobs:

- Click **"Send Saved Jobs to Local Backend"**

This stores jobs into the database and triggers AI analysis.