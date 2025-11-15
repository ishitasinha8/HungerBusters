"""
Bhookh Buster - Main Flask Application with Claude AI Integration
Cornell Dining Edition - Food Security Web Application

Run: python app.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify, request, session
from flask_cors import CORS
from datetime import datetime
import random
import os

# Import project modules
from config import Config
from models import User, Order
from data_manager import DataManager
from templates import HTML_TEMPLATE
from claude_ai_service import ClaudeAIService

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize data manager and load dining data
data_manager = DataManager()
data_manager.load_dining_data()

# Initialize Claude AI service
claude_ai = ClaudeAIService()


class BhookhBusterService:
    """Main business logic service for Bhookh Buster with AI integration"""
    
    def __init__(self, data_manager, claude_service):
        self.data_manager = data_manager
        self.claude_ai = claude_service
        self.users = {}
        self.orders = []
        self.order_counter = 0
    
    def register_user(self, user_id, name, location, dietary_preferences=None):
        """Register a new user"""
        user = User(user_id, name, location, dietary_preferences)
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def create_surprise_bag(self, user_id):
        """Create a free surprise bag for the user"""
        user = self.get_user(user_id)
        if not user:
            return {'error': 'User not found'}
        
        # Get all available items
        available_items = self.data_manager.get_all_available_items(user.location)
        
        if not available_items:
            return {'error': 'No surplus food available nearby'}
        
        # Filter by user preferences if any
        filtered_items = self._filter_by_preferences(available_items, user)
        
        if not filtered_items:
            filtered_items = available_items  # Fallback to all items
        
        # Select random items for surprise bag
        bag_size = min(
            random.randint(Config.SURPRISE_BAG_MIN_ITEMS, Config.SURPRISE_BAG_MAX_ITEMS),
            len(filtered_items)
        )
        surprise_bag = random.sample(filtered_items, bag_size)
        
        return {
            'type': 'surprise_bag',
            'cost': 0,
            'items': surprise_bag,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_ai_suggestions(self, user_id, mood=None):
        """Get AI-powered food suggestions using Claude"""
        user = self.get_user(user_id)
        if not user:
            return []
        
        # Get all available items
        available_items = self.data_manager.get_all_available_items(user.location)
        
        if not available_items:
            return []
        
        # Use Claude AI for intelligent recommendations
        try:
            suggestions = self.claude_ai.get_personalized_suggestions(
                user=user,
                available_items=available_items,
                mood=mood,
                context={'time': datetime.now().hour}
            )
            return suggestions
        except Exception as e:
            print(f"Error getting AI suggestions: {e}")
            # Fallback to basic scoring
            return self._basic_suggestions(available_items, user, mood)
    
    def get_meal_insights(self, user_id, selected_items):
        """Get AI insights about selected meal"""
        user = self.get_user(user_id)
        if not user:
            return {'error': 'User not found'}
        
        try:
            insights = self.claude_ai.get_meal_insights(user, selected_items)
            return insights
        except Exception as e:
            print(f"Error getting meal insights: {e}")
            return {
                'nutritional_overview': 'Your meal selection looks great!',
                'balance_score': 8,
                'balance_assessment': 'Good variety',
                'suggestion': None
            }
    
    def create_custom_order(self, user_id, selected_items, mood=None):
        """Create a custom order with selected items"""
        user = self.get_user(user_id)
        if not user:
            return {'error': 'User not found'}
        
        custom_items = []
        total_cost = 0
        
        # Get all available items and filter by selected IDs
        all_items = self.data_manager.get_all_available_items(user.location)
        
        for item in all_items:
            if item['item_id'] in selected_items:
                discount_price = round(item['original_price'] * Config.DISCOUNT_RATE, 2)
                custom_items.append({
                    **item,
                    'discount_price': discount_price
                })
                total_cost += discount_price
        
        # Get AI-generated impact message
        try:
            impact_message = self.claude_ai.generate_food_waste_impact(
                len(custom_items),
                total_cost / 100
            )
        except:
            impact_message = f"Great job! You saved {len(custom_items)} meals from waste! 🌱"
        
        # Create order
        self.order_counter += 1
        order = Order(
            order_id=f"ORD_{self.order_counter:04d}",
            user_id=user_id,
            order_type='custom_bag',
            items=custom_items,
            cost=round(total_cost, 2)
        )
        
        self.orders.append(order)
        
        order_dict = order.to_dict()
        order_dict['impact_message'] = impact_message
        
        return order_dict
    
    def _filter_by_preferences(self, items, user):
        """Filter items by user's dietary preferences"""
        if not user.dietary_preferences:
            return items
        
        return [
            item for item in items 
            if any(pref in item['food_type'] for pref in user.dietary_preferences)
        ]
    
    def _basic_suggestions(self, items, user, mood):
        """Basic suggestions fallback"""
        scored_items = []
        for item in items[:15]:
            score = self._calculate_item_score(item, user, mood)
            
            scored_items.append({
                'item': item,
                'score': score,
                'ai_reason': 'Matched to your preferences',
                'discount_price': round(item['original_price'] * Config.DISCOUNT_RATE, 2)
            })
        
        scored_items.sort(key=lambda x: x['score'], reverse=True)
        return scored_items[:Config.MAX_SUGGESTIONS]
    
    def _calculate_item_score(self, item, user, mood):
        """Calculate recommendation score for an item"""
        score = 0
        
        # Preference score based on past interactions
        if item['food_type'] in user.preferences_score:
            score += user.preferences_score[item['food_type']] * Config.PREFERENCE_SCORE_WEIGHT
        
        # Dietary preference match
        if item['food_type'] in user.dietary_preferences:
            score += Config.DIETARY_MATCH_SCORE
        
        # Mood-based scoring
        if mood:
            score += self._get_mood_score(item['food_type'], mood)
        
        # Urgency based on expiry time
        hours_until_expiry = (
            datetime.fromisoformat(item['expiry']) - datetime.now()
        ).total_seconds() / 3600
        
        if hours_until_expiry < Config.URGENT_EXPIRY_HOURS:
            score += Config.URGENT_EXPIRY_SCORE
        elif hours_until_expiry < Config.NORMAL_EXPIRY_HOURS:
            score += Config.NORMAL_EXPIRY_SCORE
        
        return score
    
    def _get_mood_score(self, food_type, mood):
        """Get score based on mood-food mapping"""
        mood_map = Config.MOOD_FOOD_MAP.get(mood.lower(), {})
        return mood_map.get(food_type, 0)


# Initialize service
bhookh_service = BhookhBusterService(data_manager, claude_ai)


# ============= API ROUTES =============

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    user = bhookh_service.register_user(
        data['user_id'],
        data['name'],
        data['location'],
        data.get('dietary_preferences', [])
    )
    session['user_id'] = user.user_id
    return jsonify({'success': True, 'user_id': user.user_id})


@app.route('/api/surprise-bag', methods=['GET'])
def get_surprise_bag():
    """Get a free surprise bag"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    bag = bhookh_service.create_surprise_bag(user_id)
    return jsonify(bag)


@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Get AI-powered food suggestions using Claude"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    mood = data.get('mood')
    suggestions = bhookh_service.get_ai_suggestions(user_id, mood)
    return jsonify(suggestions)


@app.route('/api/meal-insights', methods=['POST'])
def get_meal_insights():
    """Get AI insights about selected items"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    insights = bhookh_service.get_meal_insights(user_id, data['selected_items'])
    return jsonify(insights)


@app.route('/api/custom-order', methods=['POST'])
def create_custom_order():
    """Create a custom order"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    order = bhookh_service.create_custom_order(
        user_id,
        data['selected_items'],
        data.get('mood')
    )
    return jsonify(order)


@app.route('/api/rate-item', methods=['POST'])
def rate_item():
    """Rate a food item"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    user = bhookh_service.get_user(user_id)
    user.add_interaction(data['food_type'], data['rating'])
    return jsonify({'success': True})


@app.route('/api/refresh-data', methods=['POST'])
def refresh_data():
    """Refresh dining data from Cornell API"""
    success = data_manager.refresh_data()
    return jsonify({'success': success})


# ============= MAIN =============

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🍽️  BHOOKH BUSTER - Cornell Dining Edition with AI")
    print("="*60)
    print("\n✅ Server starting...")
    print(f"📱 Open your browser: http://localhost:{Config.PORT}")
    print(f"📊 Loaded {len(data_manager.restaurants)} dining halls")
    print("🤖 Claude AI integration enabled")
    print("📄 Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )