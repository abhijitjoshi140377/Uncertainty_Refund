# Complete Setup with ngrok for IBM ICA Context Forge

## Why ngrok is Needed

You're absolutely right! **ngrok IS required** for IBM ICA Context Forge to access your local backend.

### The Problem:
- Your backend runs on `http://localhost:8000` (your computer only)
- IBM ICA Context Forge runs in the cloud (IBM's servers)
- ICA cannot access `localhost:8000` because it's not on your computer
- **Solution:** ngrok creates a public URL that tunnels to your localhost

### Without ngrok:
```
ICA Context Forge (Cloud) → http://localhost:8000 ❌ Cannot reach
```

### With ngrok:
```
ICA Context Forge (Cloud) → https://abc123.ngrok.io → localhost:8000 ✅ Works!
```

---

## Complete Setup Steps

### Step 1: Start Backend

**Terminal 1:**
```powershell
cd C:\Users\AbhijitJoshi\Uncertainty_Refund\backend
python main.py
```

**Wait for:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

---

### Step 2: Start ngrok

**Terminal 2:**
```powershell
ngrok http 8000
```

**You'll see output like:**
```
ngrok

Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123-xyz.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy the Forwarding URL:** `https://abc123-xyz.ngrok-free.app`

**Keep this terminal open!**

---

### Step 3: Test ngrok URL

**Open browser:**
```
https://abc123-xyz.ngrok-free.app/api/health
```

**Expected Result:**
```json
{
  "status": "healthy",
  "service": "refund-estimation-api",
  "timestamp": "2026-05-20T15:00:00Z"
}
```

✅ If you see this, ngrok is working!

---

### Step 4: Update Bulk Import File with ngrok URL

Now we need to update the bulk import file to use the ngrok URL instead of localhost.

**Create new file: `refund-api-bulk-import-ngrok.json`**

I'll create a script to do this automatically:

**File: `update_urls_for_ngrok.py`**
```python
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python update_urls_for_ngrok.py <ngrok-url>")
    print("Example: python update_urls_for_ngrok.py https://abc123-xyz.ngrok-free.app")
    sys.exit(1)

ngrok_url = sys.argv[1].rstrip('/')

# Read the v2 bulk import file
with open('refund-api-bulk-import-v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update all URLs
for tool in data:
    tool['url'] = tool['url'].replace('http://localhost:8000', ngrok_url)

# Write to new file
with open('refund-api-bulk-import-ngrok.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"SUCCESS: Created refund-api-bulk-import-ngrok.json")
print(f"All URLs updated to use: {ngrok_url}")
print(f"\nUpdated {len(data)} tools:")
for tool in data:
    print(f"  - {tool['name']}: {tool['url']}")
```

**Run the script:**
```powershell
python update_urls_for_ngrok.py https://abc123-xyz.ngrok-free.app
```

Replace `https://abc123-xyz.ngrok-free.app` with YOUR actual ngrok URL!

---

### Step 5: Delete Old Tools in ICA (If Possible)

If ICA allows deleting tools:
1. Go to ICA Context Forge
2. Delete all v2- tools (if possible)

If not possible, we'll import with new names.

---

### Step 6: Import New Bulk File with ngrok URLs

**In ICA Context Forge:**
1. Click **Import** → **Bulk Import**
2. Upload `refund-api-bulk-import-ngrok.json`
3. All 11 tools should import successfully
4. Tools will now use ngrok URLs

---

### Step 7: Test in ICA

Now ICA can reach your backend through ngrok!

**In ICA Context Forge:**
1. Find any tool (e.g., v2-get-bookings)
2. If there's a way to test/invoke it, try it
3. Should work now because ICA can reach ngrok URL

---

## Important ngrok Notes

### ngrok URL Changes on Restart

**Problem:** Every time you restart ngrok, you get a NEW URL:
- First run: `https://abc123.ngrok-free.app`
- Second run: `https://xyz789.ngrok-free.app` (different!)

**Solution Options:**

#### Option A: Use ngrok Free Tier (URL changes)
- Restart ngrok when needed
- Update bulk import file with new URL
- Re-import into ICA
- Good for testing

#### Option B: Use ngrok Paid Plan (Static URL)
- Get a static domain: `https://your-name.ngrok.io`
- URL never changes
- No need to update bulk import file
- Good for production

#### Option C: Deploy to Cloud
- Deploy backend to Heroku, AWS, Azure, etc.
- Get permanent URL: `https://your-app.herokuapp.com`
- No ngrok needed
- Best for production

---

## Complete Workflow

### For Testing (Free ngrok):

**Terminal 1: Backend**
```powershell
cd backend
python main.py
```

**Terminal 2: ngrok**
```powershell
ngrok http 8000
```

**Terminal 3: Update URLs**
```powershell
python update_urls_for_ngrok.py https://YOUR-NGROK-URL
```

**Browser: Import to ICA**
1. Upload `refund-api-bulk-import-ngrok.json`
2. Test tools in ICA

**Keep Terminals 1 & 2 running!**

---

### For Production (Paid ngrok or Cloud):

**Option 1: ngrok Static Domain ($8/month)**
1. Sign up: https://ngrok.com/pricing
2. Get static domain: `https://your-name.ngrok.io`
3. Run: `ngrok http 8000 --domain=your-name.ngrok.io`
4. Update bulk import once
5. Never changes!

**Option 2: Deploy to Cloud (Free tier available)**
1. Deploy backend to Heroku/Railway/Render
2. Get permanent URL
3. Update bulk import once
4. No ngrok needed!

---

## Why We Need Both Terminals Running

```
Terminal 1: Backend (python main.py)
    ↓
    Runs on localhost:8000
    ↓
Terminal 2: ngrok (ngrok http 8000)
    ↓
    Creates tunnel: ngrok URL → localhost:8000
    ↓
ICA Context Forge (Cloud)
    ↓
    Calls ngrok URL
    ↓
    ngrok forwards to localhost:8000
    ↓
    Backend responds
    ↓
    Response goes back through ngrok to ICA
```

**Both must be running for ICA to work!**

---

## Testing Checklist

- [ ] Terminal 1: Backend running (`python main.py`)
- [ ] Terminal 2: ngrok running (`ngrok http 8000`)
- [ ] Browser: ngrok URL works (`https://YOUR-URL/api/health`)
- [ ] Script: Updated bulk import file with ngrok URL
- [ ] ICA: Imported new bulk file
- [ ] ICA: Tools show ngrok URLs (not localhost)
- [ ] ICA: Tools can be invoked successfully

---

## Troubleshooting

### Issue 1: ngrok Shows "Tunnel Not Found"
**Cause:** Free ngrok has request limits  
**Solution:** Wait a moment or upgrade to paid plan

### Issue 2: ICA Still Can't Reach Backend
**Cause:** ngrok not running or wrong URL  
**Solution:** 
1. Check Terminal 2 - ngrok must be running
2. Verify ngrok URL in bulk import file
3. Test ngrok URL in browser first

### Issue 3: ngrok URL Changed
**Cause:** Restarted ngrok  
**Solution:**
1. Get new ngrok URL
2. Run update script with new URL
3. Re-import bulk file to ICA

### Issue 4: "Failed to Connect" in ICA
**Cause:** Backend not running  
**Solution:** Check Terminal 1 - backend must be running

---

## Summary

**You were RIGHT to ask about ngrok!** It's essential for ICA to access your local backend.

**Complete Setup:**
1. ✅ Start backend (Terminal 1)
2. ✅ Start ngrok (Terminal 2)
3. ✅ Update bulk import with ngrok URL
4. ✅ Import to ICA
5. ✅ Test tools in ICA

**Both terminals must stay open while using ICA!**

---

**Last Updated**: 2026-05-20  
**Critical**: ngrok is REQUIRED for ICA to access localhost  
**Next**: Create update script and import with ngrok URLs