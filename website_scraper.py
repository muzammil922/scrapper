"""
Website Scraper to extract detailed information from clinic/hospital websites
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse
from fake_useragent import UserAgent
from config import SCRAPER_SETTINGS

class WebsiteScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def extract_emails(self, html_content):
        """Extract email addresses from HTML content"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html_content)
        # Filter out common non-business emails
        filtered_emails = [e for e in emails if not any(
            x in e.lower() for x in ['example.com', 'test.com', 'domain.com', 'email.com']
        )]
        return list(set(filtered_emails))
    
    def extract_phones(self, html_content):
        """Extract phone numbers from HTML content"""
        # Pakistan phone number patterns
        patterns = [
            r'\+92\s?[0-9]{2,3}\s?[0-9]{7}',  # +92 format
            r'0[0-9]{2,3}\s?[0-9]{7}',  # 03XX format
            r'\([0-9]{2,3}\)\s?[0-9]{7}',  # (021) format
            r'[0-9]{4}[\s-]?[0-9]{7}',  # 0214-XXXXXXX
        ]
        
        phones = []
        for pattern in patterns:
            matches = re.findall(pattern, html_content)
            phones.extend(matches)
        
        return list(set(phones))
    
    def extract_established_year(self, html_content):
        """Try to extract establishment year"""
        # Look for patterns like "Established 1990", "Since 1990", etc.
        patterns = [
            r'established\s+(?:in\s+)?(\d{4})',
            r'since\s+(\d{4})',
            r'founded\s+(?:in\s+)?(\d{4})',
            r'(\d{4})\s*-\s*established',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                year = int(match.group(1))
                if 1900 <= year <= 2024:  # Reasonable year range
                    return year
        
        return None
    
    def extract_description(self, soup):
        """Extract description/about text"""
        # Try common meta tags first
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']
        
        # Try to find about section
        about_keywords = ['about', 'description', 'intro', 'overview']
        for keyword in about_keywords:
            tag = soup.find(id=re.compile(keyword, re.I)) or soup.find(class_=re.compile(keyword, re.I))
            if tag:
                text = tag.get_text(strip=True)
                if len(text) > 50:
                    return text[:500]  # Limit to 500 chars
        
        return None
    
    def extract_services(self, soup):
        """Extract services offered"""
        services = []
        
        # Look for services sections
        service_keywords = ['service', 'treatment', 'specialty', 'facility']
        for keyword in service_keywords:
            tags = soup.find_all(class_=re.compile(keyword, re.I))
            for tag in tags:
                items = tag.find_all('li') or tag.find_all(['p', 'div'])
                for item in items[:20]:  # Limit results
                    text = item.get_text(strip=True)
                    if text and len(text) < 100:
                        services.append(text)
        
        return list(set(services))[:15]  # Return max 15 unique services
    
    def scrape_website(self, url):
        """Scrape a single website for detailed information"""
        if not url or url == "N/A":
            return {}
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"Scraping website: {url}")
            response = self.session.get(url, timeout=SCRAPER_SETTINGS['timeout'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            html_text = soup.get_text()
            
            # Extract all information
            data = {
                'website': url,
                'email': ', '.join(self.extract_emails(response.text)[:3]),  # Max 3 emails
                'phone_from_website': ', '.join(self.extract_phones(response.text)[:3]),
                'established_year': self.extract_established_year(html_text),
                'description': self.extract_description(soup),
                'services': ', '.join(self.extract_services(soup)),
            }
            
            time.sleep(SCRAPER_SETTINGS['delay_between_requests'])
            return data
            
        except Exception as e:
            print(f"Error scraping website {url}: {e}")
            return {
                'website': url,
                'email': None,
                'phone_from_website': None,
                'established_year': None,
                'description': None,
                'services': None,
            }

