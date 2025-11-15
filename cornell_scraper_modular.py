"""
Cornell Dining Hall Data Scraper
Fetches dining hall data from Cornell's API and transforms it for Bhookh Buster
"""

import requests
import json
import random
from datetime import datetime, timedelta
from config import Config
import os


class CornellDiningScraper:
    """Scraper for Cornell dining hall data"""
    
    def __init__(self):
        self.api_urls = Config.CORNELL_API_URLS
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_dining_data(self):
        """Fetch data from Cornell dining API"""
        print("🌐 Fetching Cornell dining data from API...")
        
        for api_url in self.api_urls:
            try:
                response = requests.get(api_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    print(f"✓ Successfully fetched data from {api_url}")
                    return response.json()
            except requests.RequestException as e:
                print(f"✗ Error fetching from {api_url}: {e}")
                continue
        
        print("⚠️  Could not fetch data from any API endpoint")
        return None
    
    def transform_for_bhookh_buster(self, raw_data):
        """Transform Cornell API data to Bhookh Buster format"""
        if not raw_data:
            return None
        
        print("🔄 Transforming data to Bhookh Buster format...")
        
        # Handle different data structures
        if isinstance(raw_data, dict) and 'data' in raw_data:
            eateries = raw_data['data'].get('eateries', [])
        elif isinstance(raw_data, list):
            eateries = raw_data
        else:
            print("⚠️  Unknown data format")
            return None
        
        restaurants = []
        food_items = []
        
        for idx, eatery in enumerate(eateries):
            restaurant_data = self._process_eatery(eatery, idx)
            restaurants.append(restaurant_data)
            
            # Generate menu items for this restaurant
            menu_items = self._generate_menu_items(
                restaurant_data['id'],
                restaurant_data['name'],
                restaurant_data['cuisine_type']
            )
            food_items.extend(menu_items)
        
        print(f"✓ Processed {len(restaurants)} dining halls")
        print(f"✓ Generated {len(food_items)} menu items")
        
        return {
            'restaurants': restaurants,
            'food_items': food_items,
            'timestamp': datetime.now().isoformat()
        }
    
    def _process_eatery(self, eatery, idx):
        """Process a single eatery from API data"""
        eatery_id = f"R{str(idx+1).zfill(3)}"
        name = eatery.get('name', eatery.get('displayName', f'Dining Hall {idx+1}'))
        
        # Get location/campus area
        location = eatery.get('campusArea', {})
        if isinstance(location, dict):
            location = location.get('descr', 'Central Campus')
        elif not location:
            location = 'Central Campus'
        
        # Determine cuisine type based on name
        cuisine_type = self._determine_cuisine_type(name)
        
        return {
            'id': eatery_id,
            'name': name,
            'location': location,
            'cuisine_type': cuisine_type
        }
    
    def _determine_cuisine_type(self, name):
        """Determine cuisine type from dining hall name"""
        name_lower = name.lower()
        
        if 'cafe' in name_lower or 'coffee' in name_lower:
            return 'Cafe'
        elif 'grill' in name_lower:
            return 'American'
        elif 'market' in name_lower:
            return 'Market'
        else:
            return 'Dining Hall'
    
    def _generate_menu_items(self, restaurant_id, restaurant_name, cuisine_type):
        """Generate sample menu items based on dining hall type"""
        
        menu_templates = {
            'Dining Hall': [
                ('Pasta Station Special', 'italian', 280),
                ('Stir Fry Bowl', 'asian', 250),
                ('Salad Bar Selection', 'healthy', 200),
                ('Sandwich Station', 'american', 220),
                ('Pizza Slice', 'italian', 180),
                ('Veggie Burger', 'vegetarian', 190),
                ('Chicken Wrap', 'american', 240),
                ('Rice Bowl', 'asian', 230)
            ],
            'Cafe': [
                ('Espresso Drink', 'beverage', 150),
                ('Pastry Selection', 'bakery', 120),
                ('Panini', 'italian', 240),
                ('Salad Bowl', 'healthy', 210),
                ('Smoothie', 'healthy', 160),
                ('Breakfast Sandwich', 'american', 190)
            ],
            'American': [
                ('Burger Combo', 'american', 300),
                ('Chicken Wings', 'american', 280),
                ('Fries Basket', 'american', 150),
                ('Club Sandwich', 'american', 260),
                ('BBQ Platter', 'american', 320),
                ('Mac and Cheese', 'american', 210)
            ],
            'Market': [
                ('Grab & Go Salad', 'healthy', 190),
                ('Sushi Roll', 'asian', 320),
                ('Sandwich Wrap', 'american', 210),
                ('Fruit Cup', 'healthy', 140),
                ('Protein Box', 'healthy', 260),
                ('Veggie Sushi', 'vegetarian', 290)
            ]
        }
        
        templates = menu_templates.get(cuisine_type, menu_templates['Dining Hall'])
        num_items = random.randint(3, min(6, len(templates)))
        selected = random.sample(templates, num_items)
        
        items = []
        for idx, (item_name, food_type, base_price) in enumerate(selected):
            # Random expiry time (2-10 hours from now)
            expiry_hours = random.choice([2, 3, 4, 6, 7, 8, 10])
            expiry = datetime.now() + timedelta(hours=expiry_hours)
            
            items.append({
                'restaurant_id': restaurant_id,
                'item_id': f"{restaurant_id}_F{str(idx+1).zfill(3)}",
                'name': item_name,
                'food_type': food_type,
                'original_price': base_price + random.randint(-20, 50),
                'expiry': expiry.isoformat(),
                'quantity': random.randint(1, 5)
            })
        
        return items
    
    def save_data(self, data, filename=None):
        """Save transformed data to JSON file"""
        if not data:
            print("⚠️  No data to save")
            return False
        
        # Create data directory if it doesn't exist
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        
        # Use default filename if not provided
        if not filename:
            filename = Config.DINING_DATA_FILE
        
        filepath = os.path.join(Config.DATA_DIR, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Data saved to {filepath}")
            return True
        except Exception as e:
            print(f"✗ Error saving data: {e}")
            return False
    
    def run(self):
        """Main scraper workflow"""
        print("\n" + "="*60)
        print("Cornell Dining Data Scraper")
        print("="*60 + "\n")
        
        # Fetch data
        raw_data = self.fetch_dining_data()
        
        if not raw_data:
            print("\n⚠️  Could not fetch dining data from API")
            print("The app will use demo data as fallback\n")
            return None
        
        # Transform data
        transformed_data = self.transform_for_bhookh_buster(raw_data)
        
        if not transformed_data:
            print("\n⚠️  Could not transform data")
            return None
        
        # Save data
        self.save_data(transformed_data)
        
        # Print summary
        print("\n" + "="*60)
        print("Summary:")
        print(f"  Dining Halls: {len(transformed_data['restaurants'])}")
        print(f"  Food Items: {len(transformed_data['food_items'])}")
        print("\nSample Dining Halls:")
        for rest in transformed_data['restaurants'][:5]:
            print(f"  • {rest['name']} ({rest['location']}) - {rest['cuisine_type']}")
        print("="*60 + "\n")
        
        return transformed_data


def main():
    """Run the scraper"""
    scraper = CornellDiningScraper()
    scraper.run()


if __name__ == "__main__":
    main()
