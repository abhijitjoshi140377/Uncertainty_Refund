# Testing Your MCP Tools in IBM ICA Context Forge

## Important: You're Already Done! ✅

Since you successfully completed the **bulk import**, all 11 tools are already configured and ready to use. You **DO NOT need** to manually add tools one by one using the "Add New Tool" process.

The `ICA_ADD_NEW_TOOL_GUIDE.md` is only for **future reference** when you want to add **additional** endpoints beyond the 11 you already imported.

---

## What You Have Now

✅ **11 MCP Tools Imported and Active:**
1. v2-create-booking
2. v2-get-bookings
3. v2-get-booking-details
4. v2-estimate-refund
5. v2-get-refund-estimates
6. v2-get-risk-events
7. v2-get-regional-risk
8. v2-get-historical-refunds
9. v2-get-refund-statistics
10. v2-get-provider-policies
11. v2-get-provider-policy

✅ **All Tools Configured with:**
- Correct URLs
- Proper input schemas
- Authentication settings
- Headers
- Response filters

✅ **Ready to Use Immediately**

---

## How to Test Your MCP Tools

### Step 1: Start Your Backend API

**Open Terminal 1:**
```bash
cd backend
python main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Verify Backend is Running:**
```bash
curl http://localhost:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "refund-estimation-api",
  "timestamp": "2026-05-20T14:45:00Z"
}
```

---

### Step 2: Test Tools in ICA Context Forge UI

#### Test 1: Get All Bookings (Simple GET)

1. **In ICA Context Forge**:
   - Go to **Tools** section
   - Find tool: **v2-get-bookings**
   - Click on the tool name

2. **Click "Test" or "Try It"**

3. **Parameters** (optional):
   ```json
   {
     "skip": 0,
     "limit": 10
   }
   ```
   Or leave empty to use defaults

4. **Click "Execute" or "Run"**

5. **Expected Response**:
   ```json
   []
   ```
   (Empty array if no bookings exist yet)
   
   OR if you have data:
   ```json
   [
     {
       "id": 1,
       "booking_reference": "BK-2026-001",
       "customer_name": "John Doe",
       "customer_email": "john@example.com",
       "total_cost": 50000,
       "status": "confirmed",
       ...
     }
   ]
   ```

#### Test 2: Create a Booking (POST with Body)

1. **Find tool**: **v2-create-booking**

2. **Click "Test"**

3. **Enter Parameters**:
   ```json
   {
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
       },
       {
         "component_type": "hotel",
         "provider_name": "Marriott",
         "cost": 30000,
         "is_refundable": true,
         "cancellation_fee": 3000
       }
     ]
   }
   ```

4. **Click "Execute"**

5. **Expected Response**:
   ```json
   {
     "id": 1,
     "booking_reference": "BK-2026-001",
     "customer_name": "Jane Smith",
     "customer_email": "jane@example.com",
     "booking_date": "2026-05-20T14:45:00Z",
     "travel_date": "2026-06-15T10:00:00Z",
     "destination": "Paris",
     "origin": "New York",
     "total_cost": 80000,
     "status": "pending",
     "components": [...]
   }
   ```

#### Test 3: Get Booking Details (GET with Path Parameter)

1. **Find tool**: **v2-get-booking-details**

2. **Click "Test"**

3. **Enter Parameters**:
   ```json
   {
     "booking_id": 1
   }
   ```

4. **Click "Execute"**

5. **Expected Response**:
   ```json
   {
     "id": 1,
     "booking_reference": "BK-2026-001",
     "customer_name": "Jane Smith",
     ...
     "components": [
       {
         "id": 1,
         "component_type": "flight",
         "provider_name": "Air France",
         "cost": 50000,
         ...
       }
     ]
   }
   ```

#### Test 4: Estimate Refund (POST with Path Parameter)

1. **Find tool**: **v2-estimate-refund**

2. **Click "Test"**

3. **Enter Parameters**:
   ```json
   {
     "booking_id": 1,
     "selected_model": "auto",
     "severity": "high"
   }
   ```

4. **Click "Execute"**

5. **Expected Response**:
   ```json
   {
     "id": 1,
     "booking_id": 1,
     "estimate_date": "2026-05-20T14:45:00Z",
     "expected_refund_amount": 68000,
     "expected_refund_percentage": 85.0,
     "confidence_lower": 60800,
     "confidence_upper": 75200,
     "confidence_level": 0.95,
     "current_risk_level": "high",
     "risk_score": 0.85,
     "best_case_refund": 76000,
     "worst_case_refund": 56000,
     "most_likely_refund": 68000,
     "model_version": "v1.0",
     "prediction_confidence": 0.92
   }
   ```

#### Test 5: Get Risk Events (Simple GET)

1. **Find tool**: **v2-get-risk-events**

2. **Click "Test"**

3. **Parameters** (optional):
   ```json
   {
     "active_only": true
   }
   ```

4. **Click "Execute"**

5. **Expected Response**:
   ```json
   [
     {
       "id": 1,
       "event_type": "natural_disaster",
       "severity": "high",
       "affected_region": "Southeast Asia",
       "start_date": "2026-05-15T00:00:00Z",
       "description": "Typhoon affecting travel",
       "is_active": true
     }
   ]
   ```

---

### Step 3: Test All 11 Tools

Go through each tool and test with appropriate parameters:

| Tool Name | Test Parameters | Expected Result |
|-----------|----------------|-----------------|
| v2-create-booking | Full booking object | New booking created |
| v2-get-bookings | skip=0, limit=10 | Array of bookings |
| v2-get-booking-details | booking_id=1 | Single booking object |
| v2-estimate-refund | booking_id=1, severity="high" | Refund estimate |
| v2-get-refund-estimates | booking_id=1 | Array of estimates |
| v2-get-risk-events | active_only=true | Array of events |
| v2-get-regional-risk | region="Southeast Asia" | Regional risk data |
| v2-get-historical-refunds | limit=10 | Historical data |
| v2-get-refund-statistics | (no params) | Statistics object |
| v2-get-provider-policies | (no params) | Array of policies |
| v2-get-provider-policy | provider_name="Air India" | Single policy |

---

### Step 4: Generate Sample Data (If Database is Empty)

If your tests return empty arrays, generate sample data:

**Open Terminal 2** (keep backend running in Terminal 1):
```bash
cd backend
python -c "from services.data_generator import generate_sample_data; generate_sample_data()"
```

**Expected Output:**
```
Generating sample data...
Created 10 bookings
Created 15 risk events
Created 20 historical refunds
Created 8 provider policies
Sample data generation complete!
```

**Now re-test your tools** - they should return data.

---

## Step 5: Deploy MCP Server (Make Tools Available to AI Agents)

Once testing is successful in ICA, deploy your MCP server:

### Option A: Deploy in ICA Context Forge

1. **In ICA Context Forge**:
   - Go to **Deployment** or **Publish** section
   - Click **"Deploy MCP Server"** or **"Publish Tools"**
   - Choose deployment target:
     - **Cloud**: IBM Cloud deployment
     - **Local**: Local development server
     - **Custom**: Custom endpoint

2. **Configure Deployment**:
   - **Server Name**: `refund-estimation-mcp`
   - **Description**: `MCP server for travel refund estimation`
   - **Base URL**: `http://localhost:8000` (or your production URL)
   - **Version**: `v1.0`

3. **Deploy**:
   - Click **"Deploy"**
   - Wait for deployment to complete
   - Note the **MCP Server URL** provided

4. **Verify Deployment**:
   - ICA will provide an MCP endpoint URL like:
     - `https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp`
   - Test the endpoint:
     ```bash
     curl -X POST https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp \
       -H "Content-Type: application/json" \
       -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
     ```

### Option B: Use Native MCP Server (Alternative)

If ICA deployment is complex, use the native MCP server:

**Terminal 3** (keep backend running):
```bash
cd backend
python mcp_server_http.py
```

**Test MCP Protocol**:
```bash
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

**Expected Response**:
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

## Step 6: Connect AI Agent to MCP Server

### For Claude Desktop:

1. **Open Claude Desktop Settings**
2. **Go to Developer → MCP Servers**
3. **Add New Server**:
   ```json
   {
     "refund-estimation": {
       "url": "https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp",
       "type": "http"
     }
   }
   ```
4. **Restart Claude Desktop**
5. **Test**: Ask Claude to "list available tools"

### For Custom AI Agent:

**Python Example**:
```python
import requests

# MCP endpoint
mcp_url = "https://mcp.cloud.ibm.com/your-workspace/refund-estimation-mcp"

# List available tools
response = requests.post(
    mcp_url,
    json={
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    }
)

tools = response.json()["result"]["tools"]
print(f"Available tools: {len(tools)}")

# Call a tool
response = requests.post(
    mcp_url,
    json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_bookings",
            "arguments": {"skip": 0, "limit": 10}
        },
        "id": 2
    }
)

result = response.json()["result"]
print(f"Bookings: {result}")
```

---

## Step 7: Use the System End-to-End

### Scenario: Customer Requests Refund Estimate

**AI Agent Workflow**:

1. **Get Customer Booking**:
   ```
   Tool: v2-get-booking-details
   Input: {"booking_id": 1}
   ```

2. **Check Current Risk Events**:
   ```
   Tool: v2-get-risk-events
   Input: {"active_only": true}
   ```

3. **Get Regional Risk**:
   ```
   Tool: v2-get-regional-risk
   Input: {"region": "Southeast Asia"}
   ```

4. **Estimate Refund**:
   ```
   Tool: v2-estimate-refund
   Input: {
     "booking_id": 1,
     "selected_model": "auto",
     "severity": "high"
   }
   ```

5. **Get Historical Data for Context**:
   ```
   Tool: v2-get-historical-refunds
   Input: {"limit": 10}
   ```

6. **Provide Estimate to Customer**:
   - Expected refund: ₹68,000 (85% of ₹80,000)
   - Confidence: 95% (₹60,800 - ₹75,200)
   - Based on: High severity event in region
   - Historical average: Similar cases got 82-88% refund

---

## Troubleshooting

### Issue 1: Tool Test Returns "Connection Refused"
**Cause**: Backend not running  
**Solution**: Start backend in Terminal 1

### Issue 2: Tool Test Returns Empty Array
**Cause**: No data in database  
**Solution**: Run data generator script

### Issue 3: Tool Test Returns 404
**Cause**: URL mismatch  
**Solution**: Verify backend is running on port 8000

### Issue 4: Tool Test Returns 422 Validation Error
**Cause**: Invalid input parameters  
**Solution**: Check input schema and provide correct data types

### Issue 5: MCP Server Not Responding
**Cause**: Not deployed or wrong URL  
**Solution**: Verify deployment in ICA or start native MCP server

---

## Summary

### What You Need to Do:

1. ✅ **Start Backend**: `cd backend && python main.py`
2. ✅ **Test Tools in ICA**: Use built-in test feature for each tool
3. ✅ **Generate Sample Data**: If database is empty
4. ✅ **Deploy MCP Server**: In ICA or use native server
5. ✅ **Connect AI Agent**: Configure agent to use MCP endpoint
6. ✅ **Use the System**: Start estimating refunds!

### What You DON'T Need to Do:

❌ **Manually add tools one by one** - Already done via bulk import  
❌ **Configure each tool individually** - Already configured  
❌ **Write MCP server code** - Already exists (native option)  
❌ **Set up authentication** - API uses auth_type: "none"  

### Your Tools Are Ready!

All 11 tools are imported, configured, and ready to use. Just start the backend, test in ICA, deploy, and connect your AI agent.

---

**Last Updated**: 2026-05-20  
**Status**: Bulk import successful - Ready to test  
**Next**: Start backend and test tools in ICA