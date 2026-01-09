
import pickle
import pandas as pd
import numpy as np
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from config import ETA_MODEL_PATH, SCALER_PATH

def load_model():
    try:
        with open(ETA_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        return model, scaler
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

def predict_duration(model, scaler, distance, hour):
    # Rush hour definition matches main.py logic (7-10 AM or 5-8 PM)
    is_rush = 1 if (7 <= hour < 10) or (17 <= hour < 20) else 0
    is_morning_rush = 1 if 7 <= hour < 10 else 0
    is_evening_rush = 1 if 17 <= hour < 20 else 0
    
    # Feature array (Must match main.py order exactly)
    features = np.array([[
        distance,          # distance
        hour,              # hour
        2,                 # day_of_week (Wednesday)
        is_rush,           # is_rush_hour
        0,                 # is_weekend
        is_morning_rush,   # is_morning_rush
        is_evening_rush,   # is_evening_rush
        0,                 # is_late_night
        1                  # vehicle_encoded (Sedan)
    ]])
    
    feature_names = [
        'trip_distance', 'hour', 'day_of_week', 'is_rush_hour', 
        'is_weekend', 'is_morning_rush', 'is_evening_rush', 
        'is_late_night', 'vehicle_encoded'
    ]
    
    df = pd.DataFrame(features, columns=feature_names)
    scaled = scaler.transform(df)
    return model.predict(scaled)[0]

if __name__ == "__main__":
    model, scaler = load_model()
    if model:
        dist = 5.0 # 5 km trip
        
        # Test 1: Normal Time (2 PM)
        time_normal = predict_duration(model, scaler, dist, 14)
        print(f"\nScenario 1: 5km trip at 2:00 PM (Normal)")
        print(f"Prediction: {time_normal:.2f} minutes")
        
        # Test 2: Rush Hour (9 AM)
        time_rush = predict_duration(model, scaler, dist, 9)
        print(f"\nScenario 2: 5km trip at 9:00 AM (Rush Hour)")
        print(f"Prediction: {time_rush:.2f} minutes")
        
        increase = time_rush - time_normal
        percent = (increase / time_normal) * 100
        print(f"\nRESULT: Rush Hour added {increase:.2f} minutes (+{percent:.1f}%)")
    else:
        print("Could not load model.")
