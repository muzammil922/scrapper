"""
Smart Scraper - Ultimate User-Friendly Interface
Auto-detects what user wants and scrapes everything
"""

import time
from universal_main import main as universal_main
from auto_updater import AutoUpdater
from universal_aggregator import UniversalAggregator
from generic_config import GLOBAL_CATEGORIES

def smart_scraper_menu():
    """Main menu with all options"""
    print("\n" + "="*70)
    print("🌍 UNIVERSAL SMART DATA SCRAPER")
    print("="*70)
    print("\nThe Ultimate Scraper - No Restrictions, Billions of Data Points!")
    print("\nChoose your mode:")
    print("\n1. 📥 ONE-TIME SCRAPING")
    print("   → Scrape data once, export and download")
    print("\n2. 🔄 AUTO-UPDATE MODE")
    print("   → Continuously updates data automatically")
    print("   → No manual work needed, always fresh data")
    print("\n3. 🎯 SMART CATEGORY SCRAPER")
    print("   → Tell me what you want, I'll scrape it")
    print("\n4. 📊 VIEW STATISTICS")
    print("   → See what data you already have")
    print("\n5. ⚙️  MANAGE CATEGORIES")
    print("   → Add/remove categories")
    print("\n6. 📁 EXPORT EXISTING DATA")
    print("   → Export already scraped data to PDF/CSV/Excel")
    print("\n7. 🚀 CONTINUOUS MODE (Background)")
    print("   → Runs in background, keeps updating")
    print("\n0. ❌ EXIT")
    
    try:
        choice = input("\nEnter your choice (0-7): ").strip()
        return choice
    except:
        return "0"

def smart_category_scraper():
    """Let user describe what they want, then scrape"""
    print("\n" + "="*70)
    print("🎯 SMART CATEGORY SCRAPER")
    print("="*70)
    print("\nTell me what you want to scrape!")
    print("Examples:")
    print("  - 'pakistani songs'")
    print("  - 'python tutorials'")
    print("  - 'islamic knowledge'")
    print("  - 'cooking recipes'")
    print("  - 'anything you want!'")
    print()
    
    try:
        user_query = input("What do you want to scrape? ").strip()
        if not user_query:
            print("No query provided!")
            return
        
        print(f"\n✅ Got it! I'll scrape: '{user_query}'")
        print("Creating custom category...")
        
        # Create temporary category
        category_key = user_query.lower().replace(' ', '_')[:50]
        category_config = {
            "query": user_query,
            "platforms": ["youtube", "wikipedia", "google"],
            "type": "custom"
        }
        
        # Add to config temporarily
        from generic_config import GLOBAL_CATEGORIES
        GLOBAL_CATEGORIES[category_key] = category_config
        
        print(f"\n🚀 Starting scraping...")
        
        aggregator = UniversalAggregator()
        from universal_main import scrape_category
        scrape_category(category_key, category_config, aggregator)
        
        # Export
        print("\n📥 Exporting data...")
        files = aggregator.export_all_formats(f'smart_{category_key}')
        
        print(f"\n✅ Done! Files created:")
        for format_type, filename in files.items():
            print(f"   - {filename} ({format_type.upper()})")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def export_existing_data():
    """Export already scraped data"""
    import os
    import json
    
    print("\n" + "="*70)
    print("📁 EXPORT EXISTING DATA")
    print("="*70)
    
    # Look for existing JSON files
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'scraped' in f.lower()]
    
    if not json_files:
        print("\nNo existing data files found.")
        print("Please run scraping first!")
        return
    
    print(f"\nFound {len(json_files)} data file(s):")
    for i, f in enumerate(json_files, 1):
        print(f"  {i}. {f}")
    
    try:
        choice = int(input(f"\nSelect file (1-{len(json_files)}): ").strip())
        if 1 <= choice <= len(json_files):
            selected_file = json_files[choice - 1]
            
            # Load data
            with open(selected_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'data' in data:
                aggregator = UniversalAggregator()
                aggregator.all_data = data['data']
                
                print("\nExport formats:")
                print("  1. All formats (CSV, Excel, JSON, PDF)")
                print("  2. PDF only (Beautiful report)")
                print("  3. PDF per category")
                
                exp_choice = input("\nChoice [1]: ").strip() or "1"
                
                if exp_choice == "1":
                    files = aggregator.export_all_formats('exported_data')
                elif exp_choice == "2":
                    aggregator.export_to_pdf('exported_data_report.pdf')
                elif exp_choice == "3":
                    aggregator.export_to_pdf(category_specific=True)
                
                print("\n✅ Export complete!")
            else:
                print("Invalid data format!")
    except Exception as e:
        print(f"Error: {e}")

def view_statistics():
    """View statistics of scraped data"""
    import os
    import json
    
    print("\n" + "="*70)
    print("📊 DATA STATISTICS")
    print("="*70)
    
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'scraped' in f.lower()]
    
    if not json_files:
        print("\nNo data files found. Run scraping first!")
        return
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'metadata' in data:
                meta = data['metadata']
                stats = meta.get('statistics', {})
                
                print(f"\n📁 File: {json_file}")
                print(f"   Total Records: {meta.get('total_records', 0)}")
                
                if 'by_platform' in stats:
                    print(f"   Platforms: {len(stats['by_platform'])}")
                    for platform, count in list(stats['by_platform'].items())[:5]:
                        print(f"      - {platform}: {count}")
                
                if 'by_category' in stats:
                    print(f"   Categories: {len(stats['by_category'])}")
                    for cat, count in list(stats['by_category'].items())[:5]:
                        print(f"      - {cat}: {count}")
        except:
            pass

def continuous_mode():
    """Start continuous background scraping"""
    print("\n" + "="*70)
    print("🚀 CONTINUOUS MODE")
    print("="*70)
    print("\nThis will run in the background and continuously update data.")
    print("You can close this and data will keep updating!")
    print()
    
    try:
        hours = int(input("Update every how many hours? [24]: ").strip() or "24")
        
        print("\nCategories to update:")
        print("  1. All categories")
        print("  2. Selected categories")
        cat_choice = input("Choice [1]: ").strip() or "1"
        
        if cat_choice == "1":
            categories = None
        else:
            print("\nAvailable categories:")
            for i, (key, config) in enumerate(list(GLOBAL_CATEGORIES.items())[:10], 1):
                print(f"  {i}. {key}")
            cat_nums = input("Enter numbers (comma-separated): ").strip()
            indices = [int(n.strip()) - 1 for n in cat_nums.split(',')]
            category_list = list(GLOBAL_CATEGORIES.keys())
            categories = [category_list[i] for i in indices if 0 <= i < len(category_list)]
        
        print(f"\n🚀 Starting continuous mode...")
        print(f"   Updates every {hours} hours")
        print(f"   Categories: {len(categories) if categories else 'All'}")
        print(f"\n⚠️  This will keep running. Press Ctrl+C to stop.")
        
        updater = AutoUpdater()
        updater.start_continuous_mode(hours, categories)
        
    except KeyboardInterrupt:
        print("\n\nStopped.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🌍 WELCOME TO UNIVERSAL SMART DATA SCRAPER")
    print("="*70)
    print("\n✨ Features:")
    print("  ✓ Scrape ANYTHING - No restrictions")
    print("  ✓ Billions of data points")
    print("  ✓ Auto-updates - No manual work")
    print("  ✓ PDF Export - Beautiful formatted reports")
    print("  ✓ All formats - CSV, Excel, JSON, PDF")
    print("  ✓ Smart scraping - Just tell me what you want!")
    print("="*70)
    
    while True:
        choice = smart_scraper_menu()
        
        if choice == "0":
            print("\n👋 Thank you for using Universal Smart Scraper!")
            break
        
        elif choice == "1":
            universal_main()
        
        elif choice == "2":
            try:
                hours = int(input("\nUpdate every how many hours? [24]: ").strip() or "24")
                updater = AutoUpdater()
                updater.start_continuous_mode(hours)
            except KeyboardInterrupt:
                print("\nCancelled.")
        
        elif choice == "3":
            smart_category_scraper()
        
        elif choice == "4":
            view_statistics()
        
        elif choice == "5":
            print("\nTo add categories, run: python add_category.py")
            print("Or edit: generic_config.py")
        
        elif choice == "6":
            export_existing_data()
        
        elif choice == "7":
            continuous_mode()
        
        else:
            print("\nInvalid choice!")
        
        input("\n\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()

