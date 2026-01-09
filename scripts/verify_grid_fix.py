
import sys
import os
import pickle

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pricing.dynamic_pricing import get_region_id, load_demand_model, get_demand_score, DEMAND_MODEL_PATH
from config import CITY_MIN_LAT, CITY_MAX_LAT, CITY_MIN_LON, CITY_MAX_LON

def verify():
    print("=== Configuration ===")
    print(f"Lat Range: {CITY_MIN_LAT} - {CITY_MAX_LAT}")
    print(f"Lon Range: {CITY_MIN_LON} - {CITY_MAX_LON}")
    
    # Test Center Point
    center_lat = (CITY_MIN_LAT + CITY_MAX_LAT) / 2
    center_lon = (CITY_MIN_LON + CITY_MAX_LON) / 2
    
    print(f"\nTesting Center Point: ({center_lat}, {center_lon})")
    try:
        region = get_region_id(center_lat, center_lon)
        print(f"Resulting Region ID: {region}")
        if region == "2_2":
            print("SUCCESS: Center point maps to middle grid 2_2")
        else:
            print(f"WARNING: Expected 2_2 for center, got {region}")
    except Exception as e:
        print(f"ERROR calling get_region_id: {e}")

    # Inspect Demand Model
    print("\n=== Demand Model Inspection ===")
    if os.path.exists(DEMAND_MODEL_PATH):
        try:
            with open(DEMAND_MODEL_PATH, 'rb') as f:
                data = pickle.load(f)
            print("Model loaded successfully.")
            print(f"Number of keys: {len(data)}")
            print("Sample keys:")
            if 'demand_data' in data:
                print("  (Found 'demand_data' key...)")
                inner = data['demand_data']
                print(f"  Type of inner data: {type(inner)}")
                if isinstance(inner, list):
                    print(f"  Length of list: {len(inner)}")
                    if len(inner) > 0:
                        item = inner[0]
                        print("\n--- FIRST ITEM DETAILS ---")
                        for k, v in item.items():
                            print(f"KEY: {k} | VALUE: {v}")
                        print("--------------------------\n")
                elif isinstance(inner, dict):
                     for k in list(inner.keys())[:5]:
                        print(f"  {k} -> {inner[k]}")
            else:
                for k in list(data.keys())[:5]:
                    print(f"  {k}")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print(f"Model file not found at {DEMAND_MODEL_PATH}")

    print("\n=== Testing Integrated Logic ===")
    try:
        model = load_demand_model()
        if model:
            print(f"Model loaded via load_demand_model(). Type: {type(model)}")
            if isinstance(model, dict):
                first_key = list(model.keys())[0]
                print(f"Sample key: {first_key}")
                
                # Test with the sample key logic
                score = get_demand_score(str(first_key), 10, model)
                print(f"Demand Score lookup: {score}")
                
                if score != 0.5:
                     print("SUCCESS: Retrieved non-default demand score.")
                else:
                     print("WARNING: Retrieved default score (0.5). Should check if this is correct.")
            else:
                 print("ERROR: load_demand_model() did not return a dictionary.")
    except Exception as e:
        print(f"ERROR testing logic: {e}")

if __name__ == "__main__":
    verify()
