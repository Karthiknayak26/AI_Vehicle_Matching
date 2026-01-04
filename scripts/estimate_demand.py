"""
Demand Estimation Module

Estimates ride demand by region and time for surge pricing decisions.
"""

import pandas as pd
import numpy as np
import pickle
import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.features.temporal import extract_temporal_features


def create_spatial_grid(df, grid_size=5):
    """
    Divide city into spatial grid regions.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with origin_lat, origin_lon columns
    grid_size : int
        Number of grid cells per dimension (creates grid_size x grid_size grid)
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with added region_id column
    """
    # Get lat/lon bounds
    lat_min, lat_max = df['origin_lat'].min(), df['origin_lat'].max()
    lon_min, lon_max = df['origin_lon'].min(), df['origin_lon'].max()
    
    # Create bins
    lat_bins = np.linspace(lat_min, lat_max, grid_size + 1)
    lon_bins = np.linspace(lon_min, lon_max, grid_size + 1)
    
    # Assign grid cells
    df['lat_grid'] = pd.cut(df['origin_lat'], bins=lat_bins, labels=False, include_lowest=True)
    df['lon_grid'] = pd.cut(df['origin_lon'], bins=lon_bins, labels=False, include_lowest=True)
    
    # Create region ID
    df['region_id'] = df['lat_grid'].astype(str) + '_' + df['lon_grid'].astype(str)
    
    return df


def calculate_demand_by_region_hour(df):
    """
    Calculate demand statistics by region and hour.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with region_id and hour columns
    
    Returns
    -------
    pandas.DataFrame
        Demand statistics by region and hour
    """
    demand = df.groupby(['region_id', 'hour']).agg({
        'ride_id': 'count',
        'fare': 'mean',
        'trip_duration': 'mean'
    }).reset_index()
    
    demand.columns = ['region_id', 'hour', 'demand_count', 'avg_fare', 'avg_duration']
    
    # Calculate demand score (normalized 0-1)
    demand['demand_score'] = (
        (demand['demand_count'] - demand['demand_count'].min()) /
        (demand['demand_count'].max() - demand['demand_count'].min())
    )
    
    # Categorize demand level
    demand['demand_level'] = pd.cut(
        demand['demand_score'],
        bins=[0, 0.3, 0.7, 1.0],
        labels=['low', 'medium', 'high'],
        include_lowest=True
    )
    
    return demand


def calculate_surge_multiplier(demand_score):
    """
    Calculate surge pricing multiplier based on demand score.
    
    Parameters
    ----------
    demand_score : float or array-like
        Demand score between 0 and 1
    
    Returns
    -------
    float or array-like
        Surge multiplier (1.0 = normal, >1.0 = surge)
    """
    demand_score = np.asarray(demand_score)
    
    # Base multiplier
    multiplier = np.ones_like(demand_score, dtype=float)
    
    # Low demand (< 0.3): Discount
    multiplier[demand_score < 0.3] = 0.9
    
    # Medium demand (0.3 - 0.7): Normal
    multiplier[(demand_score >= 0.3) & (demand_score < 0.7)] = 1.0
    
    # High demand (0.7 - 0.85): Moderate surge
    multiplier[(demand_score >= 0.7) & (demand_score < 0.85)] = 1.3
    
    # Very high demand (>= 0.85): High surge
    multiplier[demand_score >= 0.85] = 1.5
    
    return multiplier


def analyze_demand_patterns(demand_df):
    """
    Analyze and summarize demand patterns.
    
    Parameters
    ----------
    demand_df : pandas.DataFrame
        Demand statistics DataFrame
    
    Returns
    -------
    dict
        Summary statistics and insights
    """
    # Peak hours
    hourly_demand = demand_df.groupby('hour')['demand_count'].sum().sort_values(ascending=False)
    peak_hours = hourly_demand.head(3).index.tolist()
    
    # High demand regions
    regional_demand = demand_df.groupby('region_id')['demand_count'].sum().sort_values(ascending=False)
    high_demand_regions = regional_demand.head(5).index.tolist()
    
    # Overall statistics
    total_demand = demand_df['demand_count'].sum()
    avg_demand = demand_df['demand_count'].mean()
    
    # Surge pricing opportunities
    high_surge_slots = len(demand_df[demand_df['demand_score'] >= 0.7])
    total_slots = len(demand_df)
    surge_percentage = (high_surge_slots / total_slots) * 100
    
    summary = {
        'total_demand': int(total_demand),
        'avg_demand_per_slot': round(float(avg_demand), 2),
        'peak_hours': peak_hours,
        'high_demand_regions': high_demand_regions,
        'surge_opportunities': {
            'high_demand_slots': high_surge_slots,
            'total_slots': total_slots,
            'percentage': round(surge_percentage, 2)
        }
    }
    
    return summary


def main():
    """
    Main demand estimation pipeline.
    """
    print("\n" + "="*60)
    print("DEMAND ESTIMATION PIPELINE")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv('data/raw/rides.csv')
    print(f"✓ Loaded {len(df):,} rides")
    
    # Extract temporal features
    print("Extracting temporal features...")
    df = extract_temporal_features(df)
    
    # Create spatial grid
    print("Creating spatial grid (5x5 = 25 regions)...")
    df = create_spatial_grid(df, grid_size=5)
    print(f"✓ Created {df['region_id'].nunique()} regions")
    
    # Calculate demand by region and hour
    print("\nCalculating demand by region and hour...")
    demand_df = calculate_demand_by_region_hour(df)
    print(f"✓ Generated {len(demand_df):,} demand slots")
    
    # Add surge multipliers
    print("Calculating surge multipliers...")
    demand_df['surge_multiplier'] = calculate_surge_multiplier(demand_df['demand_score'])
    
    # Analyze patterns
    print("\nAnalyzing demand patterns...")
    summary = analyze_demand_patterns(demand_df)
    
    # Print summary
    print("\n" + "="*60)
    print("DEMAND ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total demand: {summary['total_demand']:,} rides")
    print(f"Average demand per slot: {summary['avg_demand_per_slot']:.2f} rides")
    print(f"\nPeak hours: {', '.join(map(str, summary['peak_hours']))}")
    print(f"High demand regions: {', '.join(summary['high_demand_regions'][:3])}")
    print(f"\nSurge pricing opportunities:")
    print(f"  High demand slots: {summary['surge_opportunities']['high_demand_slots']}")
    print(f"  Percentage: {summary['surge_opportunities']['percentage']:.1f}%")
    print("="*60)
    
    # Save results
    print("\nSaving results...")
    os.makedirs('reports', exist_ok=True)
    os.makedirs('models/saved', exist_ok=True)
    
    # Save demand data
    demand_df.to_csv('reports/demand_by_region_hour.csv', index=False)
    print("✓ Saved: reports/demand_by_region_hour.csv")
    
    # Save summary
    with open('reports/demand_analysis.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("✓ Saved: reports/demand_analysis.json")
    
    # Save demand model (simple lookup table)
    demand_model = {
        'demand_data': demand_df.to_dict('records'),
        'grid_size': 5,
        'summary': summary
    }
    
    with open('models/saved/demand_model.pkl', 'wb') as f:
        pickle.dump(demand_model, f)
    print("✓ Saved: models/saved/demand_model.pkl")
    
    print("\n" + "="*60)
    print("DEMAND ESTIMATION COMPLETE!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
