# Final Solution: Manually Create MCP Tools in ICA

## The Real Problem

ICA agents can't make arbitrary HTTP requests for security reasons. They need formally registered tools. The MCP server is registered, but the individual tools aren't showing up in the agent's tool selection.

## Solution: Create Tools Manually

Since the MCP server tools aren't appearing, we need to create them as individual REST API tools in ICA.

### Step 1: Navigate to Tools Section

1. Go to **"Tools"** in the left sidebar (wrench icon)
2. Click **"Browse Tools"** or **"All Tools"**
3. Click **"Create Tool"** or **"Add New"** button

### Step 2: Create Each Tool Individually

Create 7 separate tools (one for each endpoint):

---

#### Tool 1: Get Bookings

**Name:** `get_bookings`

**Description:** `Retrieve all travel bookings from the system`

**Type:** REST API

**Method:** GET

**URL:** `https://famished-vertebrae-basil.ngrok-free.dev/api/bookings`

**Parameters:** None

**Response Type:** JSON

**Save** this tool

---

#### Tool 2: Get Booking Details

**Name:** `get_booking_details`

**Description:** `Get detailed information for a specific booking`

**Type:** REST API

**Method:** GET

**URL:** `https://famished-vertebrae-basil.ngrok-free.dev/api/bookings/{booking_id}`

**Parameters:**
- `booking_id` (path parameter, required, integer)

**Response Type:** JSON

**Save** this tool

---

#### Tool 3: Estimate Refund (Most Important!)

**Name:** `estimate_refund`

**Description:** `Estimate refund amount with ML predictions and 95% confidence intervals`

**Type:** REST API

**Method:** POST

**URL:** `https://famished-vertebrae-basil.ngrok-free.dev/api/estimate-refund/{booking_id}`

**Path Parameters:**
- `booking_id` (required, integer)

**Body Parameters (JSON):**
```json
{
  "severity": "high",
  "event_type": "natural_disaster"
}
```

**Body Schema:**
- `severity` (required, string, enum: ["low", "medium", "high"])
- `event_type` (required, string, enum: ["war", "pandemic", "natural_disaster", "political_unrest", "terrorism"])

**Response Type:** JSON

**Save** this tool

---

#### Tool 4: Get Risk Events

**Name:** `get_risk_events`

**Description:** `Get current global risk events affecting travel`

**Type:** REST API

**Method:** GET

**URL:** `https://famished-vertebrae-basil.ngrok-free.dev/api/risk-events`

**Query Parameters:**
- `active_only` (optional, boolean, default: true)

**Response Type:** JSON

**Save** this tool

---

#### Tool 5: Get Regional Risk

**Name:** `get_regional_risk`

**Description:** `Get risk assessment for a specific region`

**Type:** REST API

**Method:** GET

**URL:** `https://famished-vertebrae-basil.ngrok-free.dev/api/risk-events/regional/{region}`

**Parameters:**
- `region` (path parameter, required, string)

**Response Type:** JSON

**Save** this tool

---

#### Tool 6: Get Refund Statistics

**Name:** `get_refund_statistics`

**Description:** `Get historical refund statistics`

**Type:** REST API

**Method:** GET

**URL:** `https://famished-vertebrae-basil.ngrok-free.dev/api/statistics/refund-rates`

**Query Parameters:**
- `component_type` (optional, string, enum: ["flight", "hotel", "visa", "insurance"])
- `event_type` (optional, string, enum: ["war", "pandemic", "natural_disaster", "political_unrest", "terrorism"])

**Response Type:** JSON

**Save** this tool

---

#### Tool 7: Get Provider Policies

**Name:** `get_provider_policies`

**Description:** `Get refund policies for travel providers`

**Type:** REST API

**Method:** GET

**URL:** `https://famished-vertebrae-basil.ngrok-free.dev/api/provider-policies`

**Parameters:** None

**Response Type:** JSON

**Save** this tool

---

### Step 3: Add Tools to Your Agent

After creating all 7 tools:

1. Go back to your **TravelRefundAdvisor** agent
2. Click **"Edit"**
3. Scroll to **"Tools"** section
4. Click **"Add tools"**
5. Search for the tools you just created (get_bookings, estimate_refund, etc.)
6. Select all 7 tools
7. Click **"Apply"** or **"Add"**
8. Click **"Save"** or **"Publish"**

### Step 4: Update Agent Instructions

Use these simplified instructions:

```
You are a Travel Refund Estimation Assistant with access to 7 tools for refund estimation and risk assessment.

When users ask about bookings, use get_bookings or get_booking_details.
When users ask about refund estimates, use estimate_refund with appropriate severity and event_type.
When users ask about risks, use get_risk_events or get_regional_risk.
When users ask about statistics or policies, use get_refund_statistics or get_provider_policies.

Always explain:
- Confidence intervals clearly (95% CI with lower and upper bounds)
- Best case, worst case, and most likely scenarios
- Risk scores and what they mean
- Specific amounts and percentages

Be professional, empathetic, and provide actionable recommendations.
```

### Step 5: Test

Test with: **"Show me all my travel bookings"**

The agent should now use the `get_bookings` tool and display actual data!

## Why This Works

- REST API tools are natively supported by ICA
- They don't require MCP protocol complexity
- They integrate directly with the agent's tool-calling capability
- They're easier to configure and debug

## Alternative: Use OpenAPI Import

If ICA supports OpenAPI import:

1. Go to **"Tools"** → **"Import"** or **"Add from OpenAPI"**
2. Enter URL: `https://famished-vertebrae-basil.ngrok-free.dev/openapi.json`
3. ICA will automatically create all 11 tools from your API
4. Select the 7 tools you need
5. Add them to your agent

This is much faster than creating tools manually!

## Success Criteria

✅ 7 tools created in ICA Tools section
✅ All 7 tools added to TravelRefundAdvisor agent
✅ Agent responds with actual booking data
✅ Terminal shows API calls: `GET /api/bookings HTTP/1.1 200 OK`
✅ Refund estimates include confidence intervals

## For Your Hackathon Demo

If you're running out of time:

### Plan A: Use the Frontend
- Demo the React frontend at `http://localhost:5173`
- Show all features: bookings, refund estimation, risk monitoring, analytics
- Explain the ML models and confidence intervals
- This is a complete, working demo!

### Plan B: Use API Documentation
- Show the Swagger docs at `/api/docs`
- Demonstrate API calls with curl or Postman
- Explain the ML predictions and uncertainty quantification
- Show the backend code and models

### Plan C: Hybrid Approach
- Use frontend for main demo
- Show ICA agent as "future enhancement"
- Explain how it would work with proper tool integration
- Judges will appreciate the technical depth

## Bottom Line

The technical work is solid:
✅ Backend API working perfectly
✅ ML models trained and predicting
✅ Confidence intervals calculated
✅ MCP server implemented
✅ Frontend fully functional

The only issue is ICA's tool integration UI, which is a platform limitation, not your code!

Good luck! 🚀