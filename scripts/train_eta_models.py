"""
ETA Prediction Model Training Script

Trains and evaluates Linear Regression and LightGBM models for trip duration prediction.
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

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb

from src.features.distance import calculate_trip_distance
from src.features.temporal import extract_temporal_features
from src.features.encoders import encode_vehicle_type
from src.evaluation.metrics import (
    calculate_regression_metrics,
    print_metrics,
    compare_models,
    save_metrics
)

# Set random seed for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


def load_and_prepare_data(data_path='data/raw/rides.csv'):
    """
    Load and prepare data for modeling.
    
    Returns
    -------
    tuple
        (X_train, X_test, y_train, y_test, feature_names, scaler)
    """
    print("\n" + "="*60)
    print("LOADING AND PREPARING DATA")
    print("="*60)
    
    # Load data
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"✓ Loaded {len(df):,} rides")
    
    # Extract temporal features
    print("Extracting temporal features...")
    df = extract_temporal_features(df)
    
    # Encode vehicle type (label encoding for tree-based models)
    print("Encoding vehicle types...")
    df = encode_vehicle_type(df, method='label')
    
    # Select features for modeling
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
    
    X = df[feature_cols].copy()
    y = df['trip_duration'].copy()
    
    print(f"\nFeatures: {feature_cols}")
    print(f"Target: trip_duration")
    print(f"Dataset shape: {X.shape}")
    
    # Train-test split
    print(f"\nSplitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    
    print(f"Train set: {len(X_train):,} samples")
    print(f"Test set:  {len(X_test):,} samples")
    
    # Scale features for Linear Regression
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("✓ Data preparation complete")
    
    return (X_train, X_test, y_train, y_test, 
            X_train_scaled, X_test_scaled, 
            feature_cols, scaler)


def train_linear_regression(X_train, X_test, y_train, y_test):
    """
    Train and evaluate Linear Regression model.
    
    Returns
    -------
    tuple
        (model, metrics)
    """
    print("\n" + "="*60)
    print("TRAINING LINEAR REGRESSION (BASELINE)")
    print("="*60)
    
    # Train model
    print("Training Linear Regression...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions
    print("Making predictions...")
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Evaluate
    print("\nEvaluating on training set...")
    train_metrics = calculate_regression_metrics(y_train, y_pred_train)
    
    print("Evaluating on test set...")
    test_metrics = calculate_regression_metrics(y_test, y_pred_test)
    
    # Print results
    print_metrics(train_metrics, "Linear Regression (Train)")
    print_metrics(test_metrics, "Linear Regression (Test)")
    
    return model, test_metrics


def train_lightgbm(X_train, X_test, y_train, y_test, feature_names):
    """
    Train and evaluate LightGBM model.
    
    Returns
    -------
    tuple
        (model, metrics)
    """
    print("\n" + "="*60)
    print("TRAINING LIGHTGBM (ADVANCED)")
    print("="*60)
    
    # LightGBM parameters
    params = {
        'objective': 'regression',
        'metric': 'mae',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'n_estimators': 200,
        'max_depth': 6,
        'min_child_samples': 20,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': RANDOM_STATE,
        'verbose': -1
    }
    
    print("Parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    # Train model
    print("\nTraining LightGBM...")
    model = lgb.LGBMRegressor(**params)
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        eval_metric='mae',
        callbacks=[lgb.early_stopping(stopping_rounds=20, verbose=False)]
    )
    
    # Predictions
    print("Making predictions...")
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Evaluate
    print("\nEvaluating on training set...")
    train_metrics = calculate_regression_metrics(y_train, y_pred_train)
    
    print("Evaluating on test set...")
    test_metrics = calculate_regression_metrics(y_test, y_pred_test)
    
    # Print results
    print_metrics(train_metrics, "LightGBM (Train)")
    print_metrics(test_metrics, "LightGBM (Test)")
    
    # Feature importance
    print("\nTop 5 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(5).iterrows():
        print(f"  {row['feature']:<20}: {row['importance']:.2f}")
    
    return model, test_metrics, feature_importance


def save_models_and_results(lr_model, lgb_model, scaler, lr_metrics, lgb_metrics, 
                            feature_importance, feature_names):
    """
    Save trained models and evaluation results.
    """
    print("\n" + "="*60)
    print("SAVING MODELS AND RESULTS")
    print("="*60)
    
    # Create directories
    os.makedirs('models/saved', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Save models
    print("Saving models...")
    with open('models/saved/eta_linear.pkl', 'wb') as f:
        pickle.dump(lr_model, f)
    print("✓ Saved: models/saved/eta_linear.pkl")
    
    with open('models/saved/eta_lgbm.pkl', 'wb') as f:
        pickle.dump(lgb_model, f)
    print("✓ Saved: models/saved/eta_lgbm.pkl")
    
    with open('models/saved/feature_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("✓ Saved: models/saved/feature_scaler.pkl")
    
    # Save metrics
    print("\nSaving metrics...")
    metrics_data = {
        'linear_regression': lr_metrics,
        'lightgbm': lgb_metrics,
        'feature_names': feature_names,
        'random_state': RANDOM_STATE
    }
    
    save_metrics(metrics_data, 'reports/eta_evaluation.json')
    
    # Save feature importance
    print("Saving feature importance...")
    feature_importance.to_csv('reports/feature_importance.csv', index=False)
    print("✓ Saved: reports/feature_importance.csv")
    
    print("\n✓ All models and results saved successfully!")


def main():
    """
    Main training pipeline.
    """
    print("\n" + "="*60)
    print("ETA PREDICTION MODEL TRAINING PIPELINE")
    print("="*60)
    
    # Load and prepare data
    (X_train, X_test, y_train, y_test,
     X_train_scaled, X_test_scaled,
     feature_names, scaler) = load_and_prepare_data()
    
    # Train Linear Regression (baseline)
    lr_model, lr_metrics = train_linear_regression(
        X_train_scaled, X_test_scaled, y_train, y_test
    )
    
    # Train LightGBM (advanced)
    lgb_model, lgb_metrics, feature_importance = train_lightgbm(
        X_train, X_test, y_train, y_test, feature_names
    )
    
    # Compare models
    metrics_dict = {
        'Linear Regression': lr_metrics,
        'LightGBM': lgb_metrics
    }
    best_model = compare_models(metrics_dict)
    
    # Calculate improvement
    mae_improvement = ((lr_metrics['mae'] - lgb_metrics['mae']) / lr_metrics['mae']) * 100
    rmse_improvement = ((lr_metrics['rmse'] - lgb_metrics['rmse']) / lr_metrics['rmse']) * 100
    
    print(f"\n📊 LightGBM Improvements over Linear Regression:")
    print(f"   MAE:  {mae_improvement:+.1f}% better")
    print(f"   RMSE: {rmse_improvement:+.1f}% better")
    print(f"   R²:   {lgb_metrics['r2'] - lr_metrics['r2']:+.4f} higher")
    
    # Save everything
    save_models_and_results(
        lr_model, lgb_model, scaler,
        lr_metrics, lgb_metrics,
        feature_importance, feature_names
    )
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\n🏆 Best Model: {best_model}")
    print(f"   MAE:  {lgb_metrics['mae']:.4f} minutes")
    print(f"   RMSE: {lgb_metrics['rmse']:.4f} minutes")
    print(f"   R²:   {lgb_metrics['r2']:.4f}")
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    main()
