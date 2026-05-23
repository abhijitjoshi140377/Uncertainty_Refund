"""
Travel Refund Uncertainty Estimation System - Enhanced Main Application
FastAPI backend with ML-powered refund prediction
Enhanced with proper REST standards, error handling, and OpenAPI documentation
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uvicorn

from models.database import init_db, get_db
from services.refund_estimator import RefundEstimator
from services.data_generator import generate_synthetic_data
from schemas_enhanced import (
    # Response wrappers
    APIResponse, ErrorResponse, ErrorDetail, PaginatedResponse, HealthCheckResponse,
    # Booking schemas
    BookingCreate, BookingResponse,
    # Refund schemas
    RefundEstimateRequest, RefundEstimateResponse,
    # Risk schemas
    RiskEventCreate, RiskEventResponse, RegionalRiskResponse,
    # Historical data schemas
    HistoricalRefundResponse, RefundStatistics,
    # Provider schemas
    ProviderPolicyResponse,
    # Enums
    ComponentType, EventType, SeverityLevel
)
import crud

# Initialize FastAPI app with enhanced metadata
app = FastAPI(
    title="Travel Refund Uncertainty Estimation API",
    description="""
    ## AI-Powered Refund Prediction for Force Majeure Events
    
    This API provides intelligent refund estimation for travel bookings affected by force majeure events
    such as wars, pandemics, natural disasters, and political unrest.
    
    ### Features
    * **ML-Powered Predictions**: Uses ensemble machine learning models for accurate refund estimation
    * **Confidence Intervals**: Provides 95% confidence intervals for all predictions
    * **Risk Assessment**: Real-time global risk event monitoring
    * **Historical Analysis**: Access to historical refund data for trend analysis
    * **Provider Policies**: Comprehensive database of provider refund policies
    
    ### Authentication
    Currently, this API does not require authentication. For production use, implement OAuth2 or API key authentication.
    
    ### Rate Limiting
    No rate limiting is currently enforced. Consider implementing rate limiting for production use.
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    contact={
        "name": "Abhijit Joshi",
        "url": "https://github.com/abhijitjoshi140377/Uncertainty_Refund",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize refund estimator
estimator = RefundEstimator()


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors with consistent format"""
    errors = []
    for error in exc.errors():
        errors.append(ErrorDetail(
            field=".".join(str(loc) for loc in error["loc"]),
            message=error["msg"],
            type=error["type"]
        ))
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            status="error",
            message="Validation failed",
            errors=errors
        ).model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with consistent format"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status="error",
            message=exc.detail
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected errors"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            status="error",
            message="An unexpected error occurred. Please try again later."
        ).model_dump()
    )


@app.on_event("startup")
async def startup_event():
    """Initialize database and load ML models on startup"""
    print("🚀 Starting Travel Refund Uncertainty Estimation System...")
    init_db()
    print("✅ Database initialized")
    
    # Generate synthetic data if database is empty
    db = next(get_db())
    if crud.get_bookings_count(db) == 0:
        print("📊 Generating synthetic data...")
        generate_synthetic_data(db)
        print("✅ Synthetic data generated")
    
    print("🤖 Loading ML models...")
    estimator.train_models(db)
    print("✅ ML models loaded")
    print("🎉 System ready!")


# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Get basic API information and links to documentation"
)
async def root():
    """
    Root endpoint providing API information.
    
    Returns basic API metadata and links to interactive documentation.
    """
    return APIResponse(
        status="success",
        message="Travel Refund Uncertainty Estimation API",
        data={
            "version": "1.0.0",
            "status": "operational",
            "docs": "/api/docs",
            "redoc": "/api/redoc"
        }
    )


# Health check endpoint
@app.get(
    "/api/health",
    response_model=APIResponse[HealthCheckResponse],
    tags=["Health"],
    summary="Health Check",
    description="Check API health status and get service information",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Service is healthy",
                        "data": {
                            "status": "healthy",
                            "service": "refund-estimation-api",
                            "version": "1.0.0",
                            "timestamp": "2026-05-20T10:00:00Z"
                        }
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current health status of the API service along with
    service metadata and current timestamp.
    
    **Use this endpoint to:**
    - Monitor service availability
    - Check API version
    - Verify service is responding
    """
    return APIResponse(
        status="success",
        message="Service is healthy",
        data=HealthCheckResponse(
            status="healthy",
            service="refund-estimation-api",
            version="1.0.0",
            timestamp=datetime.utcnow()
        )
    )


# Booking endpoints
@app.post(
    "/api/bookings",
    response_model=APIResponse[BookingResponse],
    status_code=status.HTTP_201_CREATED,
    tags=["Bookings"],
    summary="Create New Booking",
    description="Create a new travel booking with multiple components (flight, hotel, visa, insurance)",
    responses={
        201: {
            "description": "Booking created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Booking created successfully",
                        "data": {
                            "id": 1,
                            "booking_reference": "BK12345678",
                            "customer_name": "John Doe",
                            "total_cost": 75000
                        }
                    }
                }
            }
        },
        422: {"description": "Validation error", "model": ErrorResponse}
    }
)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new travel booking.
    
    **Request Body:**
    - **customer_name**: Customer's full name (2-100 characters)
    - **customer_email**: Valid email address
    - **travel_date**: Travel date in ISO 8601 format
    - **destination**: Destination city/country
    - **origin**: Origin city/country
    - **components**: List of booking components (at least 1 required)
    
    **Each component includes:**
    - **component_type**: flight, hotel, visa, or insurance
    - **provider_name**: Service provider name
    - **cost**: Component cost (must be positive)
    - **is_refundable**: Whether component is refundable
    - **cancellation_fee**: Cancellation fee amount
    
    **Returns:**
    - Booking details with unique booking reference
    - Total cost calculated from all components
    - Booking status set to 'active'
    """
    try:
        created_booking = crud.create_booking(db, booking)
        return APIResponse(
            status="success",
            message=f"Booking created successfully with reference {created_booking.booking_reference}",
            data=created_booking
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create booking: {str(e)}"
        )


@app.get(
    "/api/bookings",
    response_model=PaginatedResponse[BookingResponse],
    tags=["Bookings"],
    summary="Get All Bookings",
    description="Retrieve all bookings with pagination support",
    responses={
        200: {
            "description": "List of bookings retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Retrieved 10 bookings",
                        "data": [],
                        "total": 50,
                        "skip": 0,
                        "limit": 10
                    }
                }
            }
        }
    }
)
async def get_bookings(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all bookings with pagination.
    
    **Query Parameters:**
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 1000)
    
    **Returns:**
    - List of bookings with full details
    - Total count of all bookings
    - Pagination metadata
    
    **Use Cases:**
    - Display bookings list in UI
    - Export booking data
    - Search and filter bookings
    """
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    total = crud.get_bookings_count(db)
    
    return PaginatedResponse(
        status="success",
        message=f"Retrieved {len(bookings)} bookings",
        data=bookings,
        total=total,
        skip=skip,
        limit=limit
    )


@app.get(
    "/api/bookings/{booking_id}",
    response_model=APIResponse[BookingResponse],
    tags=["Bookings"],
    summary="Get Booking Details",
    description="Retrieve detailed information about a specific booking",
    responses={
        200: {"description": "Booking details retrieved successfully"},
        404: {
            "description": "Booking not found",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Booking with ID 999 not found"
                    }
                }
            }
        }
    }
)
async def get_booking(
    booking_id: int = Path(..., gt=0, description="Unique booking ID"),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific booking.
    
    **Path Parameters:**
    - **booking_id**: Unique booking ID (must be positive integer)
    
    **Returns:**
    - Complete booking details including:
      - Customer information
      - Travel dates and destinations
      - All booking components
      - Total cost and status
      - Booking reference
    
    **Errors:**
    - **404**: Booking not found
    """
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID {booking_id} not found"
        )
    
    return APIResponse(
        status="success",
        message="Booking retrieved successfully",
        data=booking
    )


# Refund estimation endpoints
@app.post(
    "/api/estimate-refund/{booking_id}",
    response_model=APIResponse[RefundEstimateResponse],
    tags=["Refund Estimation"],
    summary="Generate Refund Estimate",
    description="Generate AI-powered refund estimate for a booking considering force majeure events",
    responses={
        200: {
            "description": "Refund estimate generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Refund estimate generated successfully",
                        "data": {
                            "expected_refund_amount": 37500,
                            "expected_refund_percentage": 50.0,
                            "confidence_lower": 30000,
                            "confidence_upper": 45000,
                            "risk_score": 75.5
                        }
                    }
                }
            }
        },
        404: {"description": "Booking not found", "model": ErrorResponse}
    }
)
async def estimate_refund(
    booking_id: int = Path(..., gt=0, description="Booking ID to estimate refund for"),
    request: RefundEstimateRequest = RefundEstimateRequest(),
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered refund estimate for a booking.
    
    **Path Parameters:**
    - **booking_id**: ID of the booking to estimate refund for
    
    **Request Body (Optional):**
    - **selected_model**: ML model to use (auto, random_forest, gradient_boosting, rule_based)
    - **calamity_type**: Type of force majeure event (auto for automatic detection)
    - **severity**: Event severity level (low, medium, high, critical)
    
    **Returns:**
    - **expected_refund_amount**: Most likely refund amount
    - **expected_refund_percentage**: Refund as percentage of total cost
    - **confidence_lower/upper**: 95% confidence interval bounds
    - **risk_score**: Current risk score (0-100)
    - **best_case_refund**: Maximum possible refund
    - **worst_case_refund**: Minimum possible refund
    - **most_likely_refund**: Most probable refund amount
    - **model_version**: ML model version used
    - **prediction_confidence**: Model's confidence in prediction
    
    **How it works:**
    1. Analyzes booking components and costs
    2. Checks current global risk events
    3. Applies ML models trained on historical data
    4. Calculates confidence intervals using statistical methods
    5. Provides scenario analysis (best/worst/likely cases)
    
    **Errors:**
    - **404**: Booking not found
    - **500**: Estimation failed
    """
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID {booking_id} not found"
        )
    
    try:
        estimate = estimator.estimate_refund(
            db,
            booking,
            selected_model=request.selected_model,
            calamity_type=request.calamity_type,
            severity=request.severity
        )
        created_estimate = crud.create_refund_estimate(db, booking_id, estimate)
        
        return APIResponse(
            status="success",
            message="Refund estimate generated successfully",
            data=created_estimate
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate estimate: {str(e)}"
        )


@app.get(
    "/api/estimates/{booking_id}",
    response_model=APIResponse[List[RefundEstimateResponse]],
    tags=["Refund Estimation"],
    summary="Get Refund Estimates History",
    description="Retrieve all refund estimates generated for a specific booking",
    responses={
        200: {"description": "Estimates retrieved successfully"},
        404: {"description": "Booking not found", "model": ErrorResponse}
    }
)
async def get_estimates(
    booking_id: int = Path(..., gt=0, description="Booking ID"),
    db: Session = Depends(get_db)
):
    """
    Get all refund estimates for a booking.
    
    **Path Parameters:**
    - **booking_id**: Booking ID to get estimates for
    
    **Returns:**
    - List of all estimates generated for the booking
    - Ordered by estimate date (newest first)
    
    **Use Cases:**
    - Track estimate history over time
    - Compare estimates with different parameters
    - Analyze estimate accuracy
    """
    # Verify booking exists
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID {booking_id} not found"
        )
    
    estimates = crud.get_refund_estimates(db, booking_id)
    return APIResponse(
        status="success",
        message=f"Retrieved {len(estimates)} estimates for booking {booking_id}",
        data=estimates
    )


# Risk events endpoints
@app.get(
    "/api/risk-events",
    response_model=APIResponse[List[RiskEventResponse]],
    tags=["Risk Events"],
    summary="Get Risk Events",
    description="Retrieve current global risk events (wars, pandemics, natural disasters, etc.)",
    responses={
        200: {"description": "Risk events retrieved successfully"}
    }
)
async def get_risk_events(
    active_only: bool = Query(default=True, description="Return only active events"),
    db: Session = Depends(get_db)
):
    """
    Get current global risk events.
    
    **Query Parameters:**
    - **active_only**: If true, return only active events (default: true)
    
    **Returns:**
    - List of risk events with:
      - Event type (war, pandemic, natural_disaster, etc.)
      - Severity level (low, medium, high, critical)
      - Affected region
      - Start and end dates
      - Description
      - Active status
    
    **Use Cases:**
    - Monitor global risks
    - Assess travel safety
    - Predict refund likelihood
    - Display risk warnings to users
    """
    events = crud.get_risk_events(db, active_only=active_only)
    return APIResponse(
        status="success",
        message=f"Retrieved {len(events)} risk events",
        data=events
    )


@app.post(
    "/api/risk-events",
    response_model=APIResponse[RiskEventResponse],
    status_code=status.HTTP_201_CREATED,
    tags=["Risk Events"],
    summary="Create Risk Event",
    description="Create a new risk event (admin operation)",
    responses={
        201: {"description": "Risk event created successfully"},
        422: {"description": "Validation error", "model": ErrorResponse}
    }
)
async def create_risk_event(
    event: RiskEventCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new risk event.
    
    **Request Body:**
    - **event_type**: Type of event (war, pandemic, natural_disaster, etc.)
    - **severity**: Severity level (low, medium, high, critical)
    - **affected_region**: Region or country affected
    - **start_date**: Event start date
    - **end_date**: Event end date (optional)
    - **description**: Event description (optional)
    - **is_active**: Whether event is currently active (default: true)
    
    **Returns:**
    - Created risk event with unique ID
    
    **Note:** This endpoint should be restricted to admin users in production.
    """
    try:
        created_event = crud.create_risk_event(db, event.model_dump())
        return APIResponse(
            status="success",
            message="Risk event created successfully",
            data=created_event
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create risk event: {str(e)}"
        )


@app.get(
    "/api/risk-events/region/{region}",
    response_model=APIResponse[RegionalRiskResponse],
    tags=["Risk Events"],
    summary="Get Regional Risk Assessment",
    description="Get risk assessment for a specific region or country",
    responses={
        200: {"description": "Regional risk assessment retrieved successfully"}
    }
)
async def get_risk_by_region(
    region: str = Path(..., min_length=2, max_length=100, description="Region or country name"),
    db: Session = Depends(get_db)
):
    """
    Get risk assessment for a specific region.
    
    **Path Parameters:**
    - **region**: Region or country name (e.g., "Ukraine", "Paris", "Asia")
    
    **Returns:**
    - **region**: Region name
    - **risk_level**: Aggregate risk level (low, medium, high, critical)
    - **events**: List of active events in the region
    
    **Risk Level Calculation:**
    - Takes the maximum severity of all active events in the region
    - Returns "low" if no active events found
    
    **Use Cases:**
    - Check destination safety before booking
    - Display risk warnings
    - Adjust refund estimates based on regional risk
    """
    events = crud.get_risk_events_by_region(db, region)
    
    if not events:
        return APIResponse(
            status="success",
            message=f"No active risk events found for {region}",
            data=RegionalRiskResponse(
                region=region,
                risk_level=SeverityLevel.LOW,
                events=[]
            )
        )
    
    # Calculate aggregate risk
    risk_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    max_severity = max([risk_scores.get(e.severity, 1) for e in events])
    severity_map = {1: SeverityLevel.LOW, 2: SeverityLevel.MEDIUM, 3: SeverityLevel.HIGH, 4: SeverityLevel.CRITICAL}
    
    return APIResponse(
        status="success",
        message=f"Retrieved risk assessment for {region}",
        data=RegionalRiskResponse(
            region=region,
            risk_level=severity_map[max_severity],
            events=events
        )
    )


# Historical data endpoints
@app.get(
    "/api/historical-refunds",
    response_model=APIResponse[List[HistoricalRefundResponse]],
    tags=["Historical Data"],
    summary="Get Historical Refund Data",
    description="Retrieve historical refund data for analysis and trend identification",
    responses={
        200: {"description": "Historical data retrieved successfully"}
    }
)
async def get_historical_refunds(
    component_type: Optional[ComponentType] = Query(None, description="Filter by component type"),
    event_type: Optional[EventType] = Query(None, description="Filter by event type"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum records to return"),
    db: Session = Depends(get_db)
):
    """
    Get historical refund data.
    
    **Query Parameters:**
    - **component_type**: Filter by component (flight, hotel, visa, insurance)
    - **event_type**: Filter by event (war, pandemic, natural_disaster, etc.)
    - **limit**: Maximum records to return (default: 100, max: 1000)
    
    **Returns:**
    - List of historical refund records with:
      - Component and provider details
      - Original cost and refund amount
      - Event type and severity
      - Force majeure status
      - Insurance status
      - Days before travel when cancelled
    
    **Use Cases:**
    - Analyze refund trends
    - Train ML models
    - Generate statistics
    - Provide insights to users
    """
    refunds = crud.get_historical_refunds(db, component_type, event_type, limit)
    return APIResponse(
        status="success",
        message=f"Retrieved {len(refunds)} historical refund records",
        data=refunds
    )


@app.get(
    "/api/statistics/refund-rates",
    response_model=APIResponse[List[RefundStatistics]],
    tags=["Historical Data"],
    summary="Get Refund Statistics",
    description="Get aggregated refund statistics by component type and event type",
    responses={
        200: {"description": "Statistics retrieved successfully"}
    }
)
async def get_refund_statistics(db: Session = Depends(get_db)):
    """
    Get aggregated refund statistics.
    
    **Returns:**
    - Statistics grouped by component type and event type:
      - Average refund percentage
      - Total number of cases
      - Number of force majeure cases
      - Average refund amount
    
    **Use Cases:**
    - Display statistics dashboard
    - Analyze refund patterns
    - Compare refund rates across components
    - Identify high-risk scenarios
    """
    stats = crud.get_refund_statistics(db)
    return APIResponse(
        status="success",
        message=f"Retrieved statistics for {len(stats)} categories",
        data=stats
    )


# Provider policy endpoints
@app.get(
    "/api/providers",
    response_model=APIResponse[List[ProviderPolicyResponse]],
    tags=["Provider Policies"],
    summary="Get Provider Policies",
    description="Retrieve refund policies for travel service providers",
    responses={
        200: {"description": "Provider policies retrieved successfully"}
    }
)
async def get_providers(
    provider_type: Optional[ComponentType] = Query(None, description="Filter by provider type"),
    db: Session = Depends(get_db)
):
    """
    Get provider refund policies.
    
    **Query Parameters:**
    - **provider_type**: Filter by type (flight, hotel, visa, insurance)
    
    **Returns:**
    - List of provider policies with:
      - Provider name and type
      - Standard refund percentage
      - Force majeure refund percentage
      - Cancellation fees
      - Processing time
      - Policy text and clauses
    
    **Use Cases:**
    - Display provider policies to users
    - Compare refund policies
    - Calculate expected refunds
    - Inform booking decisions
    """
    providers = crud.get_providers(db, provider_type)
    return APIResponse(
        status="success",
        message=f"Retrieved {len(providers)} provider policies",
        data=providers
    )


@app.get(
    "/api/providers/{provider_name}",
    response_model=APIResponse[ProviderPolicyResponse],
    tags=["Provider Policies"],
    summary="Get Provider Policy",
    description="Get detailed refund policy for a specific provider",
    responses={
        200: {"description": "Provider policy retrieved successfully"},
        404: {"description": "Provider not found", "model": ErrorResponse}
    }
)
async def get_provider_policy(
    provider_name: str = Path(..., min_length=2, max_length=100, description="Provider name"),
    db: Session = Depends(get_db)
):
    """
    Get specific provider policy.
    
    **Path Parameters:**
    - **provider_name**: Name of the provider (e.g., "Air India", "Marriott")
    
    **Returns:**
    - Complete provider policy details including:
      - Refund percentages (standard and force majeure)
      - Cancellation fees
      - Processing time
      - Full policy text
      - Force majeure clause
      - Last update date
    
    **Errors:**
    - **404**: Provider not found
    """
    policy = crud.get_provider_policy(db, provider_name)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider '{provider_name}' not found"
        )
    
    return APIResponse(
        status="success",
        message=f"Retrieved policy for {provider_name}",
        data=policy
    )


if __name__ == "__main__":
    uvicorn.run("main_enhanced:app", host="0.0.0.0", port=8000, reload=True)

# Made with Bob
