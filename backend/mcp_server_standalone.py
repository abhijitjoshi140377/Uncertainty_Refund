"""
Standalone MCP Server using FastMCP
Run this separately from the main FastAPI app
"""

import asyncio
from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, List, Optional
from datetime import datetime

from models.database import get_db
from services.refund_estimator import RefundEstimator
from schemas import BookingCreate, BookingComponentCreate, RefundEstimateRequest
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
    """Create a new travel booking with multiple components."""
    db = next(get_db())
    try:
        travel_date_obj = datetime.fromisoformat(travel_date.replace('Z', '+00:00'))
        booking_components = [BookingComponentCreate(**comp) for comp in components]
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
            "total_cost": result.total_cost
        }
    finally:
        db.close()


@mcp.tool()
def get_bookings(skip: int = 0, limit: int = 100) -> Dict[str, Any]:
    """Retrieve paginated list of all travel bookings."""
    db = next(get_db())
    try:
        bookings = crud.get_bookings(db, skip=skip, limit=min(limit, 1000))
        total = crud.get_bookings_count(db)
        return {
            "total": total,
            "bookings": [
                {
                    "id": b.id,
                    "booking_reference": b.booking_reference,
                    "customer_name": b.customer_name,
                    "destination": b.destination,
                    "total_cost": b.total_cost
                }
                for b in bookings
            ]
        }
    finally:
        db.close()


# Add other tools...
# (Keeping it simple for now to test)

if __name__ == "__main__":
    # Run the MCP server on port 8001
    print("Starting MCP Server on http://localhost:8001/mcp")
    mcp.run(transport="streamable-http", port=8001, path="/mcp")

# Made with Bob
