"""
Enhanced Pydantic schemas with consistent response structure
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Any, Generic, TypeVar
from datetime import datetime
from enum import Enum


# Generic Response Wrapper
T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper for consistency"""
    status: str = Field(..., description="Response status: success or error")
    message: str = Field(..., description="Human-readable message")
    data: Optional[T] = Field(None, description="Response data payload")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "data": {}
            }
        }


class ErrorDetail(BaseModel):
    """Error detail structure"""
    field: Optional[str] = Field(None, description="Field that caused the error")
    message: str = Field(..., description="Error message")
    type: Optional[str] = Field(None, description="Error type")


class ErrorResponse(BaseModel):
    """Standard error response"""
    status: str = Field(default="error", description="Always 'error' for error responses")
    message: str = Field(..., description="Error message")
    errors: Optional[List[ErrorDetail]] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Validation failed",
                "errors": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "type": "value_error"
                    }
                ]
            }
        }


# Enums for validation
class ComponentType(str, Enum):
    """Booking component types"""
    FLIGHT = "flight"
    HOTEL = "hotel"
    VISA = "visa"
    INSURANCE = "insurance"


class EventType(str, Enum):
    """Force majeure event types"""
    WAR = "war"
    PANDEMIC = "pandemic"
    NATURAL_DISASTER = "natural_disaster"
    POLITICAL_UNREST = "political_unrest"
    TERRORISM = "terrorism"


class SeverityLevel(str, Enum):
    """Risk severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MLModel(str, Enum):
    """Available ML models"""
    AUTO = "auto"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    RULE_BASED = "rule_based"


class BookingStatus(str, Enum):
    """Booking status"""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    REFUNDED = "refunded"


# Booking Component Schemas
class BookingComponentBase(BaseModel):
    """Base schema for booking components"""
    component_type: ComponentType = Field(..., description="Type of booking component")
    provider_name: str = Field(..., min_length=2, max_length=100, description="Service provider name")
    cost: float = Field(..., gt=0, description="Component cost in local currency")
    refund_policy: Optional[str] = Field(None, max_length=500, description="Provider's refund policy")
    is_refundable: bool = Field(default=False, description="Whether component is refundable")
    cancellation_fee: float = Field(default=0.0, ge=0, description="Cancellation fee amount")
    
    class Config:
        json_schema_extra = {
            "example": {
                "component_type": "flight",
                "provider_name": "Air India",
                "cost": 50000,
                "refund_policy": "50% refund if cancelled 7 days before travel",
                "is_refundable": True,
                "cancellation_fee": 500
            }
        }


class BookingComponentCreate(BookingComponentBase):
    """Schema for creating a booking component"""
    pass


class BookingComponentResponse(BookingComponentBase):
    """Schema for booking component response"""
    id: int = Field(..., description="Unique component ID")
    booking_id: int = Field(..., description="Associated booking ID")
    
    class Config:
        from_attributes = True


# Travel Booking Schemas
class BookingCreate(BaseModel):
    """Schema for creating a new booking"""
    customer_name: str = Field(..., min_length=2, max_length=100, description="Customer's full name")
    customer_email: EmailStr = Field(..., description="Customer's email address")
    travel_date: datetime = Field(..., description="Travel date and time (ISO 8601 format)")
    destination: str = Field(..., min_length=2, max_length=100, description="Destination city/country")
    origin: str = Field(..., min_length=2, max_length=100, description="Origin city/country")
    components: List[BookingComponentCreate] = Field(..., min_items=1, description="List of booking components")
    
    class Config:
        json_schema_extra = {
            "example": {
                "customer_name": "John Doe",
                "customer_email": "john.doe@example.com",
                "travel_date": "2026-08-15T10:00:00",
                "destination": "Paris",
                "origin": "Mumbai",
                "components": [
                    {
                        "component_type": "flight",
                        "provider_name": "Air India",
                        "cost": 50000,
                        "is_refundable": True,
                        "cancellation_fee": 500
                    }
                ]
            }
        }


class BookingResponse(BaseModel):
    """Schema for booking response"""
    id: int = Field(..., description="Unique booking ID")
    booking_reference: str = Field(..., description="Unique booking reference code")
    customer_name: str = Field(..., description="Customer's full name")
    customer_email: str = Field(..., description="Customer's email address")
    booking_date: datetime = Field(..., description="Date booking was created")
    travel_date: datetime = Field(..., description="Travel date")
    destination: str = Field(..., description="Destination")
    origin: str = Field(..., description="Origin")
    total_cost: float = Field(..., description="Total booking cost")
    status: BookingStatus = Field(..., description="Current booking status")
    components: List[BookingComponentResponse] = Field(..., description="Booking components")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "booking_reference": "BK12345678",
                "customer_name": "John Doe",
                "customer_email": "john.doe@example.com",
                "booking_date": "2026-05-20T10:00:00",
                "travel_date": "2026-08-15T10:00:00",
                "destination": "Paris",
                "origin": "Mumbai",
                "total_cost": 75000,
                "status": "active",
                "components": []
            }
        }


# Refund Estimate Schemas
class RefundEstimateRequest(BaseModel):
    """Schema for refund estimation request"""
    selected_model: MLModel = Field(
        default=MLModel.AUTO,
        description="ML model to use for estimation"
    )
    calamity_type: str = Field(
        default="auto",
        description="Type of force majeure event (auto for automatic detection)"
    )
    severity: SeverityLevel = Field(
        default=SeverityLevel.HIGH,
        description="Severity level of the event"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "selected_model": "auto",
                "calamity_type": "pandemic",
                "severity": "high"
            }
        }


class RefundEstimateResponse(BaseModel):
    """Schema for refund estimate response"""
    id: int = Field(..., description="Unique estimate ID")
    booking_id: int = Field(..., description="Associated booking ID")
    estimate_date: datetime = Field(..., description="Date estimate was generated")
    expected_refund_amount: float = Field(..., description="Expected refund amount")
    expected_refund_percentage: float = Field(..., description="Expected refund percentage")
    confidence_lower: float = Field(..., description="Lower bound of 95% confidence interval")
    confidence_upper: float = Field(..., description="Upper bound of 95% confidence interval")
    confidence_level: float = Field(..., description="Confidence level (typically 0.95)")
    current_risk_level: SeverityLevel = Field(..., description="Current risk level")
    risk_score: float = Field(..., description="Risk score (0-100)")
    best_case_refund: float = Field(..., description="Best case refund amount")
    worst_case_refund: float = Field(..., description="Worst case refund amount")
    most_likely_refund: float = Field(..., description="Most likely refund amount")
    model_version: str = Field(..., description="ML model version used")
    prediction_confidence: float = Field(..., description="Model prediction confidence")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "booking_id": 1,
                "estimate_date": "2026-05-20T10:00:00",
                "expected_refund_amount": 37500,
                "expected_refund_percentage": 50.0,
                "confidence_lower": 30000,
                "confidence_upper": 45000,
                "confidence_level": 0.95,
                "current_risk_level": "high",
                "risk_score": 75.5,
                "best_case_refund": 55000,
                "worst_case_refund": 15000,
                "most_likely_refund": 38000,
                "model_version": "ensemble_v1.0",
                "prediction_confidence": 0.85
            }
        }


# Risk Event Schemas
class RiskEventBase(BaseModel):
    """Base schema for risk events"""
    event_type: EventType = Field(..., description="Type of force majeure event")
    severity: SeverityLevel = Field(..., description="Event severity level")
    affected_region: str = Field(..., min_length=2, max_length=100, description="Affected region/country")
    start_date: datetime = Field(..., description="Event start date")
    end_date: Optional[datetime] = Field(None, description="Event end date (if applicable)")
    description: Optional[str] = Field(None, max_length=1000, description="Event description")
    is_active: bool = Field(default=True, description="Whether event is currently active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "pandemic",
                "severity": "high",
                "affected_region": "Global",
                "start_date": "2026-01-01T00:00:00",
                "end_date": None,
                "description": "Global health emergency",
                "is_active": True
            }
        }


class RiskEventCreate(RiskEventBase):
    """Schema for creating a risk event"""
    pass


class RiskEventResponse(RiskEventBase):
    """Schema for risk event response"""
    id: int = Field(..., description="Unique event ID")
    
    class Config:
        from_attributes = True


class RegionalRiskResponse(BaseModel):
    """Schema for regional risk assessment"""
    region: str = Field(..., description="Region name")
    risk_level: SeverityLevel = Field(..., description="Aggregate risk level")
    events: List[RiskEventResponse] = Field(..., description="Active events in region")
    
    class Config:
        json_schema_extra = {
            "example": {
                "region": "Ukraine",
                "risk_level": "critical",
                "events": []
            }
        }


# Historical Refund Schemas
class HistoricalRefundResponse(BaseModel):
    """Schema for historical refund data"""
    id: int = Field(..., description="Unique record ID")
    component_type: ComponentType = Field(..., description="Component type")
    provider_name: str = Field(..., description="Provider name")
    original_cost: float = Field(..., description="Original cost")
    refund_amount: float = Field(..., description="Refund amount received")
    refund_percentage: float = Field(..., description="Refund percentage")
    event_type: EventType = Field(..., description="Event type that caused cancellation")
    event_severity: SeverityLevel = Field(..., description="Event severity")
    days_before_travel: int = Field(..., description="Days before travel when cancelled")
    was_force_majeure: bool = Field(..., description="Whether it was force majeure")
    had_insurance: bool = Field(..., description="Whether customer had insurance")
    refund_date: datetime = Field(..., description="Date refund was processed")
    region: str = Field(..., description="Region")
    
    class Config:
        from_attributes = True


# Provider Policy Schemas
class ProviderPolicyResponse(BaseModel):
    """Schema for provider policy response"""
    id: int = Field(..., description="Unique policy ID")
    provider_name: str = Field(..., description="Provider name")
    provider_type: ComponentType = Field(..., description="Provider type")
    standard_refund_percentage: float = Field(..., description="Standard refund percentage")
    force_majeure_refund_percentage: float = Field(..., description="Force majeure refund percentage")
    cancellation_fee: float = Field(..., description="Cancellation fee")
    refund_processing_days: int = Field(..., description="Days to process refund")
    policy_text: Optional[str] = Field(None, description="Full policy text")
    force_majeure_clause: Optional[str] = Field(None, description="Force majeure clause")
    last_updated: datetime = Field(..., description="Last policy update date")
    
    class Config:
        from_attributes = True


# Statistics Schemas
class RefundStatistics(BaseModel):
    """Schema for refund statistics"""
    component_type: ComponentType = Field(..., description="Component type")
    event_type: EventType = Field(..., description="Event type")
    average_refund_percentage: float = Field(..., description="Average refund percentage")
    total_cases: int = Field(..., description="Total number of cases")
    force_majeure_cases: int = Field(..., description="Number of force majeure cases")
    average_refund_amount: float = Field(..., description="Average refund amount")
    
    class Config:
        json_schema_extra = {
            "example": {
                "component_type": "flight",
                "event_type": "pandemic",
                "average_refund_percentage": 55.5,
                "total_cases": 150,
                "force_majeure_cases": 120,
                "average_refund_amount": 27500
            }
        }


# Health Check Schema
class HealthCheckResponse(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Current server timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "refund-estimation-api",
                "version": "1.0.0",
                "timestamp": "2026-05-20T10:00:00Z"
            }
        }


# Pagination Schemas
class PaginationParams(BaseModel):
    """Schema for pagination parameters"""
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of records to return")


class PaginatedResponse(BaseModel, Generic[T]):
    """Schema for paginated responses"""
    status: str = Field(default="success", description="Response status")
    message: str = Field(..., description="Response message")
    data: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Maximum items per page")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Retrieved 10 bookings",
                "data": [],
                "total": 50,
                "skip": 0,
                "limit": 10
            }
        }

# Made with Bob
