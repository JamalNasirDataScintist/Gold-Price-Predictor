import os
import joblib
import numpy as np

MODEL_PATH = "models/gold_model.pkl"

def predict_next_price(current_price):
    """
    Predict the next gold price based on current price
    
    Args:
        current_price (float): Current gold price
    
    Returns:
        float: Predicted next price
    """
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. "
            "Please train the model first by running train_model.py"
        )
    
    try:
        # Load model
        model = joblib.load(MODEL_PATH)
        
        # Make prediction
        prediction = model.predict([[current_price]])
        
        return float(prediction[0])
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        # Return a simple fallback prediction
        return current_price * 1.01  # 1% increase as fallback