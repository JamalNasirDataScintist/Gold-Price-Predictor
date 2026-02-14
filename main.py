import sys
import os

def main():
    print("💰 Gold Price Predictor")
    print("=======================")
    print("1. Fetch current gold price")
    print("2. Train prediction model")
    print("3. Run Streamlit web app")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == "1":
        from fetch_data import fetch_gold_price
        from data_store import save_price
        data = fetch_gold_price()
        save_price(data)
        print(f"✅ Price fetched: {data['price']} {data['currency']}")
        
    elif choice == "2":
        os.system("python train_model.py")
        
    elif choice == "3":
        os.system("streamlit run streamlit_app.py")
        
    elif choice == "4":
        print("Goodbye!")
        sys.exit(0)
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()