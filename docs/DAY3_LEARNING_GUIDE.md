# Day 3 Learning Guide: Backend API & Decision Engine

> Understanding dynamic pricing, vehicle ranking, and REST APIs in simple terms

---

## 1. WHY Day 3 Exists

**The Problem:**
Day 2 gave us smart ML models, but they're useless sitting on your computer. We need:
- A way for users to REQUEST rides
- A way to CALCULATE prices in real-time
- A way to RANK vehicles by user preference
- A way to SEND results back to users

**The Solution:** Build a backend API (Application Programming Interface) - think of it as a waiter in a restaurant:
- **User (customer):** "I want a ride from A to B"
- **API (waiter):** Takes order, asks kitchen (ML models), brings back options
- **ML Models (kitchen):** Cooks up predictions and recommendations

---

## 2. Dynamic Pricing (The "Surge" Logic)

### What is Surge Pricing?

**Real-world analogy:** Movie tickets
- **Normal day (2 PM, Tuesday):** $10 ticket
- **Weekend night (8 PM, Saturday):** $15 ticket (50% surge)
- **Why?** More demand, same supply → higher price

### How We Calculate Surge

**Step 1: Demand-Supply Ratio**
```
Demand = How many people want rides (estimated from history)
Supply = How many cars are available right now
Ratio = Demand ÷ Supply
```

**Example:**
```
City center, 8 AM (rush hour):
- Estimated demand: 50 rides/hour
- Available cars: 5
- Ratio = 50 ÷ 5 = 10 (very high!)

Suburbs, 2 AM (late night):
- Estimated demand: 2 rides/hour
- Available cars: 10
- Ratio = 2 ÷ 10 = 0.2 (very low)
```

**Step 2: Map Ratio to Surge Multiplier**
```
Ratio < 0.5:     0.9× (discount - attract riders)
0.5 ≤ Ratio < 1.5:  1.0× (normal pricing)
1.5 ≤ Ratio < 3.0:  1.3× (moderate surge)
Ratio ≥ 3.0:     1.5× (high surge, capped)
```

**Step 3: Calculate Final Fare**
```
Base fare = $2.50 (economy car)
Distance cost = 5 km × $1.20/km = $6.00
Time cost = 15 min × $0.30/min = $4.50
Subtotal = $2.50 + $6.00 + $4.50 = $13.00

With 1.3× surge: $13.00 × 1.3 = $16.90
With 0.9× discount: $13.00 × 0.9 = $11.70
```

**Result:** Same trip costs $16.90 at rush hour, $11.70 at night (44% difference!)

### Fallback Logic (What if data is missing?)

**Problem:** What if we don't have demand data for a specific region/hour?

**Solution (3-tier fallback):**
1. **Try nearest hour:** No data for 8 AM? Try 7 AM or 9 AM
2. **Try city average:** No data for this region? Use average across all regions
3. **Use default:** Still nothing? Use 1.0× (normal pricing)

**Why this matters:** System never crashes, always gives a reasonable answer.

---

## 3. Vehicle Ranking (The "Recommendation" Logic)

### The Problem

You have 4 available cars:
- **CAR001:** Economy, 3 min away, $15
- **CAR002:** Sedan, 5 min away, $18
- **CAR003:** SUV, 2 min away, $22
- **CAR004:** Economy, 7 min away, $14

**Question:** Which car should we show first?

**Answer:** Depends on what the user wants!

### User Modes

**Fastest Mode (70% ETA, 20% cost, 10% comfort):**
- User is late for a meeting
- Ranking: CAR003 (2 min) → CAR001 (3 min) → CAR002 (5 min)

**Cheapest Mode (70% cost, 20% ETA, 10% comfort):**
- User is a student on a budget
- Ranking: CAR004 ($14) → CAR001 ($15) → CAR002 ($18)

**Balanced Mode (40% ETA, 40% cost, 20% comfort):**
- Regular commuter, wants good value
- Ranking: CAR001 (fast + cheap) → CAR003 (fastest) → CAR004 (cheapest)

### How Scoring Works

**Step 1: Normalize Scores (0-1 scale)**
```
ETA values: [3, 5, 2, 7] minutes
Normalized (lower is better):
- 2 min → 1.0 (best)
- 3 min → 0.8
- 5 min → 0.4
- 7 min → 0.0 (worst)

Cost values: [$15, $18, $22, $14]
Normalized (lower is better):
- $14 → 1.0 (best)
- $15 → 0.875
- $18 → 0.5
- $22 → 0.0 (worst)
```

**Step 2: Apply Weights**
```
Fastest mode for CAR001:
Score = (0.7 × 0.8) + (0.2 × 0.875) + (0.1 × 0.33)
      = 0.56 + 0.175 + 0.033
      = 0.768

Cheapest mode for CAR001:
Score = (0.2 × 0.8) + (0.7 × 0.875) + (0.1 × 0.33)
      = 0.16 + 0.6125 + 0.033
      = 0.805
```

**Result:** Same car gets different scores based on user preference!

---

## 4. FastAPI (The "Waiter" System)

### What is an API?

**Restaurant analogy:**
- **Menu:** List of things you can order (API endpoints)
- **Waiter:** Takes your order, brings food (API server)
- **Kitchen:** Prepares food (ML models, database)
- **You:** Customer making requests (user app)

### Our API Endpoints

**1. POST /vehicles/update**
```json
Request: "Hey, CAR001 is now at lat 40.75, lon -74.00, available"
Response: "Got it! You're in region 2_3, surge is 1.3×"
```

**2. POST /ride/quote**
```json
Request: "I want a ride from A to B, fastest mode"
Response: "Here are your top 3 options with prices and ETAs"
```

### Request-Response Flow

**User opens app and requests ride:**
```
1. User: "Ride from 40.75,-74.00 to 40.76,-73.99, fastest mode"
   ↓
2. API receives request, validates it
   ↓
3. API calculates distance: 1.5 km (Haversine formula)
   ↓
4. API predicts duration: 8.5 min (using ETA model)
   ↓
5. API determines region: "2_3" (city center)
   ↓
6. API calculates surge: 1.3× (high demand)
   ↓
7. API finds available cars within 5 km
   ↓
8. API calculates fare for each car
   ↓
9. API ranks cars by "fastest" mode
   ↓
10. API returns top 3 cars with details
```

**Response:**
```json
{
  "distance": 1.5,
  "duration": 8.5,
  "surge": 1.3,
  "vehicles": [
    {"id": "CAR003", "eta": 2, "fare": 12.50},
    {"id": "CAR001", "eta": 3, "fare": 11.20},
    {"id": "CAR002", "eta": 5, "fare": 13.80}
  ]
}
```

### Pydantic Validation (The "Bouncer")

**Problem:** Users might send bad data
```json
{"pickup": {"lat": 999, "lon": "hello"}}  // Invalid!
```

**Solution:** Pydantic checks every request
```python
class Location(BaseModel):
    lat: float  # Must be a number
    lon: float  # Must be a number
    
    # Validation rules
    @validator('lat')
    def lat_must_be_valid(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Invalid latitude')
        return v
```

**Result:** Bad requests get rejected with clear error messages.

---

## 5. Key Takeaways

**Dynamic Pricing:**
- Surge = Demand ÷ Supply
- Higher demand → higher price (up to 1.5× cap)
- Lower demand → discount (0.9×)
- Fallback logic prevents crashes

**Vehicle Ranking:**
- Different users want different things
- Normalize scores to 0-1 scale
- Apply weights based on user mode
- Top-k selection (show best 3)

**FastAPI:**
- Waiter between user and ML models
- Validates all requests (Pydantic)
- Fast response (< 200ms)
- Interactive docs (Swagger UI)

---

## 6. Testing It Yourself

**Start server:**
```bash
uvicorn api.main:app --reload
```

**Open browser:**
```
http://localhost:8000/docs
```

**Try it:**
1. Click on POST /ride/quote
2. Click "Try it out"
3. Enter pickup/drop coordinates
4. Select user mode
5. Click "Execute"
6. See ranked vehicles!

---

## 7. Common Questions

**Q: Why cap surge at 1.5×?**
A: Higher surge angers users → bad reviews → they switch to competitors.

**Q: Why normalize scores?**
A: ETA is in minutes, cost is in dollars. Can't compare directly. Normalization puts both on 0-1 scale.

**Q: Why 3 user modes?**
A: Different users have different priorities. One size doesn't fit all.

**Q: What if no vehicles available?**
A: API returns 404 error with message "No vehicles available in your area".

**Q: How fast is the API?**
A: < 200ms response time. Fast enough for real-time apps.

---

**Repository:** https://github.com/Karthiknayak26/AI_Vehicle_Matching.git  
**Status:** Day 3 Complete ✅
