"""
Bhookh Buster - Food Security Web Application
Full Stack Implementation with Flask Backend and HTML/CSS/JS Frontend

Installation:
pip install flask flask-cors

Run:
python app.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify, request, session
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# ============= BACKEND MODELS =============

class User:
    def __init__(self, user_id, name, location, dietary_preferences=None):
        self.user_id = user_id
        self.name = name
        self.location = location
        self.dietary_preferences = dietary_preferences or []
        self.interaction_history = []
        self.preferences_score = {}
        
    def add_interaction(self, food_type, rating):
        self.interaction_history.append({
            'food_type': food_type,
            'rating': rating,
            'timestamp': datetime.now().isoformat()
        })
        if food_type not in self.preferences_score:
            self.preferences_score[food_type] = 0
        self.preferences_score[food_type] += rating

class Restaurant:
    def __init__(self, restaurant_id, name, location, cuisine_type):
        self.restaurant_id = restaurant_id
        self.name = name
        self.location = location
        self.cuisine_type = cuisine_type
        self.surplus_inventory = []
        
    def add_surplus_food(self, food_item):
        self.surplus_inventory.append(food_item)
        
    def get_available_items(self):
        now = datetime.now()
        return [item for item in self.surplus_inventory 
                if datetime.fromisoformat(item['expiry']) > now]

class BhookhBuster:
    def __init__(self):
        self.users = {}
        self.restaurants = {}
        self.orders = []
        self._init_demo_data()
        
    def _init_demo_data(self):
        """Initialize with demo restaurants and food items"""
        restaurants_data = [
            ('R001', 'Spice Garden', 'Mumbai Central', 'Indian'),
            ('R002', 'Pizza Palace', 'Andheri', 'Italian'),
            ('R003', 'Green Bowl', 'Bandra', 'Healthy'),
            ('R004', 'Dragon Wok', 'Mumbai Central', 'Chinese'),
            ('R005', 'Burger Hub', 'Andheri', 'Fast Food')
        ]
        
        for rid, name, loc, cuisine in restaurants_data:
            rest = Restaurant(rid, name, loc, cuisine)
            self.restaurants[rid] = rest
            
        # Add surplus food items
        expiry_soon = datetime.now() + timedelta(hours=3)
        expiry_later = datetime.now() + timedelta(hours=8)
        
        foods = [
            ('R001', 'F001', 'Paneer Tikka', 'indian', 250, expiry_soon, 2),
            ('R001', 'F002', 'Dal Makhani', 'indian', 180, expiry_later, 3),
            ('R001', 'F003', 'Naan Basket', 'indian', 80, expiry_soon, 5),
            ('R002', 'F004', 'Margherita Pizza', 'italian', 300, expiry_soon, 1),
            ('R002', 'F005', 'Pasta Alfredo', 'italian', 280, expiry_later, 2),
            ('R003', 'F006', 'Quinoa Salad Bowl', 'healthy', 220, expiry_soon, 2),
            ('R003', 'F007', 'Green Smoothie', 'healthy', 120, expiry_later, 4),
            ('R003', 'F008', 'Grilled Veggie Wrap', 'healthy', 150, expiry_soon, 3),
            ('R004', 'F009', 'Hakka Noodles', 'chinese', 200, expiry_later, 2),
            ('R004', 'F010', 'Manchurian', 'chinese', 180, expiry_soon, 3),
            ('R005', 'F011', 'Veggie Burger', 'fast_food', 120, expiry_soon, 4),
            ('R005', 'F012', 'French Fries', 'fast_food', 80, expiry_later, 5),
        ]
        
        for rid, fid, name, ftype, price, expiry, qty in foods:
            self.restaurants[rid].add_surplus_food({
                'item_id': fid,
                'name': name,
                'food_type': ftype,
                'original_price': price,
                'expiry': expiry.isoformat(),
                'quantity': qty
            })
        
    def register_user(self, user_id, name, location, dietary_preferences=None):
        user = User(user_id, name, location, dietary_preferences)
        self.users[user_id] = user
        return user
        
    def get_user(self, user_id):
        return self.users.get(user_id)
        
    def create_surprise_bag(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return {'error': 'User not found'}
            
        available_items = []
        for restaurant in self.restaurants.values():
            if self._is_nearby(user.location, restaurant.location):
                for item in restaurant.get_available_items():
                    available_items.append({
                        **item,
                        'restaurant': restaurant.name,
                        'restaurant_location': restaurant.location
                    })
        
        if not available_items:
            return {'error': 'No surplus food available nearby'}
            
        filtered_items = self._filter_by_preferences(available_items, user)
        bag_size = min(random.randint(3, 5), len(filtered_items))
        surprise_bag = random.sample(filtered_items, bag_size) if filtered_items else []
        
        return {
            'type': 'surprise_bag',
            'cost': 0,
            'items': surprise_bag,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        
    def get_ai_suggestions(self, user_id, mood=None):
        user = self.users.get(user_id)
        if not user:
            return []
            
        available_items = []
        for restaurant in self.restaurants.values():
            if self._is_nearby(user.location, restaurant.location):
                for item in restaurant.get_available_items():
                    available_items.append({
                        **item,
                        'restaurant': restaurant.name,
                        'restaurant_location': restaurant.location
                    })
        
        scored_items = []
        for item in available_items:
            score = 0
            
            if item['food_type'] in user.preferences_score:
                score += user.preferences_score[item['food_type']] * 2
            
            if item['food_type'] in user.dietary_preferences:
                score += 10
            
            if mood:
                score += self._mood_score(item['food_type'], mood)
            
            hours_until_expiry = (datetime.fromisoformat(item['expiry']) - datetime.now()).total_seconds() / 3600
            if hours_until_expiry < 4:
                score += 15
            elif hours_until_expiry < 8:
                score += 10
            
            scored_items.append({
                'item': item,
                'score': score,
                'discount_price': round(item['original_price'] * 0.3, 2)
            })
        
        scored_items.sort(key=lambda x: x['score'], reverse=True)
        return scored_items[:12]
        
    def create_custom_order(self, user_id, selected_items, mood=None):
        user = self.users.get(user_id)
        if not user:
            return {'error': 'User not found'}
            
        custom_items = []
        total_cost = 0
        
        for restaurant in self.restaurants.values():
            if self._is_nearby(user.location, restaurant.location):
                for item in restaurant.get_available_items():
                    if item['item_id'] in selected_items:
                        custom_items.append({
                            **item,
                            'restaurant': restaurant.name,
                            'discount_price': round(item['original_price'] * 0.3, 2)
                        })
                        total_cost += item['original_price'] * 0.3
        
        order = {
            'order_id': f"ORD_{len(self.orders) + 1:04d}",
            'type': 'custom_bag',
            'cost': round(total_cost, 2),
            'items': custom_items,
            'user_id': user_id,
            'status': 'confirmed',
            'timestamp': datetime.now().isoformat()
        }
        
        self.orders.append(order)
        return order
        
    def _is_nearby(self, location1, location2, radius_km=5):
        return location1.lower() in location2.lower() or location2.lower() in location1.lower()
        
    def _filter_by_preferences(self, items, user):
        if not user.dietary_preferences:
            return items
        return [item for item in items 
                if any(pref in item['food_type'] for pref in user.dietary_preferences)]
        
    def _mood_score(self, food_type, mood):
        mood_food_map = {
            'happy': {'italian': 10, 'fast_food': 8, 'chinese': 7},
            'stressed': {'indian': 10, 'italian': 8, 'fast_food': 7},
            'healthy': {'healthy': 10, 'indian': 5},
            'adventurous': {'chinese': 10, 'indian': 9, 'italian': 7},
            'tired': {'fast_food': 10, 'italian': 8, 'indian': 7}
        }
        return mood_food_map.get(mood.lower(), {}).get(food_type, 0)

# Initialize app
bhookh_buster = BhookhBuster()

# ============= API ROUTES =============

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user = bhookh_buster.register_user(
        data['user_id'],
        data['name'],
        data['location'],
        data.get('dietary_preferences', [])
    )
    session['user_id'] = user.user_id
    return jsonify({'success': True, 'user_id': user.user_id})

@app.route('/api/surprise-bag', methods=['GET'])
def get_surprise_bag():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    bag = bhookh_buster.create_surprise_bag(user_id)
    return jsonify(bag)

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    mood = data.get('mood')
    suggestions = bhookh_buster.get_ai_suggestions(user_id, mood)
    return jsonify(suggestions)

@app.route('/api/custom-order', methods=['POST'])
def create_custom_order():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    order = bhookh_buster.create_custom_order(
        user_id,
        data['selected_items'],
        data.get('mood')
    )
    return jsonify(order)

@app.route('/api/rate-item', methods=['POST'])
def rate_item():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    user = bhookh_buster.get_user(user_id)
    user.add_interaction(data['food_type'], data['rating'])
    return jsonify({'success': True})

# ============= HTML TEMPLATE =============

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bhookh Buster - Fighting Food Waste</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #B31B1B 0%, #8B1515 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .registration {
            display: none;
        }
        
        .registration.active {
            display: block;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .input-group input, .input-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        
        .input-group input:focus, .input-group select:focus {
            outline: none;
            border-color: #B31B1B;
        }
        
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        
        .checkbox-group label {
            display: flex;
            align-items: center;
            padding: 8px 15px;
            background: #f5f5f5;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .checkbox-group label:hover {
            background: #e8e8e8;
        }
        
        .checkbox-group input[type="checkbox"] {
            margin-right: 8px;
            width: auto;
        }
        
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #B31B1B 0%, #8B1515 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(179, 27, 27, 0.4);
        }
        
        .btn-success {
            background: #4CAF50;
            color: white;
        }
        
        .btn-warning {
            background: #FF9800;
            color: white;
        }
        
        .main-content {
            display: none;
        }
        
        .main-content.active {
            display: block;
        }
        
        .action-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .action-card {
            background: linear-gradient(135deg, #B31B1B 0%, #8B1515 100%);
            padding: 30px;
            border-radius: 15px;
            color: white;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }
        
        .action-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        
        .action-card h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        
        .action-card.custom {
            background: linear-gradient(135deg, #222222 0%, #444444 100%);
        }
        
        .mood-selector {
            display: none;
            margin-bottom: 20px;
        }
        
        .mood-selector.active {
            display: block;
        }
        
        .mood-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 15px;
        }
        
        .mood-btn {
            padding: 10px 20px;
            border: 2px solid #B31B1B;
            background: white;
            color: #B31B1B;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .mood-btn:hover, .mood-btn.active {
            background: #B31B1B;
            color: white;
        }
        
        .items-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .item-card {
            background: #f9f9f9;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        
        .item-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .item-card.selected {
            border-color: #B31B1B;
            background: #ffe8e8;
        }
        
        .item-card h4 {
            color: #222222;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .item-details {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        
        .price {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }
        
        .original-price {
            text-decoration: line-through;
            color: #999;
        }
        
        .discount-price {
            color: #4CAF50;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-top: 8px;
        }
        
        .badge-urgent {
            background: #B31B1B;
            color: white;
        }
        
        .badge-free {
            background: #4CAF50;
            color: white;
        }
        
        .order-summary {
            position: sticky;
            bottom: 0;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
            margin-top: 30px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #B31B1B;
        }
        
        .loading::after {
            content: '...';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60% { content: '...'; }
            80%, 100% { content: ''; }
        }
        
        .success-message {
            background: #4CAF50;
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            margin-top: 20px;
        }
        
        .user-info {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍽️ Bhookh Buster</h1>
            <p>Fighting Food Waste, One Meal at a Time</p>
        </div>
        
        <div class="user-info" id="userInfo" style="display: none;"></div>
        
        <!-- Registration Form -->
        <div class="card registration active" id="registrationCard">
            <h2 style="margin-bottom: 20px; color: #333;">Join the Movement</h2>
            <div class="input-group">
                <label>Your Name</label>
                <input type="text" id="userName" placeholder="Enter your name">
            </div>
            <div class="input-group">
                <label>Location</label>
                <select id="userLocation">
                    <option value="Mumbai Central">Mumbai Central</option>
                    <option value="Andheri">Andheri</option>
                    <option value="Bandra">Bandra</option>
                    <option value="Dadar">Dadar</option>
                    <option value="Powai">Powai</option>
                </select>
            </div>
            <div class="input-group">
                <label>Dietary Preferences (Select all that apply)</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" value="indian"> Indian</label>
                    <label><input type="checkbox" value="italian"> Italian</label>
                    <label><input type="checkbox" value="chinese"> Chinese</label>
                    <label><input type="checkbox" value="healthy"> Healthy</label>
                    <label><input type="checkbox" value="fast_food"> Fast Food</label>
                    <label><input type="checkbox" value="vegetarian"> Vegetarian</label>
                    <label><input type="checkbox" value="vegan"> Vegan</label>
                </div>
            </div>
            <button class="btn btn-primary" onclick="register()">Start Saving Food!</button>
        </div>
        
        <!-- Main Content -->
        <div class="main-content" id="mainContent">
            <div class="action-buttons">
                <div class="action-card" onclick="getSurpriseBag()">
                    <h3>🎁 Surprise Bag</h3>
                    <p>Get a FREE mystery bag of delicious surplus food!</p>
                    <div class="badge badge-free">100% FREE</div>
                </div>
                <div class="action-card custom" onclick="showCustomBag()">
                    <h3>🛍️ Custom Bag</h3>
                    <p>Choose your own items and pay only 30% of original price!</p>
                    <div class="badge" style="background: rgba(255,255,255,0.3);">70% OFF</div>
                </div>
            </div>
            
            <!-- Mood Selector -->
            <div class="card mood-selector" id="moodSelector">
                <h3 style="margin-bottom: 15px; color: #333;">What's your mood today?</h3>
                <div class="mood-buttons">
                    <button class="mood-btn" data-mood="happy">😊 Happy</button>
                    <button class="mood-btn" data-mood="stressed">😰 Stressed</button>
                    <button class="mood-btn" data-mood="healthy">🥗 Healthy</button>
                    <button class="mood-btn" data-mood="adventurous">🌶️ Adventurous</button>
                    <button class="mood-btn" data-mood="tired">😴 Tired</button>
                </div>
            </div>
            
            <!-- Results Section -->
            <div class="card" id="resultsSection" style="display: none;">
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>
    
    <script>
        let currentMode = null;
        let selectedMood = null;
        let selectedItems = [];
        
        function register() {
            const name = document.getElementById('userName').value;
            const location = document.getElementById('userLocation').value;
            const preferences = Array.from(document.querySelectorAll('.checkbox-group input:checked'))
                .map(cb => cb.value);
            
            if (!name) {
                alert('Please enter your name');
                return;
            }
            
            const userId = 'U' + Date.now();
            
            fetch('/api/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    user_id: userId,
                    name: name,
                    location: location,
                    dietary_preferences: preferences
                })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('registrationCard').classList.remove('active');
                document.getElementById('mainContent').classList.add('active');
                document.getElementById('userInfo').style.display = 'block';
                document.getElementById('userInfo').innerHTML = `
                    <strong>Welcome, ${name}!</strong><br>
                    📍 ${location} | 🍽️ ${preferences.join(', ') || 'All cuisines'}
                `;
            });
        }
        
        function getSurpriseBag() {
            currentMode = 'surprise';
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('moodSelector').classList.remove('active');
            document.getElementById('resultsContent').innerHTML = '<div class="loading">Preparing your surprise bag</div>';
            
            fetch('/api/surprise-bag')
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('resultsContent').innerHTML = 
                            `<p style="color: red;">${data.error}</p>`;
                        return;
                    }
                    
                    displaySurpriseBag(data.items);
                });
        }
        
        function showCustomBag() {
            currentMode = 'custom';
            selectedItems = [];
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('moodSelector').classList.add('active');
            
            setupMoodButtons();
        }
        
        function setupMoodButtons() {
            const moodBtns = document.querySelectorAll('.mood-btn');
            moodBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    moodBtns.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    selectedMood = this.dataset.mood;
                    getSuggestions();
                });
            });
        }
        
        function getSuggestions() {
            document.getElementById('resultsContent').innerHTML = 
                '<div class="loading">Getting AI-powered suggestions for you</div>';
            
            fetch('/api/suggestions', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({mood: selectedMood})
            })
            .then(res => res.json())
            .then(data => {
                displayCustomItems(data);
            });
        }
        
        function displaySurpriseBag(items) {
            let html = '<h2 style="color: #333; margin-bottom: 20px;">🎉 Your FREE Surprise Bag!</h2>';
            html += '<div class="items-grid">';
            
            items.forEach(item => {
                const expiryTime = new Date(item.expiry);
                const hoursLeft = Math.round((expiryTime - new Date()) / (1000 * 60 * 60));
                
                html += `
                    <div class="item-card">
                        <h4>${item.name}</h4>
                        <div class="item-details">📍 ${item.restaurant}</div>
                        <div class="item-details">🍽️ ${item.food_type}</div>
                        <div class="item-details">⏰ Expires in ${hoursLeft} hours</div>
                        <div class="price">
                            <span class="original-price">₹${item.original_price}</span>
                            <span class="discount-price">FREE!</span>
                        </div>
                        ${hoursLeft < 4 ? '<div class="badge badge-urgent">⚡ Grab Soon!</div>' : ''}
                    </div>
                `;
            });
            
            html += '</div>';
            html += `
                <div class="success-message" style="margin-top: 30px;">
                    <h3>🎊 Congratulations!</h3>
                    <p>You've saved ${items.length} meals from going to waste! Pick up your bag within 2 hours.</p>
                    <button class="btn" style="background: white; color: #4CAF50; margin-top: 15px;" onclick="location.reload()">
                        Get Another Bag
                    </button>
                </div>
            `;
            
            document.getElementById('resultsContent').innerHTML = html;
        }
        
        function displayCustomItems(suggestions) {
            let html = '<h2 style="color: #333; margin-bottom: 20px;">🤖 AI-Powered Suggestions for You</h2>';
            html += '<p style="color: #666; margin-bottom: 20px;">Click items to add them to your custom bag (30% of original price)</p>';
            html += '<div class="items-grid">';
            
            suggestions.forEach(suggestion => {
                const item = suggestion.item;
                const expiryTime = new Date(item.expiry);
                const hoursLeft = Math.round((expiryTime - new Date()) / (1000 * 60 * 60));
                
                html += `
                    <div class="item-card" onclick="toggleItem('${item.item_id}', this)" data-price="${suggestion.discount_price}">
                        <h4>${item.name}</h4>
                        <div class="item-details">📍 ${item.restaurant}</div>
                        <div class="item-details">🍽️ ${item.food_type}</div>
                        <div class="item-details">⏰ Expires in ${hoursLeft} hours</div>
                        <div class="item-details">🎯 AI Score: ${suggestion.score}/40</div>
                        <div class="price">
                            <span class="original-price">₹${item.original_price}</span>
                            <span class="discount-price">₹${suggestion.discount_price}</span>
                        </div>
                        ${hoursLeft < 4 ? '<div class="badge badge-urgent">⚡ Urgent!</div>' : ''}
                    </div>
                `;
            });
            
            html += '</div>';
            html += `
                <div class="order-summary" id="orderSummary" style="display: none;">
                    <h3 style="color: #333;">Your Custom Bag</h3>
                    <div id="selectedItemsList"></div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
                        <div>
                            <strong style="font-size: 1.5em; color: #333;">Total: ₹<span id="totalPrice">0</span></strong>
                            <div style="color: #4CAF50; font-size: 0.9em;">You're saving 70%!</div>
                        </div>
                        <button class="btn btn-success" onclick="placeOrder()" style="width: auto; padding: 15px 40px;">
                            Place Order
                        </button>
                    </div>
                </div>
            `;
            
            document.getElementById('resultsContent').innerHTML = html;
        }
        
        function toggleItem(itemId, element) {
            const index = selectedItems.indexOf(itemId);
            
            if (index > -1) {
                selectedItems.splice(index, 1);
                element.classList.remove('selected');
            } else {
                selectedItems.push(itemId);
                element.classList.add('selected');
            }
            
            updateOrderSummary();
        }
        
        function updateOrderSummary() {
            if (selectedItems.length === 0) {
                document.getElementById('orderSummary').style.display = 'none';
                return;
            }
            
            document.getElementById('orderSummary').style.display = 'block';
            
            let total = 0;
            let itemsList = '<div style="margin: 15px 0;">';
            
            selectedItems.forEach(itemId => {
                const card = document.querySelector(`[onclick*="${itemId}"]`);
                if (card) {
                    const price = parseFloat(card.dataset.price);
                    total += price;
                    const name = card.querySelector('h4').textContent;
                    itemsList += `<div style="padding: 8px 0; color: #666;">✓ ${name} - ₹${price}</div>`;
                }
            });
            
            itemsList += '</div>';
            
            document.getElementById('selectedItemsList').innerHTML = itemsList;
            document.getElementById('totalPrice').textContent = total.toFixed(2);
        }
        
        function placeOrder() {
            if (selectedItems.length === 0) {
                alert('Please select at least one item');
                return;
            }
            
            document.getElementById('orderSummary').innerHTML = '<div class="loading">Processing your order</div>';
            
            fetch('/api/custom-order', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    selected_items: selectedItems,
                    mood: selectedMood
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                
                displayOrderConfirmation(data);
            });
        }
        
        function displayOrderConfirmation(order) {
            const html = `
                <div class="success-message">
                    <h2>🎉 Order Confirmed!</h2>
                    <p style="font-size: 1.2em; margin: 15px 0;">Order ID: ${order.order_id}</p>
                    <p>Total: ₹${order.cost}</p>
                    <p style="margin-top: 15px;">You saved ₹${(order.cost * 2.33).toFixed(2)} and rescued ${order.items.length} meals from waste!</p>
                    <button class="btn" style="background: white; color: #4CAF50; margin-top: 20px;" onclick="location.reload()">
                        Order More Food
                    </button>
                </div>
            `;
            
            document.getElementById('resultsContent').innerHTML = html;
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🍽️  BHOOKH BUSTER - Food Security Web Application")
    print("="*60)
    print("\n✅ Server starting...")
    print("📱 Open your browser and visit: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
