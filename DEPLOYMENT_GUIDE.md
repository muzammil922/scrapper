# 🚀 Deployment Guide - Local vs Vercel

## 📊 Comparison

| Feature | Local Version | Vercel Version |
|---------|--------------|----------------|
| **Browser Automation** | ✅ Selenium | ❌ Not supported |
| **Wikipedia** | ✅ Yes | ✅ Yes (API) |
| **YouTube** | ✅ Selenium | ✅ API (key needed) |
| **Google Search** | ✅ Selenium | ✅ API (key needed) |
| **PDF Export** | ✅ Yes | ❌ Not in API |
| **Auto-Update** | ✅ Yes | ❌ Serverless timeout |
| **File Storage** | ✅ Yes | ❌ No persistent storage |
| **Long Tasks** | ✅ Yes | ❌ 30s timeout |
| **Cost** | Free (local) | Free tier available |

---

## 🏠 Local Version (Recommended for Full Features)

**Best for:**
- Full scraping capabilities
- PDF export
- Auto-update mode
- File downloads
- No API keys needed (for Wikipedia/Google basic search)

**Run:**
```bash
python smart_scraper.py
```

**Features:**
- ✅ All scrapers work
- ✅ PDF reports
- ✅ CSV/Excel/JSON export
- ✅ Auto-update mode
- ✅ Smart category scraper
- ✅ No restrictions

---

## ☁️ Vercel Version (API Only)

**Best for:**
- API endpoints
- Serverless deployment
- Simple scraping requests
- Integration with other apps

**Deploy:**
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel
```

**API Endpoints:**
- `GET /api/health` - Health check
- `POST /api/scrape/wikipedia` - Wikipedia (no key)
- `POST /api/scrape/youtube-api` - YouTube (key needed)
- `POST /api/scrape/google-api` - Google (key needed)
- `POST /api/scrape` - Universal endpoint

**Required:**
- YouTube API key (optional, for YouTube)
- Google API key (optional, for Google Search)

**Limitations:**
- ❌ No browser automation
- ❌ No PDF export
- ❌ 30-second timeout
- ❌ No file storage
- ❌ No auto-update

---

## 🔧 What Was Changed for Vercel

### Removed:
- ❌ `selenium` package
- ❌ `undetected-chromedriver`
- ❌ `playwright`
- ❌ `webdriver-manager`
- ❌ Browser automation code
- ❌ File-based scrapers

### Added:
- ✅ Flask API (`api/index.py`)
- ✅ API-based scraping
- ✅ Serverless-friendly endpoints
- ✅ Vercel configuration (`vercel.json`)

---

## 💡 Recommendations

### Use Local Version If:
- You want full features
- You need PDF export
- You want auto-update
- You don't have API keys
- You want to scrape without limits

### Use Vercel Version If:
- You need API endpoints
- You want serverless deployment
- You have API keys
- You just need simple scraping
- You're building an API service

---

## 🎯 Quick Start

### Local (Full Features):
```bash
pip install -r requirements.txt
python smart_scraper.py
```

### Vercel (API):
```bash
# Deploy
vercel

# Use API
curl -X POST https://your-app.vercel.app/api/scrape/wikipedia \
  -H "Content-Type: application/json" \
  -d '{"query": "python", "max_results": 5}'
```

---

**For most users, LOCAL VERSION is better!**
**Use Vercel only if you specifically need API endpoints.**

