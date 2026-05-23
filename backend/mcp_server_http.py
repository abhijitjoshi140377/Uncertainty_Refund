"""
MCP Server with Streamable HTTP Transport for IBM Context Forge
Uses FastMCP to expose all API endpoints as MCP tools
Handles POST /mcp with JSON-RPC 2.0 protocol
"""

from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, List, Optional
from datetime import datetime
import json

from models.database import get_db
from services.refund_estimator import RefundEstimator
from schemas import BookingCreate, BookingComponentCreate, RefundEstimateRequest, RiskEventCreate
import crud

# Initialize FastMCP server
mcp = FastMCP("Travel Refund Estimation API")

# Initialize refund estimator
estimator = RefundEstimator()


@mcp.tool()
def create_booking(
    customer_name: str,
    customer_email: str,
    travel_date: str,
    destination: str,
    origin: str,
    components: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create a new travel booking with multiple components (flights, hotels, visa, insurance).
    
    Args:
        customer_name: Full name of the customer (2-100 characters)
        customer_email: Customer's email address (valid email format)
        travel_date: Travel date in ISO 8601 format (e.g., "2026-06-01T10:00:00Z")
        destination: Destination location (2-100 characters)
        origin: Origin location (2-100 characters)
        components: List of booking components, each with:
            - component_type: "flight", "hotel", "visa", or "insurance"
            - provider_name: Name of the service provider
            - cost: Component cost (must be > 0)
            - refund_policy: Optional refund policy description
            - is_refundable: Boolean, whether component is refundable
            - cancellation_fee: Cancellation fee amount (default: 0.0)
    
    Returns:
        Dictionary with booking details including:
        - id: Booking ID
        - booking_reference: Unique booking reference code
        - customer_name: Customer name
        - customer_email: Customer email
        - total_cost: Total booking cost
        - status: Booking status
        - components: List of booking components
    """
    db = next(get_db())
    try:
        # Parse travel date
        travel_date_obj = datetime.fromisoformat(travel_date.replace('Z', '+00:00'))
        
        # Create booking components
        booking_components = [
            BookingComponentCreate(**comp) for comp in components
        ]
        
        # Create booking
        booking_data = BookingCreate(
            customer_name=customer_name,
            customer_email=customer_email,
            travel_date=travel_date_obj,
            destination=destination,
            origin=origin,
            components=booking_components
        )
        
        result = crud.create_booking(db, booking_data)
        
        return {
            "id": result.id,
            "booking_reference": result.booking_reference,
            "customer_name": result.customer_name,
            "customer_email": result.customer_email,
            "booking_date": result.booking_date.isoformat(),
            "travel_date": result.travel_date.isoformat(),
            "destination": result.destination,
            "origin": result.origin,
            "total_cost": result.total_cost,
            "status": result.status,
            "components": [
                {
                    "id": c.id,
                    "component_type": c.component_type,
                    "provider_name": c.provider_name,
                    "cost": c.cost,
                    "is_refundable": c.is_refundable
                }
                for c in result.components
            ]
        }
    finally:
        db.close()


@mcp.tool()
def get_bookings(skip: int = 0, limit: int = 100) -> Dict[str, Any]:
    """
    Retrieve paginated list of all travel bookings.
    
    Args:
        skip: Number of records to skip for pagination (default: 0, min: 0)
        limit: Maximum number of records to return (default: 100, min: 1, max: 1000)
    
    Returns:
        Dictionary with:
        - total: Total number of bookings
        - skip: Number of records skipped
        - limit: Maximum records returned
        - bookings: List of booking summaries with id, reference, customer, destination, cost
    """
    db = next(get_db())
    try:
        bookings = crud.get_bookings(db, skip=skip, limit=min(limit, 1000))
        total = crud.get_bookings_count(db)
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "bookings": [
                {
                    "id": b.id,
                    "booking_reference": b.booking_reference,
                    "customer_name": b.customer_name,
                    "destination": b.destination,
                    "origin": b.origin,
                    "total_cost": b.total_cost,
                    "travel_date": b.travel_date.isoformat(),
                    "status": b.status
                }
                for b in bookings
            ]
        }
    finally:
        db.close()


@mcp.tool()
def get_booking_details(booking_id: int) -> Dict[str, Any]:
    """
    Get detailed information for a specific booking by ID.
    
    Args:
        booking_id: Unique booking identifier (must be > 0)
    
    Returns:
        Dictionary with complete booking information including:
        - id, booking_reference, customer details
        - travel dates, destination, origin
        - total_cost, status
        - components: List of all booking components with details
    
    Raises:
        ValueError: If booking not found
    """
    db = next(get_db())
    try:
        booking = crud.get_booking(db, booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found")
        
        return {
            "id": booking.id,
            "booking_reference": booking.booking_reference,
            "customer_name": booking.customer_name,
            "customer_email": booking.customer_email,
            "booking_date": booking.booking_date.isoformat(),
            "travel_date": booking.travel_date.isoformat(),
            "destination": booking.destination,
            "origin": booking.origin,
            "total_cost": booking.total_cost,
            "status": booking.status,
            "components": [
                {
                    "id": c.id,
                    "component_type": c.component_type,
                    "provider_name": c.provider_name,
                    "cost": c.cost,
                    "refund_policy": c.refund_policy,
                    "is_refundable": c.is_refundable,
                    "cancellation_fee": c.cancellation_fee
                }
                for c in booking.components
            ]
        }
    finally:
        db.close()


@mcp.tool()
def estimate_refund(
    booking_id: int,
    selected_model: str = "auto",
    calamity_type: str = "auto",
    severity: str = "high"
) -> Dict[str, Any]:
    """
    Generate AI-powered refund estimate for a booking considering force majeure events.
    
    Uses machine learning models (Random Forest, Gradient Boosting, Rule-based) to predict
    expected refund amounts with confidence intervals.
    
    Args:
        booking_id: Booking ID to estimate refund for (must be > 0)
        selected_model: ML model to use - "auto", "random_forest", "gradient_boosting", or "rule_based" (default: "auto")
        calamity_type: Type of force majeure event - "auto" or specific type (default: "auto")
        severity: Event severity level - "low", "medium", "high", or "critical" (default: "high")
    
    Returns:
        Dictionary with refund estimation including:
        - booking_id: ID of the booking
        - expected_refund_amount: Predicted refund amount
        - expected_refund_percentage: Predicted refund percentage
        - confidence_lower: Lower bound of 95% confidence interval
        - confidence_upper: Upper bound of 95% confidence interval
        - risk_score: Risk score (0-100)
        - best_case_refund: Best case scenario refund
        - worst_case_refund: Worst case scenario refund
        - most_likely_refund: Most likely refund amount
        - model_version: ML model used
        - prediction_confidence: Model confidence score
    
    Raises:
        ValueError: If booking not found
    """
    db = next(get_db())
    try:
        booking = crud.get_booking(db, booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found")
        
        # Generate refund estimate using ML model
        estimate = estimator.estimate_refund(
            db,
            booking,
            selected_model=selected_model,
            calamity_type=calamity_type,
            severity=severity
        )
        
        # Save estimate to database
        result = crud.create_refund_estimate(db, booking_id, estimate)
        
        return {
            "id": result.id,
            "booking_id": result.booking_id,
            "estimate_date": result.estimate_date.isoformat(),
            "expected_refund_amount": result.expected_refund_amount,
            "expected_refund_percentage": result.expected_refund_percentage,
            "confidence_lower": result.confidence_lower,
            "confidence_upper": result.confidence_upper,
            "confidence_level": result.confidence_level,
            "current_risk_level": result.current_risk_level,
            "risk_score": result.risk_score,
            "best_case_refund": result.best_case_refund,
            "worst_case_refund": result.worst_case_refund,
            "most_likely_refund": result.most_likely_refund,
            "model_version": result.model_version,
            "prediction_confidence": result.prediction_confidence
        }
    finally:
        db.close()


@mcp.tool()
def get_refund_estimates(booking_id: int) -> Dict[str, Any]:
    """
    Get all refund estimates for a specific booking.
    
    Returns history of refund estimations for tracking and comparison purposes.
    
    Args:
        booking_id: Booking ID to get estimates for (must be > 0)
    
    Returns:
        Dictionary with:
        - booking_id: ID of the booking
        - total_estimates: Number of estimates
        - estimates: List of all estimates with details
    """
    db = next(get_db())
    try:
        estimates = crud.get_refund_estimates(db, booking_id)
        
        return {
            "booking_id": booking_id,
            "total_estimates": len(estimates),
            "estimates": [
                {
                    "id": e.id,
                    "estimate_date": e.estimate_date.isoformat(),
                    "expected_refund_amount": e.expected_refund_amount,
                    "expected_refund_percentage": e.expected_refund_percentage,
                    "risk_score": e.risk_score,
                    "model_version": e.model_version,
                    "prediction_confidence": e.prediction_confidence
                }
                for e in estimates
            ]
        }
    finally:
        db.close()


@mcp.tool()
def get_risk_events(active_only: bool = True) -> Dict[str, Any]:
    """
    Query current global risk events (natural disasters, political unrest, pandemics).
    
    Args:
        active_only: Filter only currently active events (default: True)
    
    Returns:
        Dictionary with:
        - total_events: Number of events
        - active_only: Whether filtered for active events
        - events: List of risk events with type, severity, region, description
    """
    db = next(get_db())
    try:
        events = crud.get_risk_events(db, active_only=active_only)
        
        return {
            "total_events": len(events),
            "active_only": active_only,
            "events": [
                {
                    "id": e.id,
                    "event_type": e.event_type,
                    "severity": e.severity,
                    "affected_region": e.affected_region,
                    "start_date": e.start_date.isoformat(),
                    "end_date": e.end_date.isoformat() if e.end_date else None,
                    "description": e.description,
                    "is_active": e.is_active
                }
                for e in events
            ]
        }
    finally:
        db.close()


@mcp.tool()
def get_regional_risk(region: str) -> Dict[str, Any]:
    """
    Get risk assessment for a specific geographic region.
    
    Returns aggregate risk level and list of active events in the region.
    
    Args:
        region: Geographic region name (e.g., "Ukraine", "Middle East", "Southeast Asia")
    
    Returns:
        Dictionary with:
        - region: Region name
        - risk_level: Aggregate risk level ("low", "medium", "high", "critical")
        - active_events: Number of active events
        - events: List of events affecting the region
    """
    db = next(get_db())
    try:
        events = crud.get_risk_events_by_region(db, region)
        
        if not events:
            return {
                "region": region,
                "risk_level": "low",
                "active_events": 0,
                "events": []
            }
        
        # Calculate aggregate risk
        risk_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        max_severity = max([risk_scores.get(e.severity, 1) for e in events])
        severity_map = {1: "low", 2: "medium", 3: "high", 4: "critical"}
        
        return {
            "region": region,
            "risk_level": severity_map[max_severity],
            "active_events": len(events),
            "events": [
                {
                    "id": e.id,
                    "event_type": e.event_type,
                    "severity": e.severity,
                    "description": e.description,
                    "start_date": e.start_date.isoformat()
                }
                for e in events
            ]
        }
    finally:
        db.close()


@mcp.tool()
def get_historical_refunds(
    component_type: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 100
) -> Dict[str, Any]:
    """
    Access historical refund data for analytics and trend analysis.
    
    Args:
        component_type: Filter by component type - "flight", "hotel", "visa", or "insurance" (optional)
        event_type: Filter by event type (optional)
        limit: Maximum number of records to return (default: 100, min: 1, max: 1000)
    
    Returns:
        Dictionary with:
        - total_records: Number of records returned
        - filters: Applied filters
        - refunds: List of historical refund records
    """
    db = next(get_db())
    try:
        refunds = crud.get_historical_refunds(
            db,
            component_type=component_type,
            event_type=event_type,
            limit=min(limit, 1000)
        )
        
        return {
            "total_records": len(refunds),
            "filters": {
                "component_type": component_type,
                "event_type": event_type,
                "limit": limit
            },
            "refunds": [
                {
                    "id": r.id,
                    "component_type": r.component_type,
                    "event_type": r.event_type,
                    "refund_percentage": r.refund_percentage,
                    "refund_amount": r.refund_amount,
                    "original_cost": r.original_cost,
                    "processing_days": r.processing_days,
                    "was_force_majeure": r.was_force_majeure,
                    "refund_date": r.refund_date.isoformat()
                }
                for r in refunds
            ]
        }
    finally:
        db.close()


@mcp.tool()
def get_refund_statistics() -> Dict[str, Any]:
    """
    Get aggregated refund statistics grouped by component and event type.
    
    Returns average refund percentages, amounts, success rates, and processing times.
    
    Returns:
        Dictionary with:
        - total_categories: Number of component/event combinations
        - statistics: List of statistics by component and event type
    """
    db = next(get_db())
    try:
        stats = crud.get_refund_statistics(db)
        
        return {
            "total_categories": len(stats),
            "statistics": stats
        }
    finally:
        db.close()


@mcp.tool()
def get_provider_policies(provider_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Query provider refund and cancellation policies.
    
    Args:
        provider_type: Filter by provider type (e.g., "airline", "hotel") (optional)
    
    Returns:
        Dictionary with:
        - total_providers: Number of providers
        - filter: Applied filter
        - providers: List of provider policies
    """
    db = next(get_db())
    try:
        providers = crud.get_providers(db, provider_type=provider_type)
        
        return {
            "total_providers": len(providers),
            "filter": {"provider_type": provider_type},
            "providers": [
                {
                    "id": p.id,
                    "provider_name": p.provider_name,
                    "provider_type": p.provider_type,
                    "base_refund_percentage": p.base_refund_percentage,
                    "cancellation_fee": p.cancellation_fee,
                    "force_majeure_refund_percentage": p.force_majeure_refund_percentage,
                    "policy_text": p.policy_text
                }
                for p in providers
            ]
        }
    finally:
        db.close()


@mcp.tool()
def get_provider_policy(provider_name: str) -> Dict[str, Any]:
    """
    Get detailed policy for a specific service provider.
    
    Args:
        provider_name: Name of the service provider (e.g., "Air India", "Taj Hotels")
    
    Returns:
        Dictionary with complete provider policy details
    
    Raises:
        ValueError: If provider not found
    """
    db = next(get_db())
    try:
        policy = crud.get_provider_policy(db, provider_name)
        if not policy:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        return {
            "id": policy.id,
            "provider_name": policy.provider_name,
            "provider_type": policy.provider_type,
            "base_refund_percentage": policy.base_refund_percentage,
            "cancellation_fee": policy.cancellation_fee,
            "force_majeure_refund_percentage": policy.force_majeure_refund_percentage,
            "policy_text": policy.policy_text,
            "last_updated": policy.last_updated.isoformat() if policy.last_updated else None
        }
    finally:
        db.close()


# Export the FastMCP app for mounting in FastAPI
def get_mcp_app():
    """Get the FastMCP application for mounting in FastAPI"""
    return mcp

# Made with Bob
