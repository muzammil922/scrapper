# 🌍 Universal Global Data Scraper

**Scrape data for ANYTHING in the world!** This is a comprehensive, generic scraper that can collect data from multiple platforms for any category you want.

## ✨ Features

### 🎯 Universal & Generic
- **Scrape ANY category**: Songs, Movies, History, Religion, Knowledge, Science, Technology, and more!
- **Add your own categories**: Fully customizable configuration
- **Auto-filter adult content**: Built-in content filtering
- **Billions of data points**: Scalable to scrape massive amounts of data

### 📡 Multiple Platforms
- ✅ **YouTube** - Videos, music, channels, playlists
- ✅ **Wikipedia** - Articles, knowledge, history, facts
- ✅ **Google Search** - Web results, images, videos, news
- 🔄 **Spotify** - Songs, artists, albums (coming soon)
- 🔄 **IMDB** - Movies, TV shows, ratings (coming soon)
- 🔄 **Twitter/Reddit/TikTok** - Social media content (coming soon)

### 📊 Data Export
- CSV files
- Excel files (with category-wise sheets)
- JSON files (with metadata and statistics)

### 🛡️ Safety Features
- Auto-blocks adult/pornographic content
- Respects robots.txt
- Rate limiting to avoid being blocked
- Configurable delays between requests

## 🚀 Quick Start

### 1. Installation

```bash
# Install Python 3.8+
# Then install dependencies:
pip install -r requirements.txt
```

### 2. Run the Scraper

```bash
# Main universal scraper
python universal_main.py
```

You'll be prompted to:
- Choose which categories to scrape
- Select specific platforms
- Set limits

## 📁 Categories Included

### Music & Songs
- Urdu songs
- Hindi songs  
- English songs
- Music artists

### Movies & Entertainment
- Hollywood movies
- Bollywood movies
- Pakistani movies
- TV shows

### Knowledge & History
- World history
- Countries data
- World facts

### Religion & Spirituality
- Islamic knowledge
- Hindu knowledge
- Christian knowledge

### Science & Technology
- Science discoveries
- Technology innovations
- Educational videos

### And More!
- Astrology
- Health information
- Business/Companies

## ⚙️ Configuration

### Add Your Own Categories

Edit `generic_config.py`:

```python
GLOBAL_CATEGORIES = {
    "your_category": {
        "query": "your search query",
        "platforms": ["youtube", "wikipedia", "google"],
        "type": "your_type"
    }
}
```

### Enable/Disable Platforms

Edit `generic_config.py`:

```python
AVAILABLE_PLATFORMS = {
    "youtube": {
        "enabled": True,  # Set to False to disable
        "max_results": 100
    }
}
```

### Content Filtering

Adult content is automatically filtered. To adjust:

```python
CONTENT_FILTER = {
    "enabled": True,
    "block_adult": True,
    "exclude_keywords": ["porn", "xxx", "adult", ...]
}
```

## 📊 Output Files

After scraping, you'll get:

1. **universal_scraped_data.csv** - All data in CSV format
2. **universal_scraped_data.xlsx** - Excel with multiple sheets:
   - All Data sheet
   - Category-wise sheets
   - Platform-wise sheets
3. **universal_scraped_data.json** - JSON with metadata and statistics

## 📋 Data Fields Collected

Each record includes:
- Title/Name
- Category & Type
- Description/Content
- URL
- Platform/Source
- Author/Creator
- Views, Likes, Comments
- Published date
- Tags/Keywords
- And more!

## 🎯 Example Use Cases

### 1. Scrape Songs for Music App
```python
# Add to generic_config.py:
"songs_popular": {
    "query": "popular songs 2024",
    "platforms": ["youtube", "spotify"],
    "type": "music"
}
```

### 2. Scrape Educational Content
```python
"python_tutorials": {
    "query": "python programming tutorials",
    "platforms": ["youtube", "wikipedia"],
    "type": "education"
}
```

### 3. Scrape Religious Content
```python
"quran_recitations": {
    "query": "quran recitation beautiful",
    "platforms": ["youtube", "google"],
    "type": "religion"
}
```

## ⚠️ Important Notes

### Legal & Ethical
- ✅ Scrapes only **public** data
- ✅ Respects robots.txt
- ✅ Includes delays between requests
- ✅ Auto-filters inappropriate content

### Performance
- Scraping takes time - be patient!
- Each category scrapes from multiple platforms
- Progress is shown in real-time
- Can resume/interrupt and continue

### Rate Limiting
- Default: 2 seconds between requests
- Adjust in `generic_config.py` if needed
- Too fast = may get blocked

## 🛠️ Troubleshooting

### Chrome Driver Issues
```bash
# The scraper uses undetected-chromedriver
# It should auto-install, but if issues:
pip install --upgrade undetected-chromedriver
```

### No Results
- Check internet connection
- Some sites may block automated access
- Try reducing max_results in config
- Run with `headless=False` to see what's happening

### Slow Performance
- Normal! Scraping visits multiple sources
- Reduce number of categories
- Reduce max_results per category
- Use fewer platforms per category

## 📈 Statistics

After scraping, you'll see:
- Total records scraped
- Breakdown by platform
- Breakdown by category
- Breakdown by type
- Average records per minute

## 🔧 Advanced Usage

### Scrape Specific Platforms Only

Edit `generic_config.py`:
```python
"songs_urdu": {
    "query": "urdu songs",
    "platforms": ["youtube"],  # Only YouTube
    "type": "music"
}
```

### Increase/Decrease Results

Edit `generic_config.py`:
```python
SCRAPER_SETTINGS = {
    "max_results_per_category": 200,  # Increase for more data
    "max_results_per_platform": 200
}
```

### Export Only Specific Formats

Edit `generic_config.py`:
```python
SCRAPER_SETTINGS = {
    "output_format": ["csv"],  # Only CSV, no Excel/JSON
}
```

## 🌟 Pro Tips

1. **Start Small**: Test with 1-2 categories first
2. **Monitor Progress**: Watch the console output
3. **Check Output**: Verify data quality in CSV/Excel
4. **Customize**: Add your own categories as needed
5. **Backup**: Save important data regularly

## 📞 Support

For issues:
1. Check all dependencies are installed
2. Verify Chrome browser is installed
3. Check internet connection
4. Review error messages in console

## 📝 License

This project is for educational/research purposes. Always respect website terms of service and robots.txt files.

---

**Happy Scraping! 🚀**

*Scrape the world's data, category by category!*

