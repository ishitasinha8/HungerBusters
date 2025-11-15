"""
HTML templates for Bhookh Buster application
"""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bhookh Buster - Cornell Dining Edition</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #B31B1B 0%, #8B1515 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .registration { display: none; }
        .registration.active { display: block; }
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        .input-group input, .input-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        .input-group input:focus, .input-group select:focus { outline: none; border-color: #B31B1B; }
        .checkbox-group { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
        .checkbox-group label {
            display: flex;
            align-items: center;
            padding: 8px 15px;
            background: #f5f5f5;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .checkbox-group label:hover { background: #e8e8e8; }
        .checkbox-group input[type="checkbox"] { margin-right: 8px; width: auto; }
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
        .btn-success { background: #4CAF50; color: white; }
        .main-content { display: none; }
        .main-content.active { display: block; }
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
        .action-card h3 { font-size: 1.5em; margin-bottom: 10px; }
        .action-card.custom { background: linear-gradient(135deg, #222222 0%, #444444 100%); }
        .mood-selector { display: none; margin-bottom: 20px; }
        .mood-selector.active { display: block; }
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
        .item-card h4 { color: #222222; margin-bottom: 10px; font-size: 1.2em; }
        .item-details { color: #666; font-size: 0.9em; margin-bottom: 8px; }
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
        .badge-urgent { background: #B31B1B; color: white; }
        .badge-free { background: #4CAF50; color: white; }
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
            <p>Cornell Dining Edition - Fighting Food Waste, One Meal at a Time</p>
        </div>
        
        <div class="user-info" id="userInfo" style="display: none;"></div>
        
        <div class="card registration active" id="registrationCard">
            <h2 style="margin-bottom: 20px; color: #333;">Join the Movement</h2>
            <div class="input-group">
                <label>Your Name</label>
                <input type="text" id="userName" placeholder="Enter your name">
            </div>
            <div class="input-group">
                <label>Location</label>
                <select id="userLocation">
                    <option value="North Campus">North Campus</option>
                    <option value="Central Campus">Central Campus</option>
                    <option value="West Campus">West Campus</option>
                    <option value="Collegetown">Collegetown</option>
                </select>
            </div>
            <div class="input-group">
                <label>Dietary Preferences (Select all that apply)</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" value="vegetarian"> Vegetarian</label>
                    <label><input type="checkbox" value="vegan"> Vegan</label>
                    <label><input type="checkbox" value="healthy"> Healthy</label>
                    <label><input type="checkbox" value="italian"> Italian</label>
                    <label><input type="checkbox" value="asian"> Asian</label>
                    <label><input type="checkbox" value="american"> American</label>
                </div>
            </div>
            <button class="btn btn-primary" onclick="register()">Start Saving Food!</button>
        </div>
        
        <div class="main-content" id="mainContent">
            <div class="action-buttons">
                <div class="action-card" onclick="getSurpriseBag()">
                    <h3>🎁 Surprise Bag</h3>
                    <p>Get a FREE mystery bag of delicious surplus food from Cornell Dining!</p>
                    <div class="badge badge-free">100% FREE</div>
                </div>
                <div class="action-card custom" onclick="showCustomBag()">
                    <h3>🛍️ Custom Bag</h3>
                    <p>Choose your own items and pay only 30% of original price!</p>
                    <div class="badge" style="background: rgba(255,255,255,0.3);">70% OFF</div>
                </div>
            </div>
            
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
            
            <div class="card" id="resultsSection" style="display: none;">
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>
    
    <script src="/static/app.js"></script>
</body>
</html>
'''
