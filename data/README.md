# Synthetic Ride-Hailing Dataset

## Overview

This dataset contains **10,000 synthetic ride records** for a generic metro city, designed to simulate realistic ride-hailing patterns for machine learning model training.

## Dataset Characteristics

### Geographic Scope
- **City Grid:** 10km × 10km generic metro area
- **Center Coordinates:** (40.7128, -74.0060) - generic, not specific to any real city
- **Hotspots:** 4 high-demand zones simulating:
  - Business district
  - Airport area
  - Shopping district
  - Residential hub

### Temporal Coverage
- **Date Range:** 30 days (January 2024)
- **Time Distribution:** 24-hour coverage with realistic demand patterns
- **Rush Hours:** 
  - Morning: 7-10 AM (1.8× traffic multiplier)
  - Evening: 5-8 PM (2.0× traffic multiplier)
  - Late night: 11 PM - 5 AM (0.7× traffic multiplier)

### Vehicle Fleet
Three vehicle categories with different characteristics:

| Type | Fleet % | Avg Speed | Base Fare | Per-km Rate | Per-min Rate |
|------|---------|-----------|-----------|-------------|--------------|
| Economy | 50% | 30 km/h | $2.50 | $1.20 | $0.30 |
| Sedan | 35% | 35 km/h | $3.50 | $1.80 | $0.40 |
| SUV | 15% | 32 km/h | $5.00 | $2.50 | $0.50 |

## Schema

### Mandatory Fields

| Field | Type | Description | Range/Format |
|-------|------|-------------|--------------|
| `ride_id` | string | Unique ride identifier | R000001 - R010000 |
| `timestamp` | datetime | Ride request time | YYYY-MM-DD HH:MM:SS |
| `origin_lat` | float | Pickup latitude | 40.668 - 40.758 |
| `origin_lon` | float | Pickup longitude | -74.051 - -73.961 |
| `dest_lat` | float | Dropoff latitude | 40.668 - 40.758 |
| `dest_lon` | float | Dropoff longitude | -74.051 - -73.961 |
| `vehicle_type` | string | Vehicle category | economy, sedan, suv |
| `trip_distance` | float | Trip distance in km | 0.5 - 14.0 |
| `trip_duration` | float | Trip duration in minutes | 1.0 - 60.0 |
| `fare` | float | Total fare in USD | 2.0 - 150.0 |

### Derived Fields (for analysis)

| Field | Type | Description |
|-------|------|-------------|
| `hour` | int | Hour of day (0-23) |
| `day_of_week` | int | Day of week (0=Monday, 6=Sunday) |
| `is_rush_hour` | int | 1 if rush hour, 0 otherwise |

## Realism Features

### ✅ What Makes This Dataset Realistic

1. **Geographic Hotspots**
   - 40% of rides originate/end at high-demand zones
   - Simulates real-world clustering around business districts, airports, etc.

2. **Rush Hour Patterns**
   - Morning rush (7-10 AM): 1.8× slower traffic
   - Evening rush (5-8 PM): 2.0× slower traffic
   - Late night (11 PM - 5 AM): 0.7× faster traffic
   - Surge pricing: 1.3× (morning), 1.5× (evening)

3. **Vehicle Type Differences**
   - Different average speeds (economy slower than sedan)
   - Realistic fleet distribution (50% economy, 35% sedan, 15% SUV)
   - Differentiated pricing structures

4. **Distance-Duration Relationship**
   - Duration calculated from distance and vehicle speed
   - Traffic multipliers applied based on time of day
   - Controlled noise (±10%) for natural variation

5. **Fare Calculation**
   - Base fare + distance-based + time-based components
   - Surge multipliers during high-demand periods
   - Small random variation (±5%) for realism

6. **Minimum Distance Constraint**
   - All trips ≥ 0.5 km (no ultra-short rides)
   - Prevents unrealistic data points

## Limitations & Simplifications

### ⚠️ What's Simplified

1. **Routing**
   - Uses Haversine (straight-line) distance, not road network
   - Real-world: Roads add ~20-40% to straight-line distance
   - Impact: Distances may be 20-30% shorter than reality

2. **Traffic Modeling**
   - Simple time-of-day multipliers, not real-time traffic
   - No accident/event-based congestion
   - No spatial variation in traffic (entire city uses same multiplier)

3. **Demand Patterns**
   - Uniform across all days (no weekday/weekend difference)
   - No special events, holidays, or weather impacts
   - No seasonal variations

4. **Geographic Simplification**
   - Rectangular grid, not real city boundaries
   - No water bodies, parks, or restricted zones
   - Uniform hotspot distribution

5. **Pricing**
   - No dynamic surge based on real-time supply-demand
   - No promotional discounts or rider-specific pricing
   - No tolls, airport fees, or other surcharges

6. **Vehicle Behavior**
   - No vehicle repositioning or deadheading
   - No driver acceptance/rejection patterns
   - Assumes infinite vehicle supply

## Usage

### Generate Dataset
```bash
cd scripts
python generate_synthetic_data.py
```

Output: `data/raw/rides.csv`

### Run EDA
```bash
cd scripts
python eda_analysis.py
```

Outputs:
- `data/processed/duration_distribution.png`
- `data/processed/time_correlation.png`
- `data/processed/vehicle_comparison.png`
- `data/processed/correlation_matrix.png`

## Expected Statistics

### Trip Metrics
- **Distance:** Mean ~5-6 km, Range 0.5-14 km
- **Duration:** Mean ~15-20 min, Range 1-60 min
- **Fare:** Mean ~$12-15, Range $2-150

### Distributions
- **Rush hour rides:** ~30-35% of total
- **Vehicle types:** Economy 50%, Sedan 35%, SUV 15%
- **Peak hours:** 8-9 AM, 6-7 PM

### Correlations
- Distance ↔ Duration: ~0.85-0.90 (strong positive)
- Distance ↔ Fare: ~0.90-0.95 (strong positive)
- Rush hour ↔ Duration: ~0.15-0.25 (moderate positive)

## Data Quality

- **No missing values:** All fields populated
- **No duplicates:** Unique ride IDs
- **Realistic ranges:** All values within expected bounds
- **Consistent relationships:** Duration/fare align with distance
- **Reproducible:** Fixed random seed (42)

## Future Enhancements

To make this dataset more realistic:
1. Use real road network (OSM) for routing
2. Add weekday/weekend patterns
3. Incorporate weather data
4. Add spatial traffic variation
5. Simulate driver supply dynamics
6. Include cancellation/rejection patterns

## Citation

If using this dataset, please note:
- **Purpose:** Educational/MVP development
- **Realism:** Synthetic with simplified assumptions
- **Not suitable for:** Production deployment without validation
- **Best for:** Algorithm prototyping, model training, concept validation

---

**Generated:** 2024-01-03  
**Version:** 1.0  
**License:** MIT
