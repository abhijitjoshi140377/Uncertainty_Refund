"""
Travel Refund Uncertainty Estimation System - Main Application
FastAPI backend with ML-powered refund prediction and MCP HTTP endpoint
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from models.database import init_db, get_db
from services.refund_estimator import RefundEstimator
from services.data_generator import generate_synthetic_data
from schemas import (
    BookingCreate, BookingResponse, RefundEstimateRequest, RefundEstimateResponse,
    RiskEventCreate, RiskEventResponse, HistoricalRefundResponse
)
import crud
from mcp_endpoint_simple import router as mcp_router

# Initialize FastAPI app
app = FastAPI(
    title="Travel Refund Uncertainty Estimation API",
    description="AI-powered refund prediction for force majeure events",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize refund estimator
estimator = RefundEstimator()

# Include MCP router for ICA integration
app.include_router(mcp_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database and load ML models on startup"""
    print("[STARTUP] Starting Travel Refund Uncertainty Estimation System...")
    init_db()
    print("[SUCCESS] Database initialized")
    
    # Generate synthetic data if database is empty
    db = next(get_db())
    if crud.get_bookings_count(db) == 0:
        print("[INFO] Generating synthetic data...")
        generate_synthetic_data(db)
        print("[SUCCESS] Synthetic data generated")
    
    print("[INFO] Loading ML models...")
    estimator.train_models(db)
    print("[SUCCESS] ML models loaded")
    print("[SUCCESS] System ready!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Travel Refund Uncertainty Estimation API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "refund-estimation-api",
        "timestamp": "2026-05-16T08:45:00Z"
    }


# Booking endpoints
@app.post("/api/bookings", response_model=BookingResponse)
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """Create a new travel booking"""
    return crud.create_booking(db, booking)


@app.get("/api/bookings", response_model=List[BookingResponse])
async def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all bookings"""
    return crud.get_bookings(db, skip=skip, limit=limit)


@app.get("/api/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking by ID"""
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# Refund estimation endpoints
@app.post("/api/estimate-refund/{booking_id}", response_model=RefundEstimateResponse)
async def estimate_refund(
    booking_id: int,
    request: RefundEstimateRequest = RefundEstimateRequest(),
    db: Session = Depends(get_db)
):
    """Generate refund estimate for a booking"""
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    estimate = estimator.estimate_refund(
        db,
        booking,
        selected_model=request.selected_model,
        calamity_type=request.calamity_type,
        severity=request.severity
    )
    return crud.create_refund_estimate(db, booking_id, estimate)


@app.get("/api/estimates/{booking_id}", response_model=List[RefundEstimateResponse])
async def get_estimates(booking_id: int, db: Session = Depends(get_db)):
    """Get all refund estimates for a booking"""
    return crud.get_refund_estimates(db, booking_id)


# Risk events endpoints
@app.get("/api/risk-events", response_model=List[RiskEventResponse])
async def get_risk_events(active_only: bool = True, db: Session = Depends(get_db)):
    """Get current risk events"""
    return crud.get_risk_events(db, active_only=active_only)


@app.post("/api/risk-events", response_model=RiskEventResponse)
async def create_risk_event(event: RiskEventCreate, db: Session = Depends(get_db)):
    """Create a new risk event"""
    return crud.create_risk_event(db, event.model_dump())


@app.get("/api/risk-events/region/{region}")
async def get_risk_by_region(region: str, db: Session = Depends(get_db)):
    """Get risk events for a specific region"""
    events = crud.get_risk_events_by_region(db, region)
    if not events:
        return {"region": region, "risk_level": "low", "events": []}
    
    # Calculate aggregate risk
    risk_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    max_severity = max([risk_scores.get(e.severity, 1) for e in events])
    severity_map = {1: "low", 2: "medium", 3: "high", 4: "critical"}
    
    return {
        "region": region,
        "risk_level": severity_map[max_severity],
        "events": events
    }


# Historical data endpoints
@app.get("/api/historical-refunds", response_model=List[HistoricalRefundResponse])
async def get_historical_refunds(
    component_type: str = None,
    event_type: str = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get historical refund data"""
    return crud.get_historical_refunds(db, component_type, event_type, limit)


@app.get("/api/statistics/refund-rates")
async def get_refund_statistics(db: Session = Depends(get_db)):
    """Get refund statistics by component type and event type"""
    return crud.get_refund_statistics(db)


# Provider policy endpoints
@app.get("/api/providers")
async def get_providers(provider_type: str = None, db: Session = Depends(get_db)):
    """Get provider policies"""
    return crud.get_providers(db, provider_type)


@app.get("/api/providers/{provider_name}")
async def get_provider_policy(provider_name: str, db: Session = Depends(get_db)):
    """Get specific provider policy"""
    policy = crud.get_provider_policy(db, provider_name)
    if not policy:
        raise HTTPException(status_code=404, detail="Provider not found")
    return policy


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Made with Bob
