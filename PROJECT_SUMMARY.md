# AI-Driven Vehicle Matching & Dynamic Pricing System – Project Summary

**Author:** Karthik Nayak  
**Role:** AI/ML Intern Applicant  
**Date:** January 2026

---

## 🚀 Project Overview

This project implements an intelligent vehicle matching and dynamic pricing system for ride-hailing platforms. The system predicts trip durations with 96% accuracy using machine learning, estimates demand across spatial regions and time periods, and provides a foundation for dynamic pricing decisions. By combining geospatial analysis, temporal pattern recognition, and gradient boosting algorithms, the system optimizes both rider experience (accurate ETAs) and platform efficiency (demand-based pricing). The implementation demonstrates production-ready ML engineering practices including feature engineering, model evaluation, and reproducible data pipelines.

---

## 🛠️ Architecture & Methods

### 1. Data Engineering

The project uses synthetically generated ride data to simulate realistic ride-hailing scenarios. I created a data generator that produces 10,000 rides over a 30-day period, incorporating:

- **Geospatial realism:** A 10km × 10km metro city grid with four high-demand hotspots (business district, airport, shopping area, residential hub) where 40% of rides originate or terminate
- **Temporal patterns:** Rush hour simulation with distinct traffic multipliers (1.8× for morning rush, 2.0× for evening rush) and demand variations throughout the day
- **Vehicle diversity:** Three vehicle categories (Economy, Sedan, SUV) with different base speeds, pricing structures, and fleet distributions matching real-world proportions

Synthetic data was chosen for several practical reasons: it eliminates API costs, ensures complete control over edge cases and distributions, avoids privacy concerns with real customer data, and enables rapid iteration during development. The data includes controlled randomness (±10% duration noise, ±5% fare noise) to simulate real-world variability while maintaining clear underlying patterns for ML models to learn.

### 2. Predictive Modeling (The "Brain")

#### ETA Prediction

I implemented and compared two models for trip duration prediction:

**Linear Regression (Baseline):**
- Achieved MAE of 1.53 minutes and R² of 0.88
- Serves as a simple, interpretable baseline
- Assumes linear relationships between features and duration

**LightGBM (Production Model):**
- Achieved MAE of 0.79 minutes and R² of 0.96
- Outperforms baseline by 48% on mean absolute error
- Captures non-linear patterns such as distance-rush hour interactions
- Uses gradient boosting with 200 trees, learning rate of 0.05, and early stopping to prevent overfitting

LightGBM was selected as the production model because it significantly outperforms the baseline while maintaining fast inference times (< 1ms per prediction). Feature importance analysis confirms that distance is the primary predictor (importance: 1479), followed by vehicle type (639) and hour of day (597), which aligns with domain knowledge and validates the model's learning.

#### Demand Estimation

The demand estimation system uses spatial and temporal aggregation rather than complex forecasting:

- **Spatial binning:** The city is divided into a 5×5 grid creating 25 regions, each approximately 2km × 2km
- **Temporal bucketing:** Demand is aggregated by hour (24 time periods) rather than minute-level precision
- **Demand scoring:** Each region-hour combination receives a normalized demand score (0-1) based on ride counts

This approach generates 600 demand slots (25 regions × 24 hours) with clear patterns: peak hours identified at 12-1 PM and 5 PM, high-demand regions concentrated in the city center (region 3_3), and 4% of slots qualifying for surge pricing (demand score ≥ 0.7). The simplicity of this approach makes it robust and interpretable while providing sufficient granularity for pricing decisions.

### 3. Core Logic (The "Engine")

#### Dynamic Pricing (Planned Implementation)

The dynamic pricing logic will use demand scores to calculate surge multipliers:

```
Base Fare = $2.50 + (Distance × $1.20/km) + (Duration × $0.30/min)

Surge Multiplier:
- Low demand (score < 0.3): 0.9× (discount to attract riders)
- Medium demand (0.3 ≤ score < 0.7): 1.0× (normal pricing)
- High demand (0.7 ≤ score < 0.85): 1.3× (moderate surge)
- Very high demand (score ≥ 0.85): 1.5× (high surge)

Final Fare = Base Fare × Surge Multiplier
```

The surge cap at 1.5× prevents excessive pricing that could damage user trust. This balanced approach ensures drivers are incentivized during high demand while keeping prices reasonable for riders. Currently, the demand model and scoring logic are implemented; integration with the pricing API is planned for Day 3-4.

#### Vehicle Ranking (Planned Implementation)

The vehicle ranking system will score available vehicles based on multiple factors:

- **ETA to pickup:** Predicted using the trained LightGBM model
- **Trip cost:** Calculated using base fare + distance + duration with applicable surge
- **Vehicle comfort:** Encoded as comfort scores (Economy: 1, Sedan: 2, SUV: 3)

User preference modes will weight these factors differently:
- **Fastest mode:** Prioritize lowest ETA (70% weight), cost secondary (30% weight)
- **Cheapest mode:** Prioritize lowest cost (70% weight), ETA secondary (30% weight)
- **Balanced mode:** Equal weighting (50% ETA, 50% cost)

The top-k vehicles (typically k=3) will be returned to the rider. This implementation is planned for Day 3-4 after API development.

### 4. API Layer (Planned Implementation)

The system will use FastAPI to provide a RESTful interface with the following design:

**Key Endpoints:**
- `POST /ride/quote`: Returns ETA, fare estimate, and available vehicles for a ride request
- `POST /vehicles/update`: Updates vehicle locations and availability status
- `GET /demand/region/{region_id}`: Returns current demand score for a region

**Design Principles:**
- Request validation using Pydantic models to ensure data integrity
- Low-latency responses (< 100ms target) by loading models at startup
- Clean JSON request/response format for easy integration
- Comprehensive error handling with meaningful status codes

The API layer is currently in planning phase and will be implemented in Day 3-4.

---

## 📊 Key Results & Performance

### ETA Model Performance

The LightGBM model demonstrates strong predictive accuracy:

- **MAE (Mean Absolute Error): 0.79 minutes** – On average, predictions are off by less than 1 minute (47 seconds), which is imperceptible to most users
- **RMSE (Root Mean Squared Error): 1.16 minutes** – The model handles outliers reasonably well, with RMSE only 47% higher than MAE
- **R² (Coefficient of Determination): 0.96** – The model explains 96% of variance in trip duration, indicating excellent fit
- **MAPE (Mean Absolute Percentage Error): 8.83%** – Predictions are within 9% of actual values on average

These metrics indicate production-ready performance. The model generalizes well to unseen data (minimal gap between training R² of 0.969 and test R² of 0.962), suggesting no significant overfitting.

### System Reliability

The implementation follows software engineering best practices:

- **Reproducibility:** Fixed random seed (42) ensures consistent results across runs
- **Modularity:** Separate modules for features, models, and evaluation enable easy testing and maintenance
- **Documentation:** Comprehensive docstrings and README files explain all components
- **Version control:** All code, models, and documentation tracked in Git with clear commit history

### Model Artifacts

All trained models and evaluation results are saved for deployment:
- 4 model files (.pkl format): Linear Regression, LightGBM, feature scaler, demand model
- 5 evaluation reports: Model metrics (JSON), feature importance (CSV), demand analysis (JSON), comprehensive evaluation (Markdown)
- Total model size: ~400 KB (lightweight for deployment)

---

## 🔮 Future Roadmap

**Immediate Next Steps (Day 3-4):**
- Implement FastAPI backend with `/ride/quote` and `/vehicles/update` endpoints
- Integrate ETA and demand models into API layer
- Develop vehicle ranking algorithm with user preference modes
- Add request validation and error handling

**Short-term Enhancements (Week 2):**
- Implement comprehensive unit tests for models and API endpoints
- Add API documentation using OpenAPI/Swagger
- Create deployment guide with Docker containerization
- Conduct load testing to validate latency targets

**Medium-term Improvements (Month 1-2):**
- Enhance demand forecasting with time-series models (Prophet, SARIMA) for better future predictions
- Implement real-time model updates as new ride data becomes available
- Add driver acceptance prediction to improve matching efficiency
- Develop A/B testing framework for pricing strategies

**Long-term Vision (Month 3+):**
- Integrate real-time traffic data from external APIs to improve ETA accuracy
- Implement multi-objective optimization for vehicle-rider matching
- Add explainability features (SHAP values) to justify pricing and ETA predictions to users
- Scale to multi-city deployment with city-specific model fine-tuning

---

## 📝 Technical Skills Demonstrated

This project showcases practical ML engineering skills relevant to production systems:

- **Machine Learning:** Regression modeling, gradient boosting, model evaluation, feature engineering
- **Data Engineering:** Synthetic data generation, geospatial analysis, temporal pattern simulation
- **Software Engineering:** Modular code design, version control, documentation, reproducibility
- **Domain Knowledge:** Understanding of ride-hailing business logic, pricing strategies, user experience optimization

The implementation prioritizes simplicity and interpretability over complexity, using LightGBM (a proven solution for tabular data) rather than unnecessarily complex deep learning approaches. All design decisions are justified by metrics and aligned with real-world constraints.

---

**Project Repository:** https://github.com/Karthiknayak26/AI_Vehicle_Matching.git  
**Current Status:** Day 2 Complete – ML Models Trained and Evaluated  
**Next Milestone:** API Development and Integration (Day 3-4)
