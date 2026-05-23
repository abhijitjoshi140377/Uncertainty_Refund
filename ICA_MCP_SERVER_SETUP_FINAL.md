# ICA MCP Server Setup - Final Instructions

## ✅ Backend Status
Your backend is now running with MCP endpoint enabled at:
- **Local:** `http://localhost:8000/mcp`
- **Public (ngrok):** `https://famished-vertebrae-basil.ngrok-free.dev/mcp`

## Step-by-Step: Add MCP Server to ICA

### 1. Navigate to Tools Section
- In ICA left sidebar, click on **"Tools"** (wrench icon 🔧)
- Click **"Add New"** button
- Select **"Add External MCP Server"**

### 2. Fill in MCP Server Details

**MCP Server Name:**
```
RefundEstimationAPI
```

**MCP Server URL:**
```
https://famished-vertebrae-basil.ngrok-free.dev/mcp
```

**Description:**
```
Travel refund estimation API with ML-powered predictions, confidence intervals, and risk assessment for force majeure events
```

**Tile Summary:**
```
AI-powered travel refund estimation with confidence intervals
```

**Transport Type:**
- Select: **STREAMABLE HTTP** (or **HTTP** if that's the only option)

**Authentication Type:**
- Select: **None**

### 3. Test the Connection
After saving, ICA should:
1. Connect to your MCP endpoint
2. Discover 7 available tools:
   - `get_bookings`
   - `get_booking_details`
   - `estimate_refund`
   - `get_risk_events`
   - `get_regional_risk`
   - `get_refund_statistics`
   - `get_provider_policies`

### 4. Add Tools to Your Agent

Once the MCP server is registered:

1. Go back to **"Agent & Assistant Studio"**
2. Find your **"TravelRefundAdvisor"** agent
3. Click **"Edit"**
4. Scroll to **"Tools"** section
5. Click **"Add tools"**
6. Search for **"RefundEstimationAPI"** or **"refund"**
7. Select all 7 tools from your MCP server
8. Click **"Apply"**
9. Click **"Save"** or **"Publish"**

### 5. Test Your Agent

Try these prompts:

**Test 1: List Bookings**
```
Show me all my travel bookings
```
Expected: Agent calls `get_bookings` tool and displays booking list

**Test 2: Booking Details**
```
Get details for booking ID 1
```
Expected: Agent calls `get_booking_details` with booking_id=1

**Test 3: Refund Estimation** (⭐ Main Feature)
```
Estimate refund for booking 1 with high severity due to natural disaster
```
Expected: Agent calls `estimate_refund` with:
- booking_id: 1
- severity: "high"
- event_type: "natural_disaster"

Returns: Expected refund, confidence interval, scenarios

**Test 4: Risk Events**
```
What are the current global risk events?
```
Expected: Agent calls `get_risk_events` and lists active events

**Test 5: Regional Risk**
```
What's the risk level for Ukraine?
```
Expected: Agent calls `get_regional_risk` with region="Ukraine"

## Available MCP Tools

### 1. get_bookings
- **Description:** Get all travel bookings
- **Parameters:** None
- **Returns:** List of bookings with IDs, destinations, dates, costs

### 2. get_booking_details
- **Description:** Get detailed information for a specific booking
- **Parameters:**
  - `booking_id` (integer, required)
- **Returns:** Full booking details with all components

### 3. estimate_refund ⭐
- **Description:** Estimate refund amount with confidence intervals
- **Parameters:**
  - `booking_id` (integer, required)
  - `severity` (string, required): "low", "medium", or "high"
  - `event_type` (string, required): "war", "pandemic", "natural_disaster", "political_unrest", or "terrorism"
- **Returns:**
  - Expected refund amount
  - 95% confidence interval (lower/upper bounds)
  - Best/worst/most likely scenarios
  - Risk score
  - Component-wise breakdown

### 4. get_risk_events
- **Description:** Get current global risk events affecting travel
- **Parameters:**
  - `active_only` (boolean, optional, default: true)
- **Returns:** List of risk events with severity, type, affected regions

### 5. get_regional_risk
- **Description:** Get risk assessment for a specific region
- **Parameters:**
  - `region` (string, required)
- **Returns:** Aggregate risk level, active events in region

### 6. get_refund_statistics
- **Description:** Get historical refund statistics
- **Parameters:**
  - `component_type` (string, optional): "flight", "hotel", "visa", "insurance"
  - `event_type` (string, optional): "war", "pandemic", etc.
- **Returns:** Average refund rates, success rates, patterns

### 7. get_provider_policies
- **Description:** Get refund policies for travel providers
- **Parameters:** None
- **Returns:** Provider policies with standard and force majeure refund percentages

## Troubleshooting

### Issue: "Cannot connect to MCP server"
**Solutions:**
1. Verify backend is running: Check terminal for "Application startup complete"
2. Verify ngrok is running: Check ngrok dashboard
3. Test endpoint manually: Visit `https://famished-vertebrae-basil.ngrok-free.dev/api/health`
4. Check ngrok URL hasn't changed (free plan URLs change on restart)

### Issue: "404 Not Found"
**Solutions:**
1. Ensure you're using `/mcp` endpoint (not `/mcp/`)
2. Backend must be running with the updated code
3. Check terminal for any startup errors

### Issue: "Tools not appearing in agent"
**Solutions:**
1. Refresh the ICA page
2. Make sure MCP server is "Active" status
3. Try removing and re-adding the MCP server
4. Check that tools are properly associated with the agent

### Issue: "Agent says it can't access tools"
**Solutions:**
1. Verify tools are added to the agent (not just the MCP server)
2. Check agent instructions mention the tools
3. Try republishing the agent
4. Test with explicit tool names in prompts

## Backend Maintenance

### Keep Backend Running
```powershell
cd backend
python main.py
```

### Keep Ngrok Running
```powershell
ngrok http 8000
```

### If Ngrok URL Changes
1. Note the new URL from ngrok dashboard
2. Update MCP Server URL in ICA
3. Update any hardcoded URLs in agent instructions

## Success Criteria

✅ Backend running without errors
✅ Ngrok tunnel active
✅ MCP server registered in ICA
✅ 7 tools discovered
✅ Tools added to agent
✅ Agent successfully calls tools
✅ Refund estimates include confidence intervals
✅ Risk events display correctly

## Demo Tips

1. **Start with simple queries** to build confidence
2. **Highlight the ML predictions** and confidence intervals
3. **Show the uncertainty quantification** (not just point estimates)
4. **Demonstrate risk assessment** capabilities
5. **Explain the business value** of automated refund estimation

## Quick Reference

**Backend:** `http://localhost:8000`
**MCP Endpoint:** `https://famished-vertebrae-basil.ngrok-free.dev/mcp`
**API Docs:** `https://famished-vertebrae-basil.ngrok-free.dev/api/docs`
**Health Check:** `https://famished-vertebrae-basil.ngrok-free.dev/api/health`

Good luck with your hackathon! 🚀