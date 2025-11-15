import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_dining_hall_data():
    """
    Fetch dining hall data from Cornell's dining website.
    Returns a dictionary with dining hall information.
    """
    url = "https://now.dining.cornell.edu/eateries"
    
    try:
        # Fetch the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        dining_halls = []
        
        # Look for dining hall elements (common patterns on Cornell dining pages)
        # This may need adjustment based on actual HTML structure
        eatery_elements = soup.find_all(['div', 'article'], class_=lambda x: x and ('eatery' in x.lower() or 'dining' in x.lower()))
        
        for element in eatery_elements:
            hall_data = {}
            
            # Extract name
            name_elem = element.find(['h2', 'h3', 'h4'])
            if name_elem:
                hall_data['name'] = name_elem.get_text(strip=True)
            
            # Extract hours
            hours_elem = element.find(class_=lambda x: x and 'hour' in x.lower())
            if hours_elem:
                hall_data['hours'] = hours_elem.get_text(strip=True)
            
            # Extract status (open/closed)
            status_elem = element.find(class_=lambda x: x and ('status' in x.lower() or 'open' in x.lower()))
            if status_elem:
                hall_data['status'] = status_elem.get_text(strip=True)
            
            # Extract location
            location_elem = element.find(class_=lambda x: x and 'location' in x.lower())
            if location_elem:
                hall_data['location'] = location_elem.get_text(strip=True)
            
            if hall_data:
                dining_halls.append(hall_data)
        
        # If no structured data found, try to find any API endpoints
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'api' in script.string.lower():
                # Look for API URLs in the JavaScript
                pass
        
        return {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'dining_halls': dining_halls,
            'total_count': len(dining_halls)
        }
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None


def get_dining_api_data():
    """
    Alternative method: Try to fetch data from Cornell's dining API directly.
    Cornell often has a JSON API for their dining data.
    """
    api_urls = [
        "https://now.dining.cornell.edu/api/1.0/dining/eateries.json",
        "https://api.dining.cornell.edu/v1/eateries",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for api_url in api_urls:
        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    
    return None


def save_dining_data(data, filename='cornell_dining_data.json'):
    """Save dining data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")


def main():
    print("Fetching Cornell dining hall data...")
    
    # Try API first
    api_data = get_dining_api_data()
    if api_data:
        print("Successfully fetched data from API")
        print(json.dumps(api_data, indent=2))
        save_dining_data(api_data)
        return
    
    # Fall back to web scraping
    print("Trying web scraping...")
    data = get_dining_hall_data()
    
    if data and data['dining_halls']:
        print(f"Found {data['total_count']} dining halls:")
        print(json.dumps(data, indent=2))
        save_dining_data(data)
    else:
        print("No dining hall data found. The page may use dynamic JavaScript loading.")
        print("Consider using Selenium or checking for API endpoints.")


if __name__ == "__main__":
    main()
