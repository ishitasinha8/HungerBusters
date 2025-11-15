# 🍽️ Bhookh Buster - Cornell Dining Edition

A food security web application that helps reduce food waste from Cornell dining halls by connecting students with surplus food at discounted prices.

## 📁 Project Structure

```
bhookh_buster/
├── app.py                          # Main Flask application
├── models.py                       # Data models (User, Restaurant, Order)
├── cornell_dining_scraper.py       # Cornell dining data scraper
├── data_manager.py                 # Data loading and management
├── config.py                       # Configuration settings
├── templates.py                    # HTML templates
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/                           # Data directory (created automatically)
│   └── cornell_dining_bhookh_buster.json
└── static/                         # Static files (create this folder)
    └── app.js                      # Frontend JavaScript

```

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Required Directories

```bash
mkdir -p data static
```

### 3. Add JavaScript File

Create `static/app.js` and copy the frontend JavaScript code from the `app.js` artifact.

## 📊 Usage

### Step 1: Fetch Cornell Dining Data

Run the scraper to fetch dining hall data from Cornell's API:

```bash
python cornell_scraper_modular.py
```

This will:
- Fetch data from Cornell's dining API
- Transform it into Bhookh Buster format
- Save it to `data/cornell_dining_bhookh_buster.json`

### Step 2: Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Step 3: Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## 🏗️ Architecture

### Core Components

#### 1. **config.py**
- Configuration settings for the entire application
- API endpoints, business logic constants
- Mood-food mappings, scoring weights

#### 2. **models.py**
- `User`: Manages user data and preferences
- `Restaurant`: Represents dining halls and their inventory
- `Order`: Tracks food orders

#### 3. **cornell_dining_scraper.py**
- `CornellDiningScraper`: Fetches and transforms Cornell dining data
- Connects to Cornell's dining API
- Generates sample menu items based on dining hall type

#### 4. **data_manager.py**
- `DataManager`: Handles data loading and persistence
- Loads from saved JSON file or fetches fresh data
- Manages restaurant inventory

#### 5. **app.py**
- `BhookhBusterService`: Core business logic
- Flask routes for API endpoints
- Main application entry point

#### 6. **templates.py**
- HTML template for the web interface

#### 7. **static/app.js**
- Frontend JavaScript for user interactions

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/register` | POST | Register a new user |
| `/api/surprise-bag` | GET | Get a free surprise bag |
| `/api/suggestions` | POST | Get AI-powered suggestions |
| `/api/custom-order` | POST | Create a custom order |
| `/api/rate-item` | POST | Rate a food item |
| `/api/refresh-data` | POST | Refresh dining data from API |

## ✨ Features

### For Users
- **Free Surprise Bags**: Get mystery bags of surplus food for free
- **Custom Bags**: Choose specific items at 70% discount
- **AI Recommendations**: Mood-based food suggestions
- **Dietary Preferences**: Filter by vegetarian, vegan, healthy, etc.

### For Administrators
- **Data Scraping**: Automatic fetching of Cornell dining data
- **Flexible Configuration**: Easy-to-modify settings in `config.py`
- **Modular Architecture**: Clean separation of concerns

## 🎯 How It Works

1. **User Registration**: Students register with location and dietary preferences
2. **Data Loading**: App loads dining hall data from Cornell's API
3. **AI Scoring**: Items are scored based on:
   - User preferences and past interactions
   - Mood-food compatibility
   - Urgency (expiry time)
   - Dietary restrictions
4. **Order Creation**: Users select items or get surprise bags
5. **Food Waste Reduction**: Surplus food gets consumed instead of wasted

## 🔄 Modular Design Benefits

- **Separation of Concerns**: Each file has a single, clear responsibility
- **Easy Testing**: Individual components can be tested separately
- **Maintainability**: Changes to one module don't affect others
- **Scalability**: Easy to add new features or data sources
- **Reusability**: Components can be reused in other projects

## 🛠️ Configuration

Edit `config.py` to customize:
- Discount rates
- Scoring weights
- API endpoints
- Campus locations
- Dietary preferences
- Mood-food mappings

## 📝 Development

### Adding a New Data Source

1. Create a new scraper in a separate file (e.g., `other_scraper.py`)
2. Implement the same interface as `CornellDiningScraper`
3. Update `data_manager.py` to support the new source

### Modifying Business Logic

1. Edit `config.py` for scoring weights and constants
2. Update `BhookhBusterService` in `app.py` for logic changes
3. Modify models in `models.py` for data structure changes

## 🐛 Troubleshooting

### Data Not Loading
- Check if `data/cornell_dining_bhookh_buster.json` exists
- Run `python cornell_dining_scraper.py` to fetch fresh data
- App will use demo data as fallback if Cornell API is unavailable

### API Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that the `static/` directory exists with `app.js`
- Verify Flask is running on port 5000

## 📄 License

This project is for educational purposes as part of a food waste reduction initiative.

## 🤝 Contributing

This modular architecture makes it easy to contribute:
1. Fork the repository
2. Create a feature branch
3. Make changes to the relevant module
4. Test your changes
5. Submit a pull request

---

Made with ❤️ to fight food waste at Cornell University
