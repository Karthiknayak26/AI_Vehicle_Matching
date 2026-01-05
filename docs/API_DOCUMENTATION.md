# AI Vehicle Matching API Documentation

## Overview

The AI Vehicle Matching API provides intelligent vehicle recommendations and dynamic pricing for ride-hailing platforms.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required (development mode).

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check API health and model status.

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": {
    "demand_model": true,
    "eta_model": true,
    "scaler": true
  },
  "vehicles_registered": 5
}
```

---

### 2. Update Vehicle

**POST** `/vehicles/update`

Update vehicle location and status.

**Request Body:**
```json
{
  "vehicle_id": "CAR001",
  "location": {
    "lat": 40.7500,
    "lon": -74.0000
  },
  "status": "available",
  "vehicle_type": "economy"
}
```

**Parameters:**
- `vehicle_id` (string, required): Unique vehicle identifier
- `location` (object, required):
  - `lat` (float, -90 to 90): Latitude
  - `lon` (float, -180 to 180): Longitude
- `status` (string, required): One of `available`, `busy`, `offline`
- `vehicle_type` (string, required): One of `economy`, `sedan`, `suv`

**Response:**
```json
{
  "vehicle_id": "CAR001",
  "updated": true,
  "region_id": "2_3",
  "nearby_requests": 5,
  "current_surge": 1.3
}
```

---

### 3. Get Ride Quote

**POST** `/ride/quote`

Get ride quote with ranked vehicle recommendations.

**Request Body:**
```json
{
  "pickup": {
    "lat": 40.7500,
    "lon": -74.0000
  },
  "drop": {
    "lat": 40.7600,
    "lon": -73.9900
  },
  "timestamp": "2024-01-15T08:30:00",
  "user_mode": "balanced"
}
```

**Parameters:**
- `pickup` (object, required): Pickup location
  - `lat` (float): Latitude
  - `lon` (float): Longitude
- `drop` (object, required): Drop location
  - `lat` (float): Latitude
  - `lon` (float): Longitude
- `timestamp` (string, optional): ISO format timestamp (default: now)
- `user_mode` (string, optional): One of `fastest`, `cheapest`, `balanced` (default: `balanced`)

**Response:**
```json
{
  "request_id": "REQ_20240115083000_1234",
  "pickup": {
    "lat": 40.7500,
    "lon": -74.0000
  },
  "drop": {
    "lat": 40.7600,
    "lon": -73.9900
  },
  "distance": 1.52,
  "estimated_duration": 8.5,
  "surge_multiplier": 1.3,
  "surge_reason": "Calculated from demand-supply ratio (2.45)",
  "available_vehicles": [
    {
      "vehicle_id": "CAR001",
      "vehicle_type": "economy",
      "eta_pickup": 3.2,
      "eta_trip": 8.5,
      "fare_breakdown": {
        "base_fare": 2.50,
        "distance_cost": 1.82,
        "time_cost": 2.55,
        "subtotal": 6.87,
        "surge_multiplier": 1.3,
        "final_fare": 8.93
      },
      "final_fare": 8.93,
      "score": 0.875
    }
  ]
}
```

---

## User Modes

### Fastest Mode
- **Priority:** Minimize pickup + trip time
- **Weights:** 70% ETA, 20% cost, 10% comfort
- **Use case:** User is late for a meeting

### Cheapest Mode
- **Priority:** Minimize cost
- **Weights:** 70% cost, 20% ETA, 10% comfort
- **Use case:** Budget-conscious rider

### Balanced Mode
- **Priority:** Balance between speed and cost
- **Weights:** 40% ETA, 40% cost, 20% comfort
- **Use case:** Regular commute

---

## Surge Pricing

Surge multipliers are calculated based on demand-supply ratio:

| Demand-Supply Ratio | Surge Multiplier | Description |
|---------------------|------------------|-------------|
| < 0.5               | 0.9×             | Low demand (10% discount) |
| 0.5 - 1.5           | 1.0×             | Normal pricing |
| 1.5 - 3.0           | 1.3×             | Moderate surge (30% increase) |
| ≥ 3.0               | 1.5×             | High surge (50% increase, capped) |

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid timestamp format"
}
```

### 404 Not Found
```json
{
  "detail": "No vehicles available in your area"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "vehicle_type"],
      "msg": "string does not match regex",
      "type": "value_error.str.regex"
    }
  ]
}
```

---

## Running the API

### Start Server

```bash
# Method 1: Direct
python api/main.py

# Method 2: Using uvicorn
uvicorn api.main:app --reload

# Method 3: With custom host/port
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Test API

```bash
# Run test suite
python scripts/test_api.py

# Or use curl
curl -X POST http://localhost:8000/ride/quote \
  -H "Content-Type: application/json" \
  -d '{
    "pickup": {"lat": 40.75, "lon": -74.00},
    "drop": {"lat": 40.76, "lon": -73.99},
    "user_mode": "fastest"
  }'
```

### Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Example Workflow

1. **Register vehicles:**
   ```bash
   POST /vehicles/update (for each vehicle)
   ```

2. **User requests ride:**
   ```bash
   POST /ride/quote
   ```

3. **System responds with:**
   - Trip distance and duration
   - Current surge multiplier
   - Top 3 vehicle options ranked by user preference

4. **User selects vehicle** (frontend implementation)

5. **Driver accepts** (not yet implemented)

---

## Rate Limits

Currently no rate limits (development mode).

In production, consider:
- 100 requests/minute per IP
- 1000 requests/hour per API key

---

## Future Enhancements

- [ ] Driver acceptance prediction
- [ ] Real-time traffic integration
- [ ] Multi-stop rides
- [ ] Scheduled rides
- [ ] Ride pooling
- [ ] Payment integration
- [ ] Authentication & authorization
- [ ] WebSocket for real-time updates
