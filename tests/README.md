# Test Suite Documentation

## Overview

Comprehensive automated test suite for the AI Vehicle Matching System.

## Test Files

### 1. test_distance.py (8 tests)
Tests Haversine distance calculation:
- Zero distance validation
- Known distance accuracy (NYC to Boston ≈ 306 km)
- Short distance precision (~1 km)
- Symmetry (A→B = B→A)
- Positive distance guarantee
- Equator distance test
- Large distance test (antipodal points)

### 2. test_pricing.py (15 tests)
Tests surge pricing logic:
- **CRITICAL:** Surge cap never exceeded
- Surge tier validation (discount/normal/moderate/high)
- Custom surge cap enforcement
- Demand-supply ratio calculation
- Zero vehicles handling
- Fare component validation
- Surge multiplier application
- Discount application
- Fallback logic for missing data

### 3. test_ranking.py (16 tests)
Tests vehicle ranking:
- **CRITICAL:** Ranking respects user preference
- Score normalization (0-1 range)
- Fastest mode prioritizes ETA
- Cheapest mode prioritizes cost
- Balanced mode uses equal weights
- Top-k selection accuracy
- Score sorting (descending)
- Different modes produce different rankings

### 4. test_api.py (18 tests)
Tests API endpoints:
- **CRITICAL:** Response schema compliance
- Request validation (Pydantic)
- Invalid status/type/coordinates rejection
- Surge multiplier range validation (0.9-1.5)
- Positive fare guarantee
- Vehicle scores in 0-1 range
- Health check endpoint
- Vehicle update endpoint
- Ride quote endpoint (all 3 user modes)

## Running Tests

### Run All Tests
```bash
python scripts/run_tests.py
```

### Run Specific Test File
```bash
pytest tests/test_distance.py -v
pytest tests/test_pricing.py -v
pytest tests/test_ranking.py -v
pytest tests/test_api.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov=api --cov-report=html
```

## Test Results

Test results are automatically saved to `reports/TEST_RESULTS.md` including:
- Test summary (passed/failed counts)
- Detailed results per test file
- ETA model performance metrics
- Test coverage breakdown
- Final conclusion

## Key Test Assertions

### Distance Calculation
- ✅ Accuracy within 5% tolerance for known distances
- ✅ Symmetry guaranteed
- ✅ Always positive

### Surge Pricing
- ✅ **Never exceeds cap (1.5×)**
- ✅ Correct tier assignment
- ✅ Fallback to default when data missing

### Vehicle Ranking
- ✅ **Different modes produce different rankings**
- ✅ Scores always in 0-1 range
- ✅ Sorted descending by score

### API
- ✅ **All responses follow schema**
- ✅ Invalid requests rejected (422 status)
- ✅ All fares positive
- ✅ Surge within valid range

## Dependencies

```
pytest>=7.0.0
httpx>=0.24.0  # For API testing
```

## Test Coverage

**Total Tests:** 57  
**Critical Tests:** 4 (marked with **CRITICAL**)

- Distance: 8 tests
- Pricing: 15 tests
- Ranking: 16 tests
- API: 18 tests

## Continuous Integration

To integrate with CI/CD:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python scripts/run_tests.py
```

## Notes

- Tests use pytest fixtures for setup/teardown
- API tests use FastAPI TestClient (no server needed)
- All tests are independent (no shared state)
- Tests run in < 10 seconds total
