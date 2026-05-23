# Final Steps: Import to ICA and Test MCP Tools

## Current Status ✅

You have successfully:
- ✅ Created 11 MCP tools
- ✅ Started backend (running on localhost:8000)
- ✅ Started ngrok (tunneling to backend)
- ✅ Updated bulk import file with ngrok URLs
- ✅ Verified backend and ngrok are working

---

## What to Do Next (3 Steps)

### Step 1: Import to ICA Context Forge

**1.1 Open ICA Context Forge**
- Go to your IBM ICA Context Forge workspace
- URL should be something like: `https://dataplatform.cloud.ibm.com/` or your ICA URL

**1.2 Navigate to Import**
- Look for **"Import"** button or menu
- Select **"Bulk Import"** or **"Import Tools"**

**1.3 Upload File**
- Click **"Choose File"** or **"Upload"**
- Select: `refund-api-bulk-import-ngrok.json`
- Click **"Import"** or **"Upload"**

**1.4 Wait for Import**
- ICA will process the file
- Should show: "Successfully imported 11 tools" or similar message
- May take 30-60 seconds

**1.5 Verify Import**
- Go to **"Tools"** or **"MCP Tools"** section
- You should see 11 tools with "v2-" prefix:
  - v2-create-booking
  - v2-get-bookings
  - v2-get-booking-details
  - v2-estimate-refund
  - v2-get-refund-estimates
  - v2-get-risk-events
  - v2-get-regional-risk
  - v2-get-historical-refunds
  - v2-get-refund-statistics
  - v2-get-provider-policies
  - v2-get-provider-policy

---

### Step 2: Deploy/Activate MCP Server in ICA

After importing tools, you need to deploy/activate them:

**2.1 Look for Deployment Section**
- In ICA, look for:
  - **"Deploy"** button
  - **"Activate"** button
  - **"Publish"** button
  - **"MCP Server"** section
  - **"Settings"** or **"Configuration"**

**2.2 Deploy MCP Server**
- Click the deploy/activate button
- ICA will create an MCP server endpoint
- Wait for deployment to complete (may take 1-2 minutes)

**2.3 Get MCP Endpoint URL**
- After deployment, ICA should show an **MCP Endpoint URL**
- Should look like:
  - `https://mcp.cloud.ibm.com/your-workspace/refund-estimation`
  - Or similar IBM Cloud URL
- **Copy this URL** - you'll need it to connect AI agents

---

### Step 3: Test Your MCP Tools

Now you can test your MCP tools in several ways:

---

## Testing Method 1: Test in ICA Interface (If Available)

Some ICA versions have a built-in testing interface:

**Look for:**
- **"Test"** button next to each tool
- **"Try It"** or **"Execute"** option
- **"Playground"** or **"Testing"** section

**If you find it:**
1. Click on a tool (e.g., v2-get-bookings)
2. Click "Test" or "Try It"
3. Enter parameters (or leave empty for defaults)
4. Click "Execute" or "Run"
5. Should see response from your backend

**If you DON'T find it:**
- This is normal - many ICA versions don't have UI testing
- Use Method 2 or 3 below instead

---

## Testing Method 2: Test MCP Protocol with curl

If ICA gave you an MCP endpoint URL, test it directly:

**Test 1: List Available Tools**
```bash
curl -X POST https://YOUR-ICA-MCP-ENDPOINT-URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "v2-create-booking",
        "description": "Create a new travel booking...",
        "inputSchema": {...}
      },
      ...
    ]
  },
  "id": 1
}
```

**Test 2: Call a Tool (Get Bookings)**
```bash
curl -X POST https://YOUR-ICA-MCP-ENDPOINT-URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "v2-get-bookings",
      "arguments": {
        "skip": 0,
        "limit": 10
      }
    },
    "id": 2
  }'
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[]"
      }
    ]
  },
  "id": 2
}
```

---

## Testing Method 3: Connect AI Agent (Best Test)

The ultimate test is connecting an AI agent to use your tools.

### Option A: Claude Desktop

**1. Open Claude Desktop Settings**
- Click Settings icon
- Go to **Developer** → **MCP Servers**

**2. Add Your MCP Server**
```json
{
  "refund-estimation": {
    "url": "https://YOUR-ICA-MCP-ENDPOINT-URL",
    "type": "http"
  }
}
```

**3. Restart Claude Desktop**

**4. Test with Claude**
Ask Claude:
- "What tools do you have available?"
- "List all bookings"
- "Create a test booking for a trip to Paris"
- "Estimate refund for booking 1"

Claude should be able to use your 11 tools!

### Option B: Custom AI Agent (Python)

```python
import requests

# Your ICA MCP endpoint
mcp_url = "https://YOUR-ICA-MCP-ENDPOINT-URL"

# List available tools
response = requests.post(mcp_url, json={
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
})

tools = response.json()["result"]["tools"]
print(f"Available tools: {len(tools)}")
for tool in tools:
    print(f"  - {tool['name']}: {tool['description']}")

# Call a tool
response = requests.post(mcp_url, json={
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "v2-get-bookings",
        "arguments": {"skip": 0, "limit": 10}
    },
    "id": 2
})

result = response.json()["result"]
print(f"\nBookings: {result}")
```

---

## Testing Method 4: Test Backend Directly (Simplest)

Since your MCP tools just call your backend API, you can test the backend directly:

**Test with Browser:**
1. `https://famished-vertebrae-basil.ngrok-free.dev/api/health` ✅ (Already works!)
2. `https://famished-vertebrae-basil.ngrok-free.dev/api/bookings`
3. `https://famished-vertebrae-basil.ngrok-free.dev/api/risk-events`
4. `https://famished-vertebrae-basil.ngrok-free.dev/api/providers`

**If these work, your MCP tools will work!**

---

## Generate Sample Data (If Needed)

If your tests return empty arrays `[]`, generate sample data:

**Open a NEW terminal:**
```powershell
cd C:\Users\AbhijitJoshi\Uncertainty_Refund\backend
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

**Now test again** - should return data instead of empty arrays.

---

## What Success Looks Like

### ✅ Successful Import to ICA:
- 11 tools visible in ICA Tools section
- All tools show "Active" or "Ready" status
- Each tool shows ngrok URL (not localhost)

### ✅ Successful Deployment:
- ICA shows "Deployed" or "Running" status
- MCP endpoint URL is provided
- No error messages

### ✅ Successful Testing:
- curl commands return JSON responses
- AI agent can discover tools
- AI agent can call tools successfully
- Backend logs show incoming requests

---

## Troubleshooting

### Issue 1: Import Fails
**Error:** "Failed to import tools"  
**Solution:**
- Check file is `refund-api-bulk-import-ngrok.json` (not v2 version)
- Verify file has ngrok URLs (not localhost)
- Try importing one tool at a time

### Issue 2: Tools Show localhost URLs
**Error:** Tools still use `http://localhost:8000`  
**Solution:**
- You imported wrong file
- Delete tools and import `refund-api-bulk-import-ngrok.json`

### Issue 3: MCP Endpoint Not Working
**Error:** curl returns error or timeout  
**Solution:**
- Verify backend is still running (Terminal 1)
- Verify ngrok is still running (Terminal 2)
- Test ngrok URL in browser first
- Check ICA deployment status

### Issue 4: Tools Return Empty Data
**Error:** Tools work but return `[]`  
**Solution:**
- Generate sample data (see above)
- Test backend directly to verify data exists

### Issue 5: ngrok URL Changed
**Error:** Tools stop working after restart  
**Solution:**
- Get new ngrok URL
- Run: `python update_urls_for_ngrok.py <new-url>`
- Re-import to ICA

---

## Keep These Running

While using ICA and testing:

**Terminal 1: Backend**
```powershell
cd backend
python main.py
```
Status: ✅ Running (Keep open!)

**Terminal 2: ngrok**
```powershell
ngrok http 8000
```
Status: ✅ Running (Keep open!)

**Both must stay open for MCP tools to work!**

---

## Summary

### What You Need to Do:

1. **Import to ICA**
   - Upload `refund-api-bulk-import-ngrok.json`
   - Wait for import to complete
   - Verify 11 tools appear

2. **Deploy MCP Server**
   - Click Deploy/Activate in ICA
   - Get MCP endpoint URL
   - Wait for deployment

3. **Test Your Tools**
   - Method 1: ICA UI (if available)
   - Method 2: curl with MCP protocol
   - Method 3: Connect AI agent (best)
   - Method 4: Test backend directly (simplest)

4. **Generate Sample Data** (if needed)
   - Run data generator script
   - Verify data appears in tests

### Success Criteria:

✅ 11 tools imported to ICA  
✅ MCP server deployed  
✅ MCP endpoint URL obtained  
✅ Tools can be called successfully  
✅ Backend responds through ngrok  
✅ AI agent can use tools  

---

## Next Steps After Testing

Once your MCP tools are working:

1. **Use with AI Agents**
   - Connect Claude, GPT, or custom agents
   - Let AI handle customer refund requests
   - AI will use your 11 tools automatically

2. **Monitor Usage**
   - Check ICA logs/monitoring
   - Track tool invocations
   - Monitor backend performance

3. **Deploy to Production** (Optional)
   - Deploy backend to cloud (Heroku, AWS, etc.)
   - Get permanent URL (no ngrok needed)
   - Update bulk import with production URL
   - Re-import to ICA

4. **Add More Tools** (Optional)
   - Use `ICA_ADD_NEW_TOOL_GUIDE.md`
   - Add new endpoints as needed
   - Import individually or in bulk

---

**You're ready to import and test! Follow the steps above and your MCP tools will be working!** 🚀

**Last Updated**: 2026-05-20  
**Status**: Ready to import to ICA  
**Next**: Import `refund-api-bulk-import-ngrok.json` to ICA Context Forge