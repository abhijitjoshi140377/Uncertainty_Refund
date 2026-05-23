import requests
import json

# Backend API base URL
BASE_URL = "http://localhost:8000"

def test_endpoint(method, path, data=None, params=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{path}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        print(f"\n{'='*60}")
        print(f"Testing: {method} {path}")
        print(f"Status: {response.status_code}")
        
        # Print response (truncated if too long)
        response_text = json.dumps(response.json(), indent=2)
        if len(response_text) > 500:
            print(f"Response: {response_text[:500]}...")
        else:
            print(f"Response: {response_text}")
        
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"ERROR: {e}")
        return False

# Test all endpoints
tests = [
    ("GET", "/api/health", None, None),
    ("GET", "/api/bookings", None, {"skip": 0, "limit": 10}),
    ("POST", "/api/bookings", {
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "travel_date": "2026-06-15T10:00:00Z",
        "destination": "Paris",
        "origin": "New York",
        "components": [{
            "component_type": "flight",
            "provider_name": "Air France",
            "cost": 50000,
            "is_refundable": True,
            "cancellation_fee": 5000
        }]
    }, None),
    ("GET", "/api/bookings/1", None, None),
    ("POST", "/api/estimate-refund/1", {
        "selected_model": "auto",
        "severity": "high"
    }, None),
    ("GET", "/api/estimates/1", None, None),
    ("GET", "/api/risk-events", None, {"active_only": True}),
    ("GET", "/api/risk-events/region/Southeast Asia", None, None),
    ("GET", "/api/historical-refunds", None, {"limit": 10}),
    ("GET", "/api/statistics/refund-rates", None, None),
    ("GET", "/api/providers", None, None),
    ("GET", "/api/providers/Air India", None, None),
]

print("Starting API Tests...")
print("="*60)
print("Make sure backend is running: cd backend && python main.py")
print("="*60)

passed = 0
failed = 0

for method, path, data, params in tests:
    if test_endpoint(method, path, data, params):
        passed += 1
    else:
        failed += 1

print(f"\n{'='*60}")
print(f"Test Results: {passed} passed, {failed} failed")
print(f"{'='*60}")

if failed == 0:
    print("\nSUCCESS: All endpoints working!")
    print("Your MCP tools will work correctly.")
else:
    print(f"\nWARNING: {failed} endpoint(s) failed.")
    print("Check backend logs for errors.")

# Made with Bob
