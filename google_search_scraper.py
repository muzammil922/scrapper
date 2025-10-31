"""
Google Search Scraper - Universal search across all content types
"""

import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from generic_config import SCRAPER_SETTINGS, CONTENT_FILTER

class GoogleSearchScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.ua = UserAgent()
        
    def init_driver(self):
        """Initialize Chrome driver"""
        try:
            options = uc.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'user-agent={self.ua.random}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            self.driver = uc.Chrome(options=options, version_main=None)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"Error initializing driver: {e}")
            return False
    
    def should_block_content(self, title, description):
        """Check if content should be blocked"""
        if not CONTENT_FILTER.get("enabled"):
            return False
        
        text = f"{title} {description}".lower()
        
        if CONTENT_FILTER.get("block_adult"):
            blocked_keywords = SCRAPER_SETTINGS.get("exclude_keywords", [])
            for keyword in blocked_keywords:
                if keyword.lower() in text:
                    return True
        
        blocked_domains = CONTENT_FILTER.get("blocked_domains", [])
        for domain in blocked_domains:
            if domain.lower() in text.lower():
                return True
        
        return False
    
    def search(self, query, search_type="all", max_results=50):
        """
        Search Google
        search_type: "all", "images", "videos", "news"
        """
        if not self.driver:
            if not self.init_driver():
                return []
        
        try:
            if search_type == "images":
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch"
            elif search_type == "videos":
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=vid"
            elif search_type == "news":
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=nws"
            else:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            self.driver.get(search_url)
            time.sleep(3)
            
            results = []
            
            if search_type == "images":
                results = self.scrape_images(max_results)
            elif search_type == "videos":
                results = self.scrape_videos(max_results)
            elif search_type == "news":
                results = self.scrape_news(max_results)
            else:
                results = self.scrape_web_results(max_results)
            
            return results
            
        except Exception as e:
            print(f"Error searching Google: {e}")
            return []
    
    def scrape_web_results(self, max_results=50):
        """Scrape regular web search results"""
        results = []
        try:
            # Find all result elements
            result_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.g, div[data-ved]")
            
            for element in result_elements[:max_results]:
                try:
                    data = {
                        'platform': 'google',
                        'source': 'google_search',
                        'type': 'web_result'
                    }
                    
                    # Extract title
                    try:
                        title_elem = element.find_element(By.CSS_SELECTOR, "h3, a h3")
                        data['title'] = title_elem.text
                        data['name'] = data['title']
                    except:
                        continue
                    
                    # Extract URL
                    try:
                        link_elem = element.find_element(By.CSS_SELECTOR, "a[href^='http']")
                        data['url'] = link_elem.get_attribute('href')
                    except:
                        pass
                    
                    # Extract description
                    try:
                        desc_elem = element.find_element(By.CSS_SELECTOR, "span[style*='-webkit-line-clamp']")
                        data['description'] = desc_elem.text[:500]
                    except:
                        try:
                            desc_elem = element.find_element(By.CSS_SELECTOR, "div[data-sncf]")
                            data['description'] = desc_elem.text[:500]
                        except:
                            data['description'] = ""
                    
                    if data.get('title') and not self.should_block_content(
                        data.get('title', ''),
                        data.get('description', '')
                    ):
                        data['scraped_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        results.append(data)
                        
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"Error scraping web results: {e}")
        
        return results
    
    def scrape_images(self, max_results=50):
        """Scrape image search results"""
        results = []
        try:
            # Scroll to load more images
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
            
            image_elements = self.driver.find_elements(By.CSS_SELECTOR, "img[data-src], img[src]")
            
            for img in image_elements[:max_results]:
                try:
                    src = img.get_attribute('data-src') or img.get_attribute('src')
                    if not src or 'data:image' in src:
                        continue
                    
                    data = {
                        'platform': 'google',
                        'source': 'google_images',
                        'type': 'image',
                        'title': img.get_attribute('alt') or 'Image',
                        'thumbnail': src,
                        'url': src,
                        'scraped_date': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    if not self.should_block_content(data.get('title', ''), ''):
                        results.append(data)
                        
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"Error scraping images: {e}")
        
        return results
    
    def scrape_videos(self, max_results=50):
        """Scrape video search results"""
        results = []
        try:
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-ved]")
            
            for element in video_elements[:max_results]:
                try:
                    data = {
                        'platform': 'google',
                        'source': 'google_videos',
                        'type': 'video'
                    }
                    
                    # Extract title
                    try:
                        title_elem = element.find_element(By.CSS_SELECTOR, "h3, a h3")
                        data['title'] = title_elem.text
                        data['name'] = data['title']
                    except:
                        continue
                    
                    # Extract URL
                    try:
                        link_elem = element.find_element(By.CSS_SELECTOR, "a[href^='http']")
                        data['url'] = link_elem.get_attribute('href')
                    except:
                        pass
                    
                    # Extract duration
                    try:
                        duration_elem = element.find_element(By.CSS_SELECTOR, "span[style*='duration']")
                        data['duration'] = duration_elem.text
                    except:
                        pass
                    
                    # Extract source
                    try:
                        source_elem = element.find_element(By.CSS_SELECTOR, "span[style*='source']")
                        data['author'] = source_elem.text
                    except:
                        pass
                    
                    data['scraped_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    if not self.should_block_content(data.get('title', ''), ''):
                        results.append(data)
                        
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"Error scraping videos: {e}")
        
        return results
    
    def scrape_news(self, max_results=50):
        """Scrape news search results"""
        results = []
        try:
            news_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-ved]")
            
            for element in news_elements[:max_results]:
                try:
                    data = {
                        'platform': 'google',
                        'source': 'google_news',
                        'type': 'news'
                    }
                    
                    # Extract title
                    try:
                        title_elem = element.find_element(By.CSS_SELECTOR, "h3, a h3")
                        data['title'] = title_elem.text
                        data['name'] = data['title']
                    except:
                        continue
                    
                    # Extract URL
                    try:
                        link_elem = element.find_element(By.CSS_SELECTOR, "a[href^='http']")
                        data['url'] = link_elem.get_attribute('href')
                    except:
                        pass
                    
                    # Extract source and date
                    try:
                        source_elem = element.find_element(By.CSS_SELECTOR, "span[style*='source']")
                        source_text = source_elem.text
                        # Try to extract date
                        date_match = re.search(r'(\d+\s+(hours?|days?|weeks?|months?)\s+ago|\d+/\d+/\d+)', source_text)
                        if date_match:
                            data['published_date'] = date_match.group(1)
                        data['author'] = source_text
                    except:
                        pass
                    
                    # Extract description
                    try:
                        desc_elem = element.find_element(By.CSS_SELECTOR, "span[style*='line-clamp']")
                        data['description'] = desc_elem.text[:500]
                    except:
                        data['description'] = ""
                    
                    data['scraped_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    if not self.should_block_content(data.get('title', ''), data.get('description', '')):
                        results.append(data)
                        
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"Error scraping news: {e}")
        
        return results
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None

