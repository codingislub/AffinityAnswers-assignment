#!/usr/bin/env python3
"""
Manual OLX Data Collector
Since automated scraping is blocked, this tool helps you collect data manually
"""

import csv
import json
import re
from datetime import datetime
import os

class ManualOLXCollector:
    def __init__(self):
        self.results = []
        
    def collect_data_interactively(self):
        """Interactive data collection"""
        print("Manual OLX Car Cover Data Collector")
        print("=" * 50)
        print("Instructions:")
        print("1. Open https://www.olx.in/items/q-car-cover in your browser")
        print("2. For each listing, copy and paste the information when prompted")
        print("3. Type 'done' when you've collected all the data you want")
        print("4. Leave fields blank (press Enter) if information isn't available")
        print("\n" + "=" * 50)
        
        item_count = 1
        
        while True:
            print(f"\n--- ITEM {item_count} ---")
            
            title = input("Title: ").strip()
            if title.lower() == 'done':
                break
                
            if not title:
                print("Skipping empty item...")
                continue
                
            price = input("Price: ").strip()
            location = input("Location: ").strip()
            description = input("Description (optional): ").strip()
            url = input("URL (optional): ").strip()
            
            # Store the data
            item = {
                'item_number': item_count,
                'title': title,
                'price': price,
                'location': location,
                'description': description,
                'url': url,
                'collected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.results.append(item)
            print(f"✓ Item {item_count} saved!")
            
            # Ask if user wants to continue
            continue_choice = input("\nAdd another item? (y/n): ").strip().lower()
            if continue_choice in ['n', 'no']:
                break
                
            item_count += 1
        
        return self.results
    
    def collect_from_text_paste(self):
        """Collect data from a large text paste"""
        print("Text Paste Data Collector")
        print("=" * 30)
        print("Instructions:")
        print("1. Go to https://www.olx.in/items/q-car-cover")
        print("2. Copy ALL the listing data from the page")
        print("3. Paste it below (Press Enter twice when done)")
        print()
        
        lines = []
        print("Paste your data here:")
        while True:
            try:
                line = input()
                if not line:
                    break
                lines.append(line)
            except EOFError:
                break
        
        text_data = '\n'.join(lines)
        return self.parse_pasted_text(text_data)
    
    def parse_pasted_text(self, text_data):
        """Parse pasted text data to extract listings"""
        results = []
        
        # Split by common separators that might appear between listings
        # Fixed regex pattern to avoid lookbehind issues
        potential_items = re.split(r'\n\s*\n|\n(?=.*₹)', text_data)
        
        item_count = 1
        for item_text in potential_items:
            if not item_text.strip():
                continue
                
            lines = [line.strip() for line in item_text.split('\n') if line.strip()]
            
            if len(lines) < 2:
                continue
            
            # Try to identify title, price, location
            title = ""
            price = ""
            location = ""
            description = ""
            
            for line in lines:
                # Look for price (contains ₹ or Rs)
                if '₹' in line or 'Rs' in line or 'INR' in line:
                    if not price:  # Take the first price found
                        price = line
                # Look for location (common location indicators)
                elif any(word in line.lower() for word in ['delhi', 'mumbai', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 'pune', 'ahmedabad', 'city', 'nagar']):
                    if not location:
                        location = line
                # First meaningful line is likely the title
                elif not title and len(line) > 10:
                    title = line
                # Everything else goes to description
                else:
                    if description:
                        description += " " + line
                    else:
                        description = line
            
            if title:  # Only add if we found at least a title
                result = {
                    'item_number': item_count,
                    'title': title,
                    'price': price,
                    'location': location,
                    'description': description[:200],  # Limit description length
                    'url': '',
                    'collected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                results.append(result)
                item_count += 1
        
        print(f"Parsed {len(results)} items from the pasted text")
        return results
    
    def collect_from_csv_input(self):
        """Allow user to input data in CSV format"""
        print("CSV Format Data Collector")
        print("=" * 30)
        print("Enter data in CSV format: Title,Price,Location,Description")
        print("Example: Car Cover Universal,₹500,Delhi,Waterproof car cover")
        print("Press Enter on empty line when done")
        print()
        
        results = []
        item_count = 1
        
        while True:
            try:
                line = input(f"Item {item_count}: ").strip()
                if not line:
                    break
                
                parts = [part.strip() for part in line.split(',')]
                if len(parts) >= 2:  # At least title and price
                    result = {
                        'item_number': item_count,
                        'title': parts[0],
                        'price': parts[1] if len(parts) > 1 else '',
                        'location': parts[2] if len(parts) > 2 else '',
                        'description': parts[3] if len(parts) > 3 else '',
                        'url': '',
                        'collected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    results.append(result)
                    item_count += 1
                    print(f"  ✓ Added: {parts[0]}")
                else:
                    print("  ✗ Invalid format. Use: Title,Price,Location,Description")
                    
            except EOFError:
                break
        
        return results
    
    def save_results(self, results, filename_prefix="olx_manual_collection"):
        """Save results to CSV and JSON files"""
        if not results:
            print("No data to save!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to CSV
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['item_number', 'title', 'price', 'location', 'description', 'url', 'collected_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        # Save to JSON
        json_filename = f"{filename_prefix}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(results, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Data saved successfully:")
        print(f"  📄 CSV: {csv_filename}")
        print(f"  📄 JSON: {json_filename}")
        print(f"  📊 Total items: {len(results)}")
        
        # Show summary
        self.show_summary(results)
        
        return csv_filename, json_filename
    
    def show_summary(self, results):
        """Show a summary of collected data"""
        print(f"\n📋 COLLECTION SUMMARY")
        print("=" * 40)
        
        for i, item in enumerate(results[:5], 1):  # Show first 5 items
            print(f"{i}. {item['title']}")
            if item['price']:
                print(f"   💰 {item['price']}")
            if item['location']:
                print(f"   📍 {item['location']}")
            print()
        
        if len(results) > 5:
            print(f"... and {len(results) - 5} more items")
    
    def run(self):
        """Main menu"""
        print("🚗 OLX Car Cover Data Collector")
        print("=" * 40)
        print("Choose your preferred method:")
        print("1. Interactive entry (one by one)")
        print("2. Paste text data from OLX page")
        print("3. CSV format input")
        print("4. Exit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                
                if choice == '1':
                    results = self.collect_data_interactively()
                    break
                elif choice == '2':
                    results = self.collect_from_text_paste()
                    break
                elif choice == '3':
                    results = self.collect_from_csv_input()
                    break
                elif choice == '4':
                    print("Goodbye!")
                    return
                else:
                    print("Invalid choice. Please enter 1-4.")
                    
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return
        
        if results:
            self.save_results(results)
            print(f"\n🎉 Successfully collected {len(results)} items!")
        else:
            print("No data collected.")

def main():
    collector = ManualOLXCollector()
    collector.run()

if __name__ == "__main__":
    main()