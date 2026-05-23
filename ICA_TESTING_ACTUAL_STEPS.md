# IBM ICA Context Forge: Actual Testing Steps

## Important Discovery

It appears IBM ICA Context Forge may not have a built-in "Test" button in the UI for individual tools. This is common in enterprise MCP platforms where tools are meant to be used by AI agents, not tested manually in the UI.

---

## How to Actually Test Your MCP Tools

Since ICA doesn't provide a UI test feature, here are the actual ways to test:

### Method 1: Test Backend API Directly (Recommended)

Your tools call your backend API, so test the API directly first:

#### Step 1: Start Backend
```bash
cd backend
python main.py
```

#### Step 2: Test Each Endpoint with curl

**Test 1: Health Check**
```bash
curl http://localhost:8000/api/health
```

**Test 2: Get Bookings**
```bash
curl http://localhost:8000/api/bookings
```

**Test 3: Create Booking**
```bash
curl -X POST http://localhost:8000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
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
  }'
```

**Test 4: Get Booking Details**
```bash
curl http://localhost:8000/api/bookings/1
```

**Test 5: Estimate Refund**
```bash
curl -X POST http://localhost:8000/api/estimate-refund/1 \
  -H "Content-Type: application/json" \
  -d '{
    "selected_model": "auto",
    "severity": "high"
  }'
```

**Test 6: Get Risk Events**
```bash
curl "http://localhost:8000/api/risk-events?active_only=true"
```

**Test 7: Get Regional Risk**
```bash
curl http://localhost:8000/api/risk-events/region/Southeast%20Asia
```

**Test 8: Get Historical Refunds**
```bash
curl "http://localhost:8000/api/historical-refunds?limit=10"
```

**Test 9: Get Refund Statistics**
```bash
curl http://localhost:8000/api/statistics/refund-rates
```

**Test 10: Get Provider Policies**
```bash
curl http://localhost:8000/api/providers
```

**Test 11: Get Specific Provider Policy**
```bash
curl http://localhost:8000/api/providers/Air%20India
```

If all these work, your MCP tools will work because they call these same endpoints.

---

### Method 2: Use Postman or Insomnia

1. **Download Postman**: https://www.postman.com/downloads/
2. **Import Collection**: Create a collection with all 11 endpoints
3. **Test Each Endpoint**: Click "Send" to test
4. **Save Results**: Document what works

**Postman Collection JSON** (import this):
```json
{
  "info": {
    "name": "Refund Estimation API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get Bookings",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/bookings?skip=0&limit=10",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "bookings"],
          "query": [
            {"key": "skip", "value": "0"},
            {"key": "limit", "value": "10"}
          ]
        }
      }
    },
    {
      "name": "Create Booking",
      "request": {
        "method": "POST",
        "header": [
          {"key": "Content-Type", "value": "application/json"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"customer_name\": \"Jane Smith\",\n  \"customer_email\": \"jane@example.com\",\n  \"travel_date\": \"2026-06-15T10:00:00Z\",\n  \"destination\": \"Paris\",\n  \"origin\": \"New York\",\n  \"components\": [\n    {\n      \"component_type\": \"flight\",\n      \"provider_name\": \"Air France\",\n      \"cost\": 50000,\n      \"is_refundable\": true,\n      \"cancellation_fee\": 5000\n    }\n  ]\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/bookings",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "bookings"]
        }
      }
    }
  ]
}
```

---

### Method 3: Test MCP Protocol Directly

If ICA deployed your MCP server, test the MCP protocol:

#### Find Your MCP Endpoint URL

In ICA Context Forge:
1. Look for **"Deployment"** or **"Settings"** section
2. Find **"MCP Endpoint URL"** or **"Server URL"**
3. Should look like: `https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp`

#### Test MCP Tools List

```bash
curl -X POST https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "v2-create-booking",
        "description": "Create a new travel booking...",
        "inputSchema": {...}
      },
      ...
    ]
  },
  "id": 1
}
```

#### Test MCP Tool Call

```bash
curl -X POST https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "v2-get-bookings",
      "arguments": {
        "skip": 0,
        "limit": 10
      }
    },
    "id": 2
  }'
```

---

### Method 4: Use Python Script to Test

Create a test script:

**File: `test_mcp_tools.py`**
```python
import requests
import json

# Backend API base URL
BASE_URL = "http://localhost:8000"

def test_endpoint(method, path, data=None, params=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{path}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        print(f"\n{'='*60}")
        print(f"Testing: {method} {path}")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)[:500]}")
        
        return response.status_code == 200 or response.status_code == 201
    except Exception as e:
        print(f"ERROR: {e}")
        return False

# Test all endpoints
tests = [
    ("GET", "/api/health", None, None),
    ("GET", "/api/bookings", None, {"skip": 0, "limit": 10}),
    ("POST", "/api/bookings", {
        "customer_name": "Test User",
        "customer_email": "test@example.com",
        "travel_date": "2026-06-15T10:00:00Z",
        "destination": "Paris",
        "origin": "New York",
        "components": [{
            "component_type": "flight",
            "provider_name": "Air France",
            "cost": 50000,
            "is_refundable": True,
            "cancellation_fee": 5000
        }]
    }, None),
    ("GET", "/api/bookings/1", None, None),
    ("POST", "/api/estimate-refund/1", {
        "selected_model": "auto",
        "severity": "high"
    }, None),
    ("GET", "/api/estimates/1", None, None),
    ("GET", "/api/risk-events", None, {"active_only": True}),
    ("GET", "/api/risk-events/region/Southeast Asia", None, None),
    ("GET", "/api/historical-refunds", None, {"limit": 10}),
    ("GET", "/api/statistics/refund-rates", None, None),
    ("GET", "/api/providers", None, None),
    ("GET", "/api/providers/Air India", None, None),
]

print("Starting API Tests...")
print("="*60)

passed = 0
failed = 0

for method, path, data, params in tests:
    if test_endpoint(method, path, data, params):
        passed += 1
    else:
        failed += 1

print(f"\n{'='*60}")
print(f"Test Results: {passed} passed, {failed} failed")
print(f"{'='*60}")
```

**Run the test:**
```bash
python test_mcp_tools.py
```

---

### Method 5: Connect AI Agent and Test

The ultimate test is connecting an AI agent:

#### For Claude Desktop:

1. **Open Claude Desktop**
2. **Go to Settings → Developer → MCP Servers**
3. **Add Server**:
   ```json
   {
     "refund-estimation": {
       "url": "https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp",
       "type": "http"
     }
   }
   ```
4. **Restart Claude**
5. **Test**: Ask Claude:
   - "What tools do you have available?"
   - "Get all bookings"
   - "Create a test booking for Paris"
   - "Estimate refund for booking 1"

#### For Custom AI Agent:

```python
import requests

mcp_url = "https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp"

# List tools
response = requests.post(mcp_url, json={
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
})
print("Available tools:", response.json())

# Call a tool
response = requests.post(mcp_url, json={
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "v2-get-bookings",
        "arguments": {"skip": 0, "limit": 10}
    },
    "id": 2
})
print("Bookings:", response.json())
```

---

## What to Look for in ICA Context Forge

Since there's no "Test" button, look for these sections:

### 1. Tools List
- Should show all 11 tools with "v2-" prefix
- Status should be "Active" or "Ready"
- Each tool should have a green checkmark or success indicator

### 2. Deployment/Server Section
- Look for "MCP Server URL" or "Endpoint URL"
- Should show deployment status as "Active" or "Running"
- May show request count or usage statistics

### 3. Logs/Monitoring
- Check if there's a "Logs" or "Monitoring" section
- May show tool invocations
- May show errors or warnings

### 4. Documentation/API Reference
- Some platforms auto-generate API docs
- May show tool schemas and examples
- May have interactive documentation

---

## Recommended Testing Workflow

1. ✅ **Test Backend API Directly** (Method 1 - curl commands)
   - Verify all 11 endpoints work
   - Generate sample data if needed
   - Document any issues

2. ✅ **Test MCP Protocol** (Method 3 - if MCP URL available)
   - Verify tools/list works
   - Test 2-3 tool calls
   - Confirm responses are correct

3. ✅ **Connect AI Agent** (Method 5)
   - Configure Claude or custom agent
   - Test tool discovery
   - Test actual tool usage

4. ✅ **Monitor in ICA**
   - Check logs for tool invocations
   - Verify no errors
   - Monitor performance

---

## Generate Sample Data First

Before testing, generate sample data:

```bash
cd backend
python -c "from services.data_generator import generate_sample_data; generate_sample_data()"
```

This creates:
- 10 sample bookings
- 15 risk events
- 20 historical refunds
- 8 provider policies

---

## Summary

**ICA Context Forge likely doesn't have a UI "Test" button** because:
- Tools are meant for AI agents, not manual testing
- Enterprise platforms focus on deployment, not testing
- Testing is done via API calls or AI agent integration

**How to Actually Test:**
1. Test backend API directly with curl (fastest)
2. Use Postman/Insomnia (most user-friendly)
3. Test MCP protocol with curl (if URL available)
4. Write Python test script (most thorough)
5. Connect AI agent (ultimate test)

**Your tools are working if:**
- ✅ Backend API responds correctly
- ✅ All 11 endpoints return expected data
- ✅ MCP protocol returns tools list
- ✅ AI agent can discover and use tools

---

**Last Updated**: 2026-05-20  
**Issue**: No "Test" button in ICA UI  
**Solution**: Test backend API directly or via MCP protocol