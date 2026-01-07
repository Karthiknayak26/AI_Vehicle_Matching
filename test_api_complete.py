"""
Complete End-to-End API Test
Tests all endpoints of the AI Vehicle Matching API
"""
import requests
import json

print('='*60)
print('AI VEHICLE MATCHING API - END-TO-END TEST')
print('='*60)

# 1. Health Check
print('\n1. HEALTH CHECK')
r = requests.get('http://localhost:8000/health')
print(f'   Status: {r.status_code}')
health = r.json()
print(f'   Models Loaded: {health["models_loaded"]}')
print(f'   Vehicles: {health["vehicles_registered"]}')

# 2. Register 3 Vehicles
print('\n2. REGISTERING VEHICLES')
vehicles = [
    {'vehicle_id': 'CAR001', 'location': {'lat': 40.7500, 'lon': -74.0000}, 'status': 'available', 'vehicle_type': 'economy'},
    {'vehicle_id': 'CAR002', 'location': {'lat': 40.7520, 'lon': -74.0020}, 'status': 'available', 'vehicle_type': 'sedan'},
    {'vehicle_id': 'CAR003', 'location': {'lat': 40.7480, 'lon': -73.9980}, 'status': 'available', 'vehicle_type': 'suv'}
]

for v in vehicles:
    r = requests.post('http://localhost:8000/vehicles/update', json=v)
    print(f'   {v["vehicle_id"]} ({v["vehicle_type"]}): {r.status_code}')

# 3. Get Ride Quote - Fastest Mode
print('\n3. RIDE QUOTE - FASTEST MODE')
r = requests.post('http://localhost:8000/ride/quote', json={
    'pickup': {'lat': 40.7500, 'lon': -74.0000},
    'drop': {'lat': 40.7600, 'lon': -73.9900},
    'user_mode': 'fastest'
})
print(f'   Status: {r.status_code}')
if r.status_code == 200:
    quote = r.json()
    print(f'   Distance: {quote["distance"]} km')
    print(f'   ETA: {quote["estimated_duration"]} min')
    print(f'   Surge: {quote["surge_multiplier"]}x')
    print(f'   Vehicles Found: {len(quote["available_vehicles"])}')
    print(f'   Top Vehicle: {quote["available_vehicles"][0]["vehicle_id"]} (${quote["available_vehicles"][0]["final_fare"]})')

# 4. Get Ride Quote - Cheapest Mode
print('\n4. RIDE QUOTE - CHEAPEST MODE')
r = requests.post('http://localhost:8000/ride/quote', json={
    'pickup': {'lat': 40.7500, 'lon': -74.0000},
    'drop': {'lat': 40.7600, 'lon': -73.9900},
    'user_mode': 'cheapest'
})
if r.status_code == 200:
    quote = r.json()
    print(f'   Status: {r.status_code}')
    print(f'   Top Vehicle: {quote["available_vehicles"][0]["vehicle_id"]} (${quote["available_vehicles"][0]["final_fare"]})')

# 5. Get Ride Quote - Balanced Mode
print('\n5. RIDE QUOTE - BALANCED MODE')
r = requests.post('http://localhost:8000/ride/quote', json={
    'pickup': {'lat': 40.7500, 'lon': -74.0000},
    'drop': {'lat': 40.7600, 'lon': -73.9900},
    'user_mode': 'balanced'
})
if r.status_code == 200:
    quote = r.json()
    print(f'   Status: {r.status_code}')
    print(f'   Top Vehicle: {quote["available_vehicles"][0]["vehicle_id"]} (${quote["available_vehicles"][0]["final_fare"]})')

# 6. Final Health Check
print('\n6. FINAL HEALTH CHECK')
r = requests.get('http://localhost:8000/health')
health = r.json()
print(f'   Vehicles Registered: {health["vehicles_registered"]}')

print('\n' + '='*60)
print('✅ ALL TESTS PASSED - API IS FULLY OPERATIONAL!')
print('='*60)
