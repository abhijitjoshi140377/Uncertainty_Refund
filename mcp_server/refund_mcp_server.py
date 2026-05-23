"""
MCP Server for Travel Refund Uncertainty Estimation System
Wraps FastAPI endpoints for consumption by ICA (Intelligent Conversational Agents)
"""

import asyncio
import json
from typing import Any, Optional
from datetime import datetime
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Configuration
API_BASE_URL = "http://localhost:8000/api"
SERVER_NAME = "refund-estimation-mcp"
SERVER_VERSION = "1.0.0"

# Initialize MCP server
server = Server(SERVER_NAME)


# Helper function to make API calls
async def call_api(endpoint: str, method: str = "GET", data: Optional[dict] = None) -> dict:
    """Make HTTP request to FastAPI backend"""
    url = f"{API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                response = await client.get(url)
            elif method == "POST":
                response = await client.post(url, json=data)
            elif method == "PUT":
                response = await client.put(url, json=data)
            elif method == "DELETE":
                response = await client.delete(url)
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e), "status": "failed"}


# Tool 1: Create Booking
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools for ICA agents"""
    return [
        Tool(
            name="create_booking",
            description="Create a new travel booking with flight, hotel, visa, and insurance components",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Customer's full name"
                    },
                    "customer_email": {
                        "type": "string",
                        "description": "Customer's email address"
                    },
                    "travel_date": {
                        "type": "string",
                        "description": "Travel date in ISO format (YYYY-MM-DDTHH:MM:SS)"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination city/country"
                    },
                    "origin": {
                        "type": "string",
                        "description": "Origin city/country"
                    },
                    "components": {
                        "type": "array",
                        "description": "List of booking components (flight, hotel, visa, insurance)",
                        "items": {
                            "type": "object",
                            "properties": {
                                "component_type": {"type": "string"},
                                "provider_name": {"type": "string"},
                                "cost": {"type": "number"},
                                "is_refundable": {"type": "boolean"},
                                "cancellation_fee": {"type": "number"}
                            },
                            "required": ["component_type", "provider_name", "cost"]
                        }
                    }
                },
                "required": ["customer_name", "customer_email", "travel_date", "destination", "origin", "components"]
            }
        ),
        Tool(
            name="get_bookings",
            description="Retrieve all travel bookings with optional pagination",
            inputSchema={
                "type": "object",
                "properties": {
                    "skip": {
                        "type": "integer",
                        "description": "Number of records to skip (default: 0)",
                        "default": 0
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records to return (default: 100)",
                        "default": 100
                    }
                }
            }
        ),
        Tool(
            name="get_booking_details",
            description="Get detailed information about a specific booking by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "integer",
                        "description": "Unique booking ID"
                    }
                },
                "required": ["booking_id"]
            }
        ),
        Tool(
            name="estimate_refund",
            description="Generate AI-powered refund estimate for a booking considering force majeure events",
            inputSchema={
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "integer",
                        "description": "Booking ID to estimate refund for"
                    },
                    "selected_model": {
                        "type": "string",
                        "description": "ML model to use: auto, random_forest, gradient_boosting, rule_based",
                        "default": "auto"
                    },
                    "calamity_type": {
                        "type": "string",
                        "description": "Type of calamity: auto, war, pandemic, natural_disaster, political_unrest",
                        "default": "auto"
                    },
                    "severity": {
                        "type": "string",
                        "description": "Severity level: low, medium, high, critical",
                        "default": "high"
                    }
                },
                "required": ["booking_id"]
            }
        ),
        Tool(
            name="get_refund_estimates",
            description="Get all refund estimates generated for a specific booking",
            inputSchema={
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "integer",
                        "description": "Booking ID to get estimates for"
                    }
                },
                "required": ["booking_id"]
            }
        ),
        Tool(
            name="get_risk_events",
            description="Get current global risk events (wars, pandemics, natural disasters)",
            inputSchema={
                "type": "object",
                "properties": {
                    "active_only": {
                        "type": "boolean",
                        "description": "Return only active events (default: true)",
                        "default": True
                    }
                }
            }
        ),
        Tool(
            name="get_regional_risk",
            description="Get risk assessment for a specific region/country",
            inputSchema={
                "type": "object",
                "properties": {
                    "region": {
                        "type": "string",
                        "description": "Region or country name"
                    }
                },
                "required": ["region"]
            }
        ),
        Tool(
            name="get_historical_refunds",
            description="Get historical refund data for analysis and trends",
            inputSchema={
                "type": "object",
                "properties": {
                    "component_type": {
                        "type": "string",
                        "description": "Filter by component: flight, hotel, visa, insurance"
                    },
                    "event_type": {
                        "type": "string",
                        "description": "Filter by event: war, pandemic, natural_disaster, political_unrest"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum records to return (default: 100)",
                        "default": 100
                    }
                }
            }
        ),
        Tool(
            name="get_refund_statistics",
            description="Get aggregated refund statistics by component type and event type",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_provider_policies",
            description="Get refund policies for travel service providers",
            inputSchema={
                "type": "object",
                "properties": {
                    "provider_type": {
                        "type": "string",
                        "description": "Filter by provider type: airline, hotel, visa_service, insurance"
                    }
                }
            }
        ),
        Tool(
            name="get_provider_policy",
            description="Get detailed refund policy for a specific provider",
            inputSchema={
                "type": "object",
                "properties": {
                    "provider_name": {
                        "type": "string",
                        "description": "Name of the provider"
                    }
                },
                "required": ["provider_name"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls from ICA agents"""
    
    try:
        if name == "create_booking":
            result = await call_api("/bookings", "POST", arguments)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_bookings":
            skip = arguments.get("skip", 0)
            limit = arguments.get("limit", 100)
            result = await call_api(f"/bookings?skip={skip}&limit={limit}")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_booking_details":
            booking_id = arguments["booking_id"]
            result = await call_api(f"/bookings/{booking_id}")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "estimate_refund":
            booking_id = arguments["booking_id"]
            request_data = {
                "selected_model": arguments.get("selected_model", "auto"),
                "calamity_type": arguments.get("calamity_type", "auto"),
                "severity": arguments.get("severity", "high")
            }
            result = await call_api(f"/estimate-refund/{booking_id}", "POST", request_data)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_refund_estimates":
            booking_id = arguments["booking_id"]
            result = await call_api(f"/estimates/{booking_id}")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_risk_events":
            active_only = arguments.get("active_only", True)
            result = await call_api(f"/risk-events?active_only={active_only}")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_regional_risk":
            region = arguments["region"]
            result = await call_api(f"/risk-events/region/{region}")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_historical_refunds":
            params = []
            if "component_type" in arguments:
                params.append(f"component_type={arguments['component_type']}")
            if "event_type" in arguments:
                params.append(f"event_type={arguments['event_type']}")
            if "limit" in arguments:
                params.append(f"limit={arguments['limit']}")
            
            query = "?" + "&".join(params) if params else ""
            result = await call_api(f"/historical-refunds{query}")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_refund_statistics":
            result = await call_api("/statistics/refund-rates")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_provider_policies":
            provider_type = arguments.get("provider_type")
            query = f"?provider_type={provider_type}" if provider_type else ""
            result = await call_api(f"/providers{query}")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        elif name == "get_provider_policy":
            provider_name = arguments["provider_name"]
            result = await call_api(f"/providers/{provider_name}")
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"})
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e), "tool": name})
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
