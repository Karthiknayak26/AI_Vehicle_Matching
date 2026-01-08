import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.insert(0, PROJECT_ROOT)

from src.features.temporal import extract_temporal_features
from src.features.encoders import encode_vehicle_type

DATA_PATH = os.path.join(BASE_DIR, '../data/raw/rides.csv')
MODEL_PATH = os.path.join(BASE_DIR, '../models/saved/eta_lgbm.pkl')
REPORT_DIR = os.path.join(BASE_DIR, '../reports')

os.makedirs(REPORT_DIR, exist_ok=True)

def run_analysis():
    print("Loading data...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Preprocessing
    print("Preprocessing data...")
    # 1. Temporal Features
    df = extract_temporal_features(df)
    # 2. Vehicle Encoding (label for LGBM)
    df = encode_vehicle_type(df, method='label')
    
    # Define exact features used in training
    feature_cols = [
        'trip_distance',
        'hour',
        'day_of_week',
        'is_rush_hour',
        'is_weekend',
        'is_morning_rush',
        'is_evening_rush',
        'is_late_night',
        'vehicle_encoded'
    ]
    
    target_col = 'trip_duration'
    
    # Take last 20% as test set to simulate "Test Data"
    test_size = int(len(df) * 0.2)
    test_df = df.tail(test_size).copy()
    
    # Select features and target
    X_test = test_df[feature_cols].copy()
    y_test = test_df[target_col].copy()
    
    print("Loading model...")
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        return

    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Predict
    print("Predicting...")
    try:
        y_pred = model.predict(X_test)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return
    
    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    
    # Save Plots
    print("Generating plots...")
    
    # 1. Scatter
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual ETA (min)')
    plt.ylabel('Predicted ETA (min)')
    plt.title('Actual vs Predicted ETA')
    plt.savefig(os.path.join(REPORT_DIR, 'analysis_scatter.png'))
    plt.close()
    
    # 2. Error Dist
    error = y_test - y_pred
    plt.figure(figsize=(8, 6))
    sns.histplot(error, bins=30, kde=True, color='purple')
    plt.title('Error Distribution')
    plt.xlabel('Error (Minutes)')
    plt.savefig(os.path.join(REPORT_DIR, 'analysis_error_dist.png'))
    plt.close()
    
    # 3. Line Plot (Sample)
    sample_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred}).head(50)
    plt.figure(figsize=(12, 6))
    plt.plot(sample_df.index, sample_df['Actual'], label='Actual', marker='o')
    plt.plot(sample_df.index, sample_df['Predicted'], label='Predicted', marker='x', linestyle='--')
    plt.title('Actual vs Predicted (First 50 Samples)')
    plt.legend()
    plt.savefig(os.path.join(REPORT_DIR, 'analysis_line_plot.png'))
    plt.close()
    
    print("Analysis complete. Plots saved to reports/")

if __name__ == "__main__":
    run_analysis()
