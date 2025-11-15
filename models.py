"""
Data models for Bhookh Buster application
"""

from datetime import datetime
import hashlib


class User:
    """User model for tracking preferences and interactions"""
    
    def __init__(self, user_id, name, location, dietary_preferences=None, email=None, phone=None,
                 dietary_restrictions=None, allergens=None, food_categories=None, 
                 quick_preferences=None, dislikes=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.location = location
        
        # All dietary-related preferences combined for AI
        self.dietary_preferences = dietary_preferences or []
        
        # Detailed preference breakdown
        self.dietary_restrictions = dietary_restrictions or []  # vegetarian, vegan, gluten-free, etc.
        self.allergens = allergens or []  # Critical safety information
        self.food_categories = food_categories or []  # produce, bakery, prepared meals, etc.
        self.quick_preferences = quick_preferences or []  # spicy, light-meals, high-protein, etc.
        self.dislikes = dislikes or []  # Foods to avoid (not allergies)
        
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
    
    def has_allergen(self, allergen):
        """Check if user has a specific allergen"""
        return allergen.lower() in [a.lower() for a in self.allergens]
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'dietary_preferences': self.dietary_preferences,
            'dietary_restrictions': self.dietary_restrictions,
            'allergens': self.allergens,
            'food_categories': self.food_categories,
            'quick_preferences': self.quick_preferences,
            'dislikes': self.dislikes,
            'interaction_history': self.interaction_history,
            'preferences_score': self.preferences_score
        }


class DiningHallAdmin:
    """Admin account for dining hall staff"""
    
    def __init__(self, admin_id, restaurant_id, username, password_hash, email):
        self.admin_id = admin_id
        self.restaurant_id = restaurant_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = datetime.now().isoformat()
    
    @staticmethod
    def hash_password(password):
        """Hash a password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify a password against the hash"""
        return self.password_hash == self.hash_password(password)
    
    def to_dict(self):
        """Convert admin to dictionary (excluding password)"""
        return {
            'admin_id': self.admin_id,
            'restaurant_id': self.restaurant_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
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
        
    def update_item_quantity(self, item_id, new_quantity):
        """Update the quantity of a specific item"""
        for item in self.surplus_inventory:
            if item['item_id'] == item_id:
                item['quantity'] = new_quantity
                item['updated_at'] = datetime.now().isoformat()
                return True
        return False
    
    def remove_item(self, item_id):
        """Remove an item from inventory"""
        self.surplus_inventory = [
            item for item in self.surplus_inventory 
            if item['item_id'] != item_id
        ]
        
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
        self.order_type = order_type
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