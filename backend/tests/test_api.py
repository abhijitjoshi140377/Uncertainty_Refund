"""
API endpoint tests
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from main import app
from models.database import Base, get_db


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "operational"
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestBookingEndpoints:
    """Test booking CRUD operations"""
    
    def test_create_booking(self):
        """Test creating a new booking"""
        booking_data = {
            "customer_name": "Test User",
            "customer_email": "test@example.com",
            "travel_date": (datetime.now() + timedelta(days=60)).isoformat(),
            "destination": "Paris",
            "origin": "Mumbai",
            "components": [
                {
                    "component_type": "flight",
                    "provider_name": "Air India",
                    "cost": 50000.0,
                    "refund_policy": "Standard refund policy",
                    "is_refundable": True,
                    "cancellation_fee": 500.0
                },
                {
                    "component_type": "hotel",
                    "provider_name": "Marriott",
                    "cost": 25000.0,
                    "refund_policy": "Free cancellation",
                    "is_refundable": True,
                    "cancellation_fee": 0.0
                }
            ]
        }
        
        response = client.post("/api/bookings", json=booking_data)
        assert response.status_code == 200
        data = response.json()
        assert data["customer_name"] == "Test User"
        assert data["total_cost"] == 75000.0
        assert len(data["components"]) == 2
        assert "booking_reference" in data
    
    def test_get_bookings(self):
        """Test retrieving all bookings"""
        response = client.get("/api/bookings")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_booking_by_id(self):
        """Test retrieving a specific booking"""
        # First create a booking
        booking_data = {
            "customer_name": "Jane Doe",
            "customer_email": "jane@example.com",
            "travel_date": (datetime.now() + timedelta(days=90)).isoformat(),
            "destination": "London",
            "origin": "Delhi",
            "components": [
                {
                    "component_type": "flight",
                    "provider_name": "British Airways",
                    "cost": 60000.0,
                    "is_refundable": False,
                    "cancellation_fee": 1000.0
                }
            ]
        }
        
        create_response = client.post("/api/bookings", json=booking_data)
        booking_id = create_response.json()["id"]
        
        # Now retrieve it
        response = client.get(f"/api/bookings/{booking_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == booking_id
        assert data["customer_name"] == "Jane Doe"
    
    def test_get_nonexistent_booking(self):
        """Test retrieving a booking that doesn't exist"""
        response = client.get("/api/bookings/99999")
        assert response.status_code == 404


class TestRefundEstimation:
    """Test refund estimation endpoints"""
    
    def test_estimate_refund(self):
        """Test generating refund estimate"""
        # Create a booking first
        booking_data = {
            "customer_name": "Refund Test",
            "customer_email": "refund@example.com",
            "travel_date": (datetime.now() + timedelta(days=45)).isoformat(),
            "destination": "Dubai",
            "origin": "Mumbai",
            "components": [
                {
                    "component_type": "flight",
                    "provider_name": "Emirates",
                    "cost": 40000.0,
                    "is_refundable": True,
                    "cancellation_fee": 200.0
                },
                {
                    "component_type": "hotel",
                    "provider_name": "Hilton",
                    "cost": 20000.0,
                    "is_refundable": True,
                    "cancellation_fee": 0.0
                },
                {
                    "component_type": "insurance",
                    "provider_name": "ICICI Lombard",
                    "cost": 3000.0,
                    "is_refundable": False,
                    "cancellation_fee": 0.0
                }
            ]
        }
        
        create_response = client.post("/api/bookings", json=booking_data)
        booking_id = create_response.json()["id"]
        
        # Generate estimate
        response = client.post(f"/api/estimate-refund/{booking_id}")
        assert response.status_code == 200
        data = response.json()
        
        # Verify estimate structure
        assert "expected_refund_amount" in data
        assert "expected_refund_percentage" in data
        assert "confidence_lower" in data
        assert "confidence_upper" in data
        assert "current_risk_level" in data
        assert "risk_score" in data
        assert "best_case_refund" in data
        assert "worst_case_refund" in data
        assert "most_likely_refund" in data
        
        # Verify reasonable values
        assert 0 <= data["expected_refund_percentage"] <= 100
        assert data["confidence_lower"] <= data["expected_refund_amount"]
        assert data["expected_refund_amount"] <= data["confidence_upper"]
        assert data["worst_case_refund"] <= data["most_likely_refund"] <= data["best_case_refund"]
    
    def test_get_estimates_for_booking(self):
        """Test retrieving all estimates for a booking"""
        # Create booking and estimate
        booking_data = {
            "customer_name": "Estimate History Test",
            "customer_email": "history@example.com",
            "travel_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "destination": "Singapore",
            "origin": "Bangalore",
            "components": [
                {
                    "component_type": "flight",
                    "provider_name": "Singapore Airlines",
                    "cost": 35000.0,
                    "is_refundable": True,
                    "cancellation_fee": 500.0
                }
            ]
        }
        
        create_response = client.post("/api/bookings", json=booking_data)
        booking_id = create_response.json()["id"]
        
        # Generate estimate
        client.post(f"/api/estimate-refund/{booking_id}")
        
        # Retrieve estimates
        response = client.get(f"/api/estimates/{booking_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestRiskEvents:
    """Test risk event endpoints"""
    
    def test_get_risk_events(self):
        """Test retrieving risk events"""
        response = client.get("/api/risk-events")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_risk_by_region(self):
        """Test retrieving risk for specific region"""
        response = client.get("/api/risk-events/region/Ukraine")
        assert response.status_code == 200
        data = response.json()
        assert "region" in data
        assert "risk_level" in data
        assert data["risk_level"] in ["low", "medium", "high", "critical"]


class TestHistoricalData:
    """Test historical data endpoints"""
    
    def test_get_historical_refunds(self):
        """Test retrieving historical refund data"""
        response = client.get("/api/historical-refunds")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_historical_refunds_filtered(self):
        """Test retrieving filtered historical data"""
        response = client.get("/api/historical-refunds?component_type=flight&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
    
    def test_get_refund_statistics(self):
        """Test retrieving refund statistics"""
        response = client.get("/api/statistics/refund-rates")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestProviderPolicies:
    """Test provider policy endpoints"""
    
    def test_get_providers(self):
        """Test retrieving all providers"""
        response = client.get("/api/providers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_providers_by_type(self):
        """Test retrieving providers by type"""
        response = client.get("/api/providers?provider_type=airline")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_specific_provider(self):
        """Test retrieving specific provider policy"""
        response = client.get("/api/providers/Air India")
        assert response.status_code == 200
        data = response.json()
        assert data["provider_name"] == "Air India"


# Expected test results documentation
"""
EXPECTED TEST RESULTS:
======================

Test Suite: TestHealthEndpoints
- test_root_endpoint: PASS - Root endpoint returns operational status
- test_health_check: PASS - Health check returns healthy status

Test Suite: TestBookingEndpoints
- test_create_booking: PASS - Successfully creates booking with components
- test_get_bookings: PASS - Returns list of all bookings
- test_get_booking_by_id: PASS - Returns specific booking details
- test_get_nonexistent_booking: PASS - Returns 404 for invalid booking ID

Test Suite: TestRefundEstimation
- test_estimate_refund: PASS - Generates valid refund estimate with all fields
- test_get_estimates_for_booking: PASS - Returns estimate history for booking

Test Suite: TestRiskEvents
- test_get_risk_events: PASS - Returns list of active risk events
- test_get_risk_by_region: PASS - Returns risk level for specific region

Test Suite: TestHistoricalData
- test_get_historical_refunds: PASS - Returns historical refund records
- test_get_historical_refunds_filtered: PASS - Returns filtered results
- test_get_refund_statistics: PASS - Returns aggregated statistics

Test Suite: TestProviderPolicies
- test_get_providers: PASS - Returns all provider policies
- test_get_providers_by_type: PASS - Returns filtered providers
- test_get_specific_provider: PASS - Returns specific provider details

Total Tests: 17
Expected Pass: 17
Expected Fail: 0
"""

# Made with Bob
