"""
Data Manager for Bhookh Buster
Handles loading and managing dining hall and food data
"""

import json
import os
import random
from datetime import datetime, timedelta
from models import Restaurant
from config import Config
from cornell_scraper_modular import CornellDiningScraper


class DataManager:
    """Manages data loading and initialization"""
    
    def __init__(self):
        self.restaurants = {}
        self.data_filepath = os.path.join(Config.DATA_DIR, Config.DINING_DATA_FILE)
    
    def load_dining_data(self):
        """Load dining data from file or fetch fresh data"""
        
        # Try to load from saved file first
        if os.path.exists(self.data_filepath):
            print(f"📂 Loading saved Cornell dining data from {self.data_filepath}...")
            data = self._load_from_file()
            if data:
                self._populate_restaurants(data)
                return True
        
        # If file doesn't exist, try to fetch fresh data
        print("🌐 No saved data found. Fetching fresh Cornell dining data...")
        data = self._fetch_fresh_data()
        
        if data:
            self._populate_restaurants(data)
            return True
        
        # If both fail, use demo data
        print("⚠️  Could not load Cornell data. Using demo data as fallback...")
        self._load_demo_data()
        return False
    
    def _load_from_file(self):
        """Load data from JSON file"""
        try:
            with open(self.data_filepath, 'r') as f:
                data = json.load(f)
            print(f"✓ Loaded {len(data.get('restaurants', []))} dining halls from file")
            return data
        except Exception as e:
            print(f"✗ Error loading from file: {e}")
            return None
    
    def _fetch_fresh_data(self):
        """Fetch fresh data using scraper"""
        scraper = CornellDiningScraper()
        return scraper.run()
    
    def _populate_restaurants(self, data):
        """Populate restaurant objects from data"""
        print(f"🏗️  Building restaurant objects...")
        
        # Create restaurant objects
        for rest_data in data['restaurants']:
            rest = Restaurant(
                rest_data['id'],
                rest_data['name'],
                rest_data['location'],
                rest_data['cuisine_type']
            )
            self.restaurants[rest_data['id']] = rest
        
        # Load food items into restaurants
        for item in data['food_items']:
            restaurant_id = item['restaurant_id']
            if restaurant_id in self.restaurants:
                self.restaurants[restaurant_id].add_surplus_food(item)
        
        print(f"✓ Loaded {len(self.restaurants)} dining halls")
        print(f"✓ Loaded {len(data['food_items'])} food items")
        
        # Print sample
        sample_names = [r.name for r in list(self.restaurants.values())[:3]]
        print(f"✓ Sample: {', '.join(sample_names)}")
    
    def _load_demo_data(self):
        """Load demo/fallback data"""
        print("Loading demo data...")
        
        demo_restaurants = [
            ('R001', 'Campus Cafe', 'North Campus', 'Cafe'),
            ('R002', 'Main Dining Hall', 'Central Campus', 'Dining Hall'),
            ('R003', 'West Campus Market', 'West Campus', 'Market'),
        ]
        
        for rid, name, loc, cuisine in demo_restaurants:
            rest = Restaurant(rid, name, loc, cuisine)
            self.restaurants[rid] = rest
        
        # Add demo food items
        expiry_soon = datetime.now() + timedelta(hours=3)
        expiry_later = datetime.now() + timedelta(hours=8)
        
        demo_foods = [
            ('R001', 'F001', 'Coffee & Pastry', 'bakery', 150, expiry_soon, 3),
            ('R001', 'F002', 'Sandwich Combo', 'american', 240, expiry_later, 2),
            ('R002', 'F003', 'Pasta Bowl', 'italian', 280, expiry_soon, 2),
            ('R002', 'F004', 'Salad Bar', 'healthy', 200, expiry_later, 4),
            ('R003', 'F005', 'Sushi Roll', 'asian', 320, expiry_soon, 1),
            ('R003', 'F006', 'Fruit Cup', 'healthy', 140, expiry_later, 5),
        ]
        
        for rid, fid, name, ftype, price, expiry, qty in demo_foods:
            self.restaurants[rid].add_surplus_food({
                'item_id': fid,
                'name': name,
                'food_type': ftype,
                'original_price': price,
                'expiry': expiry.isoformat(),
                'quantity': qty
            })
        
        print(f"✓ Loaded {len(self.restaurants)} demo restaurants")
    
    def get_all_restaurants(self):
        """Get all restaurant objects"""
        return self.restaurants
    
    def get_restaurant(self, restaurant_id):
        """Get a specific restaurant by ID"""
        return self.restaurants.get(restaurant_id)
    
    def get_all_available_items(self, user_location=None):
        """Get all available (non-expired) items, optionally filtered by location"""
        available_items = []
        
        for restaurant in self.restaurants.values():
            # Location filtering (simplified - always show all for Cornell)
            for item in restaurant.get_available_items():
                available_items.append({
                    **item,
                    'restaurant': restaurant.name,
                    'restaurant_location': restaurant.location
                })
        
        return available_items
    
    def refresh_data(self):
        """Refresh data by fetching from API"""
        print("🔄 Refreshing dining data...")
        data = self._fetch_fresh_data()
        
        if data:
            # Clear existing data
            self.restaurants.clear()
            # Load new data
            self._populate_restaurants(data)
            return True
        
        print("⚠️  Could not refresh data")
        return False