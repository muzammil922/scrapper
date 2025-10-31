"""
PDF Exporter - Beautiful formatted PDF reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

class PDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Heading style
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Subheading style
        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        )
        
        # Normal text style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            alignment=TA_LEFT,
            leading=14
        )
        
        # Metadata style
        self.meta_style = ParagraphStyle(
            'MetaStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_LEFT
        )
    
    def export_data_to_pdf(self, data, stats, filename='scraped_data_report.pdf'):
        """Export data to a beautifully formatted PDF"""
        try:
            doc = SimpleDocTemplate(
                filename,
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            story = []
            
            # Cover Page
            story.append(Spacer(1, 2*inch))
            story.append(Paragraph("🌍 Universal Data Scraper", self.title_style))
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("Comprehensive Data Report", self.heading_style))
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.meta_style))
            story.append(PageBreak())
            
            # Statistics Page
            story.append(Paragraph("📊 Statistics Overview", self.heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Stats table
            stats_data = [
                ['Metric', 'Value'],
                ['Total Records', str(stats.get('total_records', 0))],
                ['Total Platforms', str(len(stats.get('by_platform', {})))],
                ['Total Categories', str(len(stats.get('by_category', {})))],
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Platform breakdown
            if stats.get('by_platform'):
                story.append(Paragraph("Platform Distribution", self.subheading_style))
                platform_data = [['Platform', 'Records']]
                for platform, count in sorted(stats['by_platform'].items(), key=lambda x: x[1], reverse=True):
                    platform_data.append([platform.title(), str(count)])
                
                platform_table = Table(platform_data, colWidths=[4*inch, 2*inch])
                platform_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ]))
                story.append(platform_table)
                story.append(Spacer(1, 0.3*inch))
            
            # Category breakdown
            if stats.get('by_category'):
                story.append(Paragraph("Category Distribution", self.subheading_style))
                category_data = [['Category', 'Records']]
                for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True)[:10]:
                    category_data.append([category.replace('_', ' ').title(), str(count)])
                
                category_table = Table(category_data, colWidths=[4*inch, 2*inch])
                category_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ]))
                story.append(category_table)
            
            story.append(PageBreak())
            
            # Data Records (sample - first 50 to keep PDF manageable)
            story.append(Paragraph("📋 Data Records", self.heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Group by category
            from collections import defaultdict
            by_category = defaultdict(list)
            for record in data:
                category = record.get('category', 'Unknown')
                by_category[category].append(record)
            
            for category, records in list(by_category.items())[:10]:  # Limit categories
                story.append(Paragraph(f"Category: {category.replace('_', ' ').title()}", self.subheading_style))
                story.append(Spacer(1, 0.1*inch))
                
                # Show sample records per category (max 20 per category)
                for i, record in enumerate(records[:20], 1):
                    story.append(Paragraph(f"<b>{i}. {record.get('title', record.get('name', 'N/A'))}</b>", self.normal_style))
                    
                    # Add key fields
                    fields_to_show = ['platform', 'url', 'description', 'views', 'author']
                    field_text = []
                    for field in fields_to_show:
                        if field in record and record[field]:
                            value = str(record[field])[:100]  # Limit length
                            field_text.append(f"<b>{field.title()}:</b> {value}")
                    
                    if field_text:
                        story.append(Paragraph(" | ".join(field_text), self.meta_style))
                    
                    story.append(Spacer(1, 0.15*inch))
                
                if len(records) > 20:
                    story.append(Paragraph(f"... and {len(records) - 20} more records in this category", self.meta_style))
                
                story.append(Spacer(1, 0.2*inch))
                
                # Page break if needed (every 3 categories)
                if list(by_category.keys()).index(category) % 3 == 2:
                    story.append(PageBreak())
            
            # Build PDF
            doc.build(story)
            print(f"\n✓ PDF exported to {filename}")
            return filename
            
        except Exception as e:
            print(f"Error creating PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def export_category_pdf(self, category_data, category_name, filename=None):
        """Export a specific category to PDF"""
        if not filename:
            safe_name = category_name.replace(' ', '_').replace('/', '_')[:50]
            filename = f"{safe_name}_data.pdf"
        
        stats = {
            'total_records': len(category_data),
            'by_platform': {},
            'by_category': {category_name: len(category_data)}
        }
        
        # Count by platform
        for record in category_data:
            platform = record.get('platform', 'unknown')
            stats['by_platform'][platform] = stats['by_platform'].get(platform, 0) + 1
        
        return self.export_data_to_pdf(category_data, stats, filename)

