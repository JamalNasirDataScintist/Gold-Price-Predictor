import csv
import os
from datetime import datetime

DATA_FILE = "data/gold_prices.csv"

def save_price(data):
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Format timestamp
    timestamp_str = datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if file exists
    file_exists = os.path.isfile(DATA_FILE)
    
    # Append data to CSV
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Write header if file is new
        if not file_exists:
            writer.writerow(["timestamp", "price", "currency"])
        
        # Write data row
        writer.writerow([timestamp_str, data["price"], data["currency"]])
    
    print(f"✅ Price saved: {timestamp_str} - ${data['price']:.2f} {data['currency']}")