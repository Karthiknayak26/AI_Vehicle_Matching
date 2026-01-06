"""
Unit Tests for Distance Calculation

Tests the Haversine distance formula for correctness.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.features.distance import haversine_distance


class TestDistanceCalculation:
    """Test suite for distance calculation"""
    
    def test_zero_distance(self):
        """Test distance between same point is zero"""
        lat, lon = 40.7128, -74.0060
        distance = haversine_distance(lat, lon, lat, lon)
        assert distance == 0.0, "Distance between same point should be 0"
    
    def test_known_distance_nyc_to_boston(self):
        """Test known distance: NYC to Boston ≈ 306 km"""
        # NYC coordinates
        nyc_lat, nyc_lon = 40.7128, -74.0060
        # Boston coordinates
        boston_lat, boston_lon = 42.3601, -71.0589
        
        distance = haversine_distance(nyc_lat, nyc_lon, boston_lat, boston_lon)
        
        # Allow 5% tolerance for spherical earth approximation
        expected = 306.0
        tolerance = expected * 0.05
        assert abs(distance - expected) < tolerance, \
            f"NYC to Boston distance should be ~{expected} km, got {distance:.2f} km"
    
    def test_known_distance_short(self):
        """Test short distance: ~1 km"""
        # Two points roughly 1 km apart
        lat1, lon1 = 40.7128, -74.0060
        lat2, lon2 = 40.7218, -74.0060  # ~1 km north
        
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        
        # Should be close to 1 km
        assert 0.9 < distance < 1.1, \
            f"Distance should be ~1 km, got {distance:.2f} km"
    
    def test_symmetry(self):
        """Test that distance(A,B) == distance(B,A)"""
        lat1, lon1 = 40.7128, -74.0060
        lat2, lon2 = 40.7500, -73.9800
        
        dist_ab = haversine_distance(lat1, lon1, lat2, lon2)
        dist_ba = haversine_distance(lat2, lon2, lat1, lon1)
        
        assert abs(dist_ab - dist_ba) < 0.001, \
            "Distance should be symmetric"
    
    def test_positive_distance(self):
        """Test that distance is always positive"""
        lat1, lon1 = 40.7128, -74.0060
        lat2, lon2 = 40.7500, -73.9800
        
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        
        assert distance >= 0, "Distance should always be non-negative"
    
    def test_equator_distance(self):
        """Test distance along equator"""
        # 1 degree longitude at equator ≈ 111 km
        lat1, lon1 = 0.0, 0.0
        lat2, lon2 = 0.0, 1.0
        
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        
        expected = 111.0
        tolerance = expected * 0.05
        assert abs(distance - expected) < tolerance, \
            f"1 degree at equator should be ~{expected} km, got {distance:.2f} km"
    
    def test_large_distance(self):
        """Test large distance: opposite sides of Earth"""
        # Antipodal points (opposite sides)
        lat1, lon1 = 0.0, 0.0
        lat2, lon2 = 0.0, 180.0
        
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        
        # Half Earth's circumference ≈ 20,000 km
        expected = 20000.0
        tolerance = expected * 0.1  # 10% tolerance
        assert abs(distance - expected) < tolerance, \
            f"Half Earth circumference should be ~{expected} km, got {distance:.2f} km"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
