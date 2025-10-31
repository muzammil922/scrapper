# 🚀 Vercel Deployment Guide

## ⚠️ Important Changes for Vercel

**Vercel par ye changes kiye gaye hain:**

### ❌ Removed (Vercel par nahi chalta):
- ❌ Selenium (Chrome browser automation)
- ❌ undetected-chromedriver
- ❌ playwright
- ❌ webdriver-manager
- ❌ Long-running processes
- ❌ File-based scraping with browser

### ✅ Added (Vercel-compatible):
- ✅ Flask API (serverless-friendly)
- ✅ Wikipedia scraper (pure requests)
- ✅ YouTube Data API v3
- ✅ Google Custom Search API
- ✅ RESTful endpoints

---

## 📋 Deployment Steps

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
vercel
```

### 4. Set Environment Variables (Important!)

Vercel dashboard me jao aur ye variables add karo:

**Required (at least one):**
- `YOUTUBE_API_KEY` - YouTube Data API v3 key
- `GOOGLE_API_KEY` - Google Custom Search API key
- `GOOGLE_SEARCH_ENGINE_ID` - Custom Search Engine ID

**How to get API keys:**
- **YouTube**: https://console.cloud.google.com/apis/library/youtube.googleapis.com
- **Google Search**: https://programmablesearchengine.google.com/

### 5. Update Dependencies

Vercel automatically uses `requirements.txt`, but make sure it has:
- flask
- flask-cors
- requests
- beautifulsoup4
- (No Selenium!)

---

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### Scrape Wikipedia (No API key needed)
```bash
POST /api/scrape/wikipedia
{
  "query": "python programming",
  "max_results": 10
}
```

### Scrape YouTube (Requires API key)
```bash
POST /api/scrape/youtube-api
{
  "query": "pakistani songs",
  "max_results": 10
}
```

### Scrape Google (Requires API key)
```bash
POST /api/scrape/google-api
{
  "query": "web scraping",
  "max_results": 10
}
```

### Universal Scrape
```bash
POST /api/scrape
{
  "query": "python tutorials",
  "platforms": ["wikipedia", "youtube", "google"],
  "max_results": 10,
  "category": "education"
}
```

---

## 🎯 Local Testing

```bash
# Install Vercel-compatible requirements
pip install -r vercel_requirements.txt

# Run API locally
cd api
python index.py
```

Test endpoints:
```bash
curl http://localhost:5000/api/health
curl -X POST http://localhost:5000/api/scrape/wikipedia \
  -H "Content-Type: application/json" \
  -d '{"query": "python", "max_results": 5}'
```

---

## 📝 Notes

1. **Selenium removed**: Vercel serverless functions me Chrome browser nahi chal sakta
2. **API-based scraping**: Ab APIs use hote hain (YouTube Data API, Google Custom Search)
3. **Wikipedia works**: Wikipedia scraper bina API key ke kaam karta hai
4. **Timeout limit**: Vercel functions 30 seconds tak chali sakti hain (maxDuration: 30)
5. **No file storage**: Vercel me permanent file storage nahi hota

---

## 🔄 Local vs Vercel

**Local Version** (Full features):
- ✅ Selenium scraping
- ✅ Browser automation
- ✅ File downloads
- ✅ PDF export
- ✅ Auto-update mode
- ✅ All platforms

**Vercel Version** (API only):
- ✅ REST API
- ✅ Wikipedia scraping (no API key)
- ✅ YouTube (with API key)
- ✅ Google Search (with API key)
- ❌ No browser automation
- ❌ No file storage
- ❌ No long-running tasks

---

## 💡 Recommendation

**For full features (Selenium, PDF, etc.):**
- Use local version: `python smart_scraper.py`
- Or deploy on: Railway, Render, DigitalOcean (not Vercel)

**For API-only scraping:**
- Deploy on Vercel
- Use API endpoints
- Get YouTube/Google API keys

---

## 🐛 Troubleshooting

**"Module not found" error:**
- Make sure `vercel_requirements.txt` has all needed packages
- Or update `requirements.txt` to remove Selenium packages

**"API key required" error:**
- Set environment variables in Vercel dashboard
- Restart deployment after adding env vars

**Timeout errors:**
- Reduce `max_results` parameter
- Vercel has 30-second timeout limit

---

## ✅ Quick Deploy Checklist

- [ ] Install Vercel CLI
- [ ] Run `vercel login`
- [ ] Set API keys in Vercel dashboard:
  - [ ] YOUTUBE_API_KEY (optional)
  - [ ] GOOGLE_API_KEY (optional)
  - [ ] GOOGLE_SEARCH_ENGINE_ID (optional)
- [ ] Run `vercel`
- [ ] Test API endpoints
- [ ] Done! 🎉

---

**Local version (full features) ke liye:**
```bash
python smart_scraper.py
```

**Vercel API version ke liye:**
- Deploy to Vercel
- Use REST endpoints
- Get API keys

