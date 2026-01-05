"""
Test script for API endpoints

Demonstrates vehicle updates and ride quote requests.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("=" * 70)
    print("TEST 1: Health Check")
    print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_vehicle_update():
    """Test vehicle update endpoint"""
    print("=" * 70)
    print("TEST 2: Vehicle Updates")
    print("=" * 70)
    
    # Register 5 vehicles
    vehicles = [
        {
            "vehicle_id": "CAR001",
            "location": {"lat": 40.7500, "lon": -74.0000},
            "status": "available",
            "vehicle_type": "economy"
        },
        {
            "vehicle_id": "CAR002",
            "location": {"lat": 40.7520, "lon": -74.0020},
            "status": "available",
            "vehicle_type": "sedan"
        },
        {
            "vehicle_id": "CAR003",
            "location": {"lat": 40.7480, "lon": -73.9980},
            "status": "available",
            "vehicle_type": "suv"
        },
        {
            "vehicle_id": "CAR004",
            "location": {"lat": 40.7510, "lon": -74.0010},
            "status": "available",
            "vehicle_type": "economy"
        },
        {
            "vehicle_id": "CAR005",
            "location": {"lat": 40.7490, "lon": -73.9990},
            "status": "busy",
            "vehicle_type": "sedan"
        }
    ]
    
    for vehicle in vehicles:
        response = requests.post(
            f"{BASE_URL}/vehicles/update",
            json=vehicle
        )
        print(f"Vehicle {vehicle['vehicle_id']}: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Region: {data['region_id']}, Surge: {data['current_surge']}×")
    
    print()


def test_ride_quote_fastest():
    """Test ride quote with fastest mode"""
    print("=" * 70)
    print("TEST 3: Ride Quote (Fastest Mode)")
    print("=" * 70)
    
    request_data = {
        "pickup": {"lat": 40.7500, "lon": -74.0000},
        "drop": {"lat": 40.7600, "lon": -73.9900},
        "timestamp": datetime.now().isoformat(),
        "user_mode": "fastest"
    }
    
    response = requests.post(
        f"{BASE_URL}/ride/quote",
        json=request_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nRequest ID: {data['request_id']}")
        print(f"Distance: {data['distance']} km")
        print(f"Estimated Duration: {data['estimated_duration']} min")
        print(f"Surge: {data['surge_multiplier']}× ({data['surge_reason']})")
        print(f"\nTop {len(data['available_vehicles'])} Vehicles (Fastest Mode):")
        
        for i, vehicle in enumerate(data['available_vehicles'], 1):
            print(f"\n{i}. {vehicle['vehicle_id']} ({vehicle['vehicle_type']})")
            print(f"   Pickup ETA: {vehicle['eta_pickup']} min")
            print(f"   Trip ETA: {vehicle['eta_trip']} min")
            print(f"   Fare: ${vehicle['final_fare']}")
            print(f"   Score: {vehicle['score']}")
    else:
        print(f"Error: {response.json()}")
    
    print()


def test_ride_quote_cheapest():
    """Test ride quote with cheapest mode"""
    print("=" * 70)
    print("TEST 4: Ride Quote (Cheapest Mode)")
    print("=" * 70)
    
    request_data = {
        "pickup": {"lat": 40.7500, "lon": -74.0000},
        "drop": {"lat": 40.7600, "lon": -73.9900},
        "user_mode": "cheapest"
    }
    
    response = requests.post(
        f"{BASE_URL}/ride/quote",
        json=request_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Top {len(data['available_vehicles'])} Vehicles (Cheapest Mode):")
        
        for i, vehicle in enumerate(data['available_vehicles'], 1):
            print(f"\n{i}. {vehicle['vehicle_id']} ({vehicle['vehicle_type']})")
            print(f"   Pickup ETA: {vehicle['eta_pickup']} min")
            print(f"   Fare: ${vehicle['final_fare']}")
            print(f"   Score: {vehicle['score']}")
    
    print()


def test_ride_quote_balanced():
    """Test ride quote with balanced mode"""
    print("=" * 70)
    print("TEST 5: Ride Quote (Balanced Mode)")
    print("=" * 70)
    
    request_data = {
        "pickup": {"lat": 40.7500, "lon": -74.0000},
        "drop": {"lat": 40.7600, "lon": -73.9900},
        "user_mode": "balanced"
    }
    
    response = requests.post(
        f"{BASE_URL}/ride/quote",
        json=request_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Top {len(data['available_vehicles'])} Vehicles (Balanced Mode):")
        
        for i, vehicle in enumerate(data['available_vehicles'], 1):
            print(f"\n{i}. {vehicle['vehicle_id']} ({vehicle['vehicle_type']})")
            print(f"   Pickup ETA: {vehicle['eta_pickup']} min")
            print(f"   Fare: ${vehicle['final_fare']}")
            print(f"   Score: {vehicle['score']}")
    
    print()


def run_all_tests():
    """Run all tests"""
    try:
        test_health_check()
        test_vehicle_update()
        test_ride_quote_fastest()
        test_ride_quote_cheapest()
        test_ride_quote_balanced()
        
        print("=" * 70)
        print("ALL TESTS COMPLETED")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("Make sure the server is running:")
        print("  python api/main.py")
        print("  or")
        print("  uvicorn api.main:app --reload")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AI VEHICLE MATCHING API - TEST SUITE")
    print("=" * 70)
    print()
    
    run_all_tests()
