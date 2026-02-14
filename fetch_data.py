import requests
from config import GOLD_API_KEY, METAL, CURRENCY
import time

BASE_URL = "https://www.goldapi.io/api"

def fetch_gold_price():
    url = f"{BASE_URL}/{METAL}/{CURRENCY}"
    
    headers = {
        "x-access-token": GOLD_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "timestamp": int(time.time()),
                "price": float(data.get("price", 1950.50)),
                "currency": data.get("currency", "USD")
            }
        else:
            print(f"API Error {response.status_code}")
            return {
                "timestamp": int(time.time()),
                "price": 1950.50,
                "currency": "USD"
            }
            
    except Exception as e:
        print(f"Error: {e}")
        return {
            "timestamp": int(time.time()),
            "price": 1950.50,
            "currency": "USD"
        }