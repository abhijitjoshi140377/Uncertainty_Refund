"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# Booking Component Schemas
class BookingComponentBase(BaseModel):
    component_type: str = Field(..., description="Type: flight, hotel, visa, insurance")
    provider_name: str
    cost: float = Field(..., gt=0)
    refund_policy: Optional[str] = None
    is_refundable: bool = False
    cancellation_fee: float = 0.0


class BookingComponentCreate(BookingComponentBase):
    pass


class BookingComponentResponse(BookingComponentBase):
    id: int
    booking_id: int
    
    class Config:
        from_attributes = True


# Travel Booking Schemas
class BookingCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_email: EmailStr
    travel_date: datetime
    destination: str = Field(..., min_length=2, max_length=100)
    origin: str = Field(..., min_length=2, max_length=100)
    components: List[BookingComponentCreate]


class BookingResponse(BaseModel):
    id: int
    booking_reference: str
    customer_name: str
    customer_email: str
    booking_date: datetime
    travel_date: datetime
    destination: str
    origin: str
    total_cost: float
    status: str
    components: List[BookingComponentResponse]
    
    class Config:
        from_attributes = True


# Refund Estimate Schemas
class RefundEstimateRequest(BaseModel):
    selected_model: str = Field(default="auto", description="auto, random_forest, gradient_boosting, rule_based")
    calamity_type: str = Field(default="auto", description="auto or selected event type")
    severity: str = Field(default="high", description="low, medium, high, critical")


class RefundEstimateResponse(BaseModel):
    id: int
    booking_id: int
    estimate_date: datetime
    expected_refund_amount: float
    expected_refund_percentage: float
    confidence_lower: float
    confidence_upper: float
    confidence_level: float
    current_risk_level: str
    risk_score: float
    best_case_refund: float
    worst_case_refund: float
    most_likely_refund: float
    model_version: str
    prediction_confidence: float
    
    class Config:
        from_attributes = True


# Risk Event Schemas
class RiskEventBase(BaseModel):
    event_type: str
    severity: str
    affected_region: str = Field(..., min_length=2, max_length=100)
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    is_active: bool = True


class RiskEventCreate(RiskEventBase):
    pass


class RiskEventResponse(RiskEventBase):
    id: int
    
    class Config:
        from_attributes = True


# Historical Refund Schemas
class HistoricalRefundResponse(BaseModel):
    id: int
    component_type: str
    provider_name: str
    original_cost: float
    refund_amount: float
    refund_percentage: float
    event_type: str
    event_severity: str
    days_before_travel: int
    was_force_majeure: bool
    had_insurance: bool
    refund_date: datetime
    region: str
    
    class Config:
        from_attributes = True


# Provider Policy Schemas
class ProviderPolicyResponse(BaseModel):
    id: int
    provider_name: str
    provider_type: str
    standard_refund_percentage: float
    force_majeure_refund_percentage: float
    cancellation_fee: float
    refund_processing_days: int
    policy_text: Optional[str]
    force_majeure_clause: Optional[str]
    last_updated: datetime
    
    class Config:
        from_attributes = True


# Statistics Schemas
class RefundStatistics(BaseModel):
    component_type: str
    event_type: str
    average_refund_percentage: float
    total_cases: int
    force_majeure_cases: int
    average_refund_amount: float

# Made with Bob
