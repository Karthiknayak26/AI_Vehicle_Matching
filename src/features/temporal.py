"""
Temporal Feature Engineering Module

Extracts time-based features from timestamps for ML models.
"""

import pandas as pd
import numpy as np


def extract_temporal_features(df, timestamp_col='timestamp'):
    """
    Extract temporal features from timestamp column.
    
    Creates features useful for predicting time-dependent patterns like
    rush hour traffic, weekend behavior, etc.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with timestamp column
    timestamp_col : str, default='timestamp'
        Name of the timestamp column
    
    Returns
    -------
    pandas.DataFrame
        Original DataFrame with added temporal features:
        - hour: Hour of day (0-23)
        - day_of_week: Day of week (0=Monday, 6=Sunday)
        - is_rush_hour: Binary flag for rush hours
        - is_weekend: Binary flag for weekends
        - is_morning_rush: Binary flag for morning rush (7-10 AM)
        - is_evening_rush: Binary flag for evening rush (5-8 PM)
    
    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'timestamp': pd.to_datetime(['2024-01-15 08:30:00', '2024-01-15 14:30:00'])
    ... })
    >>> df = extract_temporal_features(df)
    >>> df[['hour', 'is_rush_hour']]
       hour  is_rush_hour
    0     8             1
    1    14             0
    """
    # Ensure timestamp is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    # Extract basic temporal features
    df['hour'] = df[timestamp_col].dt.hour
    df['day_of_week'] = df[timestamp_col].dt.dayofweek
    df['day_of_month'] = df[timestamp_col].dt.day
    df['month'] = df[timestamp_col].dt.month
    
    # Rush hour flags
    df['is_morning_rush'] = ((df['hour'] >= 7) & (df['hour'] < 10)).astype(int)
    df['is_evening_rush'] = ((df['hour'] >= 17) & (df['hour'] < 20)).astype(int)
    df['is_rush_hour'] = (df['is_morning_rush'] | df['is_evening_rush']).astype(int)
    
    # Weekend flag
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Late night flag (11 PM - 5 AM)
    df['is_late_night'] = ((df['hour'] >= 23) | (df['hour'] < 5)).astype(int)
    
    # Time of day categories
    df['time_of_day'] = pd.cut(
        df['hour'],
        bins=[0, 6, 12, 18, 24],
        labels=['night', 'morning', 'afternoon', 'evening'],
        include_lowest=True
    )
    
    return df


def get_rush_hour_multiplier(hour):
    """
    Get traffic multiplier for a given hour.
    
    Parameters
    ----------
    hour : int or array-like
        Hour of day (0-23)
    
    Returns
    -------
    float or array-like
        Traffic multiplier (1.0 = normal, >1.0 = slower)
    
    Examples
    --------
    >>> get_rush_hour_multiplier(8)
    1.8
    >>> get_rush_hour_multiplier(14)
    1.0
    """
    hour = np.asarray(hour)
    multiplier = np.ones_like(hour, dtype=float)
    
    # Morning rush: 7-10 AM
    multiplier[(hour >= 7) & (hour < 10)] = 1.8
    
    # Evening rush: 5-8 PM
    multiplier[(hour >= 17) & (hour < 20)] = 2.0
    
    # Late night: 11 PM - 5 AM (less traffic)
    multiplier[(hour >= 23) | (hour < 5)] = 0.7
    
    return multiplier


def get_demand_multiplier(hour):
    """
    Get demand multiplier for surge pricing.
    
    Parameters
    ----------
    hour : int or array-like
        Hour of day (0-23)
    
    Returns
    -------
    float or array-like
        Demand multiplier for pricing
    
    Examples
    --------
    >>> get_demand_multiplier(8)
    1.3
    >>> get_demand_multiplier(18)
    1.5
    """
    hour = np.asarray(hour)
    multiplier = np.ones_like(hour, dtype=float)
    
    # Morning rush
    multiplier[(hour >= 7) & (hour < 10)] = 1.3
    
    # Evening rush (higher demand)
    multiplier[(hour >= 17) & (hour < 20)] = 1.5
    
    # Late night (lower demand)
    multiplier[(hour >= 23) | (hour < 5)] = 0.8
    
    return multiplier
