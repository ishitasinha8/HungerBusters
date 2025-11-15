"""
Data models for Bhookh Buster application
"""

from datetime import datetime

class User:
    """User model for tracking preferences and interactions"""
    
    def __init__(self, user_id, name, location, dietary_preferences=None):
        self.user_id = user_id
        self.name = name
        self.location = location
        self.dietary_preferences = dietary_preferences or []
        self.interaction_history = []
        self.preferences_score = {}
        
    def add_interaction(self, food_type, rating):
        """Record user interaction with a food item"""
        self.interaction_history.append({
            'food_type': food_type,
            'rating': rating,
            'timestamp': datetime.now().isoformat()
        })
        
        if food_type not in self.preferences_score:
            self.preferences_score[food_type] = 0
        self.preferences_score[food_type] += rating
    
    def get_preference_score(self, food_type):
        """Get user's preference score for a food type"""
        return self.preferences_score.get(food_type, 0)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'location': self.location,
            'dietary_preferences': self.dietary_preferences,
            'interaction_history': self.interaction_history,
            'preferences_score': self.preferences_score
        }


class Restaurant:
    """Restaurant/Dining hall model"""
    
    def __init__(self, restaurant_id, name, location, cuisine_type):
        self.restaurant_id = restaurant_id
        self.name = name
        self.location = location
        self.cuisine_type = cuisine_type
        self.surplus_inventory = []
        
    def add_surplus_food(self, food_item):
        """Add a surplus food item to inventory"""
        self.surplus_inventory.append(food_item)
        
    def get_available_items(self):
        """Get all non-expired items"""
        now = datetime.now()
        return [
            item for item in self.surplus_inventory 
            if datetime.fromisoformat(item['expiry']) > now
        ]
    
    def get_item_by_id(self, item_id):
        """Get a specific item by ID"""
        for item in self.surplus_inventory:
            if item['item_id'] == item_id:
                return item
        return None
    
    def to_dict(self):
        """Convert restaurant to dictionary"""
        return {
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'location': self.location,
            'cuisine_type': self.cuisine_type,
            'inventory_count': len(self.surplus_inventory),
            'available_count': len(self.get_available_items())
        }


class Order:
    """Order model for tracking food orders"""
    
    def __init__(self, order_id, user_id, order_type, items, cost):
        self.order_id = order_id
        self.user_id = user_id
        self.order_type = order_type  # 'surprise_bag' or 'custom_bag'
        self.items = items
        self.cost = cost
        self.status = 'confirmed'
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'type': self.order_type,
            'items': self.items,
            'cost': self.cost,
            'status': self.status,
            'timestamp': self.timestamp
        }