# IBM Context Studio Integration Guide
## Travel Refund Uncertainty Estimation System

Complete step-by-step guide following IBM Context Studio's 4-step workflow:
1. **Start with a Schema** — Define your schema with method, industry, domain knowledge
2. **Create a Context** — Create context space to add connectors, attach schemas, upload contents
3. **Add Sources & Data** — Ingest and validate your context, with or without schema
4. **Expose via MCP** — Make your context available to external applications

---

## Prerequisites ✅

Before starting, ensure you have:

1. ✅ **Backend API Running**
   - Terminal 1: `cd backend && python main.py`
   - Running on: http://localhost:8000

2. ✅ **Ngrok Tunnel Active**
   - Terminal 2: `cd backend && ngrok http 8000`
   - Public URL: https://famished-vertebrae-basil.ngrok-free.dev

3. ✅ **IBM Cloud Account**
   - Access to IBM Cloud: https://cloud.ibm.com
   - Context Studio enabled

4. ✅ **API Endpoints Working**
   - Test: https://famished-vertebrae-basil.ngrok-free.dev/api/health
   - Should return: `{"status": "healthy", ...}`

5. ✅ **Schema File Ready**
   - File: `context_schema.yaml` (already in your project ✅)

---

## Access IBM Context Studio

### Step 1: Login to IBM Cloud

1. Go to: **https://cloud.ibm.com**
2. Click **"Log in"**
3. Enter your IBM Cloud credentials
4. Complete authentication

### Step 2: Navigate to Context Studio

1. Go to: **https://context-studio.cloud.ibm.com**
2. Or from IBM Cloud Dashboard:
   - Click **"Catalog"**
   - Search for **"Context Studio"**
   - Click **"Launch Context Studio"**

You should see the welcome screen with 4 steps.

---

## STEP 1: Start with a Schema (Optional)

### ⚠️ Important: Schema is Optional!

IBM Context Studio allows you to:
- **Option A**: Create/upload a schema (recommended for structured data)
- **Option B**: Skip schema and proceed without it (faster, less structured)

### Should You Use a Schema?

**Use Schema If:**
- ✅ You want structured, validated data
- ✅ You need clear entity relationships
- ✅ You want better AI understanding of your domain
- ✅ You have complex data models
- ✅ You want type checking and validation

**Skip Schema If:**
- ✅ You want quick setup
- ✅ Your API is self-documenting (OpenAPI/Swagger)
- ✅ You prefer flexibility over structure
- ✅ You're prototyping or testing

---

## Option A: Create Schema (Recommended)

### What is a Schema?

A schema defines the structure of your domain knowledge:
- **Method**: How your system works (APIs, data flow)
- **Industry**: Travel and tourism
- **Domain Knowledge**: Refund estimation, force majeure events, booking management

### A1: Upload Your Existing Schema

You now have a JSON-LD schema file: `context_schema.jsonld`

**⚠️ Important**: IBM Context Studio requires **JSON-LD format**, not YAML.

1. **In Context Studio:**
   - Click **"Start with a Schema"** or **"Create Schema"**
   - Click **"Upload Schema"** or **"Import"**

2. **Upload File:**
   - Click **"Choose File"**
   - Select: `context_schema.jsonld` from your project ✅
   - **Do NOT use** `context_schema.yaml` (will cause error)
   - Click **"Upload"**

3. **Review Schema:**
   - Context Studio will parse your JSON-LD file
   - Review the structure:
     - Backend API endpoints (11 endpoints)
     - Data models (BookingCreate, RefundEstimateRequest, etc.)
     - ML models (random_forest, gradient_boosting)
     - Business rules
     - Enums and types
   - Click **"Confirm"** or **"Save"**

4. **Configure Schema Options:**
   - **Name**: `Refund Estimation Schema`
   - **Description**: `Schema for travel refund uncertainty estimation system with AI-powered predictions`
   - **Version**: `1.0.0`
   - **Industry**: `Travel & Tourism`
   - **Domain**: `Refund Management, Risk Assessment`
   
5. **Include Method Checkbox:**
   - ☑️ **Check "Include Method"** (Recommended)
   - **What it does**: Enables method/process details from your schema to be passed to AI agents via the `getSchemas` MCP tool
   - **Why enable it**:
     - AI agents will understand your system's workflow
     - Better planning and decision-making by agents
     - Agents can see how refund estimation process works
     - Includes business logic and rules from your schema
   - **Your schema includes**:
     - Refund calculation methods
     - ML model selection logic
     - Risk assessment process
     - API workflow and dependencies
   
6. **Click "Create"**

### Option B: Create Schema Manually

If upload doesn't work, create schema manually:

1. **Click "Create New Schema"**

2. **Basic Information:**
   - **Name**: `Refund Estimation Schema`
   - **Version**: `1.0.0`
   - **Description**: `AI-powered travel refund estimation system`

3. **Define Entities:**

   **Entity 1: Booking**
   - Name: `TravelBooking`
   - Properties:
     - `id` (integer)
     - `booking_reference` (string)
     - `customer_name` (string)
     - `customer_email` (string)
     - `travel_date` (datetime)
     - `destination` (string)
     - `origin` (string)
     - `total_cost` (float)
     - `status` (enum: active, cancelled, completed, refunded)

   **Entity 2: RefundEstimate**
   - Name: `RefundEstimate`
   - Properties:
     - `id` (integer)
     - `booking_id` (integer)
     - `expected_refund_amount` (float)
     - `expected_refund_percentage` (float)
     - `confidence_lower` (float)
     - `confidence_upper` (float)
     - `risk_score` (float)
     - `current_risk_level` (enum: low, medium, high, critical)

   **Entity 3: RiskEvent**
   - Name: `RiskEvent`
   - Properties:
     - `id` (integer)
     - `event_type` (enum: war, pandemic, natural_disaster, political_unrest, terrorism)
     - `severity` (enum: low, medium, high, critical)
     - `affected_region` (string)
     - `is_active` (boolean)

4. **Define Relationships:**
   - `TravelBooking` → has many → `BookingComponent`
   - `TravelBooking` → has many → `RefundEstimate`
   - `RiskEvent` → affects → `TravelBooking`

5. **Include Method Checkbox:**
   - ☑️ **Check "Include Method"** (Recommended)
   - This ensures method/process details are available to AI agents
   - Helps agents understand your system's workflow and business logic
   - Passed via `getSchemas` MCP tool for agent planning

6. **Save Schema**

---

## Option B: Skip Schema (Quick Setup)

### When to Skip Schema

Skip schema creation if:
- You want to get started quickly
- Your API endpoints are well-documented
- You don't need strict data validation
- You're testing or prototyping

### How to Skip Schema

1. **In Context Studio Welcome Screen:**
   - You'll see: "Start with a Schema" (Step 1)
   - Look for **"Skip"** or **"Continue without schema"** button
   - Click it to proceed directly to Step 2

2. **Or Click "Next" Without Creating Schema:**
   - Some versions allow you to click "Next" or "Continue"
   - This moves you to Step 2 without schema

3. **Result:**
   - You proceed to Step 2 (Create Context)
   - Context Studio will work without schema
   - Data structure inferred from API responses
   - Less validation but more flexibility

---

## STEP 2: Create a Context

### What is a Context?

A context is a container that:
- Holds your schema
- Connects to data sources
- Organizes domain knowledge
- Makes data accessible to AI

### Create Your Context

1. **In Context Studio:**
   - Click **"Create a Context"** or **"New Context"**

2. **Configure Context:**
   - **Name**: `Refund Estimation Context`
   - **Description**: `Context for travel refund estimation with real-time risk assessment`
   - **Type**: Select **"API-based"** or **"Dynamic"**
   - **Attach Schema**:
     - If you created schema: Select `Refund Estimation Schema`
     - If you skipped schema: Leave as "None" or "No schema"
   - Click **"Create"**

3. **Context Settings:**
   - **Access Level**: Private (or as needed)
   - **Refresh Rate**: Real-time (for live API data)
   - **Cache Duration**: 5 minutes (or as needed)
   - Click **"Save"**

---

## STEP 3: Add Sources & Data

### What are Sources?

Sources are where your data comes from:
- REST APIs (your FastAPI backend)
- Databases
- Files
- Other systems

### Add Your API as a Data Source

#### 3.1: Add API Connector

1. **In Your Context:**
   - Go to **"Sources"** or **"Data Sources"** tab
   - Click **"Add Source"** or **"Add Connector"**

2. **Select Connector Type:**
   - Choose **"REST API"** or **"HTTP API"**
   - Click **"Next"**

3. **Configure API Connection:**
   - **Name**: `Refund Estimation API`
   - **Base URL**: `https://famished-vertebrae-basil.ngrok-free.dev/api`
   - **Authentication**: Select **"None"** (or configure if you have auth)
   - **Headers**: (optional)
     ```json
     {
       "Content-Type": "application/json"
     }
     ```
   - Click **"Test Connection"**
   - Should show: ✅ Connection successful
   - Click **"Save"**

#### 3.2: Configure API Endpoints

**Note about Schema Mapping:**
- **If you created a schema**: Map each endpoint to corresponding entity (TravelBooking, RefundEstimate, etc.)
- **If you skipped schema**: Leave entity mapping blank - Context Studio will infer structure from API responses

Configure your 11 API endpoints:

**Endpoint 1: Get Bookings**
- **Method**: GET
- **Path**: `/bookings`
- **Maps to Entity**: `TravelBooking` (if using schema) or leave blank
- **Query Parameters**:
  - `skip` (integer, default: 0)
  - `limit` (integer, default: 100)
- **Response Type**: Array of TravelBooking
- Click **"Add Endpoint"**

**Endpoint 2: Create Booking**
- **Method**: POST
- **Path**: `/bookings`
- **Maps to Entity**: `TravelBooking`
- **Request Body**: BookingCreate schema
- **Response Type**: TravelBooking
- Click **"Add Endpoint"**

**Endpoint 3: Get Booking Details**
- **Method**: GET
- **Path**: `/bookings/{booking_id}`
- **Maps to Entity**: `TravelBooking`
- **Path Parameters**:
  - `booking_id` (integer, required)
- **Response Type**: TravelBooking
- Click **"Add Endpoint"**

**Endpoint 4: Estimate Refund**
- **Method**: POST
- **Path**: `/estimate-refund/{booking_id}`
- **Maps to Entity**: `RefundEstimate`
- **Path Parameters**:
  - `booking_id` (integer, required)
- **Request Body**:
  ```json
  {
    "selected_model": "auto",
    "severity": "high"
  }
  ```
- **Response Type**: RefundEstimate
- Click **"Add Endpoint"**

**Endpoint 5: Get Refund Estimates**
- **Method**: GET
- **Path**: `/estimates/{booking_id}`
- **Maps to Entity**: `RefundEstimate`
- **Path Parameters**:
  - `booking_id` (integer, required)
- **Response Type**: Array of RefundEstimate
- Click **"Add Endpoint"**

**Endpoint 6: Get Risk Events**
- **Method**: GET
- **Path**: `/risk-events`
- **Maps to Entity**: `RiskEvent`
- **Query Parameters**:
  - `active_only` (boolean, default: true)
- **Response Type**: Array of RiskEvent
- Click **"Add Endpoint"**

**Endpoint 7: Get Regional Risk**
- **Method**: GET
- **Path**: `/risk-events/region/{region}`
- **Maps to Entity**: `RiskEvent`
- **Path Parameters**:
  - `region` (string, required)
- **Response Type**: RegionalRiskResponse
- Click **"Add Endpoint"**

**Endpoint 8: Get Historical Refunds**
- **Method**: GET
- **Path**: `/historical-refunds`
- **Maps to Entity**: `HistoricalRefund`
- **Query Parameters**:
  - `component_type` (string, optional)
  - `event_type` (string, optional)
  - `limit` (integer, default: 100)
- **Response Type**: Array of HistoricalRefund
- Click **"Add Endpoint"**

**Endpoint 9: Get Refund Statistics**
- **Method**: GET
- **Path**: `/statistics/refund-rates`
- **Maps to Entity**: `RefundStatistics`
- **Response Type**: Array of RefundStatistics
- Click **"Add Endpoint"**

**Endpoint 10: Get Provider Policies**
- **Method**: GET
- **Path**: `/providers`
- **Maps to Entity**: `ProviderPolicy`
- **Query Parameters**:
  - `provider_type` (string, optional)
- **Response Type**: Array of ProviderPolicy
- Click **"Add Endpoint"**

**Endpoint 11: Get Provider Policy**
- **Method**: GET
- **Path**: `/providers/{provider_name}`
- **Maps to Entity**: `ProviderPolicy`
- **Path Parameters**:
  - `provider_name` (string, required)
- **Response Type**: ProviderPolicy
- Click **"Add Endpoint"**

#### 3.3: Validate Data Ingestion

1. **Test Each Endpoint:**
   - Click **"Test"** button for each endpoint
   - Verify data is returned correctly
   - Check data matches schema

2. **Ingest Sample Data:**
   - Click **"Ingest Data"** or **"Sync Now"**
   - Context Studio will fetch data from your API
   - Review ingested data
   - Verify entities are populated

3. **Set Refresh Schedule:**
   - **Refresh Mode**: Real-time or Scheduled
   - **Interval**: Every 5 minutes (or as needed)
   - Click **"Save"**

---

## STEP 4: Expose via MCP

### What is MCP Exposure?

MCP (Model Context Protocol) exposure makes your context available to:
- AI assistants (Claude, GPT, watsonx)
- External applications
- Other systems

### Configure MCP Server

#### 4.1: Enable MCP

1. **In Your Context:**
   - Go to **"MCP"** or **"Expose"** tab
   - Click **"Enable MCP"** or **"Create MCP Server"**

2. **Configure MCP Server:**
   - **Server Name**: `refund-estimation-mcp`
   - **Description**: `MCP server for travel refund estimation`
   - **Version**: `1.0.0`
   - **Protocol**: MCP 1.0
   - Click **"Create"**

#### 4.2: Define MCP Tools

Context Studio will automatically create MCP tools from your endpoints. Review and customize:

**Tool 1: create_booking**
- **Name**: `create_booking`
- **Description**: `Create a new travel booking with multiple components`
- **Input Schema**: From BookingCreate entity
- **Endpoint**: POST /bookings
- **Enabled**: ✅
- Click **"Save"**

**Tool 2: get_bookings**
- **Name**: `get_bookings`
- **Description**: `Retrieve all travel bookings with pagination`
- **Input Schema**: skip, limit parameters
- **Endpoint**: GET /bookings
- **Enabled**: ✅
- Click **"Save"**

**Tool 3: get_booking_details**
- **Name**: `get_booking_details`
- **Description**: `Get detailed information about a specific booking`
- **Input Schema**: booking_id parameter
- **Endpoint**: GET /bookings/{booking_id}
- **Enabled**: ✅
- Click **"Save"**

**Tool 4: estimate_refund**
- **Name**: `estimate_refund`
- **Description**: `Generate AI-powered refund estimate for a booking`
- **Input Schema**: booking_id, selected_model, severity
- **Endpoint**: POST /estimate-refund/{booking_id}
- **Enabled**: ✅
- Click **"Save"**

**Tool 5: get_refund_estimates**
- **Name**: `get_refund_estimates`
- **Description**: `Get all refund estimates for a booking`
- **Input Schema**: booking_id parameter
- **Endpoint**: GET /estimates/{booking_id}
- **Enabled**: ✅
- Click **"Save"**

**Tool 6: get_risk_events**
- **Name**: `get_risk_events`
- **Description**: `Get current global risk events`
- **Input Schema**: active_only parameter
- **Endpoint**: GET /risk-events
- **Enabled**: ✅
- Click **"Save"**

**Tool 7: get_regional_risk**
- **Name**: `get_regional_risk`
- **Description**: `Get risk assessment for a specific region`
- **Input Schema**: region parameter
- **Endpoint**: GET /risk-events/region/{region}
- **Enabled**: ✅
- Click **"Save"**

**Tool 8: get_historical_refunds**
- **Name**: `get_historical_refunds`
- **Description**: `Get historical refund data for analysis`
- **Input Schema**: component_type, event_type, limit
- **Endpoint**: GET /historical-refunds
- **Enabled**: ✅
- Click **"Save"**

**Tool 9: get_refund_statistics**
- **Name**: `get_refund_statistics`
- **Description**: `Get aggregated refund statistics`
- **Input Schema**: None
- **Endpoint**: GET /statistics/refund-rates
- **Enabled**: ✅
- Click **"Save"**

**Tool 10: get_provider_policies**
- **Name**: `get_provider_policies`
- **Description**: `Get refund policies for travel providers`
- **Input Schema**: provider_type parameter
- **Endpoint**: GET /providers
- **Enabled**: ✅
- Click **"Save"**

**Tool 11: get_provider_policy**
- **Name**: `get_provider_policy`
- **Description**: `Get detailed policy for a specific provider`
- **Input Schema**: provider_name parameter
- **Endpoint**: GET /providers/{provider_name}
- **Enabled**: ✅
- Click **"Save"**

#### 4.3: Get MCP Endpoint URL

1. **After enabling MCP:**
   - Context Studio will provide an MCP endpoint URL
   - Example: `https://mcp.context-studio.cloud.ibm.com/v1/contexts/your-context-id`
   - **Copy this URL** - you'll need it to connect AI agents

2. **Test MCP Endpoint:**
   - Click **"Test MCP"** button
   - Or use curl:
   ```bash
   curl -X POST https://mcp.context-studio.cloud.ibm.com/v1/contexts/your-context-id \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
   ```
   - Should return list of 11 tools

3. **Get API Key (if required):**
   - Go to **"Settings"** or **"API Keys"**
   - Click **"Generate API Key"**
   - Copy the key
   - Use in Authorization header: `Authorization: Bearer your-api-key`

---

## Test Your Integration

### Test in Context Studio

1. **Go to "Test" or "Playground" Section**

2. **Test Tool Calls:**

**Test 1: List Bookings**
```json
{
  "tool": "get_bookings",
  "arguments": {
    "skip": 0,
    "limit": 10
  }
}
```

**Test 2: Create Booking**
```json
{
  "tool": "create_booking",
  "arguments": {
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
      }
    ]
  }
}
```

**Test 3: Estimate Refund**
```json
{
  "tool": "estimate_refund",
  "arguments": {
    "booking_id": 1,
    "severity": "high"
  }
}
```

3. **Verify Responses:**
   - Check data is returned correctly
   - Verify schema validation
   - Review any errors

---

## Connect AI Assistant

### Option 1: Use watsonx Assistant

1. **In IBM Cloud:**
   - Go to watsonx Assistant service
   - Create new assistant: `Refund Estimation Assistant`

2. **Connect to Context Studio:**
   - In assistant settings, go to **"Integrations"**
   - Click **"Add Integration"**
   - Select **"Context Studio"** or **"MCP"**
   - Enter your MCP endpoint URL
   - Enter API key (if required)
   - Click **"Connect"**

3. **Enable Tools:**
   - Select all 11 tools
   - Click **"Enable"**

4. **Test:**
   - Open chat preview
   - Ask: "Show me all bookings"
   - Ask: "Create a booking for Tokyo"
   - Ask: "Estimate refund for booking 1"

### Option 2: Use Claude Desktop

1. **Configure Claude Desktop:**
   - Open: `C:\Users\AbhijitJoshi\AppData\Roaming\Claude\claude_desktop_config.json`
   - Add:
   ```json
   {
     "mcpServers": {
       "refund-estimation": {
         "url": "https://mcp.context-studio.cloud.ibm.com/v1/contexts/your-context-id",
         "type": "http",
         "headers": {
           "Authorization": "Bearer your-api-key"
         }
       }
     }
   }
   ```

2. **Restart Claude Desktop**

3. **Test:**
   - Ask Claude: "What tools do you have?"
   - Should list 11 refund estimation tools
   - Ask: "List all bookings"

### Option 3: Custom Integration

Use the MCP endpoint in your own application:

```python
import requests

MCP_URL = "https://mcp.context-studio.cloud.ibm.com/v1/contexts/your-context-id"
API_KEY = "your-api-key"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# List available tools
response = requests.post(
    MCP_URL,
    headers=headers,
    json={
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    }
)
print("Available tools:", response.json())

# Call a tool
response = requests.post(
    MCP_URL,
    headers=headers,
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
print("Bookings:", response.json())
```

---

## Generate Sample Data

If your database is empty, generate sample data:

**In Terminal 3** (keep backend and ngrok running):
```powershell
cd backend
python -c "from services.data_generator import generate_sample_data; generate_sample_data()"
```

**Output:**
```
Generating sample data...
Created 10 bookings
Created 15 risk events
Created 20 historical refunds
Created 8 provider policies
Sample data generation complete!
```

Now your API will return data when tools are called.

---

## Monitor and Maintain

### Monitor Usage

1. **In Context Studio:**
   - Go to **"Analytics"** or **"Monitoring"**
   - View metrics:
     - Tool invocations
     - Success/error rates
     - Response times
     - Data refresh status

2. **Check Logs:**
   - Go to **"Logs"** section
   - Filter by tool, time, status
   - Review errors and warnings

### Update Context

**When your API changes:**

1. **Update Schema:**
   - Edit schema to add new entities/properties
   - Save changes

2. **Update Endpoints:**
   - Add new endpoints in Sources
   - Update existing endpoint configurations
   - Test connections

3. **Update MCP Tools:**
   - Add new tools or update existing
   - Re-publish MCP server
   - Notify connected applications

### Refresh Data

1. **Manual Refresh:**
   - Go to Sources tab
   - Click **"Sync Now"** or **"Refresh"**

2. **Automatic Refresh:**
   - Configure refresh schedule
   - Set interval (e.g., every 5 minutes)
   - Enable real-time updates

---

## Production Deployment

### Move from Ngrok to Production

**Current (Development):**
- Backend: localhost:8000
- Public URL: ngrok (temporary)

**Production:**

1. **Deploy Backend to Cloud:**
   - IBM Cloud Code Engine
   - IBM Cloud Foundry
   - AWS, Azure, or GCP
   - Get permanent URL: `https://refund-api.yourdomain.com`

2. **Update Context Studio:**
   - Edit API connector
   - Change base URL to production URL
   - Test connection
   - Save changes

3. **Update MCP:**
   - MCP endpoint automatically uses new URL
   - No changes needed for connected applications

### Add Security

1. **Enable Authentication:**
   - Add API key to your backend
   - Update Context Studio connector:
     - Add header: `X-API-Key: your-key`
   - Test connection

2. **Configure CORS:**
   - Allow Context Studio domain
   - Configure in backend

3. **Enable HTTPS:**
   - Use SSL/TLS certificate
   - Ensure all connections are secure

---

## Troubleshooting

### Issue 1: Schema Upload Fails

**Solutions:**
1. Verify YAML syntax is correct
2. Check file size (< 10MB)
3. Try manual schema creation
4. Contact IBM support

### Issue 2: API Connection Test Fails

**Solutions:**
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check ngrok is active: `curl https://your-ngrok-url/api/health`
3. Verify URL in connector matches ngrok URL
4. Check firewall/network settings
5. Review CORS configuration

### Issue 3: No Data Ingested

**Solutions:**
1. Generate sample data (see above)
2. Check API returns data: `curl https://your-ngrok-url/api/bookings`
3. Click "Sync Now" in Sources tab
4. Review ingestion logs for errors

### Issue 4: MCP Tools Not Working

**Solutions:**
1. Verify all 11 tools are enabled
2. Test each tool individually
3. Check MCP endpoint URL is correct
4. Verify API key (if required)
5. Review tool input schemas

### Issue 5: Ngrok URL Changed

**Solutions:**
1. Get new ngrok URL from terminal
2. Update API connector base URL
3. Test connection
4. Re-sync data
5. Or use ngrok with fixed domain (paid)

---

## Quick Reference

### IBM Context Studio 4-Step Workflow

1. ✅ **Schema** → Define domain structure (OPTIONAL - can skip)
2. ✅ **Context** → Create container for data
3. ✅ **Sources** → Connect to your API
4. ✅ **MCP** → Expose to AI applications

### Two Approaches:

**Approach 1: With Schema (Recommended)**
- More structured and validated
- Better AI understanding
- Upload `context_schema.yaml`
- Map endpoints to entities

**Approach 2: Without Schema (Faster)**
- Quick setup
- Skip Step 1
- Structure inferred from API
- More flexible

### Essential URLs

- **Context Studio**: https://context-studio.cloud.ibm.com
- **Your Backend**: http://localhost:8000
- **Your Ngrok**: https://famished-vertebrae-basil.ngrok-free.dev
- **API Docs**: http://localhost:8000/api/docs

### Essential Commands

**Start Backend:**
```powershell
cd backend
python main.py
```

**Start Ngrok:**
```powershell
cd backend
ngrok http 8000
```

**Generate Sample Data:**
```powershell
cd backend
python -c "from services.data_generator import generate_sample_data; generate_sample_data()"
```

**Test API:**
```powershell
curl http://localhost:8000/api/health
curl https://your-ngrok-url.ngrok-free.dev/api/health
```

### Integration Checklist

- [ ] Backend running on port 8000
- [ ] Ngrok tunnel active
- [ ] **Choose approach**: With schema OR without schema
- [ ] Schema uploaded to Context Studio (if using schema approach)
- [ ] Context created
- [ ] API connector added
- [ ] All 11 endpoints configured
- [ ] Endpoints mapped to entities (if using schema)
- [ ] Data ingested successfully
- [ ] MCP server enabled
- [ ] 11 tools created and enabled
- [ ] MCP endpoint tested
- [ ] AI assistant connected
- [ ] End-to-end test completed

---

## Summary

You have successfully integrated your Travel Refund Uncertainty Estimation System with IBM Context Studio! 🎉

**What You've Accomplished:**

1. ✅ **Schema**: Uploaded domain structure (context_schema.yaml) OR skipped for quick setup
2. ✅ **Context**: Created context space for refund estimation
3. ✅ **Sources**: Connected your FastAPI backend with 11 endpoints
4. ✅ **MCP**: Exposed 11 tools via MCP protocol

**Two Integration Paths:**

**Path 1: With Schema (Recommended)**
- ✅ Uploaded `context_schema.yaml`
- ✅ Structured entities and relationships
- ✅ Better validation and AI understanding
- ✅ Mapped endpoints to schema entities

**Path 2: Without Schema (Quick)**
- ✅ Skipped schema creation
- ✅ Faster setup
- ✅ Structure inferred from API responses
- ✅ More flexible but less validated

**Your System Can Now:**
- Accept natural language requests via AI assistants
- Create and manage travel bookings
- Estimate refunds with AI/ML models
- Check global risk events
- Analyze regional safety
- Review provider policies
- Access historical data
- Provide statistics and insights

**Next Steps:**
- Test all 11 tools in Context Studio
- Connect watsonx Assistant or Claude
- Deploy to production with permanent URL
- Monitor usage and improve
- Collect user feedback

---

**Created**: 2026-05-21  
**Version**: 2.0 (Updated for Context Studio 4-step workflow)  
**Author**: Bob  
**For**: Abhijit Joshi - Uncertainty_Refund Project