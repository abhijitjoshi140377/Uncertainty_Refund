# IBM Context Studio - Simplified Integration Guide
## Travel Refund Uncertainty Estimation System

**Based on actual IBM Context Studio interface**

---

## Prerequisites ✅

1. ✅ **Backend API Running**
   - Terminal 1: `cd backend && python main.py`
   - Running on: http://localhost:8000

2. ✅ **Ngrok Tunnel Active**
   - Terminal 2: `cd backend && ngrok http 8000`
   - Public URL: https://famished-vertebrae-basil.ngrok-free.dev

3. ✅ **IBM Cloud Account**
   - Access to: https://context-studio.cloud.ibm.com

---

## Simplified 3-Step Process

### STEP 1: Create Context (Skip Schema)

**What to Do:**

1. **Go to Context Studio**: https://context-studio.cloud.ibm.com

2. **Create New Context:**
   - Click **"Create Context"** or **"New Context"**
   - **Name**: `Refund Estimation Context`
   - **Description**: `AI-powered travel refund estimation with real-time risk assessment`
   - Click **"Create"**

3. **Skip Schema Builder:**
   - If you see Schema Builder interface (Add Node, Add Rule, etc.)
   - **Don't add anything manually**
   - Look for **"Skip"**, **"Next"**, or **"Continue"** button
   - Or simply close/minimize the Schema Builder panel
   - Proceed to add data sources

**Why Skip Schema?**
- ✅ Your API is self-documenting (FastAPI/Swagger)
- ✅ Context Studio will infer structure from API responses
- ✅ Faster setup
- ✅ Less manual work

---

### STEP 2: Add Your API as Data Source

**What to Do:**

1. **In Your Context, Go to "Sources" or "Data Sources" Tab**

2. **Add API Connector:**
   - Click **"Add Source"** or **"Add Connector"**
   - Select **"REST API"** or **"HTTP API"**
   - Click **"Next"**

3. **Configure API Connection:**
   - **Name**: `Refund Estimation API`
   - **Base URL**: `https://famished-vertebrae-basil.ngrok-free.dev/api`
   - **Authentication**: None (or select "No Authentication")
   - **Headers** (optional):
     ```json
     {
       "Content-Type": "application/json"
     }
     ```
   - Click **"Test Connection"**
   - Should show: ✅ Connection successful
   - Click **"Save"** or **"Add"**

4. **Add Your 11 Endpoints:**

For each endpoint, click **"Add Endpoint"** and configure:

**Endpoint 1: Get Bookings**
- **Name**: `get_bookings`
- **Method**: GET
- **Path**: `/bookings`
- **Query Parameters**:
  - `skip` (integer, default: 0)
  - `limit` (integer, default: 100)
- Click **"Save"**

**Endpoint 2: Create Booking**
- **Name**: `create_booking`
- **Method**: POST
- **Path**: `/bookings`
- **Request Body**: JSON (Context Studio may auto-detect from API)
- Click **"Save"**

**Endpoint 3: Get Booking Details**
- **Name**: `get_booking_details`
- **Method**: GET
- **Path**: `/bookings/{booking_id}`
- **Path Parameters**:
  - `booking_id` (integer, required)
- Click **"Save"**

**Endpoint 4: Estimate Refund**
- **Name**: `estimate_refund`
- **Method**: POST
- **Path**: `/estimate-refund/{booking_id}`
- **Path Parameters**:
  - `booking_id` (integer, required)
- **Request Body**: JSON
- Click **"Save"**

**Endpoint 5: Get Refund Estimates**
- **Name**: `get_refund_estimates`
- **Method**: GET
- **Path**: `/estimates/{booking_id}`
- **Path Parameters**:
  - `booking_id` (integer, required)
- Click **"Save"**

**Endpoint 6: Get Risk Events**
- **Name**: `get_risk_events`
- **Method**: GET
- **Path**: `/risk-events`
- **Query Parameters**:
  - `active_only` (boolean, default: true)
- Click **"Save"**

**Endpoint 7: Get Regional Risk**
- **Name**: `get_regional_risk`
- **Method**: GET
- **Path**: `/risk-events/region/{region}`
- **Path Parameters**:
  - `region` (string, required)
- Click **"Save"**

**Endpoint 8: Get Historical Refunds**
- **Name**: `get_historical_refunds`
- **Method**: GET
- **Path**: `/historical-refunds`
- **Query Parameters**:
  - `component_type` (string, optional)
  - `event_type` (string, optional)
  - `limit` (integer, default: 100)
- Click **"Save"**

**Endpoint 9: Get Refund Statistics**
- **Name**: `get_refund_statistics`
- **Method**: GET
- **Path**: `/statistics/refund-rates`
- Click **"Save"**

**Endpoint 10: Get Provider Policies**
- **Name**: `get_provider_policies`
- **Method**: GET
- **Path**: `/providers`
- **Query Parameters**:
  - `provider_type` (string, optional)
- Click **"Save"**

**Endpoint 11: Get Provider Policy**
- **Name**: `get_provider_policy`
- **Method**: GET
- **Path**: `/providers/{provider_name}`
- **Path Parameters**:
  - `provider_name` (string, required)
- Click **"Save"**

5. **Test Endpoints:**
   - Click **"Test"** button for each endpoint
   - Verify data is returned correctly
   - Fix any errors

6. **Sync/Ingest Data:**
   - Click **"Sync Now"** or **"Ingest Data"**
   - Context Studio will fetch data from your API
   - Wait for sync to complete

---

### STEP 3: Expose via MCP

**What to Do:**

1. **Go to "MCP" or "Expose" Tab in Your Context**

2. **Enable MCP:**
   - Click **"Enable MCP"** or **"Create MCP Server"**
   - **Server Name**: `refund-estimation-mcp`
   - **Description**: `MCP server for travel refund estimation`
   - Click **"Create"** or **"Enable"**

3. **Review MCP Tools:**
   - Context Studio will automatically create MCP tools from your 11 endpoints
   - Review the list - should show 11 tools
   - Verify each tool has correct name and description
   - All tools should be **"Enabled"**

4. **Get MCP Endpoint URL:**
   - Context Studio will provide an MCP endpoint URL
   - Example: `https://mcp.context-studio.cloud.ibm.com/v1/contexts/your-context-id`
   - **Copy this URL** - you'll need it to connect AI agents

5. **Get API Key (if required):**
   - Look for **"API Keys"** or **"Settings"** section
   - Click **"Generate API Key"**
   - Copy the key
   - You'll use this in Authorization header

6. **Test MCP Endpoint:**
   - Click **"Test"** button
   - Or use curl:
   ```bash
   curl -X POST https://mcp.context-studio.cloud.ibm.com/v1/contexts/your-context-id \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-api-key" \
     -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
   ```
   - Should return list of 11 tools

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

3. **Test:**
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

---

## Generate Sample Data (If Needed)

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

## Troubleshooting

### Issue 1: Can't Skip Schema Builder

**Solution:**
- Look for "Next", "Continue", or "Skip" button
- Or close the Schema Builder panel
- Or create minimal schema with 1-2 nodes and proceed
- Schema is not required for API-based contexts

### Issue 2: API Connection Test Fails

**Solutions:**
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check ngrok is active: `curl https://your-ngrok-url/api/health`
3. Verify URL in connector matches ngrok URL exactly
4. Check firewall/network settings

### Issue 3: Endpoints Not Working

**Solutions:**
1. Test each endpoint directly with curl first
2. Verify path is correct (starts with `/` not `api/`)
3. Check parameter types match API expectations
4. Review Context Studio logs for errors

### Issue 4: MCP Tools Not Created

**Solutions:**
1. Verify all 11 endpoints are added and saved
2. Check endpoints are enabled
3. Try "Refresh" or "Sync" in MCP section
4. Re-enable MCP if needed

### Issue 5: Ngrok URL Changed

**Solutions:**
1. Get new ngrok URL from terminal
2. Update API connector base URL in Context Studio
3. Test connection again
4. Re-sync data
5. Or use ngrok with fixed domain (paid feature)

---

## Quick Reference

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
- [ ] Context created in Context Studio
- [ ] API connector added with correct base URL
- [ ] All 11 endpoints configured
- [ ] Connection tested successfully
- [ ] Data synced/ingested
- [ ] MCP enabled
- [ ] 11 MCP tools created
- [ ] MCP endpoint URL obtained
- [ ] API key generated (if required)
- [ ] AI assistant connected
- [ ] End-to-end test completed

---

## Summary

**Simplified 3-Step Process:**

1. ✅ **Create Context** (skip schema builder)
2. ✅ **Add API Source** (configure 11 endpoints)
3. ✅ **Enable MCP** (get endpoint URL)

**Key Points:**
- ✅ Schema is optional - skip it for faster setup
- ✅ Context Studio infers structure from API responses
- ✅ 11 endpoints = 11 MCP tools automatically
- ✅ Connect AI assistant using MCP endpoint URL
- ✅ Test with natural language queries

**You're ready to integrate with IBM Context Studio!** 🎉

---

**Created**: 2026-05-21  
**Version**: 1.0 (Simplified based on actual interface)  
**Author**: Bob  
**For**: Abhijit Joshi - Uncertainty_Refund Project