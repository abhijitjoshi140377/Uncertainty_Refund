"""
Simple MCP HTTP endpoint for ICA integration
Uses basic HTTP POST for tool calls
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import httpx
import json

router = APIRouter()

# Define available tools
TOOLS = [
    {
        "name": "get_bookings",
        "description": "Get all travel bookings",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_booking_details",
        "description": "Get detailed information for a specific booking",
        "inputSchema": {
            "type": "object",
            "properties": {
                "booking_id": {
                    "type": "integer",
                    "description": "The booking ID"
                }
            },
            "required": ["booking_id"]
        }
    },
    {
        "name": "estimate_refund",
        "description": "Estimate refund amount for a booking with confidence intervals",
        "inputSchema": {
            "type": "object",
            "properties": {
                "booking_id": {
                    "type": "integer",
                    "description": "The booking ID"
                },
                "severity": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Severity level of the force majeure event"
                },
                "event_type": {
                    "type": "string",
                    "enum": ["war", "pandemic", "natural_disaster", "political_unrest", "terrorism"],
                    "description": "Type of force majeure event"
                }
            },
            "required": ["booking_id", "severity", "event_type"]
        }
    },
    {
        "name": "get_risk_events",
        "description": "Get current global risk events affecting travel",
        "inputSchema": {
            "type": "object",
            "properties": {
                "active_only": {
                    "type": "boolean",
                    "description": "Filter to show only active events",
                    "default": True
                }
            },
            "required": []
        }
    },
    {
        "name": "get_regional_risk",
        "description": "Get risk assessment for a specific region",
        "inputSchema": {
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "Region name (e.g., 'Ukraine', 'Middle East')"
                }
            },
            "required": ["region"]
        }
    },
    {
        "name": "get_refund_statistics",
        "description": "Get historical refund statistics",
        "inputSchema": {
            "type": "object",
            "properties": {
                "component_type": {
                    "type": "string",
                    "enum": ["flight", "hotel", "visa", "insurance"],
                    "description": "Filter by component type"
                },
                "event_type": {
                    "type": "string",
                    "enum": ["war", "pandemic", "natural_disaster", "political_unrest", "terrorism"],
                    "description": "Filter by event type"
                }
            },
            "required": []
        }
    },
    {
        "name": "get_provider_policies",
        "description": "Get refund policies for travel providers",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

@router.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    Simple MCP HTTP endpoint that handles tool calls (JSON-RPC 2.0)
    """
    try:
        # Log the incoming request
        body = await request.json()
        print(f"[MCP] Received request: {json.dumps(body, indent=2)}")
        
        method = body.get("method")
        request_id = body.get("id", 0)
        
        # Handle initialize request
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "RefundEstimationAPI",
                        "version": "1.0.0"
                    }
                }
            }
            print(f"[MCP] Sending response: {json.dumps(response, indent=2)}")
            return JSONResponse(response)
        
        # Handle tools/list request
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": TOOLS
                }
            }
            print(f"[MCP] Sending tools list")
            return JSONResponse(response)
        
        # Handle tools/call request
        elif method == "tools/call":
            tool_name = body.get("params", {}).get("name")
            arguments = body.get("params", {}).get("arguments", {})
            
            print(f"[MCP] Calling tool: {tool_name} with args: {arguments}")
            
            # Call the appropriate internal API
            result = await call_internal_api(tool_name, arguments)
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            return JSONResponse(response)
        
        else:
            print(f"[MCP] Unknown method: {method}")
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            })
            
    except json.JSONDecodeError as e:
        print(f"[MCP] JSON decode error: {e}")
        return JSONResponse({
            "error": "Invalid JSON in request body"
        }, status_code=400)
    except Exception as e:
        print(f"[MCP] Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({
            "error": str(e)
        }, status_code=500)

async def call_internal_api(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call internal API endpoints based on tool name
    """
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        try:
            if tool_name == "get_bookings":
                response = await client.get(f"{base_url}/api/bookings")
                return response.json()
            
            elif tool_name == "get_booking_details":
                booking_id = arguments.get("booking_id")
                response = await client.get(f"{base_url}/api/bookings/{booking_id}")
                return response.json()
            
            elif tool_name == "estimate_refund":
                booking_id = arguments.get("booking_id")
                payload = {
                    "severity": arguments.get("severity"),
                    "event_type": arguments.get("event_type")
                }
                response = await client.post(
                    f"{base_url}/api/estimate-refund/{booking_id}",
                    json=payload
                )
                return response.json()
            
            elif tool_name == "get_risk_events":
                active_only = arguments.get("active_only", True)
                response = await client.get(
                    f"{base_url}/api/risk-events",
                    params={"active_only": active_only}
                )
                return response.json()
            
            elif tool_name == "get_regional_risk":
                region = arguments.get("region")
                response = await client.get(f"{base_url}/api/risk-events/regional/{region}")
                return response.json()
            
            elif tool_name == "get_refund_statistics":
                params = {}
                if "component_type" in arguments:
                    params["component_type"] = arguments["component_type"]
                if "event_type" in arguments:
                    params["event_type"] = arguments["event_type"]
                response = await client.get(
                    f"{base_url}/api/statistics/refund-rates",
                    params=params
                )
                return response.json()
            
            elif tool_name == "get_provider_policies":
                response = await client.get(f"{base_url}/api/provider-policies")
                return response.json()
            
            else:
                return {"error": f"Unknown tool: {tool_name}"}
                
        except Exception as e:
            return {"error": str(e)}

# Made with Bob
