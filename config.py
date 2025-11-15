"""
Configuration settings for Bhookh Buster application
"""

import os
import secrets

class Config:
    """Base configuration"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5001
    
    # Data settings
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    DINING_DATA_FILE = 'cornell_dining_bhookh_buster.json'
    
    # Cornell Dining API
    CORNELL_API_URLS = [
        "https://now.dining.cornell.edu/api/1.0/dining/eateries.json",
    ]
    
    # Business logic settings
    DISCOUNT_RATE = 0.3  # 70% off (pay 30%)
    SURPRISE_BAG_MIN_ITEMS = 3
    SURPRISE_BAG_MAX_ITEMS = 5
    MAX_SUGGESTIONS = 12
    NEARBY_RADIUS_KM = 5
    
    # Scoring weights
    PREFERENCE_SCORE_WEIGHT = 2
    DIETARY_MATCH_SCORE = 10
    URGENT_EXPIRY_HOURS = 4
    URGENT_EXPIRY_SCORE = 15
    NORMAL_EXPIRY_HOURS = 8
    NORMAL_EXPIRY_SCORE = 10
    
    # User settings
    CORNELL_LOCATIONS = [
        'North Campus',
        'Central Campus',
        'West Campus',
        'Collegetown'
    ]
    
    DIETARY_PREFERENCES = [
        'vegetarian',
        'vegan',
        'healthy',
        'italian',
        'asian',
        'american'
    ]
    
    # Mood-food mapping
    MOOD_FOOD_MAP = {
        'happy': {'italian': 10, 'american': 8, 'asian': 7},
        'stressed': {'healthy': 10, 'italian': 8, 'american': 7},
        'healthy': {'healthy': 10, 'vegetarian': 9},
        'adventurous': {'asian': 10, 'italian': 7},
        'tired': {'american': 10, 'italian': 8}
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # In production, SECRET_KEY must be set via environment variable

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}