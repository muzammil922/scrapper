"""
Wikipedia Scraper - Scrape articles, knowledge, history, facts
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from fake_useragent import UserAgent
from generic_config import SCRAPER_SETTINGS, CONTENT_FILTER

class WikipediaScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        self.base_url = "https://en.wikipedia.org"
    
    def should_block_content(self, title, content):
        """Check if content should be blocked"""
        if not CONTENT_FILTER.get("enabled"):
            return False
        
        text = f"{title} {content}".lower()
        
        if CONTENT_FILTER.get("block_adult"):
            blocked_keywords = SCRAPER_SETTINGS.get("exclude_keywords", [])
            for keyword in blocked_keywords:
                if keyword.lower() in text:
                    return True
        
        return False
    
    def search_articles(self, query, max_results=50):
        """Search Wikipedia for articles"""
        try:
            search_url = f"{self.base_url}/w/index.php?search={query.replace(' ', '+')}"
            response = self.session.get(search_url, timeout=SCRAPER_SETTINGS['timeout'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find search results
            results = soup.find_all('li', class_='mw-search-result')
            
            for result in results[:max_results]:
                try:
                    article_data = self.extract_search_result(result)
                    if article_data and not self.should_block_content(
                        article_data.get('title', ''),
                        article_data.get('description', '')
                    ):
                        articles.append(article_data)
                except Exception as e:
                    continue
                
                time.sleep(SCRAPER_SETTINGS['delay_between_requests'])
            
            return articles
            
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []
    
    def extract_search_result(self, result_element):
        """Extract information from search result"""
        try:
            data = {
                'platform': 'wikipedia',
                'source': 'wikipedia',
            }
            
            # Extract title and URL
            title_elem = result_element.find('a', href=re.compile('/wiki/'))
            if not title_elem:
                return None
            
            data['title'] = title_elem.text.strip()
            data['url'] = self.base_url + title_elem['href']
            data['name'] = data['title']
            
            # Extract snippet/description
            snippet = result_element.find('div', class_='searchresult')
            if snippet:
                data['description'] = snippet.get_text(strip=True)[:500]
            
            return data
            
        except Exception as e:
            return None
    
    def get_article_content(self, article_url):
        """Get full content of a Wikipedia article"""
        try:
            response = self.session.get(article_url, timeout=SCRAPER_SETTINGS['timeout'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'platform': 'wikipedia',
                'source': 'wikipedia',
                'url': article_url
            }
            
            # Extract title
            title_elem = soup.find('h1', class_='firstHeading')
            if title_elem:
                data['title'] = title_elem.text.strip()
                data['name'] = data['title']
            
            # Extract main content
            content_div = soup.find('div', class_='mw-parser-output')
            if content_div:
                # Remove unwanted elements
                for elem in content_div.find_all(['table', 'div', 'span'], class_=re.compile('navbox|infobox|metadata|hatnote')):
                    elem.decompose()
                
                paragraphs = content_div.find_all('p')
                content_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs[:20]])
                data['content'] = content_text[:5000]  # Limit to 5000 chars
                data['description'] = content_text[:500]  # First 500 chars as description
            
            # Extract infobox data
            infobox = soup.find('table', class_='infobox')
            if infobox:
                metadata = {}
                rows = infobox.find_all('tr')
                for row in rows[:10]:  # Limit to 10 rows
                    header = row.find('th')
                    value = row.find('td')
                    if header and value:
                        key = header.get_text(strip=True)
                        val = value.get_text(strip=True)
                        metadata[key] = val
                data['metadata'] = str(metadata)
            
            # Extract categories
            categories = []
            cat_links = soup.find('div', id='mw-normal-catlinks')
            if cat_links:
                for link in cat_links.find_all('a')[1:]:  # Skip first "Categories:" link
                    categories.append(link.text.strip())
            data['tags'] = ', '.join(categories[:10])
            
            # Extract images
            images = []
            for img in soup.find_all('img', src=re.compile('^//upload')):
                if img.get('src'):
                    images.append('https:' + img['src'])
            if images:
                data['thumbnail'] = images[0]
            
            # Extract references/links
            links = []
            for link in content_div.find_all('a', href=re.compile('^/wiki/'))[:20]:
                links.append(self.base_url + link['href'])
            data['related_links'] = ', '.join(links)
            
            data['scraped_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            return data
            
        except Exception as e:
            print(f"Error getting article content: {e}")
            return None
    
    def get_category_pages(self, category_name, max_results=50):
        """Get all pages in a Wikipedia category"""
        try:
            category_url = f"{self.base_url}/wiki/Category:{category_name.replace(' ', '_')}"
            response = self.session.get(category_url, timeout=SCRAPER_SETTINGS['timeout'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find category pages
            content_div = soup.find('div', id='mw-pages')
            if content_div:
                links = content_div.find_all('a', href=re.compile('^/wiki/'))
                
                for link in links[:max_results]:
                    try:
                        article_url = self.base_url + link['href']
                        article_data = self.get_article_content(article_url)
                        if article_data:
                            articles.append(article_data)
                        time.sleep(SCRAPER_SETTINGS['delay_between_requests'])
                    except Exception as e:
                        continue
            
            return articles
            
        except Exception as e:
            print(f"Error getting category pages: {e}")
            return []

