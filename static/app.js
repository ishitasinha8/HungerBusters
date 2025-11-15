/**
 * Frontend JavaScript for Bhookh Buster Application
 */

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
    })
    .catch(error => {
        console.error('Registration error:', error);
        alert('Error registering. Please try again.');
    });
}

function getSurpriseBag() {
    currentMode = 'surprise';
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('moodSelector').classList.remove('active');
    document.getElementById('resultsContent').innerHTML = 
        '<div class="loading">Preparing your surprise bag from Cornell Dining</div>';
    
    fetch('/api/surprise-bag')
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                document.getElementById('resultsContent').innerHTML = 
                    `<p style="color: red; text-align: center;">${data.error}</p>`;
                return;
            }
            displaySurpriseBag(data.items);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resultsContent').innerHTML = 
                '<p style="color: red; text-align: center;">Error loading surprise bag. Please try again.</p>';
        });
}

function showCustomBag() {
    currentMode = 'custom';
    selectedItems = [];
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('moodSelector').classList.add('active');
    document.getElementById('resultsContent').innerHTML = '';
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
        '<div class="loading">Getting AI-powered suggestions from Cornell dining halls</div>';
    
    fetch('/api/suggestions', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({mood: selectedMood})
    })
    .then(res => res.json())
    .then(data => {
        displayCustomItems(data);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultsContent').innerHTML = 
            '<p style="color: red; text-align: center;">Error loading suggestions. Please try again.</p>';
    });
}

function displaySurpriseBag(items) {
    let html = '<h2 style="color: #333; margin-bottom: 20px;">🎉 Your FREE Surprise Bag from Cornell Dining!</h2>';
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
                    <span class="original-price">$${(item.original_price/100).toFixed(2)}</span>
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
            <p>You've saved ${items.length} meals from Cornell Dining from going to waste!</p>
            <p style="margin-top: 10px;">Pick up your bag within 2 hours from the dining hall.</p>
            <button class="btn" style="background: white; color: #4CAF50; margin-top: 15px;" onclick="location.reload()">
                Get Another Bag
            </button>
        </div>
    `;
    
    document.getElementById('resultsContent').innerHTML = html;
}

function displayCustomItems(suggestions) {
    let html = '<h2 style="color: #333; margin-bottom: 20px;">🤖 AI-Powered Suggestions from Cornell Dining</h2>';
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
                    <span class="original-price">$${(item.original_price/100).toFixed(2)}</span>
                    <span class="discount-price">$${(suggestion.discount_price/100).toFixed(2)}</span>
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
                    <strong style="font-size: 1.5em; color: #333;">Total: $<span id="totalPrice">0</span></strong>
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
            itemsList += `<div style="padding: 8px 0; color: #666;">✓ ${name} - $${(price/100).toFixed(2)}</div>`;
        }
    });
    
    itemsList += '</div>';
    
    document.getElementById('selectedItemsList').innerHTML = itemsList;
    document.getElementById('totalPrice').textContent = (total/100).toFixed(2);
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
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error placing order. Please try again.');
    });
}

function displayOrderConfirmation(order) {
    const html = `
        <div class="success-message">
            <h2>🎉 Order Confirmed!</h2>
            <p style="font-size: 1.2em; margin: 15px 0;">Order ID: ${order.order_id}</p>
            <p>Total: $${(order.cost/100).toFixed(2)}</p>
            <p style="margin-top: 15px;">You saved $${(order.cost * 2.33/100).toFixed(2)} and rescued ${order.items.length} meals from Cornell Dining!</p>
            <button class="btn" style="background: white; color: #4CAF50; margin-top: 20px;" onclick="location.reload()">
                Order More Food
            </button>
        </div>
    `;
    
    document.getElementById('resultsContent').innerHTML = html;
}
