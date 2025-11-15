"""
HTML Template for Bhookh Buster with Claude AI Integration
"""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bhookh Buster - Cornell Dining with AI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            padding: 30px 20px;
            margin-bottom: 30px;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .ai-badge {
            display: inline-block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .subtitle {
            font-size: 1.2em;
            margin-top: 10px;
            opacity: 0.95;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            display: none;
        }
        
        .card.active {
            display: block;
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        
        input[type="text"],
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        
        .checkbox-group label {
            display: flex;
            align-items: center;
            font-weight: normal;
            cursor: pointer;
        }
        
        .checkbox-group input[type="checkbox"] {
            margin-right: 8px;
            cursor: pointer;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        }
        
        .btn-success:hover {
            box-shadow: 0 5px 20px rgba(76, 175, 80, 0.4);
        }
        
        .action-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        
        .action-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .action-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .action-card h3 {
            margin-bottom: 10px;
            font-size: 1.5em;
        }
        
        .action-card p {
            opacity: 0.95;
        }
        
        .mood-selector {
            display: none;
            margin-bottom: 30px;
        }
        
        .mood-selector.active {
            display: block;
        }
        
        .mood-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .mood-btn {
            padding: 15px 20px;
            background: white;
            border: 3px solid #e0e0e0;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1.1em;
        }
        
        .mood-btn:hover {
            border-color: #667eea;
            transform: scale(1.05);
        }
        
        .mood-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }
        
        .items-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .item-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .item-card:hover {
            border-color: #667eea;
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .item-card.selected {
            border-color: #4CAF50;
            background: #f1f8f4;
            box-shadow: 0 5px 20px rgba(76, 175, 80, 0.2);
        }
        
        .item-card h4 {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .item-details {
            color: #666;
            font-size: 0.9em;
            margin: 5px 0;
        }
        
        .ai-reason {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 8px;
            margin: 12px 0;
            font-size: 0.85em;
            color: #1976d2;
            border-left: 3px solid #2196f3;
        }
        
        .price {
            margin-top: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .original-price {
            text-decoration: line-through;
            color: #999;
            font-size: 0.9em;
        }
        
        .discount-price {
            color: #4CAF50;
            font-size: 1.3em;
            font-weight: bold;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .badge-urgent {
            background: #ff5252;
            color: white;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 1.2em;
            color: #666;
        }
        
        .success-message {
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-radius: 15px;
            margin-top: 20px;
        }
        
        .success-message h3 {
            color: #2e7d32;
            font-size: 2em;
            margin-bottom: 20px;
        }
        
        .order-summary {
            background: #f5f5f5;
            border-radius: 12px;
            padding: 25px;
            margin-top: 30px;
        }
        
        #userInfo {
            display: none;
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        #resultsSection {
            display: none;
        }
        
        .impact-badge {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .action-buttons {
                grid-template-columns: 1fr;
            }
            
            .items-grid {
                grid-template-columns: 1fr;
            }
            
            header h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🍽️ Bhookh Buster</h1>
            <div class="ai-badge">🤖 Powered by Claude AI</div>
            <p class="subtitle">Cornell Dining | Fight Food Waste | Save Money</p>
        </header>
        
        <div id="userInfo"></div>
        
        <!-- Registration Card -->
        <div class="card active" id="registrationCard">
            <h2>Welcome! Let's Get Started</h2>
            <p style="color: #666; margin-bottom: 20px;">
                Sign up to get personalized AI-powered food recommendations and help reduce waste at Cornell!
            </p>
            
            <div class="form-group">
                <label for="userName">Your Name</label>
                <input type="text" id="userName" placeholder="Enter your name" required>
            </div>
            
            <div class="form-group">
                <label for="userLocation">Campus Location</label>
                <select id="userLocation">
                    <option value="North Campus">North Campus</option>
                    <option value="Central Campus">Central Campus</option>
                    <option value="West Campus">West Campus</option>
                    <option value="Collegetown">Collegetown</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Dietary Preferences (Optional)</label>
                <p style="font-size: 0.9em; color: #666; margin-bottom: 10px;">
                    Help Claude AI personalize your recommendations
                </p>
                <div class="checkbox-group">
                    <label><input type="checkbox" value="vegetarian"> 🥗 Vegetarian</label>
                    <label><input type="checkbox" value="vegan"> 🌱 Vegan</label>
                    <label><input type="checkbox" value="healthy"> 💪 Healthy</label>
                    <label><input type="checkbox" value="italian"> 🍝 Italian</label>
                    <label><input type="checkbox" value="asian"> 🍜 Asian</label>
                    <label><input type="checkbox" value="american"> 🍔 American</label>
                </div>
            </div>
            
            <button class="btn" onclick="register()">Start Saving Food! 🚀</button>
        </div>
        
        <!-- Main Content -->
        <div class="card" id="mainContent">
            <h2>Choose Your Food Rescue Mission</h2>
            
            <div class="action-buttons">
                <div class="action-card" onclick="getSurpriseBag()" style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);">
                    <h3>🎁 Free Surprise Bag</h3>
                    <p>Get 3-5 random items - Completely FREE!</p>
                    <p style="font-size: 0.9em; margin-top: 10px;">Save food from waste instantly</p>
                </div>
                
                <div class="action-card" onclick="showCustomBag()">
                    <h3>🤖 AI Custom Bag</h3>
                    <p>Personalized recommendations - 70% OFF!</p>
                    <p style="font-size: 0.9em; margin-top: 10px;">Claude AI picks the best for you</p>
                </div>
            </div>
        </div>
        
        <!-- Results Section -->
        <div id="resultsSection">
            <!-- Mood Selector -->
            <div class="card mood-selector" id="moodSelector">
                <h2>What's Your Vibe Today?</h2>
                <p style="color: #666; margin-bottom: 15px;">
                    Tell Claude AI how you're feeling for better recommendations
                </p>
                <div class="mood-buttons">
                    <button class="mood-btn" data-mood="happy">😊 Happy</button>
                    <button class="mood-btn" data-mood="stressed">😰 Stressed</button>
                    <button class="mood-btn" data-mood="healthy">💪 Healthy</button>
                    <button class="mood-btn" data-mood="adventurous">🌟 Adventurous</button>
                    <button class="mood-btn" data-mood="tired">😴 Tired</button>
                </div>
            </div>
            
            <!-- Results Display -->
            <div class="card active" id="resultsCard">
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='app_enhanced.js') }}"></script>
</body>
</html>
'''