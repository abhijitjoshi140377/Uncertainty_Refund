# MCP SSE Endpoint Integration Guide

## Overview

The FastAPI backend now includes a **native MCP (Model Context Protocol) SSE endpoint** at `/mcp` that exposes all 11 API tools using the MCP protocol with Server-Sent Events (SSE) transport.

## What is MCP SSE?

**MCP (Model Context Protocol)** is a standardized protocol for AI agents to interact with tools and services. The **SSE (Server-Sent Events)** transport allows real-time, bidirectional communication between AI agents and the API.

### Key Benefits

✅ **Native Integration** - Built directly into FastAPI backend  
✅ **Real-Time Communication** - SSE transport for instant responses  
✅ **Standardized Protocol** - MCP-compliant for all AI agents  
✅ **11 Production Tools** - All API endpoints exposed as MCP tools  
✅ **Structured Responses** - Consistent JSON format  
✅ **Error Handling** - Comprehensive error responses  
✅ **No External Server** - No need for separate MCP server process  

## Endpoint Details

### URL
- **Local**: `http://localhost:8000/mcp`
- **Ngrok**: `https://famished-vertebrae-basil.ngrok-free.dev/mcp`
- **Production**: `https://your-domain.com/mcp`

### Method
`GET` (SSE connection)

### Protocol
MCP (Model Context Protocol) v1.0

### Transport
SSE (Server-Sent Events)

## Available Tools

The MCP endpoint exposes 11 tools:

### 1. create_booking
Create travel bookings with multiple components (flights, hotels, visa, insurance).

**Input Schema:**
```json
{
  "customer_name": "string (required)",
  "customer_email": "string (email, required)",
  "booking_date": "string (ISO 8601, required)",
  "travel_start_date": "string (ISO 8601, required)",
  "travel_end_date": "string (ISO 8601, required)",
  "destination_country": "string (required)",
  "total_cost": "number (required)",
  "components": [
    {
      "component_type": "flight|hotel|visa|insurance (required)",
      "provider": "string (required)",
      "cost": "number (required)",
      "booking_reference": "string (optional)",
      "cancellation_policy": "string (optional)"
    }
  ]
}
```

### 2. get_bookings
List all bookings with pagination.

**Input Schema:**
```json
{
  "skip": "integer (default: 0)",
  "limit": "integer (default: 100, max: 1000)"
}
```

### 3. get_booking_details
Get detailed information for a specific booking.

**Input Schema:**
```json
{
  "booking_id": "integer (required)"
}
```

### 4. estimate_refund
AI-powered refund estimation using ML models.

**Input Schema:**
```json
{
  "booking_id": "integer (required)",
  "selected_model": "auto|random_forest|gradient_boosting|rule_based (default: auto)",
  "calamity_type": "natural_disaster|political_unrest|pandemic|terrorism|economic_crisis|other (default: natural_disaster)",
  "severity": "low|medium|high|critical (default: medium)"
}
```

### 5. get_refund_estimates
Get all refund estimates for a booking.

**Input Schema:**
```json
{
  "booking_id": "integer (required)"
}
```

### 6. get_risk_events
Query current global risk events.

**Input Schema:**
```json
{
  "active_only": "boolean (default: true)"
}
```

### 7. get_regional_risk
Get risk assessment for a specific region.

**Input Schema:**
```json
{
  "region": "string (required)"
}
```

### 8. get_historical_refunds
Access historical refund data.

**Input Schema:**
```json
{
  "component_type": "flight|hotel|visa|insurance (optional)",
  "event_type": "string (optional)",
  "limit": "integer (default: 100, max: 1000)"
}
```

### 9. get_refund_statistics
Get aggregated refund statistics.

**Input Schema:**
```json
{}
```

### 10. get_provider_policies
Query provider refund policies.

**Input Schema:**
```json
{
  "provider_type": "string (optional)"
}
```

### 11. get_provider_policy
Get specific provider policy details.

**Input Schema:**
```json
{
  "provider_name": "string (required)"
}
```

## Response Format

All tools return structured JSON responses:

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {
    // Tool-specific response data
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error_type": "not_found|execution_error|unknown_tool",
  "message": "Error description"
}
```

## Setup and Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New dependencies added:**
- `mcp==0.9.0` - MCP Python SDK
- `sse-starlette==1.8.2` - SSE support for FastAPI

### 2. Start Backend

```bash
python main.py
```

The MCP endpoint will be available at: `http://localhost:8000/mcp`

### 3. Verify Endpoint

Check the API documentation:
- Swagger UI: `http://localhost:8000/api/docs`
- Look for the `/mcp` endpoint

## Using with AI Agents

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "refund-estimation-sse": {
      "url": "http://localhost:8000/mcp",
      "transport": "sse"
    }
  }
}
```

### Cline (VS Code)

Add to MCP settings:

```json
{
  "mcpServers": {
    "refund-estimation-sse": {
      "url": "http://localhost:8000/mcp",
      "transport": "sse"
    }
  }
}
```

### Custom MCP Client

```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("http://localhost:8000/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Call a tool
            result = await session.call_tool(
                "get_bookings",
                arguments={"skip": 0, "limit": 10}
            )
            print(result)

asyncio.run(main())
```

## Ngrok Integration

### Setup Ngrok Tunnel

```bash
# Install ngrok
# Download from https://ngrok.com/download

# Start ngrok tunnel
ngrok http 8000
```

You'll get a URL like: `https://famished-vertebrae-basil.ngrok-free.app`

### Configure AI Agent

Use the ngrok URL for the MCP endpoint:

```json
{
  "mcpServers": {
    "refund-estimation-sse": {
      "url": "https://famished-vertebrae-basil.ngrok-free.app/mcp",
      "transport": "sse"
    }
  }
}
```

### CORS Configuration

The backend already includes CORS middleware, but you may need to add your ngrok domain:

```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://famished-vertebrae-basil.ngrok-free.app"  # Add ngrok URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Example Usage

### Example 1: Create Booking

**MCP Tool Call:**
```json
{
  "tool": "create_booking",
  "arguments": {
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "booking_date": "2026-05-20T10:00:00Z",
    "travel_start_date": "2026-06-01T10:00:00Z",
    "travel_end_date": "2026-06-15T10:00:00Z",
    "destination_country": "France",
    "total_cost": 75000,
    "components": [
      {
        "component_type": "flight",
        "provider": "Air India",
        "cost": 50000,
        "booking_reference": "AI123456",
        "cancellation_policy": "50% refund if cancelled 7 days before"
      },
      {
        "component_type": "hotel",
        "provider": "Taj Hotels",
        "cost": 25000,
        "booking_reference": "TAJ789",
        "cancellation_policy": "Full refund if cancelled 3 days before"
      }
    ]
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Booking created successfully with reference BK12345678",
  "data": {
    "id": 1,
    "booking_reference": "BK12345678",
    "customer_name": "John Doe",
    "total_cost": 75000
  }
}
```

### Example 2: Estimate Refund

**MCP Tool Call:**
```json
{
  "tool": "estimate_refund",
  "arguments": {
    "booking_id": 1,
    "selected_model": "auto",
    "calamity_type": "natural_disaster",
    "severity": "high"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Refund estimate generated successfully",
  "data": {
    "booking_id": 1,
    "expected_refund_amount": 52500,
    "expected_refund_percentage": 70,
    "confidence_interval_lower": 45000,
    "confidence_interval_upper": 60000,
    "risk_score": 75,
    "best_case_refund": 60000,
    "worst_case_refund": 45000,
    "most_likely_refund": 52500,
    "model_used": "random_forest",
    "prediction_confidence": 0.85
  }
}
```

### Example 3: Regional Risk Assessment

**MCP Tool Call:**
```json
{
  "tool": "get_regional_risk",
  "arguments": {
    "region": "Ukraine"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Risk assessment for Ukraine",
  "data": {
    "region": "Ukraine",
    "risk_level": "high",
    "active_events": 2,
    "events": [
      {
        "event_type": "political_unrest",
        "severity": "high",
        "description": "Ongoing conflict in eastern regions"
      },
      {
        "event_type": "economic_crisis",
        "severity": "medium",
        "description": "Currency instability"
      }
    ]
  }
}
```

## AI Agent Conversation Examples

### Example 1: Booking and Refund Estimation

```
User: I need to book a trip to France for June 2026

Agent: I'll create a booking for you using the create_booking tool...
[Calls create_booking with provided details]

Agent: Your booking has been created with reference BK12345678.
Total cost: ₹75,000. Would you like me to estimate potential refunds?

User: Yes, what if there's a natural disaster?

Agent: Let me estimate that using the estimate_refund tool...
[Calls estimate_refund with booking_id=1, calamity_type="natural_disaster", severity="high"]

Agent: Based on AI prediction:
- Expected refund: ₹52,500 (70%)
- 95% confidence interval: ₹45,000 - ₹60,000
- Risk score: 75/100
- Best case: ₹60,000
- Worst case: ₹45,000
```

### Example 2: Risk Assessment

```
User: Is it safe to travel to Ukraine right now?

Agent: Let me check the current risk level...
[Calls get_regional_risk with region="Ukraine"]

Agent: Based on current data:
- Risk Level: HIGH
- Active Events: 2
  1. Political unrest (high severity) - Ongoing conflict in eastern regions
  2. Economic crisis (medium severity) - Currency instability

I would advise against non-essential travel to Ukraine at this time.
```

### Example 3: Provider Policy Check

```
User: What's Air India's cancellation policy?

Agent: Let me look that up...
[Calls get_provider_policy with provider_name="Air India"]

Agent: Air India's cancellation policy:
- Cancellation fee: 20% of ticket price
- Refund percentage: 80% if cancelled 7+ days before departure
- Force majeure clause: Full refund for natural disasters and pandemics
- Processing time: 7-14 business days
```

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Agent (Claude, GPT)                  │
└─────────────────────────┬───────────────────────────────────┘
                          │ MCP Protocol (SSE)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (/mcp endpoint)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           MCP Server (mcp_endpoint.py)               │  │
│  │  - Tool Registration                                 │  │
│  │  - Request Handling                                  │  │
│  │  - Response Formatting                               │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              CRUD Operations (crud.py)               │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │         SQLAlchemy ORM + SQLite Database             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

1. **AI Agent** connects to `/mcp` endpoint via SSE
2. **MCP Server** lists available tools
3. **AI Agent** calls a tool with JSON arguments
4. **MCP Server** validates input schema
5. **CRUD Layer** executes database operations
6. **MCP Server** formats response as JSON
7. **AI Agent** receives structured response

## Error Handling

### Not Found Errors
```json
{
  "status": "error",
  "error_type": "not_found",
  "message": "Booking 999 not found"
}
```

### Execution Errors
```json
{
  "status": "error",
  "error_type": "execution_error",
  "message": "Invalid date format: expected ISO 8601"
}
```

### Unknown Tool Errors
```json
{
  "status": "error",
  "error_type": "unknown_tool",
  "message": "Unknown tool: invalid_tool_name"
}
```

## Testing

### Test with curl (SSE)

```bash
curl -N -H "Accept: text/event-stream" http://localhost:8000/mcp
```

### Test with Python

```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def test_mcp():
    async with sse_client("http://localhost:8000/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test list tools
            tools = await session.list_tools()
            print(f"✅ Found {len(tools.tools)} tools")
            
            # Test get_bookings
            result = await session.call_tool("get_bookings", {"limit": 5})
            print(f"✅ Retrieved bookings: {result}")

asyncio.run(test_mcp())
```

### Test with MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector http://localhost:8000/mcp
```

## Production Deployment

### 1. Update CORS Origins

```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-production-domain.com",
        "https://your-ai-agent-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Use HTTPS

Ensure your production server uses HTTPS:
- `https://api.yourcompany.com/mcp`

### 3. Add Authentication (Optional)

```python
from fastapi import Header, HTTPException

@app.get("/mcp")
async def mcp_endpoint(
    request: Request,
    authorization: str = Header(None)
):
    # Validate API key
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return await mcp_sse_endpoint(request)
```

### 4. Monitor Performance

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Troubleshooting

### Issue: Connection Refused

**Solution:**
1. Verify backend is running: `http://localhost:8000/api/docs`
2. Check if port 8000 is available
3. Ensure no firewall blocking

### Issue: SSE Connection Drops

**Solution:**
1. Check network stability
2. Increase timeout settings
3. Implement reconnection logic in client

### Issue: Tool Not Found

**Solution:**
1. Verify tool name matches exactly (case-sensitive)
2. Check tool is registered in `mcp_endpoint.py`
3. Restart backend to reload tools

### Issue: Invalid Arguments

**Solution:**
1. Validate JSON schema matches tool input schema
2. Check required fields are present
3. Verify data types (string, integer, etc.)
4. Ensure enum values are exact matches

## Benefits Over Standalone MCP Server

### ✅ Simplified Architecture
- No separate MCP server process
- Single backend handles both REST and MCP
- Easier deployment and maintenance

### ✅ Shared Resources
- Same database connection pool
- Shared ML models and estimator
- Consistent error handling

### ✅ Better Performance
- No network overhead between services
- Direct function calls
- Reduced latency

### ✅ Easier Development
- Single codebase
- Unified logging
- Consistent configuration

## Documentation

- **API Documentation**: `http://localhost:8000/api/docs`
- **MCP Endpoint**: `http://localhost:8000/mcp`
- **Backend Code**: `backend/mcp_endpoint.py`
- **Main Application**: `backend/main.py`

## Support

For issues or questions:
1. Check API documentation at `/api/docs`
2. Review error messages in structured responses
3. Check backend logs for detailed error traces
4. Refer to MCP protocol documentation

## Conclusion

The MCP SSE endpoint provides a **native, production-ready** integration of the Model Context Protocol directly into the FastAPI backend. This allows AI agents to seamlessly access all 11 refund estimation tools using standardized MCP protocol with real-time SSE transport.

**Key Advantages:**
✅ Native FastAPI integration  
✅ Real-time SSE communication  
✅ 11 production-ready tools  
✅ Structured JSON responses  
✅ Comprehensive error handling  
✅ Easy deployment with ngrok  
✅ Compatible with all MCP clients  

**Next Steps:**
1. Install dependencies: `pip install -r requirements.txt`
2. Start backend: `python main.py`
3. Configure AI agent with MCP endpoint URL
4. Test tools with your AI agent
5. Deploy to production with HTTPS