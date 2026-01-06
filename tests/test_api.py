"""
Integration Tests for API

Tests API endpoints, request validation, and response schemas.
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

# Create test client
client = TestClient(app)


class TestAPIEndpoints:
    """Test suite for API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "models_loaded" in data


class TestVehicleUpdateEndpoint:
    """Test suite for /vehicles/update endpoint"""
    
    def test_vehicle_update_valid_request(self):
        """Test valid vehicle update request"""
        request_data = {
            "vehicle_id": "TEST001",
            "location": {"lat": 40.7500, "lon": -74.0000},
            "status": "available",
            "vehicle_type": "economy"
        }
        
        response = client.post("/vehicles/update", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["vehicle_id"] == "TEST001"
        assert data["updated"] == True
        assert "region_id" in data
        assert "current_surge" in data
    
    def test_vehicle_update_invalid_status(self):
        """Test invalid vehicle status"""
        request_data = {
            "vehicle_id": "TEST001",
            "location": {"lat": 40.7500, "lon": -74.0000},
            "status": "invalid_status",  # Invalid
            "vehicle_type": "economy"
        }
        
        response = client.post("/vehicles/update", json=request_data)
        
        # Should return 422 validation error
        assert response.status_code == 422
    
    def test_vehicle_update_invalid_vehicle_type(self):
        """Test invalid vehicle type"""
        request_data = {
            "vehicle_id": "TEST001",
            "location": {"lat": 40.7500, "lon": -74.0000},
            "status": "available",
            "vehicle_type": "invalid_type"  # Invalid
        }
        
        response = client.post("/vehicles/update", json=request_data)
        
        assert response.status_code == 422
    
    def test_vehicle_update_invalid_coordinates(self):
        """Test invalid coordinates"""
        request_data = {
            "vehicle_id": "TEST001",
            "location": {"lat": 999.0, "lon": -74.0000},  # Invalid lat
            "status": "available",
            "vehicle_type": "economy"
        }
        
        response = client.post("/vehicles/update", json=request_data)
        
        assert response.status_code == 422


class TestRideQuoteEndpoint:
    """Test suite for /ride/quote endpoint"""
    
    def setup_method(self):
        """Setup: Register test vehicles before each test"""
        vehicles = [
            {
                "vehicle_id": "TEST001",
                "location": {"lat": 40.7500, "lon": -74.0000},
                "status": "available",
                "vehicle_type": "economy"
            },
            {
                "vehicle_id": "TEST002",
                "location": {"lat": 40.7520, "lon": -74.0020},
                "status": "available",
                "vehicle_type": "sedan"
            },
            {
                "vehicle_id": "TEST003",
                "location": {"lat": 40.7480, "lon": -73.9980},
                "status": "available",
                "vehicle_type": "suv"
            }
        ]
        
        for vehicle in vehicles:
            client.post("/vehicles/update", json=vehicle)
    
    def test_ride_quote_valid_request(self):
        """Test valid ride quote request"""
        request_data = {
            "pickup": {"lat": 40.7500, "lon": -74.0000},
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "balanced"
        }
        
        response = client.post("/ride/quote", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response schema
        assert "request_id" in data
        assert "distance" in data
        assert "estimated_duration" in data
        assert "surge_multiplier" in data
        assert "available_vehicles" in data
    
    def test_ride_quote_response_schema(self):
        """CRITICAL: Test response follows schema"""
        request_data = {
            "pickup": {"lat": 40.7500, "lon": -74.0000},
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "fastest"
        }
        
        response = client.post("/ride/quote", json=request_data)
        data = response.json()
        
        # Check all required fields
        required_fields = [
            "request_id", "pickup", "drop", "distance",
            "estimated_duration", "surge_multiplier",
            "surge_reason", "available_vehicles"
        ]
        
        for field in required_fields:
            assert field in data, f"Response missing required field: {field}"
        
        # Check vehicle schema
        if data["available_vehicles"]:
            vehicle = data["available_vehicles"][0]
            vehicle_fields = [
                "vehicle_id", "vehicle_type", "eta_pickup",
                "eta_trip", "fare_breakdown", "final_fare", "score"
            ]
            for field in vehicle_fields:
                assert field in vehicle, f"Vehicle missing field: {field}"
    
    def test_ride_quote_fastest_mode(self):
        """Test fastest mode returns vehicles"""
        request_data = {
            "pickup": {"lat": 40.7500, "lon": -74.0000},
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "fastest"
        }
        
        response = client.post("/ride/quote", json=request_data)
        data = response.json()
        
        assert len(data["available_vehicles"]) > 0, \
            "Should return available vehicles"
    
    def test_ride_quote_cheapest_mode(self):
        """Test cheapest mode returns vehicles"""
        request_data = {
            "pickup": {"lat": 40.7500, "lon": -74.0000},
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "cheapest"
        }
        
        response = client.post("/ride/quote", json=request_data)
        data = response.json()
        
        assert len(data["available_vehicles"]) > 0
    
    def test_ride_quote_invalid_user_mode(self):
        """Test invalid user mode"""
        request_data = {
            "pickup": {"lat": 40.7500, "lon": -74.0000},
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "invalid_mode"  # Invalid
        }
        
        response = client.post("/ride/quote", json=request_data)
        
        assert response.status_code == 422
    
    def test_ride_quote_invalid_coordinates(self):
        """Test invalid coordinates"""
        request_data = {
            "pickup": {"lat": 999.0, "lon": -74.0000},  # Invalid
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "balanced"
        }
        
        response = client.post("/ride/quote", json=request_data)
        
        assert response.status_code == 422
    
    def test_ride_quote_surge_multiplier_valid(self):
        """Test surge multiplier is within valid range"""
        request_data = {
            "pickup": {"lat": 40.7500, "lon": -74.0000},
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "balanced"
        }
        
        response = client.post("/ride/quote", json=request_data)
        data = response.json()
        
        surge = data["surge_multiplier"]
        assert 0.9 <= surge <= 1.5, \
            f"Surge {surge}× should be within valid range [0.9, 1.5]"
    
    def test_ride_quote_fare_positive(self):
        """Test that all fares are positive"""
        request_data = {
            "pickup": {"lat": 40.7500, "lon": -74.0000},
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "balanced"
        }
        
        response = client.post("/ride/quote", json=request_data)
        data = response.json()
        
        for vehicle in data["available_vehicles"]:
            assert vehicle["final_fare"] > 0, "Fare should be positive"
    
    def test_ride_quote_scores_in_range(self):
        """Test that vehicle scores are in 0-1 range"""
        request_data = {
            "pickup": {"lat": 40.7500, "lon": -74.0000},
            "drop": {"lat": 40.7600, "lon": -73.9900},
            "user_mode": "balanced"
        }
        
        response = client.post("/ride/quote", json=request_data)
        data = response.json()
        
        for vehicle in data["available_vehicles"]:
            score = vehicle["score"]
            assert 0.0 <= score <= 1.0, \
                f"Score {score} should be in range [0, 1]"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
