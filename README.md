# AI Vehicle Matching & Dynamic Pricing

> A machine learning system that recommends optimal vehicles for ride requests based on ETA prediction, demand forecasting, and dynamic pricing.

## 📋 Assignment Overview

This project implements an AI-driven vehicle matching and dynamic pricing system for ride-hailing platforms. The system predicts ETAs, forecasts demand, calculates dynamic pricing, and ranks vehicles based on rider preferences.

## 🎯 Project Status

- ✅ **Day 1**: Project setup and synthetic data generation (10,000 rides)
- 🔄 **Day 2-3**: Model training (ETA, demand forecasting)
- ⏳ **Day 4-5**: API development and integration
- ⏳ **Day 6-7**: Testing and documentation

## 🛠️ Tech Stack

- **Python 3.8+**
- **ML:** scikit-learn, LightGBM/XGBoost, Prophet
- **Data:** pandas, numpy, geopandas, H3
- **API:** FastAPI
- **Testing:** pytest

## 📂 Project Structure

```
ride-matching-mvp/
├── data/
│   ├── raw/              # Original datasets
│   ├── processed/        # Cleaned data
│   └── README.md         # Data documentation
├── scripts/
│   ├── generate_synthetic_data.py
│   └── eda_analysis.py
├── notebooks/            # Exploratory analysis
├── requirements.txt
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

## 📈 Key Metrics (Day 1)

- **Distance**: Mean 4.36 km, Range 0.5-11.46 km
- **Duration**: Mean 9.39 min, Range 1.0-45.67 min
- **Fare**: Mean $14.64, Range $2.57-$76.56
- **Rush hour impact**: 60% longer trips during peak hours

## 📝 Assignment Compliance

✅ Data generation with rush hours and demand surges  
✅ Comprehensive EDA with visualizations  
✅ Clean, production-style code structure  
✅ Detailed documentation  
⏳ ETA prediction model (upcoming)  
⏳ Demand forecasting model (upcoming)  
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

**Last Updated:** January 3, 2026  
**Status:** Day 1 Complete - Project Setup & Data Generation ✅
