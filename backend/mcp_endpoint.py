"""
MCP (Model Context Protocol) SSE Endpoint for FastAPI
Exposes all API endpoints as MCP tools via Server-Sent Events transport
"""

import json
import asyncio
from typing import Any, Dict, List
from fastapi import Request
from sse_starlette.sse import EventSourceResponse
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from sqlalchemy.orm import Session

from models.database import get_db
from services.refund_estimator import RefundEstimator
from schemas import BookingCreate, RefundEstimateRequest, RiskEventCreate
import crud


class RefundMCPServer:
    """MCP Server for Refund Estimation API"""
    
    def __init__(self):
        self.server = Server("refund-estimation-api")
        self.estimator = RefundEstimator()
        self._setup_tools()
    
    def _setup_tools(self):
        """Register all MCP tools"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available MCP tools"""
            return [
                Tool(
                    name="create_booking",
                    description="""Create a new travel booking with multiple components (flights, hotels, visa, insurance).
                    
                    Returns booking reference, total cost, and booking ID. Use this when a customer wants to book travel.
                    
                    Required fields: customer_name, customer_email, booking_date, travel_start_date, travel_end_date, 
                    destination_country, total_cost, components (array of booking components).
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "customer_name": {"type": "string", "description": "Full name of the customer"},
                            "customer_email": {"type": "string", "format": "email", "description": "Customer's email address"},
                            "booking_date": {"type": "string", "format": "date-time", "description": "Booking creation date (ISO 8601)"},
                            "travel_start_date": {"type": "string", "format": "date-time", "description": "Travel start date (ISO 8601)"},
                            "travel_end_date": {"type": "string", "format": "date-time", "description": "Travel end date (ISO 8601)"},
                            "destination_country": {"type": "string", "description": "Destination country name"},
                            "total_cost": {"type": "number", "description": "Total booking cost in INR", "minimum": 0},
                            "components": {
                                "type": "array",
                                "description": "List of booking components",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "component_type": {"type": "string", "enum": ["flight", "hotel", "visa", "insurance"]},
                                        "provider": {"type": "string", "description": "Service provider name"},
                                        "cost": {"type": "number", "description": "Component cost in INR", "minimum": 0},
                                        "booking_reference": {"type": "string", "description": "Provider's booking reference"},
                                        "cancellation_policy": {"type": "string", "description": "Cancellation policy details"}
                                    },
                                    "required": ["component_type", "provider", "cost"]
                                }
                            }
                        },
                        "required": ["customer_name", "customer_email", "booking_date", "travel_start_date", 
                                   "travel_end_date", "destination_country", "total_cost", "components"]
                    }
                ),
                Tool(
                    name="get_bookings",
                    description="""Retrieve paginated list of all travel bookings.
                    
                    Returns list of bookings with customer details, travel dates, and total costs.
                    Use skip and limit for pagination (max 1000 records per request).
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "skip": {"type": "integer", "description": "Number of records to skip", "default": 0, "minimum": 0},
                            "limit": {"type": "integer", "description": "Maximum records to return", "default": 100, "minimum": 1, "maximum": 1000}
                        }
                    }
                ),
                Tool(
                    name="get_booking_details",
                    description="""Get detailed information for a specific booking by ID.
                    
                    Returns complete booking information including all components, customer details, and travel dates.
                    Returns 404 error if booking not found.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "booking_id": {"type": "integer", "description": "Unique booking identifier", "minimum": 1}
                        },
                        "required": ["booking_id"]
                    }
                ),
                Tool(
                    name="estimate_refund",
                    description="""Generate AI-powered refund estimate for a booking considering force majeure events.
                    
                    Uses machine learning models (Random Forest, Gradient Boosting, Rule-based) to predict expected refund
                    amounts with 95% confidence intervals. Considers provider policies, booking components, and event severity.
                    
                    Returns: expected refund amount/percentage, confidence intervals, risk score, best/worst/likely scenarios,
                    model version, and prediction confidence.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "booking_id": {"type": "integer", "description": "Booking ID to estimate refund for", "minimum": 1},
                            "selected_model": {
                                "type": "string",
                                "enum": ["auto", "random_forest", "gradient_boosting", "rule_based"],
                                "description": "ML model to use for prediction",
                                "default": "auto"
                            },
                            "calamity_type": {
                                "type": "string",
                                "enum": ["natural_disaster", "political_unrest", "pandemic", "terrorism", "economic_crisis", "other"],
                                "description": "Type of force majeure event",
                                "default": "natural_disaster"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "description": "Severity level of the event",
                                "default": "medium"
                            }
                        },
                        "required": ["booking_id"]
                    }
                ),
                Tool(
                    name="get_refund_estimates",
                    description="""Get all refund estimates for a specific booking.
                    
                    Returns history of refund estimations for tracking and comparison purposes.
                    Useful for comparing different scenarios or tracking estimates over time.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "booking_id": {"type": "integer", "description": "Booking ID to get estimates for", "minimum": 1}
                        },
                        "required": ["booking_id"]
                    }
                ),
                Tool(
                    name="get_risk_events",
                    description="""Query current global risk events (natural disasters, political unrest, pandemics).
                    
                    Returns list of active force majeure events with severity levels, affected regions, and descriptions.
                    Use active_only=true to filter only currently active events.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "active_only": {"type": "boolean", "description": "Filter only active events", "default": True}
                        }
                    }
                ),
                Tool(
                    name="get_regional_risk",
                    description="""Get risk assessment for a specific geographic region.
                    
                    Returns aggregate risk level (low/medium/high/critical) and list of active events in the region.
                    Useful for assessing travel safety and refund likelihood for a destination.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "region": {"type": "string", "description": "Geographic region name (e.g., 'Ukraine', 'Middle East')"}
                        },
                        "required": ["region"]
                    }
                ),
                Tool(
                    name="get_historical_refunds",
                    description="""Access historical refund data for analytics and trend analysis.
                    
                    Returns historical refund records with actual refund amounts, processing times, and outcomes.
                    Filter by component_type (flight/hotel/visa/insurance) or event_type.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_type": {"type": "string", "enum": ["flight", "hotel", "visa", "insurance"], "description": "Filter by component type"},
                            "event_type": {"type": "string", "description": "Filter by event type"},
                            "limit": {"type": "integer", "description": "Maximum records to return", "default": 100, "minimum": 1, "maximum": 1000}
                        }
                    }
                ),
                Tool(
                    name="get_refund_statistics",
                    description="""Get aggregated refund statistics grouped by component and event type.
                    
                    Returns average refund percentages, amounts, success rates, and processing times.
                    Useful for understanding refund patterns and trends across different scenarios.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_provider_policies",
                    description="""Query provider refund and cancellation policies.
                    
                    Returns list of all service providers (airlines, hotels, visa services, insurance) with their
                    cancellation policies, refund percentages, and fees. Filter by provider_type if needed.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "provider_type": {"type": "string", "description": "Filter by provider type (e.g., 'airline', 'hotel')"}
                        }
                    }
                ),
                Tool(
                    name="get_provider_policy",
                    description="""Get detailed policy for a specific service provider.
                    
                    Returns complete cancellation policy text, refund percentages, fees, and force majeure clauses
                    for a specific provider. Returns 404 if provider not found.
                    """,
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "provider_name": {"type": "string", "description": "Name of the service provider (e.g., 'Air India', 'Taj Hotels')"}
                        },
                        "required": ["provider_name"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute MCP tool calls"""
            db = next(get_db())
            
            try:
                if name == "create_booking":
                    booking_data = BookingCreate(**arguments)
                    result = crud.create_booking(db, booking_data)
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": f"Booking created successfully with reference {result.booking_reference}",
                            "data": {
                                "id": result.id,
                                "booking_reference": result.booking_reference,
                                "customer_name": result.customer_name,
                                "total_cost": result.total_cost
                            }
                        }, indent=2)
                    )]
                
                elif name == "get_bookings":
                    skip = arguments.get("skip", 0)
                    limit = arguments.get("limit", 100)
                    bookings = crud.get_bookings(db, skip=skip, limit=limit)
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": f"Retrieved {len(bookings)} bookings",
                            "data": [
                                {
                                    "id": b.id,
                                    "booking_reference": b.booking_reference,
                                    "customer_name": b.customer_name,
                                    "destination_country": b.destination_country,
                                    "total_cost": b.total_cost,
                                    "travel_start_date": b.travel_start_date.isoformat() if b.travel_start_date else None
                                }
                                for b in bookings
                            ]
                        }, indent=2)
                    )]
                
                elif name == "get_booking_details":
                    booking_id = arguments["booking_id"]
                    booking = crud.get_booking(db, booking_id)
                    if not booking:
                        return [TextContent(
                            type="text",
                            text=json.dumps({
                                "status": "error",
                                "error_type": "not_found",
                                "message": f"Booking {booking_id} not found"
                            }, indent=2)
                        )]
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": "Booking details retrieved",
                            "data": {
                                "id": booking.id,
                                "booking_reference": booking.booking_reference,
                                "customer_name": booking.customer_name,
                                "customer_email": booking.customer_email,
                                "destination_country": booking.destination_country,
                                "total_cost": booking.total_cost,
                                "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
                                "travel_start_date": booking.travel_start_date.isoformat() if booking.travel_start_date else None,
                                "travel_end_date": booking.travel_end_date.isoformat() if booking.travel_end_date else None,
                                "components": [
                                    {
                                        "component_type": c.component_type,
                                        "provider": c.provider,
                                        "cost": c.cost,
                                        "booking_reference": c.booking_reference
                                    }
                                    for c in booking.components
                                ]
                            }
                        }, indent=2)
                    )]
                
                elif name == "estimate_refund":
                    booking_id = arguments["booking_id"]
                    booking = crud.get_booking(db, booking_id)
                    if not booking:
                        return [TextContent(
                            type="text",
                            text=json.dumps({
                                "status": "error",
                                "error_type": "not_found",
                                "message": f"Booking {booking_id} not found"
                            }, indent=2)
                        )]
                    
                    estimate = self.estimator.estimate_refund(
                        db,
                        booking,
                        selected_model=arguments.get("selected_model", "auto"),
                        calamity_type=arguments.get("calamity_type", "natural_disaster"),
                        severity=arguments.get("severity", "medium")
                    )
                    result = crud.create_refund_estimate(db, booking_id, estimate)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": "Refund estimate generated successfully",
                            "data": {
                                "booking_id": result.booking_id,
                                "expected_refund_amount": result.expected_refund_amount,
                                "expected_refund_percentage": result.expected_refund_percentage,
                                "confidence_interval_lower": result.confidence_interval_lower,
                                "confidence_interval_upper": result.confidence_interval_upper,
                                "risk_score": result.risk_score,
                                "best_case_refund": result.best_case_refund,
                                "worst_case_refund": result.worst_case_refund,
                                "most_likely_refund": result.most_likely_refund,
                                "model_used": result.model_used,
                                "prediction_confidence": result.prediction_confidence
                            }
                        }, indent=2)
                    )]
                
                elif name == "get_refund_estimates":
                    booking_id = arguments["booking_id"]
                    estimates = crud.get_refund_estimates(db, booking_id)
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": f"Retrieved {len(estimates)} refund estimates",
                            "data": [
                                {
                                    "id": e.id,
                                    "expected_refund_amount": e.expected_refund_amount,
                                    "expected_refund_percentage": e.expected_refund_percentage,
                                    "risk_score": e.risk_score,
                                    "model_used": e.model_used,
                                    "created_at": e.created_at.isoformat() if e.created_at else None
                                }
                                for e in estimates
                            ]
                        }, indent=2)
                    )]
                
                elif name == "get_risk_events":
                    active_only = arguments.get("active_only", True)
                    events = crud.get_risk_events(db, active_only=active_only)
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": f"Retrieved {len(events)} risk events",
                            "data": [
                                {
                                    "id": e.id,
                                    "event_type": e.event_type,
                                    "severity": e.severity,
                                    "affected_region": e.affected_region,
                                    "description": e.description,
                                    "is_active": e.is_active
                                }
                                for e in events
                            ]
                        }, indent=2)
                    )]
                
                elif name == "get_regional_risk":
                    region = arguments["region"]
                    events = crud.get_risk_events_by_region(db, region)
                    
                    if not events:
                        return [TextContent(
                            type="text",
                            text=json.dumps({
                                "status": "success",
                                "message": f"No active risk events in {region}",
                                "data": {
                                    "region": region,
                                    "risk_level": "low",
                                    "events": []
                                }
                            }, indent=2)
                        )]
                    
                    risk_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
                    max_severity = max([risk_scores.get(e.severity, 1) for e in events])
                    severity_map = {1: "low", 2: "medium", 3: "high", 4: "critical"}
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": f"Risk assessment for {region}",
                            "data": {
                                "region": region,
                                "risk_level": severity_map[max_severity],
                                "active_events": len(events),
                                "events": [
                                    {
                                        "event_type": e.event_type,
                                        "severity": e.severity,
                                        "description": e.description
                                    }
                                    for e in events
                                ]
                            }
                        }, indent=2)
                    )]
                
                elif name == "get_historical_refunds":
                    component_type = arguments.get("component_type")
                    event_type = arguments.get("event_type")
                    limit = arguments.get("limit", 100)
                    refunds = crud.get_historical_refunds(db, component_type, event_type, limit)
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": f"Retrieved {len(refunds)} historical refunds",
                            "data": [
                                {
                                    "id": r.id,
                                    "component_type": r.component_type,
                                    "event_type": r.event_type,
                                    "refund_percentage": r.refund_percentage,
                                    "refund_amount": r.refund_amount,
                                    "processing_days": r.processing_days
                                }
                                for r in refunds
                            ]
                        }, indent=2)
                    )]
                
                elif name == "get_refund_statistics":
                    stats = crud.get_refund_statistics(db)
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": "Refund statistics retrieved",
                            "data": stats
                        }, indent=2)
                    )]
                
                elif name == "get_provider_policies":
                    provider_type = arguments.get("provider_type")
                    providers = crud.get_providers(db, provider_type)
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": f"Retrieved {len(providers)} provider policies",
                            "data": providers
                        }, indent=2)
                    )]
                
                elif name == "get_provider_policy":
                    provider_name = arguments["provider_name"]
                    policy = crud.get_provider_policy(db, provider_name)
                    if not policy:
                        return [TextContent(
                            type="text",
                            text=json.dumps({
                                "status": "error",
                                "error_type": "not_found",
                                "message": f"Provider '{provider_name}' not found"
                            }, indent=2)
                        )]
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "success",
                            "message": f"Policy for {provider_name} retrieved",
                            "data": policy
                        }, indent=2)
                    )]
                
                else:
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "error",
                            "error_type": "unknown_tool",
                            "message": f"Unknown tool: {name}"
                        }, indent=2)
                    )]
            
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "error",
                        "error_type": "execution_error",
                        "message": str(e)
                    }, indent=2)
                )]
            finally:
                db.close()


# Global MCP server instance
mcp_server = RefundMCPServer()


async def mcp_sse_endpoint(request: Request):
    """
    MCP SSE endpoint handler
    
    This endpoint provides Server-Sent Events (SSE) transport for the MCP protocol.
    Clients can connect to this endpoint to access all refund estimation API tools
    via the MCP protocol.
    
    URL: /mcp
    Method: GET
    Transport: SSE (Server-Sent Events)
    Protocol: MCP (Model Context Protocol)
    """
    async def event_generator():
        """Generate SSE events for MCP protocol"""
        transport = SseServerTransport("/mcp")
        
        async with transport.connect_sse(
            request.scope,
            request.receive,
            request._send
        ) as streams:
            await mcp_server.server.run(
                streams[0],
                streams[1],
                mcp_server.server.create_initialization_options()
            )
    
    return EventSourceResponse(event_generator())

# Made with Bob
