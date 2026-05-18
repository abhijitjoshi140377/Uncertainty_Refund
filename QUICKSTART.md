# Quick Start Guide

Get the Travel Refund Uncertainty Estimation System running in 5 minutes!

## Prerequisites Check

Before starting, verify you have:

```bash
# Check Python version (need 3.9+)
python --version

# Check Node.js version (need 16.0+)
node --version

# Check npm version (need 8.0+)
npm --version
```

If any are missing, install them first:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

## Installation (One-Time Setup)

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Frontend Setup (2 minutes)

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Option 1: Using Startup Scripts (Easiest)

**Windows - Batch File:**
```bash
# Double-click start.bat or run:
start.bat
```

**Windows - PowerShell:**
```bash
# Right-click start.ps1 -> Run with PowerShell or:
.\start.ps1
```

### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access the Application

Once both servers are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

## First Steps

1. **Open the application** at http://localhost:3000
2. **Explore the Dashboard** - View sample bookings and statistics
3. **Create a booking**:
   - Click "Create New Booking"
   - Fill in the form
   - Submit
4. **Generate estimate**:
   - Open the booking you created
   - Click "Generate Estimate"
   - View the refund prediction

## What Happens on First Run?

The system automatically:
- ✅ Creates SQLite database
- ✅ Generates 500 historical refund records
- ✅ Creates 50 sample bookings
- ✅ Populates provider policies
- ✅ Trains ML models

This takes about 10-15 seconds on first startup.

## Common Issues & Solutions

### Backend won't start

**Issue**: `ModuleNotFoundError`
```bash
cd backend
pip install -r requirements.txt
```

**Issue**: Port 8000 in use
```bash
# Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Frontend won't start

**Issue**: Dependencies not installed
```bash
cd frontend
npm install
```

**Issue**: Port 3000 in use
- Vite will automatically use next available port (3001, 3002, etc.)

### Can't connect to backend

1. Ensure backend is running (check Terminal 1)
2. Check http://localhost:8000/api/health
3. Restart backend if needed

## Testing the System

### Quick Test

1. Go to http://localhost:3000
2. Click "Create New Booking"
3. Fill form with:
   - Name: Test User
   - Email: test@example.com
   - Origin: Mumbai
   - Destination: Paris
   - Travel Date: 60 days from today
   - Flight Cost: 50000
   - Hotel Cost: 25000
4. Submit and view booking
5. Click "Generate Estimate"
6. Verify estimate appears with refund amount

### Expected Result

- Booking created successfully
- Estimate shows:
  - Expected refund amount
  - Confidence interval
  - Risk level
  - Scenario analysis

## Next Steps

- 📖 Read full [README.md](README.md) for detailed documentation
- 🧪 Check [TESTING.md](TESTING.md) for testing guide
- 🔍 Explore API at http://localhost:8000/api/docs
- 📊 View Analytics page for historical data
- ⚠️ Check Risk Monitor for global events

## Stopping the Application

### If using startup scripts:
- Close the terminal windows

### If running manually:
- Press `Ctrl+C` in each terminal

## Restarting

Just run the startup script again or restart both servers manually.

## Need Help?

- Check [README.md](README.md) for full documentation
- Check [TESTING.md](TESTING.md) for troubleshooting
- Review API docs at http://localhost:8000/api/docs

---

**Ready to start?** Run `start.bat` (Windows) and open http://localhost:3000!