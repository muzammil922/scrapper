"""
Auto-Updater - Continuously updates data without manual intervention
"""

import time
import schedule
import threading
from datetime import datetime
from universal_aggregator import UniversalAggregator
from generic_config import GLOBAL_CATEGORIES, SCRAPER_SETTINGS
from youtube_scraper import YouTubeScraper
from wikipedia_scraper import WikipediaScraper
from google_search_scraper import GoogleSearchScraper
import os

class AutoUpdater:
    def __init__(self):
        self.aggregator = UniversalAggregator()
        self.running = False
        self.update_history = []
        self.last_update_time = None
        
    def load_existing_data(self, filename='scraped_data.json'):
        """Load existing scraped data to avoid duplicates"""
        if os.path.exists(filename):
            try:
                import json
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'data' in data:
                        self.aggregator.all_data = data['data']
                        print(f"✓ Loaded {len(self.aggregator.all_data)} existing records")
                        return True
            except Exception as e:
                print(f"Could not load existing data: {e}")
        return False
    
    def update_category(self, category_key, category_config):
        """Update a single category"""
        print(f"\n[UPDATE] Scraping {category_key}...")
        try:
            query = category_config['query']
            platforms = category_config['platforms']
            category_type = category_config.get('type', 'general')
            max_results = SCRAPER_SETTINGS.get('max_results_per_category', 100) // len(platforms)
            
            records_found = 0
            
            for platform in platforms:
                try:
                    records = []
                    if platform == 'youtube':
                        scraper = YouTubeScraper(headless=SCRAPER_SETTINGS['headless'])
                        records = scraper.search_videos(query, max_results=max_results)
                        scraper.close()
                    elif platform == 'wikipedia':
                        scraper = WikipediaScraper()
                        records = scraper.search_articles(query, max_results=max_results)
                    elif platform == 'google':
                        scraper = GoogleSearchScraper(headless=SCRAPER_SETTINGS['headless'])
                        records = scraper.search(query, search_type='all', max_results=max_results)
                        scraper.close()
                    
                    for record in records:
                        record['category'] = category_key
                        record['type'] = category_type
                        self.aggregator.add_record(record)
                    
                    records_found += len(records)
                    time.sleep(SCRAPER_SETTINGS['delay_between_requests'])
                    
                except Exception as e:
                    print(f"  Error on {platform}: {e}")
                    continue
            
            self.update_history.append({
                'category': category_key,
                'records_found': records_found,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✓ Updated {category_key}: {records_found} new records")
            return records_found
            
        except Exception as e:
            print(f"✗ Error updating {category_key}: {e}")
            return 0
    
    def save_data(self, base_filename='auto_updated_data'):
        """Save data to all formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{base_filename}_{timestamp}"
        
        files = self.aggregator.export_all_formats(filename)
        
        # Also save with standard name (latest)
        self.aggregator.export_all_formats(base_filename)
        
        self.last_update_time = datetime.now()
        return files
    
    def run_update_cycle(self, categories_to_update=None):
        """Run one update cycle for specified categories"""
        if categories_to_update is None:
            categories_to_update = list(GLOBAL_CATEGORIES.keys())
        
        print(f"\n{'='*70}")
        print(f"🔄 AUTO-UPDATE CYCLE STARTED")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Categories to update: {len(categories_to_update)}")
        print(f"{'='*70}\n")
        
        total_new_records = 0
        
        for category_key in categories_to_update:
            if not self.running:
                break
            
            category_config = GLOBAL_CATEGORIES[category_key]
            records = self.update_category(category_key, category_config)
            total_new_records += records
            
            # Save periodically (every 5 categories)
            if categories_to_update.index(category_key) % 5 == 4:
                print("\n[SAVE] Periodic save...")
                self.save_data()
                time.sleep(2)
        
        # Final save
        print("\n[SAVE] Final save...")
        files = self.save_data()
        
        print(f"\n{'='*70}")
        print(f"✅ UPDATE CYCLE COMPLETE")
        print(f"Total new records: {total_new_records}")
        print(f"Total records in database: {len(self.aggregator.all_data)}")
        print(f"Files saved: {', '.join(files.keys())}")
        print(f"{'='*70}\n")
        
        return total_new_records
    
    def start_continuous_mode(self, update_interval_hours=24, categories=None):
        """Start continuous auto-update mode"""
        self.running = True
        
        # Load existing data
        self.load_existing_data()
        
        print(f"\n{'='*70}")
        print(f"🚀 CONTINUOUS AUTO-UPDATE MODE STARTED")
        print(f"{'='*70}")
        print(f"Update interval: Every {update_interval_hours} hours")
        print(f"Categories: {len(categories) if categories else 'All'}")
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nPress Ctrl+C to stop")
        print(f"{'='*70}\n")
        
        if categories is None:
            categories = list(GLOBAL_CATEGORIES.keys())
        
        # Schedule updates
        schedule.every(update_interval_hours).hours.do(
            lambda: self.run_update_cycle(categories)
        )
        
        # Run first update immediately
        self.run_update_cycle(categories)
        
        # Keep running
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Stopping auto-updater...")
            self.stop()
    
    def start_background_mode(self, update_interval_hours=24, categories=None):
        """Start auto-update in background thread"""
        def run_background():
            self.start_continuous_mode(update_interval_hours, categories)
        
        thread = threading.Thread(target=run_background, daemon=True)
        thread.start()
        return thread
    
    def stop(self):
        """Stop the auto-updater"""
        self.running = False
        schedule.clear()
        print("✓ Auto-updater stopped")
    
    def get_status(self):
        """Get current status"""
        return {
            'running': self.running,
            'total_records': len(self.aggregator.all_data),
            'last_update': self.last_update_time.isoformat() if self.last_update_time else None,
            'update_count': len(self.update_history),
            'recent_updates': self.update_history[-5:] if self.update_history else []
        }

