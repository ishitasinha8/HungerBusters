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
            background: linear-gradient(135deg, #B31B1B 0%, #8B0000 100%);
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
            background: linear-gradient(135deg, #B31B1B 0%, #8B0000 100%);
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
            border-color: #B31B1B;
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
            background: linear-gradient(135deg, #B31B1B 0%, #8B0000 100%);
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
            box-shadow: 0 5px 20px rgba(179, 27, 27, 0.4);
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
            background: linear-gradient(135deg, #B31B1B 0%, #8B0000 100%);
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
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            margin-top: 15px;
        }
        
        .mood-btn {
            padding: 15px 30px;
            background: white;
            border: 3px solid #e0e0e0;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1.1em;
            min-width: 140px;
        }
        
        .mood-btn:hover {
            border-color: #B31B1B;
            transform: scale(1.05);
        }
        
        .mood-btn.active {
            background: #B31B1B;
            color: white;
            border-color: #B31B1B;
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
            border-color: #B31B1B;
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
            
            .checkbox-grid {
                grid-template-columns: 1fr !important;
            }
        }
        
        /* Enhanced Form Styling */
        .form-section {
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 20px;
        }
        
        .form-section:last-of-type {
            border-bottom: none;
        }
        
        .checkbox-label {
            display: flex;
            align-items: center;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            background: white;
        }
        
        .checkbox-label:hover {
            border-color: #B31B1B;
            background: #fff5f5;
        }
        
        .checkbox-label input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-right: 10px;
            cursor: pointer;
            accent-color: #B31B1B;
        }
        
        .checkbox-label span {
            font-size: 1em;
            color: #333;
        }
        
        .checkbox-label input[type="checkbox"]:checked + span {
            font-weight: 600;
            color: #B31B1B;
        }
        
        .allergen-label {
            border-color: #ffe0e0;
            background: #fffafa;
        }
        
        .allergen-label:hover {
            border-color: #ff6b6b;
            background: #fff0f0;
        }
        
        .allergen-checkbox:checked + span {
            color: #d63031 !important;
        }
        
        input[type="email"],
        input[type="tel"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        input[type="email"]:focus,
        input[type="tel"]:focus {
            outline: none;
            border-color: #B31B1B;
        }
        
        textarea:focus {
            outline: none;
            border-color: #B31B1B;
        }
        
        .cu-login-btn {
            position: relative;
            overflow: hidden;
        }
        
        .cu-login-btn:hover {
            box-shadow: 0 5px 25px rgba(179, 27, 27, 0.5) !important;
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
            <h2 style="text-align: center; margin-bottom: 10px;">🎓 Student Sign Up</h2>
            <p style="text-align: center; color: #666; margin-bottom: 25px;">
                Join Bhookh Buster and help reduce food waste at Cornell!
            </p>
            
            <!-- CU Login Button -->
            <div style="margin-bottom: 25px;">
                <button class="btn cu-login-btn" onclick="loginWithCornell()" style="background: linear-gradient(135deg, #B31B1B 0%, #8B0000 100%); display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <span style="font-size: 1.2em;">🎓</span>
                    <span>Sign in with Cornell NetID</span>
                </button>
                <p style="text-align: center; color: #999; margin: 15px 0; font-size: 0.9em;">
                    ──────── or sign up manually ────────
                </p>
            </div>
            
            <!-- Basic Information -->
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #333; font-size: 1.2em; margin-bottom: 15px; border-left: 4px solid #B31B1B; padding-left: 12px;">
                    Basic Information
                </h3>
                
                <div class="form-group">
                    <label for="userName">Full Name *</label>
                    <input type="text" id="userName" placeholder="Enter your full name" required>
                </div>
                
                <div class="form-group">
                    <label for="userEmail">Cornell Email *</label>
                    <input type="email" id="userEmail" placeholder="netid@cornell.edu" required>
                </div>
                
                <div class="form-group">
                    <label for="userPhone">Phone Number (Optional)</label>
                    <input type="tel" id="userPhone" placeholder="(555) 123-4567">
                </div>
                
                <div class="form-group">
                    <label for="userLocation">Campus Location *</label>
                    <select id="userLocation" required>
                        <option value="">Select your location</option>
                        <option value="North Campus">North Campus</option>
                        <option value="Central Campus">Central Campus</option>
                        <option value="West Campus">West Campus</option>
                        <option value="Collegetown">Collegetown</option>
                    </select>
                </div>
            </div>
            
            <!-- Dietary Restrictions -->
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #333; font-size: 1.2em; margin-bottom: 10px; border-left: 4px solid #B31B1B; padding-left: 12px;">
                    Dietary Restrictions
                </h3>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    Select all that apply to ensure safe food recommendations
                </p>
                
                <div class="checkbox-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                    <label class="checkbox-label">
                        <input type="checkbox" value="vegetarian" class="dietary-checkbox">
                        <span>🥗 Vegetarian</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="vegan" class="dietary-checkbox">
                        <span>🌱 Vegan</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="gluten-free" class="dietary-checkbox">
                        <span>🌾 Gluten-Free</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="dairy-free" class="dietary-checkbox">
                        <span>🥛 Dairy-Free</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="kosher" class="dietary-checkbox">
                        <span>✡️ Kosher</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="halal" class="dietary-checkbox">
                        <span>☪️ Halal</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="pescatarian" class="dietary-checkbox">
                        <span>🐟 Pescatarian</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="low-carb" class="dietary-checkbox">
                        <span>🥑 Low-Carb</span>
                    </label>
                </div>
            </div>
            
            <!-- Allergens to Avoid -->
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #333; font-size: 1.2em; margin-bottom: 10px; border-left: 4px solid #B31B1B; padding-left: 12px;">
                    Allergens to Avoid
                </h3>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    ⚠️ Critical for your safety - select all allergens
                </p>
                
                <div class="checkbox-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="peanuts" class="allergen-checkbox">
                        <span>🥜 Peanuts</span>
                    </label>
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="tree-nuts" class="allergen-checkbox">
                        <span>🌰 Tree Nuts</span>
                    </label>
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="milk" class="allergen-checkbox">
                        <span>🥛 Milk/Dairy</span>
                    </label>
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="eggs" class="allergen-checkbox">
                        <span>🥚 Eggs</span>
                    </label>
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="soy" class="allergen-checkbox">
                        <span>🫘 Soy</span>
                    </label>
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="wheat" class="allergen-checkbox">
                        <span>🌾 Wheat</span>
                    </label>
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="fish" class="allergen-checkbox">
                        <span>🐟 Fish</span>
                    </label>
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="shellfish" class="allergen-checkbox">
                        <span>🦐 Shellfish</span>
                    </label>
                    <label class="checkbox-label allergen-label">
                        <input type="checkbox" value="sesame" class="allergen-checkbox">
                        <span>🌾 Sesame</span>
                    </label>
                </div>
            </div>
            
            <!-- Preferred Food Categories -->
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #333; font-size: 1.2em; margin-bottom: 10px; border-left: 4px solid #B31B1B; padding-left: 12px;">
                    Preferred Food Categories
                </h3>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    What types of food do you prefer? (Select multiple)
                </p>
                
                <div class="checkbox-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                    <label class="checkbox-label">
                        <input type="checkbox" value="produce" class="category-checkbox">
                        <span>🥬 Fresh Produce</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="bakery" class="category-checkbox">
                        <span>🥖 Bakery Items</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="prepared-meals" class="category-checkbox">
                        <span>🍱 Prepared Meals</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="snacks" class="category-checkbox">
                        <span>🍿 Snacks</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="beverages" class="category-checkbox">
                        <span>🥤 Beverages</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="desserts" class="category-checkbox">
                        <span>🍰 Desserts</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="sandwiches" class="category-checkbox">
                        <span>🥪 Sandwiches</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="salads" class="category-checkbox">
                        <span>🥗 Salads</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" value="hot-entrees" class="category-checkbox">
                        <span>🍝 Hot Entrées</span>
                    </label>
                </div>
            </div>
            
            <!-- Food Preferences -->
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #333; font-size: 1.2em; margin-bottom: 10px; border-left: 4px solid #B31B1B; padding-left: 12px;">
                    Quick Preferences
                </h3>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    Help our AI suggest better options for you
                </p>
                
                <div style="display: flex; flex-direction: column; gap: 15px;">
                    <label style="display: flex; align-items: center; font-size: 1.05em; color: #333; font-weight: normal;">
                        <input type="checkbox" value="spicy" class="preference-checkbox" style="width: 20px; height: 20px; margin-right: 12px; cursor: pointer; accent-color: #B31B1B;"> 
                        I like spicy food 🌶️
                    </label>
                    <label style="display: flex; align-items: center; font-size: 1.05em; color: #333; font-weight: normal;">
                        <input type="checkbox" value="light-meals" class="preference-checkbox" style="width: 20px; height: 20px; margin-right: 12px; cursor: pointer; accent-color: #B31B1B;"> 
                        I prefer light meals 🥗
                    </label>
                    <label style="display: flex; align-items: center; font-size: 1.05em; color: #333; font-weight: normal;">
                        <input type="checkbox" value="high-protein" class="preference-checkbox" style="width: 20px; height: 20px; margin-right: 12px; cursor: pointer; accent-color: #B31B1B;"> 
                        I want high-protein options 💪
                    </label>
                    <label style="display: flex; align-items: center; font-size: 1.05em; color: #333; font-weight: normal;">
                        <input type="checkbox" value="comfort-food" class="preference-checkbox" style="width: 20px; height: 20px; margin-right: 12px; cursor: pointer; accent-color: #B31B1B;"> 
                        I'm craving comfort food 🍕
                    </label>
                </div>
            </div>
            
            <!-- Dislikes/Avoids -->
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #333; font-size: 1.2em; margin-bottom: 10px; border-left: 4px solid #B31B1B; padding-left: 12px;">
                    Dislikes / Foods to Avoid
                </h3>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    Foods you simply don't like or prefer to avoid (not allergies)
                </p>
                
                <div class="form-group">
                    <textarea 
                        id="userDislikes" 
                        placeholder="e.g., mushrooms, olives, cilantro, blue cheese, seafood, etc."
                        style="width: 100%; min-height: 80px; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1em; font-family: inherit; resize: vertical;"
                    ></textarea>
                    <p style="font-size: 0.85em; color: #999; margin-top: 5px;">
                        Separate items with commas
                    </p>
                </div>
            </div>
            
            <!-- Terms and Conditions -->
            <div class="form-section" style="margin-bottom: 20px;">
                <label style="display: flex; align-items: flex-start; gap: 10px; cursor: pointer;">
                    <input type="checkbox" id="termsCheckbox" required style="width: 20px; height: 20px; margin-top: 2px; cursor: pointer; accent-color: #B31B1B;">
                    <span style="font-size: 0.9em; color: #555; line-height: 1.5;">
                        I agree to the <a href="#" style="color: #B31B1B; text-decoration: none; font-weight: 600;">Terms & Conditions</a> and <a href="#" style="color: #B31B1B; text-decoration: none; font-weight: 600;">Privacy Policy</a>. I understand that food items are surplus and should be consumed promptly.
                    </span>
                </label>
            </div>
            
            <button class="btn" onclick="register()">
                Complete Sign Up 🚀
            </button>
            
            <p style="text-align: center; color: #999; margin-top: 15px; font-size: 0.9em;">
                Already have an account? <a href="#" onclick="showLogin()" style="color: #B31B1B; text-decoration: none; font-weight: 600;">Sign In</a>
            </p>
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
                <h2 style="font-size: 1.8em; margin-bottom: 10px;">What's your mood today?</h2>
                <p style="color: #666; margin-bottom: 20px; font-size: 1.05em;">
                    Our AI will tailor suggestions to match your vibe
                </p>
                <div class="mood-buttons">
                    <button class="mood-btn" data-mood="happy">😊 Happy</button>
                    <button class="mood-btn" data-mood="stressed">😰 Stressed</button>
                    <button class="mood-btn" data-mood="healthy">🥗 Healthy</button>
                    <button class="mood-btn" data-mood="adventurous">🌶️ Adventurous</button>
                    <button class="mood-btn" data-mood="tired">😴 Tired</button>
                    <button class="mood-btn" data-mood="energetic">⚡ Energetic</button>
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