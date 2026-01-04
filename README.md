# AI Vehicle Matching & Dynamic Pricing

> A machine learning system that recommends optimal vehicles for ride requests based on ETA prediction, demand forecasting, and dynamic pricing.

## 📋 Assignment Overview

This project implements an AI-driven vehicle matching and dynamic pricing system for ride-hailing platforms. The system predicts ETAs, forecasts demand, calculates dynamic pricing, and ranks vehicles based on rider preferences.

## 🎯 Project Status

- ✅ **Day 1**: Project setup and synthetic data generation (10,000 rides)
- ✅ **Day 2**: ML model training (ETA: 96% accuracy, Demand estimation)
- 🔄 **Day 3-4**: API development and integration
- ⏳ **Day 5-6**: Testing and documentation

## 🛠️ Tech Stack

- **Python 3.8+**
- **ML:** scikit-learn, LightGBM/XGBoost, Prophet
- **Data:** pandas, numpy, geopandas, H3
- **API:** FastAPI
- **Testing:** pytest

## 📂 Project Structure

```
AI_Vehicle_Matching/
├── data/
│   ├── raw/                    # Raw datasets
│   │   └── rides.csv          # 10,000 synthetic rides
│   ├── processed/              # Processed data & visualizations
│   │   ├── duration_distribution.png
│   │   ├── time_correlation.png
│   │   ├── vehicle_comparison.png
│   │   └── correlation_matrix.png
│   └── README.md              # Data documentation
│
├── src/
│   ├── features/              # Feature engineering modules
│   │   ├── distance.py        # Haversine distance calculation
│   │   ├── temporal.py        # Time-based features
│   │   └── encoders.py        # Vehicle type encoding
│   ├── models/                # Model implementations (planned)
│   └── evaluation/            # Evaluation metrics
│       └── metrics.py         # MAE, RMSE, R² calculations
│
├── scripts/
│   ├── generate_synthetic_data.py  # Data generator
│   ├── eda_analysis.py            # Exploratory analysis
│   ├── train_eta_models.py        # ETA model training
│   └── estimate_demand.py         # Demand estimation
│
├── models/saved/              # Trained models
│   ├── eta_linear.pkl         # Linear Regression baseline
│   ├── eta_lgbm.pkl          # LightGBM (production model)
│   ├── feature_scaler.pkl    # Feature scaler
│   └── demand_model.pkl      # Demand estimation model
│
├── reports/                   # Evaluation reports
│   ├── MODEL_EVALUATION.md   # Comprehensive evaluation
│   ├── eta_evaluation.json   # Model metrics
│   ├── feature_importance.csv
│   ├── demand_analysis.json
│   └── demand_by_region_hour.csv
│
├── docs/                      # Documentation
│   ├── DAY1_LEARNING_GUIDE.md
│   └── DAY2_LEARNING_GUIDE.md
│
├── PROJECT_SUMMARY.md         # Project summary report
├── PROJECT_THEORY.md          # Complete system theory
├── requirements.txt           # Python dependencies
└── README.md
```


## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Karthiknayak26/AI_Vehicle_Matching.git
cd AI_Vehicle_Matching

# Install dependencies
pip install -r requirements.txt
```

### Generate Synthetic Data

```bash
python scripts/generate_synthetic_data.py
```

### Run EDA

```bash
python scripts/eda_analysis.py
```

### Train ML Models

```bash
# Train ETA prediction models (Linear Regression + LightGBM)
python scripts/train_eta_models.py

# Estimate demand by region and time
python scripts/estimate_demand.py
```


## 📊 Dataset

- **10,000 synthetic rides** over 30 days
- **3 vehicle types**: Economy (50%), Sedan (35%), SUV (15%)
- **Rush hour simulation**: Morning (7-10 AM), Evening (5-8 PM)
- **Realistic patterns**: Hotspots, traffic multipliers, surge pricing

See `data/README.md` for detailed documentation.

## 🎯 Core Features

1. **ETA Prediction** - Predict pickup time and trip duration
2. **Demand Forecasting** - Predict short-term demand per region
3. **Dynamic Pricing** - Calculate surge multipliers based on supply-demand
4. **Vehicle Ranking** - Recommend top-k vehicles by rider preference

## 📈 Key Metrics

**Dataset (Day 1):**
- **Distance**: Mean 4.36 km, Range 0.5-11.46 km
- **Duration**: Mean 9.39 min, Range 1.0-45.67 min
- **Fare**: Mean $14.64, Range $2.57-$76.56
- **Rush hour impact**: 60% longer trips during peak hours

**ML Models (Day 2):**
- **ETA Model (LightGBM)**: MAE 0.79 min, RMSE 1.16 min, R² 0.96
- **Baseline (Linear Regression)**: MAE 1.53 min, R² 0.88
- **Improvement**: 48% better than baseline
- **Demand Model**: 25 regions, 600 time slots, 4% surge opportunities


## 📝 Assignment Compliance

✅ Data generation with rush hours and demand surges  
✅ Comprehensive EDA with visualizations  
✅ Clean, production-style code structure  
✅ Detailed documentation  
✅ ETA prediction model (LightGBM: 96% accuracy)  
✅ Demand forecasting model (spatial + temporal)  
✅ Feature engineering (Haversine, temporal, encoding)  
✅ Model evaluation and comparison  
⏳ Dynamic pricing logic (upcoming)  
⏳ Vehicle ranking system (upcoming)  
⏳ REST API (upcoming)
  

## 📧 Contact

For questions or feedback:
- **Email:** shricharan@unloadin.com
- **WhatsApp:** +91 9886498481

## 📄 License

MIT

---

**Last Updated:** January 4, 2026  
**Status:** Day 2 Complete - ML Models Trained ✅

