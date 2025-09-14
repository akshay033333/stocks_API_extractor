import os
import requests
import csv
import json
import time
from datetime import datetime
from dotenv import load_dotenv

def load_api_key():
    """
    Load API key from .env file
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the API key
    api_key = os.getenv('POLYGON_API_KEY')
    
    if api_key:
        print(f"API Key loaded successfully")  # Show partial key for security
        return api_key
    else:
        print("Error: POLYGON_API_KEY not found in .env file")
        return None

def fetch_stock_tickers(api_key):
    """
    Fetch stock tickers from Polygon API with pagination
    """
    limit = 1000
    API_URI = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={limit}&sort=ticker&apiKey={api_key}"
    
    all_results = []
    current_url = API_URI
    page_count = 0
    
    try:
        print("Fetching stock data from Polygon API...")
        
        while current_url:
            page_count += 1
            print(f"📄 Fetching page {page_count}...")
            
            try:
                response = requests.get(current_url)
                
                # Handle rate limiting
                if response.status_code == 429:
                    print(f"   ⏳ Rate limit hit. Waiting 60 seconds before retrying...")
                    time.sleep(60)
                    continue
                
                response.raise_for_status()  # Raises an HTTPError for bad responses
                
                data = response.json()
                
                # Add results to our collection
                if 'results' in data and data['results']:
                    all_results.extend(data['results'])
                    print(f"   ✅ Added {len(data['results'])} tickers from page {page_count}")
                
                # Check if there's a next page
                if 'next_url' in data and data['next_url']:
                    # Add API key to the next_url since it doesn't include it
                    next_url = data['next_url']
                    if 'apiKey=' not in next_url:
                        separator = '&' if '?' in next_url else '?'
                        current_url = f"{next_url}{separator}apiKey={api_key}"
                    else:
                        current_url = next_url
                    print(f"   🔄 Next page available: {current_url[:50]}...")
                    
                    # Add a small delay to avoid rate limiting
                    time.sleep(0.5)
                else:
                    current_url = None
                    print(f"   🏁 No more pages available")
                    
            except requests.exceptions.RequestException as e:
                if "429" in str(e):
                    print(f"   ⏳ Rate limit hit. Waiting 60 seconds before retrying...")
                    time.sleep(60)
                    continue
                else:
                    print(f"   ❌ Error on page {page_count}: {e}")
                    break
        
        print(f"✅ Successfully fetched {len(all_results)} total stock tickers across {page_count} pages")
        
        # Return data in the same format as before
        return {
            'results': all_results,
            'status': 'OK',
            'count': len(all_results)
        }
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON response: {e}")
        return None

def save_to_csv(data, filename=None):
    """
    Save stock ticker data to CSV file
    """
    if not data or 'results' not in data:
        print("❌ No data to save")
        return False
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stock_tickers_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if data['results']:
                # Get fieldnames from the first result
                fieldnames = data['results'][0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for row in data['results']:
                    writer.writerow(row)
                
                print(f"✅ Data saved to {filename}")
                print(f"📊 Total records: {len(data['results'])}")
                return True
            else:
                print("❌ No data in results to save")
                return False
                
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")
        return False

def main():
    """
    Main function to fetch stock data and save to CSV
    """
    print("Loading API key from .env file...")
    api_key = load_api_key()
    
    if api_key:
        print("✅ API key is ready to use!")
        
        # Fetch stock data
        data = fetch_stock_tickers(api_key)
        
        if data:
            # Save to CSV
            save_to_csv(data)
        else:
            print("❌ Failed to fetch data")
    else:
        print("❌ Failed to load API key")

if __name__ == "__main__":
    main()


