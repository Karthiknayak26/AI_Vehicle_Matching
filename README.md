# AI-Driven Vehicle Matching & Dynamic Pricing System

**🔴 LIVE DEMO:** [https://ai-vehicle-matching-kappa.vercel.app/](https://ai-vehicle-matching-kappa.vercel.app/) (Frontend hosted on Vercel, Backend on Render)

---

## 1. Overview

This system solves the "Dispatch Intelligence" problem in modern ride-hailing: ensuring that the right car reaches the right passenger at a fair market price, instantly.

Unlike simple taxi dispatchers that just look for the closest car, this engine uses a three-step intelligence pipeline:
1.  **Predictive Modeling**: A LightGBM regression model estimates travel time (ETA) based on distance, traffic patterns, and vehicle type, predicting trip duration with 96% accuracy.
2.  **Dynamic Pricing**: The system monitors supply and demand in real-time geospatial bins. When demand outstrips supply, it applies surge pricing to equilibrate the market.
3.  **Intelligent Ranking**: Instead of a "one-size-fits-all" match, the ranking engine scores vehicles based on user intent (Fastest vs. Cheapest vs. Balanced) to optimize the rider experience.

---

## 2. Key Assumptions & Constraints

To build a functional MVP within a constrained timeline, the following engineering assumptions were made:

*   **Surge Pricing Cap (1.5x)**
    *   **Reasoning:** To prevent price gouging during simulated extreme demand and maintain a realistic user experience.
    *   **Implementation:** Clamped in `src.pricing.dynamic_pricing`.
*   **Haversine Distance**
    *   **Reasoning:** Calculating "as-the-crow-flies" distance avoids the latency and cost of external Routing APIs (Google Directions) for validatable logic.
    *   **Implementation:** `src.utils.distance_calc`.
*   **Simulated Vehicle Supply**
    *   **Reasoning:** Without a real fleet of drivers, we simulate 50 vehicles moving around Udupi/Manipal to demonstrate matching logic.
    *   **Implementation:** In-memory `VehicleStore` initialized on startup.
*   **Hardcoded Rush Hour Logic**
    *   **Reasoning:** Traffic patterns are deterministic for the simulation (Morning: 7-10 AM, Evening: 5-8 PM) to guarantee predictable model behavior.
    *   **Implementation:** `SimulatedClock` and `TrafficGenerator`.
*   **Mock Geocoding**
    *   **Reasoning:** The frontend uses predefined coordinates for local landmarks (e.g., Manipal University, Malpe Beach) to simplify the demo flow.
    *   **Implementation:** `geocoding.js` in frontend.

---

## 3. Day-wise Implementation Breakdown

### Day 1: Data Engineering & Analysis
*   **Synthetic Data Generation:** I built a custom generator to produce 10,000 historical ride records.
*   **Why:** Real-world dispatch data is proprietary. Synthetic data allowed me to inject specific signals (e.g., "Rain slows traffic by 1.5x") to test if the model could learn them.
*   **EDA:** Analysis confirmed that distance and hour-of-day were the strongest predictors of duration, validating the feature set.

### Day 2: AI & Predictive Modeling
*   **Feature Engineering:** Raw timestamps were converted into cyclical features (hour, day_of_week) and boolean flags (is_rush_hour) to help the model generalize.
*   **ETA Model:** Trained a **LightGBM Regressor** because it handles non-linear relationships (like traffic congestion tiers) better than linear regression.
*   **Demand Forecasting:** Implemented a spatial binning strategy (Grid system) to estimate demand density per km².

### Day 3: Core Engine (Business Logic)
*   **Dynamic Pricing:** Implemented the `get_surge_multiplier` logic based on the Demand-to-Supply ratio.
*   **Vehicle Ranking:** Built a multi-objective scoring function.
    *   *Fastest:* 70% ETA weight.
    *   *Cheapest:* 70% Price weight.
*   **API:** Exposed these capabilities via **FastAPI** endpoints (`/ride/quote`, `/vehicles/update`) ensuring <200ms response times.

### Day 4: Verification & Quality Assurance
*   **Unit Testing:** Wrote 57 tests using `pytest` covering 100% of the critical pricing and ranking paths.
*   **Reliability:** Strict tests ensure that surge multipliers never exceed the 1.5x cap and that ranking order changes deterministically based on user preference.
*   **Validation:** Verified the end-to-end flow from request to quote response.

### Day 5: UI/UX & Integration
*   **Frontend Demo:** Built a React + Leaflet application to visualize the backend intelligence.
*   **Visualization:** Created an "AI Processing" overlay that shows the user exactly what the system is doing (Fetching Candidates → Calculating Scores → Optimizing Rank).
*   **Experience:** Implemented valid route visualization and vehicle animations to mimic a production app like Uber/Ola.

---

## 4. Model Performance

The ETA prediction system runs on a trained LightGBM model.

*   **Model Type:** LightGBM Regressor (Gradient Boosting)
*   **MAE (Mean Absolute Error):** 0.79 minutes
*   **RMSE (Root Mean Square Error):** 1.16 minutes
*   **R² Score:** 0.96

**Interpretation:** On average, the system's ETA prediction is accurate to within **48 seconds** of the actual trip duration. The high R² indicates the model has successfully learned the traffic and distance patterns of the simulated city.

---

## 5. Setup Instructions

1.  **Clone and Setup Backend:**
    ```bash
    git clone https://github.com/Karthiknayak26/AI_Vehicle_Matching.git
    cd AI_Vehicle_Matching
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    # source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Setup Frontend:**
    ```bash
    cd frontend
    npm install
    ```

---

## 6. Running the Project

**1. Start the API Server:**
```bash
# From root directory
python api/main.py
```
*Server runs at http://localhost:8000*

**2. Start the Frontend:**
```bash
# From frontend directory
npm run dev
```
*App runs at http://localhost:5173*

**3. Run Tests:**
```bash
pytest tests/ -v
```

---

## 7. Limitations

*   **Simulated Traffic:** We use time-of-day multipliers rather than real-time Google Maps Traffic data.
*   **In-Memory State:** Vehicles reset when the server restarts; a production version would use Redis.
*   **Single-Passenger:** The current logic does not support ride-pooling or multi-stop trips.

---

## 8. Future Improvements

*   **Real-time GPS:** Integration with driver mobile apps for live location streaming.
*   **Persistent Database:** Storing ride history in PostgreSQL for long-term analytics.
*   **Advanced Forecasting:** Using Prophet or LSTM models for temporal demand forecasting.
*   **Cloud Scaling:** Deploying the inference engine on Kubernetes for horizontal scaling.

## 9. Demo Scenarios (Try It Live!)

To see the dynamic system in action, try these specific locations:

*   **⚡ High Demand Surge (1.4x):**
    *   **Pickup:** `Manipal University`
    *   **Reason:** Simulates a student rush hour scenario.
*   **💰 Low Demand Discount (0.9x):**
    *   **Pickup:** `Malpe Beach`
    *   **Reason:** Simulates low foot traffic times (Promotion applied).
*   **⚖️ Normal Pricing:**
    *   **Pickup:** `Udupi Sri Krishna Temple`
    *   **Reason:** Standard balanced market conditions.
