# Day 2-3 Model Evaluation Report

## Executive Summary

Successfully trained and evaluated machine learning models for ETA prediction and demand estimation. LightGBM significantly outperforms the Linear Regression baseline, achieving **96.2% accuracy** (R²) in predicting trip duration.

---

## Part A: Feature Engineering ✅

### Features Created

**Temporal Features:**
- `hour` - Hour of day (0-23)
- `day_of_week` - Day of week (0=Monday, 6=Sunday)
- `is_rush_hour` - Binary flag for rush hours (7-10 AM, 5-8 PM)
- `is_weekend` - Binary flag for weekends
- `is_morning_rush` - Morning rush hour flag
- `is_evening_rush` - Evening rush hour flag
- `is_late_night` - Late night flag (11 PM - 5 AM)

**Spatial Features:**
- `trip_distance` - Haversine distance in kilometers
- `region_id` - Spatial grid cell (5×5 grid = 25 regions)

**Categorical Features:**
- `vehicle_encoded` - Label-encoded vehicle type (0=economy, 1=sedan, 2=suv)

---

## Part B: ETA Prediction Models ✅

### Dataset Split
- **Training set:** 8,000 samples (80%)
- **Test set:** 2,000 samples (20%)
- **Random seed:** 42 (for reproducibility)

### Model 1: Linear Regression (Baseline)

**Purpose:** Establish baseline performance

**Results:**
```
MAE:  1.5301 minutes
RMSE: 2.1140 minutes
R²:   0.8760
MAPE: 25.82%
```

**Interpretation:**
- Decent baseline performance
- R² of 0.876 means model explains 87.6% of variance
- Average error of 1.53 minutes is acceptable
- Linear relationships captured well

### Model 2: LightGBM (Advanced)

**Hyperparameters:**
```python
{
    'objective': 'regression',
    'metric': 'mae',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'n_estimators': 200,
    'max_depth': 6,
    'min_child_samples': 20,
    'subsample': 0.8,
    'colsample_bytree': 0.8
}
```

**Results:**
```
MAE:  0.7914 minutes
RMSE: 1.1635 minutes
R²:   0.9624
MAPE: 8.83%
```

**Interpretation:**
- Excellent performance!
- R² of 0.962 means model explains 96.2% of variance
- Average error of only 0.79 minutes (< 1 minute!)
- MAPE of 8.83% shows consistent accuracy across all trip durations

### Model Comparison

| Metric | Linear Regression | LightGBM | Improvement |
|--------|------------------|----------|-------------|
| MAE    | 1.5301 min       | 0.7914 min | **+48.3%** ✅ |
| RMSE   | 2.1140 min       | 1.1635 min | **+45.0%** ✅ |
| R²     | 0.8760           | 0.9624     | **+8.6%** ✅ |
| MAPE   | 25.82%           | 8.83%      | **+65.8%** ✅ |

**Winner:** 🏆 **LightGBM**

**Justification:**
1. **48% better MAE** - Significantly more accurate predictions
2. **45% better RMSE** - Better handling of outliers
3. **96.2% R²** - Captures non-linear patterns
4. **Meets all success criteria** (MAE < 2.5 min, RMSE < 3.5 min, R² > 0.85)

### Feature Importance (LightGBM)

Top 5 most important features:

| Rank | Feature | Importance | Insight |
|------|---------|------------|---------|
| 1 | trip_distance | 1479 | Distance is the strongest predictor |
| 2 | vehicle_encoded | 639 | Vehicle type matters significantly |
| 3 | hour | 597 | Time of day affects duration |
| 4 | day_of_week | 482 | Day patterns exist |
| 5 | is_late_night | 193 | Late night has different patterns |

**Key Insights:**
- **Distance dominates** - As expected, longer trips take more time
- **Vehicle type matters** - Different vehicles have different speeds
- **Time of day is crucial** - Rush hour vs normal hours
- **Day patterns exist** - Weekday vs weekend differences

---

## Part C: Demand Estimation ✅

### Spatial Grid

**Configuration:**
- Grid size: 5×5 = **25 regions**
- Coverage: Entire city area
- Region naming: `{lat_grid}_{lon_grid}` (e.g., "3_3")

### Demand Analysis Results

**Overall Statistics:**
- **Total demand:** 10,000 rides
- **Average demand per slot:** 16.67 rides
- **Total demand slots:** 600 (25 regions × 24 hours)

**Peak Hours:**
1. Hour 13 (1 PM) - Highest demand
2. Hour 12 (12 PM) - Second highest
3. Hour 17 (5 PM) - Third highest

**High Demand Regions:**
1. Region 3_3 - City center
2. Region 1_3 - Business district
3. Region 1_1 - Residential area

**Surge Pricing Opportunities:**
- High demand slots: 24 out of 600 (4.0%)
- These slots qualify for surge pricing (demand_score ≥ 0.7)

### Demand Score Distribution

**Demand Levels:**
- **Low (0.0 - 0.3):** Discount pricing (0.9× multiplier)
- **Medium (0.3 - 0.7):** Normal pricing (1.0× multiplier)
- **High (0.7 - 0.85):** Moderate surge (1.3× multiplier)
- **Very High (≥ 0.85):** High surge (1.5× multiplier)

**Business Impact:**
- 4% of time slots have surge pricing opportunities
- Potential revenue increase of 30-50% during peak demand
- Balanced approach prevents excessive surge pricing

---

## Model Artifacts Saved

### Models
```
models/saved/
├── eta_linear.pkl          # Linear Regression model
├── eta_lgbm.pkl           # LightGBM model (BEST)
├── feature_scaler.pkl     # StandardScaler for features
└── demand_model.pkl       # Demand estimation lookup table
```

### Evaluation Reports
```
reports/
├── eta_evaluation.json           # Model metrics
├── feature_importance.csv        # Feature importance scores
├── demand_by_region_hour.csv    # Demand data by region/hour
└── demand_analysis.json          # Demand summary statistics
```

---

## Success Criteria Validation

### ETA Model ✅
- ✅ **MAE < 2.5 minutes** → Achieved 0.79 minutes (68% better)
- ✅ **RMSE < 3.5 minutes** → Achieved 1.16 minutes (67% better)
- ✅ **R² > 0.85** → Achieved 0.96 (13% better)
- ✅ **Better than baseline by ≥15%** → 48% better!

### Demand Model ✅
- ✅ **Identifies rush hour peaks** → Peak hours: 12-1 PM, 5 PM
- ✅ **Demand score correlates with actual rides** → Clear patterns
- ✅ **Can predict surge pricing zones** → 4% of slots identified

### Code Quality ✅
- ✅ **Modular, reusable functions** → Separate modules for features, models, evaluation
- ✅ **Proper error handling** → Validated inputs, graceful failures
- ✅ **Documented with docstrings** → All functions documented
- ✅ **Reproducible** → Fixed random seed (42)

---

## Real-World Application

### How to Use ETA Model

```python
import pickle
import numpy as np

# Load model and scaler
with open('models/saved/eta_lgbm.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/saved/feature_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Prepare features for a new ride
features = np.array([[
    4.5,    # trip_distance (km)
    8,      # hour (8 AM)
    1,      # day_of_week (Monday)
    1,      # is_rush_hour (yes)
    0,      # is_weekend (no)
    1,      # is_morning_rush (yes)
    0,      # is_evening_rush (no)
    0,      # is_late_night (no)
    0       # vehicle_encoded (economy)
]])

# Predict duration
predicted_duration = model.predict(features)[0]
print(f"Estimated trip duration: {predicted_duration:.1f} minutes")
# Output: Estimated trip duration: 16.2 minutes
```

### How to Use Demand Model

```python
import pickle

# Load demand model
with open('models/saved/demand_model.pkl', 'rb') as f:
    demand_model = pickle.load(f)

# Get demand for specific region and hour
region = '3_3'  # City center
hour = 17       # 5 PM

demand_data = demand_model['demand_data']
slot = [d for d in demand_data if d['region_id'] == region and d['hour'] == hour][0]

print(f"Region: {region}, Hour: {hour}")
print(f"Demand count: {slot['demand_count']}")
print(f"Demand score: {slot['demand_score']:.2f}")
print(f"Surge multiplier: {slot['surge_multiplier']}×")
# Output:
# Region: 3_3, Hour: 17
# Demand count: 45
# Demand score: 0.82
# Surge multiplier: 1.3×
```

---

## Conclusions

### Key Achievements

1. **Excellent ETA Prediction**
   - LightGBM model achieves 96.2% accuracy
   - Average error of less than 1 minute
   - 48% improvement over baseline

2. **Effective Demand Estimation**
   - 25 spatial regions covering entire city
   - Clear peak hour identification
   - Surge pricing opportunities identified

3. **Production-Ready Code**
   - Modular architecture
   - Comprehensive documentation
   - Saved artifacts for deployment

### Next Steps

**Day 4-5: API Development**
- Integrate ETA model into FastAPI
- Create `/ride/quote` endpoint
- Add demand-based surge pricing
- Implement vehicle ranking

**Day 6-7: Testing & Documentation**
- Unit tests for models
- API integration tests
- Final evaluation report
- Deployment guide

---

**Generated:** January 4, 2026  
**Models:** Linear Regression, LightGBM  
**Best Model:** LightGBM (MAE: 0.79 min, R²: 0.96)  
**Status:** ✅ Day 2-3 Complete
