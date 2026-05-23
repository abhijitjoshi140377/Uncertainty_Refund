# Hackathon Demo Workaround - Working Solution

## Problem
ICA's interface doesn't show the MCP tools in the "Add tools" dialog, even though the MCP server is registered and working.

## Solution: Use the Agent's Natural Language Understanding

Since ICA agents are powered by GPT-4, they can understand API documentation and make HTTP requests when properly instructed. We'll use this capability instead of formal MCP tool integration.

## Step-by-Step Setup

### 1. Update Agent Instructions

In your agent's **"Instructions"** text box, replace the current content with this:

```
You are a Travel Refund Estimation Assistant with direct access to a refund estimation API.

API BASE URL: https://famished-vertebrae-basil.ngrok-free.dev

AVAILABLE API ENDPOINTS:

1. GET /api/bookings
   - Lists all travel bookings
   - Returns: Array of bookings with id, customer, destination, dates, total_cost

2. GET /api/bookings/{booking_id}
   - Gets detailed booking information
   - Parameter: booking_id (integer)
   - Returns: Full booking details with all components (flights, hotels, visas, insurance)

3. POST /api/estimate-refund/{booking_id}
   - Estimates refund with ML predictions and 95% confidence intervals
   - Parameter: booking_id (integer)
   - Request body: {
       "severity": "low" | "medium" | "high",
       "event_type": "war" | "pandemic" | "natural_disaster" | "political_unrest" | "terrorism"
     }
   - Returns: {
       "booking_id": int,
       "expected_refund": float,
       "confidence_interval": {"lower": float, "upper": float},
       "scenarios": {"best_case": float, "worst_case": float, "most_likely": float},
       "risk_score": float,
       "component_estimates": [...]
     }

4. GET /api/risk-events?active_only=true
   - Gets current global risk events
   - Returns: Array of events with type, severity, affected_regions, start_date

5. GET /api/risk-events/regional/{region}
   - Gets risk assessment for specific region
   - Parameter: region (string, e.g., "Ukraine", "Middle East")
   - Returns: Aggregate risk level and active events

6. GET /api/statistics/refund-rates?component_type=flight&event_type=pandemic
   - Gets historical refund statistics
   - Optional parameters: component_type, event_type
   - Returns: Average refund rates and success rates

7. GET /api/provider-policies
   - Gets provider refund policies
   - Returns: Array of providers with standard and force majeure refund percentages

HOW TO USE THESE ENDPOINTS:

When users ask questions, make HTTP requests to the appropriate endpoint and interpret the results.

Example 1: User asks "Show me my bookings"
- Make GET request to: https://famished-vertebrae-basil.ngrok-free.dev/api/bookings
- Parse the JSON response
- Present the bookings in a clear, formatted way

Example 2: User asks "Estimate refund for booking 1 due to natural disaster"
- Make POST request to: https://famished-vertebrae-basil.ngrok-free.dev/api/estimate-refund/1
- Body: {"severity": "high", "event_type": "natural_disaster"}
- Parse the response and explain:
  * Expected refund amount
  * 95% confidence interval (lower to upper bounds)
  * Best case, worst case, and most likely scenarios
  * Risk score
  * Component-wise breakdown

Example 3: User asks "What are current risk events?"
- Make GET request to: https://famished-vertebrae-basil.ngrok-free.dev/api/risk-events?active_only=true
- Parse and present the events with severity levels

RESPONSE GUIDELINES:

1. Always make the API call first, then respond based on actual data
2. Explain confidence intervals clearly: "There's a 95% chance your refund will be between $X and $Y"
3. Present scenarios: "Best case: $A, Most likely: $B, Worst case: $C"
4. Be empathetic and professional
5. Provide specific amounts and percentages
6. Cite the data source (ML predictions, historical data, etc.)
7. Give actionable recommendations

IMPORTANT:
- All API responses are in JSON format
- Parse the JSON and present it in human-readable format
- Always include confidence intervals when discussing refund estimates
- Explain uncertainty and risk clearly
- Use the actual data from the API, don't make up numbers
```

### 2. Update "What would you like to create?"

```
A travel refund estimation assistant that queries a live API to provide ML-powered refund estimates with confidence intervals, assess global and regional risks, and help customers understand their refund options during force majeure events.
```

### 3. Save and Test

1. Click **"Save"** or **"Publish"**
2. Go to the agent chat
3. Test with: **"Show me all my travel bookings"**

## Expected Behavior

The agent should:
1. Understand it needs to call the API
2. Make an HTTP GET request to `/api/bookings`
3. Parse the JSON response
4. Present the bookings in a clear format

You should see in the terminal:
```
INFO: 127.0.0.1:xxxxx - "GET /api/bookings HTTP/1.1" 200 OK
```

## Test Prompts for Demo

### Test 1: List Bookings
```
Show me all my travel bookings
```

### Test 2: Booking Details
```
Get details for booking ID 1
```

### Test 3: Refund Estimation (Main Feature)
```
I need to cancel booking 1 due to a natural disaster. Can you estimate my refund with high severity?
```

### Test 4: Risk Events
```
What are the current global risk events affecting travel?
```

### Test 5: Regional Risk
```
I'm planning to travel to Ukraine. What's the current risk level?
```

### Test 6: Statistics
```
Show me historical refund statistics for flight cancellations during pandemics
```

### Test 7: Provider Policies
```
What are the refund policies for different travel providers?
```

## Why This Works

Modern AI assistants (GPT-4) have the capability to:
- Understand API documentation
- Make HTTP requests
- Parse JSON responses
- Present data in human-readable format

By providing clear API documentation in the instructions, the agent can function as if it has native tool access.

## Advantages for Hackathon

✅ **No complex MCP setup needed**
✅ **Works immediately**
✅ **More flexible** - agent can combine multiple API calls
✅ **Easier to debug** - just check terminal logs
✅ **Demonstrates AI capabilities** - shows the agent can understand and use APIs

## Monitoring

Watch your terminal for API calls:
```
INFO: GET /api/bookings HTTP/1.1 200 OK
INFO: POST /api/estimate-refund/1 HTTP/1.1 200 OK
INFO: GET /api/risk-events HTTP/1.1 200 OK
```

Each successful call means the agent is working correctly!

## Troubleshooting

### If agent says "I can't access the API":
- Make sure backend is running
- Make sure ngrok is active
- Try being more explicit: "Make an HTTP GET request to https://famished-vertebrae-basil.ngrok-free.dev/api/bookings"

### If agent returns generic responses:
- The agent might not have web access enabled
- Check agent settings for "Web Search" or "External API" capabilities
- Try a different agent template that supports external calls

### If nothing works:
- Use the frontend demo instead
- Show the API documentation at `/api/docs`
- Demonstrate the ML models and confidence intervals through the web UI

## Success Criteria

✅ Agent responds with actual booking data (not generic responses)
✅ Terminal shows API calls being made
✅ Refund estimates include confidence intervals
✅ Risk events show current data
✅ Agent explains results clearly

Good luck with your hackathon! 🚀