# MCP Server Setup Guide for Refund Estimation API

This guide provides step-by-step instructions to create and configure an MCP (Model Context Protocol) server for the Travel Refund Uncertainty Estimation Platform.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Option 1: Using IBM Context Forge (Recommended)](#option-1-using-ibm-context-forge-recommended)
3. [Option 2: Native MCP Server with FastMCP](#option-2-native-mcp-server-with-fastmcp)
4. [Testing Your MCP Server](#testing-your-mcp-server)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- Python 3.8 or higher
- Backend API running on `http://localhost:8000`
- Git (for cloning the repository)

### Required Python Packages
```bash
pip install mcp==1.1.2
pip install requests==2.31.0
```

---

## Option 1: Using IBM Context Forge (Recommended)

IBM Context Forge is the easiest way to convert your REST API into MCP tools without writing code.

### Step 1: Access IBM Context Forge
1. Navigate to IBM Context Forge web interface
2. Log in with your IBM credentials

### Step 2: Import Bulk Configuration
1. Locate the file: `refund-api-bulk-import.json` in your project root
2. In Context Forge, click **"Import"** → **"Bulk Import"**
3. Upload `refund-api-bulk-import.json`
4. Review the 11 imported endpoints:
   - create-booking
   - get-bookings
   - get-booking-details
   - estimate-refund
   - get-refund-estimates
   - get-risk-events
   - get-regional-risk
   - get-historical-refunds
   - get-refund-statistics
   - get-provider-policies
   - get-provider-policy

### Step 3: Configure Base URL
1. In Context Forge settings, set base URL to: `http://localhost:8000`
2. Ensure authentication is set to "none" (as configured in bulk import)

### Step 4: Test Endpoints
1. Use Context Forge's built-in testing tool
2. Test each endpoint with sample data
3. Verify responses match expected format

### Step 5: Deploy MCP Server
1. Click **"Deploy"** in Context Forge
2. Choose deployment target (local, cloud, etc.)
3. Note the MCP server URL provided

### Step 6: Connect AI Agent
1. Configure your AI agent (Claude, GPT, etc.) to use the MCP server URL
2. Test tool discovery and execution

---

## Option 2: Native MCP Server with FastMCP

If you prefer a native Python MCP server implementation, follow these steps.

### Step 1: Verify MCP Server File Exists
Check that `backend/mcp_server_http.py` exists in your project:
```bash
ls backend/mcp_server_http.py
```

### Step 2: Review MCP Server Code
The file contains 11 MCP tools that directly call the CRUD layer:
- `create_booking`
- `get_bookings`
- `get_booking_details`
- `estimate_refund`
- `get_refund_estimates`
- `get_risk_events`
- `get_regional_risk`
- `get_historical_refunds`
- `get_refund_statistics`
- `get_provider_policies`
- `get_provider_policy`

### Step 3: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

Ensure these packages are installed:
```
mcp==1.1.2
requests==2.31.0
fastapi
uvicorn
sqlalchemy
pydantic
```

### Step 4: Start Backend API
In one terminal:
```bash
cd backend
python main.py
```

Verify API is running:
```bash
curl http://localhost:8000/api/health
```

### Step 5: Run MCP Server (Standalone)
In another terminal:
```bash
cd backend
python mcp_server_http.py
```

This starts the MCP server on a separate port (default: 8001).

### Step 6: Alternative - Integrated MCP Endpoint
To integrate MCP into the main FastAPI app:

1. Open `backend/main.py`
2. Add import:
```python
from mcp_server_http import mcp
```

3. Mount MCP server:
```python
# Add before if __name__ == "__main__":
app.mount("/mcp", mcp.streamable_http_app())
```

4. Restart backend:
```bash
python main.py
```

5. MCP endpoint available at: `http://localhost:8000/mcp`

### Step 7: Test MCP Protocol
Test with JSON-RPC 2.0 request:
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

Expected response:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "create_booking",
        "description": "Create a new travel booking...",
        "inputSchema": {...}
      },
      ...
    ]
  },
  "id": 1
}
```

---

## Testing Your MCP Server

### Test 1: List Available Tools
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

### Test 2: Call a Tool (Get Bookings)
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_bookings",
      "arguments": {
        "skip": 0,
        "limit": 10
      }
    },
    "id": 2
  }'
```

### Test 3: Create Booking via MCP
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "create_booking",
      "arguments": {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "travel_date": "2026-06-15T10:00:00Z",
        "destination": "Paris",
        "origin": "New York",
        "components": [
          {
            "component_type": "flight",
            "provider_name": "Air France",
            "cost": 50000,
            "is_refundable": true,
            "cancellation_fee": 5000
          }
        ]
      }
    },
    "id": 3
  }'
```

### Test 4: Estimate Refund via MCP
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "estimate_refund",
      "arguments": {
        "booking_id": 1,
        "selected_model": "auto",
        "severity": "high"
      }
    },
    "id": 4
  }'
```

---

## Troubleshooting

### Issue 1: MCP Endpoint Times Out
**Problem**: `/mcp` endpoint doesn't respond or times out

**Solution**:
1. Run MCP server standalone instead of mounting
2. Use IBM Context Forge (recommended approach)
3. Check FastMCP version: `pip show mcp`

### Issue 2: Tools Not Discovered
**Problem**: AI agent can't see MCP tools

**Solution**:
1. Verify MCP server is running: `curl http://localhost:8000/mcp`
2. Check JSON-RPC response format
3. Ensure all 11 tools are registered in `mcp_server_http.py`

### Issue 3: Tool Execution Fails
**Problem**: Tool calls return errors

**Solution**:
1. Verify backend API is running: `curl http://localhost:8000/api/health`
2. Check database exists: `ls backend/refund_estimation.db`
3. Review tool input schema matches API requirements
4. Check logs in terminal running MCP server

### Issue 4: Import Errors
**Problem**: `ModuleNotFoundError: No module named 'mcp'`

**Solution**:
```bash
pip install mcp==1.1.2
pip install requests==2.31.0
```

### Issue 5: Database Not Found
**Problem**: `sqlite3.OperationalError: unable to open database file`

**Solution**:
1. Initialize database:
```bash
cd backend
python -c "from models.database import init_db; init_db()"
```

2. Generate sample data:
```bash
python -c "from services.data_generator import generate_sample_data; generate_sample_data()"
```

### Issue 6: Port Already in Use
**Problem**: `OSError: [Errno 48] Address already in use`

**Solution**:
1. Find process using port:
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

2. Kill process or use different port:
```python
# In main.py
uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
```

---

## Architecture Overview

### MCP Server Components

```
┌─────────────────────────────────────────┐
│         AI Agent (Claude/GPT)           │
└─────────────────┬───────────────────────┘
                  │ MCP Protocol
                  │ (JSON-RPC 2.0)
┌─────────────────▼───────────────────────┐
│         MCP Server (FastMCP)            │
│  ┌─────────────────────────────────┐   │
│  │  11 MCP Tools (@mcp.tool())     │   │
│  │  - create_booking               │   │
│  │  - get_bookings                 │   │
│  │  - estimate_refund              │   │
│  │  - get_risk_events              │   │
│  │  - ...                          │   │
│  └─────────────┬───────────────────┘   │
└────────────────┼───────────────────────┘
                 │ Direct Function Calls
┌────────────────▼───────────────────────┐
│         CRUD Layer (crud.py)           │
│  - Database operations                 │
│  - Business logic                      │
└────────────────┬───────────────────────┘
                 │ SQLAlchemy ORM
┌────────────────▼───────────────────────┐
│    SQLite Database (refund_estimation.db)│
│  - Bookings                            │
│  - Refund Estimates                    │
│  - Risk Events                         │
│  - Historical Data                     │
└────────────────────────────────────────┘
```

### Data Flow

1. **AI Agent Request**: Agent sends JSON-RPC 2.0 request to MCP server
2. **Tool Discovery**: MCP server lists available tools with schemas
3. **Tool Execution**: Agent calls specific tool with arguments
4. **CRUD Operation**: MCP tool calls CRUD layer function
5. **Database Query**: CRUD layer executes SQLAlchemy query
6. **Response**: Data flows back through layers to AI agent

---

## Best Practices

### 1. Use IBM Context Forge for Production
- No code maintenance required
- Automatic schema validation
- Built-in monitoring and logging
- Easy updates when API changes

### 2. Keep MCP Server Stateless
- Don't store session data in MCP server
- Use database for persistence
- Each tool call should be independent

### 3. Validate Input Thoroughly
- Use Pydantic schemas for validation
- Check required fields
- Validate data types and ranges
- Return clear error messages

### 4. Handle Errors Gracefully
- Catch database exceptions
- Return meaningful error messages
- Log errors for debugging
- Don't expose internal details

### 5. Monitor Performance
- Log tool execution times
- Monitor database query performance
- Set appropriate timeouts
- Use connection pooling

### 6. Security Considerations
- Validate all user input
- Use parameterized queries (SQLAlchemy handles this)
- Don't expose sensitive data in errors
- Consider adding authentication for production

---

## Next Steps

1. ✅ Choose your MCP server approach (Context Forge recommended)
2. ✅ Follow setup steps for your chosen approach
3. ✅ Test all 11 tools with sample data
4. ✅ Connect your AI agent to the MCP server
5. ✅ Monitor and optimize performance
6. ✅ Deploy to production environment

---

## Additional Resources

- **MCP Protocol Specification**: https://modelcontextprotocol.io/
- **FastMCP Documentation**: https://github.com/jlowin/fastmcp
- **IBM Context Forge**: Contact IBM for access
- **Project Documentation**: See `README.md` and `QUICKSTART.md`

---

## Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review `backend/mcp_server_http.py` code
3. Check `refund-api-bulk-import.json` configuration
4. Review backend API logs
5. Test endpoints directly with curl/Postman

---

**Last Updated**: 2026-05-20  
**Version**: 1.0  
**Author**: Bob (AI Assistant)