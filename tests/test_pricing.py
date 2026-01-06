"""
Unit Tests for Dynamic Pricing

Tests surge pricing logic, cap enforcement, and fallback handling.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pricing.dynamic_pricing import (
    get_surge_multiplier,
    calculate_demand_supply_ratio,
    calculate_fare,
    get_surge_with_fallback
)
from config import SURGE_CAP, SURGE_MULTIPLIERS


class TestSurgePricing:
    """Test suite for surge pricing logic"""
    
    def test_surge_cap_never_exceeded(self):
        """CRITICAL: Surge multiplier must never exceed cap"""
        # Test extreme demand scenarios
        extreme_ratios = [5.0, 10.0, 50.0, 100.0, 1000.0]
        
        for ratio in extreme_ratios:
            surge = get_surge_multiplier(ratio, surge_cap=SURGE_CAP)
            assert surge <= SURGE_CAP, \
                f"Surge {surge}× exceeds cap {SURGE_CAP}× for ratio {ratio}"
    
    def test_surge_tiers(self):
        """Test surge multiplier tiers"""
        test_cases = [
            (0.3, 0.9),   # Low demand → discount
            (1.0, 1.0),   # Normal demand → normal
            (2.0, 1.3),   # Moderate demand → moderate surge
            (5.0, 1.5),   # High demand → high surge (capped)
        ]
        
        for ratio, expected_surge in test_cases:
            surge = get_surge_multiplier(ratio)
            assert surge == expected_surge, \
                f"Ratio {ratio} should give {expected_surge}×, got {surge}×"
    
    def test_discount_tier(self):
        """Test discount tier (ratio < 0.5)"""
        surge = get_surge_multiplier(0.2)
        assert surge == SURGE_MULTIPLIERS['discount'], \
            f"Low demand should give discount {SURGE_MULTIPLIERS['discount']}×"
    
    def test_normal_tier(self):
        """Test normal tier (0.5 ≤ ratio < 1.5)"""
        surge = get_surge_multiplier(1.0)
        assert surge == SURGE_MULTIPLIERS['normal'], \
            f"Normal demand should give {SURGE_MULTIPLIERS['normal']}×"
    
    def test_moderate_surge_tier(self):
        """Test moderate surge tier (1.5 ≤ ratio < 3.0)"""
        surge = get_surge_multiplier(2.0)
        assert surge == SURGE_MULTIPLIERS['moderate'], \
            f"Moderate demand should give {SURGE_MULTIPLIERS['moderate']}×"
    
    def test_high_surge_tier(self):
        """Test high surge tier (ratio ≥ 3.0)"""
        surge = get_surge_multiplier(5.0)
        assert surge == SURGE_MULTIPLIERS['high'], \
            f"High demand should give {SURGE_MULTIPLIERS['high']}×"
    
    def test_custom_surge_cap(self):
        """Test custom surge cap"""
        custom_cap = 2.0
        surge = get_surge_multiplier(100.0, surge_cap=custom_cap)
        assert surge <= custom_cap, \
            f"Surge should respect custom cap {custom_cap}×"
    
    def test_demand_supply_ratio_calculation(self):
        """Test demand-supply ratio calculation"""
        # Mock demand data (simplified)
        demand_data = {
            ('2_3', 8): {'demand_score': 0.8}  # High demand region
        }
        
        ratio = calculate_demand_supply_ratio('2_3', 8, 5, demand_data)
        
        # Demand score 0.8 → ~40 rides, 5 cars → ratio = 8.0
        assert ratio > 0, "Ratio should be positive"
        assert ratio > 1.5, "High demand should give ratio > 1.5"
    
    def test_zero_vehicles_handling(self):
        """Test handling of zero available vehicles"""
        # Should not crash, should use minimum 1 vehicle
        ratio = calculate_demand_supply_ratio('2_3', 8, 0, None)
        assert ratio >= 0, "Should handle zero vehicles gracefully"


class TestFareCalculation:
    """Test suite for fare calculation"""
    
    def test_fare_components(self):
        """Test fare breakdown components"""
        fare = calculate_fare(
            distance=5.0,
            duration=15.0,
            vehicle_type='economy',
            surge_multiplier=1.0
        )
        
        assert 'base_fare' in fare
        assert 'distance_cost' in fare
        assert 'time_cost' in fare
        assert 'subtotal' in fare
        assert 'surge_multiplier' in fare
        assert 'final_fare' in fare
    
    def test_fare_with_surge(self):
        """Test fare calculation with surge"""
        fare_normal = calculate_fare(5.0, 15.0, 'economy', 1.0)
        fare_surge = calculate_fare(5.0, 15.0, 'economy', 1.5)
        
        # Surge fare should be 1.5× normal fare
        expected_surge_fare = fare_normal['final_fare'] * 1.5
        assert abs(fare_surge['final_fare'] - expected_surge_fare) < 0.01, \
            "Surge fare should be multiplied correctly"
    
    def test_fare_with_discount(self):
        """Test fare calculation with discount"""
        fare_normal = calculate_fare(5.0, 15.0, 'economy', 1.0)
        fare_discount = calculate_fare(5.0, 15.0, 'economy', 0.9)
        
        # Discount fare should be 0.9× normal fare
        expected_discount_fare = fare_normal['final_fare'] * 0.9
        assert abs(fare_discount['final_fare'] - expected_discount_fare) < 0.01, \
            "Discount fare should be multiplied correctly"
    
    def test_fare_positive(self):
        """Test that fare is always positive"""
        fare = calculate_fare(5.0, 15.0, 'economy', 1.0)
        assert fare['final_fare'] > 0, "Fare should always be positive"
    
    def test_invalid_vehicle_type(self):
        """Test handling of invalid vehicle type"""
        with pytest.raises(ValueError):
            calculate_fare(5.0, 15.0, 'invalid_type', 1.0)


class TestFallbackLogic:
    """Test suite for fallback logic"""
    
    def test_fallback_with_no_data(self):
        """Test fallback when no demand data available"""
        surge, reason = get_surge_with_fallback('0_0', 8, 5, None, default_surge=1.0)
        
        # Should use default or calculated value
        assert surge > 0, "Should return valid surge"
        assert isinstance(reason, str), "Should return reason string"
    
    def test_fallback_returns_valid_surge(self):
        """Test that fallback always returns valid surge"""
        surge, reason = get_surge_with_fallback('999_999', 99, 5, None)
        
        assert 0.9 <= surge <= SURGE_CAP, \
            f"Fallback surge {surge}× should be within valid range"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
