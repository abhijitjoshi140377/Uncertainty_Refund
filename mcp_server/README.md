# MCP Server for Travel Refund Uncertainty Estimation System

This MCP (Model Context Protocol) server wraps the FastAPI refund estimation endpoints, making them accessible to ICA (Intelligent Conversational Agents) and other AI systems.

## Overview

The MCP server exposes 11 tools that allow AI agents to:
- Create and manage travel bookings
- Generate AI-powered refund estimates
- Query risk events and regional risks
- Access historical refund data and statistics
- Retrieve provider refund policies

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ICA Agent / AI System                 │
│                  (Claude, GPT, Custom AI)                │
└─────────────────────────────────────────────────────────┘
                            │
                            │ MCP Protocol
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   MCP Server (Python)                    │
│              refund_mcp_server.py                        │
│                                                           │
│  Tools:                                                   │
│  • create_booking                                         │
│  • get_bookings                                           │
│  • get_booking_details                                    │
│  • estimate_refund                                        │
│  • get_refund_estimates                                   │
│  • get_risk_events                                        │
│  • get_regional_risk                                      │
│  • get_historical_refunds                                 │
│  • get_refund_statistics                                  │
│  • get_provider_policies                                  │
│  • get_provider_policy                                    │
└─────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (localhost:8000)            │
│         Travel Refund Uncertainty Estimation API         │
└─────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

1. **Python 3.9+** installed
2. **FastAPI backend** running on `http://localhost:8000`

### Step 1: Install Dependencies

```bash
# Navigate to mcp_server directory
cd mcp_server

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Verify Backend is Running

Make sure your FastAPI backend is running:

```bash
# In another terminal, from project root
cd backend
python main.py
```

The backend should be accessible at `http://localhost:8000`

## Running the MCP Server

### Method 1: Direct Execution

```bash
cd mcp_server
python refund_mcp_server.py
```

### Method 2: Using MCP Configuration

Add to your MCP client configuration (e.g., Claude Desktop, Cline):

```json
{
  "mcpServers": {
    "refund-estimation": {
      "command": "python",
      "args": [
        "C:/Users/AbhijitJoshi/Uncertainty_Refund/mcp_server/refund_mcp_server.py"
      ],
      "env": {
        "API_BASE_URL": "http://localhost:8000/api"
      }
    }
  }
}
```

**For Claude Desktop**: Add to `%APPDATA%\Claude\claude_desktop_config.json`  
**For Cline**: Add to VS Code settings under MCP servers

## Available Tools

### 1. create_booking
Create a new travel booking with multiple components.

**Parameters:**
- `customer_name` (string, required): Customer's full name
- `customer_email` (string, required): Customer's email
- `travel_date` (string, required): ISO format date
- `destination` (string, required): Destination city/country
- `origin` (string, required): Origin city/country
- `components` (array, required): List of booking components

**Example:**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "travel_date": "2026-08-15T00:00:00",
  "destination": "Paris",
  "origin": "Mumbai",
  "components": [
    {
      "component_type": "flight",
      "provider_name": "Air India",
      "cost": 50000,
      "is_refundable": true,
      "cancellation_fee": 500
    },
    {
      "component_type": "hotel",
      "provider_name": "Marriott",
      "cost": 25000,
      "is_refundable": true,
      "cancellation_fee": 1000
    }
  ]
}
```

### 2. get_bookings
Retrieve all bookings with pagination.

**Parameters:**
- `skip` (integer, optional): Records to skip (default: 0)
- `limit` (integer, optional): Max records (default: 100)

### 3. get_booking_details
Get detailed information about a specific booking.

**Parameters:**
- `booking_id` (integer, required): Booking ID

### 4. estimate_refund
Generate AI-powered refund estimate for a booking.

**Parameters:**
- `booking_id` (integer, required): Booking ID
- `selected_model` (string, optional): ML model (auto, random_forest, gradient_boosting, rule_based)
- `calamity_type` (string, optional): Event type (auto, war, pandemic, natural_disaster, political_unrest)
- `severity` (string, optional): Severity level (low, medium, high, critical)

**Example:**
```json
{
  "booking_id": 1,
  "selected_model": "auto",
  "calamity_type": "pandemic",
  "severity": "high"
}
```

**Returns:**
- Expected refund amount and percentage
- Confidence intervals (95% level)
- Risk score and level
- Best/worst/most likely case scenarios
- Model version and confidence

### 5. get_refund_estimates
Get all refund estimates for a booking.

**Parameters:**
- `booking_id` (integer, required): Booking ID

### 6. get_risk_events
Get current global risk events.

**Parameters:**
- `active_only` (boolean, optional): Return only active events (default: true)

### 7. get_regional_risk
Get risk assessment for a specific region.

**Parameters:**
- `region` (string, required): Region or country name

**Example:**
```json
{
  "region": "Ukraine"
}
```

**Returns:**
- Risk level (low, medium, high, critical)
- Active events in the region
- Event details

### 8. get_historical_refunds
Get historical refund data for analysis.

**Parameters:**
- `component_type` (string, optional): Filter by flight, hotel, visa, insurance
- `event_type` (string, optional): Filter by event type
- `limit` (integer, optional): Max records (default: 100)

### 9. get_refund_statistics
Get aggregated refund statistics.

**Returns:**
- Average refund percentages by component and event type
- Total cases and force majeure cases
- Average refund amounts

### 10. get_provider_policies
Get refund policies for travel providers.

**Parameters:**
- `provider_type` (string, optional): Filter by airline, hotel, visa_service, insurance

### 11. get_provider_policy
Get detailed policy for a specific provider.

**Parameters:**
- `provider_name` (string, required): Provider name

## Usage Examples

### Example 1: AI Agent Creates Booking and Gets Estimate

```
User: "I need to book a trip to Paris from Mumbai for August 15, 2026. 
       Flight costs ₹50,000 and hotel costs ₹25,000. What refund can I expect 
       if there's a pandemic?"

AI Agent Actions:
1. Calls create_booking with the details
2. Gets booking_id from response
3. Calls estimate_refund with booking_id and calamity_type="pandemic"
4. Returns refund estimate to user
```

### Example 2: AI Agent Checks Regional Risk

```
User: "Is it safe to travel to Ukraine right now?"

AI Agent Actions:
1. Calls get_regional_risk with region="Ukraine"
2. Analyzes risk level and active events
3. Provides risk assessment to user
```

### Example 3: AI Agent Analyzes Historical Trends

```
User: "What's the average refund for flight cancellations during pandemics?"

AI Agent Actions:
1. Calls get_historical_refunds with component_type="flight" and event_type="pandemic"
2. Calls get_refund_statistics
3. Analyzes data and provides insights
```

## Configuration

### Environment Variables

You can configure the MCP server using environment variables:

```bash
# API base URL (default: http://localhost:8000/api)
export API_BASE_URL="http://localhost:8000/api"
```

### Changing API URL

Edit `refund_mcp_server.py` line 23:

```python
API_BASE_URL = "http://your-api-url:port/api"
```

## Troubleshooting

### Issue: "Connection refused" or "API not reachable"

**Solution:**
1. Ensure FastAPI backend is running: `http://localhost:8000`
2. Test API health: `curl http://localhost:8000/api/health`
3. Check firewall settings

### Issue: "Module 'mcp' not found"

**Solution:**
```bash
pip install mcp>=0.9.0
```

### Issue: "Module 'httpx' not found"

**Solution:**
```bash
pip install httpx>=0.27.0
```

### Issue: MCP server not appearing in Claude/Cline

**Solution:**
1. Check config file path is correct
2. Restart Claude Desktop or VS Code
3. Verify Python path in config
4. Check MCP server logs

## Testing the MCP Server

### Test 1: List Available Tools

The MCP server should expose 11 tools when connected.

### Test 2: Create a Test Booking

Use the `create_booking` tool with sample data.

### Test 3: Generate Refund Estimate

Use the `estimate_refund` tool with a booking ID.

### Test 4: Query Risk Events

Use the `get_risk_events` tool to see active global risks.

## Integration with AI Agents

### Claude Desktop

1. Add MCP server to `claude_desktop_config.json`
2. Restart Claude Desktop
3. Claude will automatically discover and use the tools

### Cline (VS Code)

1. Add MCP server to VS Code settings
2. Reload VS Code
3. Cline will have access to all tools

### Custom AI Agents

Use the MCP protocol to connect your custom AI agent:

```python
from mcp.client import Client

async def use_refund_tools():
    async with Client() as client:
        # Connect to MCP server
        await client.connect("refund-estimation")
        
        # List available tools
        tools = await client.list_tools()
        
        # Call a tool
        result = await client.call_tool(
            "estimate_refund",
            {"booking_id": 1, "severity": "high"}
        )
```

## Security Considerations

1. **Local Network Only**: The MCP server connects to `localhost:8000` by default
2. **No Authentication**: Currently no auth between MCP server and FastAPI (add if needed)
3. **Input Validation**: All inputs are validated by FastAPI backend
4. **Rate Limiting**: Consider adding rate limiting for production use

## Performance

- **Response Time**: < 500ms for most operations
- **Estimate Generation**: 1-3 seconds (includes ML inference)
- **Concurrent Requests**: Supports async operations
- **Timeout**: 30 seconds per API call

## Logging

The MCP server logs all tool calls and API interactions. Check logs for debugging:

```bash
# Run with verbose logging
python refund_mcp_server.py --verbose
```

## Contributing

To add new tools:

1. Add tool definition in `list_tools()`
2. Add handler in `call_tool()`
3. Update this README with tool documentation

## Support

- **FastAPI Backend Docs**: http://localhost:8000/api/docs
- **MCP Protocol**: https://modelcontextprotocol.io
- **Project Repository**: https://github.com/abhijitjoshi140377/Uncertainty_Refund

## Version History

- **v1.0.0** (2026-05-20): Initial release with 11 tools

---

**Made with ❤️ for AI Agent Integration**