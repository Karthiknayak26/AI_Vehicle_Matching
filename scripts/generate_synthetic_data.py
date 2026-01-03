"""
Synthetic Ride-Hailing Dataset Generator

Generates realistic ride data for a generic metro city with:
- Rush hour patterns
- Vehicle type variations
- Distance-based duration and fare
- Controlled randomness
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


class MetroCityGrid:
    """Defines a generic metro city grid (10km x 10km)"""
    
    def __init__(self):
        # City center coordinates (generic)
        self.center_lat = 40.7128
        self.center_lon = -74.0060
        
        # Grid boundaries (±5km from center)
        self.lat_range = (self.center_lat - 0.045, self.center_lat + 0.045)
        self.lon_range = (self.center_lon - 0.045, self.center_lon + 0.045)
        
        # High-demand zones (business districts, airports, etc.)
        self.hotspots = [
            (self.center_lat + 0.020, self.center_lon + 0.015),  # Business district
            (self.center_lat - 0.025, self.center_lon - 0.020),  # Airport area
            (self.center_lat + 0.010, self.center_lon - 0.030),  # Shopping area
            (self.center_lat - 0.015, self.center_lon + 0.025),  # Residential hub
        ]
    
    def random_location(self, hotspot_prob=0.3):
        """Generate random location, biased toward hotspots"""
        if random.random() < hotspot_prob:
            # Pick a hotspot and add small noise
            base_lat, base_lon = random.choice(self.hotspots)
            lat = base_lat + np.random.normal(0, 0.005)
            lon = base_lon + np.random.normal(0, 0.005)
        else:
            # Uniform random in grid
            lat = np.random.uniform(*self.lat_range)
            lon = np.random.uniform(*self.lon_range)
        
        return lat, lon


class VehicleType:
    """Vehicle categories with different characteristics"""
    
    TYPES = {
        'economy': {
            'avg_speed_kmh': 30,
            'base_fare': 2.5,
            'per_km_rate': 1.2,
            'per_min_rate': 0.3,
            'weight': 0.5  # 50% of fleet
        },
        'sedan': {
            'avg_speed_kmh': 35,
            'base_fare': 3.5,
            'per_km_rate': 1.8,
            'per_min_rate': 0.4,
            'weight': 0.35  # 35% of fleet
        },
        'suv': {
            'avg_speed_kmh': 32,
            'base_fare': 5.0,
            'per_km_rate': 2.5,
            'per_min_rate': 0.5,
            'weight': 0.15  # 15% of fleet
        }
    }
    
    @classmethod
    def random_type(cls):
        """Select random vehicle type based on fleet distribution"""
        types = list(cls.TYPES.keys())
        weights = [cls.TYPES[t]['weight'] for t in types]
        return random.choices(types, weights=weights)[0]


class RushHourSimulator:
    """Simulates traffic patterns throughout the day"""
    
    @staticmethod
    def get_traffic_multiplier(hour):
        """
        Returns traffic multiplier based on time of day
        1.0 = normal, >1.0 = slower (rush hour)
        """
        # Morning rush: 7-10 AM
        if 7 <= hour < 10:
            return 1.8
        # Evening rush: 5-8 PM
        elif 17 <= hour < 20:
            return 2.0
        # Late night: 11 PM - 5 AM (less traffic)
        elif hour >= 23 or hour < 5:
            return 0.7
        # Normal hours
        else:
            return 1.0
    
    @staticmethod
    def get_demand_multiplier(hour):
        """Returns demand multiplier for surge pricing"""
        if 7 <= hour < 10:
            return 1.3
        elif 17 <= hour < 20:
            return 1.5
        elif hour >= 23 or hour < 5:
            return 0.8
        else:
            return 1.0


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km using Haversine formula"""
    R = 6371  # Earth radius in km
    
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c


def calculate_trip_duration(distance_km, vehicle_type, hour):
    """Calculate trip duration with traffic and vehicle speed"""
    vehicle_info = VehicleType.TYPES[vehicle_type]
    base_speed = vehicle_info['avg_speed_kmh']
    
    # Apply traffic multiplier
    traffic_mult = RushHourSimulator.get_traffic_multiplier(hour)
    effective_speed = base_speed / traffic_mult
    
    # Duration in minutes
    duration = (distance_km / effective_speed) * 60
    
    # Add controlled noise (±10%)
    noise = np.random.normal(1.0, 0.1)
    duration *= noise
    
    return max(1.0, duration)  # Minimum 1 minute


def calculate_fare(distance_km, duration_min, vehicle_type, hour):
    """Calculate fare with surge pricing"""
    vehicle_info = VehicleType.TYPES[vehicle_type]
    
    # Base fare calculation
    base_fare = vehicle_info['base_fare']
    distance_fare = distance_km * vehicle_info['per_km_rate']
    time_fare = duration_min * vehicle_info['per_min_rate']
    
    base_total = base_fare + distance_fare + time_fare
    
    # Apply surge multiplier
    surge_mult = RushHourSimulator.get_demand_multiplier(hour)
    
    # Add small random variation (±5%)
    noise = np.random.normal(1.0, 0.05)
    
    final_fare = base_total * surge_mult * noise
    
    return round(final_fare, 2)


def generate_synthetic_rides(num_rides=10000, start_date='2024-01-01', num_days=30):
    """
    Generate synthetic ride dataset
    
    Args:
        num_rides: Number of rides to generate
        start_date: Start date for timestamps
        num_days: Number of days to spread rides across
    
    Returns:
        pandas DataFrame with ride data
    """
    print(f"Generating {num_rides} synthetic rides...")
    
    city = MetroCityGrid()
    rides = []
    
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    
    for i in range(num_rides):
        # Generate random timestamp
        day_offset = random.randint(0, num_days - 1)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        timestamp = start_dt + timedelta(
            days=day_offset,
            hours=hour,
            minutes=minute,
            seconds=second
        )
        
        # Generate origin and destination
        origin_lat, origin_lon = city.random_location(hotspot_prob=0.4)
        dest_lat, dest_lon = city.random_location(hotspot_prob=0.4)
        
        # Ensure minimum distance (0.5 km)
        while haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon) < 0.5:
            dest_lat, dest_lon = city.random_location(hotspot_prob=0.3)
        
        # Select vehicle type
        vehicle_type = VehicleType.random_type()
        
        # Calculate trip metrics
        trip_distance = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
        trip_duration = calculate_trip_duration(trip_distance, vehicle_type, hour)
        fare = calculate_fare(trip_distance, trip_duration, vehicle_type, hour)
        
        ride = {
            'ride_id': f'R{i+1:06d}',
            'timestamp': timestamp,
            'origin_lat': round(origin_lat, 6),
            'origin_lon': round(origin_lon, 6),
            'dest_lat': round(dest_lat, 6),
            'dest_lon': round(dest_lon, 6),
            'vehicle_type': vehicle_type,
            'trip_distance': round(trip_distance, 2),
            'trip_duration': round(trip_duration, 2),
            'fare': fare
        }
        
        rides.append(ride)
        
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1}/{num_rides} rides...")
    
    df = pd.DataFrame(rides)
    
    # Add derived features for analysis
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_rush_hour'] = df['hour'].apply(
        lambda h: 1 if (7 <= h < 10) or (17 <= h < 20) else 0
    )
    
    print(f"✓ Generated {len(df)} rides successfully!")
    return df


def main():
    """Generate dataset and save to CSV"""
    
    # Generate 10,000 rides over 30 days
    df = generate_synthetic_rides(num_rides=10000, start_date='2024-01-01', num_days=30)
    
    # Save to CSV
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_path = os.path.join(project_dir, 'data', 'raw', 'rides.csv')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"\n✓ Dataset saved to: {output_path}")

    
    # Print summary statistics
    print("\n" + "="*60)
    print("DATASET SUMMARY")
    print("="*60)
    print(f"Total rides: {len(df):,}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"\nVehicle distribution:")
    print(df['vehicle_type'].value_counts())
    print(f"\nRush hour rides: {df['is_rush_hour'].sum():,} ({df['is_rush_hour'].mean()*100:.1f}%)")
    print(f"\nDistance stats (km):")
    print(df['trip_distance'].describe())
    print(f"\nDuration stats (minutes):")
    print(df['trip_duration'].describe())
    print(f"\nFare stats ($):")
    print(df['fare'].describe())
    print("="*60)


if __name__ == '__main__':
    main()
