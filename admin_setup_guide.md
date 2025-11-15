# 🏢 Dining Hall Admin Portal Setup Guide

## Overview

The admin portal allows dining hall staff to:
- ✅ Register their dining hall
- ✅ Login to a secure dashboard
- ✅ Add surplus food items with expiry times
- ✅ Update quantities in real-time
- ✅ Delete items that are sold out
- ✅ View statistics (total items, expiring soon, etc.)

## New Files Added

### 1. **models.py** (Updated)
Added `DiningHallAdmin` class with:
- Password hashing for security
- Admin authentication
- Restaurant association

### 2. **admin_templates.py** (New)
Contains three HTML templates:
- `ADMIN_LOGIN_TEMPLATE` - Login page
- `ADMIN_REGISTER_TEMPLATE` - Registration page
- `ADMIN_DASHBOARD_TEMPLATE` - Inventory management dashboard

### 3. **static/admin.js** (New)
Frontend JavaScript for admin dashboard:
- Load and display inventory
- Add new items
- Update quantities (+/- buttons)
- Delete items
- Real-time statistics

### 4. **app.py** (Updated)
Added admin routes:
- `/admin/login` - Login page
- `/admin/register` - Registration page
- `/admin/dashboard` - Management dashboard
- Multiple API endpoints for inventory operations

## Quick Start

### Step 1: Ensure All Files Are in Place

```
bhookh_buster/
├── models.py (updated with DiningHallAdmin)
├── admin_templates.py (new)
├── app.py (updated with admin routes)
├── static/
│   ├── app.js (existing)
│   └── admin.js (new)
└── ... (other existing files)
```

### Step 2: Demo Admin Account

A demo admin is automatically created when you start the app:

```
Username: admin
Password: admin123
```

This account is linked to the first dining hall in your database.

### Step 3: Start the Application

```bash
python app.py
```

### Step 4: Access Admin Portal

**Login Page:**
```
http://localhost:5000/admin/login
```

**Register New Dining Hall:**
```
http://localhost:5000/admin/register
```

## User Guide

### For Dining Hall Staff

#### 1. **First Time Setup - Register**

1. Visit `http://localhost:5000/admin/register`
2. Select your dining hall from the dropdown
3. Choose a username and password
4. Enter your Cornell email
5. Click "Register"

#### 2. **Login**

1. Visit `http://localhost:5000/admin/login`
2. Enter your username and password
3. Click "Login"

#### 3. **Dashboard Overview**

After login, you'll see:
- **Header**: Your dining hall name and location
- **Statistics Cards**: 
  - Total Items
  - Available Items (not expired, quantity > 0)
  - Expiring Soon (< 4 hours)
- **Inventory Table**: All your surplus food items

#### 4. **Add New Surplus Item**

1. Click the "+ Add New Item" button
2. Fill in the form:
   - **Item Name**: e.g., "Chicken Tikka Masala"
   - **Food Type**: Select from dropdown
   - **Original Price**: Regular menu price in dollars
   - **Quantity**: How many portions available
   - **Expires In**: Hours until expiration
3. Click "Add Item"

#### 5. **Update Quantities**

**Method 1: +/- Buttons**
- Click `-` to decrease quantity by 1
- Click `+` to increase quantity by 1

**Method 2: Direct Input**
- Click on the quantity number
- Type the new quantity
- Press Enter or click outside

#### 6. **Delete Items**

- Click the "Delete" button next to any item
- Confirm the deletion
- Item is permanently removed

#### 7. **Monitor Status**

Items are automatically color-coded:
- 🔴 **Red (Urgent)**: < 4 hours until expiry
- 🟡 **Orange (Warning)**: 4-8 hours until expiry
- 🟢 **Green (Good)**: > 8 hours until expiry

#### 8. **Logout**

Click the "Logout" button in the top-right corner

## API Endpoints

### Authentication
- `POST /admin/api/login` - Login
- `POST /admin/api/register` - Register new admin
- `POST /admin/api/logout` - Logout

### Inventory Management
- `GET /admin/api/inventory` - Get all items
- `POST /admin/api/add-item` - Add new item
- `POST /admin/api/update-quantity` - Increment/decrement quantity
- `POST /admin/api/set-quantity` - Set exact quantity
- `POST /admin/api/delete-item` - Delete item

## Security Features

✅ **Password Hashing**: Passwords are hashed using SHA-256  
✅ **Session Management**: Secure Flask sessions  
✅ **Authentication Required**: All admin API endpoints check authentication  
✅ **Restaurant Isolation**: Admins can only manage their own dining hall's inventory

## Workflow Example

### Scenario: End of Lunch Service

1. **Login** to admin dashboard
2. **Review** what food is left over
3. **Add items** that would otherwise go to waste:
   - "Pasta Alfredo" - 3 portions - expires in 4 hours
   - "Caesar Salad" - 5 portions - expires in 6 hours
   - "Garlic Bread" - 8 portions - expires in 3 hours
4. Students see these items in the app at 70% discount
5. As items are ordered, **update quantities**
6. **Delete** sold-out items
7. Food waste is reduced! ✨

## Tips for Dining Hall Staff

💡 **Best Practices:**
- Add items 2-3 hours before they would be thrown away
- Set realistic expiry times (account for pickup time)
- Update quantities immediately when items are picked up
- Use descriptive names so students know exactly what they're getting
- Mark allergen information in the item name (e.g., "Pizza - Contains Dairy")

💡 **Expiry Time Guidelines:**
- Hot food: 2-4 hours
- Cold prepared food: 4-8 hours
- Baked goods: 6-12 hours
- Pre-packaged items: Use actual expiry date

## Troubleshooting

### Can't Login?
- Verify username and password
- Make sure you registered first
- Try the demo account (admin/admin123)

### Can't Add Items?
- Make sure you're logged in
- Check all required fields are filled
- Ensure price and quantity are positive numbers

### Items Not Showing Up?
- Refresh the page
- Check if items have already expired
- Verify you're looking at the correct dining hall's inventory

## Future Enhancements

Potential features to add:
- 📊 Analytics dashboard (items saved, revenue, waste reduction)
- 📧 Email notifications when items are about to expire
- 📱 Mobile app for on-the-go management
- 🔔 Alert admins when inventory is running low
- 📈 Historical data and trends
- 🏆 Leaderboard for dining halls reducing most waste

---

**Questions or Issues?**  
Contact the Bhookh Buster support team or check the main README.md
