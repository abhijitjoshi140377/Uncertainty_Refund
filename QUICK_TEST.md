# Quick Test - Is Backend Running?

## Problem
The test script hangs because **backend is not running**.

---

## Quick Test Method (30 seconds)

### Step 1: Check if Backend is Running

**Open your browser and go to:**
```
http://localhost:8000/api/health
```

**Expected Result:**
- ✅ If you see JSON response: `{"status": "healthy", ...}` → Backend is running
- ❌ If you see "Can't reach this page" or "Connection refused" → Backend is NOT running

---

### Step 2: Start Backend (If Not Running)

**Open a NEW terminal/PowerShell window:**
```powershell
cd C:\Users\AbhijitJoshi\Uncertainty_Refund\backend
python main.py
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Leave this terminal open!** (Backend must keep running)

---

### Step 3: Test in Browser (Easiest Method)

Now open these URLs in your browser:

**Test 1: Health Check**
```
http://localhost:8000/api/health
```
Should show: `{"status": "healthy", ...}`

**Test 2: Get Bookings**
```
http://localhost:8000/api/bookings
```
Should show: `[]` (empty array) or list of bookings

**Test 3: Get Risk Events**
```
http://localhost:8000/api/risk-events?active_only=true
```
Should show: Array of risk events

**Test 4: Get Providers**
```
http://localhost:8000/api/providers
```
Should show: Array of provider policies

**Test 5: Get Statistics**
```
http://localhost:8000/api/statistics/refund-rates
```
Should show: Statistics object

---

### Step 4: Generate Sample Data (If Empty)

If you see empty arrays `[]`, generate sample data:

**In a NEW terminal:**
```powershell
cd C:\Users\AbhijitJoshi\Uncertainty_Refund\backend
python -c "from services.data_generator import generate_sample_data; generate_sample_data()"
```

**Then refresh the browser URLs above** - should now show data.

---

## Alternative: Use Frontend to Test

### Step 1: Start Frontend

**Open a NEW terminal:**
```powershell
cd C:\Users\AbhijitJoshi\Uncertainty_Refund\frontend
npm run dev
```

### Step 2: Open in Browser
```
http://localhost:5173
```

### Step 3: Use the UI
- Click "Bookings" → Should show list
- Click "Create Booking" → Create a test booking
- Click "Analytics" → Should show statistics
- Click "Risk Monitor" → Should show risk events

If the frontend works, your backend (and therefore MCP tools) are working!

---

## Why Test Script Hangs

The Python test script tries to connect to `http://localhost:8000` but:
- ❌ Backend is not running
- ❌ Script waits forever for connection
- ❌ Eventually times out

**Solution:** Start backend FIRST, then run test script.

---

## Correct Order

1. **Terminal 1**: Start backend
   ```powershell
   cd backend
   python main.py
   ```

2. **Terminal 2**: Generate data (optional)
   ```powershell
   cd backend
   python -c "from services.data_generator import generate_sample_data; generate_sample_data()"
   ```

3. **Terminal 3**: Run tests OR use browser
   ```powershell
   python test_mcp_tools.py
   ```
   OR just open `http://localhost:8000/api/health` in browser

---

## Quickest Test (Browser Only)

1. Start backend: `cd backend && python main.py`
2. Open browser: `http://localhost:8000/api/health`
3. If you see JSON → ✅ Working!
4. Open: `http://localhost:8000/api/bookings`
5. If you see `[]` or data → ✅ Working!

**That's it! Your MCP tools will work if these URLs work.**

---

## Summary

**Problem:** Test script hangs  
**Cause:** Backend not running  
**Solution:** Start backend first  
**Quickest Test:** Open `http://localhost:8000/api/health` in browser  

**If browser shows JSON response, your MCP tools are working! ✅**