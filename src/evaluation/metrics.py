"""
Evaluation Metrics Module

Provides standard regression metrics for model evaluation.
"""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import json


def calculate_regression_metrics(y_true, y_pred):
    """
    Calculate comprehensive regression metrics.
    
    Parameters
    ----------
    y_true : array-like
        True target values
    y_pred : array-like
        Predicted values
    
    Returns
    -------
    dict
        Dictionary containing:
        - mae: Mean Absolute Error
        - rmse: Root Mean Squared Error
        - r2: R-squared score
        - mape: Mean Absolute Percentage Error
    
    Examples
    --------
    >>> y_true = [10, 15, 20, 25]
    >>> y_pred = [11, 14, 21, 24]
    >>> metrics = calculate_regression_metrics(y_true, y_pred)
    >>> metrics['mae']
    1.0
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    # Mean Absolute Percentage Error
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return {
        'mae': round(float(mae), 4),
        'rmse': round(float(rmse), 4),
        'r2': round(float(r2), 4),
        'mape': round(float(mape), 4)
    }


def print_metrics(metrics, model_name='Model'):
    """
    Print metrics in a formatted way.
    
    Parameters
    ----------
    metrics : dict
        Dictionary of metrics from calculate_regression_metrics
    model_name : str
        Name of the model for display
    """
    print(f"\n{'='*60}")
    print(f"{model_name} Performance Metrics")
    print(f"{'='*60}")
    print(f"MAE (Mean Absolute Error):     {metrics['mae']:.4f} minutes")
    print(f"RMSE (Root Mean Squared Error): {metrics['rmse']:.4f} minutes")
    print(f"R² (R-squared):                 {metrics['r2']:.4f}")
    print(f"MAPE (Mean Abs % Error):        {metrics['mape']:.2f}%")
    print(f"{'='*60}\n")


def compare_models(metrics_dict):
    """
    Compare multiple models and identify the best one.
    
    Parameters
    ----------
    metrics_dict : dict
        Dictionary mapping model names to their metrics
        Example: {'Linear Regression': {...}, 'LightGBM': {...}}
    
    Returns
    -------
    str
        Name of the best model
    
    Examples
    --------
    >>> metrics = {
    ...     'Model A': {'mae': 2.5, 'rmse': 3.2, 'r2': 0.85},
    ...     'Model B': {'mae': 1.8, 'rmse': 2.4, 'r2': 0.92}
    ... }
    >>> compare_models(metrics)
    'Model B'
    """
    print(f"\n{'='*80}")
    print("MODEL COMPARISON")
    print(f"{'='*80}")
    print(f"{'Model':<20} {'MAE':<12} {'RMSE':<12} {'R²':<12} {'MAPE':<12}")
    print(f"{'-'*80}")
    
    best_model = None
    best_r2 = -np.inf
    
    for model_name, metrics in metrics_dict.items():
        print(f"{model_name:<20} {metrics['mae']:<12.4f} {metrics['rmse']:<12.4f} "
              f"{metrics['r2']:<12.4f} {metrics['mape']:<12.2f}%")
        
        if metrics['r2'] > best_r2:
            best_r2 = metrics['r2']
            best_model = model_name
    
    print(f"{'-'*80}")
    print(f"\n🏆 Best Model: {best_model} (R² = {best_r2:.4f})")
    print(f"{'='*80}\n")
    
    return best_model


def save_metrics(metrics, filepath):
    """
    Save metrics to JSON file.
    
    Parameters
    ----------
    metrics : dict
        Metrics dictionary
    filepath : str
        Path to save JSON file
    """
    with open(filepath, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Metrics saved to: {filepath}")


def load_metrics(filepath):
    """
    Load metrics from JSON file.
    
    Parameters
    ----------
    filepath : str
        Path to JSON file
    
    Returns
    -------
    dict
        Metrics dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)
