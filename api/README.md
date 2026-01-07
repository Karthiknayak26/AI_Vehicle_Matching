# AI Vehicle Matching - Backend API Service

The backend service for the AI Vehicle Matching system, built with **FastAPI**. It handles ride requests, calculates dynamic pricing, ranks vehicles using ML models, and manages vehicle state.

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Validations:** Pydantic
- **ML Models:** scikit-learn, LightGBM
- **Server:** Uvicorn

## 🚀 Key Features

### 1. **CORS Support**
- Fully configured for frontend integration
- Allowed Origins: `http://localhost:3000`, `http://localhost:5173`, `http://127.0.0.1:3000`
- Supports `GET`, `POST`, `OPTIONS` methods

### 2. **India Localization (Udupi)**
- **Geofencing:** Validates coordinates within Udupi region
- **Mock Data:** Pre-configured with Udupi landmarks
- **Vehicle Data:** Generates Indian vehicle models and Karnataka (KA) registration plates

### 3. **Dynamic Pricing Engine**
- **Surge Multipliers:** Calculates price based on demand (0.9x - 1.5x)
- **Factors:** Traffic density, time of day, weather conditions (simulated)

### 4. **AI Vehicle Ranking**
- Scores vehicles based on user preference:
    - **Fastest:** Prioritizes lower OTA
    - **Cheapest:** Prioritizes lower price
    - **Balanced:** Weighted score of price and time

---

## 🚦 Setup & Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Server
```bash
uvicorn api.main:app --reload
```
Server runs at: `http://localhost:8000`

### 3. API Documentation
interactive Swagger UI available at: `http://localhost:8000/docs`

---

## 📡 API Endpoints

### `GET /health`
Checks API status.
**Response:** `{"status": "active", "version": "1.0.0"}`

### `POST /vehicles/update`
Updates vehicle location and status.
```json
{
  "vehicle_id": "KA20AB1234",
  "location": {"lat": 13.3409, "lon": 74.7421},
  "status": "available",
  "vehicle_type": "sedan"
}
```

### `POST /ride/quote`
Get ride estimates and vehicle recommendations.
```json
{
  "pickup": {"lat": 13.3525, "lon": 74.7928},
  "drop": {"lat": 13.3409, "lon": 74.7421},
  "user_mode": "balanced"
}
```

---

**Last Updated:** January 7, 2026
**Status:** Active & Integrated ✅
