import requests
from bs4 import BeautifulSoup
import csv
import os
from requests.exceptions import RequestException, Timeout, ConnectionError

def extract_product_data(url):
    """Extracts product data from a URL"""
    products = []
    
    # Network error handling
    try:
        print(f"Connecting to {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Timeout:
        print(f"Error: Timeout while connecting to {url}")
        return None
    except ConnectionError:
        print(f"Error: Could not connect to {url}")
        return None
    except RequestException as e:
        print(f"Network error: {e}")
        return None
    
    # Process content
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all(["div", "li", "article"])
    
    for item in items[:100]:  # Limit to first 100 items to avoid overload
        text = item.get_text(strip=True)
        if len(text) > 30 and any(char.isdigit() for char in text):
            # Extract more useful information
            price = item.find(class_=["price", "precio"])
            name = item.find(class_=["name", "title", "product-name"])
            
            product_data = [
                text[:100],  # Short description
                price.get_text(strip=True) if price else "No price",
                name.get_text(strip=True) if name else "No name"
            ]
            products.append(product_data)
    
    return products

def save_to_csv(products, filename="data.csv"):
    """Saves data to CSV with error handling"""
    if not products:
        print("No data to save")
        return False
    
    try:
        # Check if we can write to the directory
        current_dir = os.getcwd()
        test_file = os.path.join(current_dir, "test_write.tmp")
        
        # Test write permissions
        try:
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except IOError as e:
            print(f"Cannot write to {current_dir}: {e}")
            return False
        
        # Save data
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Extracted Data", "Price", "Name"])
            writer.writerows(products)
        
        print(f"Data saved to {filename}")
        print(f"Total items extracted: {len(products)}")
        
        # Show file information
        file_size = os.path.getsize(filename)
        print(f"File size: {file_size} bytes")
        
        return True
        
    except PermissionError:
        print(f"Error: Permission denied to write {filename}")
        print("Suggestion: Try saving to a different location")
        return False
    except OSError as e:
        print(f"System error while saving file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error while saving: {e}")
        return False

def main():
    """Main function with error handling"""
    print("=== Web Product Scraper ===")
    
    # Get URL with basic validation
    while True:
        url = input("Enter the website URL: ").strip()
        if url:
            if url.startswith(("http://", "https://")):
                break
            else:
                print("URL must start with http:// or https://")
        else:
            print("Please enter a valid URL")
    
    # Extract data
    products = extract_product_data(url)
    
    if products is None:
        print("Could not complete extraction")
        return
    
    if not products:
        print("No products found on the page")
        return
    
    if len(products) < 5:
        print("Warning: Very few items found, the page may require specific adjustments")
    
    # Ask for filename
    filename = input(f"CSV filename (default: data.csv): ").strip()
    if not filename:
        filename = "data.csv"
    elif not filename.endswith(".csv"):
        filename += ".csv"
    
    # Save data
    save_to_csv(products, filename)

if __name__ == "__main__":
    main()