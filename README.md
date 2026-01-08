# AI Vehicle Matching & Dynamic Pricing

> A machine learning system that recommends optimal vehicles for ride requests based on ETA prediction, demand forecasting, and dynamic pricing.

## 📋 Assignment Overview

This project implements an AI-driven vehicle matching and dynamic pricing system for ride-hailing platforms. The system predicts ETAs, forecasts demand, calculates dynamic pricing, and ranks vehicles based on rider preferences.

## 🎯 Project Status

- ✅ **Day 1**: Project setup and synthetic data generation (10,000 rides)
- ✅ **Day 2**: ML model training (ETA: 96% accuracy, Demand estimation)
- ✅ **Day 3**: Backend API with dynamic pricing and vehicle ranking
- ✅ **Day 4**: Automated testing suite (53/57 tests passed, 92.9%)
- ⏳ **Day 5-6**: Deployment and CI/CD
- ⏳ **Day 7**: Final documentation

## 🛠️ Tech Stack

- **Python 3.8+**
- **ML:** scikit-learn, LightGBM
- **Data:** pandas, numpy
- **API:** FastAPI, Pydantic, Uvicorn
- **Testing:** pytest, httpx

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
│   ├── pricing/               # Dynamic pricing module
│   │   └── dynamic_pricing.py # Surge pricing logic
│   ├── ranking/               # Vehicle ranking module
│   │   └── vehicle_ranker.py  # Weighted scoring
│   └── evaluation/            # Evaluation metrics
│       └── metrics.py         # MAE, RMSE, R² calculations
│
├── api/                       # FastAPI application
│   └── main.py               # REST API endpoints
│
├── scripts/
│   ├── generate_synthetic_data.py  # Data generator
│   ├── eda_analysis.py            # Exploratory analysis
│   ├── train_eta_models.py        # ETA model training
│   ├── estimate_demand.py         # Demand estimation
│   └── test_api.py               # API test suite
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
│   ├── DAY2_LEARNING_GUIDE.md
│   ├── DAY3_LEARNING_GUIDE.md
│   └── API_DOCUMENTATION.md   # API endpoint docs
│
├── tests/                     # Automated test suite
│   ├── __init__.py
│   ├── test_distance.py       # Distance calculation tests (7 tests)
│   ├── test_pricing.py        # Surge pricing tests (15 tests)
│   ├── test_ranking.py        # Vehicle ranking tests (16 tests)
│   ├── test_api.py           # API integration tests (18 tests)
│   └── README.md             # Test documentation
│
├── config.py                  # Configuration settings
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

### Run API Server

```bash
# Start FastAPI server
uvicorn api.main:app --reload

# Test API endpoints
python scripts/test_api.py

# Interactive API docs
# Open browser: http://localhost:8000/docs
```

### Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_pricing.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov=api
```


## 📊 Dataset

- **10,000 synthetic rides** over 30 days
- **3 vehicle types**: Economy (50%), Sedan (35%), SUV (15%)
- **Rush hour simulation**: Morning (7-10 AM), Evening (5-8 PM)
- **Realistic patterns**: Hotspots, traffic multipliers, surge pricing

See `data/README.md` for detailed documentation.

## 🎯 Core Features

1. **ETA Prediction** - Predict pickup time and trip duration (96% accuracy)
2. **Demand Forecasting** - Predict short-term demand per region (25 regions × 24 hours)
3. **Dynamic Pricing** - Calculate surge multipliers based on supply-demand (0.9× to 1.5×)
4. **Vehicle Ranking** - Recommend top-3 vehicles by rider preference (fastest/cheapest/balanced)
5. **REST API** - FastAPI endpoints for vehicle updates and ride quotes
6. **Automated Testing** - 57 comprehensive tests with 92.9% pass rate

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

**Backend API (Day 3):**
- **Dynamic Pricing**: 22% price variation based on demand-supply ratio
- **Surge Range**: 0.9× (discount) to 1.5× (high surge, capped)
- **Vehicle Ranking**: Different rankings for 3 user modes
- **API Response Time**: < 200ms (target met)
- **Endpoints**: 2 POST endpoints with Pydantic validation

**Automated Testing (Day 4):**
- **Total Tests**: 57 tests across 4 test files
- **Pass Rate**: 92.9% (53/57 tests passed)
- **Test Coverage**: Distance (7), Pricing (15), Ranking (16), API (18)
- **Critical Tests**: All 4 critical tests passed (surge cap, ranking, schema)
- **Execution Time**: 5.93 seconds


## 📝 Assignment Compliance

✅ Data generation with rush hours and demand surges  
✅ Comprehensive EDA with visualizations  
✅ Clean, production-style code structure  
✅ Detailed documentation  
✅ ETA prediction model (LightGBM: 96% accuracy)  
✅ Demand forecasting model (spatial + temporal)  
✅ Feature engineering (Haversine, temporal, encoding)  
✅ Model evaluation and comparison  
✅ Dynamic pricing logic (surge multipliers with fallback)  
✅ Vehicle ranking system (weighted scoring, 3 user modes)  
✅ REST API (FastAPI with 2 endpoints)  
✅ Request validation (Pydantic schemas)  
✅ API documentation (Swagger UI + manual docs)  
✅ Automated test suite (57 tests, 92.9% pass rate)  
✅ Distance calculation tests (7 tests, 100% pass)  
✅ Surge pricing tests (15 tests, 100% pass)  
✅ Vehicle ranking tests (16 tests, 100% pass)  
✅ API integration tests (15 tests, 83% pass)  
⏳ Deployment guide (upcoming)  
⏳ CI/CD pipeline (upcoming)
  

## 📧 Contact

For questions or feedback:
- **Email:** shricharan@unloadin.com
- **WhatsApp:** +91 9886498481

## 📄 License

MIT

## 🚀 API Endpoints

### POST /vehicles/update
Update vehicle location and status
```json
{
  "vehicle_id": "CAR001",
  "location": {"lat": 40.75, "lon": -74.00},
  "status": "available",
  "vehicle_type": "economy"
}
```

### POST /ride/quote
Get ride quote with ranked vehicle recommendations
```json
{
  "pickup": {"lat": 40.75, "lon": -74.00},
  "drop": {"lat": 40.76, "lon": -73.99},
  "user_mode": "fastest"
}
```

**Interactive Docs:** http://localhost:8000/docs

---

**Last Updated:** January 6, 2026  
**Status:** Day 4 Complete - Automated Testing Verified ✅

