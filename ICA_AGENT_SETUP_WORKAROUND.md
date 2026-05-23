# ICA Agent Setup - Workaround for Hackathon

## Problem
The MCP HTTP endpoint has compatibility issues with FastMCP and ICA's transport layer.

## Solution
Use ICA's natural language capabilities with explicit API instructions instead of MCP tools.

## Steps to Configure Your Agent

### 1. Cancel the MCP Server Setup
- Click "Cancel" on the "Add External MCP Server" form
- We'll use a different approach

### 2. Edit Your Agent Instructions

Go back to your agent edit page and update the **Instructions** field with this:

```
You are a Travel Refund Estimation Assistant that helps customers understand refund options during force majeure events.

IMPORTANT: You have access to a refund estimation API. When users ask about bookings or refunds, make HTTP requests to these endpoints:

API Base URL: https://famished-vertebrae-basil.ngrok-free.dev

Available Endpoints:

1. GET /api/bookings
   - Lists all travel bookings
   - Returns: booking_id, customer info, destination, dates, costs

2. GET /api/bookings/{booking_id}
   - Gets detailed booking information
   - Returns: full booking details with all components

3. POST /api/estimate-refund/{booking_id}
   - Estimates refund for a booking
   - Body: {"severity": "low|medium|high", "event_type": "war|pandemic|natural_disaster|political_unrest|terrorism"}
   - Returns: expected_refund, confidence_interval, scenarios, risk_score

4. GET /api/risk-events
   - Lists current global risk events
   - Optional params: ?active_only=true
   - Returns: events with severity, type, affected regions

5. GET /api/risk-events/regional/{region}
   - Gets risk assessment for specific region
   - Returns: aggregate risk level, active events

6. GET /api/statistics/refund-rates
   - Gets historical refund statistics
   - Optional params: ?component_type=flight&event_type=pandemic
   - Returns: average refund rates, success rates

7. GET /api/provider-policies
   - Lists provider refund policies
   - Returns: standard and force majeure refund percentages

When users ask questions:
- Use the appropriate endpoint
- Explain the results clearly
- Include specific amounts and confidence intervals
- Be professional and empathetic
- Provide actionable recommendations

Example interactions:
- "Show me my bookings" → Call GET /api/bookings
- "Estimate refund for booking 1" → Call POST /api/estimate-refund/1 with appropriate severity
- "What are current risks?" → Call GET /api/risk-events
```

### 3. Update Welcome Message

```
Hello! I'm your Travel Refund Estimation Assistant. I can help you understand your refund options for travel bookings affected by force majeure events. How can I assist you today?
```

### 4. Save the Agent

Click "Save" or "Publish" to update your agent.

### 5. Test the Agent

Try these prompts:
1. "Show me all my bookings"
2. "Get details for booking ID 1"
3. "Estimate refund for booking 1 with high severity"
4. "What are current global risk events?"

## Why This Works

ICA's agents (powered by GPT models) can understand API documentation in natural language and make HTTP requests when properly instructed. This is actually more flexible than MCP for a hackathon demo because:

1. ✅ No complex MCP server setup needed
2. ✅ Works with any HTTP API
3. ✅ Agent can intelligently choose which endpoint to call
4. ✅ Can handle complex multi-step workflows
5. ✅ Easier to debug and modify

## Alternative: Use Function Calling

If the above doesn't work, ICA might support OpenAI-style function calling. In that case:

1. Go to agent settings
2. Look for "Functions" or "Tools" section
3. Add each API endpoint as a function with JSON schema
4. ICA will automatically call them when needed

## For Production

For a production system, you would:
1. Fix the FastMCP compatibility issues
2. Use proper MCP transport (SSE or WebSocket)
3. Add authentication
4. Use a permanent domain (not ngrok)

## Hackathon Demo Tips

1. Keep backend running: `python main.py`
2. Keep ngrok running: `ngrok http 8000`
3. Test 2-3 prompts before presenting
4. Have backup screenshots ready
5. Explain the ML models and confidence intervals
6. Emphasize the business value

Good luck! 🚀