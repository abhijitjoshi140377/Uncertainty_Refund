# MCP HTTP Endpoint Integration Guide

## Overview

The FastAPI backend now includes a **native MCP (Model Context Protocol) HTTP endpoint** at `/mcp` that uses **streamable HTTP transport** with **JSON-RPC 2.0 protocol**. This is specifically designed for **IBM Context Forge** and other MCP clients that expect POST requests (not SSE).

**Implementation**: Uses `FastMCP.streamable_http_app()` to mount the MCP server at `/mcp` endpoint.

## Critical Protocol Details

### ✅ Streamable HTTP Transport
- **Method**: POST (not GET)
- **Protocol**: JSON-RPC 2.0
- **Content-Type**: application/json
- **Endpoint**: `/mcp`

### ❌ NOT Server-Sent Events (SSE)
This implementation uses **streamable HTTP**, not SSE. IBM Context Forge expects:
- ✅ `POST /mcp` → JSON-RPC request/response
- ❌ `GET /mcp` → SSE stream

## Endpoint Details

### URL
- **Local**: `http://localhost:8000/mcp`
- **Ngrok**: `https://famished-vertebrae-basil.ngrok-free.app/mcp`
- **Production**: `https://your-domain.com/mcp`

### Method
`POST` with JSON-RPC 2.0 payload

### Protocol
MCP (Model Context Protocol) with JSON-RPC 2.0

### Transport
Streamable HTTP (not SSE)

## JSON-RPC 2.0 Protocol

### Request Format
```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "params": { /* method parameters */ },
  "id": 1
}
```

### Response Format
```json
{
  "jsonrpc": "2.0",
  "result": { /* method result */ },
  "id": 1
}
```

### Error Response Format
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Error description",
    "data": { /* additional error info */ }
  },
  "id": 1
}
```

## MCP Methods

### 1. initialize
Handshake to establish MCP connection.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "context-forge",
      "version": "1.0.0"
    }
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "Travel Refund Estimation API",
      "version": "1.0.0"
    }
  },
  "id": 1
}
```

### 2. tools/list
List all available MCP tools.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 2
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "create_booking",
        "description": "Create a new travel booking...",
        "inputSchema": {
          "type": "object",
          "properties": { /* ... */ },
          "required": [ /* ... */ ]
        }
      },
      // ... 10 more tools
    ]
  },
  "id": 2
}
```

### 3. tools/call
Execute a specific tool.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_bookings",
    "arguments": {
      "skip": 0,
      "limit": 10
    }
  },
  "id": 3
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"total\": 5, \"bookings\": [...]}"
      }
    ]
  },
  "id": 3
}
```

## Available Tools (11)

All tools are automatically registered from the existing FastAPI backend routes:

### 1. create_booking
Create a new travel booking with multiple components.

**Arguments:**
- `customer_name` (string, required): Customer full name
- `customer_email` (string, required): Valid email address
- `travel_date` (string, required): ISO 8601 date-time
- `destination` (string, required): Destination location
- `origin` (string, required): Origin location
- `components` (array, required): List of booking components
  - `component_type`: "flight", "hotel", "visa", or "insurance"
  - `provider_name`: Provider name
  - `cost`: Component cost (> 0)
  - `refund_policy`: Optional policy description
  - `is_refundable`: Boolean
  - `cancellation_fee`: Fee amount (default: 0.0)

**Returns:** Booking details with ID, reference, and components

### 2. get_bookings
Retrieve paginated list of all bookings.

**Arguments:**
- `skip` (integer, optional): Records to skip (default: 0)
- `limit` (integer, optional): Max records (default: 100, max: 1000)

**Returns:** Total count and list of bookings

### 3. get_booking_details
Get detailed information for a specific booking.

**Arguments:**
- `booking_id` (integer, required): Booking ID

**Returns:** Complete booking details with all components

### 4. estimate_refund
AI-powered refund estimation using ML models.

**Arguments:**
- `booking_id` (integer, required): Booking ID
- `selected_model` (string, optional): "auto", "random_forest", "gradient_boosting", "rule_based" (default: "auto")
- `calamity_type` (string, optional): Event type (default: "auto")
- `severity` (string, optional): "low", "medium", "high", "critical" (default: "high")

**Returns:** Refund estimate with confidence intervals, risk score, scenarios

### 5. get_refund_estimates
Get all refund estimates for a booking.

**Arguments:**
- `booking_id` (integer, required): Booking ID

**Returns:** List of all estimates with history

### 6. get_risk_events
Query current global risk events.

**Arguments:**
- `active_only` (boolean, optional): Filter active events (default: true)

**Returns:** List of risk events with severity and regions

### 7. get_regional_risk
Get risk assessment for a specific region.

**Arguments:**
- `region` (string, required): Region name (e.g., "Ukraine")

**Returns:** Risk level and active events in region

### 8. get_historical_refunds
Access historical refund data.

**Arguments:**
- `component_type` (string, optional): Filter by type
- `event_type` (string, optional): Filter by event
- `limit` (integer, optional): Max records (default: 100, max: 1000)

**Returns:** Historical refund records

### 9. get_refund_statistics
Get aggregated refund statistics.

**Arguments:** None

**Returns:** Statistics grouped by component and event type

### 10. get_provider_policies
Query provider refund policies.

**Arguments:**
- `provider_type` (string, optional): Filter by provider type

**Returns:** List of provider policies

### 11. get_provider_policy
Get specific provider policy details.

**Arguments:**
- `provider_name` (string, required): Provider name

**Returns:** Complete provider policy

## Setup and Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Key dependency:**
- `mcp==1.1.2` - Official MCP Python SDK with FastMCP

### 2. Start Backend

```bash
python main.py
```

The MCP endpoint will be available at: `http://localhost:8000/mcp`

### 3. Verify Endpoint

```bash
# Test initialize handshake
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {},
    "id": 1
  }'
```

## IBM Context Forge Integration

### Add MCP Server

1. Open IBM Context Forge
2. Navigate to "Add New Tool from REST API"
3. Select "MCP Server"
4. Enter MCP Server URL:
   - Local: `http://localhost:8000/mcp`
   - Ngrok: `https://famished-vertebrae-basil.ngrok-free.app/mcp`
5. Protocol: **MCP (JSON-RPC 2.0)**
6. Transport: **HTTP** (not SSE)
7. Click "Connect"

### Configuration

```json
{
  "name": "refund-estimation-mcp",
  "url": "http://localhost:8000/mcp",
  "protocol": "mcp",
  "transport": "http",
  "method": "POST"
}
```

## Testing

### Run Test Suite

```bash
cd backend
python test_mcp_endpoint.py
```

**Test Coverage:**
- ✅ Initialize handshake
- ✅ List tools
- ✅ Call tool (get_bookings)
- ✅ Error handling (invalid booking ID)

### Manual Testing with curl

**1. Initialize:**
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test", "version": "1.0"}
    },
    "id": 1
  }'
```

**2. List Tools:**
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
  }'
```

**3. Call Tool:**
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_bookings",
      "arguments": {"skip": 0, "limit": 5}
    },
    "id": 3
  }'
```

### Testing with Python

```python
import requests
import json

MCP_URL = "http://localhost:8000/mcp"

# Initialize
response = requests.post(MCP_URL, json={
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {},
    "id": 1
})
print(json.dumps(response.json(), indent=2))

# List tools
response = requests.post(MCP_URL, json={
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
})
print(json.dumps(response.json(), indent=2))

# Call tool
response = requests.post(MCP_URL, json={
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "get_bookings",
        "arguments": {"skip": 0, "limit": 5}
    },
    "id": 3
})
print(json.dumps(response.json(), indent=2))
```

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│              IBM Context Forge / AI Agent                    │
└─────────────────────────┬───────────────────────────────────┘
                          │ POST /mcp (JSON-RPC 2.0)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (main.py)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         FastMCP Server (mcp_server_http.py)          │  │
│  │  - 11 @mcp.tool() decorated functions                │  │
│  │  - Direct CRUD layer calls                           │  │
│  │  - JSON-RPC 2.0 protocol handling                    │  │
│  │  - Streamable HTTP transport                         │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │              CRUD Operations (crud.py)               │  │
│  │  - create_booking, get_bookings, etc.                │  │
│  │  - Direct database operations                        │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │         SQLAlchemy ORM + SQLite Database             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

1. **IBM Context Forge** sends POST /mcp with JSON-RPC 2.0 request
2. **FastAPI** routes to mounted FastMCP app
3. **FastMCP** parses JSON-RPC method and params
4. **Tool function** executes with direct CRUD calls
5. **CRUD layer** performs database operations
6. **FastMCP** formats result as JSON-RPC 2.0 response
7. **IBM Context Forge** receives structured response

## Key Differences from SSE Implementation

| Feature | SSE (Old) | HTTP (New) |
|---------|-----------|------------|
| **Method** | GET | POST |
| **Protocol** | SSE stream | JSON-RPC 2.0 |
| **Transport** | Server-Sent Events | Streamable HTTP |
| **Connection** | Long-lived stream | Request/response |
| **IBM Context Forge** | ❌ Not compatible | ✅ Compatible |
| **Tool Calls** | Via SSE messages | Via JSON-RPC |
| **Response Format** | SSE events | JSON-RPC result |

## Ngrok Setup

### Start Ngrok Tunnel

```bash
ngrok http 8000
```

You'll get a URL like: `https://famished-vertebrae-basil.ngrok-free.app`

### Configure Context Forge

```json
{
  "name": "refund-estimation-mcp",
  "url": "https://famished-vertebrae-basil.ngrok-free.app/mcp",
  "protocol": "mcp",
  "transport": "http"
}
```

### Update CORS (if needed)

The backend already allows all origins (`"*"`), but you can be more specific:

```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://famished-vertebrae-basil.ngrok-free.app",
        "https://context-forge.ibm.com"  # Add Context Forge domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

### Tool Execution Errors

When a tool raises an exception (e.g., booking not found), FastMCP automatically converts it to a JSON-RPC error:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_booking_details",
    "arguments": {"booking_id": 99999}
  },
  "id": 4
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Booking 99999 not found",
    "data": {
      "type": "ValueError"
    }
  },
  "id": 4
}
```

### Invalid Method

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "invalid_method",
  "params": {},
  "id": 5
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 5
}
```

## Production Deployment

### 1. Use HTTPS

Ensure your production server uses HTTPS:
- `https://api.yourcompany.com/mcp`

### 2. Add Authentication (Optional)

```python
from fastapi import Header, HTTPException

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        api_key = request.headers.get("X-API-Key")
        if api_key != "your-secret-key":
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized"}
            )
    return await call_next(request)
```

### 3. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/mcp")
@limiter.limit("100/minute")
async def mcp_endpoint(request: Request):
    # ... existing code
```

### 4. Monitoring

```python
import time
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_mcp_requests(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(f"MCP request: {duration:.2f}s")
        return response
    return await call_next(request)
```

## Troubleshooting

### Issue: Connection Refused

**Solution:**
1. Verify backend is running: `http://localhost:8000/api/docs`
2. Check if port 8000 is available
3. Ensure no firewall blocking

### Issue: Method Not Found

**Solution:**
1. Verify method name is correct: "initialize", "tools/list", "tools/call"
2. Check JSON-RPC format is correct
3. Ensure Content-Type is "application/json"

### Issue: Tool Not Found

**Solution:**
1. List all tools first: `POST /mcp` with method "tools/list"
2. Verify tool name matches exactly (case-sensitive)
3. Check tool is registered in `mcp_server_http.py`

### Issue: Invalid Arguments

**Solution:**
1. Check tool's inputSchema in tools/list response
2. Verify all required arguments are provided
3. Ensure data types match (string, integer, boolean, etc.)
4. Validate date-time format: ISO 8601

## Benefits

### ✅ IBM Context Forge Compatible
- Uses POST requests with JSON-RPC 2.0
- Streamable HTTP transport
- Proper MCP protocol implementation

### ✅ Direct CRUD Integration
- No HTTP calls to itself
- Direct database operations
- Shared resources (DB pool, ML models)
- Better performance

### ✅ Automatic Tool Registration
- Tools defined with @mcp.tool() decorator
- Automatic input schema generation
- Type hints for validation
- Comprehensive docstrings

### ✅ Production Ready
- Proper error handling
- JSON-RPC 2.0 compliance
- Structured responses
- Easy to test and monitor

## Documentation

- **MCP Endpoint Code**: [backend/mcp_server_http.py](backend/mcp_server_http.py)
- **Main Application**: [backend/main.py](backend/main.py)
- **Test Script**: [backend/test_mcp_endpoint.py](backend/test_mcp_endpoint.py)
- **API Documentation**: `http://localhost:8000/api/docs`

## Support

For issues or questions:
1. Check API documentation at `/api/docs`
2. Run test script: `python test_mcp_endpoint.py`
3. Review error messages in JSON-RPC responses
4. Check backend logs for detailed error traces

## Conclusion

The MCP HTTP endpoint provides a **production-ready, IBM Context Forge compatible** implementation of the Model Context Protocol using:

✅ **Streamable HTTP transport** (POST requests)  
✅ **JSON-RPC 2.0 protocol**  
✅ **11 automatically registered tools**  
✅ **Direct CRUD layer integration**  
✅ **Proper error handling**  
✅ **Easy testing and monitoring**  

**Next Steps:**
1. Install dependencies: `pip install -r requirements.txt`
2. Start backend: `python main.py`
3. Test endpoint: `python test_mcp_endpoint.py`
4. Configure IBM Context Forge with MCP URL
5. Start using tools via Context Forge