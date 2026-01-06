"""
Configuration for AI Vehicle Matching System
"""

# ============================================================================
# PRICING CONFIGURATION
# ============================================================================

# Base fares by vehicle type (USD)
VEHICLE_BASE_FARES = {
    'economy': 2.50,
    'sedan': 3.50,
    'suv': 5.00
}

# Price per kilometer by vehicle type (USD/km)
PRICE_PER_KM = {
    'economy': 1.20,
    'sedan': 1.50,
    'suv': 2.00
}

# Price per minute by vehicle type (USD/min)
PRICE_PER_MIN = {
    'economy': 0.30,
    'sedan': 0.40,
    'suv': 0.50
}

# ============================================================================
# SURGE PRICING CONFIGURATION
# ============================================================================

# Maximum surge multiplier (cap)
SURGE_CAP = 1.5

# Default surge when no data available
DEFAULT_SURGE = 1.0

# Demand-supply ratio thresholds
SURGE_THRESHOLDS = {
    'discount': 0.5,      # ratio < 0.5 → discount
    'normal': 1.5,        # 0.5 ≤ ratio < 1.5 → normal
    'moderate': 3.0,      # 1.5 ≤ ratio < 3.0 → moderate surge
    'high': float('inf')  # ratio ≥ 3.0 → high surge
}

# Surge multipliers for each tier
SURGE_MULTIPLIERS = {
    'discount': 0.9,   # 10% discount
    'normal': 1.0,     # No surge
    'moderate': 1.3,   # 30% surge
    'high': 1.5        # 50% surge (capped)
}

# ============================================================================
# VEHICLE RANKING CONFIGURATION
# ============================================================================

# Comfort scores by vehicle type (1-3 scale)
COMFORT_SCORES = {
    'economy': 1,
    'sedan': 2,
    'suv': 3
}

# User preference mode weights
USER_MODE_WEIGHTS = {
    'fastest': {
        'eta': 0.7,      # 70% weight on ETA
        'cost': 0.2,     # 20% weight on cost
        'comfort': 0.1   # 10% weight on comfort
    },
    'cheapest': {
        'cost': 0.7,     # 70% weight on cost
        'eta': 0.2,      # 20% weight on ETA
        'comfort': 0.1   # 10% weight on comfort
    },
    'balanced': {
        'eta': 0.4,      # 40% weight on ETA
        'cost': 0.4,     # 40% weight on cost
        'comfort': 0.2   # 20% weight on comfort
    }
}

# ============================================================================
# API CONFIGURATION
# ============================================================================

# Number of top vehicles to return
TOP_K_VEHICLES = 3

# Maximum search radius for available vehicles (km)
MAX_SEARCH_RADIUS_KM = 5.0

# API response timeout (seconds)
API_TIMEOUT_SECONDS = 10.0

# ============================================================================
# SPATIAL CONFIGURATION
# ============================================================================

# City grid configuration (must match demand model)
CITY_MIN_LAT = 40.7000
CITY_MAX_LAT = 40.8000
CITY_MIN_LON = -74.0200
CITY_MAX_LON = -73.9200
GRID_SIZE = 5  # 5x5 grid = 25 regions

# ============================================================================
# MODEL PATHS
# ============================================================================

import os

# Get the project root directory (where config.py is located)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Model paths (absolute paths from project root)
ETA_MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'saved', 'eta_lgbm.pkl')
SCALER_PATH = os.path.join(PROJECT_ROOT, 'models', 'saved', 'feature_scaler.pkl')
DEMAND_MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'saved', 'demand_model.pkl')

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
