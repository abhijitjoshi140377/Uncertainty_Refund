# ICA-MCP Context Forge Integration Guide

## Overview

This guide explains how to import the Refund Estimation API into IBM ICA (Intelligent Conversational Agents) using the MCP Context Forge bulk import feature.

## What is ICA-MCP Context Forge?

**ICA-MCP Context Forge** is IBM's tool for converting REST APIs into MCP (Model Context Protocol) tools that can be consumed by conversational AI agents. It allows you to:

- Import REST API endpoints as AI-accessible tools
- Define input schemas and validation rules
- Configure authentication and headers
- Filter and transform API responses
- Create reusable tool libraries for AI agents

## Prerequisites

1. **Backend Running**: Ensure the FastAPI backend is running on `http://localhost:8000`
2. **ICA Access**: Access to IBM ICA platform with Context Forge enabled
3. **Bulk Import File**: Use the provided `refund-api-bulk-import.json` file

## Quick Start

### Step 1: Start the Backend

```bash
cd backend
python main.py
```

Verify the API is accessible at: `http://localhost:8000/docs`

### Step 2: Access ICA-MCP Context Forge

1. Log into IBM ICA platform
2. Navigate to **Context Forge** or **MCP Tools**
3. Click **"Add New Tool from REST API"**
4. Select **"Bulk Import"** option

### Step 3: Import the Bulk File

1. Click **"Upload JSON"** or **"Import from File"**
2. Select `refund-api-bulk-import.json` from your project directory
3. Review the 11 tools that will be imported:
   - ✅ create-booking
   - ✅ get-bookings
   - ✅ get-booking-details
   - ✅ estimate-refund
   - ✅ get-refund-estimates
   - ✅ get-risk-events
   - ✅ get-regional-risk
   - ✅ get-historical-refunds
   - ✅ get-refund-statistics
   - ✅ get-provider-policies
   - ✅ get-provider-policy
4. Click **"Import All"** or select specific tools

### Step 4: Configure Base URL (if needed)

If your backend is running on a different host/port, update the URLs:

**Find and Replace:**
- From: `http://localhost:8000`
- To: `http://your-server:port`

Or use Context Forge's **"Base URL Override"** feature if available.

### Step 5: Test the Tools

Use ICA's test interface to verify each tool:

```json
// Test create-booking
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "booking_date": "2026-05-20T10:00:00Z",
  "travel_start_date": "2026-06-01T10:00:00Z",
  "travel_end_date": "2026-06-15T10:00:00Z",
  "destination_country": "France",
  "total_cost": 75000,
  "components": [
    {
      "component_type": "flight",
      "provider": "Air India",
      "cost": 50000,
      "booking_reference": "AI123456",
      "cancellation_policy": "50% refund if cancelled 7 days before"
    }
  ]
}
```

## Available Tools

### 1. create-booking
**Purpose**: Create new travel bookings  
**Method**: POST  
**Use Case**: When customer wants to book travel with multiple components

**Example Prompt for AI Agent**:
> "Create a booking for John Doe traveling to France from June 1-15, 2026. Include Air India flight for ₹50,000 and Taj Hotel for ₹25,000."

### 2. get-bookings
**Purpose**: List all bookings with pagination  
**Method**: GET  
**Use Case**: View all bookings or search for specific bookings

**Example Prompt**:
> "Show me all bookings" or "List the first 10 bookings"

### 3. get-booking-details
**Purpose**: Get detailed information for a specific booking  
**Method**: GET  
**Use Case**: View complete booking information including all components

**Example Prompt**:
> "Show me details for booking ID 123"

### 4. estimate-refund
**Purpose**: AI-powered refund estimation using ML models  
**Method**: POST  
**Use Case**: Estimate refund amount considering force majeure events

**Example Prompt**:
> "Estimate refund for booking 123 due to high severity natural disaster in Ukraine on May 20, 2026"

**Response Includes**:
- Expected refund amount and percentage
- 95% confidence interval (lower/upper bounds)
- Risk score (0-100)
- Best case, worst case, most likely scenarios
- Model version and confidence

### 5. get-refund-estimates
**Purpose**: List all refund estimates  
**Method**: GET  
**Use Case**: View history of refund estimations

**Example Prompt**:
> "Show me all refund estimates"

### 6. get-risk-events
**Purpose**: Get current global risk events  
**Method**: GET  
**Use Case**: Monitor active force majeure events worldwide

**Example Prompt**:
> "What are the current global risk events?"

### 7. get-regional-risk
**Purpose**: Get risk assessment for specific region  
**Method**: GET  
**Use Case**: Assess travel risk for a destination

**Example Prompt**:
> "What's the risk level for traveling to Ukraine?" or "Show me risk assessment for Middle East"

### 8. get-historical-refunds
**Purpose**: Retrieve historical refund data  
**Method**: GET  
**Use Case**: Analyze past refund patterns and trends

**Example Prompt**:
> "Show me historical refund data"

### 9. get-refund-statistics
**Purpose**: Get aggregated refund statistics  
**Method**: GET  
**Use Case**: View metrics like average refund amounts, success rates

**Example Prompt**:
> "What are the refund statistics?" or "Show me average refund amounts"

### 10. get-provider-policies
**Purpose**: List all provider cancellation policies  
**Method**: GET  
**Use Case**: Compare policies across providers

**Example Prompt**:
> "Show me all provider cancellation policies"

### 11. get-provider-policy
**Purpose**: Get specific provider's policy details  
**Method**: GET  
**Use Case**: View detailed policy for a specific provider

**Example Prompt**:
> "What's Air India's cancellation policy?" or "Show me Taj Hotels refund policy"

## Input Schema Details

### Booking Creation Schema

```json
{
  "customer_name": "string (required)",
  "customer_email": "string (email format, required)",
  "booking_date": "string (ISO 8601 datetime, required)",
  "travel_start_date": "string (ISO 8601 datetime, required)",
  "travel_end_date": "string (ISO 8601 datetime, required)",
  "destination_country": "string (required)",
  "total_cost": "number (minimum: 0, required)",
  "components": [
    {
      "component_type": "enum (flight|hotel|visa|insurance, required)",
      "provider": "string (required)",
      "cost": "number (minimum: 0, required)",
      "booking_reference": "string (optional)",
      "cancellation_policy": "string (optional)"
    }
  ]
}
```

### Refund Estimation Schema

```json
{
  "booking_id": "integer (minimum: 1, required)",
  "event_type": "enum (natural_disaster|political_unrest|pandemic|terrorism|economic_crisis|other, required)",
  "severity": "enum (low|medium|high|critical, required)",
  "affected_region": "string (required)",
  "event_date": "string (ISO 8601 datetime, required)"
}
```

## Response Format

All API responses follow this structure:

```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": {
    // Actual response data
  }
}
```

The `jsonpath_filter: "$.data"` in the bulk import file extracts only the `data` field, so AI agents receive clean, focused responses.

## Authentication

Currently, the API uses **no authentication** (`auth_type: "none"`). 

### Adding Authentication (Future)

If you add authentication to your API, update the bulk import file:

**Bearer Token:**
```json
{
  "auth_type": "bearer",
  "auth_value": "your-api-token-here"
}
```

**Basic Auth:**
```json
{
  "auth_type": "basic",
  "auth_value": "username:password"
}
```

**Custom Headers:**
```json
{
  "auth_type": "authheaders",
  "auth_value": "X-API-Key: your-api-key-here"
}
```

## URL Path Parameters

Some tools use path parameters (e.g., `{booking_id}`, `{region}`). Context Forge automatically:

1. Detects path parameters in the URL
2. Extracts them from the input schema
3. Substitutes values when making requests

**Example:**
- URL: `http://localhost:8000/api/bookings/{booking_id}`
- Input: `{"booking_id": 123}`
- Actual Request: `http://localhost:8000/api/bookings/123`

## Tags and Organization

Tools are tagged for easy filtering and organization:

- **booking**: Booking-related operations
- **refund**: Refund estimation and history
- **risk**: Risk monitoring and assessment
- **analytics**: Statistical analysis and reporting
- **provider**: Provider policy information
- **refund-estimation**: All tools in this project

Use tags in Context Forge to:
- Filter tools by category
- Create tool collections
- Organize agent capabilities

## Troubleshooting

### Issue: "Connection Refused" or "Cannot Connect"

**Solution:**
1. Verify backend is running: `http://localhost:8000/docs`
2. Check if port 8000 is available
3. Update URLs in bulk import if using different port

### Issue: "Invalid Input Schema"

**Solution:**
1. Check that all required fields are provided
2. Verify data types match schema (string, integer, etc.)
3. Ensure enums use exact values (case-sensitive)
4. Validate date-time format: ISO 8601 (e.g., `2026-05-20T10:00:00Z`)

### Issue: "404 Not Found"

**Solution:**
1. Verify API endpoint exists: Check `http://localhost:8000/docs`
2. Ensure path parameters are correctly substituted
3. Check for typos in URLs

### Issue: "422 Validation Error"

**Solution:**
1. Review the error response for field-level details
2. Check required fields are present
3. Verify data types and formats
4. Ensure enum values are valid

## Advanced Configuration

### Custom Headers

Add custom headers for specific requirements:

```json
{
  "headers": {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Request-ID": "unique-id",
    "X-Client-Version": "1.0.0"
  }
}
```

### Response Filtering with JSONPath

Use JSONPath to extract specific data from responses:

```json
{
  "jsonpath_filter": "$.data.bookings[*].{id: id, customer: customer_name}"
}
```

**Common JSONPath Patterns:**
- `$.data` - Extract data field
- `$.data.items[*]` - Extract all items from array
- `$.data.bookings[0]` - Get first booking
- `$.data.{id: id, name: customer_name}` - Transform response

### Pagination

For paginated endpoints, use `skip` and `limit` parameters:

```json
{
  "skip": 0,    // Start from first record
  "limit": 50   // Return 50 records
}
```

**Example Prompts:**
- "Show me the first 10 bookings" → `skip: 0, limit: 10`
- "Show me the next 10 bookings" → `skip: 10, limit: 10`
- "Show me bookings 21-30" → `skip: 20, limit: 10`

## Integration with AI Agents

### Claude Desktop

After importing tools in Context Forge, they become available to Claude:

**Example Conversation:**
```
User: I need to book a trip to France for June 2026

Claude: I'll help you create a booking. Let me use the create-booking tool...
[Uses create-booking tool with provided details]

Claude: Your booking has been created with reference BK12345678. 
The total cost is ₹75,000. Would you like me to estimate potential 
refund amounts in case of cancellation?

User: Yes, what if there's a natural disaster?

Claude: Let me estimate that for you...
[Uses estimate-refund tool]

Claude: Based on the AI model, if a high-severity natural disaster 
occurs in France, you can expect:
- Expected refund: ₹52,500 (70%)
- 95% confidence interval: ₹45,000 - ₹60,000
- Risk score: 75/100
```

### Cline (VS Code)

Tools are available in Cline's MCP interface:

```
User: Check if there are any risk events in Ukraine

Cline: [Uses get-regional-risk tool]
Result: High risk level detected in Ukraine due to ongoing 
political unrest. Risk score: 85/100. Travel advisory: Avoid 
non-essential travel.
```

## Best Practices

### 1. Tool Naming
- Use descriptive, action-oriented names
- Follow kebab-case convention (e.g., `create-booking`)
- Keep names concise but clear

### 2. Descriptions
- Write clear, 2-3 sentence descriptions
- Include use cases ("Use this when...")
- Mention key return values
- Explain business context

### 3. Input Schemas
- Mark all required fields explicitly
- Provide helpful descriptions for each field
- Use enums for fixed value sets
- Set appropriate min/max constraints
- Use format validators (email, date-time, etc.)

### 4. Error Handling
- Test all tools with invalid inputs
- Verify error messages are clear
- Check that validation errors are helpful
- Ensure 404/500 errors are handled gracefully

### 5. Testing
- Test each tool individually before bulk import
- Verify pagination works correctly
- Test path parameter substitution
- Validate response filtering with JSONPath
- Check authentication if enabled

## Production Deployment

### Update URLs for Production

Before deploying to production, update all URLs in the bulk import file:

```bash
# Find and replace
From: http://localhost:8000
To: https://api.yourcompany.com
```

### Add Authentication

Implement and configure authentication:

1. Add API key or OAuth to backend
2. Update `auth_type` and `auth_value` in bulk import
3. Test authentication with Context Forge
4. Document auth requirements for users

### Enable HTTPS

Ensure all production URLs use HTTPS:
- `https://api.yourcompany.com` ✅
- `http://api.yourcompany.com` ❌

### Rate Limiting

Consider adding rate limiting headers:

```json
{
  "headers": {
    "X-RateLimit-Limit": "1000",
    "X-RateLimit-Remaining": "999"
  }
}
```

## Support and Resources

### Documentation
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Project README**: `README.md`
- **API Enhancement Guide**: `backend/API_ENHANCEMENT_GUIDE.md`
- **Context Schema**: `context_schema.yaml`

### Example Files
- **Bulk Import**: `refund-api-bulk-import.json`
- **Sample Import**: `bulk-import-sample.json`
- **MCP Server**: `mcp_server/refund_mcp_server_production.py`

### Testing
- **Test Script**: `test_setup.py`
- **API Tests**: `backend/tests/test_api.py`

## Conclusion

The `refund-api-bulk-import.json` file provides a complete, production-ready configuration for importing all 11 Refund Estimation API endpoints into ICA-MCP Context Forge. 

**Key Benefits:**
✅ **One-Click Import** - All 11 tools in a single file  
✅ **Complete Schemas** - Full input validation and documentation  
✅ **AI-Optimized** - Descriptions tailored for conversational agents  
✅ **Production-Ready** - Proper error handling and response filtering  
✅ **Well-Documented** - Comprehensive descriptions and examples  

**Next Steps:**
1. Start your backend server
2. Import the bulk file into Context Forge
3. Test each tool with sample data
4. Integrate with your AI agents
5. Monitor usage and refine as needed

For questions or issues, refer to the project documentation or contact the development team.