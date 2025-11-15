/**
 * Admin Dashboard JavaScript for Dining Hall Management
 */

// Load inventory on page load
document.addEventListener('DOMContentLoaded', function() {
    loadInventory();
});

function loadInventory() {
    fetch('/admin/api/inventory')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                displayInventory(data.items);
                updateStats(data.items);
            }
        })
        .catch(err => console.error('Error loading inventory:', err));
}

function displayInventory(items) {
    const tbody = document.getElementById('itemsBody');
    tbody.innerHTML = '';
    
    if (items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 40px; color: #999;">No items in inventory. Add your first surplus food item!</td></tr>';
        return;
    }
    
    items.forEach(item => {
        const expiryTime = new Date(item.expiry);
        const now = new Date();
        const hoursLeft = Math.round((expiryTime - now) / (1000 * 60 * 60));
        
        let statusBadge = '';
        if (hoursLeft < 4) {
            statusBadge = '<span class="badge badge-urgent">⚡ Urgent</span>';
        } else if (hoursLeft < 8) {
            statusBadge = '<span class="badge badge-warning">⚠️ Soon</span>';
        } else {
            statusBadge = '<span class="badge badge-good">✓ Good</span>';
        }
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${item.name}</strong></td>
            <td>${item.food_type}</td>
            <td>$${(item.original_price / 100).toFixed(2)}</td>
            <td>
                <div class="quantity-control">
                    <button onclick="updateQuantity('${item.item_id}', -1)">-</button>
                    <input type="number" value="${item.quantity}" 
                           onchange="setQuantity('${item.item_id}', this.value)"
                           min="0">
                    <button onclick="updateQuantity('${item.item_id}', 1)">+</button>
                </div>
            </td>
            <td>${hoursLeft}h</td>
            <td>${statusBadge}</td>
            <td>
                <button class="delete-btn" onclick="deleteItem('${item.item_id}')">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function updateStats(items) {
    const now = new Date();
    let availableCount = 0;
    let expiringSoonCount = 0;
    
    items.forEach(item => {
        const expiryTime = new Date(item.expiry);
        const hoursLeft = (expiryTime - now) / (1000 * 60 * 60);
        
        if (expiryTime > now && item.quantity > 0) {
            availableCount++;
        }
        
        if (hoursLeft < 4 && hoursLeft > 0) {
            expiringSoonCount++;
        }
    });
    
    document.getElementById('totalItems').textContent = items.length;
    document.getElementById('availableItems').textContent = availableCount;
    document.getElementById('expiringSoon').textContent = expiringSoonCount;
}

function showAddItemModal() {
    document.getElementById('addItemModal').classList.add('show');
}

function closeModal() {
    document.getElementById('addItemModal').classList.remove('show');
    document.getElementById('addItemForm').reset();
}

function addItem(event) {
    event.preventDefault();
    
    const data = {
        name: document.getElementById('itemName').value,
        food_type: document.getElementById('foodType').value,
        original_price: parseFloat(document.getElementById('price').value) * 100, // Convert to cents
        quantity: parseInt(document.getElementById('quantity').value),
        expiry_hours: parseInt(document.getElementById('expiryHours').value)
    };
    
    fetch('/admin/api/add-item', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeModal();
            loadInventory();
            alert('Item added successfully!');
        } else {
            alert('Error adding item: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(err => {
        alert('Error adding item. Please try again.');
        console.error('Error:', err);
    });
}

function updateQuantity(itemId, change) {
    fetch('/admin/api/update-quantity', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ item_id: itemId, change: change })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            loadInventory();
        } else {
            alert('Error updating quantity');
        }
    })
    .catch(err => console.error('Error:', err));
}

function setQuantity(itemId, newQuantity) {
    fetch('/admin/api/set-quantity', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ item_id: itemId, quantity: parseInt(newQuantity) })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            loadInventory();
        } else {
            alert('Error setting quantity');
        }
    })
    .catch(err => console.error('Error:', err));
}

function deleteItem(itemId) {
    if (!confirm('Are you sure you want to delete this item?')) {
        return;
    }
    
    fetch('/admin/api/delete-item', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ item_id: itemId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            loadInventory();
            alert('Item deleted successfully');
        } else {
            alert('Error deleting item');
        }
    })
    .catch(err => console.error('Error:', err));
}

function logout() {
    fetch('/admin/api/logout', { method: 'POST' })
        .then(() => {
            window.location.href = '/admin/login';
        });
}
