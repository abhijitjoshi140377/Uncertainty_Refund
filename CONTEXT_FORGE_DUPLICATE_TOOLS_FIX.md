# Context Forge: Fixing "Failed Tools - APIs Already Present" Error

## Problem
When importing `refund-api-bulk-import.json`, you see:
```
Failed Tools (11)
Reason: APIs are already present
```

This means tools with the same names already exist in your Context Forge workspace.

---

## Solution Options

### Option 1: Delete Existing Tools (Recommended)

**Step 1: View Existing Tools**
1. In IBM Context Forge, go to **Tools** or **MCP Tools** section
2. You should see 11 existing tools with these names:
   - create-booking
   - get-bookings
   - get-booking-details
   - estimate-refund
   - get-refund-estimates
   - get-risk-events
   - get-regional-risk
   - get-historical-refunds
   - get-refund-statistics
   - get-provider-policies
   - get-provider-policy

**Step 2: Delete All Existing Tools**
1. Select all 11 tools (use checkbox or Ctrl+Click)
2. Click **Delete** or **Remove** button
3. Confirm deletion
4. Wait for deletion to complete

**Step 3: Re-import Bulk File**
1. Click **Import** → **Bulk Import**
2. Upload `refund-api-bulk-import.json`
3. All 11 tools should import successfully now

---

### Option 2: Update Existing Tools

If you want to keep existing tools but update their configurations:

**Step 1: Use Update/Replace Mode**
1. In Context Forge import dialog, look for options like:
   - "Replace existing tools"
   - "Update if exists"
   - "Overwrite duplicates"
2. Enable this option
3. Import the bulk file again

**Step 2: Manual Update (if no replace option)**
1. Click on each existing tool
2. Click **Edit** or **Update**
3. Copy configuration from `refund-api-bulk-import.json`
4. Paste and save
5. Repeat for all 11 tools

---

### Option 3: Rename Tools in Bulk Import File

If you want to keep both old and new versions:

**Step 1: Modify Tool Names**
1. Open `refund-api-bulk-import.json`
2. Add prefix to all tool names:

```json
{
  "name": "v2-create-booking",  // Changed from "create-booking"
  "displayName": "Create Travel Booking (v2)",
  ...
}
```

**Step 2: Update All 11 Tool Names**
Add "v2-" prefix to these names:
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

**Step 3: Save and Re-import**
1. Save modified `refund-api-bulk-import.json`
2. Import the file
3. You'll now have both old and new versions

---

### Option 4: Create New Workspace/Project

If you want a clean start:

**Step 1: Create New Workspace**
1. In Context Forge, click **Workspaces** or **Projects**
2. Click **Create New Workspace**
3. Name it: "Refund Estimation MCP"
4. Save

**Step 2: Switch to New Workspace**
1. Select the new workspace
2. Verify it's empty (no existing tools)

**Step 3: Import Bulk File**
1. Click **Import** → **Bulk Import**
2. Upload `refund-api-bulk-import.json`
3. All 11 tools should import successfully

---

## Quick Fix Script (Option 1 - Automated)

If Context Forge has an API, you can automate deletion:

```python
import requests
import json

# Context Forge API configuration
API_URL = "https://api.dataplatform.cloud.ibm.com/v2/context-forge"
API_KEY = "YOUR_IBM_CLOUD_API_KEY"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Tool names to delete
tool_names = [
    "create-booking",
    "get-bookings",
    "get-booking-details",
    "estimate-refund",
    "get-refund-estimates",
    "get-risk-events",
    "get-regional-risk",
    "get-historical-refunds",
    "get-refund-statistics",
    "get-provider-policies",
    "get-provider-policy"
]

# Delete each tool
for tool_name in tool_names:
    delete_url = f"{API_URL}/tools/{tool_name}"
    response = requests.delete(delete_url, headers=headers)
    print(f"Deleted {tool_name}: {response.status_code}")

print("\nAll tools deleted. Now import the bulk file.")
```

---

## Verification Steps

After successfully importing:

**Step 1: Check Tool Count**
- Go to Tools section
- Verify you see exactly 11 tools
- All should have status "Active" or "Ready"

**Step 2: Test One Tool**
1. Select "get-bookings" tool
2. Click **Test** or **Try it**
3. Leave parameters empty (uses defaults)
4. Click **Execute**
5. Should return: `{"status": "error", "message": "Backend not running"}`
   - This is expected if backend isn't running
   - Confirms tool is configured correctly

**Step 3: Start Backend and Test Again**
```bash
cd backend
python main.py
```

Then test "get-bookings" again:
- Should return: `[]` (empty array) or list of bookings
- Confirms end-to-end connection works

---

## Common Issues After Import

### Issue 1: Tools Import But Don't Work
**Symptom**: Tools show as "Active" but fail when executed  
**Cause**: Backend API not running  
**Solution**:
```bash
cd backend
python main.py
# Verify: curl http://localhost:8000/api/health
```

### Issue 2: Some Tools Work, Others Don't
**Symptom**: Only some of the 11 tools execute successfully  
**Cause**: URL mismatch or backend routes missing  
**Solution**:
1. Check which tools fail
2. Verify those endpoints exist in `backend/main.py`
3. Test directly: `curl http://localhost:8000/api/bookings`

### Issue 3: Tools Import But Show Wrong Data
**Symptom**: Tools execute but return unexpected results  
**Cause**: Database not initialized or empty  
**Solution**:
```bash
cd backend
python -c "from services.data_generator import generate_sample_data; generate_sample_data()"
```

### Issue 4: Authentication Errors When Testing
**Symptom**: "401 Unauthorized" when testing tools  
**Cause**: Context Forge trying to authenticate with backend  
**Solution**:
- Our API has `auth_type: "none"` in bulk import
- Verify backend doesn't require authentication
- Check `backend/main.py` has no auth middleware

---

## Best Practice: Version Control Your Tools

To avoid this issue in the future:

**Step 1: Export Current Configuration**
1. Before making changes, export existing tools
2. In Context Forge: **Export** → **All Tools**
3. Save as `refund-api-backup-YYYYMMDD.json`

**Step 2: Use Git for Bulk Import File**
```bash
git add refund-api-bulk-import.json
git commit -m "Update MCP tool configurations"
git push
```

**Step 3: Document Changes**
- Keep a changelog of tool modifications
- Note which version is deployed
- Track when tools were last updated

---

## Summary

The "APIs already present" error means:
1. ✅ You successfully imported tools before
2. ✅ Context Forge prevents duplicate tool names
3. ✅ You need to delete old tools or rename new ones

**Recommended Solution:**
1. Delete all 11 existing tools in Context Forge
2. Re-import `refund-api-bulk-import.json`
3. Verify all 11 tools are active
4. Test with backend running

**Alternative:**
- Use Option 3 (rename with v2- prefix) if you want to keep old versions
- Use Option 4 (new workspace) for a completely clean start

---

## Next Steps

After successful import:

1. ✅ Start backend API: `cd backend && python main.py`
2. ✅ Test all 11 tools in Context Forge
3. ✅ Deploy MCP server
4. ✅ Connect AI agent
5. ✅ Start using the refund estimation system

---

**Last Updated**: 2026-05-20  
**Issue**: Failed Tools (11) - APIs already present  
**Solution**: Delete existing tools and re-import