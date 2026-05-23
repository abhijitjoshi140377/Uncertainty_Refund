# Missing Integration Step: Create Virtual MCP Server from External Endpoint

## The Missing Link

You have:
✅ External MCP Server registered (RefundEstimationAPI)
✅ Backend MCP endpoint working (`/mcp`)
❌ Virtual MCP Server to expose tools to agents

## Solution: Fill Out the "Add New Tools" Form

In the dialog you're seeing, fill it out like this:

### Field 1: Name
```
RefundEstimationTools
```

### Field 2: Card Description (Required)
```
Travel refund estimation tools with ML predictions and confidence intervals
```

### Field 3: Full Description
```
Complete set of tools for travel refund estimation including:
- Booking management (list and details)
- ML-powered refund estimation with 95% confidence intervals
- Global and regional risk assessment
- Historical refund statistics
- Provider policy information

These tools connect to the RefundEstimationAPI MCP server to provide real-time data and predictions for force majeure travel refund scenarios.
```

### Field 4: Server ID

This is the tricky part. You need to create a Virtual Server first. Here's how:

**Option A: If there's a "Create New Server" or "+" button:**
1. Click it
2. Enter Server Name: `RefundEstimationVirtualServer`
3. Enter MCP Endpoint URL: `https://famished-vertebrae-basil.ngrok-free.dev/mcp`
4. Save
5. Select it from the dropdown

**Option B: If you need to create it elsewhere:**
1. Cancel this dialog
2. Go to Settings or Admin section
3. Look for "Virtual Servers" or "MCP Servers"
4. Create new Virtual Server:
   - Name: `RefundEstimationVirtualServer`
   - Type: External/HTTP
   - URL: `https://famished-vertebrae-basil.ngrok-free.dev/mcp`
   - Protocol: JSON-RPC 2.0
5. Save
6. Come back to "Add New Tools" dialog
7. Select the Virtual Server from dropdown

**Option C: Use the External MCP Server directly:**

If the form allows, try entering the MCP endpoint URL directly:
```
https://famished-vertebrae-basil.ngrok-free.dev/mcp
```

### Field 5: Authentication Type

Select: **System Credentials** or **None** (since your API doesn't require auth)

### After Filling the Form:

1. Click **"Add"** button
2. ICA will connect to your MCP endpoint
3. It will discover the 7 tools
4. The tools will be created as a tool set
5. You can then add these tools to your agent

## Alternative: Import from OpenAPI

If the above doesn't work, try this simpler approach:

1. **Cancel the current dialog**
2. Look for **"Import from OpenAPI"** or **"Add from API Spec"** option
3. Enter your OpenAPI URL:
   ```
   https://famished-vertebrae-basil.ngrok-free.dev/openapi.json
   ```
4. ICA will automatically create tools for all your API endpoints
5. Select the 7 tools you need
6. Add them to your agent

## What Should Happen:

After successful creation, you should see:
- ✅ 7 new tools in the "Available Tools" list
- ✅ Each tool corresponds to an API endpoint
- ✅ Tools can be added to agents
- ✅ Agents can call these tools

## Test After Setup:

1. Add the tools to your TravelRefundAdvisor agent
2. Test with: "Show me all my travel bookings"
3. Check terminal for: `[MCP] Calling tool: get_bookings`
4. Agent should display actual booking data

## If Still Stuck:

The issue might be that ICA requires a specific Virtual Server configuration that's separate from External MCP Servers. In that case:

### Final Workaround: Manual REST API Tools

Create each tool individually as REST API tools (not MCP):

1. Go to Tools → Create Tool
2. For each of the 7 endpoints, create a REST API tool:
   - Tool 1: GET `/api/bookings`
   - Tool 2: GET `/api/bookings/{id}`
   - Tool 3: POST `/api/estimate-refund/{id}`
   - Tool 4: GET `/api/risk-events`
   - Tool 5: GET `/api/risk-events/regional/{region}`
   - Tool 6: GET `/api/statistics/refund-rates`
   - Tool 7: GET `/api/provider-policies`

This bypasses the MCP complexity and creates direct REST API tools.

## Summary

The missing step is creating a **Virtual MCP Server** or **Tool Set** that bridges your External MCP Server to ICA's agent system. Fill out the form in the dialog, or use the OpenAPI import method as an alternative.