"""
Vercel-compatible API - Serverless version
Uses APIs instead of Selenium for Vercel deployment
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Import scrapers that work in serverless (without Selenium)
from wikipedia_scraper import WikipediaScraper
import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    """API Home"""
    return jsonify({
        "message": "Universal Data Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "/api/scrape": "Scrape data (POST)",
            "/api/scrape/wikipedia": "Scrape Wikipedia (POST)",
            "/api/scrape/google": "Scrape Google (GET)",
            "/api/health": "Health check (GET)"
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/scrape/wikipedia', methods=['POST'])
def scrape_wikipedia():
    """Scrape Wikipedia articles"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        scraper = WikipediaScraper()
        results = scraper.search_articles(query, max_results=max_results)
        
        return jsonify({
            "success": True,
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scrape/google-api', methods=['POST'])
def scrape_google_api():
    """Scrape using Google Custom Search API (requires API key)"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        api_key = os.environ.get('GOOGLE_API_KEY')
        search_engine_id = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        if not api_key or not search_engine_id:
            return jsonify({
                "error": "Google API key and Search Engine ID required",
                "note": "Set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID in Vercel environment variables"
            }), 400
        
        # Use Google Custom Search API
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': query,
            'num': min(max_results, 10)  # Max 10 per request
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('items', []):
            results.append({
                'title': item.get('title'),
                'url': item.get('link'),
                'description': item.get('snippet'),
                'platform': 'google',
                'source': 'google_custom_search'
            })
        
        return jsonify({
            "success": True,
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scrape/youtube-api', methods=['POST'])
def scrape_youtube_api():
    """Scrape YouTube using YouTube Data API"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        api_key = os.environ.get('YOUTUBE_API_KEY')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        if not api_key:
            return jsonify({
                "error": "YouTube API key required",
                "note": "Set YOUTUBE_API_KEY in Vercel environment variables"
            }), 400
        
        # Use YouTube Data API v3
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': query,
            'key': api_key,
            'maxResults': min(max_results, 50),
            'type': 'video'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']
            results.append({
                'title': snippet.get('title'),
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'description': snippet.get('description', '')[:500],
                'thumbnail': snippet.get('thumbnails', {}).get('default', {}).get('url'),
                'channel': snippet.get('channelTitle'),
                'published_date': snippet.get('publishedAt'),
                'platform': 'youtube',
                'source': 'youtube_api'
            })
        
        return jsonify({
            "success": True,
            "query": query,
            "results": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scrape', methods=['POST'])
def scrape_universal():
    """Universal scraping endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        platforms = data.get('platforms', ['wikipedia'])
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        all_results = []
        
        # Wikipedia (no API key needed)
        if 'wikipedia' in platforms:
            scraper = WikipediaScraper()
            wiki_results = scraper.search_articles(query, max_results=max_results)
            for result in wiki_results:
                result['category'] = data.get('category', 'general')
            all_results.extend(wiki_results)
        
        # YouTube (requires API key)
        if 'youtube' in platforms:
            api_key = os.environ.get('YOUTUBE_API_KEY')
            if api_key:
                yt_url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': query,
                    'key': api_key,
                    'maxResults': min(max_results, 50),
                    'type': 'video'
                }
                try:
                    response = requests.get(yt_url, params=params, timeout=10)
                    if response.status_code == 200:
                        yt_data = response.json()
                        for item in yt_data.get('items', []):
                            video_id = item['id']['videoId']
                            snippet = item['snippet']
                            all_results.append({
                                'title': snippet.get('title'),
                                'url': f"https://www.youtube.com/watch?v={video_id}",
                                'description': snippet.get('description', '')[:500],
                                'thumbnail': snippet.get('thumbnails', {}).get('default', {}).get('url'),
                                'platform': 'youtube',
                                'category': data.get('category', 'general'),
                                'source': 'youtube_api'
                            })
                except:
                    pass  # Skip if API fails
        
        # Google (requires API key)
        if 'google' in platforms:
            api_key = os.environ.get('GOOGLE_API_KEY')
            search_engine_id = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
            if api_key and search_engine_id:
                google_url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    'key': api_key,
                    'cx': search_engine_id,
                    'q': query,
                    'num': min(max_results, 10)
                }
                try:
                    response = requests.get(google_url, params=params, timeout=10)
                    if response.status_code == 200:
                        google_data = response.json()
                        for item in google_data.get('items', []):
                            all_results.append({
                                'title': item.get('title'),
                                'url': item.get('link'),
                                'description': item.get('snippet'),
                                'platform': 'google',
                                'category': data.get('category', 'general'),
                                'source': 'google_custom_search'
                            })
                except:
                    pass  # Skip if API fails
        
        return jsonify({
            "success": True,
            "query": query,
            "results": all_results,
            "count": len(all_results),
            "platforms_used": platforms,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For Vercel
def handler(request):
    """Vercel serverless handler"""
    return app(request.environ, request.start_response)

if __name__ == '__main__':
    app.run(debug=True)

