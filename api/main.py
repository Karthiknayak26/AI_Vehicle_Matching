"""
FastAPI Application for AI Vehicle Matching System

Provides REST API endpoints for vehicle updates and ride quotes.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import pickle
import numpy as np
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.features.distance import haversine_distance
from src.features.temporal import extract_temporal_features
from src.pricing.dynamic_pricing import (
    load_demand_model,
    get_region_id,
    get_surge_with_fallback,
    calculate_fare
)
from src.ranking.vehicle_ranker import rank_vehicles, format_vehicle_for_response
from config import ETA_MODEL_PATH, SCALER_PATH, TOP_K_VEHICLES

# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class Location(BaseModel):
    """Geographic location"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")


class VehicleUpdate(BaseModel):
    """Vehicle location and status update"""
    vehicle_id: str = Field(..., min_length=1, description="Unique vehicle ID")
    location: Location
    status: str = Field(..., pattern="^(available|busy|offline)$", description="Vehicle status")
    vehicle_type: str = Field(..., pattern="^(economy|sedan|suv)$", description="Vehicle type")


class RideQuoteRequest(BaseModel):
    """Ride quote request"""
    pickup: Location
    drop: Location
    timestamp: Optional[str] = Field(None, description="ISO format timestamp (default: now)")
    user_mode: Optional[str] = Field('balanced', pattern="^(fastest|cheapest|balanced)$")


class FareBreakdown(BaseModel):
    """Fare breakdown"""
    base_fare: float
    distance_cost: float
    time_cost: float
    subtotal: float
    surge_multiplier: float
    final_fare: float


class VehicleOption(BaseModel):
    """Vehicle option in quote response"""
    vehicle_id: str
    vehicle_type: str
    eta_pickup: float  # minutes
    eta_trip: float  # minutes
    fare_breakdown: FareBreakdown
    final_fare: float
    score: float


class RideQuoteResponse(BaseModel):
    """Ride quote response"""
    request_id: str
    pickup: Location
    drop: Location
    distance: float  # km
    estimated_duration: float  # minutes
    surge_multiplier: float
    surge_reason: str
    available_vehicles: List[VehicleOption]


class VehicleUpdateResponse(BaseModel):
    """Vehicle update response"""
    vehicle_id: str
    updated: bool
    region_id: str
    nearby_requests: int
    current_surge: float


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="AI Vehicle Matching API",
    description="Dynamic pricing and vehicle ranking for ride-hailing",
    version="1.0.0"
)

# Global state (in production, use Redis or database)
vehicle_registry: Dict[str, Dict] = {}
demand_model = None
eta_model = None
scaler = None


@app.on_event("startup")
async def load_models():
    """Load ML models on startup"""
    global demand_model, eta_model, scaler
    
    print("Loading models...")
    
    # Load demand model
    demand_model = load_demand_model()
    if demand_model:
        print(f"✓ Demand model loaded ({len(demand_model)} region-hour slots)")
    else:
        print("⚠ Demand model not found, using defaults")
    
    # Load ETA model
    try:
        with open(ETA_MODEL_PATH, 'rb') as f:
            eta_model = pickle.load(f)
        print(f"✓ ETA model loaded from {ETA_MODEL_PATH}")
    except FileNotFoundError:
        print(f"⚠ ETA model not found at {ETA_MODEL_PATH}")
        eta_model = None
    
    # Load scaler
    try:
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        print(f"✓ Feature scaler loaded from {SCALER_PATH}")
    except FileNotFoundError:
        print(f"⚠ Scaler not found at {SCALER_PATH}")
        scaler = None
    
    print("Models loaded successfully!")


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "AI Vehicle Matching API",
        "version": "1.0.0",
        "endpoints": {
            "POST /vehicles/update": "Update vehicle location and status",
            "POST /ride/quote": "Get ride quote with vehicle recommendations"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": {
            "demand_model": demand_model is not None,
            "eta_model": eta_model is not None,
            "scaler": scaler is not None
        },
        "vehicles_registered": len(vehicle_registry)
    }


@app.post("/vehicles/update", response_model=VehicleUpdateResponse)
async def update_vehicle(vehicle: VehicleUpdate):
    """
    Update vehicle location and status
    
    Stores vehicle in registry and returns current demand info for the region.
    """
    # Update vehicle registry
    vehicle_registry[vehicle.vehicle_id] = {
        'id': vehicle.vehicle_id,
        'location': {'lat': vehicle.location.lat, 'lon': vehicle.location.lon},
        'status': vehicle.status,
        'vehicle_type': vehicle.vehicle_type,
        'last_updated': datetime.now().isoformat()
    }
    
    # Determine region
    region_id = get_region_id(vehicle.location.lat, vehicle.location.lon)
    
    # Get current hour
    current_hour = datetime.now().hour
    
    # Count available vehicles in region
    available_in_region = sum(
        1 for v in vehicle_registry.values()
        if v['status'] == 'available' and 
        get_region_id(v['location']['lat'], v['location']['lon']) == region_id
    )
    
    # Get surge for this region
    surge, _ = get_surge_with_fallback(
        region_id, current_hour, available_in_region, demand_model
    )
    
    # Mock nearby requests (in production, query from database)
    nearby_requests = max(0, int(np.random.normal(5, 2)))
    
    return VehicleUpdateResponse(
        vehicle_id=vehicle.vehicle_id,
        updated=True,
        region_id=region_id,
        nearby_requests=nearby_requests,
        current_surge=surge
    )


@app.post("/ride/quote", response_model=RideQuoteResponse)
async def get_ride_quote(request: RideQuoteRequest):
    """
    Get ride quote with vehicle recommendations
    
    Steps:
    1. Calculate trip distance and predict duration
    2. Determine surge pricing based on demand
    3. Find available vehicles and calculate costs
    4. Rank vehicles by user preference
    5. Return top-k vehicles
    """
    # Parse timestamp
    if request.timestamp:
        try:
            request_time = datetime.fromisoformat(request.timestamp.replace('Z', '+00:00'))
        except:
            raise HTTPException(status_code=400, detail="Invalid timestamp format")
    else:
        request_time = datetime.now()
    
    # 1. Calculate trip distance
    distance = haversine_distance(
        request.pickup.lat, request.pickup.lon,
        request.drop.lat, request.drop.lon
    )
    
    # 2. Extract temporal features
    hour = request_time.hour
    day_of_week = request_time.weekday()
    day_of_month = request_time.day
    month = request_time.month
    
    # Calculate temporal flags
    is_rush_hour = 1 if (7 <= hour < 10) or (17 <= hour < 20) else 0
    is_morning_rush = 1 if 7 <= hour < 10 else 0
    is_evening_rush = 1 if 17 <= hour < 20 else 0
    is_weekend = 1 if day_of_week >= 5 else 0
    is_late_night = 1 if hour >= 23 or hour < 5 else 0

    
    # 3. Predict trip duration using ETA model
    if eta_model and scaler:
        # Prepare features (must match training order)
        features = np.array([[
            distance,
            hour,
            day_of_week,
            day_of_month,
            month,
            is_rush_hour,
            is_morning_rush,
            is_evening_rush,
            is_weekend,
            is_late_night,
            1  # vehicle_encoded (economy as default for prediction)
        ]])
        
        # Predict duration
        duration = eta_model.predict(features)[0]
    else:
        # Fallback: simple estimation
        duration = distance / 0.5  # Assume 30 km/h average speed
    
    # 4. Determine pickup region and surge
    pickup_region = get_region_id(request.pickup.lat, request.pickup.lon)
    
    # Count available vehicles in region
    available_in_region = sum(
        1 for v in vehicle_registry.values()
        if v['status'] == 'available' and 
        get_region_id(v['location']['lat'], v['location']['lon']) == pickup_region
    )
    
    surge, surge_reason = get_surge_with_fallback(
        pickup_region, hour, max(available_in_region, 1), demand_model
    )
    
    # 5. Find available vehicles and calculate costs
    available_vehicles = []
    
    for vehicle_id, vehicle_data in vehicle_registry.items():
        if vehicle_data['status'] != 'available':
            continue
        
        # Calculate pickup ETA (simple distance-based)
        pickup_distance = haversine_distance(
            vehicle_data['location']['lat'],
            vehicle_data['location']['lon'],
            request.pickup.lat,
            request.pickup.lon
        )
        
        # Skip if too far
        if pickup_distance > 5.0:  # 5km max radius
            continue
        
        # Estimate pickup time (assume 40 km/h in city)
        eta_pickup = (pickup_distance / 40.0) * 60  # minutes
        
        # Calculate fare
        fare = calculate_fare(
            distance, duration, vehicle_data['vehicle_type'], surge
        )
        
        available_vehicles.append({
            'id': vehicle_id,
            'vehicle_type': vehicle_data['vehicle_type'],
            'eta_pickup': eta_pickup,
            'trip_cost': fare['final_fare'],
            'fare_breakdown': fare
        })
    
    # Check if any vehicles available
    if not available_vehicles:
        raise HTTPException(
            status_code=404,
            detail="No vehicles available in your area"
        )
    
    # 6. Rank vehicles by user preference
    ranked_vehicles = rank_vehicles(
        available_vehicles,
        user_mode=request.user_mode,
        top_k=TOP_K_VEHICLES
    )
    
    # 7. Format response
    vehicle_options = []
    for v in ranked_vehicles:
        vehicle_options.append(VehicleOption(
            vehicle_id=v['id'],
            vehicle_type=v['vehicle_type'],
            eta_pickup=round(v['eta_pickup'], 1),
            eta_trip=round(duration, 1),
            fare_breakdown=FareBreakdown(**v['fare_breakdown']),
            final_fare=v['trip_cost'],
            score=round(v['final_score'], 3)
        ))
    
    # Generate request ID
    request_id = f"REQ_{datetime.now().strftime('%Y%m%d%H%M%S')}_{np.random.randint(1000, 9999)}"
    
    return RideQuoteResponse(
        request_id=request_id,
        pickup=request.pickup,
        drop=request.drop,
        distance=round(distance, 2),
        estimated_duration=round(duration, 1),
        surge_multiplier=surge,
        surge_reason=surge_reason,
        available_vehicles=vehicle_options
    )


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
