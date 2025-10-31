"""
Data Aggregator to combine and export scraped data
"""

import pandas as pd
import re
from datetime import datetime
from config import DATA_FIELDS

class DataAggregator:
    def __init__(self):
        self.all_data = []
    
    def merge_data(self, google_data, website_data, social_data):
        """Merge data from all sources into a single record"""
        merged = {}
        
        # Start with Google Maps data
        if google_data:
            merged.update(google_data)
        
        # Add website data
        if website_data:
            # Merge email (prefer website email if available)
            if website_data.get('email') and website_data['email'] != "N/A":
                merged['email'] = website_data['email'] if not merged.get('email') else f"{merged['email']}, {website_data['email']}"
            
            # Merge phone (prefer website phone if available)
            if website_data.get('phone_from_website'):
                if not merged.get('phone') or merged['phone'] == "N/A":
                    merged['phone'] = website_data['phone_from_website']
            
            # Add other website fields
            merged.update({
                'established_year': website_data.get('established_year') or merged.get('established_year'),
                'description': website_data.get('description') or merged.get('description'),
                'services': website_data.get('services') or merged.get('services'),
            })
        
        # Add social media data
        if social_data:
            # Merge social media URLs
            merged.update({
                'facebook_url': social_data.get('facebook_url') or merged.get('facebook_url'),
                'instagram_url': social_data.get('instagram_url') or merged.get('instagram_url'),
                'tiktok_url': social_data.get('tiktok_url') or merged.get('tiktok_url'),
            })
            
            # Merge emails from social media
            email_sources = []
            if merged.get('email'):
                email_sources.append(merged['email'])
            if social_data.get('email_from_facebook'):
                email_sources.append(social_data['email_from_facebook'])
            if social_data.get('email_from_instagram'):
                email_sources.append(social_data['email_from_instagram'])
            
            if email_sources:
                merged['email'] = ', '.join(set(email_sources))
            
            # Merge phones from social media
            phone_sources = []
            if merged.get('phone') and merged['phone'] != "N/A":
                phone_sources.append(merged['phone'])
            if social_data.get('phone_from_facebook'):
                phone_sources.append(social_data['phone_from_facebook'])
            
            if phone_sources:
                merged['phone'] = ', '.join(set(phone_sources))
            
            # Add follower counts
            followers = {}
            if social_data.get('facebook_followers'):
                followers['Facebook'] = social_data['facebook_followers']
            if social_data.get('instagram_followers'):
                followers['Instagram'] = social_data['instagram_followers']
            if social_data.get('tiktok_followers'):
                followers['TikTok'] = social_data['tiktok_followers']
            
            if followers:
                merged['social_media_followers'] = ', '.join([f"{k}: {v}" for k, v in followers.items()])
        
        # Calculate traffic estimate (rough estimate based on reviews and followers)
        traffic = self.estimate_traffic(merged)
        merged['traffic_estimate'] = traffic
        
        # Add scraping metadata
        merged['scraped_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Extract city from address if available
        if merged.get('address') and not merged.get('city'):
            merged['city'] = self.extract_city(merged['address'])
        
        return merged
    
    def extract_city(self, address):
        """Extract city name from address"""
        from config import CITIES
        if not address or address == "N/A":
            return "N/A"
        
        address_lower = address.lower()
        for city in CITIES:
            if city.lower() in address_lower:
                return city
        
        return "N/A"
    
    def estimate_traffic(self, data):
        """Estimate traffic based on reviews and social media followers"""
        try:
            traffic_score = 0
            
            # Reviews contribute to traffic
            if data.get('review_count') and data['review_count'] != "0" and data['review_count'] != "N/A":
                try:
                    reviews = int(str(data['review_count']).replace(',', ''))
                    # Rough estimate: 10-20% of people who visit leave reviews
                    traffic_score += reviews * 10
                except:
                    pass
            
            # Social media followers contribute
            if data.get('social_media_followers'):
                followers_text = str(data['social_media_followers'])
                follower_nums = re.findall(r'(\d+)', followers_text)
                for num_str in follower_nums:
                    try:
                        traffic_score += int(num_str)
                    except:
                        pass
            
            if traffic_score == 0:
                return "Low (< 1K)"
            elif traffic_score < 5000:
                return f"Low-Medium ({traffic_score//1000}K-{traffic_score//500}K)"
            elif traffic_score < 20000:
                return f"Medium ({traffic_score//1000}K-{(traffic_score*2)//1000}K)"
            elif traffic_score < 100000:
                return f"Medium-High ({(traffic_score//1000)}K-{(traffic_score*2)//1000}K)"
            else:
                return f"High ({traffic_score//1000}K+)"
        
        except Exception as e:
            return "Unknown"
    
    def add_record(self, record):
        """Add a merged record to the collection"""
        self.all_data.append(record)
    
    def export_to_csv(self, filename='pakistan_hospitals_clinics_data.csv'):
        """Export data to CSV file"""
        if not self.all_data:
            print("No data to export!")
            return
        
        df = pd.DataFrame(self.all_data)
        
        # Reorder columns to match DATA_FIELDS
        existing_columns = [col for col in DATA_FIELDS if col in df.columns]
        other_columns = [col for col in df.columns if col not in DATA_FIELDS]
        df = df[existing_columns + other_columns]
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✓ Data exported to {filename}")
        print(f"Total records: {len(df)}")
        return filename
    
    def export_to_excel(self, filename='pakistan_hospitals_clinics_data.xlsx'):
        """Export data to Excel file"""
        if not self.all_data:
            print("No data to export!")
            return
        
        df = pd.DataFrame(self.all_data)
        
        # Reorder columns
        existing_columns = [col for col in DATA_FIELDS if col in df.columns]
        other_columns = [col for col in df.columns if col not in DATA_FIELDS]
        df = df[existing_columns + other_columns]
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Hospitals & Clinics')
        
        print(f"\n✓ Data exported to {filename}")
        print(f"Total records: {len(df)}")
        return filename
    
    def get_statistics(self):
        """Get statistics about scraped data"""
        if not self.all_data:
            return {}
        
        df = pd.DataFrame(self.all_data)
        
        stats = {
            'total_records': len(df),
            'categories': df['category'].value_counts().to_dict() if 'category' in df.columns else {},
            'cities': df['city'].value_counts().to_dict() if 'city' in df.columns else {},
            'with_emails': len(df[df['email'].notna() & (df['email'] != "N/A")]) if 'email' in df.columns else 0,
            'with_phones': len(df[df['phone'].notna() & (df['phone'] != "N/A")]) if 'phone' in df.columns else 0,
            'with_websites': len(df[df['website'].notna() & (df['website'] != "N/A")]) if 'website' in df.columns else 0,
            'with_facebook': len(df[df['facebook_url'].notna() & (df['facebook_url'] != "N/A")]) if 'facebook_url' in df.columns else 0,
            'with_instagram': len(df[df['instagram_url'].notna() & (df['instagram_url'] != "N/A")]) if 'instagram_url' in df.columns else 0,
        }
        
        return stats

