# Final ICA Integration Steps - Complete Guide

## Current Status
✅ Backend running with MCP endpoint
✅ MCP Server "RefundEstimationAPI" registered in ICA
✅ 7 tools available via MCP
❌ Tools NOT yet connected to the agent

## Problem
The agent has the MCP server registered, but the tools are not associated with the agent. ICA's interface for this specific assistant type doesn't show an "Add tools" button in the edit page.

## Solution: Create a New Assistant with Tools

Since the current agent interface doesn't allow adding MCP tools directly, we need to create a new assistant that includes the tools from the start.

### Step 1: Navigate to Assistant Creation

1. Go to **"Agent & Assistant Studio"** in left sidebar
2. Click **"Create"** or **"New Assistant"** button
3. Select **"Assistant"** (not Agent)

### Step 2: Configure the Assistant

**Name:**
```
TravelRefundAdvisor
```

**Description:**
```
AI-powered travel refund estimation assistant that helps customers understand refund options during force majeure events using ML predictions and confidence intervals.
```

**Instructions:**
```
You are a Travel Refund Estimation Assistant with access to a refund estimation API through MCP tools.

Your capabilities:
- Retrieve travel bookings and booking details
- Estimate refunds with ML-powered predictions and 95% confidence intervals
- Assess global and regional risk events
- Provide historical refund statistics
- Explain provider refund policies

When users ask about bookings or refunds:
1. Use the appropriate MCP tool (get_bookings, get_booking_details, estimate_refund, etc.)
2. Interpret the results clearly
3. Explain confidence intervals and uncertainty
4. Provide specific amounts and recommendations
5. Be professional and empathetic

Always include:
- Expected refund amounts
- Confidence intervals (lower/upper bounds)
- Best/worst/most likely scenarios
- Risk assessments
- Clear explanations
```

**Welcome Message:**
```
Hello! I'm your Travel Refund Estimation Assistant. I can help you understand your refund options for travel bookings affected by force majeure events. How can I assist you today?
```

### Step 3: Add MCP Tools

In the assistant creation form, look for:
- **"Tools"** section
- **"Add tools"** or **"Select tools"** button
- **"MCP Servers"** dropdown

Then:
1. Click **"Add tools"** or expand **"MCP Servers"**
2. Find **"RefundEstimationAPI"**
3. Select ALL 7 tools:
   - ☑ get_bookings
   - ☑ get_booking_details
   - ☑ estimate_refund
   - ☑ get_risk_events
   - ☑ get_regional_risk
   - ☑ get_refund_statistics
   - ☑ get_provider_policies

### Step 4: Configure Model Settings

**Model:** OpenAI GPT-4 or GPT-4 Turbo (recommended for tool use)

**Temperature:** 0.7 (balanced between creativity and consistency)

**Max Tokens:** 2000 (enough for detailed responses)

### Step 5: Save and Test

1. Click **"Create"** or **"Publish"**
2. Navigate to the assistant chat
3. Test with: **"Show me all my travel bookings"**

## Alternative: Use Existing Agent with Manual Tool Association

If you want to keep the existing agent:

### Option A: Through Agent Settings

1. Go to your **TravelRefundAdvisor** agent
2. Look for **"Settings"** or **"Configuration"** tab
3. Find **"MCP Servers"** or **"External Tools"** section
4. Associate **"RefundEstimationAPI"** with the agent
5. Save changes

### Option B: Through MCP Server Settings

1. Go to **"Tools"** section in left sidebar
2. Find **"RefundEstimationAPI"** MCP server
3. Click on it to open settings
4. Look for **"Associated Agents"** or **"Used by"** section
5. Add **"TravelRefundAdvisor"** to the list
6. Save changes

### Option C: Through Bulk Import (Advanced)

If ICA supports bulk import of assistant configurations:

1. Export your current agent configuration
2. Add MCP tools to the JSON/YAML
3. Re-import the configuration

## Test Prompts

Once tools are connected, test with these:

### Test 1: Basic Query
```
Show me all my travel bookings
```
**Expected:** Agent calls `get_bookings` tool and displays list

### Test 2: Specific Booking
```
Get details for booking ID 1
```
**Expected:** Agent calls `get_booking_details` with booking_id=1

### Test 3: Refund Estimation (Main Feature)
```
Estimate refund for booking 1 with high severity due to natural disaster
```
**Expected:** Agent calls `estimate_refund` and shows:
- Expected refund amount
- 95% confidence interval
- Best/worst/likely scenarios
- Risk score

### Test 4: Risk Assessment
```
What are the current global risk events?
```
**Expected:** Agent calls `get_risk_events` and lists events

### Test 5: Regional Risk
```
What's the risk level for Ukraine?
```
**Expected:** Agent calls `get_regional_risk` with region="Ukraine"

## Troubleshooting

### Issue: Agent still doesn't use tools

**Check:**
1. MCP server status is "Active" or "Connected"
2. Tools are explicitly associated with the agent
3. Agent has permission to use external tools
4. Model supports function calling (GPT-4, GPT-4 Turbo)

**Try:**
1. Recreate the assistant from scratch
2. Use a different agent/assistant template
3. Check ICA documentation for tool association
4. Contact ICA support if needed

### Issue: Tools return errors

**Check terminal for:**
- `[MCP] Received request: ...`
- `[MCP] Calling tool: ...`
- Any error messages

**Common fixes:**
1. Ensure backend is running
2. Ensure ngrok is active
3. Check ngrok URL hasn't changed
4. Verify API endpoints are accessible

## Quick Reference

**Backend:** `http://localhost:8000`
**MCP Endpoint:** `https://famished-vertebrae-basil.ngrok-free.dev/mcp`
**API Health:** `https://famished-vertebrae-basil.ngrok-free.dev/api/health`
**API Docs:** `https://famished-vertebrae-basil.ngrok-free.dev/api/docs`

**MCP Server Name:** RefundEstimationAPI
**Tools Count:** 7
**Status:** Registered and Active

## For Hackathon Demo

If you can't get MCP tools working in time:

### Fallback Option: Direct API Instructions

Update agent instructions to be more explicit:

```
When users ask about bookings, make HTTP GET requests to:
https://famished-vertebrae-basil.ngrok-free.dev/api/bookings

When users ask for refund estimates, make HTTP POST requests to:
https://famished-vertebrae-basil.ngrok-free.dev/api/estimate-refund/{booking_id}
with body: {"severity": "high", "event_type": "natural_disaster"}

Parse the JSON responses and explain them clearly to users.
```

Some AI assistants can make HTTP requests directly when given explicit instructions.

## Success Criteria

✅ Agent responds to "Show me all my bookings" with actual booking data
✅ Agent can estimate refunds with confidence intervals
✅ Agent can check risk events
✅ Terminal shows `[MCP] Calling tool: get_bookings`
✅ Responses include specific amounts and data from your API

Good luck! 🚀