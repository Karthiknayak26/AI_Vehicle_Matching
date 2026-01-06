"""
Unit Tests for Vehicle Ranking

Tests ranking logic, score normalization, and user preference modes.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ranking.vehicle_ranker import (
    normalize_scores,
    calculate_vehicle_score,
    rank_vehicles
)
from config import USER_MODE_WEIGHTS


class TestScoreNormalization:
    """Test suite for score normalization"""
    
    def test_normalize_single_value(self):
        """Test normalization of single value"""
        scores = normalize_scores([5.0])
        assert scores == [1.0], "Single value should normalize to 1.0"
    
    def test_normalize_identical_values(self):
        """Test normalization of identical values"""
        scores = normalize_scores([5.0, 5.0, 5.0])
        assert all(s == 1.0 for s in scores), "Identical values should all be 1.0"
    
    def test_normalize_range(self):
        """Test normalization to 0-1 range"""
        scores = normalize_scores([1.0, 5.0, 10.0], lower_is_better=True)
        
        # Lower is better: 1.0 → 1.0, 10.0 → 0.0
        assert scores[0] == 1.0, "Lowest value should be 1.0"
        assert scores[2] == 0.0, "Highest value should be 0.0"
        assert 0.0 <= scores[1] <= 1.0, "Middle value should be in range"
    
    def test_normalize_lower_is_better(self):
        """Test lower_is_better flag"""
        values = [10, 20, 30]
        scores = normalize_scores(values, lower_is_better=True)
        
        # Lower is better: 10 should get highest score
        assert scores[0] > scores[1] > scores[2], \
            "Lower values should get higher scores"
    
    def test_normalize_higher_is_better(self):
        """Test higher_is_better flag"""
        values = [10, 20, 30]
        scores = normalize_scores(values, lower_is_better=False)
        
        # Higher is better: 30 should get highest score
        assert scores[2] > scores[1] > scores[0], \
            "Higher values should get higher scores"


class TestVehicleScoring:
    """Test suite for vehicle scoring"""
    
    def test_fastest_mode_prioritizes_eta(self):
        """Test that fastest mode prioritizes ETA"""
        vehicle = {
            'id': 'CAR001',
            'eta_pickup': 3.0,
            'trip_cost': 20.0,
            'vehicle_type': 'economy',
            'comfort_score': 1,
            'eta_score_normalized': 1.0,  # Best ETA
            'cost_score_normalized': 0.0,  # Worst cost
            'comfort_score_normalized': 0.0
        }
        
        score = calculate_vehicle_score(vehicle, user_mode='fastest')
        
        # Fastest mode: 70% ETA weight
        # Score should be dominated by ETA
        assert score >= 0.7, "Fastest mode should heavily weight ETA"
    
    def test_cheapest_mode_prioritizes_cost(self):
        """Test that cheapest mode prioritizes cost"""
        vehicle = {
            'id': 'CAR001',
            'eta_pickup': 10.0,
            'trip_cost': 10.0,
            'vehicle_type': 'economy',
            'comfort_score': 1,
            'eta_score_normalized': 0.0,  # Worst ETA
            'cost_score_normalized': 1.0,  # Best cost
            'comfort_score_normalized': 0.0
        }
        
        score = calculate_vehicle_score(vehicle, user_mode='cheapest')
        
        # Cheapest mode: 70% cost weight
        assert score >= 0.7, "Cheapest mode should heavily weight cost"
    
    def test_balanced_mode_weights(self):
        """Test balanced mode uses equal weights"""
        vehicle = {
            'id': 'CAR001',
            'eta_pickup': 5.0,
            'trip_cost': 15.0,
            'vehicle_type': 'sedan',
            'comfort_score': 2,
            'eta_score_normalized': 0.5,
            'cost_score_normalized': 0.5,
            'comfort_score_normalized': 0.5
        }
        
        score = calculate_vehicle_score(vehicle, user_mode='balanced')
        
        # Balanced: 40% ETA, 40% cost, 20% comfort
        # All at 0.5 → score should be 0.5
        assert abs(score - 0.5) < 0.01, "Balanced mode should weight evenly"
    
    def test_invalid_mode_defaults_to_balanced(self):
        """Test invalid mode defaults to balanced"""
        vehicle = {
            'id': 'CAR001',
            'eta_pickup': 5.0,
            'trip_cost': 15.0,
            'vehicle_type': 'economy',
            'comfort_score': 1,
            'eta_score_normalized': 0.5,
            'cost_score_normalized': 0.5,
            'comfort_score_normalized': 0.5
        }
        
        score = calculate_vehicle_score(vehicle, user_mode='invalid_mode')
        
        # Should default to balanced
        assert abs(score - 0.5) < 0.01


class TestVehicleRanking:
    """Test suite for vehicle ranking"""
    
    def test_ranking_respects_user_preference(self):
        """CRITICAL: Ranking must respect user preference mode"""
        vehicles = [
            {'id': 'CAR001', 'eta_pickup': 2.0, 'trip_cost': 20.0, 'vehicle_type': 'suv'},
            {'id': 'CAR002', 'eta_pickup': 5.0, 'trip_cost': 12.0, 'vehicle_type': 'economy'},
            {'id': 'CAR003', 'eta_pickup': 3.0, 'trip_cost': 15.0, 'vehicle_type': 'sedan'},
        ]
        
        # Fastest mode should rank CAR001 first (lowest ETA)
        fastest = rank_vehicles(vehicles.copy(), user_mode='fastest', top_k=3)
        assert fastest[0]['id'] == 'CAR001', \
            "Fastest mode should rank lowest ETA first"
        
        # Cheapest mode should rank CAR002 first (lowest cost)
        cheapest = rank_vehicles(vehicles.copy(), user_mode='cheapest', top_k=3)
        assert cheapest[0]['id'] == 'CAR002', \
            "Cheapest mode should rank lowest cost first"
    
    def test_ranking_returns_top_k(self):
        """Test that ranking returns exactly top_k vehicles"""
        vehicles = [
            {'id': f'CAR{i:03d}', 'eta_pickup': i, 'trip_cost': 10+i, 'vehicle_type': 'economy'}
            for i in range(10)
        ]
        
        for k in [1, 3, 5]:
            ranked = rank_vehicles(vehicles, top_k=k)
            assert len(ranked) == k, f"Should return exactly {k} vehicles"
    
    def test_ranking_adds_scores(self):
        """Test that ranking adds final_score to vehicles"""
        vehicles = [
            {'id': 'CAR001', 'eta_pickup': 3.0, 'trip_cost': 15.0, 'vehicle_type': 'economy'},
        ]
        
        ranked = rank_vehicles(vehicles)
        
        assert 'final_score' in ranked[0], "Should add final_score"
        assert 0.0 <= ranked[0]['final_score'] <= 1.0, "Score should be 0-1"
    
    def test_ranking_sorts_descending(self):
        """Test that ranking sorts by score (descending)"""
        vehicles = [
            {'id': 'CAR001', 'eta_pickup': 5.0, 'trip_cost': 20.0, 'vehicle_type': 'suv'},
            {'id': 'CAR002', 'eta_pickup': 2.0, 'trip_cost': 15.0, 'vehicle_type': 'sedan'},
            {'id': 'CAR003', 'eta_pickup': 3.0, 'trip_cost': 12.0, 'vehicle_type': 'economy'},
        ]
        
        ranked = rank_vehicles(vehicles, user_mode='fastest')
        
        # Scores should be in descending order
        for i in range(len(ranked) - 1):
            assert ranked[i]['final_score'] >= ranked[i+1]['final_score'], \
                "Vehicles should be sorted by score (descending)"
    
    def test_empty_vehicle_list(self):
        """Test handling of empty vehicle list"""
        ranked = rank_vehicles([])
        assert ranked == [], "Empty list should return empty list"
    
    def test_different_modes_different_rankings(self):
        """Test that different modes produce different rankings"""
        vehicles = [
            {'id': 'CAR001', 'eta_pickup': 2.0, 'trip_cost': 25.0, 'vehicle_type': 'suv'},
            {'id': 'CAR002', 'eta_pickup': 8.0, 'trip_cost': 10.0, 'vehicle_type': 'economy'},
        ]
        
        fastest = rank_vehicles(vehicles.copy(), user_mode='fastest')
        cheapest = rank_vehicles(vehicles.copy(), user_mode='cheapest')
        
        # Rankings should be different
        assert fastest[0]['id'] != cheapest[0]['id'], \
            "Different modes should produce different rankings"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
