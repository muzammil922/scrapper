"""
YouTube Scraper - Scrape videos, music, channels, playlists
"""

import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from config import SCRAPER_SETTINGS as BASE_SETTINGS
from generic_config import SCRAPER_SETTINGS, CONTENT_FILTER

class YouTubeScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.ua = UserAgent()
        self.data = []
        
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
        """Check if content should be blocked based on filters"""
        if not CONTENT_FILTER.get("enabled"):
            return False
        
        text = f"{title} {description}".lower()
        
        # Block adult content
        if CONTENT_FILTER.get("block_adult"):
            blocked_keywords = SCRAPER_SETTINGS.get("exclude_keywords", [])
            for keyword in blocked_keywords:
                if keyword.lower() in text:
                    return True
        
        # Block specific domains
        blocked_domains = CONTENT_FILTER.get("blocked_domains", [])
        for domain in blocked_domains:
            if domain in text:
                return True
        
        return False
    
    def parse_views(self, views_text):
        """Parse view count from text like '1.2M views' or '500K views'"""
        if not views_text:
            return 0
        
        views_text = views_text.lower().replace('views', '').strip()
        
        try:
            if 'm' in views_text:
                return int(float(views_text.replace('m', '')) * 1000000)
            elif 'k' in views_text:
                return int(float(views_text.replace('k', '')) * 1000)
            elif 'b' in views_text:
                return int(float(views_text.replace('b', '')) * 1000000000)
            else:
                return int(views_text.replace(',', ''))
        except:
            return 0
    
    def parse_duration(self, duration_text):
        """Parse duration from text like '10:30' or '5:23:45'"""
        if not duration_text:
            return None
        
        parts = duration_text.split(':')
        try:
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except:
            pass
        
        return None
    
    def search_videos(self, query, max_results=50):
        """Search for videos on YouTube"""
        if not self.driver:
            if not self.init_driver():
                return []
        
        try:
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Scroll to load more results
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
            
            videos = []
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer, ytd-grid-video-renderer")
            
            for element in video_elements[:max_results]:
                try:
                    video_data = self.extract_video_info(element)
                    if video_data and not self.should_block_content(
                        video_data.get('title', ''), 
                        video_data.get('description', '')
                    ):
                        videos.append(video_data)
                except Exception as e:
                    continue
            
            return videos
            
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []
    
    def extract_video_info(self, element):
        """Extract video information from element"""
        try:
            data = {
                'platform': 'youtube',
                'source': 'youtube',
            }
            
            # Extract title
            try:
                title_elem = element.find_element(By.CSS_SELECTOR, "#video-title, ytd-video-meta-block #video-title")
                data['title'] = title_elem.get_attribute('title') or title_elem.text
                data['url'] = title_elem.get_attribute('href')
            except:
                return None
            
            # Extract channel
            try:
                channel_elem = element.find_element(By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.yt-formatted-string")
                data['author'] = channel_elem.text
                data['creator'] = channel_elem.text
            except:
                data['author'] = "Unknown"
            
            # Extract views
            try:
                views_elem = element.find_element(By.CSS_SELECTOR, "#metadata-line span")
                views_text = views_elem.text
                data['views'] = self.parse_views(views_text)
            except:
                data['views'] = 0
            
            # Extract duration
            try:
                duration_elem = element.find_element(By.CSS_SELECTOR, "span.style-scope.ytd-thumbnail-overlay-time-status-renderer")
                duration_text = duration_elem.text.strip()
                data['duration'] = duration_text
                data['duration_seconds'] = self.parse_duration(duration_text)
            except:
                data['duration'] = None
            
            # Extract thumbnail
            try:
                thumb_elem = element.find_element(By.CSS_SELECTOR, "img")
                data['thumbnail'] = thumb_elem.get_attribute('src')
            except:
                data['thumbnail'] = None
            
            # Extract description
            try:
                desc_elem = element.find_element(By.CSS_SELECTOR, "#description-text")
                data['description'] = desc_elem.text[:500]  # Limit to 500 chars
            except:
                data['description'] = ""
            
            # Try to get more details by visiting the video page
            if data.get('url'):
                try:
                    self.driver.get(data['url'])
                    time.sleep(2)
                    
                    # Get likes (if visible)
                    try:
                        like_button = self.driver.find_element(By.CSS_SELECTOR, "ytd-toggle-button-renderer button")
                        like_text = like_button.get_attribute('aria-label')
                        likes_match = re.search(r'([\d,]+)', like_text)
                        if likes_match:
                            data['likes'] = likes_match.group(1).replace(',', '')
                    except:
                        pass
                    
                    # Get description from video page
                    try:
                        desc_section = self.driver.find_element(By.CSS_SELECTOR, "#description")
                        data['description'] = desc_section.text[:1000]
                    except:
                        pass
                    
                    # Get tags
                    try:
                        tags_elem = self.driver.find_element(By.CSS_SELECTOR, "yt-formatted-string[class*='tags']")
                        tags = tags_elem.text.split('#')[1:]  # Remove first empty
                        data['tags'] = ', '.join([t.strip() for t in tags[:10]])
                    except:
                        pass
                    
                    # Go back to search results
                    self.driver.back()
                    time.sleep(2)
                    
                except Exception as e:
                    pass
            
            data['scraped_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            return data
            
        except Exception as e:
            print(f"Error extracting video info: {e}")
            return None
    
    def search_channels(self, query, max_results=20):
        """Search for YouTube channels"""
        if not self.driver:
            if not self.init_driver():
                return []
        
        try:
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}&sp=EgIQAg%253D%253D"
            self.driver.get(search_url)
            time.sleep(3)
            
            channels = []
            channel_elements = self.driver.find_elements(By.CSS_SELECTOR, "ytd-channel-renderer")
            
            for element in channel_elements[:max_results]:
                try:
                    data = {
                        'platform': 'youtube',
                        'source': 'youtube',
                        'type': 'channel'
                    }
                    
                    # Extract channel name
                    try:
                        name_elem = element.find_element(By.CSS_SELECTOR, "#text a")
                        data['name'] = name_elem.text
                        data['url'] = name_elem.get_attribute('href')
                    except:
                        continue
                    
                    # Extract subscriber count
                    try:
                        sub_elem = element.find_element(By.CSS_SELECTOR, "#subscribers")
                        data['followers'] = sub_elem.text
                    except:
                        data['followers'] = "0"
                    
                    # Extract description
                    try:
                        desc_elem = element.find_element(By.CSS_SELECTOR, "#description")
                        data['description'] = desc_elem.text[:500]
                    except:
                        data['description'] = ""
                    
                    data['scraped_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    channels.append(data)
                    
                except Exception as e:
                    continue
            
            return channels
            
        except Exception as e:
            print(f"Error searching channels: {e}")
            return []
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None

