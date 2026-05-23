"""
Production-Ready MCP Server for Travel Refund Uncertainty Estimation System
Optimized for IBM ICA (Intelligent Conversational Agents)

Features:
- Comprehensive error handling
- Request timeouts
- Structured JSON responses
- Logging and monitoring
- Input validation
- Retry logic
"""

import asyncio
import json
import logging
from typing import Any, Optional, Dict
from datetime import datetime
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration
API_BASE_URL = "http://localhost:8000/api"
SERVER_NAME = "refund-estimation-mcp-production"
SERVER_VERSION = "1.0.0"
REQUEST_TIMEOUT = 30.0  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(SERVER_NAME)

# Initialize MCP server
server = Server(SERVER_NAME)


class MCPError(Exception):
    """Custom exception for MCP server errors"""
    def __init__(self, message: str, error_type: str = "internal_error", details: Optional[Dict] = None):
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        super().__init__(self.message)


def create_error_response(error: Exception, tool_name: str) -> Dict:
    """Create structured error response"""
    if isinstance(error, MCPError):
        return {
            "status": "error",
            "error_type": error.error_type,
            "message": error.message,
            "details": error.details,
            "tool": tool_name,
            "timestamp": datetime.utcnow().isoformat()
        }
    elif isinstance(error, httpx.TimeoutException):
        return {
            "status": "error",
            "error_type": "timeout",
            "message": f"Request timed out after {REQUEST_TIMEOUT} seconds",
            "tool": tool_name,
            "timestamp": datetime.utcnow().isoformat()
        }
    elif isinstance(error, httpx.HTTPError):
        return {
            "status": "error",
            "error_type": "http_error",
            "message": str(error),
            "tool": tool_name,
            "timestamp": datetime.utcnow().isoformat()
        }
    else:
        return {
            "status": "error",
            "error_type": "unexpected_error",
            "message": str(error),
            "tool": tool_name,
            "timestamp": datetime.utcnow().isoformat()
        }


def create_success_response(data: Any, tool_name: str, message: str = "Success") -> Dict:
    """Create structured success response"""
    return {
        "status": "success",
        "message": message,
        "data": data,
        "tool": tool_name,
        "timestamp": datetime.utcnow().isoformat()
    }


async def call_api_with_retry(
    endpoint: str,
    method: str = "GET",
    data: Optional[dict] = None,
    max_retries: int = MAX_RETRIES
) -> dict:
    """
    Make HTTP request to FastAPI backend with retry logic
    
    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, PUT, DELETE)
        data: Request body data
        max_retries: Maximum number of retry attempts
    
    Returns:
        dict: API response data
    
    Raises:
        MCPError: On API errors
        httpx.TimeoutException: On timeout
        httpx.HTTPError: On HTTP errors
    """
    url = f"{API_BASE_URL}{endpoint}"
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                logger.info(f"API Request: {method} {url} (Attempt {attempt + 1}/{max_retries})")
                
                if method == "GET":
                    response = await client.get(url)
                elif method == "POST":
                    response = await client.post(url, json=data)
                elif method == "PUT":
                    response = await client.put(url, json=data)
                elif method == "DELETE":
                    response = await client.delete(url)
                else:
                    raise MCPError(f"Unsupported HTTP method: {method}", "invalid_method")
                
                response.raise_for_status()
                result = response.json()
                
                logger.info(f"API Response: {response.status_code} - Success")
                return result
                
        except httpx.TimeoutException as e:
            logger.warning(f"Request timeout (Attempt {attempt + 1}/{max_retries})")
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(RETRY_DELAY)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            # Don't retry on 4xx errors (client errors)
            if 400 <= e.response.status_code < 500:
                raise MCPError(
                    f"API request failed: {e.response.text}",
                    "api_error",
                    {"status_code": e.response.status_code}
                )
            # Retry on 5xx errors (server errors)
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(RETRY_DELAY)
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {str(e)}")
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(RETRY_DELAY)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools for IBM ICA agents
    
    Returns comprehensive tool definitions with:
    - Clear names and descriptions
    - Detailed input schemas
    - Parameter validation rules
    - Usage examples
    """
    return [
        Tool(
            name="create_booking",
            description="""
            Create a new travel booking with multiple components (flight, hotel, visa, insurance).
            
            This tool allows ICA agents to create complete travel bookings on behalf of customers.
            The booking will be assigned a unique reference number and can be used for refund estimation.
            
            Use this when:
            - Customer wants to book travel
            - Need to create booking for refund estimation
            - Setting up test scenarios
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Customer's full name (2-100 characters)",
                        "minLength": 2,
                        "maxLength": 100
                    },
                    "customer_email": {
                        "type": "string",
                        "format": "email",
                        "description": "Customer's email address (must be valid email format)"
                    },
                    "travel_date": {
                        "type": "string",
                        "format": "date-time",
                        "description": "Travel date in ISO 8601 format (e.g., 2026-08-15T10:00:00)"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination city or country (2-100 characters)",
                        "minLength": 2,
                        "maxLength": 100
                    },
                    "origin": {
                        "type": "string",
                        "description": "Origin city or country (2-100 characters)",
                        "minLength": 2,
                        "maxLength": 100
                    },
                    "components": {
                        "type": "array",
                        "description": "List of booking components (at least 1 required)",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "properties": {
                                "component_type": {
                                    "type": "string",
                                    "enum": ["flight", "hotel", "visa", "insurance"],
                                    "description": "Type of booking component"
                                },
                                "provider_name": {
                                    "type": "string",
                                    "description": "Service provider name (e.g., Air India, Marriott)"
                                },
                                "cost": {
                                    "type": "number",
                                    "minimum": 0,
                                    "description": "Component cost in local currency (must be positive)"
                                },
                                "is_refundable": {
                                    "type": "boolean",
                                    "default": False,
                                    "description": "Whether this component is refundable"
                                },
                                "cancellation_fee": {
                                    "type": "number",
                                    "minimum": 0,
                                    "default": 0,
                                    "description": "Cancellation fee amount"
                                }
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
            description="""
            Retrieve all travel bookings with pagination support.
            
            Returns a list of bookings with full details including customer information,
            travel dates, components, and total costs.
            
            Use this when:
            - Need to display list of bookings
            - Searching for specific bookings
            - Exporting booking data
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "skip": {
                        "type": "integer",
                        "minimum": 0,
                        "default": 0,
                        "description": "Number of records to skip for pagination"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 100,
                        "description": "Maximum number of records to return (1-1000)"
                    }
                }
            }
        ),
        
        Tool(
            name="get_booking_details",
            description="""
            Get detailed information about a specific booking by ID.
            
            Returns complete booking details including all components, customer information,
            travel dates, and current status.
            
            Use this when:
            - Need full details of a specific booking
            - Before generating refund estimate
            - Displaying booking to customer
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Unique booking ID (must be positive integer)"
                    }
                },
                "required": ["booking_id"]
            }
        ),
        
        Tool(
            name="estimate_refund",
            description="""
            Generate AI-powered refund estimate for a booking considering force majeure events.
            
            Uses machine learning models trained on historical data to predict expected refund
            amounts with 95% confidence intervals. Considers current global risk events,
            provider policies, and booking components.
            
            Returns:
            - Expected refund amount and percentage
            - 95% confidence interval (lower and upper bounds)
            - Risk score (0-100)
            - Best case, worst case, and most likely scenarios
            - Model version and prediction confidence
            
            Use this when:
            - Customer wants to know potential refund
            - Assessing cancellation options
            - Comparing different scenarios
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Booking ID to estimate refund for"
                    },
                    "selected_model": {
                        "type": "string",
                        "enum": ["auto", "random_forest", "gradient_boosting", "rule_based"],
                        "default": "auto",
                        "description": "ML model to use (auto selects best model)"
                    },
                    "calamity_type": {
                        "type": "string",
                        "enum": ["auto", "war", "pandemic", "natural_disaster", "political_unrest", "terrorism"],
                        "default": "auto",
                        "description": "Type of force majeure event (auto for automatic detection)"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"],
                        "default": "high",
                        "description": "Severity level of the event"
                    }
                },
                "required": ["booking_id"]
            }
        ),
        
        Tool(
            name="get_refund_estimates",
            description="""
            Get all refund estimates generated for a specific booking.
            
            Returns historical estimates showing how predictions changed over time.
            Useful for tracking estimate accuracy and comparing different scenarios.
            
            Use this when:
            - Need estimate history
            - Comparing multiple estimates
            - Analyzing estimate accuracy
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Booking ID to get estimates for"
                    }
                },
                "required": ["booking_id"]
            }
        ),
        
        Tool(
            name="get_risk_events",
            description="""
            Get current global risk events (wars, pandemics, natural disasters, etc.).
            
            Returns list of active force majeure events worldwide with severity levels,
            affected regions, and descriptions.
            
            Use this when:
            - Checking global risk situation
            - Assessing travel safety
            - Understanding refund likelihood
            - Displaying risk warnings
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "active_only": {
                        "type": "boolean",
                        "default": True,
                        "description": "If true, return only currently active events"
                    }
                }
            }
        ),
        
        Tool(
            name="get_regional_risk",
            description="""
            Get risk assessment for a specific region or country.
            
            Returns aggregate risk level (low/medium/high/critical) and list of active
            events affecting the region. Risk level is calculated from maximum severity
            of all active events in the region.
            
            Use this when:
            - Checking destination safety
            - Assessing travel risk
            - Displaying regional warnings
            - Adjusting refund estimates
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "region": {
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 100,
                        "description": "Region or country name (e.g., 'Ukraine', 'Paris', 'Asia')"
                    }
                },
                "required": ["region"]
            }
        ),
        
        Tool(
            name="get_historical_refunds",
            description="""
            Get historical refund data for analysis and trend identification.
            
            Returns historical records showing actual refunds processed, including
            component types, event types, refund percentages, and force majeure status.
            
            Use this when:
            - Analyzing refund trends
            - Training ML models
            - Generating statistics
            - Providing insights to customers
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "component_type": {
                        "type": "string",
                        "enum": ["flight", "hotel", "visa", "insurance"],
                        "description": "Filter by component type (optional)"
                    },
                    "event_type": {
                        "type": "string",
                        "enum": ["war", "pandemic", "natural_disaster", "political_unrest", "terrorism"],
                        "description": "Filter by event type (optional)"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 100,
                        "description": "Maximum records to return (1-1000)"
                    }
                }
            }
        ),
        
        Tool(
            name="get_refund_statistics",
            description="""
            Get aggregated refund statistics by component type and event type.
            
            Returns statistics including average refund percentages, total cases,
            force majeure cases, and average refund amounts grouped by component
            and event type.
            
            Use this when:
            - Displaying statistics dashboard
            - Analyzing refund patterns
            - Comparing refund rates
            - Identifying high-risk scenarios
            """,
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        Tool(
            name="get_provider_policies",
            description="""
            Get refund policies for travel service providers.
            
            Returns list of provider policies including standard refund percentages,
            force majeure refund percentages, cancellation fees, and policy texts.
            
            Use this when:
            - Displaying provider policies
            - Comparing refund policies
            - Calculating expected refunds
            - Informing booking decisions
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "provider_type": {
                        "type": "string",
                        "enum": ["flight", "hotel", "visa", "insurance"],
                        "description": "Filter by provider type (optional)"
                    }
                }
            }
        ),
        
        Tool(
            name="get_provider_policy",
            description="""
            Get detailed refund policy for a specific provider.
            
            Returns complete policy details including refund percentages, cancellation
            fees, processing time, full policy text, and force majeure clause.
            
            Use this when:
            - Need specific provider details
            - Displaying policy to customer
            - Calculating refunds
            - Comparing providers
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "provider_name": {
                        "type": "string",
                        "minLength": 2,
                        "maxLength": 100,
                        "description": "Provider name (e.g., 'Air India', 'Marriott')"
                    }
                },
                "required": ["provider_name"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Handle tool calls from IBM ICA agents with comprehensive error handling
    
    Args:
        name: Tool name
        arguments: Tool arguments
    
    Returns:
        list[TextContent]: Structured JSON response
    """
    try:
        logger.info(f"Tool called: {name} with arguments: {json.dumps(arguments, default=str)}")
        
        # Route to appropriate handler
        if name == "create_booking":
            result = await call_api_with_retry("/bookings", "POST", arguments)
            response = create_success_response(
                result,
                name,
                f"Booking created successfully with reference {result.get('booking_reference', 'N/A')}"
            )
        
        elif name == "get_bookings":
            skip = arguments.get("skip", 0)
            limit = arguments.get("limit", 100)
            result = await call_api_with_retry(f"/bookings?skip={skip}&limit={limit}")
            response = create_success_response(
                result,
                name,
                f"Retrieved {len(result) if isinstance(result, list) else 0} bookings"
            )
        
        elif name == "get_booking_details":
            booking_id = arguments["booking_id"]
            result = await call_api_with_retry(f"/bookings/{booking_id}")
            response = create_success_response(
                result,
                name,
                f"Retrieved booking details for ID {booking_id}"
            )
        
        elif name == "estimate_refund":
            booking_id = arguments["booking_id"]
            request_data = {
                "selected_model": arguments.get("selected_model", "auto"),
                "calamity_type": arguments.get("calamity_type", "auto"),
                "severity": arguments.get("severity", "high")
            }
            result = await call_api_with_retry(f"/estimate-refund/{booking_id}", "POST", request_data)
            response = create_success_response(
                result,
                name,
                f"Refund estimate generated for booking {booking_id}"
            )
        
        elif name == "get_refund_estimates":
            booking_id = arguments["booking_id"]
            result = await call_api_with_retry(f"/estimates/{booking_id}")
            response = create_success_response(
                result,
                name,
                f"Retrieved {len(result) if isinstance(result, list) else 0} estimates"
            )
        
        elif name == "get_risk_events":
            active_only = arguments.get("active_only", True)
            result = await call_api_with_retry(f"/risk-events?active_only={active_only}")
            response = create_success_response(
                result,
                name,
                f"Retrieved {len(result) if isinstance(result, list) else 0} risk events"
            )
        
        elif name == "get_regional_risk":
            region = arguments["region"]
            result = await call_api_with_retry(f"/risk-events/region/{region}")
            response = create_success_response(
                result,
                name,
                f"Retrieved risk assessment for {region}"
            )
        
        elif name == "get_historical_refunds":
            params = []
            if "component_type" in arguments:
                params.append(f"component_type={arguments['component_type']}")
            if "event_type" in arguments:
                params.append(f"event_type={arguments['event_type']}")
            if "limit" in arguments:
                params.append(f"limit={arguments['limit']}")
            
            query = "?" + "&".join(params) if params else ""
            result = await call_api_with_retry(f"/historical-refunds{query}")
            response = create_success_response(
                result,
                name,
                f"Retrieved {len(result) if isinstance(result, list) else 0} historical records"
            )
        
        elif name == "get_refund_statistics":
            result = await call_api_with_retry("/statistics/refund-rates")
            response = create_success_response(
                result,
                name,
                f"Retrieved statistics for {len(result) if isinstance(result, list) else 0} categories"
            )
        
        elif name == "get_provider_policies":
            provider_type = arguments.get("provider_type")
            query = f"?provider_type={provider_type}" if provider_type else ""
            result = await call_api_with_retry(f"/providers{query}")
            response = create_success_response(
                result,
                name,
                f"Retrieved {len(result) if isinstance(result, list) else 0} provider policies"
            )
        
        elif name == "get_provider_policy":
            provider_name = arguments["provider_name"]
            result = await call_api_with_retry(f"/providers/{provider_name}")
            response = create_success_response(
                result,
                name,
                f"Retrieved policy for {provider_name}"
            )
        
        else:
            raise MCPError(f"Unknown tool: {name}", "unknown_tool")
        
        logger.info(f"Tool {name} completed successfully")
        return [TextContent(
            type="text",
            text=json.dumps(response, indent=2, default=str)
        )]
    
    except MCPError as e:
        logger.error(f"MCP Error in {name}: {e.message}")
        error_response = create_error_response(e, name)
        return [TextContent(
            type="text",
            text=json.dumps(error_response, indent=2)
        )]
    
    except httpx.TimeoutException as e:
        logger.error(f"Timeout in {name}: Request exceeded {REQUEST_TIMEOUT} seconds")
        error_response = create_error_response(e, name)
        return [TextContent(
            type="text",
            text=json.dumps(error_response, indent=2)
        )]
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP Error in {name}: {str(e)}")
        error_response = create_error_response(e, name)
        return [TextContent(
            type="text",
            text=json.dumps(error_response, indent=2)
        )]
    
    except Exception as e:
        logger.error(f"Unexpected error in {name}: {str(e)}", exc_info=True)
        error_response = create_error_response(e, name)
        return [TextContent(
            type="text",
            text=json.dumps(error_response, indent=2)
        )]


async def main():
    """Run the production MCP server"""
    logger.info(f"Starting {SERVER_NAME} v{SERVER_VERSION}")
    logger.info(f"API Base URL: {API_BASE_URL}")
    logger.info(f"Request Timeout: {REQUEST_TIMEOUT}s")
    logger.info(f"Max Retries: {MAX_RETRIES}")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
