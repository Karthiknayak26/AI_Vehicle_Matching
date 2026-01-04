"""
Encoding Module for Categorical Features

Provides encoding utilities for vehicle types and other categorical variables.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


def encode_vehicle_type(df, method='onehot', vehicle_col='vehicle_type'):
    """
    Encode vehicle type as numerical features.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with vehicle_type column
    method : str, default='onehot'
        Encoding method: 'onehot', 'label', or 'ordinal'
    vehicle_col : str, default='vehicle_type'
        Name of the vehicle type column
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with encoded vehicle features
    
    Examples
    --------
    >>> df = pd.DataFrame({'vehicle_type': ['economy', 'sedan', 'suv']})
    >>> encode_vehicle_type(df, method='onehot')
       vehicle_economy  vehicle_sedan  vehicle_suv
    0                1              0            0
    1                0              1            0
    2                0              0            1
    """
    if method == 'onehot':
        # One-hot encoding (creates binary columns)
        dummies = pd.get_dummies(df[vehicle_col], prefix='vehicle')
        df = pd.concat([df, dummies], axis=1)
        
    elif method == 'label':
        # Label encoding (0, 1, 2)
        le = LabelEncoder()
        df['vehicle_encoded'] = le.fit_transform(df[vehicle_col])
        
    elif method == 'ordinal':
        # Ordinal encoding based on price hierarchy
        vehicle_order = {'economy': 0, 'sedan': 1, 'suv': 2}
        df['vehicle_encoded'] = df[vehicle_col].map(vehicle_order)
    
    return df


def get_vehicle_features(vehicle_type):
    """
    Get vehicle-specific features for modeling.
    
    Parameters
    ----------
    vehicle_type : str or array-like
        Vehicle type(s): 'economy', 'sedan', or 'suv'
    
    Returns
    -------
    dict
        Dictionary with vehicle features:
        - base_speed: Average speed in km/h
        - base_fare: Base fare in dollars
        - per_km_rate: Rate per kilometer
        - per_min_rate: Rate per minute
    
    Examples
    --------
    >>> get_vehicle_features('economy')
    {'base_speed': 30, 'base_fare': 2.5, ...}
    """
    vehicle_specs = {
        'economy': {
            'base_speed': 30,
            'base_fare': 2.50,
            'per_km_rate': 1.20,
            'per_min_rate': 0.30,
            'comfort_score': 1
        },
        'sedan': {
            'base_speed': 35,
            'base_fare': 3.50,
            'per_km_rate': 1.80,
            'per_min_rate': 0.40,
            'comfort_score': 2
        },
        'suv': {
            'base_speed': 32,
            'base_fare': 5.00,
            'per_km_rate': 2.50,
            'per_min_rate': 0.50,
            'comfort_score': 3
        }
    }
    
    if isinstance(vehicle_type, str):
        return vehicle_specs.get(vehicle_type, vehicle_specs['economy'])
    else:
        # Vectorized version
        return [vehicle_specs.get(v, vehicle_specs['economy']) for v in vehicle_type]


def add_vehicle_features(df, vehicle_col='vehicle_type'):
    """
    Add vehicle-specific features to DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with vehicle_type column
    vehicle_col : str, default='vehicle_type'
        Name of the vehicle type column
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with added vehicle features
    
    Examples
    --------
    >>> df = pd.DataFrame({'vehicle_type': ['economy', 'sedan']})
    >>> add_vehicle_features(df)
      vehicle_type  base_speed  base_fare  comfort_score
    0      economy          30       2.50              1
    1        sedan          35       3.50              2
    """
    features = df[vehicle_col].apply(get_vehicle_features)
    
    df['base_speed'] = features.apply(lambda x: x['base_speed'])
    df['base_fare'] = features.apply(lambda x: x['base_fare'])
    df['per_km_rate'] = features.apply(lambda x: x['per_km_rate'])
    df['per_min_rate'] = features.apply(lambda x: x['per_min_rate'])
    df['comfort_score'] = features.apply(lambda x: x['comfort_score'])
    
    return df
