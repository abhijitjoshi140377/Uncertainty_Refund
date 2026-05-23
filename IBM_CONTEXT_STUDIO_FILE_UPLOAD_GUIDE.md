# IBM Context Studio - File Upload Guide
## Travel Refund Uncertainty Estimation System

**Based on actual IBM Context Studio interface - File Upload Method**

---

## What You Discovered ✅

IBM Context Studio's "Sources & Data" tab expects you to **upload data files** (JSON, CSV, etc.) rather than configure API endpoints directly.

Your screenshot shows:
- **"No data sources found"**
- **"Upload Files"** button
- **Data Files** section for uploading documents

---

## Step-by-Step File Upload Process

### STEP 1: Upload Sample Data Files

I've created 3 sample data files for you to upload:

#### File 1: Bookings Data
**File**: `sample_bookings_data.json`
- Contains 5 sample travel bookings
- Includes customer info, travel dates, destinations
- Has booking components (flights, hotels, visas)

#### File 2: Risk Events Data
**File**: `sample_risk_events_data.json`
- Contains 5 global risk events
- Includes natural disasters, political unrest, war
- Shows severity levels and affected regions

#### File 3: Refund Estimates Data
**File**: `sample_refund_estimates_data.json`
- Contains 3 refund estimates
- Includes confidence intervals, risk scores
- Shows best/worst case scenarios

---

### STEP 2: Upload Files to Context Studio

1. **In Context Studio, go to your context**: "Refund Estimation Context"

2. **Click on "Sources & Data" tab**

3. **Click "Upload Files" button** (shown in your screenshot)

4. **Upload First File**:
   - Click "Choose File" or drag and drop
   - Select: `sample_bookings_data.json`
   - **Category**: Select "Bookings" or "Travel Data"
   - **Type**: JSON
   - Click "Upload"

5. **Upload Second File**:
   - Click "Upload Files" again
   - Select: `sample_risk_events_data.json`
   - **Category**: Select "Risk Events" or "Events"
   - **Type**: JSON
   - Click "Upload"

6. **Upload Third File**:
   - Click "Upload Files" again
   - Select: `sample_refund_estimates_data.json`
   - **Category**: Select "Estimates" or "Predictions"
   - **Type**: JSON
   - Click "Upload"

7. **Wait for Processing**:
   - Context Studio will process the files
   - Check "Sync Status" column
   - Should show "Completed" or "Success"

---

### STEP 3: Verify Data Ingestion

1. **Check "Sources & Data" tab**:
   - Should now show 3 data files
   - Each with "Sync Status": Completed

2. **Go to "Knowledge Graph" tab**:
   - Should show entities extracted from your data
   - Nodes for: Bookings, Risk Events, Estimates
   - Relationships between entities

3. **Review Data**:
   - Click on each file to view contents
   - Verify data was parsed correctly
   - Check for any errors

---

### STEP 4: Expose via MCP

1. **Go to "MCP" or "Expose" tab**

2. **Enable MCP**:
   - Click "Enable MCP" or "Create MCP Server"
   - **Server Name**: `refund-estimation-mcp`
   - Click "Create"

3. **MCP Tools Auto-Generated**:
   - Context Studio will create tools based on your data
   - Tools for querying bookings, risk events, estimates
   - May include:
     - `get_bookings` - Query booking data
     - `get_risk_events` - Query risk events
     - `get_estimates` - Query refund estimates
     - `search_context` - General search across all data

4. **Get MCP Endpoint URL**:
   - Copy the MCP endpoint URL provided
   - Example: `https://mcp.context-studio.cloud.ibm.com/v1/contexts/your-context-id`

5. **Get API Key** (if required):
   - Go to Settings or API Keys
   - Generate new API key
   - Copy and save it

---

### STEP 5: Connect AI Assistant

#### Option 1: watsonx Assistant

1. In IBM Cloud, go to watsonx Assistant
2. Create assistant: "Refund Estimation Assistant"
3. Add Context Studio integration
4. Enter MCP endpoint URL
5. Enter API key
6. Test with queries:
   - "Show me all bookings"
   - "What risk events are active?"
   - "Show refund estimates"

#### Option 2: Claude Desktop

1. Configure `claude_desktop_config.json`:
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

2. Restart Claude Desktop
3. Test: "What tools do you have?"

---

## Alternative: Connect Your Live API

If you want to connect your live API instead of uploading static files:

### Option A: API Connector (if available)

1. Look for "Add Connector" or "Add API Source" button
2. If available, configure:
   - Base URL: `https://famished-vertebrae-basil.ngrok-free.dev/api`
   - Add endpoints
   - Test connection

### Option B: Webhook/Integration

1. Look for "Integrations" or "Webhooks" section
2. Configure webhook to your API
3. Set up real-time data sync

### Option C: Export Data from Your API

1. **Get data from your running API**:
```powershell
# Get bookings
curl https://famished-vertebrae-basil.ngrok-free.dev/api/bookings > live_bookings.json

# Get risk events
curl https://famished-vertebrae-basil.ngrok-free.dev/api/risk-events > live_risk_events.json

# Get statistics
curl https://famished-vertebrae-basil.ngrok-free.dev/api/statistics/refund-rates > live_statistics.json
```

2. **Upload these live data files** to Context Studio
3. **Set up periodic refresh** (if available)

---

## Troubleshooting

### Issue 1: File Upload Fails

**Solutions:**
- Check file size (< 10MB recommended)
- Verify JSON is valid (use jsonlint.com)
- Try uploading one file at a time
- Check file encoding (UTF-8)

### Issue 2: Data Not Parsed Correctly

**Solutions:**
- Review file structure
- Ensure consistent field names
- Check data types match expectations
- Look for parsing errors in logs

### Issue 3: No MCP Tools Created

**Solutions:**
- Verify files uploaded successfully
- Check "Sync Status" is "Completed"
- Try refreshing the page
- Re-enable MCP if needed

### Issue 4: Can't Find API Connector Option

**Solution:**
- Context Studio may be file-based only
- Use file upload method instead
- Export data from your API periodically
- Upload updated files to keep data fresh

---

## Summary

### What You Need to Do:

1. ✅ **Upload 3 sample data files** I created for you:
   - `sample_bookings_data.json`
   - `sample_risk_events_data.json`
   - `sample_refund_estimates_data.json`

2. ✅ **Wait for processing** to complete

3. ✅ **Enable MCP** to expose data as tools

4. ✅ **Connect AI assistant** using MCP endpoint

5. ✅ **Test** with natural language queries

### Files Ready to Upload:

✅ **`sample_bookings_data.json`** - 5 travel bookings  
✅ **`sample_risk_events_data.json`** - 5 risk events  
✅ **`sample_refund_estimates_data.json`** - 3 refund estimates  

### Next Steps:

1. Go to Context Studio
2. Open "Refund Estimation Context"
3. Click "Sources & Data" tab
4. Click "Upload Files"
5. Upload all 3 files
6. Enable MCP
7. Connect AI assistant

**You're ready to upload and integrate!** 🎉

---

**Created**: 2026-05-21  
**Version**: 1.0 (File Upload Method)  
**Author**: Bob  
**For**: Abhijit Joshi - Uncertainty_Refund Project