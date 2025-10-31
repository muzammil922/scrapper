"""
Universal Generic Data Scraper Configuration
Scrape data for ANYTHING in the world - Songs, Movies, History, Religion, Knowledge, etc.
"""

# ============================================================================
# GLOBAL CATEGORIES - Add any category you want to scrape
# ============================================================================

GLOBAL_CATEGORIES = {
    # Music & Songs
    "songs_urdu": {
        "query": "urdu songs",
        "platforms": ["youtube", "spotify", "google"],
        "type": "music"
    },
    "songs_english": {
        "query": "english songs",
        "platforms": ["youtube", "spotify", "google"],
        "type": "music"
    },
    "songs_hindi": {
        "query": "hindi songs",
        "platforms": ["youtube", "spotify", "google"],
        "type": "music"
    },
    "music_artists": {
        "query": "music artists",
        "platforms": ["youtube", "spotify", "wikipedia", "google"],
        "type": "music"
    },
    
    # Movies & Entertainment
    "movies_hollywood": {
        "query": "hollywood movies",
        "platforms": ["imdb", "wikipedia", "google", "youtube"],
        "type": "movie"
    },
    "movies_bollywood": {
        "query": "bollywood movies",
        "platforms": ["imdb", "wikipedia", "google", "youtube"],
        "type": "movie"
    },
    "movies_pakistani": {
        "query": "pakistani movies",
        "platforms": ["imdb", "wikipedia", "google", "youtube"],
        "type": "movie"
    },
    "tv_shows": {
        "query": "tv shows series",
        "platforms": ["imdb", "wikipedia", "google", "youtube"],
        "type": "tv"
    },
    
    # Knowledge & History
    "world_history": {
        "query": "world history events",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "history"
    },
    "countries_data": {
        "query": "countries information",
        "platforms": ["wikipedia", "google"],
        "type": "geography"
    },
    "world_facts": {
        "query": "world facts information",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "knowledge"
    },
    
    # Religion & Spirituality
    "islamic_knowledge": {
        "query": "islamic knowledge quran hadith",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "religion"
    },
    "hindu_knowledge": {
        "query": "hindu religion knowledge",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "religion"
    },
    "christian_knowledge": {
        "query": "christianity bible knowledge",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "religion"
    },
    
    # Astrology & Mysticism
    "astrology": {
        "query": "astrology horoscope zodiac",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "astrology"
    },
    
    # Educational Content
    "science": {
        "query": "science discoveries facts",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "education"
    },
    "technology": {
        "query": "technology innovations",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "tech"
    },
    "education_videos": {
        "query": "educational videos tutorials",
        "platforms": ["youtube", "google"],
        "type": "education"
    },
    
    # Business & Economy
    "companies": {
        "query": "companies businesses",
        "platforms": ["google", "wikipedia", "linkedin"],
        "type": "business"
    },
    
    # Health & Medicine
    "health_information": {
        "query": "health medicine information",
        "platforms": ["wikipedia", "google", "youtube"],
        "type": "health"
    },
    
    # Add YOUR custom categories here:
    # "your_category": {
    #     "query": "your search query",
    #     "platforms": ["youtube", "wikipedia", "google"],
    #     "type": "your_type"
    # }
}

# ============================================================================
# PLATFORMS TO SCRAPE FROM
# ============================================================================

AVAILABLE_PLATFORMS = {
    "youtube": {
        "enabled": True,
        "scrape": ["videos", "channels", "playlists", "comments"],
        "max_results": 100
    },
    "wikipedia": {
        "enabled": True,
        "scrape": ["articles", "categories", "images"],
        "max_results": 100
    },
    "google": {
        "enabled": True,
        "scrape": ["search_results", "images", "news", "videos"],
        "max_results": 100
    },
    "spotify": {
        "enabled": True,
        "scrape": ["songs", "artists", "albums", "playlists"],
        "max_results": 50
    },
    "imdb": {
        "enabled": True,
        "scrape": ["movies", "tv_shows", "actors", "ratings"],
        "max_results": 100
    },
    "twitter": {
        "enabled": True,
        "scrape": ["tweets", "users", "trends"],
        "max_results": 50
    },
    "reddit": {
        "enabled": True,
        "scrape": ["posts", "comments", "subreddits"],
        "max_results": 50
    },
    "tiktok": {
        "enabled": True,
        "scrape": ["videos", "users", "hashtags"],
        "max_results": 50
    },
    "instagram": {
        "enabled": True,
        "scrape": ["posts", "users", "hashtags"],
        "max_results": 50
    },
    "facebook": {
        "enabled": True,
        "scrape": ["pages", "posts", "groups"],
        "max_results": 50
    }
}

# ============================================================================
# UNIVERSAL DATA FIELDS
# ============================================================================

UNIVERSAL_DATA_FIELDS = [
    "title",
    "name",
    "category",
    "type",
    "description",
    "content",
    "url",
    "source",
    "platform",
    "author",
    "creator",
    "published_date",
    "views",
    "likes",
    "comments",
    "shares",
    "followers",
    "rating",
    "duration",
    "thumbnail",
    "tags",
    "keywords",
    "language",
    "country",
    "related_links",
    "scraped_date",
    "metadata"
]

# ============================================================================
# SCRAPER SETTINGS
# ============================================================================

SCRAPER_SETTINGS = {
    "delay_between_requests": 2,  # seconds
    "max_results_per_category": 100,
    "max_results_per_platform": 100,
    "headless": True,
    "timeout": 30,
    "retry_attempts": 3,
    "concurrent_requests": 1,  # Set to 1 to avoid being blocked
    "save_images": False,
    "save_videos": False,
    "output_format": ["csv", "json", "excel"],
    "exclude_keywords": [
        "porn", "xxx", "adult", "18+", "nsfw", 
        "explicit", "sexual", "nude"  # Auto-filter adult content
    ]
}

# ============================================================================
# COUNTRIES & LANGUAGES
# ============================================================================

COUNTRIES = [
    "Pakistan", "India", "USA", "UK", "Canada", "Australia",
    "Bangladesh", "UAE", "Saudi Arabia", "Turkey", "Malaysia",
    "Indonesia", "China", "Japan", "South Korea", "Germany",
    "France", "Spain", "Italy", "Brazil", "Mexico", "Argentina"
]

LANGUAGES = [
    "English", "Urdu", "Hindi", "Arabic", "Spanish", "French",
    "German", "Chinese", "Japanese", "Korean", "Turkish"
]

# ============================================================================
# FILTER SETTINGS (Auto-filter inappropriate content)
# ============================================================================

CONTENT_FILTER = {
    "enabled": True,
    "block_adult": True,
    "block_violence": False,
    "min_age_rating": None,
    "allowed_languages": None,  # None = all languages
    "blocked_domains": [
        "pornhub.com",
        "xvideos.com",
        "xhamster.com",
        # Add more adult sites to block
    ]
}

