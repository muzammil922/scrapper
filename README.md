# Pakistan Hospitals & Clinics Data Scraper

A comprehensive web scraper that collects detailed information about hospitals, clinics, and medical facilities across Pakistan from multiple sources including Google Maps, websites, and social media platforms.

## Features

- **Multi-Source Data Collection:**
  - ✅ Google Maps listings
  - ✅ Hospital/Clinic websites
  - ✅ Facebook pages
  - ✅ Instagram profiles
  - ✅ TikTok accounts

- **Data Fields Collected:**
  - Business name
  - Category (Hospital, Dental Clinic, Eye Clinic, etc.)
  - Address and City
  - Phone numbers
  - Email addresses
  - Website URLs
  - Social media links (Facebook, Instagram, TikTok)
  - Google Maps link
  - Established year
  - Review count and ratings
  - Traffic estimates
  - Social media followers
  - Description and services offered

- **Export Formats:**
  - CSV file
  - Excel file (.xlsx)

## Installation

1. **Install Python 3.8 or higher**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Chrome browser** (required for Selenium)

## Usage

1. **Run the scraper:**
   ```bash
   python main.py
   ```

2. **The scraper will:**
   - Scrape Google Maps for hospitals/clinics in major Pakistani cities
   - Visit each website to extract detailed information
   - Find and scrape social media pages
   - Merge all data and export to CSV and Excel files

3. **Output files:**
   - `pakistan_hospitals_clinics_data.csv`
   - `pakistan_hospitals_clinics_data.xlsx`

## Configuration

You can customize the scraper in `config.py`:

- **Categories:** Add or modify medical facility categories
- **Cities:** Add or remove cities to scrape
- **Settings:** Adjust delays, timeouts, and limits

## Categories Included

- Hospitals
- Dental Clinics
- Eye Clinics
- General Clinics
- Maternity Hospitals
- Cardiac Hospitals
- Orthopedic Hospitals

## Cities Covered

Major cities in Pakistan including:
- Karachi
- Lahore
- Islamabad
- Rawalpindi
- Faisalabad
- And more...

## Important Notes

⚠️ **Legal & Ethical Considerations:**
- This scraper is for educational/research purposes
- Respect robots.txt and terms of service
- Use reasonable delays between requests
- Don't overload servers with requests

⚠️ **Rate Limiting:**
- The scraper includes delays between requests to avoid being blocked
- Adjust delays in `config.py` if needed

⚠️ **Data Accuracy:**
- Data is scraped from public sources
- Verify important information before use
- Some fields may be missing or incomplete

## Troubleshooting

**Chrome driver issues:**
- The scraper uses `undetected-chromedriver` which should auto-install ChromeDriver
- If issues persist, manually install ChromeDriver

**No results:**
- Check your internet connection
- Some websites may block automated access
- Try running with `headless=False` to see what's happening

**Slow performance:**
- Scraping takes time due to delays between requests
- Reduce number of cities/categories in `config.py` for faster scraping
- The scraper processes multiple sources per listing, which takes time

## File Structure

```
.
├── main.py                    # Main script to run
├── config.py                  # Configuration settings
├── google_maps_scraper.py    # Google Maps scraper
├── website_scraper.py        # Website scraper
├── social_media_scraper.py   # Social media scrapers
├── data_aggregator.py        # Data merging and export
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Support

For issues or questions, please check:
1. All dependencies are installed
2. Chrome browser is installed
3. Internet connection is stable
4. No firewall blocking requests

## License

This project is provided as-is for educational purposes.

