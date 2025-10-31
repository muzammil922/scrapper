"""
Vercel-compatible API - Serverless version
Uses BaseHTTPRequestHandler for Vercel Python runtime
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import urllib.parse

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        path = self.path.split('?')[0]
        
        if path == '/' or path == '/api':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "message": "Universal Data Scraper API",
                "version": "1.0.0",
                "status": "running",
                "endpoints": {
                    "/api/health": "Health check (GET)",
                    "/api/scrape/wikipedia": "Scrape Wikipedia (POST)"
                }
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "environment": os.environ.get('VERCEL_ENV', 'development')
            }
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Not found", "path": path}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        path = self.path.split('?')[0]
        
        if path == '/api/scrape/wikipedia':
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body.decode()) if body else {}
                query = data.get('query', '')
                max_results = int(data.get('max_results', 10))
                
                if not query:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {"error": "Query parameter is required"}
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                # Scrape Wikipedia
                results = self.scrape_wikipedia(query, max_results)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    "success": True,
                    "query": query,
                    "results": results,
                    "count": len(results),
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
            
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Not found", "path": path}
            self.wfile.write(json.dumps(response).encode())
    
    def scrape_wikipedia(self, query, max_results=10):
        """Scrape Wikipedia articles"""
        if not HAS_DEPS:
            return []
        
        try:
            base_url = "https://en.wikipedia.org"
            search_url = f"{base_url}/w/index.php?search={urllib.parse.quote(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Find search results
            search_results = soup.find_all('li', class_='mw-search-result')
            
            for result in search_results[:max_results]:
                try:
                    title_elem = result.find('a', href=lambda x: x and '/wiki/' in x)
                    if not title_elem:
                        continue
                    
                    data = {
                        'platform': 'wikipedia',
                        'source': 'wikipedia',
                        'title': title_elem.text.strip(),
                        'url': base_url + title_elem['href'],
                        'name': title_elem.text.strip()
                    }
                    
                    # Extract snippet
                    snippet = result.find('div', class_='searchresult')
                    if snippet:
                        data['description'] = snippet.get_text(strip=True)[:500]
                    
                    results.append(data)
                    
                except Exception:
                    continue
            
            return results
            
        except Exception as e:
            return []
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass
