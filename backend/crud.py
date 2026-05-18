"""
CRUD operations for database models
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from typing import List, Optional
from datetime import datetime
import random
import string

from models.database import (
    TravelBooking, BookingComponent, RiskEvent, 
    HistoricalRefund, RefundEstimate, ProviderPolicy
)
from schemas import BookingCreate


def generate_booking_reference() -> str:
    """Generate unique booking reference"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


# Booking CRUD
def create_booking(db: Session, booking: BookingCreate) -> TravelBooking:
    """Create a new travel booking"""
    total_cost = sum(comp.cost for comp in booking.components)
    
    db_booking = TravelBooking(
        booking_reference=generate_booking_reference(),
        customer_name=booking.customer_name,
        customer_email=booking.customer_email,
        travel_date=booking.travel_date,
        destination=booking.destination,
        origin=booking.origin,
        total_cost=total_cost,
        status='active'
    )
    db.add(db_booking)
    db.flush()
    
    # Add components
    for comp in booking.components:
        db_component = BookingComponent(
            booking_id=db_booking.id,
            component_type=comp.component_type,
            provider_name=comp.provider_name,
            cost=comp.cost,
            refund_policy=comp.refund_policy,
            is_refundable=comp.is_refundable,
            cancellation_fee=comp.cancellation_fee
        )
        db.add(db_component)
    
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int) -> Optional[TravelBooking]:
    """Get booking by ID"""
    return db.query(TravelBooking).filter(TravelBooking.id == booking_id).first()


def get_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[TravelBooking]:
    """Get all bookings"""
    return db.query(TravelBooking).offset(skip).limit(limit).all()


def get_bookings_count(db: Session) -> int:
    """Get total number of bookings"""
    return db.query(TravelBooking).count()


# Refund Estimate CRUD
def create_refund_estimate(db: Session, booking_id: int, estimate_data: dict) -> RefundEstimate:
    """Create a refund estimate"""
    db_estimate = RefundEstimate(
        booking_id=booking_id,
        **estimate_data
    )
    db.add(db_estimate)
    db.commit()
    db.refresh(db_estimate)
    return db_estimate


def get_refund_estimates(db: Session, booking_id: int) -> List[RefundEstimate]:
    """Get all refund estimates for a booking"""
    return db.query(RefundEstimate).filter(
        RefundEstimate.booking_id == booking_id
    ).order_by(RefundEstimate.estimate_date.desc()).all()


# Risk Event CRUD
def get_risk_events(db: Session, active_only: bool = True) -> List[RiskEvent]:
    """Get risk events"""
    query = db.query(RiskEvent)
    if active_only:
        query = query.filter(RiskEvent.is_active == True)
    return query.order_by(RiskEvent.start_date.desc()).all()


def get_risk_events_by_region(db: Session, region: str) -> List[RiskEvent]:
    """Get risk events for a specific region"""
    return db.query(RiskEvent).filter(
        RiskEvent.affected_region.ilike(f"%{region}%"),
        RiskEvent.is_active == True
    ).all()


# Historical Refund CRUD
def get_historical_refunds(
    db: Session, 
    component_type: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 100
) -> List[HistoricalRefund]:
    """Get historical refund data"""
    query = db.query(HistoricalRefund)
    
    if component_type:
        query = query.filter(HistoricalRefund.component_type == component_type)
    if event_type:
        query = query.filter(HistoricalRefund.event_type == event_type)
    
    return query.order_by(HistoricalRefund.refund_date.desc()).limit(limit).all()


def get_refund_statistics(db: Session) -> List[dict]:
    """Get refund statistics grouped by component and event type"""
    results = db.query(
        HistoricalRefund.component_type,
        HistoricalRefund.event_type,
        func.avg(HistoricalRefund.refund_percentage).label('avg_refund_pct'),
        func.count(HistoricalRefund.id).label('total_cases'),
        func.sum(func.cast(HistoricalRefund.was_force_majeure, Integer)).label('force_majeure_cases'),
        func.avg(HistoricalRefund.refund_amount).label('avg_refund_amount')
    ).group_by(
        HistoricalRefund.component_type,
        HistoricalRefund.event_type
    ).all()
    
    return [
        {
            'component_type': r.component_type,
            'event_type': r.event_type,
            'average_refund_percentage': round(r.avg_refund_pct, 2),
            'total_cases': r.total_cases,
            'force_majeure_cases': r.force_majeure_cases or 0,
            'average_refund_amount': round(r.avg_refund_amount, 2)
        }
        for r in results
    ]


# Provider Policy CRUD
def get_providers(db: Session, provider_type: Optional[str] = None) -> List[ProviderPolicy]:
    """Get provider policies"""
    query = db.query(ProviderPolicy)
    if provider_type:
        query = query.filter(ProviderPolicy.provider_type == provider_type)
    return query.all()


def get_provider_policy(db: Session, provider_name: str) -> Optional[ProviderPolicy]:
    """Get specific provider policy"""
    return db.query(ProviderPolicy).filter(
        ProviderPolicy.provider_name == provider_name
    ).first()


def create_historical_refund(db: Session, refund_data: dict) -> HistoricalRefund:
    """Create historical refund record"""
    db_refund = HistoricalRefund(**refund_data)
    db.add(db_refund)
    db.commit()
    db.refresh(db_refund)
    return db_refund


def create_risk_event(db: Session, event_data: dict) -> RiskEvent:
    """Create risk event"""
    db_event = RiskEvent(**event_data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def create_provider_policy(db: Session, policy_data: dict) -> ProviderPolicy:
    """Create provider policy"""
    db_policy = ProviderPolicy(**policy_data)
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

# Made with Bob
