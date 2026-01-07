"""
Dynamic Pricing Module

Calculates surge multipliers based on demand-supply ratio with fallback logic.
"""

import pickle
import numpy as np
from typing import Dict, Optional, Tuple
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    VEHICLE_BASE_FARES,
    PRICE_PER_KM,
    PRICE_PER_MIN,
    SURGE_CAP,
    DEFAULT_SURGE,
    SURGE_THRESHOLDS,
    SURGE_MULTIPLIERS,
    DEMAND_MODEL_PATH
)


def load_demand_model():
    """Load the demand estimation model"""
    try:
        with open(DEMAND_MODEL_PATH, 'rb') as f:
            demand_data = pickle.load(f)
        return demand_data
    except FileNotFoundError:
        print(f"Warning: Demand model not found at {DEMAND_MODEL_PATH}")
        return None


def get_region_id(lat: float, lon: float, grid_size: int = 5) -> str:
    """
    Convert lat/lon to region ID
    
    Args:
        lat: Latitude
        lon: Longitude
        grid_size: Grid size (default 5x5)
    
    Returns:
        str: Region ID (e.g., "2_3")
    """
    # City bounds (must match training data)
    min_lat, max_lat = 40.7000, 40.8000
    min_lon, max_lon = -74.0200, -73.9200
    
    # Calculate grid indices
    lat_idx = int((lat - min_lat) / (max_lat - min_lat) * grid_size)
    lon_idx = int((lon - min_lon) / (max_lon - min_lon) * grid_size)
    
    # Clamp to valid range
    lat_idx = max(0, min(grid_size - 1, lat_idx))
    lon_idx = max(0, min(grid_size - 1, lon_idx))
    
    return f"{lat_idx}_{lon_idx}"


def get_demand_score(
    region_id: str,
    hour: int,
    demand_data: Optional[Dict] = None
) -> float:
    """
    Get demand score for a region and hour
    
    Args:
        region_id: Region identifier (e.g., "2_3")
        hour: Hour of day (0-23)
        demand_data: Loaded demand model data
    
    Returns:
        float: Demand score (0-1), or 0.5 if no data
    """
    if demand_data is None:
        return 0.5  # Default to medium demand
    
    # Look up demand score
    key = (region_id, hour)
    if key in demand_data:
        return demand_data[key].get('demand_score', 0.5)
    
    # Fallback 1: Try same region, nearest hour
    for hour_offset in [1, -1, 2, -2]:
        fallback_hour = (hour + hour_offset) % 24
        fallback_key = (region_id, fallback_hour)
        if fallback_key in demand_data:
            return demand_data[fallback_key].get('demand_score', 0.5)
    
    # Fallback 2: Try same hour, city-wide average
    hour_scores = [
        data.get('demand_score', 0.5)
        for (r, h), data in demand_data.items()
        if h == hour
    ]
    if hour_scores:
        return np.mean(hour_scores)
    
    # Fallback 3: Return default
    return 0.5


def calculate_demand_supply_ratio(
    region_id: str,
    hour: int,
    available_vehicles: int,
    demand_data: Optional[Dict] = None
) -> float:
    """
    Calculate demand-to-supply ratio
    
    Args:
        region_id: Region identifier
        hour: Hour of day (0-23)
        available_vehicles: Number of available vehicles in region
        demand_data: Loaded demand model data
    
    Returns:
        float: Demand-supply ratio (0-inf)
    """
    # Get demand score (0-1)
    demand_score = get_demand_score(region_id, hour, demand_data)
    
    # Convert demand score to estimated ride count
    # Assume max demand is ~50 rides/hour in peak region
    estimated_demand = demand_score * 50
    
    # Calculate ratio (avoid division by zero)
    supply = max(available_vehicles, 1)
    ratio = estimated_demand / supply
    
    return ratio


def get_surge_multiplier(
    demand_supply_ratio: float,
    surge_cap: float = SURGE_CAP
) -> float:
    """
    Derive surge multiplier from demand-supply ratio
    
    Thresholds:
    - ratio < 0.5: 0.9× (discount)
    - 0.5 ≤ ratio < 1.5: 1.0× (normal)
    - 1.5 ≤ ratio < 3.0: 1.3× (moderate surge)
    - ratio ≥ 3.0: 1.5× (high surge, capped)
    
    Args:
        demand_supply_ratio: Calculated demand-supply ratio
        surge_cap: Maximum surge multiplier (default from config)
    
    Returns:
        float: Surge multiplier (0.9 - surge_cap)
    """
    if demand_supply_ratio < SURGE_THRESHOLDS['discount']:
        multiplier = SURGE_MULTIPLIERS['discount']
    elif demand_supply_ratio < SURGE_THRESHOLDS['normal']:
        multiplier = SURGE_MULTIPLIERS['normal']
    elif demand_supply_ratio < SURGE_THRESHOLDS['moderate']:
        multiplier = SURGE_MULTIPLIERS['moderate']
    else:
        multiplier = SURGE_MULTIPLIERS['high']
    
    # Apply surge cap
    return min(multiplier, surge_cap)


def get_surge_with_fallback(
    region_id: str,
    hour: int,
    available_vehicles: int,
    demand_data: Optional[Dict] = None,
    default_surge: float = DEFAULT_SURGE
) -> Tuple[float, str]:
    """
    Get surge multiplier with comprehensive fallback logic
    
    Args:
        region_id: Region identifier
        hour: Hour of day (0-23)
        available_vehicles: Number of available vehicles
        demand_data: Loaded demand model data
        default_surge: Default surge if all else fails
    
    Returns:
        tuple: (surge_multiplier, reason)
            - surge_multiplier: float
            - reason: str explaining how surge was calculated
    """
    try:
        # Calculate demand-supply ratio
        ratio = calculate_demand_supply_ratio(
            region_id, hour, available_vehicles, demand_data
        )
        
        # Get surge multiplier
        surge = get_surge_multiplier(ratio)
        
        reason = f"Calculated from demand-supply ratio ({ratio:.2f})"
        return surge, reason
        
    except Exception as e:
        # Complete fallback - use friendly message
        print(f"Error calculating surge: {e}. Using default.")
        return default_surge, "Normal demand"


def calculate_fare(
    distance: float,
    duration: float,
    vehicle_type: str,
    surge_multiplier: float
) -> Dict[str, float]:
    """
    Calculate final fare with surge pricing
    
    Formula:
    base_fare = VEHICLE_BASE_FARES[vehicle_type]
    distance_cost = distance * PRICE_PER_KM[vehicle_type]
    time_cost = duration * PRICE_PER_MIN[vehicle_type]
    subtotal = base_fare + distance_cost + time_cost
    final_fare = subtotal * surge_multiplier
    
    Args:
        distance: Trip distance in kilometers
        duration: Trip duration in minutes
        vehicle_type: 'economy', 'sedan', or 'suv'
        surge_multiplier: Surge multiplier (0.9 - 1.5)
    
    Returns:
        dict: Fare breakdown with all components
    """
    # Validate vehicle type
    if vehicle_type not in VEHICLE_BASE_FARES:
        raise ValueError(f"Invalid vehicle type: {vehicle_type}")
    
    # Calculate components
    base_fare = VEHICLE_BASE_FARES[vehicle_type]
    distance_cost = distance * PRICE_PER_KM[vehicle_type]
    time_cost = duration * PRICE_PER_MIN[vehicle_type]
    subtotal = base_fare + distance_cost + time_cost
    final_fare = subtotal * surge_multiplier
    
    return {
        'base_fare': round(base_fare, 2),
        'distance_cost': round(distance_cost, 2),
        'time_cost': round(time_cost, 2),
        'subtotal': round(subtotal, 2),
        'surge_multiplier': round(surge_multiplier, 2),
        'final_fare': round(final_fare, 2)
    }


# Example usage
if __name__ == "__main__":
    # Load demand model
    demand_data = load_demand_model()
    
    # Example 1: High demand scenario
    print("Example 1: High demand (rush hour, city center)")
    region = "2_3"  # City center
    hour = 8  # Morning rush
    vehicles = 5
    
    ratio = calculate_demand_supply_ratio(region, hour, vehicles, demand_data)
    surge, reason = get_surge_with_fallback(region, hour, vehicles, demand_data)
    
    print(f"  Region: {region}, Hour: {hour}, Vehicles: {vehicles}")
    print(f"  Demand-supply ratio: {ratio:.2f}")
    print(f"  Surge multiplier: {surge}× ({reason})")
    
    fare = calculate_fare(5.0, 15.0, 'economy', surge)
    print(f"  Fare for 5km, 15min economy ride: ${fare['final_fare']}")
    print()
    
    # Example 2: Low demand scenario
    print("Example 2: Low demand (late night, suburbs)")
    region = "0_0"  # Suburbs
    hour = 2  # Late night
    vehicles = 10
    
    ratio = calculate_demand_supply_ratio(region, hour, vehicles, demand_data)
    surge, reason = get_surge_with_fallback(region, hour, vehicles, demand_data)
    
    print(f"  Region: {region}, Hour: {hour}, Vehicles: {vehicles}")
    print(f"  Demand-supply ratio: {ratio:.2f}")
    print(f"  Surge multiplier: {surge}× ({reason})")
    
    fare = calculate_fare(5.0, 15.0, 'economy', surge)
    print(f"  Fare for 5km, 15min economy ride: ${fare['final_fare']}")
