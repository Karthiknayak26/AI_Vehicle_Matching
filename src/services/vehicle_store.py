
import random
from datetime import datetime
from typing import Dict, List, Optional
import math

class VehicleStore:
    """
    Singleton In-Memory Vehicle Store.
    
    Design Decisions:
    1. Singleton: Ensures all API requests access the SAME vehicle state (critical for serverless/local persistence).
    2. In-Memory (Dict): Fastest lookup (O(1)) for IDs. No external DB needed for demo.
    3. Lat/Lon Indexing: For production, we'd use a geospatial index (e.g., Uber H3, R-Tree). 
       For this demo, a simple list filter is acceptable (N < 1000).
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VehicleStore, cls).__new__(cls)
            cls._instance._vehicles: Dict[str, Dict] = {}
            cls._instance._initialized = False
        return cls._instance

    def initialize_fleet(self, center_lat: float, center_lon: float, count: int = 10):
        """
        Pre-populates the store with vehicles around a specific location.
        CRITICAL: Running this on startup prevents the "0 vehicles available" bug.
        """
        if self._initialized and self._vehicles:
            print(f"VehicleStore: Already initialized with {len(self._vehicles)} vehicles.")
            return

        print(f"VehicleStore: Initializing fleet of {count} vehicles around ({center_lat}, {center_lon})...")
        
        vehicle_types = ['economy', 'sedan', 'suv']  # Matches config.py
        
        for i in range(count):
            # Random distribution within ~3km (approx 0.03 degrees)
            lat_offset = random.uniform(-0.03, 0.03)
            lon_offset = random.uniform(-0.03, 0.03)
            
            v_type = random.choice(vehicle_types)
            v_id = f"v_{v_type}_{i}_{random.randint(1000,9999)}"
            
            self._vehicles[v_id] = {
                'id': v_id,
                'vehicle_type': v_type,
                'location': {
                    'lat': center_lat + lat_offset,
                    'lon': center_lon + lon_offset
                },
                'status': 'available',
                'last_updated': datetime.now().isoformat(),
                # Demo attributes
                'rating': round(random.uniform(3.5, 5.0), 1),
                'trips_completed': random.randint(10, 500)
            }
            
        self._initialized = True
        print(f"VehicleStore: Initialization complete. {len(self._vehicles)} vehicles ready.")

    def get_all(self) -> List[Dict]:
        return list(self._vehicles.values())

    def get_vehicle(self, vehicle_id: str) -> Optional[Dict]:
        return self._vehicles.get(vehicle_id)

    def update_vehicle(self, vehicle_id: str, lat: float, lon: float, status: str = None):
        if vehicle_id in self._vehicles:
            self._vehicles[vehicle_id]['location'] = {'lat': lat, 'lon': lon}
            self._vehicles[vehicle_id]['last_updated'] = datetime.now().isoformat()
            if status:
                self._vehicles[vehicle_id]['status'] = status
            return True
        return False

    def get_nearby(self, lat: float, lon: float, radius_km: float = 5.0) -> List[Dict]:
        """
        Filters vehicles by proximity using Haversine distance (approximate).
        Why this is okay for demo: Simple math is reliable.
        """
        nearby = []
        for v in self._vehicles.values():
            if v['status'] != 'available':
                continue
                
            v_lat = v['location']['lat']
            v_lon = v['location']['lon']
            
            # Quick bounding box check (optimization)
            if abs(v_lat - lat) > 0.1 or abs(v_lon - lon) > 0.1:
                continue
                
            dist = self._haversine(lat, lon, v_lat, v_lon)
            if dist <= radius_km:
                # Inject distance for frontend use if needed
                v_copy = v.copy()
                v_copy['distance_km'] = round(dist, 2)
                nearby.append(v_copy)
                
        return nearby

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

# Global instance
vehicle_store = VehicleStore()
