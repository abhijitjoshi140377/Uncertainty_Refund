# Complete ICA Agent Orchestration Setup Guide

## Current Situation

✅ **What's Working:**
- Backend MCP endpoint: `https://famished-vertebrae-basil.ngrok-free.dev/mcp`
- MCP server responding to initialize, ping, tools/list
- 7 tools defined and ready
- External MCP Server registered in Tools section

❌ **What's Missing:**
- MCP server NOT in Agent Orchestration's "AVAILABLE RESOURCES"
- Agent Orchestration cannot see the tools
- Cannot generate YAML without registered tools

## Solution: Register MCP Server for Agent Orchestration

### Step 1: Find MCP Administration in Agent Orchestration

Look for one of these options in the Agent Orchestration interface:

**Option A: Settings/Configuration**
- Click **"Settings"** icon (gear icon)
- Look for **"MCP Servers"** or **"Tool Registry"**
- Click **"Add MCP Server"** or **"Register Server"**

**Option B: Available Resources**
- Look for **"Available Resources"** link/tab
- Click **"Add Resource"** or **"+"** button
- Select **"MCP Server"**

**Option C: Tools Menu**
- In Agent Orchestration, look for **"Tools"** menu
- Click **"Add MCP Server"**
- Or **"Import from External"**

**Option D: Direct Registration Form**
- Look for **"Register MCP Server"** button anywhere on the page
- Or **"Connect to MCP Server"**

### Step 2: Fill in MCP Server Details

When you find the registration form, enter:

**Server Name:**
```
RefundEstimationAPI
```

**Server URL:**
```
https://famished-vertebrae-basil.ngrok-free.dev/mcp
```

**Server Type:**
```
External HTTP MCP Server
```

**Protocol:**
```
JSON-RPC 2.0
```

**Transport:**
```
HTTP or STREAMABLE HTTP
```

**Authentication:**
```
None
```

**Description:**
```
Travel refund estimation API with ML-powered predictions and confidence intervals
```

### Step 3: Verify Registration

After saving, you should see:

**In AVAILABLE RESOURCES:**
```
RefundEstimationAPI.get_bookings
RefundEstimationAPI.get_booking_details
RefundEstimationAPI.estimate_refund
RefundEstimationAPI.get_risk_events
RefundEstimationAPI.get_regional_risk
RefundEstimationAPI.get_refund_statistics
RefundEstimationAPI.get_provider_policies
```

### Step 4: Create Agent with Tools

Once tools are visible, go back to Agent Orchestration chat and say:

```
The RefundEstimationAPI MCP server is now registered and tools are visible in AVAILABLE RESOURCES.

Please create a LangGraph ReAct travel refund estimation agent using these tools:
- RefundEstimationAPI.get_bookings
- RefundEstimationAPI.get_booking_details
- RefundEstimationAPI.estimate_refund
- RefundEstimationAPI.get_risk_events
- RefundEstimationAPI.get_regional_risk
- RefundEstimationAPI.get_refund_statistics
- RefundEstimationAPI.get_provider_policies

The agent should be professional, empathetic, and explain 95% confidence intervals clearly to customers dealing with travel cancellations during force majeure events.
```

### Step 5: Review Generated YAML

ICA will generate something like:

```yaml
name: TravelRefundAdvisor
platform: ica
framework: langgraph
pattern: react
model: gpt-5.2

tools:
  - RefundEstimationAPI.get_bookings
  - RefundEstimationAPI.get_booking_details
  - RefundEstimationAPI.estimate_refund
  - RefundEstimationAPI.get_risk_events
  - RefundEstimationAPI.get_regional_risk
  - RefundEstimationAPI.get_refund_statistics
  - RefundEstimationAPI.get_provider_policies

instructions: |
  You are a professional travel refund estimation assistant...
  [detailed instructions]
```

### Step 6: Deploy and Test

1. Review the YAML
2. Click **"Deploy"** or **"Create Agent"**
3. Test with: "Show me all my travel bookings"
4. Check terminal for: `[MCP] Calling tool: get_bookings`

## Alternative: If You Can't Find MCP Registration

### Plan B: Use REST API Tools Instead

If Agent Orchestration doesn't support External MCP Servers, create REST API tools:

1. In Agent Orchestration, look for **"Add REST API Tool"**
2. Create 7 individual REST API tools:

**Tool 1: get_bookings**
- Method: GET
- URL: `https://famished-vertebrae-basil.ngrok-free.dev/api/bookings`

**Tool 2: get_booking_details**
- Method: GET
- URL: `https://famished-vertebrae-basil.ngrok-free.dev/api/bookings/{booking_id}`
- Parameters: booking_id (integer, required)

**Tool 3: estimate_refund**
- Method: POST
- URL: `https://famished-vertebrae-basil.ngrok-free.dev/api/estimate-refund/{booking_id}`
- Path Parameters: booking_id (integer, required)
- Body Parameters: severity (string), event_type (string)

**Tool 4-7:** Similar pattern for other endpoints

3. Once all 7 REST API tools are created, they'll appear in AVAILABLE RESOURCES
4. Create agent using these REST API tools

## Plan C: Use Frontend Demo

If Agent Orchestration integration is too complex for the hackathon timeline:

### Your Frontend is Production-Ready!

**URL:** `http://localhost:5173`

**Features:**
✅ All bookings with search/filter
✅ ML-powered refund estimation
✅ 95% confidence intervals
✅ Best/worst/likely scenarios
✅ Global and regional risk monitoring
✅ Historical statistics
✅ Beautiful, professional UI

**Demo Flow:**
1. Show bookings list (2 min)
2. Click booking → Show refund estimation with confidence intervals (3 min)
3. Show risk monitor (2 min)
4. Show analytics (1 min)
5. Explain ML models and business value (2 min)

**This is a complete, impressive demo!**

## Summary

### To Complete ICA Integration:

1. ✅ Find MCP Server registration in Agent Orchestration
2. ✅ Register RefundEstimationAPI with your ngrok URL
3. ✅ Verify tools appear in AVAILABLE RESOURCES
4. ✅ Create agent using the chat interface
5. ✅ Deploy and test

### If Integration Takes Too Long:

1. ✅ Use your frontend demo (fully working!)
2. ✅ Show API documentation
3. ✅ Explain the architecture
4. ✅ Mention ICA integration as "future work"

**You have a complete, working system. The ICA integration is a bonus, not a requirement for an impressive demo!**

## Quick Decision Matrix

**Time Available:**
- **< 30 minutes:** Use frontend demo
- **30-60 minutes:** Try Agent Orchestration registration
- **> 60 minutes:** Complete full ICA integration

**For Hackathon:**
- Frontend demo is **safer** and **more impressive**
- ICA integration shows **enterprise thinking**
- Both together is **ideal** but not required

Good luck! 🚀