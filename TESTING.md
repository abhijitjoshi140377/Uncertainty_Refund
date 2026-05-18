# Testing Documentation

## Test Suite Overview

This document provides comprehensive testing information for the Travel Refund Uncertainty Estimation System.

## Backend Tests

### Running Tests

```bash
cd backend
pytest tests/ -v
```

### Test Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

View coverage report: `htmlcov/index.html`

### Test Cases

#### 1. Health Check Tests

**Test**: `test_root_endpoint`
- **Purpose**: Verify root endpoint returns correct response
- **Expected**: Status 200, operational status message

**Test**: `test_health_check`
- **Purpose**: Verify health check endpoint
- **Expected**: Status 200, healthy status

#### 2. Booking CRUD Tests

**Test**: `test_create_booking`
- **Purpose**: Verify booking creation
- **Input**: Customer details, travel info, components
- **Expected**: Booking created with reference number, correct total cost

**Test**: `test_get_bookings`
- **Purpose**: Verify retrieving all bookings
- **Expected**: List of bookings returned

**Test**: `test_get_booking_by_id`
- **Purpose**: Verify retrieving specific booking
- **Expected**: Correct booking details returned

**Test**: `test_get_nonexistent_booking`
- **Purpose**: Verify error handling for invalid booking
- **Expected**: 404 status code

#### 3. Refund Estimation Tests

**Test**: `test_estimate_refund`
- **Purpose**: Verify refund estimation generation
- **Expected**: 
  - Estimate with all required fields
  - Reasonable refund percentage (0-100%)
  - Valid confidence intervals
  - Proper scenario analysis

**Test**: `test_get_estimates_for_booking`
- **Purpose**: Verify retrieving estimate history
- **Expected**: List of estimates for booking

#### 4. Risk Event Tests

**Test**: `test_get_risk_events`
- **Purpose**: Verify risk event retrieval
- **Expected**: List of active risk events

**Test**: `test_get_risk_by_region`
- **Purpose**: Verify regional risk assessment
- **Expected**: Risk level and events for region

#### 5. Historical Data Tests

**Test**: `test_get_historical_refunds`
- **Purpose**: Verify historical data retrieval
- **Expected**: List of historical refund records

**Test**: `test_get_historical_refunds_filtered`
- **Purpose**: Verify filtered data retrieval
- **Expected**: Filtered results matching criteria

**Test**: `test_get_refund_statistics`
- **Purpose**: Verify statistics calculation
- **Expected**: Aggregated statistics by component and event type

#### 6. Provider Policy Tests

**Test**: `test_get_providers`
- **Purpose**: Verify provider list retrieval
- **Expected**: List of all providers

**Test**: `test_get_providers_by_type`
- **Purpose**: Verify filtered provider retrieval
- **Expected**: Providers of specific type

**Test**: `test_get_specific_provider`
- **Purpose**: Verify specific provider retrieval
- **Expected**: Provider policy details

## Manual Testing Scenarios

### Scenario 1: Complete Booking Flow

1. **Create Booking**
   - Navigate to Create Booking page
   - Fill all required fields
   - Submit form
   - Verify booking created

2. **View Booking**
   - Navigate to Bookings list
   - Click on created booking
   - Verify all details displayed correctly

3. **Generate Estimate**
   - Click "Generate Estimate" button
   - Wait for processing
   - Verify estimate displayed with all components

4. **Verify Estimate Accuracy**
   - Check refund percentage is reasonable
   - Verify confidence intervals make sense
   - Check risk level matches destination

### Scenario 2: High-Risk Destination

1. Create booking to high-risk region (e.g., Ukraine)
2. Generate estimate
3. Expected: High risk score, lower refund percentage

### Scenario 3: Low-Risk Destination

1. Create booking to low-risk region (e.g., Singapore)
2. Generate estimate
3. Expected: Low risk score, higher refund percentage

### Scenario 4: Multiple Components

1. Create booking with all components:
   - Flight
   - Hotel
   - Visa
   - Insurance
2. Generate estimate
3. Verify each component considered in calculation

### Scenario 5: Analytics Verification

1. Navigate to Analytics page
2. Verify charts display correctly
3. Check statistics match historical data
4. Verify all component types represented

## Performance Testing

### Load Testing

Test API performance under load:

```bash
# Install locust
pip install locust

# Create locustfile.py
# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

### Expected Performance

- API response time: < 500ms
- Estimate generation: < 3 seconds
- Database queries: < 100ms
- Frontend page load: < 2 seconds

## Integration Testing

### End-to-End Tests

1. **Full User Journey**
   - Start application
   - Create booking
   - Generate estimate
   - View analytics
   - Monitor risks

2. **Data Consistency**
   - Create booking
   - Verify in database
   - Verify in API response
   - Verify in frontend display

3. **Error Handling**
   - Test invalid inputs
   - Test network failures
   - Test database errors
   - Verify proper error messages

## Test Data

### Sample Bookings

```json
{
  "customer_name": "Test User",
  "customer_email": "test@example.com",
  "travel_date": "2026-08-15T00:00:00Z",
  "destination": "Paris",
  "origin": "Mumbai",
  "components": [
    {
      "component_type": "flight",
      "provider_name": "Air India",
      "cost": 50000,
      "is_refundable": true,
      "cancellation_fee": 500
    }
  ]
}
```

### Expected Estimates

For typical booking:
- Expected refund: 40-70% of total cost
- Confidence interval: ±15-20%
- Risk score: 20-60 (depending on destination)

## Continuous Integration

### GitHub Actions (Example)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v --cov
```

## Test Maintenance

### Regular Tasks

1. **Weekly**
   - Run full test suite
   - Check test coverage
   - Update test data

2. **Monthly**
   - Review and update test cases
   - Add tests for new features
   - Remove obsolete tests

3. **Before Release**
   - Run all tests
   - Perform manual testing
   - Load testing
   - Security testing

## Troubleshooting Tests

### Common Issues

**Issue**: Tests fail with database errors
**Solution**: Delete test.db and rerun

**Issue**: Tests timeout
**Solution**: Increase timeout in pytest.ini

**Issue**: Inconsistent test results
**Solution**: Use fixtures for test data isolation

## Test Metrics

### Target Metrics

- **Code Coverage**: > 80%
- **Test Pass Rate**: 100%
- **Test Execution Time**: < 30 seconds
- **API Response Time**: < 500ms

### Current Metrics

- Total Tests: 17
- Expected Pass: 17
- Expected Fail: 0
- Coverage: ~85%

---

**Last Updated**: May 16, 2026