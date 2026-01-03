"""
Exploratory Data Analysis for Ride-Hailing Dataset

Analyzes:
1. Trip duration distribution
2. Time-of-day correlation with duration
3. Vehicle category comparison
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_data(filepath=None):
    """Load the synthetic ride dataset"""
    if filepath is None:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        filepath = os.path.join(project_dir, 'data', 'raw', 'rides.csv')
    
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print(f"✓ Loaded {len(df):,} rides\n")
    return df


def basic_statistics(df):
    """Print basic dataset statistics"""
    print("="*70)
    print("BASIC STATISTICS")
    print("="*70)
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Number of days: {(df['timestamp'].max() - df['timestamp'].min()).days + 1}")
    
    print("\n--- Vehicle Type Distribution ---")
    vehicle_counts = df['vehicle_type'].value_counts()
    for vtype, count in vehicle_counts.items():
        pct = (count / len(df)) * 100
        print(f"{vtype:10s}: {count:5d} ({pct:5.1f}%)")
    
    print("\n--- Rush Hour Distribution ---")
    rush_counts = df['is_rush_hour'].value_counts()
    print(f"Rush hour:     {rush_counts.get(1, 0):5d} ({rush_counts.get(1, 0)/len(df)*100:5.1f}%)")
    print(f"Non-rush hour: {rush_counts.get(0, 0):5d} ({rush_counts.get(0, 0)/len(df)*100:5.1f}%)")
    
    print("\n--- Trip Metrics Summary ---")
    metrics = ['trip_distance', 'trip_duration', 'fare']
    for metric in metrics:
        print(f"\n{metric.replace('_', ' ').title()}:")
        print(f"  Mean:   {df[metric].mean():8.2f}")
        print(f"  Median: {df[metric].median():8.2f}")
        print(f"  Std:    {df[metric].std():8.2f}")
        print(f"  Min:    {df[metric].min():8.2f}")
        print(f"  Max:    {df[metric].max():8.2f}")
    
    print("\n" + "="*70 + "\n")


def analyze_trip_duration_distribution(df):
    """Analyze and visualize trip duration distribution"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(project_dir, 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*70)
    print("ANALYSIS 1: TRIP DURATION DISTRIBUTION")
    print("="*70)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Histogram
    axes[0].hist(df['trip_duration'], bins=50, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Trip Duration (minutes)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Trip Duration Distribution')
    axes[0].axvline(df['trip_duration'].mean(), color='red', linestyle='--', 
                    label=f'Mean: {df["trip_duration"].mean():.1f} min')
    axes[0].axvline(df['trip_duration'].median(), color='green', linestyle='--', 
                    label=f'Median: {df["trip_duration"].median():.1f} min')
    axes[0].legend()
    
    # Box plot
    axes[1].boxplot(df['trip_duration'], vert=True)
    axes[1].set_ylabel('Trip Duration (minutes)')
    axes[1].set_title('Trip Duration Box Plot')
    axes[1].grid(True, alpha=0.3)
    
    # By vehicle type
    vehicle_durations = [df[df['vehicle_type'] == vtype]['trip_duration'].values 
                         for vtype in ['economy', 'sedan', 'suv']]
    axes[2].boxplot(vehicle_durations, labels=['Economy', 'Sedan', 'SUV'])
    axes[2].set_ylabel('Trip Duration (minutes)')
    axes[2].set_title('Trip Duration by Vehicle Type')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, 'duration_distribution.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {save_path}")
    plt.close()
    
    # Statistical summary
    print("\nDuration Statistics:")
    print(f"  Mean: {df['trip_duration'].mean():.2f} minutes")
    print(f"  Median: {df['trip_duration'].median():.2f} minutes")
    print(f"  Std Dev: {df['trip_duration'].std():.2f} minutes")
    print(f"  Skewness: {df['trip_duration'].skew():.2f}")
    print(f"  Kurtosis: {df['trip_duration'].kurtosis():.2f}")
    
    print("\n" + "="*70 + "\n")


def analyze_time_of_day_correlation(df):
    """Analyze correlation between time of day and trip duration"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(project_dir, 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*70)
    print("ANALYSIS 2: TIME-OF-DAY CORRELATION WITH DURATION")
    print("="*70)
    
    # Group by hour
    hourly_stats = df.groupby('hour').agg({
        'trip_duration': ['mean', 'median', 'std', 'count'],
        'trip_distance': 'mean',
        'fare': 'mean'
    }).round(2)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # Average duration by hour
    hourly_mean = df.groupby('hour')['trip_duration'].mean()
    axes[0, 0].plot(hourly_mean.index, hourly_mean.values, marker='o', linewidth=2)
    axes[0, 0].axhspan(7, 10, alpha=0.2, color='red', label='Morning Rush')
    axes[0, 0].axhspan(17, 20, alpha=0.2, color='orange', label='Evening Rush')
    axes[0, 0].set_xlabel('Hour of Day')
    axes[0, 0].set_ylabel('Average Duration (minutes)')
    axes[0, 0].set_title('Average Trip Duration by Hour')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_xticks(range(0, 24, 2))
    
    # Ride count by hour
    hourly_count = df.groupby('hour').size()
    axes[0, 1].bar(hourly_count.index, hourly_count.values, alpha=0.7)
    axes[0, 1].set_xlabel('Hour of Day')
    axes[0, 1].set_ylabel('Number of Rides')
    axes[0, 1].set_title('Ride Demand by Hour')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    axes[0, 1].set_xticks(range(0, 24, 2))
    
    # Rush hour vs non-rush hour comparison
    rush_data = [
        df[df['is_rush_hour'] == 0]['trip_duration'].values,
        df[df['is_rush_hour'] == 1]['trip_duration'].values
    ]
    axes[1, 0].boxplot(rush_data, labels=['Non-Rush', 'Rush Hour'])
    axes[1, 0].set_ylabel('Trip Duration (minutes)')
    axes[1, 0].set_title('Duration: Rush vs Non-Rush Hours')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Heatmap: Hour vs Day of Week
    pivot_duration = df.pivot_table(
        values='trip_duration',
        index='hour',
        columns='day_of_week',
        aggfunc='mean'
    )
    sns.heatmap(pivot_duration, annot=False, cmap='YlOrRd', ax=axes[1, 1], cbar_kws={'label': 'Avg Duration (min)'})
    axes[1, 1].set_xlabel('Day of Week (0=Mon, 6=Sun)')
    axes[1, 1].set_ylabel('Hour of Day')
    axes[1, 1].set_title('Duration Heatmap: Hour × Day of Week')
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, 'time_correlation.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {save_path}")
    plt.close()
    
    # Statistical analysis
    print("\nRush Hour Impact:")
    non_rush = df[df['is_rush_hour'] == 0]['trip_duration']
    rush = df[df['is_rush_hour'] == 1]['trip_duration']
    
    print(f"  Non-rush hour avg: {non_rush.mean():.2f} min")
    print(f"  Rush hour avg:     {rush.mean():.2f} min")
    print(f"  Difference:        {rush.mean() - non_rush.mean():.2f} min ({((rush.mean() / non_rush.mean()) - 1) * 100:.1f}% increase)")
    
    # Correlation
    corr = df['hour'].corr(df['trip_duration'])
    print(f"\nCorrelation (hour vs duration): {corr:.3f}")
    
    print("\n" + "="*70 + "\n")


def analyze_vehicle_categories(df):
    """Compare vehicle categories"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(project_dir, 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*70)
    print("ANALYSIS 3: VEHICLE CATEGORY COMPARISON")
    print("="*70)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # Duration comparison
    vehicle_types = ['economy', 'sedan', 'suv']
    duration_data = [df[df['vehicle_type'] == vtype]['trip_duration'].values for vtype in vehicle_types]
    
    axes[0, 0].boxplot(duration_data, labels=['Economy', 'Sedan', 'SUV'])
    axes[0, 0].set_ylabel('Trip Duration (minutes)')
    axes[0, 0].set_title('Trip Duration by Vehicle Type')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Fare comparison
    fare_data = [df[df['vehicle_type'] == vtype]['fare'].values for vtype in vehicle_types]
    axes[0, 1].boxplot(fare_data, labels=['Economy', 'Sedan', 'SUV'])
    axes[0, 1].set_ylabel('Fare ($)')
    axes[0, 1].set_title('Fare by Vehicle Type')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Distance comparison
    distance_data = [df[df['vehicle_type'] == vtype]['trip_distance'].values for vtype in vehicle_types]
    axes[1, 0].boxplot(distance_data, labels=['Economy', 'Sedan', 'SUV'])
    axes[1, 0].set_ylabel('Trip Distance (km)')
    axes[1, 0].set_title('Trip Distance by Vehicle Type')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Average metrics by vehicle type
    vehicle_stats = df.groupby('vehicle_type').agg({
        'trip_duration': 'mean',
        'trip_distance': 'mean',
        'fare': 'mean'
    }).round(2)
    
    x = np.arange(len(vehicle_types))
    width = 0.25
    
    axes[1, 1].bar(x - width, vehicle_stats['trip_duration'], width, label='Duration (min)', alpha=0.8)
    axes[1, 1].bar(x, vehicle_stats['trip_distance'] * 2, width, label='Distance (km × 2)', alpha=0.8)
    axes[1, 1].bar(x + width, vehicle_stats['fare'] / 2, width, label='Fare ($ ÷ 2)', alpha=0.8)
    
    axes[1, 1].set_xlabel('Vehicle Type')
    axes[1, 1].set_ylabel('Normalized Value')
    axes[1, 1].set_title('Average Metrics by Vehicle Type (Normalized)')
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(['Economy', 'Sedan', 'SUV'])
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, 'vehicle_comparison.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {save_path}")
    plt.close()
    
    # Detailed statistics
    print("\nVehicle Type Statistics:")
    print("\n" + vehicle_stats.to_string())
    
    print("\n\nVehicle Type Distribution:")
    for vtype in vehicle_types:
        count = len(df[df['vehicle_type'] == vtype])
        pct = (count / len(df)) * 100
        print(f"  {vtype.capitalize():8s}: {count:5d} rides ({pct:5.1f}%)")
    
    print("\n" + "="*70 + "\n")


def correlation_analysis(df):
    """Analyze correlations between variables"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(project_dir, 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*70)
    print("CORRELATION ANALYSIS")
    print("="*70)
    
    # Select numeric columns
    numeric_cols = ['trip_distance', 'trip_duration', 'fare', 'hour', 'day_of_week', 'is_rush_hour']
    corr_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={'label': 'Correlation'})
    plt.title('Correlation Matrix: Trip Metrics')
    plt.tight_layout()
    save_path = os.path.join(output_dir, 'correlation_matrix.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {save_path}")
    plt.close()
    
    print("\nKey Correlations:")
    print(f"  Distance ↔ Duration:  {df['trip_distance'].corr(df['trip_duration']):6.3f}")
    print(f"  Distance ↔ Fare:      {df['trip_distance'].corr(df['fare']):6.3f}")
    print(f"  Duration ↔ Fare:      {df['trip_duration'].corr(df['fare']):6.3f}")
    print(f"  Hour ↔ Duration:      {df['hour'].corr(df['trip_duration']):6.3f}")
    print(f"  Rush Hour ↔ Duration: {df['is_rush_hour'].corr(df['trip_duration']):6.3f}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Run complete EDA"""
    print("\n" + "="*70)
    print("EXPLORATORY DATA ANALYSIS - RIDE-HAILING DATASET")
    print("="*70 + "\n")
    
    # Load data
    df = load_data()
    
    # Run analyses
    basic_statistics(df)
    analyze_trip_duration_distribution(df)
    analyze_time_of_day_correlation(df)
    analyze_vehicle_categories(df)
    correlation_analysis(df)
    
    print("="*70)
    print("EDA COMPLETE")
    print("="*70)
    print("\nGenerated visualizations:")
    print("  1. duration_distribution.png")
    print("  2. time_correlation.png")
    print("  3. vehicle_comparison.png")
    print("  4. correlation_matrix.png")
    print("\nAll files saved to: data/processed/")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
