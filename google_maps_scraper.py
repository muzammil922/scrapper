"""
Google Maps Scraper for Hospitals and Clinics in Pakistan
"""

import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import pandas as pd
from config import CATEGORIES, CITIES, DATA_FIELDS

class GoogleMapsScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.ua = UserAgent()
        self.data = []
        
    def init_driver(self):
        """Initialize Chrome driver with anti-detection measures"""
        try:
            options = uc.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'user-agent={self.ua.random}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = uc.Chrome(options=options, version_main=None)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"Error initializing driver: {e}")
            return False
    
    def search_location(self, query):
        """Search for locations on Google Maps"""
        try:
            search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Scroll to load more results
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
            for _ in range(5):
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight',
                    scrollable_div
                )
                time.sleep(2)
            
            return True
        except Exception as e:
            print(f"Error searching location: {e}")
            return False
    
    def extract_business_info(self, element):
        """Extract business information from a listing element"""
        try:
            info = {}
            
            # Click on the listing to get details
            element.click()
            time.sleep(2)
            
            # Extract name
            try:
                name_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1[data-attrid='title']"))
                )
                info['name'] = name_element.text
            except:
                try:
                    info['name'] = self.driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
                except:
                    info['name'] = "N/A"
            
            # Extract address
            try:
                address_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address']")
                info['address'] = address_button.find_element(By.XPATH, "..").text
            except:
                info['address'] = "N/A"
            
            # Extract phone
            try:
                phone_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id*='phone']")
                info['phone'] = phone_button.find_element(By.XPATH, "..").text
            except:
                info['phone'] = "N/A"
            
            # Extract website
            try:
                website_button = self.driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']")
                info['website'] = website_button.get_attribute('href')
            except:
                info['website'] = "N/A"
            
            # Extract rating and reviews
            try:
                rating_element = self.driver.find_element(By.CSS_SELECTOR, "div.F7nice span")
                info['rating'] = rating_element.text
            except:
                info['rating'] = "N/A"
            
            try:
                reviews_element = self.driver.find_element(By.CSS_SELECTOR, "span.hqzQac")
                review_text = reviews_element.text
                review_count = re.search(r'([\d,]+)', review_text)
                info['review_count'] = review_count.group(1) if review_count else "0"
            except:
                info['review_count'] = "0"
            
            # Get Google Maps URL
            info['google_maps_url'] = self.driver.current_url
            
            # Close the detail panel
            try:
                close_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']")
                close_button.click()
                time.sleep(1)
            except:
                pass
            
            return info
            
        except Exception as e:
            print(f"Error extracting business info: {e}")
            return None
    
    def scrape_category(self, category_name, search_query):
        """Scrape all listings for a specific category"""
        print(f"\nScraping {category_name}...")
        
        if not self.search_location(search_query):
            return []
        
        results = []
        try:
            # Find all listing elements
            listings = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")
            
            unique_listings = []
            seen_urls = set()
            for listing in listings:
                try:
                    url = listing.get_attribute('href')
                    if url and url not in seen_urls and '/maps/place/' in url:
                        seen_urls.add(url)
                        unique_listings.append(listing)
                except:
                    continue
            
            print(f"Found {len(unique_listings)} listings for {category_name}")
            
            # Extract info from each listing
            for i, listing in enumerate(unique_listings[:50]):  # Limit to 50 per category
                try:
                    print(f"Processing {i+1}/{min(len(unique_listings), 50)}: {category_name}")
                    info = self.extract_business_info(listing)
                    if info:
                        info['category'] = category_name
                        results.append(info)
                    time.sleep(2)
                except Exception as e:
                    print(f"Error processing listing {i+1}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error scraping category {category_name}: {e}")
        
        return results
    
    def scrape_all(self):
        """Scrape all categories"""
        if not self.init_driver():
            return []
        
        all_results = []
        
        try:
            for category_key, search_query in CATEGORIES.items():
                for city in CITIES[:3]:  # Limit to first 3 cities for now
                    query = f"{search_query} {city}"
                    results = self.scrape_category(category_key, query)
                    all_results.extend(results)
                    time.sleep(5)  # Delay between cities
        except Exception as e:
            print(f"Error in scrape_all: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return all_results

