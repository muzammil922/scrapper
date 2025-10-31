"""
Configuration file for the Pakistan Hospital/Clinic Scraper
"""

# Categories to search for
CATEGORIES = {
    "hospital": "hospitals in Pakistan",
    "dental_clinic": "dental clinics in Pakistan",
    "eye_clinic": "eye clinics in Pakistan",
    "general_clinic": "clinics in Pakistan",
    "maternity": "maternity hospitals in Pakistan",
    "cardiac": "cardiac hospitals in Pakistan",
    "orthopedic": "orthopedic hospitals in Pakistan"
}

# Major cities in Pakistan
CITIES = [
    "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad",
    "Multan", "Peshawar", "Quetta", "Sialkot", "Gujranwala",
    "Hyderabad", "Sargodha", "Bahawalpur", "Sukkur", "Larkana"
]

# Data fields to collect
DATA_FIELDS = [
    "name",
    "category",
    "address",
    "city",
    "phone",
    "email",
    "website",
    "facebook_url",
    "instagram_url",
    "tiktok_url",
    "google_maps_url",
    "established_year",
    "review_count",
    "rating",
    "traffic_estimate",
    "social_media_followers",
    "description",
    "services",
    "scraped_date"
]

# Scraper settings
SCRAPER_SETTINGS = {
    "delay_between_requests": 2,  # seconds
    "max_results_per_category": 100,
    "headless": True,
    "timeout": 30
}

