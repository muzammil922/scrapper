"""
Quick Start Script - Test the scraper with limited data
Use this to test the scraper before running the full version
"""

import time
from selenium.webdriver.common.by import By
from google_maps_scraper import GoogleMapsScraper
from website_scraper import WebsiteScraper
from social_media_scraper import SocialMediaScraper
from data_aggregator import DataAggregator
from config import SCRAPER_SETTINGS

def quick_test():
    """Quick test with just 1-2 listings"""
    print("=" * 60)
    print("QUICK TEST MODE - Limited Data Scraping")
    print("=" * 60)
    print("\nThis will scrape just 1-2 listings for testing purposes.\n")
    
    # Initialize scrapers
    print("Initializing scrapers...")
    google_scraper = GoogleMapsScraper(headless=False)  # Show browser for testing
    website_scraper = WebsiteScraper()
    social_scraper = SocialMediaScraper(headless=False)
    aggregator = DataAggregator()
    
    # Test with just one category and one city
    print("\nTesting with: Dental clinics in Karachi")
    
    if not google_scraper.init_driver():
        print("Failed to initialize driver!")
        return
    
    # Scrape just 2-3 listings
    if google_scraper.search_location("dental clinics in Karachi"):
        try:
            listings = google_scraper.driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")
            unique_listings = []
            seen_urls = set()
            
            for listing in listings[:10]:  # Just get first 10
                try:
                    url = listing.get_attribute('href')
                    if url and url not in seen_urls and '/maps/place/' in url:
                        seen_urls.add(url)
                        unique_listings.append(listing)
                        if len(unique_listings) >= 2:  # Limit to 2 for testing
                            break
                except:
                    continue
            
            print(f"\nFound {len(unique_listings)} listings. Processing...")
            
            for i, listing in enumerate(unique_listings, 1):
                print(f"\n[{i}/{len(unique_listings)}] Processing listing...")
                info = google_scraper.extract_business_info(listing)
                
                if info:
                    info['category'] = 'dental_clinic'
                    
                    # Scrape website
                    website_data = {}
                    if info.get('website') and info['website'] != "N/A":
                        website_data = website_scraper.scrape_website(info['website'])
                    
                    # Scrape social media
                    social_data = social_scraper.scrape_all_social_media(
                        info.get('name', ''), 
                        info.get('address', ''), 
                        info
                    )
                    
                    # Merge and save
                    merged = aggregator.merge_data(info, website_data, social_data)
                    aggregator.add_record(merged)
                    
                    print(f"  ✓ Name: {merged.get('name')}")
                    print(f"  ✓ Email: {merged.get('email', 'N/A')}")
                    print(f"  ✓ Phone: {merged.get('phone', 'N/A')}")
                    
                    time.sleep(3)
        
        except Exception as e:
            print(f"Error during scraping: {e}")
            import traceback
            traceback.print_exc()
    
    # Close browsers
    if google_scraper.driver:
        google_scraper.driver.quit()
    social_scraper.close()
    
    # Export
    if aggregator.all_data:
        print("\n" + "=" * 60)
        print("Exporting test data...")
        print("=" * 60)
        aggregator.export_to_csv('test_data.csv')
        aggregator.export_to_excel('test_data.xlsx')
        print("\n✓ Test complete! Check test_data.csv and test_data.xlsx")
    else:
        print("\nNo data collected. Please check your internet connection and try again.")

if __name__ == "__main__":
    try:
        quick_test()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        import traceback
        traceback.print_exc()

