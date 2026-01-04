"""
Distance Calculation Module

Provides Haversine distance calculation for geographic coordinates.
"""

import numpy as np


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on Earth.
    
    Uses the Haversine formula to compute the shortest distance over the 
    earth's surface, giving an "as-the-crow-flies" distance between points.
    
    Parameters
    ----------
    lat1 : float or array-like
        Latitude of first point(s) in degrees
    lon1 : float or array-like
        Longitude of first point(s) in degrees
    lat2 : float or array-like
        Latitude of second point(s) in degrees
    lon2 : float or array-like
        Longitude of second point(s) in degrees
    
    Returns
    -------
    float or array-like
        Distance in kilometers
    
    Examples
    --------
    >>> haversine_distance(40.7128, -74.0060, 40.7500, -73.9800)
    4.52
    
    >>> # Vectorized calculation
    >>> lats1 = [40.7128, 40.7200]
    >>> lons1 = [-74.0060, -74.0100]
    >>> lats2 = [40.7500, 40.7600]
    >>> lons2 = [-73.9800, -73.9900]
    >>> haversine_distance(lats1, lons1, lats2, lons2)
    array([4.52, 4.85])
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Distance in kilometers
    distance = R * c
    
    return distance


def calculate_trip_distance(df):
    """
    Calculate trip distance for all rides in a DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with columns: origin_lat, origin_lon, dest_lat, dest_lon
    
    Returns
    -------
    pandas.Series
        Trip distances in kilometers
    
    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'origin_lat': [40.7128, 40.7200],
    ...     'origin_lon': [-74.0060, -74.0100],
    ...     'dest_lat': [40.7500, 40.7600],
    ...     'dest_lon': [-73.9800, -73.9900]
    ... })
    >>> calculate_trip_distance(df)
    0    4.52
    1    4.85
    dtype: float64
    """
    return haversine_distance(
        df['origin_lat'].values,
        df['origin_lon'].values,
        df['dest_lat'].values,
        df['dest_lon'].values
    )
