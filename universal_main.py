"""
Universal Global Data Scraper - Main Script
Scrape data for ANYTHING in the world!
"""

import time
from youtube_scraper import YouTubeScraper
from wikipedia_scraper import WikipediaScraper
from google_search_scraper import GoogleSearchScraper
from universal_aggregator import UniversalAggregator
from generic_config import GLOBAL_CATEGORIES, AVAILABLE_PLATFORMS, SCRAPER_SETTINGS

def scrape_category(category_key, category_config, aggregator):
    """Scrape a single category across all configured platforms"""
    print(f"\n{'='*70}")
    print(f"SCRAPING CATEGORY: {category_key.upper()}")
    print(f"Query: {category_config['query']}")
    print(f"Platforms: {', '.join(category_config['platforms'])}")
    print(f"{'='*70}\n")
    
    query = category_config['query']
    platforms = category_config['platforms']
    category_type = category_config.get('type', 'general')
    max_results = SCRAPER_SETTINGS.get('max_results_per_category', 100)
    
    total_found = 0
    
    # Scrape from each platform
    for platform in platforms:
        if not AVAILABLE_PLATFORMS.get(platform, {}).get('enabled', True):
            print(f"  ⏭ Skipping {platform} (disabled)")
            continue
        
        try:
            print(f"\n  📡 Scraping from {platform.upper()}...")
            
            platform_max = min(
                max_results // len(platforms),
                AVAILABLE_PLATFORMS.get(platform, {}).get('max_results', 50)
            )
            
            records = []
            
            if platform == 'youtube':
                scraper = YouTubeScraper(headless=SCRAPER_SETTINGS['headless'])
                records = scraper.search_videos(query, max_results=platform_max)
                scraper.close()
            
            elif platform == 'wikipedia':
                scraper = WikipediaScraper()
                records = scraper.search_articles(query, max_results=platform_max)
            
            elif platform == 'google':
                scraper = GoogleSearchScraper(headless=SCRAPER_SETTINGS['headless'])
                records = scraper.search(query, search_type='all', max_results=platform_max)
                scraper.close()
            
            elif platform == 'spotify':
                # Spotify scraper would go here
                print(f"    ⚠ Spotify scraper not yet implemented")
                continue
            
            elif platform == 'imdb':
                # IMDB scraper would go here
                print(f"    ⚠ IMDB scraper not yet implemented")
                continue
            
            # Add category and type to each record
            for record in records:
                record['category'] = category_key
                record['type'] = category_type
                aggregator.add_record(record)
            
            total_found += len(records)
            print(f"    ✓ Found {len(records)} records from {platform}")
            
            time.sleep(SCRAPER_SETTINGS['delay_between_requests'])
            
        except Exception as e:
            print(f"    ✗ Error scraping {platform}: {e}")
            continue
    
    print(f"\n  ✓ Total records found for {category_key}: {total_found}")
    return total_found

def main():
    print("="*70)
    print("🌍 UNIVERSAL GLOBAL DATA SCRAPER 🌍")
    print("="*70)
    print("\nScrape data for ANYTHING in the world!")
    print("Categories: Songs, Movies, History, Religion, Knowledge, and more!")
    print("\n" + "="*70 + "\n")
    
    # Initialize aggregator
    aggregator = UniversalAggregator()
    
    # Ask user which categories to scrape
    print("Available Categories:")
    for i, (key, config) in enumerate(GLOBAL_CATEGORIES.items(), 1):
        print(f"  {i}. {key.replace('_', ' ').title()} - {config['query']}")
    
    print("\nOptions:")
    print("  1. Scrape ALL categories (this will take a long time!)")
    print("  2. Scrape specific categories (enter numbers separated by commas)")
    print("  3. Quick test (scrape 1-2 categories)")
    
    try:
        choice = input("\nEnter your choice (1/2/3) [default: 3]: ").strip() or "3"
    except:
        choice = "3"
    
    categories_to_scrape = []
    
    if choice == "1":
        categories_to_scrape = list(GLOBAL_CATEGORIES.keys())
        print(f"\n⚠️  WARNING: Scraping ALL {len(categories_to_scrape)} categories will take a VERY long time!")
        confirm = input("Continue? (yes/no) [no]: ").strip().lower()
        if confirm != 'yes':
            print("Cancelled.")
            return
    
    elif choice == "2":
        try:
            numbers = input("Enter category numbers (e.g., 1,3,5): ").strip()
            indices = [int(n.strip()) - 1 for n in numbers.split(',')]
            category_list = list(GLOBAL_CATEGORIES.keys())
            categories_to_scrape = [category_list[i] for i in indices if 0 <= i < len(category_list)]
        except:
            print("Invalid input. Using default: Quick test")
            categories_to_scrape = list(GLOBAL_CATEGORIES.keys())[:2]
    
    else:  # Quick test
        categories_to_scrape = list(GLOBAL_CATEGORIES.keys())[:2]
        print("\n🚀 Running QUICK TEST mode (2 categories)")
    
    if not categories_to_scrape:
        print("No categories selected. Exiting.")
        return
    
    print(f"\n✅ Will scrape {len(categories_to_scrape)} category/categories")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    # Scrape each category
    start_time = time.time()
    total_records = 0
    
    for i, category_key in enumerate(categories_to_scrape, 1):
        print(f"\n\n[{i}/{len(categories_to_scrape)}] Processing category...")
        
        category_config = GLOBAL_CATEGORIES[category_key]
        records_found = scrape_category(category_key, category_config, aggregator)
        total_records += records_found
        
        # Progress update
        elapsed = time.time() - start_time
        avg_time = elapsed / i
        remaining = avg_time * (len(categories_to_scrape) - i)
        print(f"\n⏱  Progress: {i}/{len(categories_to_scrape)} | "
              f"Time elapsed: {elapsed/60:.1f} min | "
              f"Est. remaining: {remaining/60:.1f} min")
    
    # Export data
    print("\n" + "="*70)
    print("EXPORTING DATA...")
    print("="*70)
    
    print("\nExport options:")
    print("  1. All formats (CSV, Excel, JSON, PDF) - Recommended")
    print("  2. CSV only")
    print("  3. Excel only")
    print("  4. JSON only")
    print("  5. PDF only (Beautiful formatted report)")
    print("  6. PDF per category (separate PDF for each category)")
    
    try:
        export_choice = input("\nChoose export format (1-6) [default: 1]: ").strip() or "1"
    except:
        export_choice = "1"
    
    if export_choice == "1":
        # Export all formats including PDF
        files = aggregator.export_all_formats('universal_scraped_data')
        print(f"\n✅ All formats exported!")
    
    elif export_choice == "2":
        aggregator.export_to_csv()
    
    elif export_choice == "3":
        aggregator.export_to_excel()
    
    elif export_choice == "4":
        aggregator.export_to_json()
    
    elif export_choice == "5":
        pdf_file = aggregator.export_to_pdf('universal_scraped_data_report.pdf')
        if pdf_file:
            print(f"\n✅ PDF report created: {pdf_file}")
            print("   You can now download and view the beautifully formatted PDF!")
    
    elif export_choice == "6":
        pdf_files = aggregator.export_to_pdf(category_specific=True)
        if pdf_files:
            print(f"\n✅ Created {len(pdf_files)} PDF files (one per category)")
    
    else:
        # Default: all formats
        files = aggregator.export_all_formats('universal_scraped_data')
    
    # Show statistics
    print("\n" + "="*70)
    print("📊 SCRAPING STATISTICS")
    print("="*70)
    stats = aggregator.get_statistics()
    
    print(f"\n✅ Total Records Scraped: {stats['total_records']}")
    
    if stats['by_platform']:
        print(f"\n📡 By Platform:")
        for platform, count in sorted(stats['by_platform'].items(), key=lambda x: x[1], reverse=True):
            print(f"   - {platform}: {count}")
    
    if stats['by_category']:
        print(f"\n📁 By Category:")
        for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True):
            print(f"   - {category}: {count}")
    
    if stats['by_type']:
        print(f"\n🏷  By Type:")
        for type_val, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
            print(f"   - {type_val}: {count}")
    
    total_time = time.time() - start_time
    print(f"\n⏱  Total Time: {total_time/60:.2f} minutes")
    print(f"⚡ Average: {stats['total_records']/(total_time/60):.1f} records/minute")
    
    print("\n" + "="*70)
    print("✅ SCRAPING COMPLETE!")
    print("="*70)
    print("\n📁 Output files available:")
    print("   - universal_scraped_data.csv (Spreadsheet format)")
    print("   - universal_scraped_data.xlsx (Excel with multiple sheets)")
    print("   - universal_scraped_data.json (JSON data)")
    print("   - universal_scraped_data_report.pdf (Beautiful PDF report)")
    print("\n💡 TIP: Open the PDF to see a beautifully formatted report!")
    print("="*70)
    
    # Ask about auto-update
    print("\n🔄 Would you like to enable AUTO-UPDATE mode?")
    print("   (Data will update automatically without manual intervention)")
    try:
        auto_update = input("Enable auto-update? (yes/no) [no]: ").strip().lower()
        if auto_update == 'yes':
            try:
                hours = int(input("Update every how many hours? [24]: ").strip() or "24")
            except:
                hours = 24
            
            print(f"\n🚀 Starting auto-update mode (updates every {hours} hours)...")
            from auto_updater import AutoUpdater
            updater = AutoUpdater()
            updater.aggregator = aggregator
            updater.start_continuous_mode(update_interval_hours=hours, categories=categories_to_scrape)
    except KeyboardInterrupt:
        print("\nSkipping auto-update.")
    except Exception as e:
        print(f"Could not start auto-update: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user.")
        print("Data scraped so far has been saved.")
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

