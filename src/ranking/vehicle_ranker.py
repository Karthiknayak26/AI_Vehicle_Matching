"""
Vehicle Ranking Module

Ranks vehicles based on user preferences (fastest/cheapest/balanced) using weighted scoring.
"""

import numpy as np
from typing import List, Dict, Optional
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    COMFORT_SCORES,
    USER_MODE_WEIGHTS,
    TOP_K_VEHICLES
)


def normalize_scores(values: List[float], lower_is_better: bool = True) -> List[float]:
    """
    Normalize values to 0-1 range using min-max scaling
    
    Args:
        values: List of values to normalize
        lower_is_better: If True, lower values get higher scores (for ETA, cost)
                        If False, higher values get higher scores (for comfort)
    
    Returns:
        list: Normalized scores (0-1, higher is better)
    """
    if not values or len(values) == 0:
        return []
    
    if len(values) == 1:
        return [1.0]  # Single value gets perfect score
    
    min_val = min(values)
    max_val = max(values)
    
    # Avoid division by zero
    if max_val == min_val:
        return [1.0] * len(values)
    
    if lower_is_better:
        # Lower values get higher scores (for ETA, cost)
        normalized = [(max_val - v) / (max_val - min_val) for v in values]
    else:
        # Higher values get higher scores (for comfort)
        normalized = [(v - min_val) / (max_val - min_val) for v in values]
    
    return normalized


def calculate_vehicle_score(
    vehicle: Dict,
    user_mode: str = 'balanced',
    eta_scores: Optional[List[float]] = None,
    cost_scores: Optional[List[float]] = None,
    comfort_scores: Optional[List[float]] = None
) -> float:
    """
    Calculate weighted score for a vehicle
    
    Args:
        vehicle: Vehicle dict with:
            - 'id': str
            - 'eta_pickup': float (minutes)
            - 'trip_cost': float (dollars)
            - 'vehicle_type': str
            - 'comfort_score': int (1-3)
            - 'eta_score_normalized': float (0-1, pre-normalized)
            - 'cost_score_normalized': float (0-1, pre-normalized)
            - 'comfort_score_normalized': float (0-1, pre-normalized)
        user_mode: 'fastest' | 'cheapest' | 'balanced'
    
    Returns:
        float: Weighted score (0-1, higher is better)
    """
    # Validate user mode
    if user_mode not in USER_MODE_WEIGHTS:
        user_mode = 'balanced'
    
    # Get weights for this mode
    weights = USER_MODE_WEIGHTS[user_mode]
    
    # Calculate weighted score
    score = (
        weights['eta'] * vehicle['eta_score_normalized'] +
        weights['cost'] * vehicle['cost_score_normalized'] +
        weights['comfort'] * vehicle['comfort_score_normalized']
    )
    
    return score


def rank_vehicles(
    available_vehicles: List[Dict],
    user_mode: str = 'balanced',
    top_k: int = TOP_K_VEHICLES
) -> List[Dict]:
    """
    Rank vehicles and return top-k
    
    Args:
        available_vehicles: List of vehicle dicts with:
            - 'id': str
            - 'eta_pickup': float (minutes to pickup)
            - 'trip_cost': float (total trip cost in dollars)
            - 'vehicle_type': str ('economy', 'sedan', 'suv')
            - Optional: 'comfort_score': int (1-3)
        user_mode: 'fastest' | 'cheapest' | 'balanced'
        top_k: Number of top vehicles to return
    
    Returns:
        list: Top-k vehicles with scores, sorted by score (descending)
    """
    if not available_vehicles:
        return []
    
    # Add comfort scores if not present
    for vehicle in available_vehicles:
        if 'comfort_score' not in vehicle:
            vehicle['comfort_score'] = COMFORT_SCORES.get(
                vehicle['vehicle_type'], 1
            )
    
    # Extract values for normalization
    eta_values = [v['eta_pickup'] for v in available_vehicles]
    cost_values = [v['trip_cost'] for v in available_vehicles]
    comfort_values = [v['comfort_score'] for v in available_vehicles]
    
    # Normalize scores
    eta_scores = normalize_scores(eta_values, lower_is_better=True)
    cost_scores = normalize_scores(cost_values, lower_is_better=True)
    comfort_scores = normalize_scores(comfort_values, lower_is_better=False)
    
    # Add normalized scores to vehicles
    for i, vehicle in enumerate(available_vehicles):
        vehicle['eta_score_normalized'] = eta_scores[i]
        vehicle['cost_score_normalized'] = cost_scores[i]
        vehicle['comfort_score_normalized'] = comfort_scores[i]
    
    # Calculate weighted scores
    for vehicle in available_vehicles:
        vehicle['final_score'] = calculate_vehicle_score(vehicle, user_mode)
    
    # Sort by score (descending)
    ranked_vehicles = sorted(
        available_vehicles,
        key=lambda v: v['final_score'],
        reverse=True
    )
    
    # Return top-k
    return ranked_vehicles[:top_k]


def format_vehicle_for_response(vehicle: Dict) -> Dict:
    """
    Format vehicle data for API response
    
    Args:
        vehicle: Vehicle dict with all scores
    
    Returns:
        dict: Formatted vehicle data
    """
    return {
        'vehicle_id': vehicle['id'],
        'vehicle_type': vehicle['vehicle_type'],
        'eta_pickup': round(vehicle['eta_pickup'], 1),
        'trip_cost': round(vehicle['trip_cost'], 2),
        'comfort_score': vehicle['comfort_score'],
        'final_score': round(vehicle['final_score'], 3),
        'fare_breakdown': vehicle.get('fare_breakdown', {})
    }


# Example usage
if __name__ == "__main__":
    # Mock available vehicles
    vehicles = [
        {
            'id': 'CAR001',
            'vehicle_type': 'economy',
            'eta_pickup': 3.0,  # 3 minutes away
            'trip_cost': 15.50,
            'fare_breakdown': {'base': 2.5, 'distance': 10.0, 'time': 3.0}
        },
        {
            'id': 'CAR002',
            'vehicle_type': 'sedan',
            'eta_pickup': 5.0,  # 5 minutes away
            'trip_cost': 18.00,
            'fare_breakdown': {'base': 3.5, 'distance': 12.0, 'time': 2.5}
        },
        {
            'id': 'CAR003',
            'vehicle_type': 'suv',
            'eta_pickup': 2.0,  # 2 minutes away
            'trip_cost': 22.00,
            'fare_breakdown': {'base': 5.0, 'distance': 15.0, 'time': 2.0}
        },
        {
            'id': 'CAR004',
            'vehicle_type': 'economy',
            'eta_pickup': 7.0,  # 7 minutes away
            'trip_cost': 14.00,
            'fare_breakdown': {'base': 2.5, 'distance': 9.0, 'time': 2.5}
        }
    ]
    
    print("Available Vehicles:")
    for v in vehicles:
        print(f"  {v['id']}: {v['vehicle_type']}, ETA {v['eta_pickup']}min, ${v['trip_cost']}")
    print()
    
    # Test different user modes
    for mode in ['fastest', 'cheapest', 'balanced']:
        print(f"Ranking for '{mode}' mode:")
        ranked = rank_vehicles(vehicles, user_mode=mode, top_k=3)
        
        for i, v in enumerate(ranked, 1):
            print(f"  {i}. {v['id']} ({v['vehicle_type']})")
            print(f"     ETA: {v['eta_pickup']}min, Cost: ${v['trip_cost']}, Comfort: {v['comfort_score']}")
            print(f"     Score: {v['final_score']:.3f}")
        print()
