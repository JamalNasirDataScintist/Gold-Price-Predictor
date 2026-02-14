import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

print("🔧 Training Gold Price Prediction Model...")
print("=" * 50)

# Create models directory
os.makedirs("models", exist_ok=True)

# Check if data exists
if not os.path.exists("data/gold_prices.csv"):
    print("❌ Error: No data found!")
    print("Please run the app and collect some data first.")
    exit(1)

# Load data
df = pd.read_csv("data/gold_prices.csv")
print(f"📊 Loaded {len(df)} records from data/gold_prices.csv")

if len(df) < 3:
    print(f"❌ Not enough data! Need at least 3 records, found {len(df)}")
    print("Please collect more data by running the app multiple times.")
    exit(1)

print("\n📈 Data Preview:")
print(df.tail())

# Create features (use previous price to predict next price)
df["previous_price"] = df["price"].shift(1)
df = df.dropna()  # Remove first row with NaN

print(f"\n🎯 Training on {len(df)} samples")

# Prepare training data
X = df[["previous_price"]]
y = df["price"]

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    max_depth=10,
    min_samples_split=5
)

model.fit(X, y)

# Save model
model_path = "models/gold_model.pkl"
joblib.dump(model, model_path)

print(f"\n✅ Model trained successfully!")
print(f"📍 Saved to: {model_path}")

# Show prediction example
if len(df) > 0:
    last_price = df["price"].iloc[-1]
    prediction = model.predict([[last_price]])[0]
    print(f"\n📊 Example Prediction:")
    print(f"   Last price: ${last_price:.2f}")
    print(f"   Next predicted: ${prediction:.2f}")
    print(f"   Change: ${(prediction - last_price):.2f}")