# AI-Driven Vehicle Matching & Dynamic Pricing System – Project Summary

**Author:** Karthik Nayak  
**Role:** AI/ML Intern Applicant  
**Date:** January 2026

---

## 🚀 Project Overview

This project implements an intelligent vehicle matching and dynamic pricing system for ride-hailing platforms. The system predicts accurate trip durations (ETA), estimates regional demand patterns, calculates fair surge pricing, and ranks available vehicles based on user preferences. By combining machine learning models with business logic, the system optimizes both rider experience (minimizing wait times and costs) and driver utilization (maximizing earnings during peak demand). The solution demonstrates end-to-end ML engineering—from synthetic data generation to production-ready API deployment—while maintaining interpretability and real-world applicability.

---

## 🛠️ Architecture & Methods

### 1. Data Engineering

The foundation of this system is a realistic synthetic dataset of 10,000 ride records spanning 30 days. Rather than relying on expensive third-party APIs or proprietary data, I generated controlled data that captures real-world patterns: a 10km × 10km metro city grid with four high-demand hotspots (business district, airport, shopping area, residential hub), temporal variations including morning rush (7-10 AM) and evening rush (5-8 PM) with traffic multipliers up to 2.0×, and three vehicle categories (Economy, Sedan, SUV) with distinct speed and pricing characteristics. This approach provided complete control over edge cases, ensured reproducibility for testing, and allowed rapid iteration without external dependencies. The data includes mandatory fields (coordinates, timestamps, vehicle type, distance, duration, fare) and derived features (hour, day of week, rush hour flags) that directly support downstream ML models.

### 2. Predictive Modeling (The "Brain")

**ETA Prediction:**

I trained two models to predict trip duration: a Linear Regression baseline and a LightGBM gradient boosting model. The baseline achieved an MAE of 1.53 minutes with R² of 0.88, demonstrating that linear relationships capture much of the pattern. However, LightGBM significantly outperformed with MAE of 0.79 minutes and R² of 0.96—a 48% improvement. This performance gain comes from LightGBM's ability to learn non-linear interactions (e.g., short trips during rush hour are disproportionately slower due to traffic lights) and automatically handle feature importance (distance dominates, followed by vehicle type and hour). The model uses nine engineered features: Haversine distance, hour of day, day of week, rush hour flags (morning/evening/combined), weekend flag, late night flag, and encoded vehicle type. With an average error under one minute, the model provides reliable ETAs that users can trust.

**Demand Estimation:**

Instead of complex time-series forecasting, I implemented a pragmatic spatial-temporal aggregation approach. The city is divided into a 5×5 grid (25 regions), and demand is aggregated by region and hour, creating 600 demand slots (25 regions × 24 hours). Each slot receives a normalized demand score (0-1) based on historical ride counts. This approach is sufficient for surge pricing decisions—we don't need to predict exact ride counts, just whether demand is low, medium, or high. The model successfully identified peak hours (12-1 PM, 5-8 PM) and high-demand regions (city center, business district), with 4% of slots qualifying for surge pricing. This balance prevents excessive surging while capturing genuine supply-demand imbalances.

### 3. Core Logic (The "Engine")

**Dynamic Pricing:**

The pricing engine implements demand-responsive surge multipliers based on the demand score. The logic is straightforward: low demand (score < 0.3) applies a 0.9× discount to incentivize rides and utilize idle drivers; medium demand (0.3-0.7) maintains normal 1.0× pricing; high demand (0.7-0.85) applies a 1.3× moderate surge; and very high demand (≥0.85) applies a 1.5× maximum surge. This capped approach prevents price gouging while balancing supply and demand. The base fare calculation follows the formula:

```
Base Fare = Base Rate + (Distance × Per-KM Rate) + (Duration × Per-Minute Rate)
Final Fare = Base Fare × Surge Multiplier
```

For example, a 5 km, 12-minute Economy ride normally costs $12.50, but during high demand (1.3× surge), it becomes $16.25. This transparent pricing helps drivers earn more during peak times while keeping fares reasonable for riders.

**Vehicle Ranking:**

The ranking system scores available vehicles using a weighted combination of three factors: ETA to pickup (predicted using our ML model), estimated trip cost (calculated using the pricing formula), and vehicle comfort score (Economy=1, Sedan=2, SUV=3). Users can select their preference mode: Fastest (100% weight on ETA), Cheapest (100% weight on cost), or Balanced (50% ETA, 30% cost, 20% comfort). Each vehicle receives a normalized score (0-100), and the top-k vehicles are returned. For instance, in Fastest mode, a vehicle 3 minutes away scores higher than one 8 minutes away, regardless of price. This flexibility allows the system to adapt to different user priorities while maintaining objective, data-driven rankings.

### 4. API Layer

The system exposes a RESTful API built with FastAPI, chosen for its automatic validation, async support, and built-in OpenAPI documentation. The core endpoint `/ride/quote` accepts a ride request (pickup/drop coordinates, vehicle preference, user mode) and returns a ranked list of available vehicles with predicted ETAs, estimated fares, and surge information. The API loads pre-trained models at startup (LightGBM for ETA, demand lookup table for surge), performs feature extraction (Haversine distance, temporal features, vehicle encoding), runs predictions in under 10ms, and returns JSON responses with clear structure. Request validation using Pydantic ensures type safety and prevents invalid inputs. The design prioritizes low latency (critical for real-time user experience) and clean separation of concerns (API layer, business logic, ML models).

---

## 📊 Key Results & Performance

**ETA Model Performance:**

The LightGBM model achieved a Mean Absolute Error (MAE) of 0.79 minutes, meaning predictions are off by approximately 47 seconds on average. The Root Mean Squared Error (RMSE) of 1.16 minutes indicates the model handles outliers reasonably well. With an R² score of 0.96, the model explains 96% of the variance in trip duration—only 4% is attributed to unpredictable factors. Feature importance analysis confirms intuitive patterns: distance is the strongest predictor (importance: 1479), followed by vehicle type (639), hour of day (597), and day of week (482). These metrics demonstrate production-ready accuracy that would provide reliable ETAs to end users.

**System Reliability:**

The system demonstrates strong reliability through comprehensive testing and validation. Train-test split (80-20) with consistent performance across both sets indicates minimal overfitting. The demand model correctly identifies all expected peak hours and high-traffic regions, with demand scores correlating strongly with actual ride counts. Edge case handling includes minimum trip distances (0.5 km), late-night discounts, and surge caps to prevent extreme pricing. All model artifacts (4 .pkl files totaling ~400 KB) are lightweight and load in under 100ms, suitable for serverless deployment.

**API Performance:**

The FastAPI implementation achieves sub-10ms prediction latency for single requests, with the majority of time spent on feature extraction rather than model inference. The API handles concurrent requests efficiently through async processing and maintains clean error handling for invalid inputs (out-of-bounds coordinates, unsupported vehicle types). OpenAPI documentation auto-generates interactive API docs, making integration straightforward for frontend developers.

---

## 🔮 Future Roadmap

**Short-term Enhancements:**
- Implement real-time traffic data integration using Google Maps Traffic API to replace static rush hour multipliers with dynamic traffic conditions
- Add driver acceptance prediction to estimate likelihood of ride acceptance and adjust rankings accordingly
- Develop A/B testing framework to compare pricing strategies and measure impact on rider satisfaction and driver earnings

**Medium-term Improvements:**
- Build interactive dashboard for monitoring model performance, demand patterns, and pricing effectiveness in production
- Implement online learning pipeline to retrain models weekly with new ride data, adapting to changing traffic patterns and seasonal variations
- Add multi-objective optimization for vehicle assignment that balances rider wait time, driver utilization, and total system efficiency

**Long-term Vision:**
- Scale to multi-city deployment with city-specific models and pricing strategies
- Integrate weather data and event calendars (concerts, sports games) for better demand forecasting
- Develop reinforcement learning agent for dynamic driver repositioning to reduce pickup times in high-demand areas

---

**Technical Stack:** Python, LightGBM, scikit-learn, FastAPI, pandas, numpy  
**Code Quality:** Modular architecture, comprehensive docstrings, reproducible (fixed random seed)  
**Documentation:** 3 detailed reports (EDA, Model Evaluation, Learning Guides), production-ready README

---

*This project demonstrates practical ML engineering skills: data generation, feature engineering, model selection, evaluation, and API deployment. The focus on interpretability, business logic, and real-world constraints reflects production-ready thinking rather than academic experimentation.*
