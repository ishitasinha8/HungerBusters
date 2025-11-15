"""
Admin templates for Dining Hall Management Interface
"""

ADMIN_LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dining Hall Admin Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .login-container {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #1e3c72;
            font-size: 2em;
            margin-bottom: 5px;
        }
        .logo p {
            color: #666;
            font-size: 0.9em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        .form-group input:focus {
            outline: none;
            border-color: #1e3c72;
        }
        .btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(30, 60, 114, 0.4);
        }
        .error {
            background: #f44336;
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        .error.show {
            display: block;
        }
        .register-link {
            text-align: center;
            margin-top: 20px;
            color: #666;
        }
        .register-link a {
            color: #1e3c72;
            text-decoration: none;
            font-weight: 600;
        }
        .register-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>🏢 Admin Portal</h1>
            <p>Dining Hall Management</p>
        </div>
        
        <div class="error" id="errorMsg"></div>
        
        <form id="loginForm" onsubmit="login(event)">
            <div class="form-group">
                <label>Username</label>
                <input type="text" id="username" required placeholder="Enter your username">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required placeholder="Enter your password">
            </div>
            <button type="submit" class="btn">Login</button>
        </form>
        
        <div class="register-link">
            Don't have an account? <a href="/admin/register">Register your dining hall</a>
        </div>
    </div>
    
    <script>
        function login(event) {
            event.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            fetch('/admin/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ username, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/admin/dashboard';
                } else {
                    showError(data.error || 'Invalid credentials');
                }
            })
            .catch(err => {
                showError('Login failed. Please try again.');
            });
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('errorMsg');
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
            setTimeout(() => errorDiv.classList.remove('show'), 5000);
        }
    </script>
</body>
</html>
'''

ADMIN_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register Dining Hall</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .register-container {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 500px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #1e3c72;
            font-size: 2em;
            margin-bottom: 5px;
        }
        .logo p {
            color: #666;
            font-size: 0.9em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #1e3c72;
        }
        .btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(30, 60, 114, 0.4);
        }
        .message {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        .message.success {
            background: #4CAF50;
            color: white;
        }
        .message.error {
            background: #f44336;
            color: white;
        }
        .message.show {
            display: block;
        }
        .login-link {
            text-align: center;
            margin-top: 20px;
            color: #666;
        }
        .login-link a {
            color: #1e3c72;
            text-decoration: none;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="register-container">
        <div class="logo">
            <h1>🏢 Register Dining Hall</h1>
            <p>Join Bhookh Buster</p>
        </div>
        
        <div class="message" id="message"></div>
        
        <form id="registerForm" onsubmit="register(event)">
            <div class="form-group">
                <label>Select Your Dining Hall</label>
                <select id="restaurantId" required>
                    <option value="">-- Select Dining Hall --</option>
                    {% for restaurant in restaurants %}
                    <option value="{{ restaurant.restaurant_id }}">{{ restaurant.name }} ({{ restaurant.location }})</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label>Username</label>
                <input type="text" id="username" required placeholder="Choose a username">
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" required placeholder="your.email@cornell.edu">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="password" required placeholder="Create a secure password">
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <input type="password" id="confirmPassword" required placeholder="Re-enter password">
            </div>
            <button type="submit" class="btn">Register</button>
        </form>
        
        <div class="login-link">
            Already have an account? <a href="/admin/login">Login here</a>
        </div>
    </div>
    
    <script>
        function register(event) {
            event.preventDefault();
            
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (password !== confirmPassword) {
                showMessage('Passwords do not match', 'error');
                return;
            }
            
            const data = {
                restaurant_id: document.getElementById('restaurantId').value,
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: password
            };
            
            fetch('/admin/api/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showMessage('Registration successful! Redirecting to login...', 'success');
                    setTimeout(() => window.location.href = '/admin/login', 2000);
                } else {
                    showMessage(data.error || 'Registration failed', 'error');
                }
            })
            .catch(err => {
                showMessage('Registration failed. Please try again.', 'error');
            });
        }
        
        function showMessage(text, type) {
            const msgDiv = document.getElementById('message');
            msgDiv.textContent = text;
            msgDiv.className = 'message ' + type + ' show';
            setTimeout(() => msgDiv.classList.remove('show'), 5000);
        }
    </script>
</body>
</html>
'''

ADMIN_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dining Hall Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            font-size: 1.8em;
        }
        .header-info {
            text-align: right;
        }
        .logout-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        .logout-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-card h3 {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            color: #1e3c72;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .card h2 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }
        .add-item-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-bottom: 20px;
        }
        .add-item-btn:hover {
            background: #45a049;
        }
        .items-table {
            width: 100%;
            border-collapse: collapse;
        }
        .items-table th {
            background: #f5f5f5;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
        }
        .items-table td {
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        .items-table tr:hover {
            background: #f9f9f9;
        }
        .quantity-control {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .quantity-control button {
            background: #1e3c72;
            color: white;
            border: none;
            width: 30px;
            height: 30px;
            border-radius: 5px;
            cursor: pointer;
        }
        .quantity-control button:hover {
            background: #2a5298;
        }
        .quantity-control input {
            width: 60px;
            text-align: center;
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .delete-btn {
            background: #f44336;
            color: white;
            border: none;
            padding: 6px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .delete-btn:hover {
            background: #da190b;
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .badge-urgent {
            background: #f44336;
            color: white;
        }
        .badge-warning {
            background: #FF9800;
            color: white;
        }
        .badge-good {
            background: #4CAF50;
            color: white;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
        }
        .modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 10px;
            width: 90%;
            max-width: 500px;
        }
        .modal-content h3 {
            margin-bottom: 20px;
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #333;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .modal-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        .modal-buttons button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .btn-primary {
            background: #1e3c72;
            color: white;
        }
        .btn-secondary {
            background: #ddd;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div>
                <h1>🏢 {{ restaurant_name }}</h1>
                <p>{{ restaurant_location }}</p>
            </div>
            <div class="header-info">
                <div>Welcome, {{ username }}</div>
                <button class="logout-btn" onclick="logout()">Logout</button>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <h3>Total Items</h3>
                <div class="number" id="totalItems">0</div>
            </div>
            <div class="stat-card">
                <h3>Available Items</h3>
                <div class="number" id="availableItems">0</div>
            </div>
            <div class="stat-card">
                <h3>Expiring Soon</h3>
                <div class="number" id="expiringSoon">0</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Surplus Food Inventory</h2>
            <button class="add-item-btn" onclick="showAddItemModal()">+ Add New Item</button>
            
            <table class="items-table" id="itemsTable">
                <thead>
                    <tr>
                        <th>Item Name</th>
                        <th>Type</th>
                        <th>Price ($)</th>
                        <th>Quantity</th>
                        <th>Expires In</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="itemsBody">
                    <!-- Items will be loaded here -->
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Add Item Modal -->
    <div class="modal" id="addItemModal">
        <div class="modal-content">
            <h3>Add New Surplus Item</h3>
            <form id="addItemForm" onsubmit="addItem(event)">
                <div class="form-group">
                    <label>Item Name</label>
                    <input type="text" id="itemName" required>
                </div>
                <div class="form-group">
                    <label>Food Type</label>
                    <select id="foodType" required>
                        <option value="italian">Italian</option>
                        <option value="asian">Asian</option>
                        <option value="american">American</option>
                        <option value="healthy">Healthy</option>
                        <option value="vegetarian">Vegetarian</option>
                        <option value="vegan">Vegan</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Original Price ($)</label>
                    <input type="number" id="price" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Quantity</label>
                    <input type="number" id="quantity" min="1" required>
                </div>
                <div class="form-group">
                    <label>Expires In (hours)</label>
                    <input type="number" id="expiryHours" min="1" required>
                </div>
                <div class="modal-buttons">
                    <button type="submit" class="btn-primary">Add Item</button>
                    <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
                </div>
            </form>
        </div>
    </div>
    
    <script src="/static/admin.js"></script>
</body>
</html>
'''
