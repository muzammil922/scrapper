"""
Universal Data Aggregator - Combines data from all sources
"""

import pandas as pd
import json
import re
from datetime import datetime
from generic_config import UNIVERSAL_DATA_FIELDS, SCRAPER_SETTINGS
from pdf_exporter import PDFExporter

class UniversalAggregator:
    def __init__(self):
        self.all_data = []
        self.stats = {
            'total_records': 0,
            'by_platform': {},
            'by_category': {},
            'by_type': {}
        }
        self.pdf_exporter = PDFExporter()
    
    def add_record(self, record):
        """Add a record to the collection"""
        if record and isinstance(record, dict):
            # Ensure required fields
            if 'scraped_date' not in record:
                record['scraped_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            self.all_data.append(record)
            self.update_stats(record)
    
    def add_records(self, records):
        """Add multiple records"""
        for record in records:
            self.add_record(record)
    
    def update_stats(self, record):
        """Update statistics"""
        self.stats['total_records'] = len(self.all_data)
        
        platform = record.get('platform', 'unknown')
        self.stats['by_platform'][platform] = self.stats['by_platform'].get(platform, 0) + 1
        
        category = record.get('category', 'unknown')
        self.stats['by_category'][category] = self.stats['by_category'].get(category, 0) + 1
        
        type_val = record.get('type', 'unknown')
        self.stats['by_type'][type_val] = self.stats['by_type'].get(type_val, 0) + 1
    
    def export_to_csv(self, filename='universal_scraped_data.csv'):
        """Export data to CSV"""
        if not self.all_data:
            print("No data to export!")
            return None
        
        df = pd.DataFrame(self.all_data)
        
        # Reorder columns to prioritize universal fields
        existing_universal = [col for col in UNIVERSAL_DATA_FIELDS if col in df.columns]
        other_columns = [col for col in df.columns if col not in UNIVERSAL_DATA_FIELDS]
        df = df[existing_universal + other_columns]
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✓ Data exported to {filename}")
        print(f"Total records: {len(df)}")
        return filename
    
    def export_to_excel(self, filename='universal_scraped_data.xlsx'):
        """Export data to Excel with multiple sheets by category"""
        if not self.all_data:
            print("No data to export!")
            return None
        
        df = pd.DataFrame(self.all_data)
        
        # Reorder columns
        existing_universal = [col for col in UNIVERSAL_DATA_FIELDS if col in df.columns]
        other_columns = [col for col in df.columns if col not in UNIVERSAL_DATA_FIELDS]
        df = df[existing_universal + other_columns]
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # All data sheet
            df.to_excel(writer, index=False, sheet_name='All Data')
            
            # Category-wise sheets
            if 'category' in df.columns:
                categories = df['category'].unique()
                for category in categories[:20]:  # Limit to 20 sheets
                    cat_data = df[df['category'] == category]
                    sheet_name = str(category)[:31]  # Excel sheet name limit
                    cat_data.to_excel(writer, index=False, sheet_name=sheet_name)
            
            # Platform-wise sheets
            if 'platform' in df.columns:
                platforms = df['platform'].unique()
                for platform in platforms[:10]:
                    platform_data = df[df['platform'] == platform]
                    sheet_name = str(platform)[:31]
                    platform_data.to_excel(writer, index=False, sheet_name=sheet_name)
        
        print(f"\n✓ Data exported to {filename}")
        print(f"Total records: {len(df)}")
        return filename
    
    def export_to_json(self, filename='universal_scraped_data.json'):
        """Export data to JSON"""
        if not self.all_data:
            print("No data to export!")
            return None
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total_records': len(self.all_data),
                    'scraped_date': datetime.now().isoformat(),
                    'statistics': self.stats
                },
                'data': self.all_data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Data exported to {filename}")
        print(f"Total records: {len(self.all_data)}")
        return filename
    
    def get_statistics(self):
        """Get scraping statistics"""
        return {
            'total_records': len(self.all_data),
            'by_platform': self.stats['by_platform'],
            'by_category': self.stats['by_category'],
            'by_type': self.stats['by_type'],
            'fields_present': list(set([field for record in self.all_data for field in record.keys()]))
        }
    
    def filter_by_category(self, category):
        """Filter records by category"""
        return [r for r in self.all_data if r.get('category') == category]
    
    def filter_by_platform(self, platform):
        """Filter records by platform"""
        return [r for r in self.all_data if r.get('platform') == platform]
    
    def filter_by_type(self, type_val):
        """Filter records by type"""
        return [r for r in self.all_data if r.get('type') == type_val]
    
    def get_top_records(self, sort_by='views', limit=100):
        """Get top records sorted by a field"""
        if not self.all_data:
            return []
        
        # Convert views to numbers for sorting
        sortable_data = []
        for record in self.all_data:
            record_copy = record.copy()
            views = record.get('views', 0)
            if isinstance(views, str):
                # Try to parse "1.2M" format
                try:
                    if 'm' in views.lower():
                        record_copy['_sort_views'] = float(views.lower().replace('m', '')) * 1000000
                    elif 'k' in views.lower():
                        record_copy['_sort_views'] = float(views.lower().replace('k', '')) * 1000
                    else:
                        record_copy['_sort_views'] = float(views.replace(',', ''))
                except:
                    record_copy['_sort_views'] = 0
            else:
                record_copy['_sort_views'] = views or 0
            sortable_data.append(record_copy)
        
        sorted_data = sorted(sortable_data, key=lambda x: x.get('_sort_views', 0), reverse=True)
        
        # Remove temporary sort field
        for record in sorted_data:
            record.pop('_sort_views', None)
        
        return sorted_data[:limit]
    
    def export_to_pdf(self, filename='scraped_data_report.pdf', category_specific=False):
        """Export data to PDF with beautiful formatting"""
        if not self.all_data:
            print("No data to export to PDF!")
            return None
        
        stats = self.get_statistics()
        
        if category_specific:
            # Export each category as separate PDF
            from collections import defaultdict
            by_category = defaultdict(list)
            for record in self.all_data:
                category = record.get('category', 'Unknown')
                by_category[category].append(record)
            
            pdf_files = []
            for category, records in by_category.items():
                safe_name = str(category).replace(' ', '_').replace('/', '_')[:50]
                pdf_file = f"{safe_name}_report.pdf"
                result = self.pdf_exporter.export_category_pdf(records, category, pdf_file)
                if result:
                    pdf_files.append(result)
            
            print(f"\n✓ Exported {len(pdf_files)} category-specific PDF files")
            return pdf_files
        else:
            # Export all data to one PDF
            return self.pdf_exporter.export_data_to_pdf(self.all_data, stats, filename)
    
    def export_all_formats(self, base_filename='scraped_data'):
        """Export to all formats: CSV, Excel, JSON, and PDF"""
        files = {}
        
        # CSV
        csv_file = self.export_to_csv(f'{base_filename}.csv')
        if csv_file:
            files['csv'] = csv_file
        
        # Excel
        excel_file = self.export_to_excel(f'{base_filename}.xlsx')
        if excel_file:
            files['excel'] = excel_file
        
        # JSON
        json_file = self.export_to_json(f'{base_filename}.json')
        if json_file:
            files['json'] = json_file
        
        # PDF
        pdf_file = self.export_to_pdf(f'{base_filename}_report.pdf')
        if pdf_file:
            files['pdf'] = pdf_file
        
        return files

