"""
Main script to run the comprehensive Pakistan Hospital/Clinic Scraper
"""

import time
from google_maps_scraper import GoogleMapsScraper
from website_scraper import WebsiteScraper
from social_media_scraper import SocialMediaScraper
from data_aggregator import DataAggregator
from config import SCRAPER_SETTINGS

def main():
    print("=" * 60)
    print("PAKISTAN HOSPITALS & CLINICS DATA SCRAPER")
    print("=" * 60)
    print("\nThis scraper will collect data from:")
    print("  ✓ Google Maps")
    print("  ✓ Hospital/Clinic Websites")
    print("  ✓ Facebook Pages")
    print("  ✓ Instagram Pages")
    print("  ✓ TikTok Pages")
    print("\n" + "=" * 60 + "\n")
    
    # Initialize scrapers
    print("Initializing scrapers...")
    google_scraper = GoogleMapsScraper(headless=SCRAPER_SETTINGS['headless'])
    website_scraper = WebsiteScraper()
    social_scraper = SocialMediaScraper(headless=SCRAPER_SETTINGS['headless'])
    aggregator = DataAggregator()
    
    # Step 1: Scrape Google Maps
    print("\n" + "=" * 60)
    print("STEP 1: Scraping Google Maps...")
    print("=" * 60)
    google_results = google_scraper.scrape_all()
    print(f"\n✓ Found {len(google_results)} listings from Google Maps")
    
    if not google_results:
        print("No results from Google Maps. Exiting.")
        return
    
    # Step 2: Scrape websites and social media for each listing
    print("\n" + "=" * 60)
    print("STEP 2: Enriching data from websites and social media...")
    print("=" * 60)
    
    total = len(google_results)
    for idx, listing in enumerate(google_results, 1):
        print(f"\n[{idx}/{total}] Processing: {listing.get('name', 'Unknown')}")
        
        # Scrape website
        website_data = {}
        if listing.get('website') and listing['website'] != "N/A":
            website_data = website_scraper.scrape_website(listing['website'])
            time.sleep(SCRAPER_SETTINGS['delay_between_requests'])
        
        # Scrape social media
        business_name = listing.get('name', '')
        location = listing.get('address', '')
        social_data = social_scraper.scrape_all_social_media(
            business_name, 
            location, 
            listing
        )
        time.sleep(SCRAPER_SETTINGS['delay_between_requests'])
        
        # Merge all data
        merged_record = aggregator.merge_data(listing, website_data, social_data)
        aggregator.add_record(merged_record)
        
        print(f"  ✓ Email: {merged_record.get('email', 'N/A')}")
        print(f"  ✓ Phone: {merged_record.get('phone', 'N/A')}")
        print(f"  ✓ Website: {merged_record.get('website', 'N/A')}")
        print(f"  ✓ Reviews: {merged_record.get('review_count', 'N/A')}")
        
        # Progress indicator
        if idx % 10 == 0:
            print(f"\n  Progress: {idx}/{total} completed ({idx*100//total}%)")
    
    # Close browser
    social_scraper.close()
    
    # Step 3: Export data
    print("\n" + "=" * 60)
    print("STEP 3: Exporting data...")
    print("=" * 60)
    
    csv_file = aggregator.export_to_csv()
    excel_file = aggregator.export_to_excel()
    
    # Show statistics
    print("\n" + "=" * 60)
    print("SCRAPING STATISTICS")
    print("=" * 60)
    stats = aggregator.get_statistics()
    print(f"\nTotal Records: {stats.get('total_records', 0)}")
    print(f"Records with Email: {stats.get('with_emails', 0)}")
    print(f"Records with Phone: {stats.get('with_phones', 0)}")
    print(f"Records with Website: {stats.get('with_websites', 0)}")
    print(f"Records with Facebook: {stats.get('with_facebook', 0)}")
    print(f"Records with Instagram: {stats.get('with_instagram', 0)}")
    
    if stats.get('categories'):
        print("\nCategories:")
        for cat, count in stats['categories'].items():
            print(f"  - {cat}: {count}")
    
    print("\n" + "=" * 60)
    print("✓ SCRAPING COMPLETE!")
    print(f"✓ CSV file: {csv_file}")
    print(f"✓ Excel file: {excel_file}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        import traceback
        traceback.print_exc()

