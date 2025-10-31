"""
Example: How to use the Vercel API
"""

import requests
import json

# Vercel deployment URL (replace with your URL)
API_URL = "https://your-project.vercel.app"

def test_api():
    """Test the deployed API"""
    
    # 1. Health check
    print("1. Health Check...")
    response = requests.get(f"{API_URL}/api/health")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # 2. Scrape Wikipedia (no API key needed)
    print("2. Scraping Wikipedia...")
    response = requests.post(
        f"{API_URL}/api/scrape/wikipedia",
        json={
            "query": "python programming",
            "max_results": 5
        }
    )
    data = response.json()
    print(f"Found {data['count']} results")
    for i, result in enumerate(data['results'][:3], 1):
        print(f"  {i}. {result['title']}")
    print()
    
    # 3. Scrape YouTube (requires API key)
    print("3. Scraping YouTube...")
    response = requests.post(
        f"{API_URL}/api/scrape/youtube-api",
        json={
            "query": "pakistani songs",
            "max_results": 5
        }
    )
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['count']} results")
        for i, result in enumerate(data['results'][:3], 1):
            print(f"  {i}. {result['title']}")
    else:
        print(f"Error: {response.json()}")
    print()
    
    # 4. Universal scrape
    print("4. Universal Scraping...")
    response = requests.post(
        f"{API_URL}/api/scrape",
        json={
            "query": "data science tutorials",
            "platforms": ["wikipedia"],  # Only Wikipedia (no API key needed)
            "max_results": 5,
            "category": "education"
        }
    )
    data = response.json()
    print(f"Found {data['count']} results from {data['platforms_used']}")
    print()

if __name__ == "__main__":
    # Replace with your Vercel URL
    API_URL = input("Enter your Vercel API URL (or press Enter for localhost:5000): ").strip()
    if not API_URL:
        API_URL = "http://localhost:5000"
    
    test_api()

