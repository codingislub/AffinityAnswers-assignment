#!/usr/bin/env python3
"""
Process the OLX data that was already collected
"""

import csv
import json
from datetime import datetime

# Your OLX data extracted from the paste
olx_data = [
    {
        "title": "Eeco car set heavy set he cover bhi heavy he",
        "price": "₹ 5,000",
        "location": "Deendayal Nagar, Ratlam",
        "date": "Today"
    },
    {
        "title": "Seltos car cover",
        "price": "₹ 1,500",
        "location": "North Paravoor, Paravur",
        "date": "Today"
    },
    {
        "title": "All cars side mirror batman cover abs plastic piano black",
        "price": "₹ 2,999",
        "location": "Ashok Nagar, Vijayawada",
        "date": "Yesterday"
    },
    {
        "title": "All cars side mirror cover batman style abs",
        "price": "₹ 2,500",
        "location": "Chembur, Mumbai",
        "date": "Yesterday"
    },
    {
        "title": "All cars side mirror covers abs",
        "price": "₹ 1,999",
        "location": "Alappuzha Cantt, Alappuzha",
        "date": "Yesterday"
    },
    {
        "title": "Waterproof Car Cover - Grand i10 Nios",
        "price": "₹ 750",
        "location": "Wagholi, Pune",
        "date": "Yesterday"
    },
    {
        "title": "Car key cover",
        "price": "₹ 300",
        "location": "New Mandi, Muzaffarnagar",
        "date": "Yesterday"
    },
    {
        "title": "Car cover - Chevrolet Sail sedan",
        "price": "₹ 600",
        "location": "Anandapura, Bengaluru",
        "date": "Yesterday"
    },
    {
        "title": "Wagon R Car Cover New",
        "price": "₹ 599",
        "location": "Calicut Medical College, Kozhikode",
        "date": "Yesterday"
    },
    {
        "title": "Car steering Cover",
        "price": "₹ 350",
        "location": "Maligaon, Guwahati",
        "date": "Yesterday"
    },
    {
        "title": "Venue car cover waterproof",
        "price": "Not specified",
        "location": "Daliml Vihar, Rajpura",
        "date": "Yesterday"
    },
    {
        "title": "Green Stone car seat cover, manufacturing and entertainment",
        "price": "₹ 4,500",
        "location": "Triplicane Chepauk Police Quarters, Chennai",
        "date": "Yesterday"
    },
    {
        "title": "All cars side mirror batman cover abs plastic piano black",
        "price": "₹ 2,499",
        "location": "Gangtok Private Estate, Gangtok",
        "date": "2 days ago"
    },
    {
        "title": "All cars side mirror cover batman style abs plastic piano black",
        "price": "₹ 2,500",
        "location": "Anna Nagar, Madurai",
        "date": "2 days ago"
    },
    {
        "title": "Brand new swift car cover",
        "price": "Not specified",
        "location": "Deen Dayal Nagar, Gwalior",
        "date": "2 days ago"
    },
    {
        "title": "Branded New Waterproof Car Body Cover-UV Protection,Heavy Duty",
        "price": "₹ 2,000",
        "location": "Srirampura Stage 2 Madhuvana Layout, Mysuru",
        "date": "2 days ago"
    },
    {
        "title": "KWID CAR COVER (Waterproof and Dust proof)",
        "price": "₹ 600",
        "location": "Rajendra Nagar Sector 2, Ghaziabad",
        "date": "2 days ago"
    },
    {
        "title": "modern manufactur car seat cover and full floor mat",
        "price": "Not specified",
        "location": "Gachibowli, Hyderabad",
        "date": "2 days ago"
    },
    {
        "title": "Renault Kwid Car Jute Material Front & Back Seat Covers",
        "price": "₹ 1,500",
        "location": "Vijay Nagar, Sangli (-Miraj)",
        "date": "3 days ago"
    },
    {
        "title": "Innova car cover brand new",
        "price": "₹ 1,000",
        "location": "Viman Nagar, Pune",
        "date": "3 days ago"
    },
    {
        "title": "Wheel cover brezza car good condition orignal",
        "price": "₹ 600",
        "location": "Lal Bara, Manglaur",
        "date": "3 days ago"
    },
    {
        "title": "Car seat covers and flooring mats",
        "price": "Not specified",
        "location": "RT Nagar, Bengaluru",
        "date": "3 days ago"
    },
    {
        "title": "Car cover original Hyundai",
        "price": "₹ 900",
        "location": "Parsi Falia, Kavant",
        "date": "3 days ago"
    },
    {
        "title": "Car Body cover",
        "price": "₹ 3,000",
        "location": "Chromepet Radha Nagar, Chennai",
        "date": "3 days ago"
    },
    {
        "title": "Car Covers",
        "price": "₹ 1,250",
        "location": "Gokul Nagar, Jamnagar",
        "date": "3 days ago"
    },
    {
        "title": "Hyundai i10 car cover",
        "price": "₹ 700",
        "location": "Kolathur City Babu Nagar, Chennai",
        "date": "3 days ago"
    },
    {
        "title": "I10 car cover new condition -very few time used",
        "price": "₹ 900",
        "location": "Shela, Ahmedabad",
        "date": "3 days ago"
    },
    {
        "title": "Maruthi Ertiga Car Leather Seat Cover 3D Mats Basic Advanced System",
        "price": "₹ 4,000",
        "location": "Gabbalalu, Bengaluru",
        "date": "3 days ago"
    },
    {
        "title": "Car cover ( santro)",
        "price": "₹ 960",
        "location": "Anaiyur, Madurai",
        "date": "3 days ago"
    },
    {
        "title": "Car Wheel Cover 15 Inch - 4 Piece",
        "price": "₹ 600",
        "location": "Kavi Nagar Jila Panchayat Colony, Ghaziabad",
        "date": "3 days ago"
    },
    {
        "title": "Brembo brake caliper covers all colours available for all cars",
        "price": "₹ 699",
        "location": "Begumpet, Hyderabad",
        "date": "4 days ago"
    },
    {
        "title": "Mahindra XUV 3X0 Original Unused Car Cover",
        "price": "₹ 1,000",
        "location": "Vasai East, Mumbai",
        "date": "4 days ago"
    },
    {
        "title": "MARUTI ALTO CAR COVER FOR SALE",
        "price": "₹ 700",
        "location": "Baner - Mahalunge Road, Pune",
        "date": "4 days ago"
    }
]

def save_to_files():
    """Save the extracted data to CSV and JSON files"""
    
    # Add additional fields
    processed_data = []
    for i, item in enumerate(olx_data, 1):
        processed_item = {
            'item_number': i,
            'title': item['title'],
            'price': item['price'],
            'location': item['location'],
            'date_posted': item['date'],
            'description': item['title'],  # Using title as description since that's what we have
            'url': '',  # Not available from the paste
            'collected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        processed_data.append(processed_item)
    
    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"olx_car_covers_{timestamp}.csv"
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['item_number', 'title', 'price', 'location', 'date_posted', 'description', 'url', 'collected_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)
    
    # Save to JSON
    json_filename = f"olx_car_covers_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(processed_data, jsonfile, indent=2, ensure_ascii=False)
    
    return csv_filename, json_filename, processed_data

def show_summary(data):
    """Display a summary of the data"""
    print(f"🚗 OLX CAR COVER SEARCH RESULTS")
    print("=" * 60)
    print(f"📊 Total items found: {len(data)}")
    
    # Price analysis
    prices = []
    for item in data:
        price_str = item['price']
        if price_str != "Not specified" and "₹" in price_str:
            # Extract number from price string
            price_num = ''.join(filter(str.isdigit, price_str.replace(',', '')))
            if price_num:
                prices.append(int(price_num))
    
    if prices:
        print(f"💰 Price range: ₹{min(prices)} - ₹{max(prices)}")
        print(f"💰 Average price: ₹{sum(prices)//len(prices)}")
    
    # Location analysis
    locations = {}
    for item in data:
        city = item['location'].split(',')[-1].strip()
        locations[city] = locations.get(city, 0) + 1
    
    print(f"\n📍 Top locations:")
    sorted_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)
    for city, count in sorted_locations[:5]:
        print(f"   {city}: {count} listings")
    
    print(f"\n🔝 Sample listings:")
    print("-" * 60)
    for i, item in enumerate(data[:10], 1):
        print(f"{i:2d}. {item['title']}")
        print(f"    💰 {item['price']} | 📍 {item['location']} | 📅 {item['date_posted']}")
        print()
    
    if len(data) > 10:
        print(f"... and {len(data) - 10} more items")

def main():
    print("Processing your OLX car cover data...")
    print("=" * 50)
    
    csv_file, json_file, data = save_to_files()
    
    print(f"✅ Data successfully saved:")
    print(f"   📄 CSV: {csv_file}")
    print(f"   📄 JSON: {json_file}")
    print()
    
    show_summary(data)
    
    print(f"\n🎉 SUCCESS! You now have {len(data)} car cover listings!")
    print("=" * 60)
    print("Files created:")
    print(f"• {csv_file} - Open with Excel")
    print(f"• {json_file} - For programming use")

if __name__ == "__main__":
    main()