# IBM Context Forge Authentication Troubleshooting Guide

## Error: "Please check your MCP credentials or login status"

This guide helps resolve authentication issues when importing the bulk configuration file into IBM Context Forge (ICA).

---

## Quick Diagnosis Checklist

Before proceeding, verify:
- [ ] You have an active IBM Cloud account
- [ ] You have access to IBM Context Forge (ICA)
- [ ] You are logged into the IBM Cloud console
- [ ] Your session hasn't expired
- [ ] You have the correct permissions/role

---

## Solution Steps

### Step 1: Verify IBM Cloud Login Status

1. **Check Current Session**
   - Open IBM Cloud Console: https://cloud.ibm.com
   - Look for your account name in top-right corner
   - If logged out, click "Log in" and authenticate

2. **Verify Session is Active**
   - Navigate to any IBM Cloud service
   - If redirected to login page, your session expired
   - Re-authenticate with your credentials

### Step 2: Access IBM Context Forge Correctly

1. **Navigate to Context Forge**
   - From IBM Cloud Dashboard
   - Go to: **Catalog** → **AI / Machine Learning** → **watsonx**
   - Or direct URL: https://dataplatform.cloud.ibm.com/

2. **Verify Context Forge Access**
   - Look for "Context Forge" or "MCP Tools" section
   - If not visible, you may need to:
     - Request access from your IBM account administrator
     - Enable the service in your IBM Cloud account
     - Check if your region supports Context Forge

### Step 3: Check Required Permissions

You need these IBM Cloud IAM roles:
- **Viewer** (minimum) - to view resources
- **Editor** - to import configurations
- **Administrator** - for full access

**To Check Your Permissions:**

1. **Go to IBM Cloud Console**: https://cloud.ibm.com

2. **Navigate to Access Management**:
   - Click **Manage** (top menu bar)
   - Select **Access (IAM)**

3. **Check Your User Permissions**:
   - Click **Users** in left sidebar
   - Find and click your username
   - Click **Access** tab

4. **Look for These Specific Services**:
   
   You need Editor or Administrator role for ONE of these services:
   
   - **watsonx.ai** - IBM's AI platform (most likely for Context Forge)
   - **Watson Studio** - Data science and ML platform
   - **Watson Machine Learning** - ML model deployment
   - **Cloud Pak for Data** - Integrated data and AI platform
   - **Context Forge** - If listed as a separate service
   
   **How to Identify the Right Service:**
   - Look at the "Service" column in your access policies table
   - Find entries containing "watson" or "watsonx"
   - Check if you have "Editor" or "Administrator" in the "Role" column
   - Verify "Resource" shows "All resources" or specific Context Forge instance

5. **Example of Correct Access**:
   ```
   Service: watsonx.ai
   Role: Editor
   Resource: All resources
   Status: Active
   ```

**If Missing Permissions:**

1. **Identify Your Account Owner**:
   - Click **Manage** → **Account**
   - Look for "Account owner" or "Account administrators"
   - Note their email address

2. **Request Access**:
   - Email the account owner
   - Subject: "Request Editor Access for watsonx.ai"
   - Message: "I need Editor role for watsonx.ai service to import MCP tools into Context Forge"
   - Include your IBM Cloud user ID

3. **Alternative - Check Resource Groups**:
   - You might have access to specific resource groups only
   - In IAM, check **Resource groups** tab
   - Ensure Context Forge instance is in a resource group you can access
   - If not, request access to that resource group

4. **Wait for Approval and Re-login**:
   - Account owner must grant access through IAM
   - You'll receive email notification when approved
   - Log out completely from IBM Cloud
   - Clear browser cache
   - Log back in
   - Try importing the bulk file again

### Step 4: Refresh Authentication Token

1. **Clear Browser Cache**
   ```
   Chrome: Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)
   Firefox: Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)
   Edge: Ctrl+Shift+Delete
   ```
   - Select "Cookies and other site data"
   - Select "Cached images and files"
   - Click "Clear data"

2. **Log Out Completely**
   - Click your profile icon (top-right)
   - Select "Log out"
   - Close all IBM Cloud browser tabs

3. **Log Back In**
   - Open new browser tab
   - Go to https://cloud.ibm.com
   - Click "Log in"
   - Enter credentials
   - Complete any 2FA if required

4. **Navigate Back to Context Forge**
   - Go to watsonx → Context Forge
   - Try importing the bulk file again

### Step 5: Verify Bulk Import File Format

The authentication error might actually be a file format issue. Verify:

1. **Check File Encoding**
   - File must be UTF-8 encoded
   - No BOM (Byte Order Mark)
   
   **To verify in VS Code:**
   - Open `refund-api-bulk-import.json`
   - Look at bottom-right status bar
   - Should show "UTF-8"
   - If not, click encoding → "Save with Encoding" → "UTF-8"

2. **Validate JSON Syntax**
   ```bash
   # Using Python
   python -m json.tool refund-api-bulk-import.json
   
   # Using Node.js
   node -e "JSON.parse(require('fs').readFileSync('refund-api-bulk-import.json'))"
   ```

3. **Check File Size**
   - Current file: ~12.1 KB
   - Maximum allowed: Usually 10-50 MB
   - Should be fine, but verify Context Forge limits

### Step 6: Try Alternative Import Methods

If bulk import continues to fail, try these alternatives:

#### Method A: Import One Endpoint at a Time

1. **Extract Single Endpoint**
   - Open `refund-api-bulk-import.json`
   - Copy one endpoint object (e.g., create-booking)
   - Save as `single-endpoint.json`:
   ```json
   {
     "name": "create-booking",
     "displayName": "Create Travel Booking",
     "url": "http://localhost:8000/api/bookings",
     "integration_type": "REST",
     "request_type": "POST",
     ...
   }
   ```

2. **Import Single File**
   - In Context Forge, click "Add Tool" or "Import"
   - Select "Single Import" (not bulk)
   - Upload `single-endpoint.json`
   - Repeat for each of the 11 endpoints

#### Method B: Manual Configuration

1. **Create Tool Manually**
   - In Context Forge, click "Create New Tool"
   - Fill in details from bulk import file:
     - Name: `create-booking`
     - Display Name: `Create Travel Booking`
     - URL: `http://localhost:8000/api/bookings`
     - Method: `POST`
     - Headers: `Content-Type: application/json`

2. **Add Input Schema**
   - Copy the `input_schema` section from bulk file
   - Paste into Context Forge schema editor
   - Validate and save

3. **Repeat for All 11 Endpoints**

#### Method C: Use API to Import

If Context Forge has an API, use it programmatically:

```python
import requests
import json

# Load bulk import file
with open('refund-api-bulk-import.json', 'r') as f:
    endpoints = json.load(f)

# IBM Context Forge API endpoint (replace with actual)
api_url = "https://api.dataplatform.cloud.ibm.com/v2/context-forge/tools"

# Your IBM Cloud API key
headers = {
    "Authorization": f"Bearer {YOUR_IBM_CLOUD_API_KEY}",
    "Content-Type": "application/json"
}

# Import each endpoint
for endpoint in endpoints:
    response = requests.post(api_url, json=endpoint, headers=headers)
    print(f"Imported {endpoint['name']}: {response.status_code}")
```

### Step 7: Contact IBM Support

If none of the above works:

1. **Gather Information**
   - IBM Cloud account ID
   - Context Forge service instance ID
   - Exact error message and timestamp
   - Screenshot of error
   - Browser and version
   - Steps you've already tried

2. **Open Support Ticket**
   - Go to IBM Cloud Console
   - Click **Support** → **Create a case**
   - Select **watsonx** or **Context Forge**
   - Describe the authentication issue
   - Attach `refund-api-bulk-import.json`

3. **Alternative Support Channels**
   - IBM Cloud Community: https://community.ibm.com/
   - Stack Overflow: Tag with `ibm-cloud` and `watsonx`
   - IBM Developer Forums

---

## Common Authentication Issues and Solutions

### Issue 1: Session Timeout
**Symptom**: Was working, now getting auth error  
**Solution**: Log out and log back in

### Issue 2: Wrong IBM Cloud Account
**Symptom**: Can't see Context Forge service  
**Solution**: Switch to correct account in top-right dropdown

### Issue 3: Service Not Provisioned
**Symptom**: Context Forge not available  
**Solution**: Provision watsonx service in IBM Cloud Catalog

### Issue 4: Regional Restrictions
**Symptom**: Service available but can't import  
**Solution**: Check if your region supports Context Forge, try different region

### Issue 5: Browser Compatibility
**Symptom**: Import button doesn't work  
**Solution**: Try different browser (Chrome, Firefox, Edge)

### Issue 6: Corporate Firewall/Proxy
**Symptom**: Connection issues  
**Solution**: Check with IT, may need to whitelist IBM Cloud domains

### Issue 7: API Key Expired
**Symptom**: Authentication fails  
**Solution**: Generate new API key in IBM Cloud IAM

---

## Verification Steps After Fixing Auth

Once authentication is working:

1. **Test Import**
   - Try importing a single endpoint first
   - Verify it appears in Context Forge
   - Test the endpoint with sample data

2. **Import Full Bulk File**
   - Upload `refund-api-bulk-import.json`
   - Verify all 11 endpoints imported
   - Check each endpoint configuration

3. **Test Endpoints**
   - Use Context Forge's test feature
   - Send sample requests to each endpoint
   - Verify responses are correct

4. **Deploy MCP Server**
   - Follow deployment steps in Context Forge
   - Note the MCP server URL
   - Test with AI agent

---

## Alternative: Use Native MCP Server

If IBM Context Forge authentication continues to be problematic, you can use the native MCP server approach:

### Quick Start with Native MCP Server

1. **Install Dependencies**
   ```bash
   pip install mcp==1.1.2 requests==2.31.0
   ```

2. **Start Backend API**
   ```bash
   cd backend
   python main.py
   ```

3. **Run MCP Server**
   ```bash
   cd backend
   python mcp_server_http.py
   ```

4. **Test MCP Endpoint**
   ```bash
   curl -X POST http://localhost:8001/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
   ```

See `MCP_SERVER_SETUP_GUIDE.md` for complete instructions.

---

## Preventive Measures

To avoid authentication issues in the future:

1. **Keep Session Active**
   - Don't let IBM Cloud session timeout
   - Refresh page periodically
   - Use "Remember me" option

2. **Use API Keys**
   - Generate IBM Cloud API key
   - Store securely
   - Use for programmatic access

3. **Bookmark Direct URLs**
   - Save Context Forge URL
   - Avoid navigating through multiple pages

4. **Regular Access**
   - Log in regularly to keep account active
   - Complete any required security updates

5. **Monitor Service Status**
   - Check IBM Cloud status page
   - Subscribe to service notifications

---

## Additional Resources

- **IBM Cloud Documentation**: https://cloud.ibm.com/docs
- **watsonx Documentation**: https://www.ibm.com/docs/en/watsonx
- **IBM Cloud Status**: https://cloud.ibm.com/status
- **IBM Support**: https://www.ibm.com/mysupport
- **Community Forums**: https://community.ibm.com/

---

## Summary

The "Please check your MCP credentials or login status" error is typically caused by:
1. Expired session → Log out and log back in
2. Missing permissions → Request Editor role
3. Service not provisioned → Enable watsonx in IBM Cloud
4. Browser cache → Clear cache and cookies
5. File format issue → Validate JSON syntax

Follow the steps above in order, and you should be able to successfully import the bulk configuration file.

If all else fails, use the native MCP server approach as a reliable alternative.

---

**Last Updated**: 2026-05-20  
**Version**: 1.0  
**For**: IBM Context Forge (ICA) Authentication Issues