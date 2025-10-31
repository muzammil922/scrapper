"""
Social Media Scraper for Facebook, Instagram, and TikTok
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from config import SCRAPER_SETTINGS

class SocialMediaScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
    
    def init_driver(self):
        """Initialize Chrome driver"""
        try:
            options = uc.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'user-agent={self.ua.random}')
            
            self.driver = uc.Chrome(options=options, version_main=None)
            return True
        except Exception as e:
            print(f"Error initializing driver: {e}")
            return False
    
    def find_facebook_page(self, business_name, location=""):
        """Search and find Facebook page for a business"""
        if not self.driver:
            if not self.init_driver():
                return {}
        
        try:
            query = f"{business_name} {location} facebook"
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Look for Facebook links in search results
            facebook_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='facebook.com']")
            
            for link in facebook_links[:3]:  # Check first 3 results
                href = link.get_attribute('href')
                if 'facebook.com' in href and '/pages/' in href or '/groups/' not in href:
                    return {'facebook_url': href}
            
            return {}
        except Exception as e:
            print(f"Error finding Facebook page: {e}")
            return {}
    
    def scrape_facebook_page(self, facebook_url):
        """Scrape Facebook page for followers, posts, etc."""
        if not facebook_url or facebook_url == "N/A":
            return {}
        
        if not self.driver:
            if not self.init_driver():
                return {}
        
        try:
            print(f"Scraping Facebook: {facebook_url}")
            self.driver.get(facebook_url)
            time.sleep(5)
            
            data = {'facebook_url': facebook_url}
            
            # Try to extract follower count
            try:
                # Look for follower/people text
                page_text = self.driver.find_element(By.TAG_NAME, 'body').text
                
                # Pattern for followers: "X followers" or "X people like this"
                follower_patterns = [
                    r'([\d,]+)\s*(?:followers|people\s+like)',
                    r'([\d,]+)\s*(?:likes)',
                ]
                
                for pattern in follower_patterns:
                    match = re.search(pattern, page_text, re.IGNORECASE)
                    if match:
                        data['facebook_followers'] = match.group(1).replace(',', '')
                        break
                
                # Extract email from page
                page_source = self.driver.page_source
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, page_source)
                if emails:
                    data['email_from_facebook'] = emails[0]
                
                # Extract phone
                phone_patterns = [
                    r'\+92\s?[0-9]{2,3}\s?[0-9]{7}',
                    r'0[0-9]{2,3}\s?[0-9]{7}',
                ]
                for pattern in phone_patterns:
                    phones = re.findall(pattern, page_source)
                    if phones:
                        data['phone_from_facebook'] = phones[0]
                        break
                
            except Exception as e:
                print(f"Error extracting Facebook data: {e}")
            
            return data
            
        except Exception as e:
            print(f"Error scraping Facebook page: {e}")
            return {}
    
    def find_instagram_page(self, business_name, location=""):
        """Search and find Instagram page for a business"""
        if not self.driver:
            if not self.init_driver():
                return {}
        
        try:
            query = f"{business_name} {location} instagram"
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Look for Instagram links
            instagram_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='instagram.com']")
            
            for link in instagram_links[:3]:
                href = link.get_attribute('href')
                if 'instagram.com' in href and '/p/' not in href and '/reel/' not in href:
                    return {'instagram_url': href}
            
            return {}
        except Exception as e:
            print(f"Error finding Instagram page: {e}")
            return {}
    
    def scrape_instagram_page(self, instagram_url):
        """Scrape Instagram page for followers, posts"""
        if not instagram_url or instagram_url == "N/A":
            return {}
        
        if not self.driver:
            if not self.init_driver():
                return {}
        
        try:
            print(f"Scraping Instagram: {instagram_url}")
            self.driver.get(instagram_url)
            time.sleep(5)
            
            data = {'instagram_url': instagram_url}
            
            # Try to extract follower count
            try:
                page_source = self.driver.page_source
                
                # Instagram follower patterns
                follower_patterns = [
                    r'"edge_followed_by":{"count":(\d+)}',
                    r'(\d+(?:,\d+)?)\s*followers',
                ]
                
                for pattern in follower_patterns:
                    match = re.search(pattern, page_source, re.IGNORECASE)
                    if match:
                        data['instagram_followers'] = match.group(1).replace(',', '')
                        break
                
                # Extract email from bio
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, page_source)
                if emails:
                    data['email_from_instagram'] = emails[0]
                
            except Exception as e:
                print(f"Error extracting Instagram data: {e}")
            
            return data
            
        except Exception as e:
            print(f"Error scraping Instagram page: {e}")
            return {}
    
    def find_tiktok_page(self, business_name, location=""):
        """Search and find TikTok page for a business"""
        if not self.driver:
            if not self.init_driver():
                return {}
        
        try:
            query = f"{business_name} {location} tiktok"
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Look for TikTok links
            tiktok_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='tiktok.com']")
            
            for link in tiktok_links[:3]:
                href = link.get_attribute('href')
                if 'tiktok.com' in href and '/video/' not in href:
                    return {'tiktok_url': href}
            
            return {}
        except Exception as e:
            print(f"Error finding TikTok page: {e}")
            return {}
    
    def scrape_tiktok_page(self, tiktok_url):
        """Scrape TikTok page for followers"""
        if not tiktok_url or tiktok_url == "N/A":
            return {}
        
        if not self.driver:
            if not self.init_driver():
                return {}
        
        try:
            print(f"Scraping TikTok: {tiktok_url}")
            self.driver.get(tiktok_url)
            time.sleep(5)
            
            data = {'tiktok_url': tiktok_url}
            
            try:
                page_source = self.driver.page_source
                
                # TikTok follower patterns
                follower_patterns = [
                    r'"followerCount":(\d+)',
                    r'(\d+(?:,\d+)?)\s*followers',
                ]
                
                for pattern in follower_patterns:
                    match = re.search(pattern, page_source, re.IGNORECASE)
                    if match:
                        data['tiktok_followers'] = match.group(1).replace(',', '')
                        break
                
            except Exception as e:
                print(f"Error extracting TikTok data: {e}")
            
            return data
            
        except Exception as e:
            print(f"Error scraping TikTok page: {e}")
            return {}
    
    def scrape_all_social_media(self, business_name, location="", existing_data=None):
        """Scrape all social media platforms for a business"""
        if existing_data is None:
            existing_data = {}
        
        # Find social media pages
        print(f"\nSearching social media for: {business_name}")
        
        # Facebook
        if 'facebook_url' not in existing_data or not existing_data.get('facebook_url'):
            fb_data = self.find_facebook_page(business_name, location)
            existing_data.update(fb_data)
        
        if existing_data.get('facebook_url'):
            fb_details = self.scrape_facebook_page(existing_data['facebook_url'])
            existing_data.update(fb_details)
            time.sleep(2)
        
        # Instagram
        if 'instagram_url' not in existing_data or not existing_data.get('instagram_url'):
            ig_data = self.find_instagram_page(business_name, location)
            existing_data.update(ig_data)
        
        if existing_data.get('instagram_url'):
            ig_details = self.scrape_instagram_page(existing_data['instagram_url'])
            existing_data.update(ig_details)
            time.sleep(2)
        
        # TikTok
        if 'tiktok_url' not in existing_data or not existing_data.get('tiktok_url'):
            tt_data = self.find_tiktok_page(business_name, location)
            existing_data.update(tt_data)
        
        if existing_data.get('tiktok_url'):
            tt_details = self.scrape_tiktok_page(existing_data['tiktok_url'])
            existing_data.update(tt_details)
            time.sleep(2)
        
        return existing_data
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

