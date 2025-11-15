"""
Bhookh Buster - Main Flask Application
Cornell Dining Edition - Food Security Web Application

Run: python app.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import os

# Import project modules
from config import Config
from models import User, Order, DiningHallAdmin
from data_manager import DataManager
from templates import HTML_TEMPLATE
from admin_templates import ADMIN_LOGIN_TEMPLATE, ADMIN_REGISTER_TEMPLATE, ADMIN_DASHBOARD_TEMPLATE

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize data manager and load dining data
data_manager = DataManager()
data_manager.load_dining_data()


class BhookhBusterService:
    """Main business logic service for Bhookh Buster"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.users = {}
        self.orders = []
        self.order_counter = 0
        self.admins = {}
        self.admin_counter = 0
        self._init_demo_admin()
    
    def _init_demo_admin(self):
        """Create a demo admin account for testing"""
        # Get first restaurant if available
        if self.data_manager.restaurants:
            first_restaurant_id = list(self.data_manager.restaurants.keys())[0]
            demo_admin = DiningHallAdmin(
                'A001',
                first_restaurant_id,
                'admin',
                DiningHallAdmin.hash_password('admin123'),
                'admin@cornell.edu'
            )
            self.admins['admin'] = demo_admin
            print(f"✓ Demo admin created - Username: admin, Password: admin123")
    
    def register_admin(self, restaurant_id, username, email, password):
        """Register a new dining hall admin"""
        if username in self.admins:
            return {'success': False, 'error': 'Username already exists'}
        
        self.admin_counter += 1
        admin = DiningHallAdmin(
            f'A{self.admin_counter:03d}',
            restaurant_id,
            username,
            DiningHallAdmin.hash_password(password),
            email
        )
        self.admins[username] = admin
        return {'success': True, 'admin_id': admin.admin_id}
    
    def authenticate_admin(self, username, password):
        """Authenticate an admin user"""
        admin = self.admins.get(username)
        if admin and admin.verify_password(password):
            return admin
        return None
    
    def get_admin_restaurant(self, username):
        """Get the restaurant associated with an admin"""
        admin = self.admins.get(username)
        if admin:
            return self.data_manager.get_restaurant(admin.restaurant_id)
        return None
    
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
        """Get AI-powered food suggestions based on user preferences and mood"""
        user = self.get_user(user_id)
        if not user:
            return []
        
        # Get all available items
        available_items = self.data_manager.get_all_available_items(user.location)
        
        if not available_items:
            return []
        
        # Score each item
        scored_items = []
        for item in available_items:
            score = self._calculate_item_score(item, user, mood)
            
            scored_items.append({
                'item': item,
                'score': score,
                'discount_price': round(item['original_price'] * Config.DISCOUNT_RATE, 2)
            })
        
        # Sort by score and return top suggestions
        scored_items.sort(key=lambda x: x['score'], reverse=True)
        return scored_items[:Config.MAX_SUGGESTIONS]
    
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
        return order.to_dict()
    
    def _filter_by_preferences(self, items, user):
        """Filter items by user's dietary preferences"""
        if not user.dietary_preferences:
            return items
        
        return [
            item for item in items 
            if any(pref in item['food_type'] for pref in user.dietary_preferences)
        ]
    
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
bhookh_service = BhookhBusterService(data_manager)


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
    """Get AI-powered food suggestions"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    mood = data.get('mood')
    suggestions = bhookh_service.get_ai_suggestions(user_id, mood)
    return jsonify(suggestions)


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


# ============= ADMIN ROUTES =============

@app.route('/admin/login')
def admin_login():
    """Admin login page"""
    return render_template_string(ADMIN_LOGIN_TEMPLATE)


@app.route('/admin/register')
def admin_register():
    """Admin registration page"""
    restaurants = [r.to_dict() for r in data_manager.restaurants.values()]
    return render_template_string(
        ADMIN_REGISTER_TEMPLATE,
        restaurants=restaurants
    )


@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    if 'admin_username' not in session:
        return redirect(url_for('admin_login'))
    
    username = session['admin_username']
    restaurant = bhookh_service.get_admin_restaurant(username)
    
    if not restaurant:
        return redirect(url_for('admin_login'))
    
    return render_template_string(
        ADMIN_DASHBOARD_TEMPLATE,
        username=username,
        restaurant_name=restaurant.name,
        restaurant_location=restaurant.location
    )


@app.route('/admin/api/login', methods=['POST'])
def admin_api_login():
    """Admin login API"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    admin = bhookh_service.authenticate_admin(username, password)
    
    if admin:
        session['admin_username'] = username
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'})


@app.route('/admin/api/register', methods=['POST'])
def admin_api_register():
    """Admin registration API"""
    data = request.json
    
    result = bhookh_service.register_admin(
        data['restaurant_id'],
        data['username'],
        data['email'],
        data['password']
    )
    
    return jsonify(result)


@app.route('/admin/api/logout', methods=['POST'])
def admin_api_logout():
    """Admin logout API"""
    session.pop('admin_username', None)
    return jsonify({'success': True})


@app.route('/admin/api/inventory')
def admin_get_inventory():
    """Get inventory for admin's restaurant"""
    if 'admin_username' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    username = session['admin_username']
    restaurant = bhookh_service.get_admin_restaurant(username)
    
    if not restaurant:
        return jsonify({'success': False, 'error': 'Restaurant not found'}), 404
    
    items = restaurant.surplus_inventory
    return jsonify({'success': True, 'items': items})


@app.route('/admin/api/add-item', methods=['POST'])
def admin_add_item():
    """Add a new surplus food item"""
    if 'admin_username' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    username = session['admin_username']
    restaurant = bhookh_service.get_admin_restaurant(username)
    
    if not restaurant:
        return jsonify({'success': False, 'error': 'Restaurant not found'}), 404
    
    data = request.json
    
    # Generate item ID
    item_count = len(restaurant.surplus_inventory) + 1
    item_id = f"{restaurant.restaurant_id}_F{item_count:03d}"
    
    # Calculate expiry time
    expiry_time = datetime.now() + timedelta(hours=data['expiry_hours'])
    
    # Create item
    item = {
        'item_id': item_id,
        'restaurant_id': restaurant.restaurant_id,
        'name': data['name'],
        'food_type': data['food_type'],
        'original_price': int(data['original_price']),
        'quantity': data['quantity'],
        'expiry': expiry_time.isoformat(),
        'created_at': datetime.now().isoformat()
    }
    
    restaurant.add_surplus_food(item)
    
    return jsonify({'success': True, 'item': item})


@app.route('/admin/api/update-quantity', methods=['POST'])
def admin_update_quantity():
    """Update item quantity (increment/decrement)"""
    if 'admin_username' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    username = session['admin_username']
    restaurant = bhookh_service.get_admin_restaurant(username)
    
    if not restaurant:
        return jsonify({'success': False, 'error': 'Restaurant not found'}), 404
    
    data = request.json
    item_id = data['item_id']
    change = data['change']
    
    item = restaurant.get_item_by_id(item_id)
    if item:
        new_quantity = max(0, item['quantity'] + change)
        restaurant.update_item_quantity(item_id, new_quantity)
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Item not found'})


@app.route('/admin/api/set-quantity', methods=['POST'])
def admin_set_quantity():
    """Set item quantity to specific value"""
    if 'admin_username' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    username = session['admin_username']
    restaurant = bhookh_service.get_admin_restaurant(username)
    
    if not restaurant:
        return jsonify({'success': False, 'error': 'Restaurant not found'}), 404
    
    data = request.json
    item_id = data['item_id']
    quantity = max(0, data['quantity'])
    
    success = restaurant.update_item_quantity(item_id, quantity)
    
    return jsonify({'success': success})


@app.route('/admin/api/delete-item', methods=['POST'])
def admin_delete_item():
    """Delete an item from inventory"""
    if 'admin_username' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    username = session['admin_username']
    restaurant = bhookh_service.get_admin_restaurant(username)
    
    if not restaurant:
        return jsonify({'success': False, 'error': 'Restaurant not found'}), 404
    
    data = request.json
    item_id = data['item_id']
    
    restaurant.remove_item(item_id)
    
    return jsonify({'success': True})


# ============= MAIN =============

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🍽️  BHOOKH BUSTER - Cornell Dining Edition")
    print("="*60)
    print("\n✅ Server starting...")
    print(f"📱 Open your browser: http://localhost:{Config.PORT}")
    print(f"📊 Loaded {len(data_manager.restaurants)} dining halls")
    print("🔄 Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )